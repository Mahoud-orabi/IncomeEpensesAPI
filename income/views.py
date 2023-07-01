from rest_framework import generics,permissions
from .models import Income
from .serializers import IncomeSerializers
from .permissions import IsOwner

# Create your views here.


class IncomeListAPIView(generics.ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializers
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)



class IncomeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializers
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    lookup_field = 'id'

    
    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)

