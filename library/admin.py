from django.contrib import admin
from .models import Admin, Author, Book, Student, IssueRequest, Fine

@admin.register(Admin)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'full_name', 'email', 'is_active', 'last_login']
    list_filter = ['is_active', 'created_at']
    search_fields = ['username', 'full_name', 'email']
    readonly_fields = ['created_at', 'last_login']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date', 'created_at']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'category', 'total_copies', 'available_copies']
    search_fields = ['title', 'author__name', 'isbn']
    list_filter = ['category', 'author']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'username', 'full_name', 'email', 'department', 'status', 'last_login']
    search_fields = ['student_id', 'username', 'first_name', 'last_name', 'email']
    list_filter = ['status', 'department']
    readonly_fields = ['created_at', 'updated_at', 'last_login']
    
    def save_model(self, request, obj, form, change):
        if not change:  # New object
            # Password should be hashed
            if 'password' in form.changed_data:
                obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

@admin.register(IssueRequest)
class IssueRequestAdmin(admin.ModelAdmin):
    list_display = ['book', 'student', 'status', 'request_date', 'expected_return_date']
    search_fields = ['book__title', 'student__student_id']
    list_filter = ['status', 'request_date']

@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount', 'days_overdue', 'is_paid', 'payment_date']
    search_fields = ['student__student_id']
    list_filter = ['is_paid', 'payment_method']