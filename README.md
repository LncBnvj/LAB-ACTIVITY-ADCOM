# ✨ Payment Method System — Python Edition ✨

Welcome to a **fully interactive payment system** built in Python! This terminal-based app demonstrates the power of **Object-Oriented Programming (OOP)** with a practical, real-world simulation of how we handle payments every day — from digital wallets to old-school cash! 🧾💰

---

## 🚀 What You'll Learn

This project is perfect for learning and showcasing:

- 🧠 **Abstraction** — Defining *what* should be done, but not *how*.
- 🏛️ **Inheritance** — Code reuse by deriving specialized classes from a base.
- 🔒 **Encapsulation** — Secure your data with privacy and validation.
- 🧬 **Polymorphism** — One interface, many implementations!

---

## 👑 Parent Class: `PaymentMethod`

Acts as the master blueprint for all payment types.

```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    def __init__(self, amount: float, currency: str, payment_id: str):
        self.amount = amount
        self.currency = currency
        self.payment_id = payment_id

    @abstractmethod
    def process_payment(self):
        pass

    def payment_details(self):
        return f"Payment ID: {self.payment_id}, Amount: {self.amount} {self.currency}"

    def validate_payment(self):
        return self.amount > 0
````

🔐 Can't be instantiated — forces subclasses to implement `process_payment()`.

---

## 🏦 Subclass: `BankBased`

Bank account payment simulation with deposit, withdrawal, and balance checks.

```python
class BankBased(PaymentMethod):
    def __init__(self, amount, currency, payment_id, bank_name, account_number, account_name):
        super().__init__(amount, currency, payment_id)
        self.bank_name = bank_name
        self.account_number = account_number
        self.account_name = account_name
        self.balance = 0.0

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            print("Insufficient balance.")

    def check_balance(self):
        return f"Current balance: {self.balance:,.2f} {self.currency}"

    def process_payment(self):
        if self.balance >= self.amount:
            self.balance -= self.amount
            return "✅ Payment processed via Bank-Based."
        return "❌ Insufficient bank balance."
```

---

## 📲 Subclass: `EWallet`

Your digital wallet experience — fast, flexible, and user-friendly.

```python
class EWallet(PaymentMethod):
    def __init__(self, balance):
        super().__init__(0, "PHP", "EWT001")
        self.balance = balance

    def cash_in(self, amount):
        if amount > 0:
            self.balance += amount

    def cash_out(self, amount):
        if amount <= self.balance:
            self.balance -= amount

    def send_payment(self, amount):
        if amount <= self.balance:
            self.balance -= amount

    def check_balance(self):
        print(f"💰 Current Balance: ₱{self.balance:,.2f}")

    def process_payment(self):
        if self.balance >= self.amount:
            self.balance -= self.amount
            print(f"✅ Payment of {self.amount:.2f} {self.currency} processed via E-Wallet.")
        else:
            print("❌ Insufficient E-Wallet balance.")
