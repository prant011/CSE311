from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum
from django.db import models
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Admin, Student, Book, Author, IssueRequest, Fine
from django.views.decorators.http import require_GET, require_http_methods

# ============= AUTHENTICATION VIEWS =============

def login_choice(request):
    """Landing page to choose login type"""
    return render(request, 'library/login_choice.html')


def admin_login(request):
    """Admin login - checks library_admin table"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Validate input
        if not username or not password:
            messages.error(request, 'Please enter both username and password!')
            return render(request, 'library/admin_login.html')
        
        try:
            # Check in Admin table
            admin = Admin.objects.get(username=username)
            
            # Check if account is active
            if not admin.is_active:
                messages.error(request, 'Your admin account is inactive. Please contact the system administrator.')
                return render(request, 'library/admin_login.html')
            
            # Check if password is set
            if not admin.password:
                messages.error(request, 'Password not set. Please contact the system administrator.')
                return render(request, 'library/admin_login.html')
            
            # Verify password
            if admin.check_password(password):
                # Clear any student session if exists
                if 'is_student' in request.session:
                    del request.session['is_student']
                    del request.session['student_id']
                    del request.session['student_username']
                
                # Set admin session
                request.session['admin_id'] = admin.id
                request.session['admin_username'] = admin.username
                request.session['is_admin'] = True
                request.session['user_type'] = 'admin'
                
                # Update last login
                admin.update_last_login()
                
                messages.success(request, f'Welcome Admin, {admin.full_name}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid password! Please try again.')
                
        except Admin.DoesNotExist:
            messages.error(request, 'Invalid username or admin account not found!')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    return render(request, 'library/admin_login.html')


def student_login(request):
    """Student login - checks library_student table"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Validate input
        if not username or not password:
            messages.error(request, 'Please enter both username and password!')
            return render(request, 'library/student_login.html')
        
        try:
            # Check in Student table - check both is_active and status
            student = Student.objects.get(username=username)
            
            # Check if account is active
            if not student.is_active:
                messages.error(request, 'Your account is inactive. Please contact the administrator.')
                return render(request, 'library/student_login.html')
            
            # Check if account is suspended
            if student.status == 'suspended':
                messages.error(request, 'Your account has been suspended. Please contact the administrator.')
                return render(request, 'library/student_login.html')
            
            # Check if password is set
            if not student.password:
                messages.error(request, 'Password not set. Please use forgot password to reset.')
                return render(request, 'library/student_login.html')
            
            # Verify password
            if student.check_password(password):
                # Clear any admin session if exists
                if 'is_admin' in request.session:
                    del request.session['is_admin']
                    del request.session['admin_id']
                    del request.session['admin_username']
                
                # Set student session
                request.session['student_id'] = student.id
                request.session['student_username'] = student.username
                request.session['is_student'] = True
                request.session['user_type'] = 'student'
                
                # Update last login
                student.update_last_login()
                
                messages.success(request, f'Welcome, {student.full_name}!')
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid password! Please try again.')
                
        except Student.DoesNotExist:
            messages.error(request, 'Invalid username or account not found!')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    return render(request, 'library/student_login.html')


def student_signup(request):
    """Student registration - creates new entry in library_student table"""
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender', '')
        department = request.POST.get('department')
        gender = request.POST.get('gender')
        
        # Validation
        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('student_signup')
        
        # Check if username exists
        if Student.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('student_signup')
        
        # Check if student ID exists
        if Student.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID already exists!')
            return redirect('student_signup')
        
        # Check if email exists
        if Student.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('student_signup')
        
        try:
            # Create student account with temporary password (will be hashed immediately)
            from django.contrib.auth.hashers import make_password
            
            student = Student.objects.create(
                username=username,
                student_id=student_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone if phone else '',
                department=department if department else '',
                gender=gender if gender else '',
                status='active',
                is_active=True,
                password=make_password(password)  # Hash password during creation
            )
            
            # Handle profile image upload
            if 'profile_image' in request.FILES:
                student.profile_image = request.FILES['profile_image']
            
            # Password is already set, just save to ensure everything is committed
            student.save()
            
            messages.success(request, f'Account created successfully! Welcome {student.full_name}. Please login.')
            return redirect('student_login')
            
        except Exception as e:
            import traceback
            error_msg = str(e)
            messages.error(request, f'Error creating account: {error_msg}')
            print(f"Student signup error: {error_msg}")
            print(traceback.format_exc())
            # Return the form with error instead of redirecting
            return render(request, 'library/student_signup.html', {
                'username': username,
                'student_id': student_id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'department': department,
            })
    
    return render(request, 'library/student_signup.html')


