from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Category


@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(
        request,
        "category_list.html",
        {"categories": categories},
    )


@login_required
def category_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Category.objects.create(name=name, user=request.user)
            return redirect("expenses:category_list")

    return render(request, "category_form.html")


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)

    if request.method == "POST":
        category.name = request.POST.get("name")
        category.save()
        return redirect("expenses:category_list")

    return render(
        request,
        "category_form.html",
        {"category": category, "is_edit": True},
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
