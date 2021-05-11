from django.urls import path
from .views import CourseView, UpdateCourseView

urlpatterns = [
    path("courses/", CourseView.as_view(), name="post courses"),
    path("courses/registrations/", UpdateCourseView.as_view(), name="update course"),
]
