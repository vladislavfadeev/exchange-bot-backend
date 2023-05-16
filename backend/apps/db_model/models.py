from datetime import datetime, timedelta
from typing import Iterable, Optional
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver



class BotUser(models.Model):

    tg = models.BigIntegerField(primary_key=True)
    name = models.CharField(
        'Имя',
        max_length=30,
        blank=True
    )
    lastName = models.CharField(
        'Фамилия',
        max_length=30,
        blank=True
    )
    phone = models.CharField(
        'Телефон',
        max_length=15,
        blank=True
    )
    dateCreated = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.tg} - {self.name} {self.lastName}'
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



class Changer(models.Model):

    tg = models.BigIntegerField(primary_key=True)
    name = models.CharField(
        'Имя',
        max_length=30
    )
    lastName = models.CharField(
        'Фамилия',
        max_length=30
    )
    phone = models.CharField(
        'Телефон',
        max_length=15,
        unique=True
    )
    dateCreated = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    isActive = models.BooleanField(default=True)
    online = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.tg} - {self.name} {self.lastName}'

    def save(self, *args, **kwargs):
        obj, bool = ChangerScore.objects.get_or_create(owner=self)
        if bool:
            obj.save()
        return super().save()
    
    class Meta:
        verbose_name = 'Обменник'
        verbose_name_plural = 'Обменники'



class Currency(models.Model):

    name = models.CharField(
        max_length=20,
        unique=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


class AllMongolianBanks(models.Model):

    name = models.CharField(
        'Название банка',
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Банк'
        verbose_name_plural = 'Все банки'


class ChangerBankAccount(models.Model):

    name = models.CharField(
        'Наименование',
        max_length=50
    )
    bankAccount = models.BigIntegerField(
        'Номер счета',
        unique=True
    )
    owner = models.ForeignKey(
        Changer,
        verbose_name='Владелец',
        related_name='accounts',
        on_delete=models.CASCADE
    )
    currency = models.ForeignKey(
        Currency,
        verbose_name='Валюта',
        on_delete=models.DO_NOTHING
    )
    comments = models.CharField(
        max_length=50,
        blank=True)
    isActive = models.BooleanField(default=True)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner} - {self.name} - {self.currency}'
    
    class Meta:
        verbose_name = 'Банковский счет обменника'
        verbose_name_plural = 'Банковские счета обменников'


class UserBankAccount(models.Model):

    name = models.CharField(
        'Наименование',
        max_length=50
    )
    bankAccount = models.BigIntegerField(
        'Номер счета',
        unique=True
    )
    owner = models.ForeignKey(
        BotUser,
        verbose_name='Владелец',
        related_name='accounts',
        on_delete=models.CASCADE
    )
    currency = models.ForeignKey(
        Currency,
        verbose_name='Валюта',
        on_delete=models.DO_NOTHING
    )
    comments = models.CharField(
        max_length=50,
        blank=True)
    isActive = models.BooleanField(default=True)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner} - {self.name} - {self.currency}'
    
    class Meta:
        verbose_name = 'Банковский счет пользователя'
        verbose_name_plural = 'Банковские счета пользователей'


class ChangerOffer(models.Model):

    owner = models.ForeignKey(
        Changer,
        verbose_name='Владелец',
        on_delete=models.CASCADE
    )
    bannerName = models.CharField(
        'Название оффера',
        max_length=64,
        blank=True
    )
    currency = models.CharField(
        'Валюта',
        max_length=10
    )
    rate = models.FloatField('Курс в MNT')
    refBanks = models.ManyToManyField(
        ChangerBankAccount,
        verbose_name= 'Банки MNT',
        related_name= 'ref_banks',
    )
    currencyBanks = models.ManyToManyField(
        ChangerBankAccount,
        verbose_name= 'Валютные банки',
        related_name= 'currency_banks',
    )
    minAmount = models.FloatField(
        'Минимальная сумма сделки',
        blank=True,
        null=True
    )
    maxAmount = models.FloatField(
        'Макимальная сумма сделки',
        blank=True,
        null=True
    )
    dateCreated = models.DateTimeField(
        'Дата создания',
        auto_now=True
    )
    isActive = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)
    type = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.owner} - {self.currency}'
    
    class Meta:
        verbose_name = 'Оффер'
        verbose_name_plural = 'Офферы'

    


class ChangerScore(models.Model):

    owner = models.OneToOneField(
        Changer,
        related_name='score',
        on_delete = models.CASCADE,
        primary_key = True
    )
    total_amount = models.FloatField(
        default=0,
        null=True,
        blank=True
    )
    total_transactions = models.IntegerField(
        default=0,
        null=True,
        blank=True
    )
    total_claims = models.IntegerField(
        default=0,
        null=True,
        blank=True
    )

    @property
    def avg_amount(self):
        try:
            avg_amount = self.total_amount / self.total_transactions
        except ZeroDivisionError:
            avg_amount = 0
        return avg_amount
    
    @property
    def avg_time(self):

        total_time = 0
        queryset = Transaction.objects.filter(
            changer = self.owner
        )
        for i in queryset:
            if i.react_time is not None:
                total_time += i.react_time

        try:
            avg_time = total_time / self.total_transactions
        except ZeroDivisionError:
            avg_time = 0

        return str(timedelta(seconds=avg_time)).split('.')[0]



class Transaction(models.Model):

    changer = models.ForeignKey(
        Changer,
        on_delete=models.CASCADE
    )
    offer = models.ForeignKey(
        ChangerOffer,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        BotUser,
        on_delete=models.CASCADE
    )
    changerBank = models.ForeignKey(
        ChangerBankAccount,
        on_delete=models.CASCADE
    )
    userBank = models.ForeignKey(
        UserBankAccount,
        on_delete=models.CASCADE
    )
    sellCurrency = models.CharField(max_length=10)
    buyCurrency = models.CharField(max_length=10)
    sellAmount = models.FloatField()
    buyAmount = models.FloatField()
    rate = models.FloatField()
    userSendMoneyDate = models.DateTimeField(
        blank=True,
        null=True
    )
    userAcceptDate = models.DateTimeField(
        blank=True,
        null=True
    )
    changerSendMoneyDate = models.DateTimeField(
        blank=True,
        null=True
    )
    changerAcceptDate = models.DateTimeField(
        blank=True,
        null=True
    )
    userProofType = models.CharField(
        max_length=50,
        blank=True
    )
    changerProofType = models.CharField(
        max_length=50,
        blank=True
    )
    userProof = models.CharField(
        max_length=500,
        blank=True
    )
    changerProof = models.CharField(
        max_length=500,
        blank=True
    )
    type = models.CharField(max_length=5)
    createDate = models.DateTimeField(auto_now_add=True)
    react_time = models.FloatField(null=True, blank=True)
    changerAccepted = models.BooleanField(default=False)
    claims = models.BooleanField(default=False)
    isCompleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} - {self.sellCurrency}'
    
    def save(self, *args, **kwargs):

        if self.changerSendMoneyDate:
            user_time = self.userSendMoneyDate
            changer_time = self.changerSendMoneyDate
            delta = changer_time - user_time
            value = delta.total_seconds()
            self.react_time = value
        
        if self.userAcceptDate:
            score = ChangerScore.objects.get(owner = self.changer)
            score.total_amount += self.buyAmount
            score.total_transactions += 1
            score.save()

        if self.claims:
            score = ChangerScore.objects.get(owner = self.changer)
            score.total_claims += 1
            score.save()

        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Совершенный перевод'
        verbose_name_plural = 'Совершенные переводы'
