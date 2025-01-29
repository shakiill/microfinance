from allauth.account import views as auth_views
from django.urls import path, re_path

from . import views
from .customer import customer_edit
from .views import UserEditView, UserInfoView

urlpatterns = [
    path("signup/", views.signup, name="account_signup"),
    # path("signup/", auth_views.signup, name="account_signup"),
    path("login/", auth_views.login, name="account_login"),
    path("logout/", auth_views.logout, name="account_logout"),
    path("password/change/", auth_views.password_change, name="account_change_password"),
    path("password/set/", auth_views.password_set, name="account_set_password"),
    # path("inactive/", auth_views.account_inactive, name="account_inactive"),
    path("email/", auth_views.email, name="account_email"),
    path("confirm-email/", auth_views.email_verification_sent, name="account_email_verification_sent"),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", auth_views.confirm_email, name="account_confirm_email"),
    path("password/reset/", auth_views.password_reset, name="account_reset_password"),
    path("password/reset/done/", auth_views.password_reset_done, name="account_reset_password_done"),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", auth_views.password_reset_from_key,
            name="account_reset_password_from_key"),
    path("password/reset/key/done/", auth_views.password_reset_from_key_done,
         name="account_reset_password_from_key_done"),
    path('update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('details/', views.ProfileDetailView.as_view(), name='profile_detail'),
    # path('registration/', views.RegistrationWizardView.as_view(), name='account_signup')
    # dashboard user

    path('user/', views.UserListView.as_view(), name='user_list'),
    path('user/add/', views.UserCreateView.as_view(), name='user_add'),
    path('user/edit/<int:pk>/', UserEditView.as_view(), name='user_edit'),
    path('user/informations/<int:pk>/', UserInfoView.as_view(), name='user_info'),
    path('user/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    # custom url
    path('customer/<int:pk>/edit/', customer_edit, name='customer_edit'),
]
