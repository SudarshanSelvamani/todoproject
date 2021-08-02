from django.urls import path
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("signup/", accounts_views.signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "settings/account/", accounts_views.UserUpdateView.as_view(), name="my_account"
    ),
    path(
        "settings/password/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "settings/password/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]
