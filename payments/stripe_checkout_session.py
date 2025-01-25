from database.auth.crud import create_or_update_subscription
from database.auth.user import User
from dotenv import load_dotenv
from enum import Enum
from fastapi import HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

import logging
import os
import stripe
import stripe.error
import sys  # Added for logging configuration

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Product(str, Enum):
    annual = 'annual'
    monthly = 'monthly'
    beta = 'beta'

class CheckoutSessionRequest(BaseModel):    
    product: Product

class CheckoutSessionIDRequest(BaseModel):
    session_id: str

class CheckoutSessionResponse(BaseModel):
    url: str

# TEST MODE PRODUCT IDs
PRODUCTS = {
    Product.annual: 'prod_RCpGRQtRhol743',
    Product.monthly: 'prod_RCpGPTdB4yqw8w',
    Product.beta: 'prod_Re9Y6zUeeTjeC7'
}

def create_checkout_session(db: Session, current_user: User, request: CheckoutSessionRequest) -> CheckoutSessionResponse:
    product_id = PRODUCTS[request.product]
    prices = stripe.Price.list(product=product_id, active=True)
    logger.info(f"Active prices for product {product_id}: {prices.data}")
    
    if prices.data:
        price_id = prices.data[0].id
    else:
        logger.error(f"No active price found for product {product_id}")
        raise HTTPException(status_code=400, detail="No active price found for the selected product.")

    session = stripe.checkout.Session.create(
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=f'http://localhost:3000/dashboard',
        cancel_url='http://localhost:3000/',
        customer_email=current_user.email,  # Ensure you are using the email attribute
        allow_promotion_codes=True
    )

    return CheckoutSessionResponse(url=session.url)

async def stripe_webhook(request: Request, db: Session):
    payload = await request.body()
    sig_header = request.headers.get('Stripe-Signature')
    secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    
    if not secret:
        logger.error("Stripe webhook secret is not set in the environment variables.")
        raise HTTPException(status_code=500, detail="Webhook secret not configured.")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, secret
        )
    except ValueError:
        logger.error("Invalid payload in Stripe webhook")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid signature in Stripe webhook")
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_id = session.get('customer')
        session_id = session['id']
        logger.info(f"Stripe webhook called for session ID: {session_id} and customer ID: {customer_id}")

        # Retrieve the customer email from Stripe
        if customer_id:
            customer = stripe.Customer.retrieve(customer_id)
            customer_email = customer.get('email')
        else:
            logger.error(f"No customer ID found in session ID: {session_id}")
            raise HTTPException(status_code=400, detail="No customer ID found in the session.")

        if not customer_email:
            logger.error(f"No customer email found for customer ID: {customer_id}")
            raise HTTPException(status_code=400, detail="No customer email found for the customer.")

        # Retrieve line items
        try:
            line_items = stripe.checkout.Session.list_line_items(session_id)
            if not line_items['data']:
                logger.error(f"No line items found for session ID: {session_id}")
                raise HTTPException(status_code=400, detail="No line items found in the session.")
            product_id = line_items['data'][0]['price']['product']
        except Exception as e:
            logger.error(f"Error retrieving line items for session ID {session_id}: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving line items.")

        # Query the user using the email
        user: User = db.query(User).filter(User.email == customer_email).first()
        if user:
            logger.info(f"User found: {user.username} with email: {user.email}")
        else:
            logger.error(f"No user found with email: {customer_email}")
            raise HTTPException(status_code=500, detail="We could not find your account. Please contact support at support@cardmath.ai.")

        logger.info(f"Product purchased: {product_id}")
        try:
            if product_id == PRODUCTS[Product.annual]:
                create_or_update_subscription(db, user_id=user.id, status="annual", duration_days=365, computations=None)
                db.commit()  # Ensure the database session is committed
                logger.info(f"Annual subscription created for user {user.username}")
            elif product_id == PRODUCTS[Product.monthly]:
                create_or_update_subscription(db, user_id=user.id, status="monthly", duration_days=30, computations=None)
                db.commit()  # Ensure the database session is committed
                logger.info(f"Monthly subscription created for user {user.username}")
            else:
                logger.error(f"Stripe webhook called with unknown product ID: {product_id}")
                raise HTTPException(status_code=400, detail="Unknown product ID in the session.")
        except Exception as e:
            logger.error(f"Error updating subscription for user {user.username}: {e}")
            raise HTTPException(status_code=500, detail="Error updating subscription.")
    else:
        logger.info(f"Unhandled event type: {event['type']}")

    return {"status": "success"}

def get_checkout_session(request: CheckoutSessionIDRequest):
    try:
        session = stripe.checkout.Session.retrieve(request.session_id)
        payment_status = session.payment_status  # 'paid', 'unpaid', or 'no_payment_required'
        
        return {
            "payment_status": payment_status
        }
    except Exception as e:
        logger.error(f"Error retrieving checkout session: {e}")
        raise HTTPException(status_code=500, detail=str(e))
