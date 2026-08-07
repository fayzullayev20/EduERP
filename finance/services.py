from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Transaction, TransactionCategory


def create_transaction(
    amount: int,
    transaction_type: str,
    category_id: int,
    created_by,
    student=None,
    description: str = ""
) -> Transaction:
    """
    Kirim va chiqim tranzaksiyalarini yaratuvchi hamda talaba balansini
    avtomatik yangilovchi xavfsiz servis funksiyasi.
    """
    if amount <= 0:
        raise ValidationError({"amount": "Summa 0 dan katta bo'lishi kerak."})

    try:
        category = TransactionCategory.objects.get(id=category_id)
    except TransactionCategory.DoesNotExist:
        raise ValidationError({"category_id": "Bunday kategoriya topilmadi."})

    with transaction.atomic():
        trx = Transaction.objects.create(
            amount=amount,
            transaction_type=transaction_type,
            category=category,
            student=student,
            created_by=created_by,
            description=description
        )

        # Agar kirim bo'lsa va talabaga bog'langan bo'lsa, balansini oshiramiz
        if transaction_type == 'income' and student:
            if hasattr(student, 'top_up_balance'):
                student.top_up_balance(amount)
            else:
                student.balance += amount
                student.save(update_fields=['balance'])

        return trx


def get_financial_summary():
    """
    Umumiy kirim, chiqim va sof foyda hisobotini qaytaruvchi yordamchi funksiya.
    """
    from django.db.models import Sum, Q

    totals = Transaction.objects.aggregate(
        total_income=Sum('amount', filter=Q(transaction_type='income')),
        total_expense=Sum('amount', filter=Q(transaction_type='expense'))
    )

    income = totals['total_income'] or 0
    expense = totals['total_expense'] or 0

    return {
        'total_income': income,
        'total_expense': expense,
        'net_profit': income - expense
    }