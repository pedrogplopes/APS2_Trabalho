from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, flight, seats_reserved):
        pass

class StandardPricingStrategy(PricingStrategy):
    def calculate_price(self, flight, seats_reserved):
        return flight.price * seats_reserved

class DiscountPricingStrategy(PricingStrategy):
    def calculate_price(self, flight, seats_reserved):
        return (flight.price * seats_reserved) * 0.9  # 10% de desconto
