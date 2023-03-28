"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    # login.html
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutView, name="logout"),
    # register.html
    path("register/", views.registerView, name="register"),
    # view all receipts of outvoices - view_outvoices.html
    path("view_outvoices/", views.view_outvoices, name="view_outvoices"),
    # view all receipts of invoices - view_invoices.html
    path("view_invoices/", views.view_invoices, name="view_invoices"),
    # sell specific tire, form shows quantity sold, send tire info and quantity to Invoice Model - buy_tires.html
    path("sell_tires/<pk>/", views.sell_tires, name="sell_tires"),
    # buy specific tire, form shows quantity desired, send tire info and quantity to Outvoice Model - sell_tires.html
    path("buy_tires/<pk>/", views.buy_tires, name="buy_tires"),
    # add tire form - add_tire.html
    path("add_tire/", views.add_tire, name="add_tire_form"),
    # delete specific tire, "are you sure?" message, confirm button - delete_tire.html
    path("delete_tire/<pk>/", views.delete_tirePage, name="delete_tire"),
    # specific tire details - tire_info.html
    path("tire_info/<pk>/", views.tire_info, name="tire_info"),
    # list of tire inventory and search function in home page - home.html
    path("cart/", views.show_cart, name="cart"),
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
]
