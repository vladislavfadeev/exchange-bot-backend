from stat import FILE_ATTRIBUTE_REPARSE_POINT
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
        'banks',
        'minAmount',
        'maxAmount',
        'dateCreated',
        'isActive',
    ]
    

class ChangerBankAccountView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, )
    queryset = ChangerBankAccount.objects.all()
    serializer_class = ChangerBanksSerializer
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
    ]




# class CustomerViewSet(viewsets.ModelViewSet):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer


# class CurrencyPairAPIList(generics.ListAPIView):
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication, )
#     queryset = CurrencyPair.objects.all()
#     serializer_class = CurrencyPairSerializer


# class ChangerAPIList(generics.ListAPIView):
#     queryset = Changer.objects.all()
#     serializer_class = ChangerListSerializer


# class ChangerBankAccountAPIViewSet(viewsets.ModelViewSet):
#     queryset = Changer.objects.all()
#     serializer_class = ChangerBankAccountSerializer


# class RequestViewSet(viewsets.ModelViewSet):
#     queryset = RequestModel.objects.all()
#     serializer_class = RequestSerializer


# class ResponseViewSet(viewsets.ModelViewSet):
#     queryset = ResponseModel.objects.all()
#     serializer_class = ResponseSerializer

#     @action(detail=True, methods=['get'])
#     def responses(self, request, *args, **kwargs):
#         queryset = views_actions.ResponseViewDataActions.all_responses(request,
#                                                                        *args,
#                                                                        **kwargs)
#         serializer = ResponseSerializer(queryset, many=True)

#         return Response(serializer.data)

#     def create(self, request):

#         data = views_actions.ResponseViewDataActions.create_action(request)
#         serializer = ResponseSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         print(request.headers)
#         return Response({'post': serializer.data})


# class CustomerChoiseViewSet(viewsets.ModelViewSet):
#     queryset = CustomerChoice.objects.all()
#     serializer_class = CustomerChoiceSerializer

#     def create(self, request):
#         print(request)
#         data = views_actions.ChoiseViewDataActions.create_action(request)
#         serializer = CustomerChoiceSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response({'post': serializer.data})


# class TransactionViewSet(viewsets.ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer

#     def create(self, request):

#         data = views_actions.TransactionViewDataActions.create_action(request)
#         serializer = TransactionSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response({'post': serializer.data})


# class WomenAPIList(generics.ListCreateAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer


# class WomenAPIUpdate(generics.UpdateAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer


# class WomenAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer


# class WomenAPIView(APIView):
#     def get(self, request):
#         queryset = Women.objects.all()
#         return Response({'posts': WomenSerializer(queryset, many=True).data})

#     def post(self, request):
#         serializer = WomenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response({'post': serializer.data})

#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({'error': 'Method PUT is not allowed'})

#         try:
#             instance = Women.objects.get(pk=pk)
#         except:
#             return Response({'error': 'Object is not exist'})

#         serializer = WomenSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'post': serializer.data})

#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({'error': 'Method delete is not allowed'})

#         try:
#             Women.objects.filter(pk=pk).delete()
#         except:
#             return Response({'error': 'Object is not exist'})

#         return Response({'post': f'Post {pk} has been deleted'})


# class WomenAPIView(generics.ListAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer
