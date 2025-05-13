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

# BankBased
class BankBased(PaymentMethod):
    def __init__(self, amount, currency, payment_id, bank_name, account_number, account_name):
        super().__init__(amount, currency, payment_id)
        self.bank_name = bank_name
        self.account_number = account_number
        self.account_name = account_name
        self.balance = 0.0

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Withdrawn {amount:,.2f} {self.currency}. New balance: {self.balance:,.2f} {self.currency}")
        else:
            print("Insufficient balance.")

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount:,.2f} {self.currency}. New balance: {self.balance:,.2f} {self.currency}")

    def check_balance(self):
        return f"Current balance: {self.balance:,.2f} {self.currency}"

    def process_payment(self):
        if self.balance >= self.amount:
            self.balance -= self.amount
            return "✅ Payment processed via Bank-Based."
        return "❌ Insufficient bank balance."

# EWallet
class EWallet(PaymentMethod):
    def __init__(self, owner_name, balance):
        super().__init__(0, "PHP", "EWT001")
        self.balance = balance
        self.owner_name = owner_name

    def process_payment(self):
        if self.amount <= self.balance:
            self.balance -= self.amount
            print(f"✅ Payment of {self.amount:.2f} {self.currency} processed via E-Wallet.")
        else:
            print("❌ Insufficient E-Wallet balance.")

    def cash_in(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"✅ Cash-in successful: ₱{amount:,.2f}")
        else:
            print("❌ Invalid amount. Cash-in must be more than ₱0.")

    def cash_out(self, amount):
        if amount <= 0:
            print("❌ Invalid amount. Cash-out must be more than ₱0.")
        elif amount > self.balance:
            print("❌ Insufficient balance.")
        else:
            self.balance -= amount
            print(f"✅ Cash-out successful: ₱{amount:,.2f}")

    def send_payment(self, amount):
        if amount <= 0:
            print("❌ Invalid amount. Payment must be more than ₱0.")
        elif amount > self.balance:
            print("❌ Payment failed. Insufficient balance.")
        else:
            self.balance -= amount
            print(f"✅ Payment of ₱{amount:,.2f} sent successfully.")

    def check_balance(self):
        print(f"💰 Current Balance: ₱{self.balance:,.2f}")

# ATMCard
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
        if amount <= 0:
            return "❌ Amount must be greater than zero."

        if account_type == "credit":
            if amount > self.__credit_balance:
                return "❌ Insufficient credit balance."
            self.__credit_balance -= amount
            return f"✅ Paid ₱{amount:,.2f} using credit. Remaining credit: ₱{self.__credit_balance:,.2f}"
        elif account_type == "savings":
            if amount > self.__savings_balance:
                return "❌ Insufficient savings balance."
            self.__savings_balance -= amount
            return f"✅ Paid ₱{amount:,.2f} using savings. Remaining savings: ₱{self.__savings_balance:,.2f}"
        else:
            return "❌ Invalid account type."

    def deposit(self, amount, account_type, password_input):
        if not self.__authenticate(password_input):
            return "❌ Incorrect password."
        if amount <= 0:
            return "❌ Deposit amount must be positive."

        if account_type == "credit":
            space = self.__credit_limit - self.__credit_balance
            deposit_amt = min(space, amount)
            self.__credit_balance += deposit_amt
            return f"✅ Deposited ₱{deposit_amt:,.2f} to credit. Available credit: ₱{self.__credit_balance:,.2f}"
        elif account_type == "savings":
            self.__savings_balance += amount
            return f"✅ Deposited ₱{amount:,.2f} to savings. New savings balance: ₱{self.__savings_balance:,.2f}"
        else:
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
        return f"✅ Paid ₱{payment:,.2f} from savings to credit. Available credit: ₱{self.__credit_balance:,.2f}"

    def check_balance(self, account_type, password_input):
        if not self.__authenticate(password_input):
            return "❌ Incorrect password."
        if account_type == "credit":
            return f"💳 Credit Balance: ₱{self.__credit_balance:,.2f} / ₱{self.__credit_limit:,.2f}"
        elif account_type == "savings":
            return f"🏦 Savings Balance: ₱{self.__savings_balance:,.2f}"
        else:
            return "❌ Invalid account type."

    def get_card_details(self, password_input):
        if not self.__authenticate(password_input):
            return "❌ Incorrect password."
        return (f"📇 Card Number: **** **** **** {str(self.__card_number)[-4:]}\n"
                f"CVV: ***\n"
                f"Expiry Date: {self.__expiry_date}\n"
                f"💳 Credit Limit: ₱{self.__credit_limit:,.2f}\n"
                f"💳 Available Credit: ₱{self.__credit_balance:,.2f}\n"
                f"🏦 Savings Balance: ₱{self.__savings_balance:,.2f}")

