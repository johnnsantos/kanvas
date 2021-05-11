from django.urls import path
from .views import ActivitiesView

urlpatterns = [
    path("activities/", ActivitiesView.as_view()),
    path("activities/<int:user_id>/", ActivitiesView.as_view()),
]
