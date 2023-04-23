import re
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.forms import model_to_dict
from django.shortcuts import render
from apps.bot_app.data_actions import views_actions
from apps.bot_app.serializers import (
    AllBanksNameSerializer,
    ChangerBankChekerSerializer,
    ChangerBanksSerializer,
    ChangerProfileSerializer,
    CurrencyListSerializer,
    OfferSerializer,
    TransactionsSerializer,
    UserBanksSerializer,
    UserInitSerializer,
)
from apps.db_model.models import (
    AllMongolianBanks,
    BotUser,
    Changer,
    ChangerBankAccount,
    ChangerOffer,
    Currency,
    Transaction,
    UserBankAccount,
)
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    UpdateAPIView,
    ListAPIView,
)



class UserInitView(CreateAPIView, UpdateAPIView):

    permission_classes = (IsAuthenticated, )
    queryset = BotUser.objects.all()
    serializer_class = UserInitSerializer

    # def post(self, request, pk):
    #     data = BotUser.objects.all()
    #     content = {'message': 'Hello, World!'}
    #     return Response(content)


class AllBankNameView(ListAPIView):
    
    permission_classes = (IsAuthenticated, )
    queryset = AllMongolianBanks.objects.all()
    serializer_class = AllBanksNameSerializer


class CurrencyListView(ListAPIView):

    permission_classes = (IsAuthenticated, )
    queryset = Currency.objects.all()
    serializer_class = CurrencyListSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = [
        'id',
        'name',
    ]


class OfferView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, )
    queryset = ChangerOffer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['owner__name']
    filterset_fields = [
        'id',
        'owner',
        'bannerName',
        'currency',
        'rate',
        'banks__id',
        'minAmount',
        'maxAmount',
        'dateCreated',
        'isActive',
        'isDeleted',
    ]
    

class ChangerBankAccountView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, )
    queryset = ChangerBankAccount.objects.all()
    serializer_class = ChangerBanksSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_fields = [
        'name',
        'bankAccount',
        'owner',
        'currency__name',
        'isActive',
        'isDeleted'
    ]

    @action(detail=False, methods=['post'])
    def checker_info(self, request, *args, **kwargs):

        banks_id = request.data['banks_id']
        response_data = {}

        for i in banks_id:

            queryset = ChangerOffer.objects.filter(banks__id = i)
            serializer = ChangerBankChekerSerializer(queryset, many=True)

            response_data[i] = serializer.data

        return Response(response_data)

    

class UserBankAccountView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, )
    queryset = UserBankAccount.objects.all()
    serializer_class = UserBanksSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter
    )
    search_fields = ['currency__name']
    filterset_fields = [
        'name',
        'bankAccount',
        'owner',
        'currency',
        'isActive',
    ]


class ChangerProfileView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, )
    queryset = Changer.objects.all()
    serializer_class = ChangerProfileSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = [
        'tg',
        'name',
        'lastName',
        'phone',
        'dateCreated',
        'isActive',
    ]


class TransactionsView(viewsets.ModelViewSet):
    
    permission_classes = (IsAuthenticated, )
    queryset = Transaction.objects.all()
    serializer_class = TransactionsSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = [
        'changer',
        'offer',
        'user',
        'changerBank',
        'userBank',
        'claims',
        'isCompleted'
    ]

