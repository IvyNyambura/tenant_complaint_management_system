CATEGORY_CHOICES = [
    ('MAINT', 'Maintenance'),
    ('BILL', 'Billing'),
    ('SEC', 'Security'),
    ('SERV', 'General Services'),
]

PRIORITY_CHOICES = [
    ('LOW', 'Low'),
    ('MED', 'Medium'),
    ('HIGH', 'High'),
]

STATUS_CHOICES = [
    ('NEW', 'New'),
    ('ACK', 'Acknowledged'),
    ('INP', 'In Progress'),
    ('RES', 'Resolved'),
    ('ESC', 'Escalated'),
    ('CLO', 'Closed'),
]