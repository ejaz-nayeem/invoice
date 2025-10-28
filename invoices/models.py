
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Invoice(models.Model):
    
    
    customer_name = models.CharField(max_length=255)

    customer_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    
    def clean(self):
        if self.customer_phone and not self.customer_phone.isdigit():
            raise ValidationError(
                {'customer_phone': 'Phone number must contain only digits.'},
                code='invalid_phone_number'
            )
        
    def __str__(self):
        status = "Paid" if self.is_paid else "Pending"
        # Use self.pk (or self.id) for representation
        return f"Invoice #{self.pk} for {self.customer_name} - Status: {status}"

    @property
    def sub_total(self):
        total = 0
        for item in self.items.all():
            total += item.quantity * item.amount
        return total


class Item(models.Model):
    invoice = models.ForeignKey(
        'Invoice',
        related_name='items',
        on_delete=models.CASCADE
    )
    
    product_name = models.CharField(max_length=255)
    
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        null=False,
        blank=False
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    def __str__(self):
        return f"{self.product_name} ({self.quantity} × {self.amount:.2f})"

    @property
    def total_amount(self):
        return self.quantity * self.amount