from django import forms
from django.core.exceptions import ValidationError
from .models import Transaction, Status, TransactionType, Category, SubCategory
from datetime import date


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'status', 'transaction_type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'value': date.today().strftime('%Y-%m-%d')
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Необязательный комментарий к операции'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = Category.objects.none()
        self.fields['subcategory'].queryset = SubCategory.objects.none()

        if 'transaction_type' in self.data:
            try:
                transaction_type_id = int(self.data.get('transaction_type'))
                self.fields['category'].queryset = Category.objects.filter(
                    transaction_type_id=transaction_type_id
                ).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['category'].queryset = self.instance.transaction_type.categories.order_by('name')

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(
                    category_id=category_id
                ).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.order_by('name')


class TransactionFilterForm(forms.Form):
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label="Дата с"
    )

    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label="Дата по"
    )

    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        empty_label="Все статусы",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Статус"
    )

    transaction_type = forms.ModelChoiceField(
        queryset=TransactionType.objects.all(),
        required=False,
        empty_label="Все типы",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Тип операции"
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Все категории",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Категория"
    )

    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.all(),
        required=False,
        empty_label="Все подкатегории",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Подкатегория"
    )


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название статуса'
            })
        }


class TransactionTypeForm(forms.ModelForm):
    class Meta:
        model = TransactionType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название типа операции'
            })
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'transaction_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название категории'
            }),
            'transaction_type': forms.Select(attrs={'class': 'form-control'})
        }


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название подкатегории'
            }),
            'category': forms.Select(attrs={'class': 'form-control'})
        }