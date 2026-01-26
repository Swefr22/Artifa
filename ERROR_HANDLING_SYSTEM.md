# Error Handling & Logging System

## Overview
A comprehensive error tracking and logging system for ARTIFA FEST that captures, logs, and displays all HTTP errors and exceptions.

## System Architecture

### 1. Three-Layer Error Persistence

#### Database Layer
- **Model**: `ErrorLog` (core/models.py)
- **Fields**:
  - `status_code`: HTTP status code (400, 403, 404, 500, etc.)
  - `error_type`: Friendly error name (e.g., "Not Found", "Forbidden")
  - `method`: HTTP method (GET, POST, PUT, DELETE)
  - `path`: URL path where error occurred
  - `query_string`: Query parameters (if any)
  - `client_ip`: IP address of requesting client
  - `user_agent`: Browser/client user agent string
  - `error_message`: Detailed error message/traceback
  - `timestamp`: When error occurred (auto-set)
  - `resolved`: Boolean flag for marking errors as resolved
  - `resolution_notes`: Admin notes about error resolution
- **Indexes**: On timestamp, status_code, path for fast queries
- **Migration**: Applied as 0003_errorlog.py

#### File Logging Layer
- **Configuration**: Django logging with rotating file handlers
- **Log Files** (in `logs/` directory):
  - `errors.log`: All errors and exceptions
  - `requests.log`: HTTP request-specific errors
  - `app.log`: Application debug logs
- **Rotation**: 10MB per file with 10 backup files
- **Format**: Verbose format with levelname, timestamp, module, process, thread

#### User Interface Layer
- **Middleware**: `ErrorLogMiddleware` (core/middleware.py)
  - Intercepts all requests before Django processing
  - Captures 4xx and 5xx HTTP responses
  - Catches exceptions with full tracebacks
  - Logs to both database and files with error handling
- **Custom Error Pages**:
  - `templates/404.html`: Page Not Found (with theme styling)
  - `templates/500.html`: Server Error (with error tracking ID)
  - `templates/403.html`: Access Forbidden (with permission info)
  - `templates/400.html`: Bad Request (with form validation hints)
- **Admin Interface**: ErrorLogAdmin in core/admin.py
  - View all logged errors with filtering
  - Search by path, client IP, error message
  - Filter by status code, error type, timestamp, resolution status
  - Read-only access with superuser-only delete
  - Organized fieldsets: Error Info, Request Details, Resolution

### 2. Error Capture Flow

```
User Request
    ↓
ErrorLogMiddleware.__call__()
    ↓
    ├─ Success (2xx/3xx) → Pass through
    ├─ Error (4xx/5xx) → log_error()
    └─ Exception → log_exception()
    ↓
log_error()/log_exception()
    ├─ Write to logs/errors.log (rotating)
    ├─ Write to ErrorLog table
    └─ Return response (4xx/5xx) or re-raise exception
    ↓
Django Error Handler
    ↓
Custom Error Template (404.html, 500.html, etc.)
```

### 3. Components

#### Middleware
**File**: `core/middleware.py`
- `ErrorLogMiddleware`: Main middleware class
  - `__call__()`: Entry point for all requests
  - `log_error()`: Logs HTTP errors to file and database
  - `log_exception()`: Logs exceptions with stack traces
  - `get_client_ip()`: Extracts IP from X-Forwarded-For or REMOTE_ADDR
  - `get_error_type()`: Maps status codes to friendly names
  - `get_error_message()`: Extracts error content from response

#### Error Handlers
**File**: `core/views.py` (lines 683-712)
- `error_404(request)`: Handles 404 Not Found
  - Logs warning to logger
  - Returns 404.html
- `error_500(request)`: Handles 500 Server Error
  - Generates unique error ID (UUID)
  - Logs error with ID for tracking
  - Returns 500.html with error_id context
- `error_403(request)`: Handles 403 Forbidden
  - Returns 403.html
- `error_400(request)`: Handles 400 Bad Request
  - Returns 400.html

#### Admin Interface
**File**: `core/admin.py` (lines 103-130)
- `ErrorLogAdmin`: ModelAdmin for viewing error logs
  - **List Display**: status_code, error_type, method, path, client_ip, timestamp, resolved
  - **Filters**: By status_code, error_type, timestamp, resolved
  - **Search**: By path, client_ip, error_message
  - **Read-only fields**: All fields are read-only
  - **Fieldsets**:
    1. Error Info (status_code, error_type, error_message)
    2. Request Details (method, path, query_string, client_ip, user_agent)
    3. Resolution (timestamp, resolved, resolution_notes)