def validate_student_id(request):
    """AJAX validation for student ID"""
    student_id = request.GET.get('student_id', '')
    
    if student_id:
        exists = Student.objects.filter(student_id=student_id).exists()
        return JsonResponse({'exists': exists})
    
    return JsonResponse({'exists': False})


def validate_username(request):
    """AJAX validation for username"""
    username = request.GET.get('username', '')
    
    if username:
        exists = Student.objects.filter(username=username).exists()
        return JsonResponse({'exists': exists})
    
    return JsonResponse({'exists': False})


def forgot_password(request):
    """Forgot password - verifies username and old password, then resets"""
    if request.method == 'POST':
        username = request.POST.get('username')
        student_id = request.POST.get('student_id')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match!')
            return redirect('forgot_password')
        
        try:
            # Find student by username AND student_id
            student = Student.objects.get(
                username=username,
                student_id=student_id,
                is_active=True
            )
            
            # Verify old password
            if student.check_password(old_password):
                # Set new password
                student.set_password(new_password)
                student.save()
                
                messages.success(request, 'Password reset successfully! Please login with your new password.')
                return redirect('student_login')
            else:
                messages.error(request, 'Old password is incorrect!')
                
        except Student.DoesNotExist:
            messages.error(request, 'Invalid username or student ID!')
    
    return render(request, 'library/forgot_password.html')


def logout_view(request):
    """Logout for both admin and student"""
    user_type = request.session.get('user_type')
    
    # Clear all session data
    request.session.flush()
    
    messages.success(request, 'Logged out successfully!')
    
    if user_type == 'admin':
        return redirect('admin_login')
    else:
        return redirect('student_login')


# ============= HELPER DECORATORS =============

from functools import wraps

def admin_required(view_func):
    """Decorator to check if user is admin"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_admin'):
            messages.error(request, 'Please login to access this page.')
            return redirect('admin_login')
        # Also check if admin_id exists in session
        if not request.session.get('admin_id'):
            messages.error(request, 'Session expired. Please login again.')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def student_required(view_func):
    """Decorator to check if user is student"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_student'):
            messages.error(request, 'Please login to access this page.')
            return redirect('student_login')
        # Also check if student_id exists in session
        if not request.session.get('student_id'):
            messages.error(request, 'Session expired. Please login again.')
            return redirect('student_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def get_current_student(request):
    """Get current logged in student"""
    student_id = request.session.get('student_id')
    if student_id:
        try:
            return Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return None
    return None


def get_current_admin(request):
    """Get current logged in admin"""
    admin_id = request.session.get('admin_id')
    if admin_id:
        try:
            return Admin.objects.get(id=admin_id)
        except Admin.DoesNotExist:
            return None
    return None


# ============= PUBLIC VIEWS =============

def home(request):
    """Homepage - accessible to everyone"""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'title')
    
    books = Book.objects.select_related('author').all()
    
    # Search
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__name__icontains=query) |
            Q(category__icontains=query) |
            Q(isbn__icontains=query)
        )
    
    # Filter by category
    if category:
        books = books.filter(category__icontains=category)
    
    # Sort
    sort_options = {
        'title': 'title',
        'author': 'author__name',
        '-title': '-title',
        '-author': '-author__name',
    }
    books = books.order_by(sort_options.get(sort_by, 'title'))
    
    # Convert to list for template rendering
    books_list = list(books)
    
    # Limit to first 12 books for homepage only if no search/filter
    if not query and not category:
        books_list = books_list[:12]
    
    categories = Book.objects.values_list('category', flat=True).distinct()
    
    # Get current student if logged in
    student = get_current_student(request)
    
    # Statistics for homepage
    total_books = Book.objects.count()
    total_members = Student.objects.filter(status='active').count()
    active_borrows = IssueRequest.objects.filter(status='issued').count()
    authors_count = Author.objects.count()
    
    context = {
        'books': books_list,
        'query': query,
        'categories': categories,
        'selected_category': category,
        'sort_by': sort_by,
        'student': student,
        'is_admin': request.session.get('is_admin', False),
        'is_student': request.session.get('is_student', False),
        'total_books': total_books,
        'total_members': total_members,
        'active_borrows': active_borrows,
        'authors_count': authors_count,
    }
    return render(request, 'library/public_home.html', context)


