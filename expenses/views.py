from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from .forms import ExpenseForm
from django.db.models import Sum
from datetime import date
from django.http import HttpResponse
from django.contrib import messages


@login_required
def dashboard(request):
    today = date.today()

    expenses = Expense.objects.filter(
        user=request.user, date__year=today.year, date__month=today.month
    )

    total_month = expenses.aggregate(total=Sum("amount"))["total"] or 0

    by_category = (
        expenses.values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    last_expenses = expenses.order_by("-date")[:5]

    return render(
        request,
        "dashboard.html",
        {
            "total_month": total_month,
            "by_category": by_category,
            "last_expenses": last_expenses,
        },
    )


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by("-date")
    total = sum(exp.amount for exp in expenses)
    return render(request, "expense_list.html", {"expenses": expenses, "total": total})


@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect("expenses:expense_list")
        else:
            print(form.errors)
    else:
        form = ExpenseForm(user=request.user)
    return render(request, "expense_form.html", {"form": form})


@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("expenses:expense_list")
    else:
        form = ExpenseForm(instance=expense, user=request.user)
    return render(request, "expense_form.html", {"form": form})


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == "POST":
        expense.delete()
        return redirect("expenses:expense_list")

    return render(request, "expense_confirm_delete.html", {"expense": expense})


@login_required
def category_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Category.objects.create(name=name, user=request.user)
            return redirect("expenses:category_list")

    return render(request, "category_form.html")


@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, "category_list.html", {"categories": categories})


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)

    if request.method == "POST":
        category.name = request.POST.get("name")
        category.save()
        return redirect("expenses:category_list")
    return render(
        request, "category_form.html", {"category": category, "is_edit": True}
    )


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)

    if category.expense_set.exists():
        messages.error(
            request,
            "you cannot delete this category because it has expenses associated",
        )
        return redirect("expenses:category_list")

    if request.method == "POST":
        category.delete()
        messages.success(request, "Category eliminated")
        return redirect("expenses:category_list")

    return render(
        request,
        "category_confirm_delete.html",
        {"category": category},
    )
