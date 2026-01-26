"""
Custom Admin Site Configuration for ARTIFA FEST
Applies Stranger Things theme to Django admin interface
"""

from django.contrib.admin import AdminSite
from django.templatetags.static import static
from django.urls import path
from django import forms


class ArtifaAdminSite(AdminSite):
    """Custom Admin Site with ARTIFA FEST branding and styling"""
    
    site_header = "ARTIFA FEST - Admin Portal"
    site_title = "ARTIFA FEST Admin"
    index_title = "Welcome to the Upside Down Control Center"
    
    def get_app_list(self, request):
        """Customize the app list ordering"""
        app_list = super().get_app_list(request)
        
        # Custom app ordering
        app_order = {
            'core': 1,
            'auth': 2,
            'admin': 3,
        }
        
        app_list.sort(
            key=lambda x: app_order.get(x['app_label'], 999)
        )
        
        return app_list
    
    def each_context(self, request):
        """Add custom context variables"""
        context = super().each_context(request)
        context.update({
            'site_header': 'ARTIFA FEST Admin',
            'site_title': 'ARTIFA FEST',
            'index_title': 'Event Management Center',
        })
        return context
    
    class Media:
        css = {
            'all': (
                static('admin.css'),
                'https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap',
            )
        }
        js = (
            static('admin.js'),
        )


# Create instance of custom admin site
artifa_admin_site = ArtifaAdminSite(name='artifa_admin')