#### Settings Configuration
**File**: `artifa_fest/settings.py`
- Added ErrorLogMiddleware to MIDDLEWARE list
- Configured Django logging with:
  - 4 Formatters (verbose, simple, json)
  - 4 Handlers (console, error_file, request_file, app_file)
  - 3 Loggers (django, django.request, core)
  - Rotating file handler (10MB, 10 backups)
- Changed DEBUG = False to enable custom error pages
- Updated ALLOWED_HOSTS for production

#### URL Configuration
**File**: `core/urls.py` (lines 33-36)
- Registered error handlers:
  - handler404 = views.error_404
  - handler500 = views.error_500
  - handler403 = views.error_403
  - handler400 = views.error_400

#### Error Templates
**Location**: `templates/`
- `404.html`: Professional 404 page with:
  - Large "404" error code with glow effect
  - Descriptive title and message
  - Alert box explaining what happened
  - 3 action buttons (Home, Back, Report)
  - Quick links to main pages
  - Smooth slideUp animation
- `500.html`: Server error page with:
  - Error tracking ID display
  - Timestamp
  - Advice for users (refresh, clear cache, contact support)
  - Professional styling
  - Shake animation on load
- `403.html`: Forbidden access page
- `400.html`: Bad request page

## Testing

### Access the Error Log Admin
1. Navigate to: `http://localhost:8000/admin/`
2. Go to: "Core" → "Error Logs"
3. View all captured errors with filtering/searching

### View Recent Errors
```bash
python manage.py shell
from core.models import ErrorLog
errors = ErrorLog.objects.all().order_by('-timestamp')[:10]
for error in errors:
    print(f"[{error.status_code}] {error.error_type}: {error.method} {error.path}")
```

### Check Log Files
```bash
# View recent errors
tail -f logs/errors.log
# View all logs
tail -f logs/app.log
```

## Usage Examples

### 1. Mark Error as Resolved
In Django admin, click on an error and set:
- `resolved` = ✓ checked
- `resolution_notes` = "Fixed database connection issue"

### 2. Track User Impact
View errors by client IP to see which users are affected:
- Filter by `client_ip`
- Group errors by status code to see patterns

### 3. Monitor Error Trends
Use timestamp filter to see errors over time:
- Last 24 hours: View recent errors
- By date range: Identify recurring issues

## Error Handling Coverage

| Status Code | Error Type | Handling |
|---|---|---|
| 400 | Bad Request | Logged + custom page |
| 403 | Forbidden | Logged + custom page |
| 404 | Not Found | Logged + custom page |
| 500 | Server Error | Logged + error ID + custom page |
| 502 | Bad Gateway | Logged |
| 503 | Service Unavailable | Logged |

## Performance Considerations

- **Database**: Indexes on timestamp, status_code, path for fast queries
- **File Logging**: Rotating handler prevents disk space issues
- **Error Handling**: All logging wrapped in try-except to prevent cascading failures
- **Middleware**: Minimal overhead - only processes 4xx+ responses

## Security

- **Read-Only Access**: Error logs are read-only in admin (prevents data loss)
- **User-Agent Limiting**: User agent truncated to 500 chars
- **Error Message Limiting**: Error messages truncated to 1000 chars
- **Superuser Only**: Delete operations restricted to superuser
- **IP Tracking**: Records client IP for security auditing

## Logging Levels

- **DEBUG**: Application debug logs (app.log)
- **INFO**: General information and request logs
- **ERROR**: All 4xx/5xx errors and exceptions (errors.log)
- **WARNING**: 4xx client errors (less severe)

## Files Modified/Created

### Created
- `core/middleware.py`: ErrorLogMiddleware
- `core/migrations/0003_errorlog.py`: Database migration
- `templates/403.html`: Forbidden error page
- `templates/400.html`: Bad request error page
- `logs/` directory: Auto-created for log files

### Modified
- `core/models.py`: Added ErrorLog model
- `core/admin.py`: Added ErrorLogAdmin
- `core/views.py`: Added 4 error handlers
- `core/urls.py`: Registered error handlers
- `artifa_fest/settings.py`: Added logging config, DEBUG=False, middleware

## Troubleshooting

### Errors Not Showing Up
1. Check DEBUG = False in settings
2. Verify middleware is in MIDDLEWARE list
3. Check logs/ directory exists
4. Verify database migration applied: `python manage.py showmigrations core`

### Custom Error Pages Not Displaying
1. Ensure DEBUG = False in settings
2. Verify templates exist in templates/ directory
3. Check template names in error handlers
4. Restart server after settings change

### Logs Not Writing
1. Check logs/ directory permissions
2. Verify LOGGING configuration in settings
3. Check django and core loggers are configured
4. Monitor disk space (rotating handler prevents overflow)
