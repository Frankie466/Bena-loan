from django.db import models
from django.contrib.auth.models import User
import random

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    id_number = models.CharField(max_length=10, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    next_of_kin_name = models.CharField(max_length=100)
    next_of_kin_phone = models.CharField(max_length=15)
    employment_status = models.CharField(
        max_length=20,
        choices=[
            ('employed', 'Employed'),
            ('self_employed', 'Self Employed'),
            ('unemployed', 'Unemployed')
        ]
    )
    loan_limit = models.IntegerField(default=0)
    savings_balance = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def assign_loan_limit(self):
        loan_limits = [
            4500, 7200, 14000, 28000,
        ]
        self.loan_limit = random.choice(loan_limits)
        self.save()

    def calculate_processing_fee(self):
        return 0.07 * self.loan_limit

    def __str__(self):
        return self.full_name

class SavingsOption(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    savings = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Ksh {self.amount} - Savings: Ksh {self.savings}"

class WithdrawalRequest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    requested_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.full_name} - Ksh {self.amount} on {self.requested_at.strftime('%Y-%m-%d')}"
