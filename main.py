from datetime import datetime
from abc import ABC, abstractmethod

class TerminalColors:
    HEADER = '\033[95m'      # Bright magenta
    OKBLUE = '\033[94m'      # Blue
    OKGREEN = '\033[92m'     # Green
    WARNING = '\033[93m'     # Yellow
    FAIL = '\033[91m'        # Red
    ENDC = '\033[0m'         # Reset to default
    BOLD = '\033[1m'         # Bold text
    UNDERLINE = '\033[4m'    # Underlined text
    PINK = '\033[38;5;205m'  # Pink

class Product:
    def __init__(self, product_id, name, price, version, available, stock, genre):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.version = version
        self.available = available
        self.stock = stock
        self.genre = genre


class ShoppingCart:
    def __init__(self):
        self.items = []

    def __add__(self, product):
        self.add_item(product)
        return self

    def add_item(self, product, quantity=1):

# adding product for the first time
        if product.stock < quantity:
            print(
                f"{TerminalColors.FAIL}Not enough stock for '{product.name}'. Available stock: {product.stock}{TerminalColors.ENDC}")
            return

# if selected item is already in the cart
        for item in self.items:
            if item['product'].product_id == product.product_id:
                if item['quantity'] + quantity > product.stock:
                    print(
                        f"{TerminalColors.FAIL}Cannot add {quantity} '{product.name}' to the cart. Exceeds stock limit.{TerminalColors.ENDC}")
                    return
                item['quantity'] += quantity
                print(f"{TerminalColors.OKGREEN}Added {quantity} '{product.name}' to the cart.{TerminalColors.ENDC}")
                return

        # saving dictionary in the list
        self.items.append({'product': product, 'quantity': quantity})
        print(f"{TerminalColors.OKGREEN}Added {quantity} '{product.name}' to the cart.{TerminalColors.ENDC}")

    def remove_item(self, product_id, quantity=1):

# if quantity to be removed is lesser than the quantity present in the cart
        for item in self.items:
            if item['product'].product_id == product_id:
                if item['quantity'] > quantity:
                    item['quantity'] -= quantity
                    print(
                        f"{TerminalColors.OKBLUE}Removed {quantity} '{item['product'].name}' from the cart.{TerminalColors.ENDC}")

# if quantity to be removed exceeds the quantity present in the cart, directly remove the product from the cart
                else:
                    self.items.remove(item)
                    print(
                        f"{TerminalColors.OKBLUE}Removed '{item['product'].name}' from the cart.{TerminalColors.ENDC}")
                return
        print(f"{TerminalColors.FAIL}Product with ID '{product_id}' not found in the cart.{TerminalColors.ENDC}")

# displaying cart
    def display_cart(self):
        print()
        print(TerminalColors.HEADER + TerminalColors.BOLD + '=' * 16 + TerminalColors.ENDC)
        print(f'{TerminalColors.PINK}{TerminalColors.BOLD}----- CART -----{TerminalColors.ENDC}')
        print(TerminalColors.HEADER + TerminalColors.BOLD + '=' * 16 + TerminalColors.ENDC)
        print()
        if self.items:
            for item in self.items:
                product = item['product']
                quantity = item['quantity']
                total_price = product.price * quantity
                print(f"- {product.name} (ID: {product.product_id}, Quantity: {quantity}, "
                      f"Price per item: {TerminalColors.OKGREEN}${product.price}{TerminalColors.ENDC}, "
                      f"Total Price: {TerminalColors.OKGREEN}${total_price}{TerminalColors.ENDC})")
        else:
            print(f"{TerminalColors.WARNING}Your cart is empty.{TerminalColors.ENDC}")

# Create a shallow copy of the current items in the cart
    def save_cart(self, user):
        user.saved_cart = self.items.copy()
        print(f"{TerminalColors.OKBLUE}\nCart saved successfully.{TerminalColors.ENDC}")

