from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.forms import model_to_dict
from django.shortcuts import render
from .data_actions import views_actions
from .serializers import *
from .models import *



class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CurrencyPairAPIList(generics.ListAPIView):
    queryset = CurrencyPair.objects.all()
    serializer_class = CurrencyPairSerializer


class ChangerAPIList(generics.ListAPIView):
    queryset = Changer.objects.all()
    serializer_class = ChangerListSerializer


class ChangerBankAccountAPIViewSet(viewsets.ModelViewSet):
    queryset = Changer.objects.all()
    serializer_class = ChangerBankAccountSerializer


class RequestViewSet(viewsets.ModelViewSet):
    queryset = RequestModel.objects.all()
    serializer_class = RequestSerializer


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = ResponseModel.objects.all()
    serializer_class = ResponseSerializer

    @action(detail=True, methods=['get'])
    def responses(self, request, *args, **kwargs):
        queryset = views_actions.ResponseViewDataActions.all_responses(request,
                                                                        *args,
                                                                        **kwargs)
        serializer = ResponseSerializer(queryset, many=True)
        
        return Response(serializer.data)

    def create(self, request):
    
        data = views_actions.ResponseViewDataActions.create_action(request)
        serializer = ResponseSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(request.headers)
        return Response({'post': serializer.data})


class CustomerChoiseViewSet(viewsets.ModelViewSet):
    queryset = CustomerChoice.objects.all()
    serializer_class = CustomerChoiceSerializer

    def create(self, request):
        print(request)
        data = views_actions.ChoiseViewDataActions.create_action(request)
        serializer = CustomerChoiceSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request):

        data = views_actions.TransactionViewDataActions.create_action(request)
        serializer = TransactionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})













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


