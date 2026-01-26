from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        """Initialize the app"""
        # Start log cleaner scheduler when Django starts
        try:
            from .scheduler import start_log_cleaner_scheduler
            start_log_cleaner_scheduler()
        except Exception as e:
            print(f'Warning: Could not start log cleaner scheduler: {str(e)}')