# Load the saved cart items from the user object and assign to the cart's items
    def load_cart(self, user):
        self.items = user.saved_cart.copy()
        print(f"{TerminalColors.OKBLUE}\nCart loaded successfully.{TerminalColors.ENDC}")



class Transaction:
    def __init__(self, user, cart):
        self.user = user
        self.cart = cart
        self.total_price = sum(item['product'].price * item['quantity'] for item in cart.items)
        self.date_time = datetime.now()

# calculating tax and checking out
    def process_transaction(self):
        tax = self.total_price * 0.15
        total_amount = self.total_price + tax
        print()
        while True:
            if self.cart.items == []:
                print(
                    TerminalColors.FAIL + "Your cart is empty. Add products to cart for checkout." + TerminalColors.ENDC)
                break
            checkout = input(TerminalColors.OKBLUE + 'Do you wanna checkout? (Yes/No): ' + TerminalColors.ENDC).lower()
            if checkout == 'no':
                break
            elif checkout == 'yes':
                address = input(TerminalColors.OKBLUE + 'Enter your address: ' + TerminalColors.ENDC)
                print()
                print(TerminalColors.HEADER + TerminalColors.BOLD + '=' * 20 + TerminalColors.ENDC)
                print(TerminalColors.PINK + TerminalColors.BOLD + "Transaction Details:" + TerminalColors.ENDC)
                print(TerminalColors.HEADER + TerminalColors.BOLD + '=' * 20 + TerminalColors.ENDC)
                print()
                print(f"Date & Time: {self.date_time}")
                print("Items Purchased:")
                for item in self.cart.items:
                    product = item['product']
                    quantity = item['quantity']
                    print(f"- {product.name} (Quantity: {quantity}, Price per item: ${product.price})")
                print(f"Total Price: ${self.total_price}")
                print(f"Tax (15%): ${tax}")
                print(f"Total Amount: ${total_amount}")
                print()

                while True:
                    password = input(TerminalColors.OKBLUE + 'Enter Password for Confirmation: ' + TerminalColors.ENDC)
                    if password == self.user.password:
                        print(TerminalColors.OKGREEN + 'Password Authenticated!' + TerminalColors.ENDC)
                        while True:
                            payment_choice = input(
                                TerminalColors.OKBLUE + "Choose payment method (cash/card): " + TerminalColors.ENDC).lower()
                            if payment_choice == 'cash':
                                CashPayment().process_payment()
                                return total_amount
                            elif payment_choice == 'card':
                                CardPayment().process_payment()
                                return total_amount
                            else:
                                print(TerminalColors.FAIL + "Invalid payment method." + TerminalColors.ENDC)
                    else:
                        while True:
                            print(TerminalColors.FAIL + "Wrong Password!" + TerminalColors.ENDC)
                            pw = input(TerminalColors.OKBLUE + "Enter 'y' to try again or 'n' to exit: " + TerminalColors.ENDC).lower()
                            if pw == 'y':
                                break
                            if pw == 'n':
                                self.process_transaction()
                                return
                            else:
                                input(TerminalColors.FAIL + "Enter 'y' or 'n': " + TerminalColors.ENDC)

            else:
                print(TerminalColors.FAIL + 'Enter Yes OR No' + TerminalColors.ENDC)


class User:
    def __init__(self, username, password, realname):
        self.username = username
        self.password = password
        self.realname = realname
        self.cart = ShoppingCart()
        self.saved_cart = []
        self.history = History()

    def add_to_history(self, transaction):
        self.history.add_transaction(transaction)


class History:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

# displaying history of the user
    def display_history(self):
        print()
        print(TerminalColors.HEADER + TerminalColors.BOLD + '=' * 20 + TerminalColors.ENDC)
        print(TerminalColors.PINK + TerminalColors.BOLD + "Transaction History:" +TerminalColors.ENDC)
        print(TerminalColors.HEADER + TerminalColors.BOLD + '=' * 20 + TerminalColors.ENDC)
        print()
# if user hasn't placed any order yet with the account
        if not self.transactions:
            print(TerminalColors.FAIL + 'The user has no history!' + TerminalColors.ENDC)
            return

