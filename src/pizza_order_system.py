"""
System zamówień pizzy – WERSJA PO refaktoryzacji z użyciem wzorca FACADE.

Klient komunikuje się tylko z PizzaOrderFacade.
Nie musi znać podsystemów ani kolejności wywołań.
"""


class InventoryManager:
    """Zarządza stanem magazynowym składników."""

    def __init__(self):
        self.inventory = {
            "Margherita": 10,
            "Pepperoni": 8,
            "Vegetariana": 5,
            "Capricciosa": 3
        }

    def check_availability(self, pizza_type):
        """Sprawdza czy pizza jest dostępna w magazynie."""
        return self.inventory.get(pizza_type, 0) > 0

    def reserve_pizza(self, pizza_type):
        """Rezerwuje pizzę (zmniejsza stan magazynowy)."""
        if self.check_availability(pizza_type):
            self.inventory[pizza_type] -= 1
            return True
        return False


class PaymentProcessor:
    """Przetwarza płatności kartą."""

    def __init__(self):
        self.valid_cards = ["1234-5678", "8765-4321", "1111-2222"]

    def validate_card(self, card_number):
        """Sprawdza czy karta jest poprawna."""
        return card_number in self.valid_cards

    def process_payment(self, card_number, amount):
        """Przetwarza płatność."""
        if self.validate_card(card_number):
            return True
        return False


class DeliveryScheduler:
    """Planuje dostawy."""

    def __init__(self):
        self.deliveries = []

    def schedule_delivery(self, address, delivery_time):
        """Planuje dostawę na określony czas."""
        delivery_id = len(self.deliveries) + 1
        self.deliveries.append({
            "id": delivery_id,
            "address": address,
            "time": delivery_time
        })
        return delivery_id


class LoyaltyPointsCalculator:
    """Zarządza punktami lojalnościowymi."""

    def __init__(self):
        self.user_points = {}

    def calculate_points(self, amount):
        """Oblicza punkty: 1 punkt za każde 10 zł."""
        return int(amount / 10)

    def add_points(self, user_id, amount):
        """Dodaje punkty użytkownikowi."""
        points = self.calculate_points(amount)
        if user_id not in self.user_points:
            self.user_points[user_id] = 0
        self.user_points[user_id] += points
        return points


class NotificationService:
    """Wysyła powiadomienia do klientów."""

    def __init__(self):
        self.sent_notifications = []

    def send_sms(self, user_id, message):
        """Wysyła SMS do użytkownika."""
        self.sent_notifications.append({
            "user_id": user_id,
            "type": "SMS",
            "message": message
        })
        return True

    def send_email(self, user_id, subject, message):
        """Wysyła email do użytkownika."""
        self.sent_notifications.append({
            "user_id": user_id,
            "type": "EMAIL",
            "subject": subject,
            "message": message
        })
        return True


class PriceCalculator:
    """Oblicza ceny pizzy."""

    def __init__(self):
        self.prices = {
            "Margherita": 25.0,
            "Pepperoni": 30.0,
            "Vegetariana": 28.0,
            "Capricciosa": 32.0
        }

    def get_price(self, pizza_type):
        """Zwraca cenę pizzy."""
        return self.prices.get(pizza_type, 0.0)




class PizzaOrderFacade:
    """
    Fasada upraszczająca składanie zamówień pizzy.
    Ukrywa złożoność wszystkich podsystemów.
    """

    def __init__(self):
        self.inventory = InventoryManager()
        self.price_calc = PriceCalculator()
        self.payment = PaymentProcessor()
        self.delivery = DeliveryScheduler()
        self.loyalty = LoyaltyPointsCalculator()
        self.notifications = NotificationService()

    def place_order(self, pizza_type, address, delivery_time, card_number, user_id):
        if not self.inventory.check_availability(pizza_type):
            return {
                "success": False,
                "error": f"Pizza {pizza_type} nie jest dostępna w magazynie"
            }

        price = self.price_calc.get_price(pizza_type)
        if price == 0.0:
            return {
                "success": False,
                "error": f"Nieznany typ pizzy: {pizza_type}"
            }

        if not self.payment.process_payment(card_number, price):
            return {
                "success": False,
                "error": "Płatność odrzucona - nieprawidłowy numer karty"
            }

        if not self.inventory.reserve_pizza(pizza_type):
            return {
                "success": False,
                "error": "Nie udało się zarezerwować pizzy"
            }

        delivery_id = self.delivery.schedule_delivery(address, delivery_time)

        points_earned = self.loyalty.add_points(user_id, price)

        self.notifications.send_sms(
            user_id,
            f"Zamówienie pizzy {pizza_type} potwierdzone! Dostawa: {delivery_time}"
        )

        self.notifications.send_email(
            user_id,
            "Potwierdzenie zamówienia",
            f"Twoje zamówienie #{delivery_id} zostało przyjęte. "
            f"Dostawa na {address} o {delivery_time}."
        )

        return {
            "success": True,
            "order_id": delivery_id,
            "pizza_type": pizza_type,
            "price": price,
            "points_earned": points_earned,
            "delivery_time": delivery_time
        }



def place_pizza_order(pizza_type, address, delivery_time, card_number, user_id):
    facade = PizzaOrderFacade()
    return facade.place_order(
        pizza_type,
        address,
        delivery_time,
        card_number,
        user_id
    )
