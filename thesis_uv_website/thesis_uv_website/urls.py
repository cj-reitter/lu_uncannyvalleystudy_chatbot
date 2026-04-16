from django.contrib import admin
from django.urls import path
from . import views
from avatar_ranking import views as ranking_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage),
    path('home/', views.homepage),
    path('chatbot/', views.chatbot),
    path('api/chat/', views.chat_api),
    path('survey/', views.survey),
    path('feedback/', views.feedback),
    path('ranking/', ranking_views.ranking),
    path('ranking/get-next-image/', ranking_views.get_next_image),
    path('ranking/submit-ranking/', ranking_views.submit_ranking),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)