from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

def redirect_admin(request):
    """Redirect Django admin to custom admin dashboard if logged in as admin"""
    if request.session.get('is_admin'):
        return HttpResponseRedirect('/admin/dashboard/')
    # If not logged in, redirect to custom admin login
    return HttpResponseRedirect('/login/admin/')

urlpatterns = [
    path('admin/', redirect_admin, name='django_admin_redirect'),
    path('', include('library.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Library Management System"
admin.site.site_title = "Library Admin"
admin.site.index_title = "Welcome to Library Management System"