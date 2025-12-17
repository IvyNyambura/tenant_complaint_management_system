from django.utils import timezone

ESCALATION_RULES = {
    'LOW': 72,   # hours
    'MED': 48,
    'HIGH': 24,
}

def set_due_date(complaint):
    """Set the due date based on complaint priority."""
    hours = ESCALATION_RULES.get(complaint.priority, 48)
    complaint.due_at = timezone.now() + timezone.timedelta(hours=hours)
    complaint.save(update_fields=['due_at'])

def assign_to_manager(complaint, manager):
    """Assign a complaint to a manager and set status to acknowledged."""
    complaint.assigned_to = manager
    complaint.status = 'ACK'  # Use the correct status code from STATUS_CHOICES
    complaint.acknowledged_at = timezone.now()  # Set acknowledged timestamp
    complaint.save()

def update_status(complaint, status):
    """Update the complaint status and set resolved timestamp if resolved."""
    complaint.status = status
    if status == 'RES':
        complaint.resolved_at = timezone.now()
    complaint.save()