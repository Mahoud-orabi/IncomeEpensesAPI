from rest_framework import serializers
from .models import Income
from django.db.models import Sum


class IncomeSerializers(serializers.ModelSerializer):
    # total_amount = serializers.SerializerMethodField()
    class Meta:
        model = Income
        fields = ['id','source','amount','description','date']

    # def get_total_amount(self,obj):
    #     queryset = Income.objects.filter(owner = obj.owner)
    #     total_amount = queryset.aggregate(total =Sum('amount'))['total']
    #     return total_amount