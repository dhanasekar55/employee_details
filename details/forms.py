from django import forms
from .models import Employee, ProductTransaction

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'phone', 'address']


class ProductTransactionForm(forms.ModelForm):
    class Meta:
        model = ProductTransaction
        fields = ['product_name', 'price_per_unit', 'quantity', 'advance_amount', 'advance_date', 'paid', 'paid_date']

    advance_amount = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.0)
    advance_date = forms.DateField(widget=forms.SelectDateWidget(), required=False)
    paid = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.0)
    paid_date = forms.DateField(widget=forms.SelectDateWidget(), required=False)
