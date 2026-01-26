import logging

logger = logging.getLogger(__name__)

scheduler = None

def start_log_cleaner_scheduler():
    """Start the background scheduler to clear logs every 5 minutes"""
    global scheduler
    
    if scheduler is None:
        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            from apscheduler.triggers.interval import IntervalTrigger
            from .log_cleaner import clear_error_logs
            
            scheduler = BackgroundScheduler()
            
            # Schedule log cleanup every 5 minutes
            scheduler.add_job(
                clear_error_logs,
                trigger=IntervalTrigger(minutes=5),
                id='clear_error_logs',
                name='Clear error logs every 5 minutes',
                replace_existing=True
            )
            
            scheduler.start()
            logger.info('Log cleaner scheduler started - Error logs will be cleared every 5 minutes')
        except ImportError:
            logger.warning('APScheduler not available. Error logs will not be auto-cleared.')
        except Exception as e:
            logger.error(f'Failed to start log cleaner scheduler: {str(e)}')

def stop_log_cleaner_scheduler():
    """Stop the background scheduler"""
    global scheduler
    
    if scheduler is not None:
        try:
            scheduler.shutdown()
            logger.info('Log cleaner scheduler stopped')
        except Exception as e:
            logger.error(f'Failed to stop log cleaner scheduler: {str(e)}')
