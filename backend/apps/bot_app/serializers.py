from rest_framework import serializers
from apps.db_model.models import (
    AllMongolianBanks,
    BotUser,
    Changer,
    ChangerBankAccount,
    ChangerOffer,
    ChangerScore,
    Currency,
    Transaction,
    UserBankAccount,
)


class UserInitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = "__all__"


class AllBanksNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllMongolianBanks
        fields = "__all__"


class CurrencyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class UserBanksSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBankAccount
        fields = "__all__"


class ChangerBanksSerializer(serializers.ModelSerializer):
    currency = CurrencyListSerializer(read_only=True)

    class Meta:
        model = ChangerBankAccount
        fields = "__all__"


class ChangerScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangerScore
        fields = ("total_amount", "total_transactions", "avg_amount", "avg_time")


class ChangerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Changer
        fields = "__all__"


class OfferSerializer(serializers.ModelSerializer):
    refBanks = ChangerBanksSerializer(many=True, read_only=True)

    refBanks_id = serializers.PrimaryKeyRelatedField(
        queryset=ChangerBankAccount.objects.all(),
        source="refBanks",
        many=True,
        write_only=True,
    )
    currencyBanks = ChangerBanksSerializer(many=True, read_only=True)

    currencyBanks_id = serializers.PrimaryKeyRelatedField(
        queryset=ChangerBankAccount.objects.all(),
        source="currencyBanks",
        many=True,
        write_only=True,
    )

    class Meta:
        model = ChangerOffer
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        score_data = ChangerScore.objects.get(owner=instance.owner)
        sr = ChangerScoreSerializer(score_data)

        data["owner_score"] = sr.data
        # data['score'] = instance.job_result.user.username     # в instance объект класса, указанный в model=
        # data['status'] = instance.job_result.status
        # data['created'] = instance.job_result.created
        # data['completed'] = instance.job_result.completed
        return data


class TransactionsSerializer(serializers.ModelSerializer):
    changerBank = ChangerBanksSerializer(read_only=True)

    changerBank_id = serializers.PrimaryKeyRelatedField(
        queryset=ChangerBankAccount.objects.all(),
        source="changerBank",
        write_only=True,
    )
    userBank = UserBanksSerializer(read_only=True)

    userBank_id = serializers.PrimaryKeyRelatedField(
        queryset=UserBankAccount.objects.all(),
        source="userBank",
        write_only=True,
    )

    class Meta:
        model = Transaction
        fields = "__all__"
