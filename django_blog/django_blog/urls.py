from django.contrib import admin
from django.urls import path, include
from blog import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Home page
    path("", views.home, name="home"),

    # Authentication system
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", views.signup, name="signup"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),

    # Custom login/logout templates
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="blog/logout.html"), name="logout"),

    # CRUD URLs (namespaced)
    path("posts/", include(("blog.urls", "blog"), namespace="blog")),
]