# if user has placed orders previously
        for i, transaction in enumerate(self.transactions, start=1):
            print(f"Transaction {i}:")
            print(f"Date & Time: {transaction.date_time}")
            print("Items Purchased:")
            for item in transaction.cart.items:
                product = item['product']
                quantity = item['quantity']
                print(f"- {product.name} (Quantity: {quantity}, Price per item: ${product.price})")
            print(f"Total Price: ${transaction.total_price}")
            print()

# shopping history for a specific date
    def display_history_by_date(self, date):
        print()
        print(TerminalColors.HEADER + TerminalColors.BOLD + '=' * 35 + TerminalColors.ENDC)
        print(TerminalColors.PINK + TerminalColors.BOLD + f"Transaction History for {date}:" + TerminalColors.ENDC)
        print(TerminalColors.HEADER + TerminalColors.BOLD + '=' * 35 + TerminalColors.ENDC)
        print()
        transactions_on_date = [t for t in self.transactions if t.date_time.date() == date]

# if there is no history for the given date
        if not transactions_on_date:
            print(TerminalColors.FAIL + 'No transactions found for this date.' + TerminalColors.ENDC)
            return

# if there is history for the specified date
        for i, transaction in enumerate(transactions_on_date, start=1):
            print(f"Transaction {i}:")
            print(f"Date & Time: {transaction.date_time}")
            print("Items Purchased:")
            for item in transaction.cart.items:
                product = item['product']
                quantity = item['quantity']
                print(f"- {product.name} (Quantity: {quantity}, Price per item: ${product.price})")
            print(f"Total Price: ${transaction.total_price}")
            print()

# shopping history for a specific item
    def display_history_by_item(self, item_name):
        print()
        print(TerminalColors.HEADER + TerminalColors.BOLD + '=' * 35 + TerminalColors.ENDC)
        print(TerminalColors.PINK + TerminalColors.BOLD + f"Transaction History for {item_name}:" + TerminalColors.ENDC)
        print(TerminalColors.HEADER + TerminalColors.BOLD + '=' * 35 + TerminalColors.ENDC)
        print()
        transactions_with_item = [t for t in self.transactions if
                                  any(item_name in item['product'].name for item in t.cart.items)]

# if the entered item has never been bought by the user previously
        if not transactions_with_item:
            print(TerminalColors.FAIL + f'No transactions found for item: {item_name}.' + TerminalColors.ENDC)
            return

# if the user has bought the entered item
        for i, transaction in enumerate(transactions_with_item, start=1):
            print(f"Transaction {i}:")
            print(f"Date & Time: {transaction.date_time}")
            print("Items Purchased:")
            for item in transaction.cart.items:
                product = item['product']
                quantity = item['quantity']
                if item_name in product.name:
                    print(f"- {product.name} (Quantity: {quantity}, Price per item: ${product.price})")
            print(f"Total Price: ${transaction.total_price}")
            print()


class LibrarySystem:
    def __init__(self):

# initializing an empty dictionary for user records
        self.users = {}

# admin account credentials
        self.admin = Admin("admin", "admin123")

