from datetime import datetime
from typing import Dict

class DeliveryService:
    def __init__(self, user_data: Dict, promo_code: str = None):
        self.user_data = user_data
        self.promo_code = promo_code

    def calculate_delivery_fee(self) -> float:
        """Calculates the delivery fee based on user data and promo code."""
        base_fee = self._get_base_fee()

        # Apply discounts
        base_fee = self._apply_membership_discount(base_fee)
        base_fee = self._apply_td_premium_discount(base_fee)
        base_fee = self._apply_wealthsimple_discount(base_fee)

        # Apply peak hour surcharge
        base_fee = self._apply_peak_hour_surcharge(base_fee)

        # Apply promo code discount
        base_fee = self._apply_promo_code_discount(base_fee)

        return base_fee

    def _get_base_fee(self) -> float:
        """Returns the base delivery fee."""
        return 5

    def _apply_membership_discount(self, base_fee: float) -> float:
        """Applies the membership discount to the base fee."""
        if self.user_data.get("is_uber_member", False):
            if self.user_data.get("is_uber_gold", False):
                return max(0, base_fee * 0.5)
            return 0
        return base_fee

    def _apply_td_premium_discount(self, base_fee: float) -> float:
        """Applies the TD premium discount to the base fee."""
        if self.user_data.get("is_td_premium", False) and self.is_weekend():
            return 0
        return base_fee

    def _apply_wealthsimple_discount(self, base_fee: float) -> float:
        """Applies the Wealthsimple discount to the base fee."""
        if self.user_data.get("is_wealthsimple_plus", False):
            return 2
        return base_fee

    def _apply_peak_hour_surcharge(self, base_fee: float) -> float:
        """Applies the peak hour surcharge to the base fee."""
        if self.is_peak_hour():
            return base_fee + 3
        return base_fee

    def _apply_promo_code_discount(self, base_fee: float) -> float:
        """Applies the promo code discount to the base fee."""
        if self.promo_code and base_fee > 0:
            return max(0, base_fee - 2)
        return base_fee

    def is_weekend(self) -> bool:
        """Returns True if today is a weekend."""
        today = datetime.now().weekday()
        return today in [5, 6]

    def is_peak_hour(self) -> bool:
        """Returns True if the current hour is a peak hour."""
        current_hour = datetime.now().hour
        return 18 <= current_hour <= 21
    
user_1 = {
    "is_uber_member": True,
    "is_uber_gold": False,
    "is_td_customer": False,
    "is_wealthsimple_customer": False,
    "is_td_premium": False
}
user_2 = {
    "is_uber_member": False,
    "is_td_customer": False,
    "is_wealthsimple_plus": True,
    "is_td_premium": False
}
user_3 = {
    "is_uber_member": False,
    "is_td_customer": False,
    "is_wealthsimple_customer": False,
    "is_td_premium": True
}

service_1 = DeliveryService(user_1)
service_2 = DeliveryService(user_2, promo_code="DISCOUNT2")
service_3 = DeliveryService(user_3)

print(f"User 1 Delivery Fee: ${service_1.calculate_delivery_fee():.2f}")
print(f"User 2 Delivery Fee: ${service_2.calculate_delivery_fee():.2f}")
print(f"User 3 Delivery Fee: ${service_3.calculate_delivery_fee():.2f}")