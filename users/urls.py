from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "users"
urlpatterns = [
    path("", views.users, name="users"),
    path("<int:user_id>/follow/", views.follow, name="follow"),
    path("<str:username>/", views.profile, name="profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)