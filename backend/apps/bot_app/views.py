from json import loads, dumps
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework import filters
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
    UpdateAPIView,
    ListAPIView,
)



class UserInitView(CreateAPIView, UpdateAPIView, ListAPIView):

    permission_classes = (IsAuthenticated, )
    queryset = BotUser.objects.all()
    serializer_class = UserInitSerializer

    def get(self, request):
        queryset = BotUser.objects.all()
        content = [obj.tg for obj in queryset]
        return Response(content)


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
        'minAmount',
        'maxAmount',
        'dateCreated',
        'isActive',
        'isDeleted',
        'owner__online',
        'type',
    ]

    @action(detail=True, methods=['get'])
    def offer_valid_checker(self, request, *args, **kwargs):
        try:
            obj: ChangerOffer = self.get_object()
            owner = obj.owner
            last_edit = timezone.localtime(obj.dateEdited)
            data = {
                'edited': last_edit,
                'owner_online': owner.online
            }
            return Response(data=data, status=200)
        except Exception as e:
            data = {
                'exception': repr(e)
            }
            return Response(data=data, status=404)



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
        'isDeleted',
        'offers_ref__id',
        'offers_curr__id'
    ]

    @action(detail=False, methods=['get'])
    def checker(self, request, *args, **kwargs):

        owner = request.GET.get('owner')
        isDeleted = True if request.GET.get('isDeleted') == 'true' else False

        queryset = ChangerBankAccount.objects.filter(owner=owner, isDeleted=isDeleted)
        banks_serializer = ChangerBanksSerializer(queryset, many=True)
        banks_data = banks_serializer.data

        for i in banks_data:

            counter = 0
            ref_queryset = ChangerOffer.objects.filter(
                refBanks = i['id'],
                isActive=True,
                isDeleted=False)
            curr_queryset = ChangerOffer.objects.filter(
                currencyBanks = i['id'],
                isActive=True,
                isDeleted=False)

            for ref in ref_queryset:
                if ref.refBanks.count() == 1:
                    counter += 1

            for curr in curr_queryset:
                if curr.currencyBanks.count() == 1:
                    counter += 1

            i['will_deactivate'] = counter

        return Response(banks_data)
    

    @action(detail=True, methods=['patch'])
    def status_setter(self, request, *args, **kwargs):

        obj = self.get_object()
        serializer = ChangerBanksSerializer(
            obj,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=400)
        
        data = serializer.data
        is_active = data.get('isActive')
        is_deleted = data.get('isDeleted')

        if not is_active or is_deleted:

            r_queryset = ChangerOffer.objects.filter(refBanks=obj.id)
            r_serializer = OfferSerializer(data=r_queryset, many=True)
            r_serializer.is_valid()
            r_data = loads(dumps(r_serializer.data))

            c_queryset = ChangerOffer.objects.filter(currencyBanks=obj.id)
            c_serializer = OfferSerializer(data=c_queryset, many=True)
            c_serializer.is_valid()
            c_data = loads(dumps(c_serializer.data))

            for i in r_data:

                for r in i['refBanks']:
                    if r['id'] == obj.id:
                        i['refBanks'].remove(r)
                        i['refBanks_id'] = i['refBanks']

                if not i['refBanks']:
                    i['isActive'] = False
                
                r_offer = ChangerOffer.objects.get(id=i['id'])
                r_serializer = OfferSerializer(r_offer, data=i, partial=True)
                if r_serializer.is_valid():
                    r_serializer.save()

            for i in c_data:

                for c in i['refBanks']:
                    if c['id'] == obj.id:
                        i['refBanks'].remove(c)

                if not i['refBanks']:
                    i['isActive'] = False

                c_offer = ChangerOffer.objects.get(id=i['id'])
                c_serializer = OfferSerializer(c_offer, data=i, partial=True)
                if c_serializer.is_valid():
                    c_serializer.save()

        return Response(data)



class UserBankAccountView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, )
    queryset = UserBankAccount.objects.all()
    serializer_class = UserBanksSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_fields = [
        'name',
        'bankAccount',
        'owner',
        'currency__name',
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

    @action(detail=False, methods=['get'])
    def id_list(self, request, *args, **kwargs):
        queryset = Changer.objects.all()
        content = [obj.tg for obj in queryset if obj.online]
        return Response(content)


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
        'isCompleted',
        'changerAccepted',
        'type',
    ]

