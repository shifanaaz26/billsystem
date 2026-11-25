import pytest

# Simple Billing System classes to test
class BillingSystem:
    def __init__(self, currency="USD"):
        self.items = []
        self.currency = currency

    def add_item(self, name, price, quantity=1):
        if price < 0 or quantity <= 0:
            raise ValueError("Price and quantity must be positive values.")
        self.items.append({"name": name, "price": price, "quantity": quantity})

    def calculate_subtotal(self):
        return sum(item["price"] * item["quantity"] for item in self.items)

    def calculate_total(self, discount_percentage=0, tax_percentage=0):
        subtotal = self.calculate_subtotal()
        discount_amount = subtotal * (discount_percentage / 100)
        taxable_amount = subtotal - discount_amount
        tax_amount = taxable_amount * (tax_percentage / 100)
        return round(taxable_amount + tax_amount, 2)


# --- PYTEST FIXTURE ---
@pytest.fixture
def empty_cart():
    """Provides a fresh, empty billing instance for each test."""
    return BillingSystem()


@pytest.fixture
def loaded_cart():
    """Provides a billing instance pre-loaded with standard retail items."""
    cart = BillingSystem()
    cart.add_item("Laptop", 1000.00, 1)
    cart.add_item("Mouse", 50.00, 2)  # Subtotal: 1100.00
    return cart


# --- TEST CASES ---

class TestBillingCalculations:
    
    def test_empty_cart_total(self, empty_cart):
        """Verifies that an empty cart totals zero."""
        assert empty_cart.calculate_subtotal() == 0.00
        assert empty_cart.calculate_total() == 0.00

    def test_add_item_increases_count(self, empty_cart):
        """Validates that adding items populates the system records correctly."""
        empty_cart.add_item("Keyboard", 75.00)
        assert len(empty_cart.items) == 1
        assert empty_cart.items[0]["name"] == "Keyboard"

    def test_subtotal_calculation(self, loaded_cart):
        """Ensures subtotal accounts for prices multiplied by their item quantities."""
        assert loaded_cart.calculate_subtotal() == 1100.00

    def test_total_with_tax(self, loaded_cart):
        """Verifies that flat percentage taxes apply properly to the subtotal."""
        # 1100 + 10% tax = 1210
        assert loaded_cart.calculate_total(tax_percentage=10) == 1210.00


# --- PARAMETRIZED DISCOUNTS ---
@pytest.mark.parametrize("discount, tax, expected_total", [
    (10, 0, 990.00),   # 1100 - 10% discount = 990
    (0, 5, 1155.00),   # 1100 + 5% tax = 1155
    (20, 10, 968.00),  # (1100 - 20%) + 10% tax = 880 + 88 = 968
])
def test_various_billing_combos(loaded_cart, discount, tax, expected_total):
    """Tests multiple combinations of discount percentages and taxes sequentially."""
    assert loaded_cart.calculate_total(discount, tax) == expected_total


# --- EXCEPTION HANDLING ---
class TestBillingErrors:

    def test_negative_price_raises_error(self, empty_cart):
        """Ensures system rejects negative billing amounts or price values."""
        with pytest.raises(ValueError, match="Price and quantity must be positive values."):
            empty_cart.add_item("Faulty Item", -10.00, 1)

    def test_zero_quantity_raises_error(self, empty_cart):
        """Ensures system prevents adding non-existent quantities to an invoice."""
        with pytest.raises(ValueError, match="Price and quantity must be positive values."):
            empty_cart.add_item("Coffee Mug", 15.00, 0)
