from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Expense
from django.db.models import Sum
from datetime import date
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
