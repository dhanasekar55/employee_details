from django.urls import path
from . import views

urlpatterns = [
    # Home page, listing all employees
    path('', views.home, name='home'),

    # Employee-related paths
    path('employee/add/', views.add_employee, name='add_employee'),
    path('employee/<int:id>/', views.employee_detail, name='employee_detail'),
    path('employee/update/<int:id>/', views.update_employee, name='update_employee'),  # This is correct
    path('employee/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    
    path('employee/<int:id>/transaction/add/', views.add_transaction, name='add_transaction'),
    path('transaction/update/<int:transaction_id>/', views.update_transaction, name='update_transaction'),
    path('transaction/delete/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),

]
