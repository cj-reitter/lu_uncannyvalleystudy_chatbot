from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage),
    path('chatbot/', views.chatbot),
    path('api/chat/', views.chat_api),
    path('survey/', views.survey),
    path('feedback/', views.feedback),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)