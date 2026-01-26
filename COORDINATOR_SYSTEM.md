# Coordinator Management System

## Overview
A complete coordinator management system has been added to ARTIFA FEST, allowing admins to:
1. **Add coordinators** for events with their details
2. **Edit coordinators** information
3. **Delete coordinators** from events
4. **View coordinators** on the About page with dynamic data from database

## New Database Model

### Coordinator Model
**File**: `core/models.py`
- **Fields**:
  - `event`: ForeignKey to Event (cascade delete)
  - `name`: Coordinator name
  - `register_number`: Student register number
  - `year`: Year choices (1st, 2nd, 3rd, 4th)
  - `event_type`: Technical or Non-Technical
  - `created_at`: Auto timestamp
- **Meta**: Ordered by -created_at

### Updated Event Model
**File**: `core/models.py`
- **New Fields**:
  - `duration`: Event duration (e.g., "7 hours")
  - `venue`: Event location/venue
- **Relationship**: One-to-Many with Coordinator

## New Views

**File**: `core/views.py`

### 1. `manage_coordinators(request, event_id=None)`
- Lists all coordinators (or for specific event if provided)
- Admin-only access
- Shows coordinator details and action buttons

### 2. `add_coordinator(request, event_id=None)`
- Form to add new coordinator
- Pre-fills event if event_id provided
- Requires: name, register_number, year, event_type

### 3. `edit_coordinator(request, coordinator_id)`
- Edit existing coordinator information
- Pre-fills form with current data
- Redirects back to coordinator list after save

### 4. `delete_coordinator(request, coordinator_id)`
- Delete coordinator with confirmation
- Shows details before deletion
- Redirects back to coordinator list after delete

## New Forms

**File**: `core/forms.py`

### CoordinatorForm
- Fields: event, name, register_number, year, event_type
- Bootstrap styling
- Validation for required fields

### Updated EventForm
- Added `duration` field (text input)
- Added `venue` field (text input)
- Helpful placeholders for both fields

## URL Routes

**File**: `core/urls.py`
```
/manage-coordinators/                          → manage all coordinators
/manage-coordinators/<event_id>/               → manage coordinators for event
/add-coordinator/                              → add new coordinator
/add-coordinator/<event_id>/                   → add coordinator to specific event
/edit-coordinator/<coordinator_id>/            → edit coordinator
/delete-coordinator/<coordinator_id>/          → delete coordinator
```

## New Templates

### 1. `manage_coordinators.html`
- List all coordinators in cards
- Shows: name, register number, year, event type, event name
- Edit/Delete buttons for each coordinator
- Add Coordinator button
- Filter by event (if event_id provided)
- Admin-only access

### 2. `coordinator_form.html`
- Form for adding/editing coordinators
- Fields: event, name, register_number, year, event_type
- Professional styling with Stranger Things theme
- Cancel button
- Error display

### 3. `confirm_delete_coordinator.html`
- Confirmation before deleting
- Shows coordinator details
- Warning message
- Delete/Cancel buttons
- Shake animation on load

## Updated Templates

### `about.html`
- Now displays coordinators from database
- Dynamic list based on event.coordinators relationship
- Shows duration and venue from event model
- Edit/Delete icons (for admins only)
- Link to manage coordinators page (for admins)
- Groups by event type (Technical/Non-Technical)

### `admin_dashboard.html`
- Added "Manage Coordinators" action card
- Links to `/manage-coordinators/` page
- Shows status of coordinator management

## Admin Interface

**File**: `core/admin.py`

### CoordinatorAdmin
- List display: name, event, register_number, year, event_type, created_at
- Filters: event_type, year, event, created_at
- Search: name, register_number, event__name
- Read-only: created_at
- Fieldsets: Coordinator Info, Event, Meta

### Updated EventAdmin
- Added duration and venue to fieldsets
- New "Event Details" fieldset
- Search now includes venue

## Access Control
- All coordinator views require superuser login
- Non-superusers redirected to home page
- About page shows edit/delete buttons only to superusers
- Admin dashboard only accessible to superusers

## Features

### Dynamic Display
- About page automatically displays all coordinators from database
- No hardcoded data - all from database
- Updates in real-time when coordinators are added/edited/deleted

### Event Duration & Venue
- Every event can have a duration (e.g., "7 hours", "2 hours")
- Every event can have a venue (e.g., "Lab 1", "Room 201")
- Displayed on about page and home page

### Coordinator Details
- Full name required
- Register number for student identification
- Year level selection (1st-4th year)
- Event type (Technical/Non-Technical)
- Linked to specific event

### Admin Controls
- Easy add/edit/delete from admin dashboard or admin panel
- Batch management possible via admin panel
- View all coordinators in one place
- Filter by event or event type

## Usage

### Adding Coordinators
1. Go to Admin Dashboard
2. Click "Manage Coordinators"
3. Click "Add Coordinator"
4. Fill in the form
5. Click "Add Coordinator"

### Editing Coordinators
1. Go to Manage Coordinators page
2. Click Edit button on coordinator card
3. Update information
4. Click "Update Coordinator"

### Deleting Coordinators
1. Go to Manage Coordinators page
2. Click Delete button on coordinator card
3. Confirm deletion on the confirmation page
4. Coordinator is deleted

### Managing by Event
1. Go to Manage Coordinators page
2. Manage Coordinators link from About page event cards
3. Shows only coordinators for that event
4. Add/Edit/Delete options available

## Database Migration

**Migration**: `0004_event_duration_event_venue_coordinator.py`
- Adds `duration` field to Event
- Adds `venue` field to Event
- Creates Coordinator model with all fields
- Sets up ForeignKey relationship to Event

## Future Enhancements

Possible additions:
- Contact information for coordinators
- Coordinator photo upload
- Coordinator bio/experience
- Bulk import/export coordinators
- Email notifications for coordinators
- Coordinator roles/responsibilities
- Event sign-up sheet for coordinators
