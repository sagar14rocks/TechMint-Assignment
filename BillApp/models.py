from django.db import models

# Create your models here.
class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.description} - {self.amount}"

class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    expense_name = models.CharField(max_length=50, blank=True, null=True)
    expenses = models.ManyToManyField(Expense, related_name='participants', through='ExpenseParticipant')

    def __str__(self):
        return self.name

class ExpenseParticipant(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    owed_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.participant.name} owes {self.owed_amount} for {self.expense.description}"
