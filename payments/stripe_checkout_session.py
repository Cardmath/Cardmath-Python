import stripe
from fastapi import Depends, HTTPException, Request
from pydantic import BaseModel
from enum import Enum

import stripe.error
from database.auth.user import User, Subscription
from database.auth.crud import create_subscription, update_subscription_status
import os
import auth.utils as auth_utils
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from datetime import timedelta

class Product(str, Enum):
    unlimited = 'unlimited'
    limited = 'limited'
    free = 'free'

class CheckoutSessionRequest(BaseModel):    
    product: Product

class CheckoutSessionResponse(BaseModel):
    url: str

load_dotenv()
stripe.api_key = os.getenv('STRIPE_API_KEY', "your_stripe_api_key")

# TEST MODE PRODUCT ID's
PRODUCTS = {
    Product.unlimited: 'prod_RCpGRQtRhol743',
    Product.limited: 'prod_RCpGPTdB4yqw8w',
    Product.free: None  # Free tier does not require checkout
}

PRODUCT_PRICE_AMOUNTS = {
    Product.free: 0,
    Product.unlimited: 6000,
    Product.limited: 3000
}

def create_checkout_session(db: Session, current_user: User, request: CheckoutSessionRequest) -> CheckoutSessionResponse:
    if request.product == Product.free:
        raise HTTPException(status_code=400, detail="Free tier does not require checkout.")
    
    product_id = PRODUCTS[request.product]
    
    # Retrieve or create the price associated with the product
    prices = stripe.Price.list(product=product_id, active=True)
    
    if prices.data:
        # Use the first available active price
        price_id = prices.data[0].id
    else:
        # Create a price if no active price exists (e.g., if you need a default price setup)
        price = stripe.Price.create(
            unit_amount=PRODUCT_PRICE_AMOUNTS[request.product],
            currency="usd",
            recurring={"interval": "month"},
            product=product_id,
        )
        price_id = price.id
    
    # Create the checkout session with the price ID
    session = stripe.checkout.Session.create(
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url=f'https://cardmath.ai/dashboard',
        cancel_url='https://cardmath.ai/dashboard',
        customer_email=current_user.email  # optional: links customer to Stripe account
    )

    return CheckoutSessionResponse(url=session.url)

async def stripe_webhook(request: Request, db: Session):
    payload = await request.body()
    sig_header = request.headers.get('Stripe-Signature')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET')
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session['customer_email']
        session_id = session['id']
        
        line_items = stripe.checkout.Session.list_line_items(session_id)
        product_id = line_items['data'][0]['price']['product']


        user = db.query(User).filter(User.email == customer_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update or create subscription based on the product purchased
        if product_id == PRODUCTS[Product.unlimited]:
            create_subscription(db, user_id=user.id, status="unlimited", duration_days=365, computations=None)
        elif product_id == PRODUCTS[Product.limited]:
            create_subscription(db, user_id=user.id, status="limited", duration_days=30, computations=10)
    
    return {"status": "success"}

def handle_subscription_upgrade(db: Session, user_id: int, product: Product):
    """
    Handle subscription upgrade based on product type.
    """
    if product == Product.unlimited:
        update_subscription_status(db, user_id=user_id, status="unlimited", computations=None)
    elif product == Product.limited:
        update_subscription_status(db, user_id=user_id, status="limited", computations=10)
