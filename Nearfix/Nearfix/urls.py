from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import home_view
from django.contrib import admin
admin.site.site_header = "NearFix Admin"
admin.site.site_title = "NearFix Admin Portal"
admin.site.index_title = "Welcome to NearFix Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('bookings.urls')),
    path('', home_view, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)