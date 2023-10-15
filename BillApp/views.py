from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import ParticipantForm, ExpenseForm
from .models import Participant, Expense, ExpenseParticipant
from django.core.mail import send_mail
from django.db.models import Sum

def index(request):
    return render(request, 'index.html')

@api_view(['POST'])
def create_expense(request):
    data = request.data
    no_of_persons = data.get('final_no_of_persons')
    expense_name = data.get('final_expense_name')
    
    expense_form = ExpenseForm({
        'amount': 0,
        'description': expense_name,
    })
    
    if expense_form.is_valid():
        expense_instance = expense_form.save()
    else:
        return JsonResponse({"status": "error", "message": "Invalid expense data"}, status=400)
    
    try:
        with transaction.atomic():
            total_expense = 0
            participants = []
            bill_split_data = []
            for i in range(1, int(no_of_persons) + 1):
                participant_form = ParticipantForm({
                    'name': data.get(f'name{i}'),
                    'email': data.get(f'email{i}'),
                    'phone_number': data.get(f'phone{i}'),
                    'expense_name': data.get(f'expense_name{i}')
                })

                if participant_form.is_valid():
                    participant_instance = participant_form.save()
                else:
                    return JsonResponse({"status": "error", "message": f"Invalid participant data for person {i}"}, status=400)

                expense = float(data.get(f'expense{i}', 0))
                ExpenseParticipant.objects.create(
                    participant=participant_instance,
                    expense=expense_instance,
                    owed_amount=0, 
                )

                participants.append((participant_instance, expense))
                total_expense += expense

            Expense.objects.filter(id=expense_instance.id).update(amount=total_expense)

            average_expense = total_expense / int(no_of_persons)
            for participant, expense in participants:
                owed_amount = average_expense - expense
                ExpenseParticipant.objects.filter(participant=participant).update(owed_amount=owed_amount)
                bill_split_data.append({
                    'participant_name': participant.name,
                    'owed_amount': round(owed_amount, 2)  # Rounding to 2 decimal places for cleaner output
                })

        return JsonResponse({
            "status": "success", 
            "message": "Data saved and bill split calculated successfully.",
            "bill_split": bill_split_data  # Including the bill split data
        }, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

@api_view(['GET'])
def get_passbook(request, participant_id):
    try:
        participant = Participant.objects.get(id=participant_id)
    except Participant.DoesNotExist as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    expense_participants = ExpenseParticipant.objects.filter(participant=participant)
    
    total_owe = expense_participants.aggregate(Sum('owed_amount'))['owed_amount__sum'] or 0

    expenses_detail = []
    for ep in expense_participants:
        expenses_detail.append({
            'expense_description': ep.expense.description,
            'expense_amount': str(ep.expense.amount),
            'owed_amount': str(ep.owed_amount),
        })
    
    passbook = {
        'participant_name': participant.name,
        'total_owe': str(total_owe),
        'expenses_detail': expenses_detail,
    }

    return JsonResponse({"status": "error", "data": passbook}, status=200)