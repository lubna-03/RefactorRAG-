from config import STANDARD_TAX_RATE, ELECTRONICS_TAX_RATE

class TaxCalculator:
    def __init__(self, standard_rate: float, electronics_rate: float):
        self.standard_rate = standard_rate
        self.electronics_rate = electronics_rate

    def calculate_tax(self, amount: float, item_category: str) -> float:
        if item_category.lower() == "electronics":
            return amount * self.electronics_rate
        return amount * self.standard_rate

    def calculate_total_with_tax(self, amount: float, item_category: str) -> float:
        tax_amount = self.calculate_tax(amount, item_category)
        return amount + tax_amount
