# pizza_order_system.py
"""
System zamówień pizzy - wersja PRZED refaktoryzacją z użyciem wzorca Facade.
Kod jest skomplikowany, klient musi znać wszystkie podsystemy i kolejność wywołań.
"""


class InventoryManager:
    """Zarządza stanem magazynowym składników."""

    def __init__(self):
        self.inventory = {
            "Margherita": 10,
            "Pepperoni": 8,
            "Vegetariana": 5,
            "Capricciosa": 3,
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
            # Tutaj byłoby rzeczywiste przetwarzanie płatności
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
        notification = {
            "user_id": user_id,
            "type": "SMS",
            "message": message
        }
        self.sent_notifications.append(notification)
        return True

    def send_email(self, user_id, subject, message):
        """Wysyła email do użytkownika."""
        notification = {
            "user_id": user_id,
            "type": "EMAIL",
            "subject": subject,
            "message": message
        }
        self.sent_notifications.append(notification)
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


# ============================================
# FUNKCJA KLIENCKA - TO JEST MASAKRA!
# ============================================

class PizzaOrderException(Exception):
    def __init__(self, message):
        super().__init__(message)


class PizzaOrderFacade:
    inventory = InventoryManager()
    price_calc = PriceCalculator()
    payment = PaymentProcessor()
    delivery = DeliveryScheduler()
    loyalty = LoyaltyPointsCalculator()
    notifications = NotificationService()

    def isAvailable(self, pizza_type):
        if not self.inventory.check_availability(pizza_type):
            raise PizzaOrderException(f"Pizza '{pizza_type}' nie jest dostępna w magazynie.")

    def getPrice(self, pizza_type):
        if self.price_calc.get_price(pizza_type) == 0:
            raise PizzaOrderException(f"Nieznany typ pizzy: {pizza_type}")
        else:
            return self.price_calc.get_price(pizza_type)

    def processPayment(self, card_number, amount):
        if not self.payment.process_payment(card_number, amount):
            raise PizzaOrderException("Płatność odrzucona - nieprawidłowy numer karty")

    def reservePizza(self, pizza_type):
        if not self.inventory.reserve_pizza(pizza_type):
            raise PizzaOrderException("Nie udało się zarezerwować pizzy")

    def scheduleDelivery(self, address, delivery_time):
        if not self.delivery.schedule_delivery(address, delivery_time):
            raise PizzaOrderException("Nie udało się zaplanować dostawy")
        else:
            return self.delivery.schedule_delivery(address, delivery_time)

    def addLoyaltyPoints(self, user_id, amount):
        if not self.loyalty.add_points(user_id, amount):
            raise PizzaOrderException("Nie udało się dodać punktów lojalnościowych")
        else:
            return self.loyalty.add_points(user_id, amount)

    def sendSMS(self, user_id, message):
        if not self.notifications.send_sms(user_id, message):
            raise PizzaOrderException("Nie udało się wysłać SMS")

    def sendEmail(self, user_id, subject, message):
        if not self.notifications.send_email(user_id, subject, message):
            raise PizzaOrderException("Nie udało się wysłać emaila")

    def place_order(self, pizza_type, address, delivery_time, card_number, user_id):
        try:
            self.isAvailable(pizza_type)
            price = self.getPrice(pizza_type)
            self.processPayment(card_number, price)
            self.reservePizza(pizza_type)
            delivery_id = self.scheduleDelivery(address, delivery_time)
            points_earned = self.addLoyaltyPoints(user_id, price)
            self.sendSMS(user_id, f"Zamówienie pizzy {pizza_type} potwierdzone! Dostawa: {delivery_time}")
            self.sendEmail(user_id, "Potwierdzenie zamówienia",
                           f"Twoje zamówienie #{delivery_id} zostało przyjęte. Dostawa na {address} o {delivery_time}.")
        except PizzaOrderException as e:
            return {
                "success": False,
                "error": str(e)
            }

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
    return facade.place_order(pizza_type, address, delivery_time, card_number, user_id)