#CashPayment
class Cash(PaymentMethod):
    def __init__(self, receipt_number, amount_due, amount_received):
        super().__init__(amount_due, "PHP", receipt_number)
        self.__receipt_number = receipt_number
        self.__amount_due = amount_due
        self.__amount_received = amount_received

    def process_payment(self):
        return self.__amount_received - self.__amount_due

    @property
    def receipt_number(self):
        return self.__receipt_number

    @receipt_number.setter
    def receipt_number(self, new_receipt_number):
        self.__receipt_number = new_receipt_number

    @property
    def change(self):
        return self.__amount_received - self.__amount_due

    @property
    def amount_received(self):
        return self.__amount_received

    @amount_received.setter
    def amount_received(self, new_amount_received):
        self.__amount_received = new_amount_received

    @property
    def amount_due(self):
        return self.__amount_due

    def calculate_change(self):
        return self.change

    def exact_payment(self):
        return self.__amount_received == self.__amount_due

    def print_receipt(self):
        print(f"\n--- CASH METHOD ---")
        print(f"Receipt Number: {self.__receipt_number}")
        print(f"Total Amount: ₱{self.__amount_due:,.2f}")
        print(f"Amount Received: ₱{self.__amount_received:,.2f}")
        print(f"Change: ₱{self.calculate_change():,.2f}")
        print(f"Exact Payment: {'Yes' if self.exact_payment() else 'No'}")

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print(" Invalid input. Please enter a valid number.")

def get_valid_amount_received(total):
    while True:
        amount = get_float("Enter amount received: ₱")
        if amount < total:
            print(" Amount received is not enough. Please enter a valid amount.")
        else:
            return amount

def get_items():
    product_list = {
        1: ("Milk", 50.00),
        2: ("Bread", 35.00),
        3: ("Eggs", 90.00),
        4: ("Rice", 45.00),
        5: ("Coffee", 120.00)
    }

    items = []
    total = 0.0

    print("\n📦 Available Products:")
    for key, (name, price) in product_list.items():
        print(f"{key}. {name} - ₱{price:.2f}")

    print("\nEnter the number of the product you want to buy (type 0 to finish):")
    while True:
        try:
            choice = int(input("Product number: "))
            if choice == 0:
                break
            if choice not in product_list:
                print("Invalid selection. Try again.")
                continue

            quantity = int(input(f"Quantity of {product_list[choice][0]}: "))
            item_name, item_price = product_list[choice]
            total += item_price * quantity
            items.append((item_name, item_price, quantity))
        except ValueError:
            print("Please enter a valid number.")

    return items, total

