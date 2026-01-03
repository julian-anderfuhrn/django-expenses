from django.urls import path
from .views import (
    expense_list,
    expense_create,
    category_list,
    category_create,
    category_delete,
    category_update,
    expense_update,
    expense_delete,
    dashboard,
)

app_name = "expenses"

urlpatterns = [
    path("", expense_list, name="expense_list"),
    path("dashboard/", dashboard, name="dashboard"),
    path("create/", expense_create, name="expense_create"),
    path("categories/", category_list, name="category_list"),
    path("categories/create", category_create, name="category_create"),
    path("categories/<int:pk>/edit", category_update, name="category_update"),
    path("categories/<int:pk>/delete", category_delete, name="category_delete"),
    path("<int:pk>/edit/", expense_update, name="expense_update"),
    path("<int:pk>/delete/", expense_delete, name="expense_delete"),
]
