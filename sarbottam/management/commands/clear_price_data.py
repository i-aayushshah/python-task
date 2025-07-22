from django.core.management.base import BaseCommand
from sarbottam.models import PriceHistory


class Command(BaseCommand):
    help = 'Clear all price history data from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion without prompting'
        )

    def handle(self, *args, **options):
        confirm = options.get('confirm', False)

        # Get count of existing records
        count = PriceHistory.objects.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS('No price history data found. Database is already clean.'))
            return

        self.stdout.write(f'Found {count} price history records in the database.')

        if not confirm:
            response = input('Are you sure you want to delete ALL price history data? (yes/no): ')
            if response.lower() != 'yes':
                self.stdout.write(self.style.WARNING('Operation cancelled.'))
                return

        try:
            # Delete all price history records
            deleted_count, _ = PriceHistory.objects.all().delete()

            self.stdout.write(
                self.style.SUCCESS(
                    f'🗑️  Successfully deleted {deleted_count} price history records!\n'
                    f'Database is now clean and ready for fresh data.'
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred while deleting data: {str(e)}'))
