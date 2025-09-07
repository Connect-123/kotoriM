"""
ninjemail.py - Core functions for email account creation
Handles all the business logic and account generation
"""

import random
import string
from datetime import datetime, timedelta
import json
import os

# Try to import the actual ninjemail library
try:
    from ninjemail import Ninjemail as NinjemailLib

    NINJEMAIL_AVAILABLE = True
except ImportError:
    print("Warning: ninjemail library not found. Install with: pip install ninjemail")
    NINJEMAIL_AVAILABLE = False
    NinjemailLib = None


class DataGenerator:
    """Generates random data for account creation"""

    # Common first names
    FIRST_NAMES_MALE = [
        "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
        "Thomas", "Christopher", "Charles", "Daniel", "Matthew", "Anthony", "Mark",
        "Donald", "Steven", "Kenneth", "Andrew", "Kenneth", "Joshua", "Kevin", "Brian",
        "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan", "Jacob"
    ]

    FIRST_NAMES_FEMALE = [
        "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica",
        "Sarah", "Karen", "Nancy", "Betty", "Margaret", "Sandra", "Ashley", "Kimberly",
        "Emily", "Donna", "Michelle", "Dorothy", "Carol", "Amanda", "Melissa", "Deborah",
        "Stephanie", "Rebecca", "Sharon", "Laura", "Cynthia", "Kathleen", "Amy", "Shirley"
    ]

    # Common last names
    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
        "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
        "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell"
    ]

    # Countries
    COUNTRIES = [
        "United States", "Canada", "United Kingdom", "Australia", "Germany", "France",
        "Italy", "Spain", "Netherlands", "Belgium", "Switzerland", "Austria", "Sweden",
        "Norway", "Denmark", "Finland", "Ireland", "New Zealand", "Singapore", "Japan"
    ]

    @staticmethod
    def generate_username(first_name=None, last_name=None):
        """Generate a random username"""
        if not first_name:
            first_name = random.choice(DataGenerator.FIRST_NAMES_MALE + DataGenerator.FIRST_NAMES_FEMALE)
        if not last_name:
            last_name = random.choice(DataGenerator.LAST_NAMES)

        # Different username patterns
        patterns = [
            f"{first_name.lower()}{last_name.lower()}{random.randint(10, 999)}",
            f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 99)}",
            f"{first_name[0].lower()}{last_name.lower()}{random.randint(100, 9999)}",
            f"{first_name.lower()}{random.randint(1, 99)}{last_name.lower()}",
            f"{first_name.lower()}_{last_name.lower()}{random.randint(1, 999)}"
        ]

        return random.choice(patterns)

    @staticmethod
    def generate_password(length=12):
        """Generate a strong random password"""
        # Ensure password has all required character types
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*"

        # Ensure at least one of each type
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special)
        ]

        # Fill the rest randomly
        all_chars = lowercase + uppercase + digits + special
        for _ in range(length - 4):
            password.append(random.choice(all_chars))

        # Shuffle the password
        random.shuffle(password)
        return ''.join(password)

    @staticmethod
    def generate_first_name(gender=None):
        """Generate a random first name"""
        if gender == "male":
            return random.choice(DataGenerator.FIRST_NAMES_MALE)
        elif gender == "female":
            return random.choice(DataGenerator.FIRST_NAMES_FEMALE)
        else:
            # Random gender
            all_names = DataGenerator.FIRST_NAMES_MALE + DataGenerator.FIRST_NAMES_FEMALE
            return random.choice(all_names)

    @staticmethod
    def generate_last_name():
        """Generate a random last name"""
        return random.choice(DataGenerator.LAST_NAMES)

    @staticmethod
    def generate_birthday(min_age=18, max_age=65):
        """Generate a random birthday"""
        today = datetime.now()

        # Calculate date range
        max_date = today - timedelta(days=min_age * 365)
        min_date = today - timedelta(days=max_age * 365)

        # Generate random date between min and max
        time_between = max_date - min_date
        days_between = time_between.days
        random_days = random.randint(0, days_between)

        birthday = min_date + timedelta(days=random_days)

        # Return in YYYY-MM-DD format
        return birthday.strftime("%Y-%m-%d")

    @staticmethod
    def generate_country():
        """Generate a random country"""
        return random.choice(DataGenerator.COUNTRIES)


