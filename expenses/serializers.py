from rest_framework import serializers
from .models import Expense


class ExpenseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id','category','amount','description','date']
