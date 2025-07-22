#!/usr/bin/env python3
"""
Test script to verify Django project setup
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cement_profile_app.settings')
django.setup()

def test_models():
    """Test model imports and basic functionality"""
    try:
        from sarbottam.models import Company, CompanyNews, CompanyFinancial, CompanyAchievement
        print("✅ Models imported successfully")

        # Test model creation (without saving to database)
        company = Company(
            name="Test Company",
            symbol="TEST",
            sector="Test Sector"
        )
        print("✅ Company model can be instantiated")

        news = CompanyNews(
            company=company,
            news_title="Test News",
            news_body="Test content"
        )
        print("✅ CompanyNews model can be instantiated")

        return True
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def test_views():
    """Test view imports"""
    try:
        from sarbottam import views
        print("✅ Views imported successfully")

        # Check if required view functions exist
        required_views = [
            'company_profile', 'news_list', 'news_detail',
            'financial_data', 'achievements'
        ]

        for view_name in required_views:
            if hasattr(views, view_name):
                print(f"✅ View '{view_name}' exists")
            else:
                print(f"❌ View '{view_name}' missing")
                return False

        return True
    except Exception as e:
        print(f"❌ View test failed: {e}")
        return False

def test_urls():
    """Test URL configuration"""
    try:
        from sarbottam import urls
        print("✅ URLs imported successfully")
        return True
    except Exception as e:
        print(f"❌ URL test failed: {e}")
        return False

def test_admin():
    """Test admin configuration"""
    try:
        from sarbottam import admin
        print("✅ Admin configuration imported successfully")
        return True
    except Exception as e:
        print(f"❌ Admin test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Django Project Setup")
    print("=" * 50)

    tests = [
        ("Models", test_models),
        ("Views", test_views),
        ("URLs", test_urls),
        ("Admin", test_admin),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}...")
        result = test_func()
        results.append((test_name, result))

    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)

    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1

    print(f"\n🎯 {passed}/{len(tests)} tests passed")

    if passed == len(tests):
        print("\n🎉 All tests passed! Your Django project is ready.")
        print("\n📋 Next steps:")
        print("1. Run: python manage.py makemigrations")
        print("2. Run: python manage.py migrate")
        print("3. Run: python manage.py add_sample_data")
        print("4. Run: python manage.py runserver")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")

    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
