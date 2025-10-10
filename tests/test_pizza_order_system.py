# test_pizza_order_system.py
"""
Testy jednostkowe dla systemu zamówień pizzy.
Testy powinny przechodzić zarówno PRZED jak i PO refaktoryzacji.
"""

import pytest
from src.pizza_order_system import (
    place_pizza_order,
    InventoryManager,
    PaymentProcessor,
    DeliveryScheduler,
    LoyaltyPointsCalculator,
    NotificationService,
    PriceCalculator
)


def test_successful_order():
    """Test pomyślnego złożenia zamówienia."""
    result = place_pizza_order(
        pizza_type="Margherita",
        address="ul. Długa 5",
        delivery_time="18:00",
        card_number="1234-5678",
        user_id="user123"
    )
    
    assert result["success"] is True
    assert result["pizza_type"] == "Margherita"
    assert result["price"] == 25.0
    assert result["points_earned"] == 2
    assert "order_id" in result


def test_invalid_card_number():
    """Test zamówienia z nieprawidłowym numerem karty."""
    result = place_pizza_order(
        pizza_type="Pepperoni",
        address="ul. Krótka 10",
        delivery_time="19:00",
        card_number="9999-9999",
        user_id="user456"
    )
    
    assert result["success"] is False
    assert "Płatność odrzucona" in result["error"]


def test_unavailable_pizza():
    """Test zamówienia pizzy, której nie ma w magazynie."""
    result = place_pizza_order(
        pizza_type="Hawaii",  # Ta pizza nie istnieje w menu
        address="ul. Szeroka 3",
        delivery_time="20:00",
        card_number="1234-5678",
        user_id="user789"
    )
    
    assert result["success"] is False
    assert "Nieznany typ pizzy" in result["error"]


def test_inventory_manager():
    """Test zarządzania magazynem."""
    inventory = InventoryManager()
    
    assert inventory.check_availability("Margherita") is True
    assert inventory.check_availability("Hawaii") is False
    
    assert inventory.reserve_pizza("Margherita") is True
    assert inventory.inventory["Margherita"] == 9


def test_payment_processor():
    """Test procesora płatności."""
    payment = PaymentProcessor()
    
    assert payment.process_payment("1234-5678", 25.0) is True
    assert payment.process_payment("9999-9999", 25.0) is False


def test_loyalty_points():
    """Test systemu punktów lojalnościowych."""
    loyalty = LoyaltyPointsCalculator()
    
    points = loyalty.add_points("user123", 35.0)
    assert points == 3
    assert loyalty.user_points["user123"] == 3


def test_price_calculator():
    """Test kalkulatora cen."""
    calc = PriceCalculator()
    
    assert calc.get_price("Margherita") == 25.0
    assert calc.get_price("Pepperoni") == 30.0
    assert calc.get_price("Hawaii") == 0.0


def test_delivery_scheduler():
    """Test planowania dostaw."""
    scheduler = DeliveryScheduler()
    
    delivery_id = scheduler.schedule_delivery("ul. Długa 5", "18:00")
    assert delivery_id == 1
    assert len(scheduler.deliveries) == 1


def test_notification_service():
    """Test serwisu powiadomień."""
    notifications = NotificationService()
    
    assert notifications.send_sms("user123", "Test message") is True
    assert notifications.send_email("user123", "Test", "Message") is True
    assert len(notifications.sent_notifications) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
