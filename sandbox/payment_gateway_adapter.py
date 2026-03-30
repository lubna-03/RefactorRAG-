import requests
from config import PAYMENT_GATEWAY_API_URL, PAYMENT_GATEWAY_API_KEY
from exceptions import PaymentGatewayError

class PaymentGatewayAdapter:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def charge_payment(self, amount_usd: float, transaction_id: str = None) -> dict:
        amount_cents = int(amount_usd * 100) # Convert to cents as required by business logic

        # Simulate an HTTP POST request to the payment gateway
        # In a real scenario, this would involve actual network calls and error handling
        try:
            # For demonstration, we'll simulate success/failure
            if amount_cents <= 0:
                raise requests.exceptions.RequestException("Invalid amount for payment.")

            # Simulate a successful response
            print(f"DEBUG: Sending {amount_cents} cents to Payment Gateway at {self.api_url} with key {self.api_key}")
            response_data = {
                'status': 'success',
                'gateway_ref_id': f'pg_ref_{transaction_id or "N/A"}_{amount_cents}',
                'amount_charged_cents': amount_cents
            }
            # requests.post(self.api_url, json={'amount': amount_cents, 'api_key': self.api_key, 'transaction_id': transaction_id})
            # response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            # return response.json()
            return response_data
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Payment Gateway communication failed: {e}")
            raise PaymentGatewayError(f"Payment Gateway error: {e}")
        except Exception as e:
            print(f"ERROR: Unexpected error during payment processing: {e}")
            raise PaymentGatewayError(f"Unexpected payment error: {e}")