def book_detail(request, pk):
    """Book detail page"""
    book = get_object_or_404(Book, pk=pk)
    student = get_current_student(request)
    book_status = None
    
    if student:
        book_status = book.get_status_for_student(student)
    
    context = {
        'book': book,
        'student': student,
        'book_status': book_status,
        'is_admin': request.session.get('is_admin', False),
        'is_student': request.session.get('is_student', False),
    }
    return render(request, 'library/book_detail.html', context)


# ============= STUDENT VIEWS (With decorator) =============

@student_required
def student_dashboard(request):
    """Student dashboard"""
    student = get_current_student(request)
    
    if not student:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('student_login')
    
    # Get statistics
    active_issues = IssueRequest.objects.filter(student=student, status='issued')
    pending_requests = IssueRequest.objects.filter(student=student, status='requested')
    unpaid_fines = Fine.objects.filter(student=student, is_paid=False)
    
    context = {
        'student': student,
        'active_issues': active_issues,
        'pending_requests': pending_requests,
        'unpaid_fines': unpaid_fines,
        'total_fine': student.total_fines,
    }
    return render(request, 'library/student_dashboard.html', context)


@student_required
def student_change_profile_picture(request):
    """Change student profile picture"""
    student = get_current_student(request)
    
    if not student:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('student_login')
    
    if request.method == 'POST':
        if 'profile_image' in request.FILES:
            student.profile_image = request.FILES['profile_image']
            student.save()
            messages.success(request, 'Profile picture updated successfully!')
        else:
            messages.error(request, 'Please select an image file.')
    
    return redirect('student_dashboard')


@student_required
def student_fines(request):
    """Student fines page"""
    student = get_current_student(request)
    
    if not student:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('student_login')
    
    # Get all fines for the student
    fines = Fine.objects.filter(student=student).order_by('-created_at')
    
    # Calculate totals
    total_pending = fines.filter(is_paid=False).aggregate(models.Sum('amount'))['amount__sum'] or 0
    total_paid = fines.filter(is_paid=True).aggregate(models.Sum('amount'))['amount__sum'] or 0
    
    context = {
        'student': student,
        'fines': fines,
        'total_pending': total_pending,
        'total_paid': total_paid,
        'total_fines': total_pending + total_paid,
    }
    return render(request, 'library/student_fines.html', context)


@student_required
def student_issues(request):
    """
    List issues for a student. Instead of assigning to the read-only
    @property 'days_remaining' on IssueRequest, compute a separate
    attribute 'days_remaining_calc' for use in the template.
    """
    # Resolve student: prefer logged-in user's student record, fallback to query/session id
    student = None
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            student_id = request.GET.get('student_id') or request.session.get('student_id')
            if student_id:
                student = get_object_or_404(Student, pk=student_id)
    else:
        student_id = request.GET.get('student_id') or request.session.get('student_id')
        if student_id:
            student = get_object_or_404(Student, pk=student_id)

    if not student:
        # No student found — render page with empty list (adjust behavior if you prefer redirect/error)
        return render(request, 'library/student_issues.html', {'issues': [], 'student': None})

    # Fetch issues and compute a non-persistent days_remaining_calc attribute
    issues = IssueRequest.objects.filter(student=student).select_related('book')
    today = timezone.now().date()
    for issue in issues:
        due = getattr(issue, 'due_date', None)
        issue.days_remaining_calc = (due - today).days if due else None

    context = {
        'issues': issues,
        'student': student,
    }
    return render(request, 'library/student_issues.html', context)


@student_required
def request_book(request, book_id):
    """Request a book"""
    student = get_current_student(request)
    
    if not student:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('student_login')
    
    book = get_object_or_404(Book, pk=book_id)
    
    # Check if book is available
    if not book.is_available():
        messages.error(request, 'Book is not available!')
        return redirect('book_detail', pk=book_id)
    
    # Check if student already has an active request/issue for this book
    existing = IssueRequest.objects.filter(
        book=book,
        student=student,
        status__in=['requested', 'issued']
    ).first()
    
    if existing:
        messages.warning(request, 'You already have an active request/issue for this book!')
        return redirect('book_detail', pk=book_id)
    
    # Check if student has unpaid fines
    if student.total_fines > 0:
        messages.error(request, 'Please clear your fines before requesting new books!')
        return redirect('student_fines')
    
    # Create issue request
    IssueRequest.objects.create(
        book=book,
        student=student,
        status='requested'
    )
    
    messages.success(request, f'Request sent for "{book.title}". Waiting for approval.')
    return redirect('student_issues')


