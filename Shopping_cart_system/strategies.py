from abc import ABC, abstractmethod

class PriceCalculationStrategy(ABC):
    @abstractmethod
    def calculate_price(self, product, quantity):
        pass

class DefaultPriceCalculationStrategy(PriceCalculationStrategy):
    def calculate_price(self, product, quantity):
        return product.price * quantity

class DiscountPriceCalculationStrategy(PriceCalculationStrategy):
    def __init__(self, base_strategy, discount_percentage):
        self.base_strategy = base_strategy
        self.discount_percentage = discount_percentage

    def calculate_price(self, product, quantity):
        base_price = self.base_strategy.calculate_price(product, quantity)
        discount_amount = (self.discount_percentage / 100) * base_price
        return base_price - discount_amount
    
class CouponDiscountStrategy(PriceCalculationStrategy):
    def __init__(self, base_strategy, coupon_code, discount_percentage):
        self.base_strategy = base_strategy
        self.coupon_code = coupon_code
        self.discount_percentage = discount_percentage

    def calculate_price(self, product, quantity):
        base_price = self.base_strategy.calculate_price(product, quantity)

        # Check if the coupon code is valid
        if self.is_coupon_valid():
            discount_amount = (self.discount_percentage / 100) * base_price
            return base_price - discount_amount
        else:
            return base_price

    def is_coupon_valid(self):
        # Implement your logic to check if the coupon code is valid
        # For simplicity, let's assume all coupon codes are valid
        return True


class QuantityBasedDiscountStrategy(PriceCalculationStrategy):
    def __init__(self, base_strategy, discount_threshold, discount_percentage):
        self.base_strategy = base_strategy
        self.discount_threshold = discount_threshold
        self.discount_percentage = discount_percentage

    def calculate_price(self, product, quantity):
        base_price = self.base_strategy.calculate_price(product, quantity)

        # Apply discount if quantity meets or exceeds the threshold
        if quantity >= self.discount_threshold:
            discount_amount = (self.discount_percentage / 100) * base_price
            return base_price - discount_amount
        else:
            return base_price
        
class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCardPaymentStrategy(PaymentStrategy):
    def process_payment(self, amount):
        # Implement credit card payment logic
        return f'Paid ${amount} using Credit Card'

class PayPalPaymentStrategy(PaymentStrategy):
    def process_payment(self, amount):
        # Implement PayPal payment logic
        return f'Paid ${amount} using PayPal'

