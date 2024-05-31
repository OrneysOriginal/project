from django.urls import path
from person import views


app_name = "person"

urlpatterns = [
    path("", views.ProfilePage.as_view(), name="profile"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("registration/", views.Registration.as_view(), name="registration"),
]
