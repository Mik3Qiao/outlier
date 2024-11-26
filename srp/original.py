from datetime import datetime
from typing import Dict, Optional
from unittest.mock import patch

# Constants to avoid magic numbers
BASE_FEE = 5.0
UBER_GOLD_DISCOUNT = 0.5
WEALTHSIMPLE_FEE = 2.0
PEAK_HOUR_FEE = 3.0
PROMO_DISCOUNT = 2.0
PEAK_START = 18
PEAK_END = 21
WEEKEND_DAYS = (5, 6)

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class DeliveryService:
    def __init__(self, user_data: Dict, promo_code: Optional[str] = None):
        self._validate_inputs(user_data, promo_code)
        self.user_data = user_data
        self.promo_code = promo_code

    def _validate_inputs(self, user_data: Dict, promo_code: Optional[str]) -> None:
        """Validate input parameters"""
        if not isinstance(user_data, dict):
            raise ValidationError("user_data must be a dictionary")
            
        required_fields = ["is_uber_member", "is_td_premium", "is_wealthsimple_plus"]
        missing_fields = [field for field in required_fields if field not in user_data]
        if missing_fields:
            raise ValidationError(f"Missing required fields: {missing_fields}")

        if promo_code is not None and not isinstance(promo_code, str):
            raise ValidationError("promo_code must be a string")

    def calculate_delivery_fee(self) -> float:
        """Calculate final delivery fee with all applicable rules"""
        base_fee = self._get_base_fee()
        fee_with_membership = self._apply_membership_discounts(base_fee)
        fee_with_time = self._apply_time_based_fees(fee_with_membership)
        final_fee = self._apply_promo_discount(fee_with_time)
        return max(0, final_fee)  # Ensure fee is never negative

    def _get_base_fee(self) -> float:
        """Get the base delivery fee"""
        return BASE_FEE

    def _apply_membership_discounts(self, fee: float) -> float:
        """Apply all membership-based discounts"""
        if self.user_data.get("is_uber_member"):
            if self.user_data.get("is_uber_gold"):
                return max(0, fee * UBER_GOLD_DISCOUNT)
            return 0

        if self.user_data.get("is_wealthsimple_plus"):
            return WEALTHSIMPLE_FEE

        if self.user_data.get("is_td_premium") and self.is_weekend():
            return 0

        return fee

    def _apply_time_based_fees(self, fee: float) -> float:
        """Apply time-based fees (peak hours)"""
        try:
            if self.is_peak_hour():
                fee += PEAK_HOUR_FEE
            return fee
        except Exception as e:
            raise ValidationError(f"Error checking time-based fees: {str(e)}")

    def _apply_promo_discount(self, fee: float) -> float:
        """Apply promo code discount if applicable"""
        if self.promo_code and fee > 0:
            return max(0, fee - PROMO_DISCOUNT)
        return fee

    def is_weekend(self) -> bool:
        """Check if current time is weekend"""
        try:
            return datetime.now().weekday() in WEEKEND_DAYS
        except Exception as e:
            raise ValidationError(f"Error checking weekend status: {str(e)}")

    def is_peak_hour(self) -> bool:
        """Check if current time is peak hour"""
        try:
            current_hour = datetime.now().hour
            return PEAK_START <= current_hour <= PEAK_END
        except Exception as e:
            raise ValidationError(f"Error checking peak hours: {str(e)}")
        
# Test cases for DeliveryService
from datetime import datetime
from unittest.mock import patch

def test_delivery_service():
    # Regular user - will pay base fee
    regular_user = {
        "is_uber_member": False,
        "is_uber_gold": False,
        "is_td_premium": False,
        "is_wealthsimple_plus": False
    }

    # Uber Gold member - will get 50% discount
    uber_gold_user = {
        "is_uber_member": True,
        "is_uber_gold": True,
        "is_td_premium": False,
        "is_wealthsimple_plus": False
    }

    # Wealthsimple Plus user - will pay fixed $2 fee
    wealthsimple_user = {
        "is_uber_member": False,
        "is_uber_gold": False,
        "is_td_premium": False,
        "is_wealthsimple_plus": True
    }

    # TD Premium user - free on weekends, regular fee on weekdays
    td_premium_user = {
        "is_uber_member": False,
        "is_uber_gold": False,
        "is_td_premium": True,
        "is_wealthsimple_plus": False
    }

    # Test during normal hours (2 PM on a Wednesday)
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value.hour = 14
        mock_datetime.now.return_value.weekday.return_value = 2

        print("\nNormal Hours (2 PM, Wednesday):")
        print(f"Regular User Fee: ${DeliveryService(regular_user).calculate_delivery_fee():.2f}")  # Should be $5
        print(f"Uber Gold User Fee: ${DeliveryService(uber_gold_user).calculate_delivery_fee():.2f}")  # Should be $2.50
        print(f"Wealthsimple Plus User Fee: ${DeliveryService(wealthsimple_user).calculate_delivery_fee():.2f}")  # Should be $2
        print(f"TD Premium User Fee: ${DeliveryService(td_premium_user).calculate_delivery_fee():.2f}")  # Should be $5

    # Test during peak hours (7 PM on a Wednesday)
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value.hour = 19
        mock_datetime.now.return_value.weekday.return_value = 2

        print("\nPeak Hours (7 PM, Wednesday):")
        print(f"Regular User Fee: ${DeliveryService(regular_user).calculate_delivery_fee():.2f}")  # Should be $8
        print(f"Regular User + Promo Fee: ${DeliveryService(regular_user, 'DISCOUNT2').calculate_delivery_fee():.2f}")  # Should be $6
        print(f"Uber Gold User Fee: ${DeliveryService(uber_gold_user).calculate_delivery_fee():.2f}")  # Should be $4
        print(f"Wealthsimple Plus User Fee: ${DeliveryService(wealthsimple_user).calculate_delivery_fee():.2f}")  # Should be $5

    # Test during weekend
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value.hour = 14
        mock_datetime.now.return_value.weekday.return_value = 6  # Sunday

        print("\nWeekend (2 PM, Sunday):")
        print(f"Regular User Fee: ${DeliveryService(regular_user).calculate_delivery_fee():.2f}")  # Should be $5
        print(f"TD Premium User Fee: ${DeliveryService(td_premium_user).calculate_delivery_fee():.2f}")  # Should be $0
        
    # Test combinations during peak weekend
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value.hour = 19  # Peak hour
        mock_datetime.now.return_value.weekday.return_value = 6  # Sunday

        print("\nPeak Weekend (7 PM, Sunday):")
        print(f"Regular User Fee: ${DeliveryService(regular_user).calculate_delivery_fee():.2f}")  # Should be $8
        print(f"TD Premium User Fee: ${DeliveryService(td_premium_user).calculate_delivery_fee():.2f}")  # Should be $0
        print(f"Uber Gold + Promo Fee: ${DeliveryService(uber_gold_user, 'DISCOUNT2').calculate_delivery_fee():.2f}")  # Should be $2

if __name__ == "__main__":
    test_delivery_service()