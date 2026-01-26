import os
from django.conf import settings
from datetime import datetime

def clear_error_logs():
    """Clear error logs automatically"""
    logs_dir = settings.LOGS_DIR
    error_log_file = os.path.join(logs_dir, 'errors.log')
    
    try:
        if os.path.exists(error_log_file):
            with open(error_log_file, 'w') as f:
                f.write('')
            print(f'[LOG CLEANUP] Error log cleared at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        else:
            print(f'[LOG CLEANUP] Warning: Error log file not found: {error_log_file}')
    except Exception as e:
        print(f'[LOG CLEANUP] Error clearing log: {str(e)}')

def clear_all_logs():
    """Clear all log files"""
    logs_dir = settings.LOGS_DIR
    log_files = ['errors.log', 'requests.log', 'app.log']
    
    for log_file in log_files:
        try:
            file_path = os.path.join(logs_dir, log_file)
            if os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    f.write('')
                print(f'[LOG CLEANUP] {log_file} cleared at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            else:
                print(f'[LOG CLEANUP] Warning: {log_file} not found: {file_path}')
        except Exception as e:
            print(f'[LOG CLEANUP] Error clearing {log_file}: {str(e)}')