# wide range of 15 products by default
        self.products = [Product("01", "XBOX", 30000, "360", True, 10, "Console"),
                         Product("02", "PLAY STATION PORTABLE", 35000, "PSP-3000", True, 8, "Console"),
                         Product("03", "VR GLASSES", 30000, "VR SHINECON 6.0", True, 5, "Accessory"),
                         Product("04", "JOY STICK", 9000, "ULTRA STIK 360FS", True, 15, "Accessory"),
                         Product("05", "GAMING HEADSET", 12000, "ASTRO A40TR", True, 12, "Accessory"),
                         Product("06", "GAMING GLOVES", 7000, "UMBRA", True, 20, "Accessory"),
                         Product("07", "GAMING PC", 600000, "ALIENWARE AURORA RYZEN R15", True, 3, "Console"),
                         Product("08", "WIRELESS CONTROLLERS", 8000, "8BITDO ULTIMATE C 2.4G", True, 18, "Accessory"),
                         Product("09", "Nintendo Switch", 30000, "V2", True, 10, "Console"),
                         Product("10", "PlayStation 5", 50000, "PS5", True, 5, "Console"),
                         Product("11", "Xbox Series X", 45000, "Series X", True, 7, "Console"),
                         Product("12", "Oculus Quest 2", 40000, "128GB", True, 8, "Accessory"),
                         Product("13", "Razer Gaming Mouse", 8000, "DeathAdder V2", True, 12, "Accessory"),
                         Product("14", "Corsair Gaming Keyboard", 10000, "K95 RGB Platinum XT", True, 6, "Accessory"),
                         Product("15", "Gaming Chair", 15000, "Secretlab Omega 2020", True, 4, "Accessory")
                         ]

# loading records for signup and login
        self.load_records()

# reading the file of user credentials for help in signup and login
    def load_records(self):
        try:
            with open("records.txt", "r") as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) == 3:
                        username, password, realname = data
                        self.users[username] = User(username, password, realname)
                    else:
                        print(TerminalColors.FAIL + f"Ignoring invalid record: {line.strip()}" + TerminalColors.ENDC)
        except FileNotFoundError:
            pass

# saving user entries
    def save_records(self):
        with open("records.txt", "w") as file:
            for user in self.users.values():
                file.write(f"{user.username},{user.password},{user.realname}\n")

# signup making sure no two users have the same username
    def sign_up(self, username, password, realname):
        if username in self.users:
            print(TerminalColors.FAIL + "Username already exists. Please choose a different one." + TerminalColors.ENDC)
            return False
        self.users[username] = User(username, password, realname)
        self.save_records()
        print(TerminalColors.OKGREEN + f"Welcome, {realname}! Your account has been created." + TerminalColors.ENDC)
        return True

# login checking the entered username and password matches with the records in the file
    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            print(TerminalColors.OKGREEN + f"Welcome back, {user.realname}!" + TerminalColors.ENDC)
            return user
        else:
            print(TerminalColors.FAIL + "Invalid username or password." + TerminalColors.ENDC)
            return None

# admin login with admin credentials only
    def admin_login(self, username, password):
        if username == self.admin.username and password == self.admin.password:
            print(TerminalColors.OKGREEN + "Welcome, Admin!" + TerminalColors.ENDC)
            return self.admin
        else:
            print(TerminalColors.FAIL + "Invalid admin credentials." + TerminalColors.ENDC)
            return None


class Payment(ABC):
    @abstractmethod
    def process_payment(self):
        pass


class CardPayment(Payment):
    def process_payment(self):
        print(
            TerminalColors.OKGREEN + "Processing payment via card...\nPayment Successful" + TerminalColors.ENDC)
        print(TerminalColors.PINK + TerminalColors.BOLD + "\nThank you for shopping with us!\n" + TerminalColors.ENDC)
# asking for review after checkout
        input(TerminalColors.OKBLUE + "Enter your review about our services: " + TerminalColors.ENDC)
        print(
            TerminalColors.OKGREEN + "Thanks for the review, we will try to make our services better!" + TerminalColors.ENDC)


class CashPayment(Payment):
    def process_payment(self):
        print(
            TerminalColors.OKGREEN + "Processing payment via cash...\nPayment Successful" + TerminalColors.ENDC)#ye line kyun  pooch rhsy 
        print(TerminalColors.PINK + TerminalColors.BOLD + "\nThank you for shopping with us!\n" + TerminalColors.ENDC)
# asking for review after checkout
        input(TerminalColors.OKBLUE + "Enter your review about our services: " + TerminalColors.ENDC)
        print(
            TerminalColors.OKGREEN + "Thanks for the review, we will try to make our services better!" + TerminalColors.ENDC)