# ============= PAYMENT VIEWS =============

@student_required
def pay_fine(request, fine_id):
    """Initiate fine payment"""
    student = get_current_student(request)
    fine = get_object_or_404(Fine, id=fine_id, student=student)
    
    if fine.is_paid:
        messages.info(request, 'This fine has already been paid!')
        return redirect('student_fines')
    
    # For now, redirect to bKash payment
    # In production, implement actual bKash integration
    messages.info(request, 'bKash payment integration coming soon. Please pay at the library.')
    return redirect('student_fines')


@student_required
def bkash_callback(request):
    """bKash payment callback"""
    # Implement bKash callback logic here
    return JsonResponse({'status': 'success'})


@student_required
def payment_success_page(request, fine_id):
    """Payment success page"""
    student = get_current_student(request)
    fine = get_object_or_404(Fine, id=fine_id, student=student)
    
    context = {
        'fine': fine,
        'student': student,
    }

    return render(request, 'library/payment_success.html', context)


# ============= ADMIN VIEWS (With decorator) =============

@admin_required
def admin_dashboard(request):
    """Admin dashboard"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    # Statistics
    total_books = Book.objects.count()
    total_students = Student.objects.filter(status='active').count()
    active_issues = IssueRequest.objects.filter(status='issued').count()
    pending_requests = IssueRequest.objects.filter(status='requested').count()
    overdue_issues = IssueRequest.objects.filter(status='overdue').count()
    unpaid_fines = Fine.objects.filter(is_paid=False).aggregate(
        total=models.Sum('amount')
    )['total'] or 0
    
    recent_requests = IssueRequest.objects.filter(status='requested').order_by('-request_date')[:5]
    recent_issues = IssueRequest.objects.filter(status='issued').order_by('-issue_date')[:5]
    
    context = {
        'admin': admin,
        'total_books': total_books,
        'total_students': total_students,
        'active_issues': active_issues,
        'pending_requests': pending_requests,
        'overdue_issues': overdue_issues,
        'unpaid_fines': unpaid_fines,
        'recent_requests': recent_requests,
        'recent_issues': recent_issues,
    }
    return render(request, 'library/admin_dashboard.html', context)


@admin_required
def admin_issues(request):
    """Admin issues management"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    # Get filter from GET request
    filter_by = request.GET.get("filter", "all")
    
    issues = IssueRequest.objects.select_related('student', 'book').all()
    
    # Update overdue status for all issued books (real-time)
    from datetime import date
    today = date.today()
    for issue in issues.filter(status='issued'):
        if issue.expected_return_date and today > issue.expected_return_date:
            issue.update_overdue_status()
    
    # Apply filter
    if filter_by == "pending":
        issues = issues.filter(status="requested")
    elif filter_by == "active":
        issues = issues.filter(status="issued")
    elif filter_by == "overdue":
        issues = issues.filter(status="overdue")
    elif filter_by == "returned":
        issues = issues.filter(status="returned")
    
    # Calculate real-time fines for each issue
    issues_list = list(issues)
    for issue in issues_list:
        issue.real_time_fine = issue.calculate_overdue_fine()
        if issue.status in ['issued', 'overdue']:
            # Do not assign to the read-only property `days_remaining`.
            # Read the property and store the value on a different attribute for templates.
            try:
                dr = issue.days_remaining
            except Exception:
                dr = None
            issue.days_remaining_calc = dr
            if dr is not None and dr < 0:
                issue.days_overdue = abs(dr)
            else:
                issue.days_overdue = 0
    
    context = {
        "issues": issues_list,
        "filter_by": filter_by,
        "admin": admin,
    }
    
    return render(request, "library/admin_issues.html", context)


