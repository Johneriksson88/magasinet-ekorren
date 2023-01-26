from django.urls import path
from . import views
from main.views import customer_form, register_form, order_form, edit_user_info

urlpatterns = [
    path("", views.index, name='index'),
    path("customerform/", views.customer_form, name='customer_form'),
    path("orderform/", views.order_form, name='order_form'),
    path("login/", views.user_login, name='login'),
    path("logout/", views.user_logout, name='logout'),
    path("user_panel/", views.user_panel, name='user_panel'),
    path("register/", views.register_form, name='register'),
    path("delete_order/<str:pk>/", views.delete_order, name="delete_order"),
    path("delete_account/<str:pk>/", views.delete_account, name="delete_account"),
    path("exportcsv/", views.export_csv, name="export_csv"),
    path("not_registered/", views.not_registered, name="not_registered"),
    path("edit_info/", views.edit_user_info, name="edit_user_info")
]
