import datetime
from auth_service import AuthService
from tax_calculator import TaxCalculator
from payment_gateway_adapter import PaymentGatewayAdapter
from reporting_service import ReportingService
from checkout_service import CheckoutService
from config import (
    AUTH_TOKEN_SECRET, STANDARD_TAX_RATE, ELECTRONICS_TAX_RATE,
    PAYMENT_GATEWAY_API_URL, PAYMENT_GATEWAY_API_KEY, S3_REPORT_BUCKET_NAME
)
from exceptions import UnauthorizedError, BadRequestError, PaymentGatewayError, ReportStorageError

def main_application_handler(action: str, auth_token: str, user_role: str, amount: float, item_cat: str) -> str:
    # 1. Initialize Services
    auth_service = AuthService(secret_token=AUTH_TOKEN_SECRET)
    tax_calculator = TaxCalculator(standard_rate=STANDARD_TAX_RATE, electronics_rate=ELECTRONICS_TAX_RATE)
    payment_gateway = PaymentGatewayAdapter(api_url=PAYMENT_GATEWAY_API_URL, api_key=PAYMENT_GATEWAY_API_KEY)
    reporting_service = ReportingService(s3_bucket_name=S3_REPORT_BUCKET_NAME)
    checkout_service = CheckoutService(
        tax_calculator=tax_calculator,
        payment_gateway=payment_gateway,
        reporting_service=reporting_service
    )

    try:
        # 2. Authentication
        auth_service.authenticate(auth_token)
        print(f"DEBUG: Authentication successful for token: {auth_token}")

        # 3. Action Routing
        if action == "checkout":
            # For simplicity, user_id is user_role here. In a real app, it would be a distinct ID.
            checkout_result = checkout_service.process_checkout(user_id=user_role, amount=amount, item_category=item_cat)
            if checkout_result['status'] == 'success':
                return f"200 OK - {checkout_result['message']} - Total Charged: ${checkout_result['total_charged_usd']:.2f} (Ref: {checkout_result['gateway_ref_id']})"
            elif checkout_result['status'] == 'partial_success':
                 return f"200 OK - {checkout_result['message']} - Total Charged: ${checkout_result.get('total_charged_usd', 'N/A'):.2f}"
            else:
                return f"400 Bad Request - {checkout_result['message']}"
        else:
            raise BadRequestError(f"Unknown action: {action}")

    except UnauthorizedError as e:
        return f"401 Unauthorized - {e}"
    except BadRequestError as e:
        return f"400 Bad Request - {e}"
    except PaymentGatewayError as e:
        return f"500 Internal Server Error - Payment Gateway Error: {e}"
    except ReportStorageError as e:
        return f"500 Internal Server Error - Report Storage Error: {e}"
    except Exception as e:
        return f"500 Internal Server Error - An unexpected error occurred: {e}"

if __name__ == "__main__":
    print("--- Simulating a successful electronics checkout ---")
    result_electronics = main_application_handler("checkout", "super_secret", "premium_user", 100, "electronics")
    print(result_electronics)
    print("\n" + "="*50 + "\n")

    print("--- Simulating a successful general product checkout ---")
    result_general = main_application_handler("checkout", "super_secret", "guest", 50, "books")
    print(result_general)
    print("\n" + "="*50 + "\n")

    print("--- Simulating an unauthorized request ---")
    result_unauthorized = main_application_handler("checkout", "wrong_secret", "user", 100, "electronics")
    print(result_unauthorized)
    print("\n" + "="*50 + "\n")

    print("--- Simulating an unknown action ---")
    result_unknown_action = main_application_handler("refund", "super_secret", "user", 100, "electronics")
    print(result_unknown_action)
    print("\n" + "="*50 + "\n")

    print("--- Simulating a payment failure (e.g., amount <= 0) ---")
    result_payment_fail = main_application_handler("checkout", "super_secret", "user", -10, "general")
    print(result_payment_fail)
    print("\n" + "="*50 + "\n")

    # To test ReportStorageError, you might need to temporarily break S3 client initialization
    # or mock the boto3 client to raise an exception. For this exercise, the simulation
    # will just print a warning if S3 client fails to initialize.
    print("--- Simulating a checkout where report storage might fail (if S3 client fails to init) ---")
    result_report_fail = main_application_handler("checkout", "super_secret", "admin", 200, "software")
    print(result_report_fail)
    print("\n" + "="*50 + "\n")