@admin_required
def accept_issue_request(request, request_id):
    """Accept an issue request"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    issue_request = get_object_or_404(IssueRequest, id=request_id, status='requested')
    book = issue_request.book
    
    # Check if book is available
    if book.available_copies <= 0:
        messages.error(request, 'Book is not available!')
        return redirect('admin_issues')
    
    # Update issue request
    from datetime import date
    issue_request.status = 'issued'
    issue_request.issue_date = date.today()
    issue_request.expected_return_date = date.today() + timedelta(days=14)
    issue_request.save()
    
    # Decrease available copies
    book.available_copies -= 1
    book.save()
    
    messages.success(request, f'Book "{book.title}" issued to {issue_request.student.full_name}')
    return redirect('admin_issues')


@admin_required
def reject_issue_request(request, request_id):
    """Reject an issue request"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    issue_request = get_object_or_404(IssueRequest, id=request_id, status='requested')
    book_title = issue_request.book.title
    
    issue_request.status = 'rejected'
    issue_request.save()
    
    messages.success(request, f'Request for "{book_title}" has been rejected.')
    return redirect('admin_issues')


@admin_required
def return_book_admin(request, request_id):
    """Admin return book - marks book as returned to library"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    issue_request = get_object_or_404(IssueRequest, id=request_id, status__in=['issued', 'overdue'])
    book = issue_request.book
    
    # Update overdue status and generate fine if needed
    issue_request.update_overdue_status()
    
    # Calculate fine if overdue (5 tk per day)
    from datetime import date
    from decimal import Decimal
    
    fine_message = ""
    if issue_request.expected_return_date and date.today() > issue_request.expected_return_date:
        days_overdue = (date.today() - issue_request.expected_return_date).days
        fine_amount = Decimal(days_overdue) * Decimal('5')  # 5 tk per day
        
        # Create or update fine
        fine, created = Fine.objects.get_or_create(
            issue_request=issue_request,
            defaults={
                'student': issue_request.student,
                'amount': fine_amount,
                'days_overdue': days_overdue,
                'description': f'Overdue fine: {days_overdue} days × 5 tk = {fine_amount} tk',
            }
        )
        
        if not created:
            # Update existing fine
            fine.amount = fine_amount
            fine.days_overdue = days_overdue
            fine.description = f'Overdue fine: {days_overdue} days × 5 tk = {fine_amount} tk'
            fine.save()
        
        fine_message = f" Fine of {fine_amount} tk generated for {days_overdue} overdue day(s)."
    
    # Update issue request
    issue_request.status = 'returned'
    issue_request.actual_return_date = date.today()
    issue_request.save()
    
    # Increase available copies
    book.available_copies += 1
    book.save()
    
    messages.success(request, f'Book "{book.title}" returned successfully!{fine_message}')
    return redirect('admin_issues')


@admin_required
def admin_books(request):
    """Admin books management"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    query = request.GET.get('q', '')
    books = Book.objects.select_related('author').all()
    
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__name__icontains=query) |
            Q(isbn__icontains=query)
        )
    
    context = {
        'books': books,
        'query': query,
        'admin': admin,
    }
    return render(request, 'library/admin_books.html', context)


@admin_required
def admin_book_add(request):
    """Add new book"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        isbn = request.POST.get('isbn')
        publisher = request.POST.get('publisher')
        publication_year = request.POST.get('publication_year')
        category = request.POST.get('category')
        description = request.POST.get('description')
        total_copies = int(request.POST.get('total_copies', 1))
        available_copies = int(request.POST.get('available_copies', total_copies))
        
        try:
            author = Author.objects.get(id=author_id)
            book = Book.objects.create(
                title=title,
                author=author,
                isbn=isbn,
                publisher=publisher,
                publication_year=publication_year if publication_year else None,
                category=category,
                description=description,
                total_copies=total_copies,
                available_copies=available_copies,
            )
            
            if 'cover_image' in request.FILES:
                book.cover_image = request.FILES['cover_image']
                book.save()
            
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('admin_books')
        except Exception as e:
            messages.error(request, f'Error adding book: {str(e)}')
    
    authors = Author.objects.all().order_by('name')
    context = {
        'admin': admin,
        'authors': authors,
    }
    return render(request, 'library/admin_book_form.html', context)


@admin_required
def admin_book_edit(request, pk):
    """Edit book"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = Author.objects.get(id=request.POST.get('author'))
        book.isbn = request.POST.get('isbn')
        book.publisher = request.POST.get('publisher')
        book.publication_year = request.POST.get('publication_year') if request.POST.get('publication_year') else None
        book.category = request.POST.get('category')
        book.description = request.POST.get('description')
        book.total_copies = int(request.POST.get('total_copies', 1))
        book.available_copies = int(request.POST.get('available_copies', book.total_copies))
        
        if 'cover_image' in request.FILES:
            book.cover_image = request.FILES['cover_image']
        
        book.save()
        
        messages.success(request, f'Book "{book.title}" updated successfully!')
        return redirect('admin_books')
    
    authors = Author.objects.all().order_by('name')
    context = {
        'admin': admin,
        'book': book,
        'authors': authors,
    }
    return render(request, 'library/admin_book_form.html', context)


