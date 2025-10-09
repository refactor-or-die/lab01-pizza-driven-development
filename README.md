# Lab 01: Pizza Driven Development

Laboratorium z wzorców projektowych - **Facade Pattern**

Organizacja: [refactor-or-die](https://github.com/refactor-or-die)

## Informacje podstawowe

- **Wzorzec:** Facade (Fasada)
- **Język:** Python
- **Czas:** 1,5 godziny
- **Forma pracy:** pair programming

## Cel zajęć

Praktyczne poznanie wzorca **Facade** poprzez refaktoryzację skomplikowanego kodu systemu zamówień pizzy. Celem jest ukrycie złożoności wielu podsystemów za prostym, jednolitym interfejsem.

## Problem do rozwiązania

W pliku `src/pizza_order_system.py` znajduje się funkcja `place_pizza_order()`, która realizuje proces składania zamówienia na pizzę. Problem polega na tym, że:

- Klient musi znać **6 różnych klas** podsystemów
- Musi znać **dokładną kolejność** wywołań wszystkich metod
- Musi **ręcznie obsługiwać** błędy na każdym kroku
- Kod jest **nieczytelny** i **trudny w utrzymaniu**
- Każda zmiana w podsystemie wymaga modyfikacji kodu klienta

### Przykład obecnego kodu

```python
def place_pizza_order(pizza_type, address, delivery_time, card_number, user_id):
    # Krok 1: Sprawdź magazyn
    inventory = InventoryManager()
    if not inventory.check_availability(pizza_type):
        return {"success": False, "error": "Brak pizzy"}
    
    # Krok 2: Oblicz cenę
    price_calc = PriceCalculator()
    price = price_calc.get_price(pizza_type)
    
    # Krok 3: Płatność
    payment = PaymentProcessor()
    if not payment.process_payment(card_number, price):
        return {"success": False, "error": "Płatność odrzucona"}
    
    # ... i tak dalej przez kolejne 5 kroków
```

To jest **zbyt skomplikowane** dla klienta, który po prostu chce zamówić pizzę.

## Zadanie

Zrefaktoryzuj kod używając wzorca **Facade**:

1. Stwórz klasę `PizzaOrderFacade` w pliku `src/pizza_order_system.py`
2. Klasa powinna mieć metodę `place_order()` o sygnaturze:
   ```python
   def place_order(self, pizza_type, address, delivery_time, card_number, user_id)
   ```
3. Metoda powinna zwracać słownik w formacie:
   ```python
   {
       "success": True/False,
       "order_id": ...,      # jeśli success=True
       "pizza_type": ...,
       "price": ...,
       "points_earned": ...,
       "delivery_time": ...,
       "error": ...          # jeśli success=False
   }
   ```
4. Zmodyfikuj funkcję `place_pizza_order()` tak, aby używała `PizzaOrderFacade`
5. Upewnij się, że **wszystkie testy przechodzą**

## Wymagania techniczne

- Python 3.8+
- pytest

## Instalacja i uruchomienie

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/refactor-or-die/lab01-pizza-driven-development.git
cd lab01-pizza-driven-development
```

### 2. Utwórz własny branch

```bash
git checkout -b lab01_nazwisko1_nazwisko2
```

### 3. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### 4. Uruchom testy (powinny przejść przed refaktoryzacją)

```bash
pytest tests/ -v
```

### 5. Refaktoryzuj kod

Pracujcie w parach (pair programming), regularnie zamieniając się rolami Driver/Navigator.

### 6. Sprawdź, czy testy nadal przechodzą

```bash
pytest tests/ -v
```

### 7. Commit i push

```bash
git add .
git commit -m "Refaktoryzacja z użyciem wzorca Facade"
git push origin lab01_nazwisko1_nazwisko2
```

## Kryteria zaliczenia

- Utworzenie klasy `PizzaOrderFacade` z metodą `place_order()`
- Uproszczenie funkcji `place_pizza_order()` przez użycie Facade
- Wszystkie testy przechodzą (`pytest tests/ -v`)
- Kod jest czytelny i zgodny z ideą wzorca Facade
- Prezentacja rozwiązania na końcu zajęć (2-3 minuty)

## Struktura projektu

```
lab01-pizza-driven-development/
├── README.md                          # Ten plik
├── .gitignore                         # Ignorowane pliki
├── requirements.txt                   # Zależności Python
├── slides/                            # Prezentacja wprowadzająca
│   └── facade_intro.pdf
├── src/
│   └── pizza_order_system.py         # Kod do refaktoryzacji
└── tests/
    └── test_pizza_order_system.py    # Testy jednostkowe
```

## Wzorzec Facade - krótkie przypomnienie

**Facade** to strukturalny wzorzec projektowy, który dostarcza uproszczony interfejs do złożonego podsystemu.

### Kiedy używać?

- System ma wiele współzależnych klas
- Klient potrzebuje tylko podstawowych operacji
- Chcesz odizolować klienta od szczegółów implementacji
- Chcesz uprościć API dla użytkowników zewnętrznych

### Zalety

- Uproszczenie interfejsu
- Redukcja zależności między klientem a podsystemem
- Łatwiejsze utrzymanie kodu
- Elastyczność w modyfikacji podsystemu

### Trade-off

- Facade może stać się "god object" jeśli wrzucimy do niej za dużo odpowiedzialności
- Dodatkowa warstwa abstrakcji (minimalny overhead)

## Pytania do przemyślenia

Po wykonaniu zadania zastanówcie się:

1. Jak Facade wpłynął na czytelność kodu?
2. Czy łatwiej byłoby teraz dodać nową funkcjonalność (np. zniżki, kupony)?
3. Jakie są potencjalne wady wprowadzenia Facade w tym przypadku?
4. Kiedy NIE powinniśmy używać tego wzorca?

## Kontakt

W razie pytań: jaroslaw.hryszko@uj.edu.pl

---

**Powodzenia!** 🍕