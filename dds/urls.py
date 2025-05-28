from django.urls import path
from . import views

app_name = 'dds'

urlpatterns = [
    path('', views.index, name='index'),
    path('transaction/create/', views.transaction_create, name='transaction_create'),
    path('transaction/<int:pk>/edit/', views.transaction_update, name='transaction_update'),
    path('transaction/<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),

    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),

    path('references/', views.references, name='references'),

    path('status/create/', views.StatusCreateView.as_view(), name='status_create'),
    path('status/<int:pk>/edit/', views.StatusUpdateView.as_view(), name='status_update'),
    path('status/<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),

    path('transaction-type/create/', views.TransactionTypeCreateView.as_view(), name='transaction_type_create'),
    path('transaction-type/<int:pk>/edit/', views.TransactionTypeUpdateView.as_view(), name='transaction_type_update'),
    path('transaction-type/<int:pk>/delete/', views.TransactionTypeDeleteView.as_view(),
         name='transaction_type_delete'),

    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),

    path('subcategory/create/', views.SubCategoryCreateView.as_view(), name='subcategory_create'),
    path('subcategory/<int:pk>/edit/', views.SubCategoryUpdateView.as_view(), name='subcategory_update'),
    path('subcategory/<int:pk>/delete/', views.SubCategoryDeleteView.as_view(), name='subcategory_delete'),
]