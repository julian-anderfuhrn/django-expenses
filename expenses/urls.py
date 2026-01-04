from django.urls import path
from . import views


app_name = "expenses"

urlpatterns = [
    # Expenses
    path("", views.expense_list, name="expense_list"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("create/", views.expense_create, name="expense_create"),
    path("<int:pk>/edit/", views.expense_update, name="expense_update"),
    path("<int:pk>/delete/", views.expense_delete, name="expense_delete"),
    # Categories
    path("categories/", views.category_list, name="category_list"),
    path("categories/create/", views.category_create, name="category_create"),
    path("categories/<int:pk>/edit/", views.category_update, name="category_update"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
]
