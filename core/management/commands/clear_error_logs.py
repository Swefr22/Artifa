from django.core.management.base import BaseCommand
from django.conf import settings
import os
from datetime import datetime

class Command(BaseCommand):
    help = 'Clear error logs to keep them clean'

    def handle(self, *args, **options):
        logs_dir = settings.LOGS_DIR
        error_log_file = os.path.join(logs_dir, 'errors.log')
        
        try:
            if os.path.exists(error_log_file):
                # Clear the file by opening it in write mode
                with open(error_log_file, 'w') as f:
                    f.write('')
                self.stdout.write(self.style.SUCCESS(f'✓ Error log cleared at {datetime.now()}'))
            else:
                self.stdout.write(self.style.WARNING(f'Error log file not found: {error_log_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error clearing log: {str(e)}'))
