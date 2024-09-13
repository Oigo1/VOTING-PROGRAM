from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('vote/<int:contestant_id>/', views.vote, name='vote'),
    path('submit_vote/', views.submit_vote, name='submit_vote'),
    path('results/', views.results, name='results'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)