from rest_framework import generics,permissions,response
from .models import Income
from .serializers import IncomeSerializers
from .permissions import IsOwner
from django.db.models import Sum

# Create your views here.


class IncomeListAPIView(generics.ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializers
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # add pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            total = queryset.aggregate(total=Sum('amount'))['total']
            data = {
                'total': total,
                'income': serializer.data
            }
            return self.get_paginated_response(data)
         
        serializer = self.get_serializer(queryset, many=True)
        total = queryset.aggregate(total=Sum('amount'))['total']
        data = {
            'total': total,
            'results': serializer.data
        }
        return response.Response(data)



class IncomeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializers
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    lookup_field = 'id'

    
    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)