def main():
    print("=== Welcome to the Payment System ===")
    items, total_amount = get_items()
    print("\n🛒 Items Purchased:")
    for name, price, qty in items:
        print(f"- {name} x{qty}: {price * qty:.2f}")
    print(f"\n🧾 Total Amount: {total_amount:.2f} PHP")

    print("\nChoose payment method:")
    print("1. Bank-Based")
    print("2. E-Wallet")
    print("3. ATM System")
    print("4. Cash")

    choice = input("Enter option (1-4): ")
    payment_id = "PMT001"
    currency = "PHP"

    if choice == "1":
        print("Welcome to Bank-Based Payment System")

        account_name = input("Enter account name: ")
        bank_name = input("Enter bank name: ")
        account_number = int(input("Enter account number: "))
        currency = input("Enter currency (e.g. PHP): ")
        payment_id = input("Enter payment ID: ")
        amount = float(input("Enter base amount for the transaction: "))

        account = BankBased(amount, currency, payment_id, bank_name, account_number, account_name)

        while True:
            print("\nChoose an option:")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            print("4. View Payment Details")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ")

            if choice == "1":
                deposit_amount = float(input("Enter amount to deposit: "))
                account.deposit(deposit_amount)
            elif choice == "2":
                withdraw_amount = float(input("Enter amount to withdraw: "))
                account.withdraw(withdraw_amount)
            elif choice == "3":
                print(account.check_balance())
            elif choice == "4":
                print(account.payment_details())
            elif choice == "5":
                print("Thank you for using the system!")
                break
            else:
                print("Invalid choice. Please try again.")

    elif choice == "2":
        print("📱 Welcome to the E-Wallet System!")

        owner_name = input("Enter your name: ")

        wallet = EWallet(owner_name, 5000.00) 

        while True:
            print("\n====== E-WALLET MENU ======")
            print("1. Check Balance")
            print("2. Cash In")
            print("3. Cash Out")
            print("4. Send Payment")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ").strip()

            if choice == "1":
                wallet.check_balance()
            elif choice == "2":
                try:
                    amount = float(input("Enter amount to cash in: ₱"))
                    wallet.cash_in(amount)
                except ValueError:
                    print("❌ Please enter a valid number.")
            elif choice == "3":
                try:
                    amount = float(input("Enter amount to cash out: ₱"))
                    wallet.cash_out(amount)
                except ValueError:
                    print("❌ Please enter a valid number.")
            elif choice == "4":
                try:
                    amount = float(input("Enter amount to send: ₱"))
                    wallet.send_payment(amount)
                except ValueError:
                    print("❌ Please enter a valid number.")
            elif choice == "5":
                print("👋 Exiting E-Wallet. Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select between 1 and 5.")

    elif choice == "3":
        print("Welcome to the ATM Card System 💳")

        try:
            card_number = int(input("Enter card number: "))
            cvv = int(input("Enter CVV: "))
            expiry = int(input("Enter expiry date (MMYY): "))
            credit_limit = float(input("Enter credit limit (₱): "))
            savings_bal = float(input("Enter initial savings balance (₱): "))
            password = int(input("Set a 4-digit password: "))
        except:
            print("❌ Invalid input. Exiting.")
            return

        card = ATMCard(card_number, cvv, expiry, credit_limit, savings_bal, password)

        while True:
            print("\n📋 MENU:")
            print("1. Pay for Purchase (Choose Credit or Savings)")
            print("2. Deposit Funds")
            print("3. Make a Payment (from Savings to Credit)")
            print("4. Check Balance")
            print("5. View Card Details")
            print("6. Exit")

            choice = input("Choose an option (1–6): ").strip()

            if choice == '1':
                account = input("Pay using which account? (credit/savings): ").strip().lower()
                amt = float(input("Enter payment amount (₱): "))
                pwd = int(input("Enter password: "))
                print(card.pay(amt, account, pwd))

            elif choice == '2':
                acct_type = input("Deposit to which account? (credit/savings): ").strip().lower()
                amt = float(input("Enter deposit amount (₱): "))
                pwd = int(input("Enter password: "))
                print(card.deposit(amt, acct_type, pwd))

            elif choice == '3':
                amt = float(input("Enter amount to pay credit from savings (₱): "))
                pwd = int(input("Enter password: "))
                print(card.make_payment(amt, pwd))

            elif choice == '4':
                acct_type = input("Check balance for which account? (credit/savings): ").strip().lower()
                pwd = int(input("Enter password: "))
                print(card.check_balance(acct_type, pwd))

            elif choice == '5':
                pwd = int(input("Enter password: "))
                print(card.get_card_details(pwd))

            elif choice == '6':
                print("👋 Thank you for using the ATM Card System!")
                break

            else:
                print("❌ Invalid option. Please try again.")

    elif choice == "4":
        print("--- CASH METHOD ---")
        receipt_no = input("Enter receipt number: ")
        total = get_float("Enter total amount: ₱")
        received = get_valid_amount_received(total)
        transaction = Cash(receipt_no, total, received)
        transaction.print_receipt()

        while True:
            response = input("\nWould you like to update the amount received or exit? (u/e): ").strip().lower()
            if response == 'u':
                new_received = get_valid_amount_received(transaction.amount_due)
                transaction.amount_received = new_received
                transaction.print_receipt()
            elif response == 'e':
                print("Thank you.")
                break
            else:
                print("Please enter a valid response [u/e]")

if __name__ == "__main__":
    main()
