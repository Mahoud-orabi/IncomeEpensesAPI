from rest_framework import generics,permissions
from .models import Expense
from .serializers import ExpenseSerializers
from .permissions import IsOwner

# Create your views here.


class ExpenseListAPIView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializers
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)



class ExpenseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializers
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    lookup_field = 'id'


    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)

