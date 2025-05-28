from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Transaction, Status, TransactionType, Category, SubCategory
from .forms import (
    TransactionForm, TransactionFilterForm, StatusForm,
    TransactionTypeForm, CategoryForm, SubCategoryForm
)


def index(request):
    filter_form = TransactionFilterForm(request.GET)
    transactions = Transaction.objects.select_related(
        'status', 'transaction_type', 'category', 'subcategory'
    ).all()

    if filter_form.is_valid():
        if filter_form.cleaned_data['date_from']:
            transactions = transactions.filter(date__gte=filter_form.cleaned_data['date_from'])

        if filter_form.cleaned_data['date_to']:
            transactions = transactions.filter(date__lte=filter_form.cleaned_data['date_to'])

        if filter_form.cleaned_data['status']:
            transactions = transactions.filter(status=filter_form.cleaned_data['status'])

        if filter_form.cleaned_data['transaction_type']:
            transactions = transactions.filter(transaction_type=filter_form.cleaned_data['transaction_type'])

        if filter_form.cleaned_data['category']:
            transactions = transactions.filter(category=filter_form.cleaned_data['category'])

        if filter_form.cleaned_data['subcategory']:
            transactions = transactions.filter(subcategory=filter_form.cleaned_data['subcategory'])

    paginator = Paginator(transactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_income = transactions.filter(transaction_type__name='Пополнение').aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_expense = transactions.filter(transaction_type__name='Списание').aggregate(
        total=Sum('amount')
    )['total'] or 0

    balance = total_income - total_expense

    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    }

    return render(request, 'dds/index.html', context)


def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Операция успешно создана!')
            return redirect('dds:index')
    else:
        form = TransactionForm()

    return render(request, 'dds/transaction_form.html', {
        'form': form,
        'title': 'Создание операции'
    })


def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Операция успешно обновлена!')
            return redirect('dds:index')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'dds/transaction_form.html', {
        'form': form,
        'title': 'Редактирование операции'
    })


def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Операция успешно удалена!')
        return redirect('dds:index')

    return render(request, 'dds/transaction_confirm_delete.html', {
        'transaction': transaction
    })


def load_categories(request):
    transaction_type_id = request.GET.get('transaction_type')
    categories = Category.objects.filter(transaction_type_id=transaction_type_id).order_by('name')

    return JsonResponse(list(categories.values('id', 'name')), safe=False)


def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id).order_by('name')

    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)


def references(request):
    context = {
        'statuses': Status.objects.all(),
        'transaction_types': TransactionType.objects.all(),
        'categories': Category.objects.select_related('transaction_type').all(),
        'subcategories': SubCategory.objects.select_related('category').all(),
    }

    return render(request, 'dds/references.html', context)


class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'dds/status_form.html'
    success_url = reverse_lazy('dds:references')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить статус'
        return context


class StatusUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'dds/status_form.html'
    success_url = reverse_lazy('dds:references')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать статус'
        return context


class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'dds/status_confirm_delete.html'
    success_url = reverse_lazy('dds:references')


class TransactionTypeCreateView(CreateView):
    model = TransactionType
    form_class = TransactionTypeForm
    template_name = 'dds/transaction_form.html'
    success_url = reverse_lazy('dds:references')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить тип операции'
        return context


class TransactionTypeUpdateView(UpdateView):
    model = TransactionType
    form_class = TransactionTypeForm
    template_name = 'dds/transaction_form.html'
    success_url = reverse_lazy('dds:references')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать тип операции'
        return context


class TransactionTypeDeleteView(DeleteView):
    model = TransactionType
    template_name = 'dds/transaction_confirm_delete.html'
    success_url = reverse_lazy('dds:references')


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dds/category_form.html'
    success_url = reverse_lazy('dds:references')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить категорию'
        return context


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dds/category_form.html'
    success_url = reverse_lazy('dds:references')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать категорию'
        return context


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'dds/category_confirm_delete.html'
    success_url = reverse_lazy('dds:references')


class SubCategoryCreateView(CreateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'dds/subcategory_form.html'
    success_url = reverse_lazy('dds:references')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить подкатегорию'
        return context


class SubCategoryUpdateView(UpdateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'dds/subcategory_form.html'
    success_url = reverse_lazy('dds:references')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать подкатегорию'
        return context


class SubCategoryDeleteView(DeleteView):
    model = SubCategory
    template_name = 'dds/subcategory_confirm_delete.html'
    success_url = reverse_lazy('dds:references')