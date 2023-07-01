from rest_framework import serializers
from .models import Income


class IncomeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id','source','amount','description','date']