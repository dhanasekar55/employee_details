from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee, ProductTransaction
from .forms import EmployeeForm, ProductTransactionForm
from decimal import Decimal
from django.db.utils import IntegrityError

def home(request):
    employees = Employee.objects.all()
    return render(request, 'home.html', {'employees': employees})

def employee_detail(request, id):
    employee = get_object_or_404(Employee, id=id)
    transactions = ProductTransaction.objects.filter(employee=employee)

    total_products = transactions.count()
    grand_total = sum([transaction.total_amount for transaction in transactions])
    total_paids = sum([transaction.paid for transaction in transactions])
    total_advance = sum([transaction.advance_amount for transaction in transactions])
    balance_due = grand_total - (total_paids + total_advance)
    total_paid = total_paids + total_advance

    remaining_quantities = {}
    for transaction in transactions:
        remaining_quantities[transaction.id] = transaction.remaining_quantity_from_balance

    return render(request, 'employee_detail.html', {
        'employee': employee,
        'transactions': transactions,
        'total_products': total_products,
        'grand_total': grand_total,
        'total_paid': total_paid,
        'balance_due': balance_due,
        'remaining_quantities': remaining_quantities,
        'total_advance':total_advance
    })

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})

def add_transaction(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == 'POST':
        form = ProductTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.employee = employee

            # Ensure default values are set if fields are empty or not provided
            if not transaction.paid:
                transaction.paid = Decimal('0.0')
            if not transaction.advance_amount:
                transaction.advance_amount = Decimal('0.0')
            if not transaction.total_amount:
                transaction.total_amount = Decimal('0.0')
            if not transaction.balance:
                transaction.balance = Decimal('0.0')
            if not transaction.remaining_cash_owed:
                transaction.remaining_cash_owed = Decimal('0.0')
            if not transaction.remaining_quantity_from_balance:
                transaction.remaining_quantity_from_balance = 0
            if not transaction.additional_quantity:
                transaction.additional_quantity = 0

            # Calculate total_amount if not provided (using price_per_unit and quantity)
            if transaction.total_amount == Decimal('0.0'):
                transaction.total_amount = transaction.price_per_unit * transaction.quantity

            try:
                # Save the transaction
                transaction.save()
                return redirect('employee_detail', id=employee.id)
            except IntegrityError as e:
                error_message = 'There was an issue saving the transaction. Please try again.'
                return render(request, 'add_transaction.html', {
                    'form': form, 
                    'employee': employee, 
                    'error_message': error_message
                })
        else:
            error_message = "Form data is invalid. Please check the fields."
            return render(request, 'add_transaction.html', {
                'form': form, 
                'employee': employee, 
                'error_message': error_message
            })
    else:
        form = ProductTransactionForm()

    return render(request, 'add_transaction.html', {'form': form, 'employee': employee})

def update_transaction(request, transaction_id):
    transaction = get_object_or_404(ProductTransaction, id=transaction_id)

    if request.method == 'POST':
        form = ProductTransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('employee_detail', id=transaction.employee.id)  # Redirect to the employee details page
    else:
        form = ProductTransactionForm(instance=transaction)

    return render(request, 'update_transaction.html', {'form': form, 'transaction': transaction})

def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(ProductTransaction, id=transaction_id)
    
    # If the user is confirming the deletion
    if request.method == 'POST':
        # Delete the transaction and redirect to employee detail page
        employee_id = transaction.employee.id
        transaction.delete()
        return redirect('employee_detail', id=employee_id)
    
    # If not confirming, show confirmation page
    return render(request, 'confirm_delete_transaction.html', {'transaction': transaction})

def update_employee(request, id):
    employee = get_object_or_404(Employee, pk=id)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_detail', id=employee.id)  # Ensure you have 'employee_detail' URL pattern
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'update_employee.html', {'form': form, 'employee': employee})

def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    employee.delete()
    return redirect('home')
