from django.urls import path
from .views import CourseView, UpdateCourseView

urlpatterns = [
    path("courses/", CourseView.as_view()),
    path("courses/registrations/", UpdateCourseView.as_view()),
]
