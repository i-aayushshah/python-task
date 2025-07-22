from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd
from django.core.management.base import BaseCommand
from datetime import datetime
from decimal import Decimal, InvalidOperation
from sarbottam.models import Company, PriceHistory
import os


class Command(BaseCommand):
    help = 'Scrape price history data for Sarbottam Cement from NEPSE website using Selenium'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=20,
            help='Number of records to scrape (default: 20)'
        )
        parser.add_argument(
            '--headless',
            action='store_true',
            help='Run Chrome in headless mode (default: True)'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        headless = options.get('headless', True)

        self.stdout.write(self.style.SUCCESS(f'Starting to scrape {limit} price history records from NEPSE...'))

        try:
            # Get or create the company
            company, created = Company.objects.get_or_create(
                symbol='SARBTM',
                defaults={'name': 'Sarbottam Cement Limited'}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created company: {company.name}'))

            # Scrape data from NEPSE using Selenium
            scraped_data = self.scrape_nepse_data(limit, headless)

            if not scraped_data:
                self.stdout.write(self.style.ERROR('No data found to scrape'))
                return

            # Save data to database
            created_count = 0
            updated_count = 0

            for data in scraped_data:
                try:
                    price_history, created = PriceHistory.objects.update_or_create(
                        company=company,
                        date=data['date'],
                        defaults={
                            'open_price': data['open_price'],
                            'high_price': data['high_price'],
                            'low_price': data['low_price'],
                            'close_price': data['close_price'],
                            'percentage_change': data.get('percentage_change', Decimal('0.00')),
                            'volume': data.get('volume', 0),
                            'turnover': data.get('turnover', Decimal('0.00')),
                        }
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(f'✓ Created: {data["date"]} - NPR {data["close_price"]}')
                    else:
                        updated_count += 1
                        self.stdout.write(f'↻ Updated: {data["date"]} - NPR {data["close_price"]}')

                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Error saving data for {data.get("date", "unknown date")}: {str(e)}'))
                    continue

            self.stdout.write(
                self.style.SUCCESS(
                    f'\n🎉 Scraping completed!\n'
                    f'Created: {created_count} records\n'
                    f'Updated: {updated_count} records\n'
                    f'Total processed: {len(scraped_data)} records'
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))

    def scrape_nepse_data(self, limit, headless=True):
        """Scrape price history data from NEPSE website using Selenium"""
        driver = None

        try:
            self.stdout.write('Setting up Chrome WebDriver...')

            # Set up Chrome options
            chrome_options = Options()
            if headless:
                chrome_options.add_argument("--headless")  # Run in background
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")

            # Check if Chrome driver is in the drivers folder
            driver_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'drivers', 'chromedriver.exe')

            if os.path.exists(driver_path):
                self.stdout.write(f'Using Chrome driver from: {driver_path}')
                driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
            else:
                self.stdout.write('Using system Chrome driver...')
                driver = webdriver.Chrome(options=chrome_options)

            # Open the NEPSE page for SARBTM
            url = "https://www.nepalstock.com/company/detail/9242"  # SARBTM company ID on NEPSE
            self.stdout.write(f'Opening NEPSE page: {url}')
            driver.get(url)

            # Wait for page to load
            self.stdout.write('Waiting for page to load...')
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(3)

            # Click on the "Price History" tab
            self.stdout.write('Clicking on Price History tab...')
            try:
                price_history_tab = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "pricehistory-tab"))
                )
                price_history_tab.click()
                self.stdout.write('✓ Price History tab clicked')
            except TimeoutException:
                # Try alternative selectors
                try:
                    price_history_tab = driver.find_element(By.XPATH, "//a[contains(text(), 'Price History')]")
                    price_history_tab.click()
                    self.stdout.write('✓ Price History tab clicked (alternative method)')
                except NoSuchElementException:
                    self.stdout.write(self.style.WARNING('Price History tab not found, trying to proceed...'))

            # Wait for price history data to load
            self.stdout.write('Waiting for price history data to load...')
            time.sleep(5)

            # Collect data from multiple pages if needed
            scraped_data = []
            current_page = 1
            records_needed = limit

            while len(scraped_data) < records_needed and current_page <= 5:  # Limit to 5 pages max
                self.stdout.write(f'Scraping page {current_page}...')

                # Try multiple selectors for the table
                table_selectors = [
                    "#pricehistorys tbody tr",
                    ".price-history tbody tr",
                    "table tbody tr",
                    ".table tbody tr"
                ]

                rows = []
                for selector in table_selectors:
                    try:
                        rows = driver.find_elements(By.CSS_SELECTOR, selector)
                        if rows:
                            self.stdout.write(f'✓ Found {len(rows)} rows on page {current_page} using selector: {selector}')
                            break
                    except:
                        continue

                if not rows:
                    self.stdout.write(self.style.WARNING(f'No table rows found on page {current_page}'))
                    break

                # Extract data from current page
                page_data = []
                records_from_page = min(len(rows), records_needed - len(scraped_data))

                for i, row in enumerate(rows[:records_from_page]):
                    try:
                        cols = row.find_elements(By.TAG_NAME, "td")
                        if len(cols) >= 7:  # Ensure we have enough columns

                            # Skip if first column is not a number (header row)
                            try:
                                int(cols[0].text.strip())
                            except ValueError:
                                continue

                            # Extract data based on NEPSE table structure:
                            # Column 0: Serial Number (1, 2, 3...)
                            # Column 1: Date (2025-07-21)
                            # Column 2: Open (888.90)
                            # Column 3: High (896.00)
                            # Column 4: Low (880.00)
                            # Column 5: Close (892.88)
                            # Column 6: Volume (79,473)
                            date_str = cols[1].text.strip()
                            open_price = self.clean_price(cols[2].text.strip())
                            high_price = self.clean_price(cols[3].text.strip())
                            low_price = self.clean_price(cols[4].text.strip())
                            close_price = self.clean_price(cols[5].text.strip())
                            volume = self.clean_volume(cols[6].text.strip())

                            if not date_str or not close_price:
                                continue

                            # Parse date
                            try:
                                date_obj = self.parse_date(date_str)
                                if not date_obj:
                                    continue
                            except Exception:
                                continue

                            data_point = {
                                'date': date_obj,
                                'open_price': open_price or close_price,
                                'high_price': high_price or close_price,
                                'low_price': low_price or close_price,
                                'close_price': close_price,
                                'volume': volume,
                            }

                            page_data.append(data_point)
                            self.stdout.write(f'✓ Page {current_page}, Row {i+1}: {date_obj} - NPR {close_price}')

                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'Error parsing page {current_page}, row {i+1}: {str(e)}'))
                        continue

                scraped_data.extend(page_data)
                self.stdout.write(f'Collected {len(page_data)} records from page {current_page}. Total: {len(scraped_data)}')

                # Check if we have enough data
                if len(scraped_data) >= records_needed:
                    break

                # Try to go to next page
                try:
                    # Look for pagination next button
                    next_selectors = [
                        "a[aria-label='Next page']",
                        ".pagination-next a",
                        ".ngx-pagination .pagination-next a",
                        "li.pagination-next a",
                        ".next",
                        ".page-next"
                    ]

                    next_clicked = False
                    for selector in next_selectors:
                        try:
                            next_button = driver.find_element(By.CSS_SELECTOR, selector)
                            if next_button.is_enabled() and next_button.is_displayed():
                                driver.execute_script("arguments[0].click();", next_button)
                                self.stdout.write(f'✓ Clicked next page button using: {selector}')
                                next_clicked = True
                                break
                        except:
                            continue

                    if not next_clicked:
                        # Try clicking page number
                        try:
                            page_number = current_page + 1
                            page_link = driver.find_element(By.XPATH, f"//a[contains(text(), '{page_number}')]")
                            driver.execute_script("arguments[0].click();", page_link)
                            self.stdout.write(f'✓ Clicked page {page_number}')
                            next_clicked = True
                        except:
                            pass

                    if not next_clicked:
                        self.stdout.write(f'Could not find next page button. Stopping at page {current_page}')
                        break

                    # Wait for new page to load
                    time.sleep(3)
                    current_page += 1

                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Error navigating to next page: {str(e)}'))
                    break

            self.stdout.write(self.style.SUCCESS(f'Successfully scraped {len(scraped_data)} records from NEPSE'))
            return scraped_data

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during scraping: {str(e)}'))
            return []

        finally:
            if driver:
                try:
                    driver.quit()
                    self.stdout.write('Chrome driver closed successfully')
                except:
                    pass

    def clean_price(self, price_str):
        """Clean and convert price string to Decimal"""
        try:
            # Remove commas, currency symbols, and extra spaces
            cleaned = price_str.replace(',', '').replace('Rs.', '').replace('NPR', '').strip()
            if not cleaned or cleaned == '-' or cleaned.lower() == 'n/a':
                return Decimal('0.00')
            return Decimal(cleaned)
        except (ValueError, TypeError, InvalidOperation):
            return Decimal('0.00')

    def clean_volume(self, volume_str):
        """Clean and convert volume string to integer"""
        try:
            # Remove commas and convert to integer
            cleaned = volume_str.replace(',', '').strip()
            if not cleaned or cleaned == '-' or cleaned.lower() == 'n/a':
                return 0
            return int(float(cleaned))
        except (ValueError, TypeError):
            return 0

    def is_valid_date(self, date_str):
        """Check if string looks like a valid date"""
        if not date_str or len(date_str) < 8:
            return False

        # Check for common date patterns
        date_patterns = [
            r'\d{4}-\d{1,2}-\d{1,2}',  # 2024-01-15
            r'\d{1,2}/\d{1,2}/\d{4}',  # 01/15/2024 or 15/01/2024
            r'\d{1,2}-\d{1,2}-\d{4}',  # 01-15-2024 or 15-01-2024
            r'\d{4}/\d{1,2}/\d{1,2}',  # 2024/01/15
        ]

        import re
        for pattern in date_patterns:
            if re.match(pattern, date_str.strip()):
                return True
        return False

    def parse_date(self, date_str):
        """Parse date string into date object"""
        if not date_str:
            return None

        try:
            # Try different date formats
            date_formats = [
                '%Y-%m-%d',    # 2024-01-15
                '%m/%d/%Y',    # 01/15/2024
                '%d/%m/%Y',    # 15/01/2024
                '%Y/%m/%d',    # 2024/01/15
                '%m-%d-%Y',    # 01-15-2024
                '%d-%m-%Y',    # 15-01-2024
                '%Y%m%d',      # 20240115
            ]

            cleaned_date = date_str.strip()

            for fmt in date_formats:
                try:
                    return datetime.strptime(cleaned_date, fmt).date()
                except ValueError:
                    continue

            return None

        except Exception:
            return None