```

💡 Great for demonstrating **encapsulation** and **balance operations**.

---

## 💳 Subclass: `ATMCard`

An advanced card system with savings, credit, and password protection.

```python
class ATMCard(PaymentMethod):
    def __init__(self, card_number, cvv, expiry_date, credit_limit, savings_balance, password):
        super().__init__(0, "PHP", "ATM001")
        self.__card_number = card_number
        self.__cvv = cvv
        self.__expiry_date = expiry_date
        self.__credit_limit = credit_limit
        self.__credit_balance = credit_limit
        self.__savings_balance = savings_balance
        self.__password = password

    def process_payment(self):
        return "⚠️ Use the 'pay' method to perform ATM transactions."

    def __authenticate(self, password_input):
        return password_input == self.__password

    def pay(self, amount, account_type, password_input):
        if not self.__authenticate(password_input):
            return "❌ Incorrect password."
        if account_type == "credit" and amount <= self.__credit_balance:
            self.__credit_balance -= amount
            return f"✅ Paid ₱{amount:,.2f} using credit."
        elif account_type == "savings" and amount <= self.__savings_balance:
            self.__savings_balance -= amount
            return f"✅ Paid ₱{amount:,.2f} using savings."
        return "❌ Insufficient balance or invalid account."

    def deposit(self, amount, account_type, password_input):
        if not self.__authenticate(password_input):
            return "❌ Incorrect password."
        if account_type == "credit":
            space = self.__credit_limit - self.__credit_balance
            deposit_amt = min(space, amount)
            self.__credit_balance += deposit_amt
            return f"✅ Deposited ₱{deposit_amt:,.2f} to credit."
        elif account_type == "savings":
            self.__savings_balance += amount
            return f"✅ Deposited ₱{amount:,.2f} to savings."
        return "❌ Invalid account type."

    def make_payment(self, amount, password_input):
        if not self.__authenticate(password_input):
            return "❌ Incorrect password."
        debt = self.__credit_limit - self.__credit_balance
        if amount > self.__savings_balance:
            return "❌ Insufficient savings balance."
        payment = min(amount, debt)
        self.__savings_balance -= payment
        self.__credit_balance += payment
        return f"✅ Paid ₱{payment:,.2f} from savings to credit."
```

🔒 Demonstrates **data protection** with private attributes and password validation.

---

## 💵 Subclass: `Cash`
Simple yet effective. Cash payments with receipt printing and change calculation.

```python
class Cash(PaymentMethod):
    def __init__(self, receipt_number, amount_due, amount_received):
        super().__init__(amount_due, "PHP", receipt_number)
        self.__receipt_number = receipt_number
        self.__amount_due = amount_due
        self.__amount_received = amount_received

    def process_payment(self):
        return self.__amount_received - self.__amount_due

    @property
    def change(self):
        return self.__amount_received - self.__amount_due

    def exact_payment(self):
        return self.__amount_received == self.__amount_due

    def print_receipt(self):
        print(f"Receipt #: {self.__receipt_number}")
        print(f"Total: ₱{self.__amount_due:,.2f}")
        print(f"Received: ₱{self.__amount_received:,.2f}")
        print(f"Change: ₱{self.change:,.2f}")
```

📜 Perfect for showing how even basic classes benefit from encapsulation and class properties.

---

## 🧪 How to Run This Project

1. ✅ Make sure you have Python 3 installed.
2. 🗂️ Open your terminal in the project folder.
3. ▶️ Run:

```bash
python CS_1204_GROUP8_PAYMENT_METHOD.py
```

4. 🧾 Follow the on-screen prompts to:

   * Shop for products
   * Choose a payment method
   * Simulate real-life transactions!

---

## 👥 Authors & Acknowledgment

### 👨‍💻 Group 8 – BSCS 1204

*   💳 *Member 1:* **Jev Austin A. Apolinar**
*   🏦 *Member 2:* **Danielle A. Balilla**
*   📲 *Member 3:* **Lance T. Buenviaje**
*   💵 *Member 4:* **Ken Frankie G. Mendoza**

> *"Each member contributed to designing, coding, and documenting the payment system project as part of our CS 1204 course."*

---

### 🙏 Acknowledgment

We would like to express our heartfelt thanks to **Ms. Fatima Marie P. Agdon, MSCS**, our `CS-121 Instructor` in CS-1204, for her continuous support, motivation, and mentorship throughout this project. Your expertise and guidance helped us gain a deeper understanding of OOP and how to apply it meaningfully.

Your passion for teaching brought a unique energy to our class, making every session more engaging and enjoyable. Thank you for being an inspiring mentor who strikes the perfect balance between dedication and enthusiasm. 💜 Your lively spirit, relatable approach, and genuine care for your students reminded us that learning can be both meaningful and fun. 

---

# Happy coding! 🚀


