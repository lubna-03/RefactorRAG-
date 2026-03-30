from tax_calculator import TaxCalculator
from payment_gateway_adapter import PaymentGatewayAdapter
from reporting_service import ReportingService
from exceptions import PaymentGatewayError, ReportStorageError
import uuid

class CheckoutService:
    def __init__(self, tax_calculator: TaxCalculator, payment_gateway: PaymentGatewayAdapter, reporting_service: ReportingService):
        self.tax_calculator = tax_calculator
        self.payment_gateway = payment_gateway
        self.reporting_service = reporting_service

    def process_checkout(self, user_id: str, amount: float, item_category: str) -> dict:
        transaction_id = str(uuid.uuid4())
        try:
            # 1. Calculate Tax
            total_amount_with_tax = self.tax_calculator.calculate_total_with_tax(amount, item_category)
            print(f"DEBUG: Calculated total for {amount} ({item_category}) with tax: {total_amount_with_tax}")

            # 2. Process Payment
            payment_result = self.payment_gateway.charge_payment(total_amount_with_tax, transaction_id)
            if payment_result.get('status') != 'success':
                raise PaymentGatewayError("Payment was not successful.")
            print(f"DEBUG: Payment successful. Gateway Ref: {payment_result.get('gateway_ref_id')}")

            # 3. Store Report
            transaction_details = {
                "transaction_id": transaction_id,
                "user_id": user_id,
                "original_amount": amount,
                "item_category": item_category,
                "total_charged_usd": total_amount_with_tax,
                "total_charged_cents": payment_result.get('amount_charged_cents'),
                "payment_gateway_ref_id": payment_result.get('gateway_ref_id'),
                "timestamp": datetime.datetime.now().isoformat()
            }
            report_stored = self.reporting_service.store_transaction_report(transaction_details)
            if not report_stored:
                # Decide how critical report storage failure is.
                # For now, we'll log and continue, but a real system might roll back or alert.
                print("WARNING: Transaction report could not be stored, but payment was successful.")

            return {
                'status': 'success',
                'message': 'Checkout processed successfully',
                'total_charged_usd': total_amount_with_tax,
                'gateway_ref_id': payment_result.get('gateway_ref_id'),
                'transaction_id': transaction_id
            }

        except PaymentGatewayError as e:
            print(f"ERROR: Checkout failed due to payment issue: {e}")
            return {'status': 'failed', 'message': f'Payment failed: {e}'}
        except ReportStorageError as e:
            print(f"ERROR: Checkout completed but report storage failed: {e}")
            # Depending on business rules, this might still be a 'success' for the user,
            # but an internal 'warning' or 'partial_success'.
            return {'status': 'partial_success', 'message': f'Checkout successful, but report storage failed: {e}'}
        except Exception as e:
            print(f"ERROR: An unexpected error occurred during checkout: {e}")
            return {'status': 'failed', 'message': f'An unexpected error occurred: {e}'}
