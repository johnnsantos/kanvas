from django.urls import path
from .views import UserView

urlpatterns = [path("accounts/", UserView.as_view())]
