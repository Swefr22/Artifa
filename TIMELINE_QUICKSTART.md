# ARTIFA FEST Timeline Management - Quick Start Guide

## What's New?

The timeline management system is a complete solution for managing festival schedules with an intuitive admin interface. Admins can now easily add, edit, view, and delete timeline items without touching code.

## Quick Navigation

### For Festival Organizers

1. **Access Admin Panel**
   - Login with admin credentials
   - Go to Admin Dashboard (`/admin-dashboard/`)

2. **Manage Timeline**
   - Click "Manage Timeline" action card
   - View all festival schedule items organized by date

3. **Add New Timeline Item**
   - Click "Add Timeline Item" button
   - Fill in: Title, Description, Date, Start Time, End Time
   - Optionally: Link to event, Mark as break
   - Click "Add Timeline Item"

4. **Edit Existing Item**
   - Click edit icon on any timeline item
   - Modify any field
   - Click "Save Changes"

5. **Delete Timeline Item**
   - Click delete icon on any timeline item
   - Review details on confirmation page
   - Click "Yes, Delete Permanently"

## Timeline Item Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Title | Text | Yes | Name of the timeline event (e.g., "Inaugural Ceremony") |
| Description | Text | No | Detailed information about the item |
| Date | Date | Yes | When the item occurs |
| Start Time | Time | Yes | When it begins (HH:MM format) |
| End Time | Time | Yes | When it ends (HH:MM format) |
| Order | Number | No | Display priority (higher = earlier) |
| Event | Dropdown | No | Link to competition if applicable |
| Is Break | Checkbox | No | Check if this is a break, lunch, or non-event time |

## Sample Timeline for February 7, 2026

```
09:00 - 10:00   Inaugural Ceremony
10:00 - 10:30   Event Registrations & Brief
10:30 - 12:30   Technical Events Round 1
12:30 - 13:30   [BREAK] Lunch Break
13:30 - 15:30   Non-Technical Events
15:30 - 17:00   Team Challenges & D&D
17:00 - 17:30   [BREAK] Evening Break & Snacks
17:30 - 19:00   Finals & Results Announcement
19:00 - 20:00   Awards & Prize Distribution
20:00 - 22:00   Closing Ceremony & Dinner
```

## URL Reference

| Action | URL | Method |
|--------|-----|--------|
| View Timeline | `/manage-schedule/` | GET |
| Add Item | `/add-schedule/` | GET/POST |
| Edit Item | `/edit-schedule/<id>/` | GET/POST |
| Delete Item | `/delete-schedule/<id>/` | GET/POST |

## Permissions

- **Required Role**: Superuser/Admin
- **Access**: Admin Dashboard only
- **Public Access**: No (timeline shown on public pages in future versions)

## Tips & Best Practices

1. **Set Correct Times**: Ensure start_time is before end_time
2. **Use Order Field**: Set order for multiple items at same time
3. **Mark Breaks**: Use checkbox to visually distinguish break times
4. **Link Events**: Associate timeline items with competitions for better tracking
5. **Clear Descriptions**: Help participants understand each timeline segment

## Troubleshooting

**Q: Can't see timeline management button?**
- A: Ensure you're logged in as superuser

**Q: Times showing incorrectly?**
- A: Check system timezone settings in Django admin

**Q: Want to backup schedule data?**
- A: Use Django's dumpdata command:
  ```bash
  python manage.py dumpdata core.Schedule > schedule_backup.json
  ```

## Data Management

### Load Default Schedule
```bash
python manage.py load_schedule
```

### Backup Current Schedule
```bash
python manage.py dumpdata core.Schedule > backup.json
```

### Restore from Backup
```bash
python manage.py loaddata backup.json
```

## Integration Points

- Timeline items can be linked to Events/Competitions
- Break times are visually distinguished in timeline view
- Schedule items are ordered by date and time
- Admin dashboard provides quick access to timeline management

## Support

For issues or feature requests:
- Check TIMELINE_MANAGEMENT_DOCS.md for technical details
- Review Django logs for error messages
- Contact development team for custom modifications
