from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Expense
from ..forms import ExpenseForm


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by("-date")
    total = sum(exp.amount for exp in expenses)
    return render(
        request,
        "expense_list.html",
        {"expenses": expenses, "total": total},
    )


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

    return render(
        request,
        "expense_confirm_delete.html",
        {"expense": expense},
    )
