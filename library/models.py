from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model

class Admin(models.Model):
    """Admin users with static credentials"""
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # Hashed password
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'library_admin'

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """Hash and set password"""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Check if password is correct"""
        return check_password(raw_password, self.password)

    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = timezone.now()
        self.save()


class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'library_author'
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=200, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'library_book'
        ordering = ['title']

    def __str__(self):
        return self.title

    def is_available(self):
        return self.available_copies > 0

    def get_status_for_student(self, student):
        if not student:
            return None
        
        active_request = IssueRequest.objects.filter(
            book=self,
            student=student,
            status__in=['requested', 'issued']
        ).first()
        
        if active_request:
            if active_request.status == 'requested':
                return 'issue requested'
            elif active_request.status == 'issued':
                return 'issued'
        
        return 'request issue' if self.is_available() else 'not available'


class Student(models.Model):
    """Student users with dynamic accounts"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    student_id = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # Hashed password
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True)
    enrollment_year = models.IntegerField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'library_student'
        ordering = ['student_id']

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, raw_password):
        """Hash and set password"""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Check if password is correct"""
        return check_password(raw_password, self.password)

    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = timezone.now()
        self.save()

   
    @property
    def total_fines(self):
        if hasattr(self, 'fines'):
            return self.fines.filter(is_paid=False).aggregate(
                total=models.Sum('amount')
            )['total'] or Decimal('0.00')
        return Decimal('0.00')

    @property
    def active_issues_count(self):
        return self.issuerequest_set.filter(status='issued').count()


class IssueRequest(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('rejected', 'Rejected'),
        ('overdue', 'Overdue'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=timezone.now)
    issue_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    expected_return_date = models.DateField(null=True, blank=True)
    actual_return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'library_issuerequest'
        ordering = ['-request_date']

    def __str__(self):
        return f"{self.book.title} - {self.student.student_id}"

    @property
    def days_remaining(self):
        if self.status != 'issued' or not self.expected_return_date:
            return None
        today = timezone.now().date()
        delta = (self.expected_return_date - today).days
        return delta

    @property
    def is_overdue(self):
        if self.status != 'issued' or not self.expected_return_date:
            return False
        return timezone.now().date() > self.expected_return_date

    def calculate_overdue_fine(self):
        """Calculate fine for overdue book (5 tk per day)"""
        if self.status not in ['issued', 'overdue'] or not self.expected_return_date:
            return 0
        
        today = timezone.now().date()
        if today > self.expected_return_date:
            days_overdue = (today - self.expected_return_date).days
            return days_overdue * 5  # 5 tk per day
        return 0
    
    def update_overdue_status(self):
        """Update status to overdue if book is past due date"""
        if self.status == 'issued' and self.is_overdue:
            self.status = 'overdue'
            self.save()
    
    def save(self, *args, **kwargs):
        if self.status == 'issued' and not self.expected_return_date:
            self.issue_date = timezone.now().date()
            self.expected_return_date = self.issue_date + timedelta(days=14)
        
        # Auto-update to overdue if past due date
        if self.status == 'issued' and self.is_overdue:
            self.status = 'overdue'
        
        super().save(*args, **kwargs)
        
        # Auto-generate fine if overdue
        if self.status == 'overdue':
            self.auto_generate_fine()
    
    def auto_generate_fine(self):
        """Automatically generate fine for overdue books"""
        from django.conf import settings
        from decimal import Decimal
        import uuid
        
        if self.status != 'overdue' or not self.expected_return_date:
            return
        
        today = timezone.now().date()
        if today > self.expected_return_date:
            days_overdue = (today - self.expected_return_date).days
            fine_amount = Decimal(days_overdue) * Decimal('5')  # 5 tk per day
            
            # Generate unique invoice number
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            invoice_number = f"INV-AUTO-{self.id}-{timestamp}"
            
            # Create or update fine
            fine, created = Fine.objects.get_or_create(
                issue_request=self,
                defaults={
                    'student': self.student,
                    'amount': fine_amount,
                    'days_overdue': days_overdue,
                    'description': f'Overdue fine for {days_overdue} days',
                    'invoice_number': invoice_number,
                }
            )
            
            # Update fine if it already exists and days have increased
            if not created and fine.days_overdue < days_overdue:
                fine.amount = fine_amount
                fine.days_overdue = days_overdue
                fine.description = f'Overdue fine for {days_overdue} days'
                fine.save()


class Fine(models.Model):
    PAYMENT_METHODS = [
        ('bkash', 'bKash'),
        ('cash', 'Cash'),
        ('card', 'Card'),
    ]
    
    # Change from OneToOneField to ForeignKey to allow multiple fines per issue
    issue_request = models.ForeignKey(IssueRequest, on_delete=models.CASCADE, null=True, blank=True, related_name='fines')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fines')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    days_overdue = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, blank=True)
    bkash_payment_id = models.CharField(max_length=100, blank=True)
    bkash_trx_id = models.CharField(max_length=100, blank=True)
    invoice_number = models.CharField(max_length=100, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'library_fine'
        ordering = ['-created_at']

    def __str__(self):
        return f"Fine: {self.student.student_id} - ৳{self.amount}"

    def mark_as_paid(self, payment_method='cash', payment_id=None, trx_id=None):
        self.is_paid = True
        self.payment_date = timezone.now()
        self.payment_method = payment_method
        if payment_id:
            self.bkash_payment_id = payment_id
        if trx_id:
            self.bkash_trx_id = trx_id
        self.save()


class Notification(models.Model):
    """System notifications for users"""
    NOTIFICATION_TYPES = [
        ('fine', 'Fine'),
        ('issue', 'Book Issue'),
        ('return', 'Book Return'),
        ('general', 'General'),
    ]
    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='general')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'library_notification'

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()