from django.urls import path 
from . views import register,login_view,logout_view,delete_account,admin_signup
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
app_name="register"


urlpatterns = [
    path("admin/signup/",admin_signup,name="admin_signup"),
    path("",register,name="register"),
    path("login/",login_view,name="login_view"),
    path("logout/",logout_view,name="logout_view"),
    path("delete/<int:id>/",delete_account,name="delete_account"),
    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
]
