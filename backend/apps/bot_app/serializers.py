from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
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
import io



class UserInitSerializer(serializers.ModelSerializer):

    class Meta:
        model = BotUser
        fields = '__all__'


class AllBanksNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = AllMongolianBanks
        fields = '__all__'


class CurrencyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = '__all__'


class UserBanksSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserBankAccount
        fields = '__all__'


class ChangerBanksSerializer(serializers.ModelSerializer):

    currency = CurrencyListSerializer(read_only=True)

    class Meta:
        model = ChangerBankAccount
        fields = '__all__'


class ChangerBankChekerSerializer(serializers.ModelSerializer):

    banks = ChangerBanksSerializer(many=True, read_only=True)

    class Meta:
        model = ChangerOffer
        fields = ('id', 'currency', 'banks')


class OfferSerializer(serializers.ModelSerializer):

    banks = ChangerBanksSerializer(many=True, read_only=True)
    
    banks_id = serializers.PrimaryKeyRelatedField(
        queryset=ChangerBankAccount.objects.all(), 
        source='banks',
        many=True,
        write_only=True,
    )

    class Meta:
        model = ChangerOffer
        fields = '__all__'


class ChangerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Changer
        fields = '__all__'


class TransactionsSerializer(serializers.ModelSerializer):

    changerBank = ChangerBanksSerializer(read_only = True)

    changerBank_id = serializers.PrimaryKeyRelatedField(
        queryset=ChangerBankAccount.objects.all(), 
        source='changerBank',
        write_only=True,
    )
    userBank = UserBanksSerializer(read_only = True)

    userBank_id = serializers.PrimaryKeyRelatedField(
        queryset=UserBankAccount.objects.all(), 
        source='userBank',
        write_only=True,
    )    

    class Meta:
        model = Transaction
        fields = '__all__'



