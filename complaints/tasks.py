from django.utils import timezone
from .models import Complaint
from .services import notify_tenant

def auto_escalate_overdue():
    qs = Complaint.objects.filter(status__in=['ACK','INP'], due_at__lt=timezone.now())
    for c in qs:
        c.status = 'ESC'
        c.escalated_at = timezone.now()
        c.save(update_fields=['status','escalated_at'])
        notify_tenant(c, 'email/complaint_update.txt', 'Your complaint has been escalated')