@admin_required
def admin_book_delete(request, pk):
    """Delete book"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('admin_books')
    
    context = {
        'admin': admin,
        'book': book,
    }
    return render(request, 'library/admin_book_confirm_delete.html', context)


@admin_required
def admin_authors(request):
    """Admin authors management"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    authors = Author.objects.all().order_by('name')
    context = {
        'admin': admin,
        'authors': authors,
    }
    return render(request, 'library/admin_authors.html', context)


@admin_required
def admin_author_add(request):
    """Add new author"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        birth_date = request.POST.get('birth_date')
        
        try:
            author = Author.objects.create(
                name=name,
                bio=bio,
                birth_date=birth_date if birth_date else None,
            )
            messages.success(request, f'Author "{author.name}" added successfully!')
            return redirect('admin_authors')
        except Exception as e:
            messages.error(request, f'Error adding author: {str(e)}')
    
    context = {
        'admin': admin,
    }
    return render(request, 'library/admin_author_form.html', context)


@admin_required
def admin_author_edit(request, pk):
    """Edit author"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    author = get_object_or_404(Author, pk=pk)
    
    if request.method == 'POST':
        author.name = request.POST.get('name')
        author.bio = request.POST.get('bio')
        author.birth_date = request.POST.get('birth_date') if request.POST.get('birth_date') else None
        author.save()
        
        messages.success(request, f'Author "{author.name}" updated successfully!')
        return redirect('admin_authors')
    
    context = {
        'admin': admin,
        'author': author,
    }
    return render(request, 'library/admin_author_form.html', context)


@admin_required
def admin_author_delete(request, pk):
    """Delete author"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    author = get_object_or_404(Author, pk=pk)
    
    if request.method == 'POST':
        author_name = author.name
        author.delete()
        messages.success(request, f'Author "{author_name}" deleted successfully!')
        return redirect('admin_authors')
    
    context = {
        'admin': admin,
        'author': author,
    }
    return render(request, 'library/admin_author_confirm_delete.html', context)


@admin_required
def admin_students(request):
    """Admin students management"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    query = request.GET.get('q', '')
    students = Student.objects.all().order_by('student_id')
    
    if query:
        students = students.filter(
            Q(student_id__icontains=query) |
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
    
    context = {
        'admin': admin,
        'students': students,
        'query': query,
    }
    return render(request, 'library/admin_students.html', context)


@admin_required
def admin_student_add(request):
    """Add new student"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        enrollment_year = request.POST.get('enrollment_year')
        
        try:
            student = Student.objects.create(
                student_id=student_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                gender=request.POST.get('gender', ''),
                department=department,
                enrollment_year=int(enrollment_year) if enrollment_year else None,
                status='active',
                is_active=True,
            )
            student.set_password(password)
            
            # Handle profile image upload
            if 'profile_image' in request.FILES:
                student.profile_image = request.FILES['profile_image']
            
            student.save()
            
            messages.success(request, f'Student "{student.full_name}" added successfully!')
            return redirect('admin_students')
        except Exception as e:
            messages.error(request, f'Error adding student: {str(e)}')
    
    context = {
        'admin': admin,
    }
    return render(request, 'library/admin_student_form.html', context)


@admin_required
def admin_student_edit(request, pk):
    """Edit student"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        student.student_id = request.POST.get('student_id')
        student.username = request.POST.get('username')
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')
        student.department = request.POST.get('department')
        student.gender = request.POST.get('gender', '')
        student.enrollment_year = int(request.POST.get('enrollment_year')) if request.POST.get('enrollment_year') else None
        student.status = request.POST.get('status')
        student.is_active = request.POST.get('is_active') == 'on'
        
        if 'profile_image' in request.FILES:
            student.profile_image = request.FILES['profile_image']
        
        if request.POST.get('password'):
            student.set_password(request.POST.get('password'))
        
        student.save()
        
        messages.success(request, f'Student "{student.full_name}" updated successfully!')
        return redirect('admin_students')
    
    context = {
        'admin': admin,
        'student': student,
    }
    return render(request, 'library/admin_student_form.html', context)


@admin_required
def admin_student_delete(request, pk):
    """Delete student"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        student_name = student.full_name
        student.delete()
        messages.success(request, f'Student "{student_name}" deleted successfully!')
        return redirect('admin_students')
    
    context = {
        'admin': admin,
        'student': student,
    }
    return render(request, 'library/admin_student_confirm_delete.html', context)


@admin_required
def admin_student_details(request, pk):
    """View student details"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    student = get_object_or_404(Student, pk=pk)
    issues = IssueRequest.objects.filter(student=student).order_by('-request_date')
    fines = Fine.objects.filter(student=student).order_by('-created_at')
    
    # Calculate statistics
    total_issues = issues.count()
    active_issues = issues.filter(status='issued').count()
    total_fines_amount = fines.filter(is_paid=False).aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'admin': admin,
        'student': student,
        'issues': issues,
        'fines': fines,
        'borrowed_count': total_issues,
        'current_borrowed': active_issues,
        'total_fines': total_fines_amount,
        'recent_borrows': issues[:10],  # Last 10 issues
    }
    return render(request, 'library/admin_student_details.html', context)


