from locale import currency
from django.db import models



class BotUser(models.Model):

    tg = models.IntegerField(primary_key=True)
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
        return f'{self.name} {self.lastName}'
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



class Changer(models.Model):

    tg = models.IntegerField(primary_key=True)
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

    def __str__(self):
        return f'{self.name} {self.lastName}'
    
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
    bankAccount = models.IntegerField(
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
    bankAccount = models.IntegerField(
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
    banks = models.ManyToManyField(
        ChangerBankAccount,
        verbose_name= 'Банки',
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

    def __str__(self):
        return f'{self.owner} - {self.currency}'
    
    class Meta:
        verbose_name = 'Оффер'
        verbose_name_plural = 'Офферы'


class OfferResponse(models.Model):

    offer = models.ForeignKey(
        ChangerOffer,
        on_delete=models.CASCADE
    )
    changer = models.ForeignKey(
        Changer,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        BotUser,
        on_delete=models.CASCADE
    )
    currency = models.CharField(max_length=10)
    userAmount = models.FloatField()
    userRate = models.FloatField(blank=True)
    isActive = models.BooleanField(default=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    sellBank = models.CharField(max_length=50)
    buyBank = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Отклик на оффер'
        verbose_name_plural = 'Отклики на офферы'
    

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
    createDate = models.DateTimeField(auto_now_add=True)
    claims = models.BooleanField(default=False)
    isCompleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Совершенный перевод'
        verbose_name_plural = 'Совершенные переводы'