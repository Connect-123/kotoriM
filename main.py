"""
main.py - Main entry point for Ninjemail
Can run in CLI mode or launch the GUI
"""

import sys
import argparse
import nmCore as nm
from gui import run_gui


def print_banner():
    """Print ASCII banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║     🥷  NINJEMAIL - Email Account Creator  🥷         ║
    ║                                                       ║
    ║     Automated email account creation tool            ║
    ║     Supports: Gmail, Outlook, Yahoo                  ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)


def cli_mode():
    """Command line interface mode"""
    print_banner()

    parser = argparse.ArgumentParser(description='Ninjemail - Email Account Creator')

    # Basic arguments
    parser.add_argument('-p', '--provider',
                        choices=['gmail', 'outlook', 'yahoo'],
                        default='gmail',
                        help='Email provider (default: gmail)')

    parser.add_argument('-b', '--browser',
                        choices=['chrome', 'firefox', 'undetected-chrome'],
                        default='chrome',
                        help='Browser to use (default: chrome)')

    parser.add_argument('--headless',
                        action='store_true',
                        help='Run browser in headless mode')

    parser.add_argument('-c', '--count',
                        type=int,
                        default=1,
                        help='Number of accounts to create (default: 1)')

    # Account details
    parser.add_argument('--username',
                        help='Specific username (auto-generated if not provided)')
    parser.add_argument('--password',
                        help='Specific password (auto-generated if not provided)')
    parser.add_argument('--firstname',
                        help='First name (auto-generated if not provided)')
    parser.add_argument('--lastname',
                        help='Last name (auto-generated if not provided)')
    parser.add_argument('--birthdate',
                        help='Birth date YYYY-MM-DD (auto-generated if not provided)')
    parser.add_argument('--country',
                        help='Country (auto-generated if not provided)')

    # SMS service
    parser.add_argument('--sms-service',
                        choices=['getsmscode', 'smspool', '5sim'],
                        help='SMS verification service')
    parser.add_argument('--sms-username',
                        help='Username for getsmscode')
    parser.add_argument('--sms-token',
                        help='API token for SMS service')

    # Proxy
    parser.add_argument('--proxy',
                        help='Proxy to use (format: http://ip:port)')
    parser.add_argument('--auto-proxy',
                        action='store_true',
                        help='Auto-fetch free proxies')

    # Output
    parser.add_argument('-o', '--output',
                        default='accounts.txt',
                        help='Output file (default: accounts.txt)')
    parser.add_argument('--json',
                        action='store_true',
                        help='Export as JSON instead of TXT')

    # Actions
    parser.add_argument('--generate-only',
                        action='store_true',
                        help='Only generate and display random data without creating accounts')
    parser.add_argument('--gui',
                        action='store_true',
                        help='Launch GUI mode')

    # --- Name list arguments ---
    parser.add_argument('--names-combined',
                        help='Path to file with "First Last" per line')
    parser.add_argument('--names-first',
                        help='Path to file with one first name per line')
    parser.add_argument('--names-last',
                        help='Path to file with one last name per line')

    args = parser.parse_args()

    # --- Load names if provided ---
    if any([args.names_combined, args.names_first, args.names_last]):
        nm.DataGenerator.load_names_from_files(
            combined=args.names_combined,
            first_names=args.names_first,
            last_names=args.names_last
        )

    # Launch GUI if requested
    if args.gui:
        run_gui()
        return

    # Generate only mode
    if args.generate_only:
        print("\n📊 Generated Data:")
        print("-" * 50)
        print(f"First Name:  {nm.DataGenerator.generate_first_name()}")
        print(f"Last Name:   {nm.DataGenerator.generate_last_name()}")
        print(f"Username:    {nm.DataGenerator.generate_username()}")
        print(f"Password:    {nm.DataGenerator.generate_password()}")
        print(f"Birthday:    {nm.DataGenerator.generate_birthday()}")
        print(f"Country:     {nm.DataGenerator.generate_country()}")
        print("-" * 50)
        return

    # Create accounts
    print(f"\n🚀 Creating {args.count} {args.provider} account(s)...")
    print("-" * 50)

    creator = nm.AccountCreator()

    # Prepare SMS config
    sms_config = None
    if args.sms_service:
        if args.sms_service == 'getsmscode':
            if args.sms_username and args.sms_token:
                sms_config = {"username": args.sms_username, "token": args.sms_token}
        elif args.sms_token:
            sms_config = {"token": args.sms_token}

    # Prepare proxies
    proxies = [args.proxy] if args.proxy else None

    # Create accounts
    accounts = creator.batch_create(
        count=args.count,
        provider=args.provider,
        browser=args.browser,
        headless=args.headless,
        username=args.username,
        password=args.password,
        firstname=args.firstname,
        lastname=args.lastname,
        birthdate=args.birthdate,
        country=args.country,
        sms_service=args.sms_service,
        sms_config=sms_config,
        proxies=proxies,
        auto_proxy=args.auto_proxy,
        auto_generate=True
    )

    # Export results
    if accounts:
        print("\n✅ Account Creation Summary:")
        print("-" * 50)

        for i, account in enumerate(accounts, 1):
            print(f"\n📧 Account #{i}:")
            print(f"   Provider: {account['provider']}")
            print(f"   Username: {account['username']}")
            print(f"   Password: {account['password']}")
            print(f"   Name: {account['firstname']} {account['lastname']}")
            print(f"   Birthday: {account['birthdate']}")
            print(f"   Country: {account['country']}")

        fmt = "json" if args.json else "txt"
        if creator.export_accounts(args.output, fmt):
            print(f"\n💾 Accounts exported to: {args.output}")
    else:
        print("\n❌ No accounts were created successfully")

    print("\n" + "=" * 50)
    print("Done! Thank you for using Ninjemail 🥷")


def interactive_mode():
    """Interactive CLI mode with menu"""
    print_banner()

    creator = nm.AccountCreator()

    while True:
        print("\n📋 Main Menu:")
        print("1. Create single account")
        print("2. Batch create accounts")
        print("3. Generate random data")
        print("4. Export accounts")
        print("5. Launch GUI")
        print("6. Exit")

        choice = input("\nSelect option (1-6): ").strip()

        if choice == "1":
            # Single account creation
            print("\n🔧 Account Configuration:")
            provider = input("Provider (gmail/outlook/yahoo) [gmail]: ").strip() or "gmail"

            auto = input("Auto-generate all fields? (y/n) [y]: ").strip().lower()

            if auto != 'n':
                account = creator.create_account(
                    provider=provider,
                    auto_generate=True
                )
            else:
                username = input("Username (leave empty to auto-generate): ").strip() or None
                password = input("Password (leave empty to auto-generate): ").strip() or None
                firstname = input("First name (leave empty to auto-generate): ").strip() or None
                lastname = input("Last name (leave empty to auto-generate): ").strip() or None
                birthdate = input("Birth date YYYY-MM-DD (leave empty to auto-generate): ").strip() or None
                country = input("Country (leave empty to auto-generate): ").strip() or None

                account = creator.create_account(
                    provider=provider,
                    username=username,
                    password=password,
                    firstname=firstname,
                    lastname=lastname,
                    birthdate=birthdate,
                    country=country,
                    auto_generate=True
                )

            if account:
                print("\n✅ Account created successfully!")
                print(f"Username: {account['username']}")
                print(f"Password: {account['password']}")
            else:
                print("\n❌ Failed to create account")

        elif choice == "2":
            # Batch creation
            print("\n📦 Batch Account Creation:")
            provider = input("Provider (gmail/outlook/yahoo) [gmail]: ").strip() or "gmail"
            count = input("Number of accounts [5]: ").strip()
            count = int(count) if count else 5

            print(f"\nCreating {count} {provider} accounts...")
            accounts = creator.batch_create(
                count=count,
                provider=provider,
                auto_generate=True
            )

            if accounts:
                print(f"\n✅ Successfully created {len(accounts)} accounts!")
                save = input("Save to file? (y/n) [y]: ").strip().lower()
                if save != 'n':
                    filename = input("Filename [accounts.txt]: ").strip() or "accounts.txt"
                    creator.export_accounts(filename)
            else:
                print("\n❌ No accounts were created")

        elif choice == "3":
            # Generate random data
            print("\n🎲 Random Data Generator:")
            print("-" * 40)
            print(f"First Name:  {nm.DataGenerator.generate_first_name()}")
            print(f"Last Name:   {nm.DataGenerator.generate_last_name()}")
            print(f"Username:    {nm.DataGenerator.generate_username()}")
            print(f"Password:    {nm.DataGenerator.generate_password()}")
            print(f"Birthday:    {nm.DataGenerator.generate_birthday()}")
            print(f"Country:     {nm.DataGenerator.generate_country()}")
            print("-" * 40)

        elif choice == "4":
            # Export accounts
            if not creator.created_accounts:
                print("\n⚠️ No accounts to export")
            else:
                print(f"\n💾 Exporting {len(creator.created_accounts)} accounts...")
                filename = input("Filename [accounts.txt]: ").strip() or "accounts.txt"
                format = "json" if filename.endswith('.json') else "txt"

                if creator.export_accounts(filename, format):
                    print(f"✅ Exported to {filename}")
                else:
                    print("❌ Export failed")

        elif choice == "5":
            # Launch GUI
            print("\n🚀 Launching GUI...")
            run_gui()
            break

        elif choice == "6":
            # Exit
            if creator.created_accounts:
                save = input("\n💾 Save accounts before exiting? (y/n): ").strip().lower()
                if save == 'y':
                    filename = input("Filename [accounts.txt]: ").strip() or "accounts.txt"
                    creator.export_accounts(filename)

            print("\n👋 Goodbye! Thank you for using Ninjemail 🥷")
            break

        else:
            print("\n❌ Invalid option. Please select 1-6")


def main():
    """Main entry point"""
    # Check if running with arguments
    if len(sys.argv) > 1:
        # CLI mode with arguments
        cli_mode()
    else:
        # Interactive mode
        try:
            interactive_mode()
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thank you for using Ninjemail 🥷")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    main()