@admin_required
def admin_change_password(request, pk):
    """Change student password"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('admin_change_password', pk=pk)
        
        student.set_password(new_password)
        student.save()
        
        messages.success(request, f'Password changed for {student.full_name}')
        return redirect('admin_student_details', pk=pk)
    
    context = {
        'admin': admin,
        'student': student,
    }
    return render(request, 'library/admin_change_password.html', context)


@admin_required
def admin_fines(request):
    """View all fines"""
    fines = Fine.objects.all().select_related('student', 'issue_request').order_by('-created_at')
    
    # Calculate statistics
    total_unpaid = fines.filter(is_paid=False).aggregate(models.Sum('amount'))['amount__sum'] or 0
    total_paid = fines.filter(is_paid=True).aggregate(models.Sum('amount'))['amount__sum'] or 0
    pending_count = fines.filter(is_paid=False).count()
    
    context = {
        'fines': fines,
        'total_unpaid': total_unpaid,
        'total_paid': total_paid,
        'pending_count': pending_count,
    }
    return render(request, 'library/admin_fines.html', context)


@admin_required
def admin_fine_create(request, issue_id):
    """Create fine from issue"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    issue = get_object_or_404(IssueRequest, id=issue_id)
    
    # Calculate fine
    today = timezone.now().date()
    due_date = issue.expected_return_date
    
    if due_date and today > due_date:
        days_overdue = (today - due_date).days
        fine_amount = days_overdue * 5.00
    else:
        fine_amount = 0.00
    
    if request.method == 'POST':
        try:
            fine, created = Fine.objects.get_or_create(
                issue_request=issue,
                defaults={
                    'student': issue.student,
                    'amount': fine_amount,
                    'days_overdue': int((today - due_date).days) if due_date else 0,
                    'description': f'Book overdue: {issue.book.title}',
                }
            )
            
            messages.success(request, f'Fine created: ৳{fine_amount}')
            return redirect('admin_fines')
        except Exception as e:
            messages.error(request, f'Error creating fine: {str(e)}')
    
    return render(request, 'library/admin_fine_create.html', {
        'admin': admin,
        'issue': issue,
        'fine_amount': fine_amount,
    })


