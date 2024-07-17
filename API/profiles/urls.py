from django.urls import path
from profiles.views import details_profile_view, profile_list_view

urlpatterns = [
    path("", profile_list_view, name="profile-list"),
    path("<str:username>/", details_profile_view, name="profile"),
]
