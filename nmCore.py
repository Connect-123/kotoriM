"""
ninjemail.py - Core functions for email account creation
Handles all the business logic and account generation
"""

import random
import string
from datetime import datetime, timedelta
import json
import os
import warnings
from typing import List, Optional

try:
    import sys
    import os

    # Add the current directory to Python path if not already there
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    from ninjemail import Ninjemail as NinjemailLib

    NINJEMAIL_AVAILABLE = True
    print(f"Successfully imported Ninjemail from {NinjemailLib.__module__}")
except ImportError as e:
    NINJEMAIL_AVAILABLE = False
    NinjemailLib = None
    print(f"Import error details: {e}")
    import traceback

    traceback.print_exc()


class DataGenerator:
    """Generates random data for account creation"""

    # Built-in fallback lists
    FIRST_NAMES_MALE = [
        "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
        "Thomas", "Christopher", "Charles", "Daniel", "Matthew", "Anthony", "Mark",
        "Donald", "Steven", "Kenneth", "Andrew", "Joshua", "Kevin", "Brian",
        "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan", "Jacob"
    ]

    FIRST_NAMES_FEMALE = [
        "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica",
        "Sarah", "Karen", "Nancy", "Betty", "Margaret", "Sandra", "Ashley", "Kimberly",
        "Emily", "Donna", "Michelle", "Dorothy", "Carol", "Amanda", "Melissa", "Deborah",
        "Stephanie", "Rebecca", "Sharon", "Laura", "Cynthia", "Kathleen", "Amy", "Shirley"
    ]

    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
        "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
        "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell"
    ]

    COUNTRIES = [
        "United States", "Canada", "United Kingdom", "Australia", "Germany", "France",
        "Italy", "Spain", "Netherlands", "Belgium", "Switzerland", "Austria", "Sweden",
        "Norway", "Denmark", "Finland", "Ireland", "New Zealand", "Singapore", "Japan"
    ]

    # --- NEW: runtime name pools (default to built-ins; can be overwritten) ---
    _FIRST_POOL: Optional[List[str]] = None
    _LAST_POOL: Optional[List[str]] = None

    @staticmethod
    def load_names_from_files(
            combined: Optional[str] = None,
            first_names: Optional[str] = None,
            last_names: Optional[str] = None
    ):
        """
        Load large name lists from text files.

        combined: text file, one person per line: "First Last"
        first_names: text file, one first name per line
        last_names:  text file, one last name per line
        """
        firsts, lasts = [], []

        def read_lines(path):
            with open(path, "r", encoding="utf-8") as f:
                return [ln.strip() for ln in f if ln.strip()]

        # Prefer combined if provided
        if combined:
            for ln in read_lines(combined):
                parts = ln.replace(",", " ").split()
                if len(parts) >= 2:
                    firsts.append(parts[0].strip())
                    lasts.append(parts[-1].strip())

        # Or separate files
        if first_names:
            firsts.extend(read_lines(first_names))
        if last_names:
            lasts.extend(read_lines(last_names))

        # Deduplicate while preserving order
        def dedup(seq):
            seen = set()
            out = []
            for x in seq:
                if x not in seen:
                    seen.add(x)
                    out.append(x)
            return out

        firsts = dedup(firsts)
        lasts = dedup(lasts)

        if firsts:
            DataGenerator._FIRST_POOL = firsts
        if lasts:
            DataGenerator._LAST_POOL = lasts

    # --- Generators using pools if available ---
    @staticmethod
    def generate_first_name(gender=None):
        pool = (DataGenerator._FIRST_POOL
                if DataGenerator._FIRST_POOL
                else DataGenerator.FIRST_NAMES_MALE + DataGenerator.FIRST_NAMES_FEMALE)
        return random.choice(pool)

    @staticmethod
    def generate_last_name():
        pool = DataGenerator._LAST_POOL if DataGenerator._LAST_POOL else DataGenerator.LAST_NAMES
        return random.choice(pool)

    @staticmethod
    def generate_username(first_name=None, last_name=None):
        if not first_name:
            first_name = DataGenerator.generate_first_name()
        if not last_name:
            last_name = DataGenerator.generate_last_name()

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

        all_chars = lowercase + uppercase + digits + special
        for _ in range(length - 4):
            password.append(random.choice(all_chars))

        random.shuffle(password)
        return ''.join(password)

    @staticmethod
    def generate_birthday(min_age=18, max_age=65):
        today = datetime.now()
        max_date = today - timedelta(days=min_age * 365)
        min_date = today - timedelta(days=max_age * 365)

        time_between = max_date - min_date
        days_between = time_between.days
        random_days = random.randint(0, days_between)

        birthday = min_date + timedelta(days=random_days)
        return birthday.strftime("%Y-%m-%d")

    @staticmethod
    def generate_country():
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
            warnings.warn(
                "ninjemail library not found; running in simulation mode. "
                "Install with 'pip install ninjemail' for real account creation.",
                RuntimeWarning,
            )
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
            # Prepare SMS keys dictionary
            sms_keys = {}
            if sms_service and sms_config:
                if sms_service == "getsmscode":
                    # getsmscode expects username and token
                    sms_keys[sms_service] = {
                        "username": sms_config.get("username"),
                        "token": sms_config.get("token")
                    }
                else:
                    # smspool and 5sim expect just a token
                    sms_keys[sms_service] = sms_config.get("token")

            # Prepare captcha keys (empty for now, can be extended later)
            captcha_keys = {}

            # Convert birthdate from YYYY-MM-DD to MM-DD-YYYY format for ninjemail
            birthdate_formatted = birthdate
            if birthdate and "-" in birthdate:
                try:
                    # Parse YYYY-MM-DD
                    parts = birthdate.split("-")
                    if len(parts) == 3:
                        year, month, day = parts
                        # Convert to MM-DD-YYYY for ninjemail
                        birthdate_formatted = f"{month.zfill(2)}-{day.zfill(2)}-{year}"
                except:
                    pass  # Keep original format if parsing fails

            # Create Ninjemail instance with correct parameters
            ninja = NinjemailLib(
                browser=browser,
                captcha_keys=captcha_keys,
                sms_keys=sms_keys,
                proxies=proxies,
                auto_proxy=auto_proxy
            )

            # Call the appropriate method based on provider
            result = None
            if provider.lower() == "gmail":
                result = ninja.create_gmail_account(
                    username=username,
                    password=password,
                    first_name=firstname,
                    last_name=lastname,
                    birthdate=birthdate_formatted,
                    use_proxy=(proxies is not None or auto_proxy)
                )
            elif provider.lower() == "outlook":
                result = ninja.create_outlook_account(
                    username=username,
                    password=password,
                    first_name=firstname,
                    last_name=lastname,
                    country=country,
                    birthdate=birthdate_formatted,
                    hotmail=False,
                    use_proxy=(proxies is not None or auto_proxy)
                )
            elif provider.lower() == "yahoo":
                result = ninja.create_yahoo_account(
                    username=username,
                    password=password,
                    first_name=firstname,
                    last_name=lastname,
                    birthdate=birthdate_formatted,
                    use_proxy=(proxies is not None or auto_proxy)
                )
            else:
                print(f"Unsupported provider: {provider}")
                return None

            if result:
                # Result might be a tuple (username, password) or dict
                if isinstance(result, tuple):
                    actual_username, actual_password = result
                elif isinstance(result, dict):
                    actual_username = result.get("email", username)
                    actual_password = result.get("password", password)
                else:
                    actual_username = username
                    actual_password = password

                account_data = {
                    "provider": provider,
                    "username": actual_username,
                    "password": actual_password,
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
            import traceback
            traceback.print_exc()
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
