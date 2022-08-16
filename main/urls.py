from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='MiniInsta',
        description='Социальная сеть с картинками',
        default_version = 'v1'
    ),
    public=True
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger')),
    path('api/v1/posts/', include('applications.posts.urls')),
    path('api/v1/account/', include('applications.account.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
