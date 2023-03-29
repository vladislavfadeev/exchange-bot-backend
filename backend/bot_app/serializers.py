from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import *
import io

class CurrencyPairSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyPair
        fields = '__all__'


class ChangerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Changer
        fields = ('tg_id', 'name', 'last_name')


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'
        # depth = 1


class ChangerBankAccountSerializer(serializers.ModelSerializer):
    accounts = BankAccountSerializer(many=True, read_only=True)

    class Meta:
        model = Changer
        fields = ('accounts', )
        

class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        # fields = '__all__'
        fields = ('tg_id', 'name', 'last_name', 
                  'phone', 'requestmodel_set')
        # depth = 1


class RequestSerializer(serializers.ModelSerializer):

    customer_id = serializers.PrimaryKeyRelatedField(
                            queryset=Customer.objects.all(), 
                            source='customer', write_only=True)
    
    currency_pair_id = serializers.PrimaryKeyRelatedField(
                            queryset=CurrencyPair.objects.all(), 
                            source='currency_pair', write_only=True)

    class Meta:
        model = RequestModel
        fields = '__all__'
        depth = 1




class ResponseSerializer(serializers.ModelSerializer):

    currency_pair_id = serializers.PrimaryKeyRelatedField(
                            queryset=CurrencyPair.objects.all(), 
                            source='currency_pair', write_only=True)
    
    currency_pair = CurrencyPairSerializer(read_only=True)

    class Meta:
        model = ResponseModel
        fields = '__all__'
        

class CustomerChoiceSerializer(serializers.ModelSerializer):

    currency_pair_id = serializers.PrimaryKeyRelatedField(
                            queryset=CurrencyPair.objects.all(), 
                            source='currency_pair', write_only=True)
    
    currency_pair = CurrencyPairSerializer(read_only=True)

    class Meta:
        model = CustomerChoice
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):

    post_choice_id = serializers.PrimaryKeyRelatedField(
                            queryset=CustomerChoice.objects.all(), 
                            source='choice_id', write_only=True)
    
    choice_id = CustomerChoiceSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'



    # def create(self, validated_data):
    #     request = Request(
    #         customer = validated_data['customer'],
    #         currency_pair = validated_data['currency_pair'],
    #         customer_bank = validated_data['customer_bank'],
    #         changer_bank = validated_data['changer_bank'],
    #         sell_rate = validated_data['sell_rate'],
    #         amount = validated_data['amount']
    #     )
    #     request.save()
    #     return request



# class RequestSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=50)
#     content = serializers.CharField()
#     time_create = serializers.DateTimeField(read_only=True)
#     time_update = serializers.DateTimeField(read_only=True)
#     is_published = serializers.BooleanField(default=True)
#     cat_id = serializers.IntegerField()

#     def create(self, validated_data):
#         return Request.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.content = validated_data.get('content', instance.content)
#         instance.time_update = validated_data.get('time_update', instance.time_update)
#         instance.is_punlished = validated_data.get('is_published', instance.is_published)
#         instance.cat_id = validated_data.get('cat_id', instance.cat_id)
#         instance.save()
#         return instance






# def encode():
#     model = WomenModel('Angelina Jolie', 'Content: Angelina Jolie')
#     model_sr = WomenSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep = '\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
     

# def decode():
#     stream = io.BytesIO(b'{"title":"Angelina Jolie","content":"Content: Angelina Jolie"}')
#     print(stream)
#     data = JSONParser().parse(stream)
#     print(data)
#     serializer = WomenSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)