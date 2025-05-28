from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название статуса")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ['name']

    def __str__(self):
        return self.name


class TransactionType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название типа")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name="Тип операции"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['transaction_type', 'name']
        unique_together = ['name', 'transaction_type']

    def __str__(self):
        return f"{self.name} ({self.transaction_type.name})"


class SubCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название подкатегории")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name="Категория"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ['category', 'name']
        unique_together = ['name', 'category']

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Transaction(models.Model):
    date = models.DateField(verbose_name="Дата операции")
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name="Статус"
    )
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.PROTECT,
        verbose_name="Тип операции"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="Категория"
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        verbose_name="Подкатегория"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Сумма (руб.)"
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Операция ДДС"
        verbose_name_plural = "Операции ДДС"
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.date} - {self.transaction_type.name} - {self.amount} руб."

    def clean(self):
        """Валидация логических зависимостей"""
        from django.core.exceptions import ValidationError

        if self.category and self.transaction_type:
            if self.category.transaction_type != self.transaction_type:
                raise ValidationError({
                    'category': 'Выбранная категория не соответствует типу операции.'
                })

        if self.subcategory and self.category:
            if self.subcategory.category != self.category:
                raise ValidationError({
                    'subcategory': 'Выбранная подкатегория не соответствует категории.'
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)