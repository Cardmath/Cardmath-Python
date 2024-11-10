import stripe
from pydantic import BaseModel
from enum import Enum
from database.auth.user import User
import os 
from dotenv import load_dotenv


class Product(str, Enum):
    unlimited = 'unlimited'
    limited = 'limited'
    free = 'free'

class CheckoutSessionRequest(BaseModel):    
    product: Product

class CheckoutSessionResponse(BaseModel):
    url: str

def create_checkout_session(current_user: User, request: CheckoutSessionRequest) -> CheckoutSessionResponse:
    load_dotenv()
    stripe.api_key = os.getenv('STRIPE_API_KEY', "your_stripe_api_key")
    session = stripe.checkout.Session.create(line_items
            =[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': 'Cardmath Unlimited',
                    },
                    'unit_amount': 5999,
                },
                'quantity': 1,
                }],
                mode='payment',
                success_url='https://cardmath.ai/dashboard',
                cancel_url='https://cardmath.ai/dashboard',
            )

    return CheckoutSessionResponse(url=session.url)