class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Adding products to provide a vast range of choices for the users
    def add_product(self, library_system):
        while True:
            product_id = input(TerminalColors.OKBLUE + "Enter Product ID: " + TerminalColors.ENDC)
            if any(product.product_id == product_id for product in library_system.products):
                print(TerminalColors.FAIL + f"Product ID '{product_id}' already exists. Please enter a different Product ID." + Admin.TerminalColors.ENDC)
                continue
            break

        name = input(TerminalColors.OKBLUE + "Enter Product Name: " + TerminalColors.ENDC)

        while True:
            try:
                price = int(input(TerminalColors.OKBLUE + "Enter Product Price: " + TerminalColors.ENDC))
                break
            except ValueError:
                print(TerminalColors.FAIL + "Invalid input for price. Please enter a valid number." + TerminalColors.ENDC)

        version = input(TerminalColors.OKBLUE + "Enter Product Version: " + TerminalColors.ENDC)

        while True:
            available_input = input(TerminalColors.OKBLUE + "Is the product available (yes/no)? " + TerminalColors.ENDC).lower()
            if available_input in ['yes', 'no']:
                available = available_input == 'yes'
                break
            else:
                print(TerminalColors.FAIL + "Invalid input for availability. Please enter 'yes' or 'no'." + TerminalColors.ENDC)

        while True:
            try:
                stock = int(input(TerminalColors.OKBLUE + "Enter Stock Quantity: " + TerminalColors.ENDC))
                break
            except ValueError:
                print(TerminalColors.FAIL + "Invalid input for stock quantity. Please enter a valid integer." + TerminalColors.ENDC)

        valid_genres = ['Accessory', 'Console']
        while True:
            genre = input(TerminalColors.OKBLUE + f"Enter Product Genre ({', '.join(valid_genres)}): " + TerminalColors.ENDC).strip().title()
            if genre in valid_genres:
                break
            else:
                print(TerminalColors.FAIL + f"Invalid input for genre. Please enter one of the following: {', '.join(valid_genres)}." + TerminalColors.ENDC)

        new_product = Product(product_id, name, price, version, available, stock, genre)

        library_system.products.append(new_product)
        print(TerminalColors.OKGREEN + f"Product '{name}' added successfully." + TerminalColors.ENDC)

    def remove_product(self, library_system):
        product_id = input(TerminalColors.OKBLUE + "Enter Product ID to remove: " + TerminalColors.ENDC)
        for product in library_system.products:
            if product.product_id == product_id:
                library_system.products.remove(product)
                print(TerminalColors.OKGREEN + f"Product '{product.name}' removed successfully." + TerminalColors.ENDC)
                return
        print(TerminalColors.FAIL + f"Product with ID '{product_id}' not found." + TerminalColors.ENDC)

    def update_product_quantity(self, library_system):
        product_id = input(TerminalColors.OKBLUE + "Enter Product ID to update quantity: " + TerminalColors.ENDC)
        for product in library_system.products:
            if product.product_id == product_id:
                while True:
                    try:
                        new_quantity = int(input(TerminalColors.OKBLUE + "Enter new stock quantity: " + TerminalColors.ENDC))
                        break
                    except ValueError:
                        print(TerminalColors.FAIL + "Invalid input for stock quantity. Please enter a valid integer." + TerminalColors.ENDC)
                product.stock = new_quantity
                print(TerminalColors.OKGREEN + f"Updated stock for '{product.name}' to {new_quantity}." + TerminalColors.ENDC)
                return
        print(TerminalColors.FAIL + f"Product with ID '{product_id}' not found." + TerminalColors.ENDC)

    def display_products(self, library_system):
        print()
        if not library_system.products:
            print(TerminalColors.WARNING + "No products available." + TerminalColors.ENDC)
            return

        products = library_system.products
        headers = ["ID", "Name", "Price", "Version", "Available", "Stock", "Genre"]
        column_widths = [max(len(str(getattr(product, attr))) for product in products) for attr in vars(products[0])]
        column_widths = [max(width, len(header)) for width, header in zip(column_widths, headers)]
        row_format = "|"
        for width in column_widths:
            row_format += " {:<" + str(width) + "} |"
        row_format = row_format.strip()

        print(TerminalColors.HEADER + TerminalColors.BOLD + "=" * (sum(column_widths) + len(column_widths) * 3 + 1) + TerminalColors.ENDC)
        print(TerminalColors.HEADER + TerminalColors.BOLD + row_format.format(*headers) + TerminalColors.ENDC)
        print(TerminalColors.HEADER + TerminalColors.BOLD + "=" * (sum(column_widths) + len(column_widths) * 3 + 1) + TerminalColors.ENDC)

        for product in library_system.products:
            availability = TerminalColors.OKGREEN + "Yes" if product.available else TerminalColors.FAIL + "No"
            print(TerminalColors.PINK + row_format.format(product.product_id, product.name, product.price, product.version, availability, product.stock, product.genre) + TerminalColors.ENDC)

        print(TerminalColors.HEADER + TerminalColors.BOLD + "=" * (sum(column_widths) + len(column_widths) * 3 + 1) + TerminalColors.ENDC)