@admin_required
def admin_fine_mark_paid(request, pk):
    """Mark fine as paid"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    fine = get_object_or_404(Fine, id=pk)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'cash')
        fine.mark_as_paid(payment_method=payment_method)
        messages.success(request, 'Fine marked as paid!')
        return redirect('admin_fines')
    
    context = {
        'admin': admin,
        'fine': fine,
    }
    return render(request, 'library/admin_fine_mark_paid.html', context)


@admin_required
def admin_fine_delete(request, pk):
    """Delete fine"""
    admin = get_current_admin(request)
    
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')
    
    fine = get_object_or_404(Fine, pk=pk)
    
    if request.method == 'POST':
        fine_amount = fine.amount
        fine.delete()
        messages.success(request, f'Fine of ৳{fine_amount} deleted successfully!')
        return redirect('admin_fines')
    
    context = {
        'admin': admin,
        'fine': fine,
    }
    return render(request, 'library/admin_fine_confirm_delete.html', context)


@admin_required
def admin_fine_select_issue(request):
    """Show issues so admin can pick an issue to create a fine for."""
    admin = get_current_admin(request)
    if not admin:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')

    issues = IssueRequest.objects.select_related('student', 'book').filter(
        status__in=['issued', 'overdue']
    ).order_by('-issue_date')

    context = {
        'admin': admin,
        'issues': issues,
    }
    return render(request, 'library/admin_fine_select_issue.html', context)


@require_GET
@admin_required
def admin_search_student(request):
    """API endpoint to search for students by ID or name"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return JsonResponse({'results': []})
    
    # Search by student ID or name
    students = Student.objects.filter(
        Q(student_id__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(username__icontains=query)
    ).values('id', 'student_id', 'first_name', 'last_name', 'email', 'department')
    
    # Format the results
    results = []
    for student in students:
        results.append({
            'id': student['id'],
            'student_id': student['student_id'],
            'full_name': f"{student['first_name']} {student['last_name']}",
            'email': student['email'],
            'department': student['department']
        })
    
    return JsonResponse({'results': results})

@require_http_methods(["GET", "POST"])
@admin_required
def admin_fine_create_custom(request):
    """Create custom fine for a student using modal popup"""
    admin = get_current_admin(request)
    if not admin:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Session expired. Please login again.'
            }, status=401)
        messages.error(request, 'Session expired. Please login again.')
        return redirect('admin_login')

    # Handle POST request from modal form
    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()
        amount_raw = request.POST.get('amount', '').strip()
        description = request.POST.get('description', '').strip()

        # Validation
        if not all([student_id, amount_raw, description]):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'All fields are required.'
                }, status=400)
            messages.error(request, 'All fields are required.')
            return render(request, 'library/admin_fine_create_custom.html', {'admin': admin})

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Student not found.'
                }, status=404)
            messages.error(request, 'Student not found.')
            return render(request, 'library/admin_fine_create_custom.html', {'admin': admin})

        try:
            amount = float(amount_raw)
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
        except ValueError:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Please enter a valid amount greater than 0.'
                }, status=400)
            messages.error(request, 'Invalid amount entered.')
            return render(request, 'library/admin_fine_create_custom.html', {'admin': admin})

        try:
            with transaction.atomic():
                # Create the fine
                fine = Fine.objects.create(
                    student=student,
                    amount=amount,
                    description=description,
                    is_paid=False,
                    days_overdue=0
                )
                
                # Generate invoice number
                timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
                fine.invoice_number = f"INV-{student.student_id}-{timestamp}"
                fine.save()
                
                # Create notification for the student
                Notification.objects.create(
                    user=student.user,
                    title='New Fine Issued',
                    message=f'A fine of ৳{amount:.2f} has been issued to your account. Reason: {description}',
                    notification_type='fine'
                )
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Fine created successfully!'
                    })
                
                messages.success(request, 'Fine created successfully!')
                return redirect('admin_fines')
                
        except Exception as e:
            logger.error(f"Error creating fine: {str(e)}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'An error occurred while creating the fine. Please try again.'
                }, status=500)
            messages.error(request, 'An error occurred. Please try again.')
            return render(request, 'library/admin_fine_create_custom.html', {'admin': admin})

    # GET request - show the modal page
    return render(request, 'library/admin_fine_create_custom.html', {'admin': admin})


@admin_required
@require_GET
def admin_search_student(request):
    """AJAX endpoint: search students (includes registered/active students)."""
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse({'results': []})

    # Match by ID, username, name, or email, and include only registered/active students
    matches = Student.objects.filter(
        (
            Q(student_id__icontains=q) |
            Q(username__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(email__icontains=q)
        ) &
        (Q(is_active=True) | Q(status__iexact='active'))
    ).order_by('first_name')[:50]

    results = []
    for s in matches:
        results.append({
            'id': s.id,
            'student_id': s.student_id or '',
            'full_name': getattr(s, 'full_name', f"{s.first_name} {s.last_name}".strip()),
            'email': s.email or '',
            'department': s.department or ''
        })

    return JsonResponse({'results': results})