from django.contrib import admin
from django.urls import path
from yawning_titan_gui.views import home
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home.as_view()),
    path('admin/', admin.site.urls),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
