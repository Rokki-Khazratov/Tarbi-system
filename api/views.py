from rest_framework import generics
from .models import *
from .serializers import *
from itertools import chain

from rest_framework import generics
from django.db.models import Q
from .models import Stuff
from .serializers import StuffSerializer

class StaffListAPIView(generics.ListAPIView):
    serializer_class = StuffSerializer

    def get_queryset(self):
        queryset = Stuff.objects.all()
        position = self.request.query_params.get('position')
        min_salary = self.request.query_params.get('min_salary')
        max_salary = self.request.query_params.get('max_salary')
        sex = self.request.query_params.get('sex')
        name = self.request.query_params.get('name')
        start_date_after = self.request.query_params.get('start_date_after')
        start_date_before = self.request.query_params.get('start_date_before')

        if position:
            queryset = queryset.filter(position=position)
        
        if min_salary:
            queryset = queryset.filter(salary__gte=min_salary)
        
        if max_salary:
            queryset = queryset.filter(salary__lte=max_salary)
        
        if sex:
            queryset = queryset.filter(sex=sex)
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        if start_date_after:
            queryset = queryset.filter(start_date__gte=start_date_after)
        
        if start_date_before:
            queryset = queryset.filter(start_date__lte=start_date_before)

        return queryset


class StuffDetailAPIView(generics.RetrieveAPIView):
    queryset = Stuff.objects.all()
    serializer_class = StuffSerializer
    lookup_field = 'pk'



class KidListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = KidsSerializer

    def get_queryset(self):
        queryset = Kid.objects.all()
        is_paid = self.request.query_params.get('is_paid')

        if is_paid is not None:
            is_paid = is_paid.lower() in ['true', '1']
            queryset = queryset.filter(month_archives__is_paid=is_paid).distinct()
        return queryset

class KidRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kid.objects.all()
    serializer_class = KidSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['filter_is_paid'] = self.request.query_params.get('is_paid', None)
        return context



class IncomeTransactionListCreateAPIView(generics.ListCreateAPIView):
    queryset = IncomeTransaction.objects.all()
    serializer_class = IncomeTransactionSerializer



class IncomeTransactionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IncomeTransaction.objects.all()
    serializer_class = IncomeTransactionSerializer



class MonthArchiveListCreateAPIView(generics.ListCreateAPIView):
    queryset = MonthArchive.objects.all()
    serializer_class = MonthArchiveSerializer

class MonthArchiveRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MonthArchive.objects.all()
    serializer_class = MonthArchiveSerializer





class GroupListCreateAPIView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class JournalListCreateAPIView(generics.ListCreateAPIView):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer

class JournalRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer   

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    