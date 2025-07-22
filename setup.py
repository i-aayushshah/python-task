#!/usr/bin/env python3
"""
Setup script for Sarbottam Cement Limited Company Profile Website
This script helps set up the Django project with all necessary configurations.
"""

import os
import sys
import subprocess


def run_command(command, description):
    """Run a command and print the result"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ SUCCESS: {description}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: {description}")
        print(f"Error output: {e.stderr}")
        return False


def main():
    """Main setup function"""
    print("""
    🏢 Sarbottam Cement Limited - Company Profile Website Setup
    ============================================================

    This script will help you set up the Django project with:
    ✓ Database migrations
    ✓ Sample company data
    ✓ Admin superuser (optional)
    ✓ Static files collection

    """)

    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: It's recommended to run this in a virtual environment")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return

    # Install requirements
    print("\n📦 Installing Python packages...")
    if not run_command("pip install -r requirements.txt", "Installing required packages"):
        print("❌ Failed to install requirements. Please install manually.")
        return

    # Make migrations
    print("\n🗃️  Creating database migrations...")
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        print("❌ Failed to create migrations.")
        return

    if not run_command("python manage.py makemigrations sarbottam", "Creating sarbottam app migrations"):
        print("❌ Failed to create sarbottam migrations.")
        return

    # Apply migrations
    print("\n🗄️  Applying database migrations...")
    if not run_command("python manage.py migrate", "Applying migrations"):
        print("❌ Failed to apply migrations.")
        return

    # Add sample data
    print("\n📊 Adding sample company data...")
    if not run_command("python manage.py add_sample_data", "Adding sample data for Sarbottam Cement"):
        print("❌ Failed to add sample data.")
        return

    # Create superuser (optional)
    print("\n👤 Creating admin superuser...")
    create_superuser = input("Would you like to create an admin superuser? (Y/n): ")
    if create_superuser.lower() != 'n':
        print("Please enter superuser details:")
        if not run_command("python manage.py createsuperuser", "Creating admin superuser"):
            print("❌ Failed to create superuser.")

    # Collect static files (if needed)
    print("\n📁 Collecting static files...")
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("⚠️  Static files collection failed (this is normal for development)")

    print(f"""

    🎉 Setup completed successfully!
    ================================

    Your Sarbottam Cement company profile website is ready!

    📋 Next Steps:
    1. Update database credentials in secret.py (if using MySQL)
    2. Start the development server: python manage.py runserver
    3. Visit: http://127.0.0.1:8000
    4. Admin panel: http://127.0.0.1:8000/admin

    📖 Features Available:
    ✅ Company profile page with comprehensive information
    ✅ News section with sample articles
    ✅ Financial data and stock information
    ✅ Achievement showcase
    ✅ Responsive design with Tailwind CSS
    ✅ Admin interface for content management

    💡 Tips:
    - Default database is SQLite (no MySQL setup required)
    - Sample data includes 3 news articles and financial reports
    - All templates use modern Tailwind CSS styling
    - Images can be uploaded through the admin interface

    🔧 For MySQL setup:
    1. Create database: CREATE DATABASE sarbottam_cement_db;
    2. Update secret.py with your MySQL credentials
    3. Run: python manage.py migrate

    Happy coding! 🚀
    """)


if __name__ == "__main__":
    main()
