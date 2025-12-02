from django.urls import path
from . import views
from django.views.decorators.http import require_http_methods

urlpatterns = [
    # ============= PUBLIC URLs =============
    path('', views.home, name='home'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    
    # ============= AUTHENTICATION URLs =============
    path('login/', views.login_choice, name='login_choice'),
    path('login/admin/', views.admin_login, name='admin_login'),
    path('login/student/', views.student_login, name='student_login'),
    path('signup/', views.student_signup, name='student_signup'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout_view, name='logout'),
    
    # AJAX Validation
    path('validate-student-id/', views.validate_student_id, name='validate_student_id'),
    path('validate-username/', views.validate_username, name='validate_username'),
    
    # Test template loading
    path('admin/test-template/', views.test_template_view, name='test_template'),
    
    # ============= STUDENT URLs =============
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/issues/', views.student_issues, name='student_issues'),
    path('student/fines/', views.student_fines, name='student_fines'),
    path('student/change-profile-picture/', views.student_change_profile_picture, name='student_change_profile_picture'),
    
    path('request-book/<int:book_id>/', views.request_book, name='request_book'),
    
    # bKash Payment URLs
    path('pay-fine/<int:fine_id>/', views.pay_fine, name='pay_fine'),
    path('bkash/callback/', views.bkash_callback, name='bkash_callback'),
    path('payment/success/<int:fine_id>/', views.payment_success_page, name='payment_success_page'),
    
    # ============= ADMIN URLs =============
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Admin - Issues
    path('admin/issues/', views.admin_issues, name='admin_issues'),
    path('admin/issue/accept/<int:request_id>/', views.accept_issue_request, name='accept_issue_request'),
    path('admin/issue/reject/<int:request_id>/', views.reject_issue_request, name='reject_issue_request'),
    path('admin/issue/return/<int:request_id>/', views.return_book_admin, name='return_book_admin'),
    
    # Admin - Books
    path('admin/books/', views.admin_books, name='admin_books'),
    path('admin/books/add/', views.admin_book_add, name='admin_book_add'),
    path('admin/books/edit/<int:pk>/', views.admin_book_edit, name='admin_book_edit'),
    path('admin/books/delete/<int:pk>/', views.admin_book_delete, name='admin_book_delete'),
    
    # Admin - Authors
    path('admin/authors/', views.admin_authors, name='admin_authors'),
    path('admin/authors/add/', views.admin_author_add, name='admin_author_add'),
    path('admin/authors/edit/<int:pk>/', views.admin_author_edit, name='admin_author_edit'),
    path('admin/authors/delete/<int:pk>/', views.admin_author_delete, name='admin_author_delete'),
    
    # Admin - Students
    path('admin/students/', views.admin_students, name='admin_students'),
    path('admin/students/add/', views.admin_student_add, name='admin_student_add'),
    path('admin/students/edit/<int:pk>/', views.admin_student_edit, name='admin_student_edit'),
    path('admin/students/delete/<int:pk>/', views.admin_student_delete, name='admin_student_delete'),
    path('admin/students/details/<int:pk>/', views.admin_student_details, name='admin_student_details'),
    path('admin/students/change-password/<int:pk>/', views.admin_change_password, name='admin_change_password'),
    path('admin/search-student/', views.admin_search_student, name='admin_search_student'),
    
    # Admin - Fines
    path('admin/fines/', views.admin_fines, name='admin_fines'),
    path('admin/fines/select-issue/', views.admin_fine_select_issue, name='admin_fine_select_issue'),
    path('admin/fines/create-custom/', views.admin_fine_create_custom, name='admin_fine_create_custom'),
    path('admin/fines/create/<int:issue_id>/', views.admin_fine_create, name='admin_fine_create'),
    path('admin/fines/mark-paid/<int:pk>/', views.admin_fine_mark_paid, name='admin_fine_mark_paid'),
    path('admin/fines/delete/<int:pk>/', views.admin_fine_delete, name='admin_fine_delete'),
]