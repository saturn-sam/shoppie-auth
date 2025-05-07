
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Health check view
def health_check(request):
    return JsonResponse({'status': 'healthy', 'service': 'auth-service'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('health/', health_check, name='health_check'),
]
