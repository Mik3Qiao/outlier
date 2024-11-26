from datetime import datetime

# Constants
BASE_FEE = 5
UBER_GOLD_DISCOUNT = 0.5
TD_PREMIUM_DISCOUNT = 0
WEALTHSIMPLE_PLUS_FEE = 2
PEAK_HOUR_FEE = 3
PROMO_CODE_DISCOUNT = 2
PEAK_HOUR_START = 18
PEAK_HOUR_END = 21
WEEKEND_DAYS = [5, 6]

class DeliveryService:
    def __init__(self, user_data: dict, promo_code: str = None) -> None:
        """
        Initialize the DeliveryService class.

        Args:
        user_data (dict): A dictionary containing user data.
        promo_code (str): A promo code to apply a discount.
        """
        self.user_data = user_data
        self.promo_code = promo_code

    def calculate_delivery_fee(self) -> float:
        """
        Calculate the delivery fee based on the user data and promo code.

        Returns:
        float: The delivery fee.
        """
        base_fee = self._calculate_base_fee()
        discounted_fee = self._apply_discounts(base_fee)
        peak_hour_fee = self._apply_peak_hour_fee(discounted_fee)
        promo_code_fee = self._apply_promo_code_discount(peak_hour_fee)
        return promo_code_fee

    def _calculate_base_fee(self) -> float:
        """
        Calculate the base delivery fee.

        Returns:
        float: The base delivery fee.
        """
        if self.user_data.get("is_uber_member", False):
            if self.user_data.get("is_uber_gold", False):
                return max(0, BASE_FEE * UBER_GOLD_DISCOUNT)
            return 0
        if self.user_data.get("is_td_premium", False) and self.is_weekend():
            return 0
        if self.user_data.get("is_wealthsimple_plus", False):
            return WEALTHSIMPLE_PLUS_FEE
        return BASE_FEE

    def _apply_discounts(self, base_fee: float) -> float:
        """
        Apply discounts to the base delivery fee.

        Args:
        base_fee (float): The base delivery fee.

        Returns:
        float: The discounted delivery fee.
        """
        return base_fee

    def _apply_peak_hour_fee(self, discounted_fee: float) -> float:
        """
        Apply a peak hour fee to the discounted delivery fee.

        Args:
        discounted_fee (float): The discounted delivery fee.

        Returns:
        float: The delivery fee with the peak hour fee applied.
        """
        if self.is_peak_hour():
            return discounted_fee + PEAK_HOUR_FEE
        return discounted_fee

    def _apply_promo_code_discount(self, peak_hour_fee: float) -> float:
        """
        Apply a promo code discount to the delivery fee.

        Args:
        peak_hour_fee (float): The delivery fee with the peak hour fee applied.

        Returns:
        float: The delivery fee with the promo code discount applied.
        """
        if self.promo_code and peak_hour_fee > 0:
            return max(0, peak_hour_fee - PROMO_CODE_DISCOUNT)
        return peak_hour_fee

    def is_weekend(self) -> bool:
        """
        Check if it's a weekend.

        Returns:
        bool: True if it's a weekend, False otherwise.
        """
        today = datetime.now().weekday()
        return today in WEEKEND_DAYS

    def is_peak_hour(self) -> bool:
        """
        Check if it's a peak hour.

        Returns:
        bool: True if it's a peak hour, False otherwise.
        """
        current_hour = datetime.now().hour
        return PEAK_HOUR_START <= current_hour <= PEAK_HOUR_END
    
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