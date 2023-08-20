from rest_framework.views import APIView
import datetime
from rest_framework import response, status
from expenses.models import Expense
from income.models import Income
from django.db.models import Sum
# Create your views here.


class ExpenseSummaryStats(APIView):

    def get_amount_for_category(self,expense_list,category):
        expenses = expense_list.filter(category=category)
        amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        return {'amount':str(amount)}

    def get_category(self,expense):
        return expense.category
    
    def get_remaining_income(self,request):
        today_date = datetime.date.today()
        ayear_ago = today_date - datetime.timedelta(days=30 * 12)
        expenses = Expense.objects.filter(owner = request.user, date__gte=ayear_ago, date__lte=today_date)
        income = Income.objects.filter(owner = request.user, date__gte=ayear_ago, date__lte=today_date)
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        total_income = income.aggregate(Sum('amount'))['amount__sum'] or 0
        return {'Total_income': total_income, 'Total_expenses': total_expenses, 'Your_balance': total_income - total_expenses}


    def get(self,request):
        today_date = datetime.date.today()
        ayear_ago = today_date - datetime.timedelta(days=30*12)
        expenses = Expense.objects.filter(owner = request.user, date__gte=ayear_ago, date__lte=today_date)
        final = {}
        categories = list(set(map(self.get_category,expenses)))
        for category in categories:
            final[category] = self.get_amount_for_category(expenses, category)
        income_data = self.get_remaining_income(request)
        return response.Response({'category_data':final,'income_data':income_data},status=status.HTTP_200_OK)


class IncomeSourcesSummaryStats(APIView):

    def get_amount_for_source(self,income_list,source):
        income = income_list.filter(source=source)
        amount = income.aggregate(Sum('amount'))['amount__sum'] or 0
        return {'amount':str(amount)}

    def get_category(self,income):
        return income.source

    def get(self,request):
        today_date = datetime.date.today()
        ayear_ago = today_date - datetime.timedelta(days=30*12)
        income = Income.objects.filter(owner = request.user, date__gte=ayear_ago, date__lte=today_date)
        final = {}
        sources = list(set(map(self.get_category,income)))
        total_income = income.aggregate(Sum('amount'))['amount__sum'] or 0
        for source in sources:
            final[source] = self.get_amount_for_source(income, source)
        return response.Response({'income_sources_data':final,'total_income':total_income},status=status.HTTP_200_OK)