class AccountCreator:
    """Handles the actual account creation process"""

    def __init__(self):
        self.created_accounts = []
        self.config = {}

    def create_account(self, provider="gmail", browser="chrome", headless=False,
                       username=None, password=None, firstname=None, lastname=None,
                       birthdate=None, country=None, sms_service=None, sms_config=None,
                       proxies=None, auto_proxy=False, auto_generate=True):
        """
        Create a single email account

        Returns:
            dict: Account details if successful, None otherwise
        """

        # Auto-generate data if requested
        if auto_generate:
            if not firstname:
                firstname = DataGenerator.generate_first_name()
            if not lastname:
                lastname = DataGenerator.generate_last_name()
            if not birthdate:
                birthdate = DataGenerator.generate_birthday()
            if not country:
                country = DataGenerator.generate_country()
            if not username:
                username = DataGenerator.generate_username(firstname, lastname)
            if not password:
                password = DataGenerator.generate_password()

        # If ninjemail library is not available, simulate account creation
        if not NINJEMAIL_AVAILABLE:
            print(f"[SIMULATION] Would create {provider} account:")
            print(f"  Username: {username}")
            print(f"  Password: {password}")
            print(f"  Name: {firstname} {lastname}")
            print(f"  Birthday: {birthdate}")
            print(f"  Country: {country}")

            # Simulate success
            account_data = {
                "provider": provider,
                "username": username,
                "password": password,
                "firstname": firstname,
                "lastname": lastname,
                "birthdate": birthdate,
                "country": country,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "simulated"
            }

            self.created_accounts.append(account_data)
            return account_data

        try:
            # Create Ninjemail instance
            ninja = NinjemailLib(
                provider=provider,
                browser=browser,
                headless=headless
            )

            # Set SMS service if configured
            if sms_service and sms_config:
                if sms_service == "getsmscode":
                    ninja.set_getsmscode(sms_config["username"], sms_config["token"])
                elif sms_service == "smspool":
                    ninja.set_smspool(sms_config["token"])
                elif sms_service == "5sim":
                    ninja.set_5sim(sms_config["token"])

            # Create the account
            result = ninja.create(
                username=username,
                password=password,
                firstname=firstname,
                lastname=lastname,
                birthdate=birthdate,
                country=country,
                proxies=proxies,
                auto_proxy=auto_proxy
            )

            if result:
                account_data = {
                    "provider": provider,
                    "username": result.get("username", username),
                    "password": result.get("password", password),
                    "firstname": firstname,
                    "lastname": lastname,
                    "birthdate": birthdate,
                    "country": country,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "success"
                }

                self.created_accounts.append(account_data)
                return account_data

        except Exception as e:
            print(f"Error creating account: {str(e)}")
            return None

        return None

    def batch_create(self, count=1, **kwargs):
        """
        Create multiple accounts

        Args:
            count: Number of accounts to create
            **kwargs: Arguments to pass to create_account

        Returns:
            list: List of created accounts
        """
        accounts = []

        for i in range(count):
            print(f"Creating account {i + 1}/{count}...")

            # Generate new data for each account
            account = self.create_account(**kwargs)

            if account:
                accounts.append(account)
                print(f"Successfully created: {account['username']}")
            else:
                print(f"Failed to create account {i + 1}")

        return accounts

    def export_accounts(self, filename="accounts.txt", format="txt"):
        """
        Export created accounts to file

        Args:
            filename: Output filename
            format: Export format (txt or json)
        """
        if not self.created_accounts:
            print("No accounts to export")
            return False

        try:
            if format == "json":
                with open(filename, 'w') as f:
                    json.dump(self.created_accounts, f, indent=2)
            else:
                with open(filename, 'w') as f:
                    f.write("=== Created Email Accounts ===\n\n")
                    for i, account in enumerate(self.created_accounts, 1):
                        f.write(f"Account #{i}\n")
                        f.write(f"Provider: {account['provider']}\n")
                        f.write(f"Username: {account['username']}\n")
                        f.write(f"Password: {account['password']}\n")
                        f.write(f"Name: {account['firstname']} {account['lastname']}\n")
                        f.write(f"Birthday: {account['birthdate']}\n")
                        f.write(f"Country: {account['country']}\n")
                        f.write(f"Created: {account['created_at']}\n")
                        f.write(f"Status: {account.get('status', 'unknown')}\n")
                        f.write("-" * 50 + "\n\n")

            print(f"Accounts exported to {filename}")
            return True

        except Exception as e:
            print(f"Error exporting accounts: {str(e)}")
            return False

    def save_config(self, config, filename="ninjemail_config.json"):
        """Save configuration to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {str(e)}")
            return False

    def load_config(self, filename="ninjemail_config.json"):
        """Load configuration from file"""
        if not os.path.exists(filename):
            return None

        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            return None


# Utility functions for standalone use
def quick_create(provider="gmail", count=1):
    """Quick function to create accounts with defaults"""
    creator = AccountCreator()
    accounts = creator.batch_create(
        count=count,
        provider=provider,
        auto_generate=True
    )

    if accounts:
        creator.export_accounts(f"{provider}_accounts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

    return accounts


if __name__ == "__main__":
    # Example usage when run directly
    print("Ninjemail Functions Module")
    print("-" * 50)

    # Test data generation
    print("\nTesting data generation:")
    print(f"First Name: {DataGenerator.generate_first_name()}")
    print(f"Last Name: {DataGenerator.generate_last_name()}")
    print(f"Birthday: {DataGenerator.generate_birthday()}")
    print(f"Username: {DataGenerator.generate_username()}")
    print(f"Password: {DataGenerator.generate_password()}")
    print(f"Country: {DataGenerator.generate_country()}")

    # Test account creation (simulation if library not installed)
    print("\n" + "-" * 50)
    print("Testing account creation:")
    creator = AccountCreator()
    account = creator.create_account(provider="gmail", auto_generate=True)

    if account:
        print(f"\nCreated account: {account['username']}")
        creator.export_accounts("test_account.txt")