def main():
    system = LibrarySystem()
    print(TerminalColors.HEADER + TerminalColors.BOLD + '=' * 39 + TerminalColors.ENDC)
    print(TerminalColors.PINK + TerminalColors.BOLD + '          --- WELCOME \u2764\ufe0f ---           ' + TerminalColors.ENDC)
    print(TerminalColors.PINK + TerminalColors.BOLD + '--- TO THE HOUSE OF GAMING NERDS !! ---' + TerminalColors.ENDC)
    print(TerminalColors.HEADER + TerminalColors.BOLD + '=' * 39 + TerminalColors.ENDC)
    while True:
        print(TerminalColors.HEADER + "\n1. Admin Login\n2. User Login\n3. User Signup\n4. Exit\n" + TerminalColors.ENDC)
        choice = input(TerminalColors.OKBLUE + "Choose an option: " + TerminalColors.ENDC)

        if choice == '1':   # admin login
            username = input(TerminalColors.OKBLUE + "Enter admin username: " + TerminalColors.ENDC)
            password = input(TerminalColors.OKBLUE + "Enter admin password: " + TerminalColors.ENDC)
            admin = system.admin_login(username, password)
            if admin:
                while True:
                    print(TerminalColors.HEADER + "\n1. Add Product\n2. Remove Product\n3. Update Product Quantity\n4. Display Products\n5. Logout\n" + TerminalColors.ENDC)
                    admin_choice = input(TerminalColors.OKBLUE + "Choose an option: " + TerminalColors.ENDC)
                    if admin_choice == '1':
                        admin.add_product(system)
                    elif admin_choice == '2':
                        admin.remove_product(system)
                    elif admin_choice == '3':
                        admin.update_product_quantity(system)
                    elif admin_choice == '4':
                        admin.display_products(system)
                    elif admin_choice == '5':
                        print(TerminalColors.OKGREEN + "Logging out..." + TerminalColors.ENDC)
                        break
                    else:
                        print(TerminalColors.FAIL + "Invalid option. Please try again." + TerminalColors.ENDC)

        elif choice == '2':   # user login
            username = input(TerminalColors.OKBLUE + "Enter username: " + TerminalColors.ENDC)
            password = input(TerminalColors.OKBLUE + "Enter password: " + TerminalColors.ENDC)
            user = system.login(username, password)
            if user:
                while True:
                    print(TerminalColors.HEADER + "\n1. Display Products\n2. Add to Cart\n3. Remove from Cart\n4. View Cart\n5. Save Cart\n6. Load Cart\n7. Checkout\n8. View History\n9. Logout\n" + TerminalColors.ENDC)
                    user_choice = input(TerminalColors.OKBLUE + "Choose an option: " + TerminalColors.ENDC)
                    if user_choice == '1':   # displaying product list
                        system.admin.display_products(system)
                    elif user_choice == '2':   # adding to cart
                        system.admin.display_products(system)
                        product_id = input(
                            TerminalColors.OKBLUE + "\nEnter Product ID to add to cart: " + TerminalColors.ENDC)
                        while True:
                            try:
                                quantity = int(input(TerminalColors.OKBLUE + "Enter quantity: " + TerminalColors.ENDC))
                                break
                            except ValueError:
                                print(
                                    TerminalColors.FAIL + "Invalid input for quantity. Please enter a valid integer." + TerminalColors.ENDC)

                        for product in system.products:
                            if product.product_id == product_id:
                                user.cart.add_item(product, quantity)
                                break
                        else:
                            print(
                                TerminalColors.FAIL + f"Product with ID '{product_id}' not found." + TerminalColors.ENDC)
                    elif user_choice == '3':
                        user.cart.display_cart()  # removing from cart
                        print()
                        product_id = input(TerminalColors.OKBLUE + "Enter Product ID to remove from cart: " + TerminalColors.ENDC)
                        while True:
                            try:
                                quantity = int(input(TerminalColors.OKBLUE + "Enter quantity: " + TerminalColors.ENDC))
                                break
                            except ValueError:
                                print(TerminalColors.FAIL + "Invalid input for quantity. Please enter a valid integer." + TerminalColors.ENDC)
                        user.cart.remove_item(product_id, quantity)
                    elif user_choice == '4':   # displaying cart
                        user.cart.display_cart()
                    elif user_choice == '5':   # saving cart
                        user.cart.save_cart(user)
                    elif user_choice == '6':   # loading cart
                        user.cart.load_cart(user)
                    elif user_choice == '7':   # checking out
                        transaction = Transaction(user, user.cart)
                        amount = transaction.process_transaction()
                        if amount:
                            user.add_to_history(transaction)
                            user.cart = ShoppingCart()   # Reset cart after successful checkout
                    elif user_choice == '8':   # viewing history
                        print(TerminalColors.HEADER + "\n1. View Complete History\n2. View History by Date\n3. View History by Item\n" + TerminalColors.ENDC)
                        history_choice = input(TerminalColors.OKBLUE + "Choose an option: " + TerminalColors.ENDC)
                        if history_choice == '1':   # viewing complete history of a user
                            user.history.display_history()
                        elif history_choice == '2':   # viewing history by a specific date
                            date_str = input(TerminalColors.OKBLUE + "Enter date (YYYY-MM-DD): " + TerminalColors.ENDC)
                            try:
                                history_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                                user.history.display_history_by_date(history_date)
                            except ValueError:
                                print(TerminalColors.FAIL + "Invalid date format." + TerminalColors.ENDC)
                        elif history_choice == '3':   # viewing history by a specific item
                            item_name = input(TerminalColors.OKBLUE + "Enter item name: " + TerminalColors.ENDC)
                            user.history.display_history_by_item(item_name)
                        else:
                            print(TerminalColors.FAIL + "Invalid option. Please try again." + TerminalColors.ENDC)
                    elif user_choice == '9':   # logging out
                        print(TerminalColors.OKGREEN + "Logging out..." + TerminalColors.ENDC)
                        break
                    else:
                        print(TerminalColors.FAIL + "Invalid option. Please try again." + TerminalColors.ENDC)

        elif choice == '3':   # user signup
            username = input(TerminalColors.OKBLUE + "Enter username: " + TerminalColors.ENDC)
            password = input(TerminalColors.OKBLUE + "Enter password: " + TerminalColors.ENDC)
            realname = input(TerminalColors.OKBLUE + "Enter real name: " + TerminalColors.ENDC)
            system.sign_up(username, password, realname)

        elif choice == '4':   # exiting the program
            print(TerminalColors.OKGREEN + "Exiting the system. Goodbye!" + TerminalColors.ENDC)
            break

        else:
            print(TerminalColors.FAIL + "Invalid option. Please try again." + TerminalColors.ENDC)


if __name__ == "__main__":
    main()