from django.db import models



class Customer(models.Model):
    tg_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=15, blank=True) # unique=True,
    date_created = models.DateTimeField(auto_now_add=True)


class Changer(models.Model):
    tg_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=15, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)


class BankAccount(models.Model):
    name = models.CharField(max_length=50)
    bank_account = models.IntegerField(unique=True)
    bank_user = models.ForeignKey(Changer, related_name='accounts', on_delete=models.PROTECT)


class CurrencyPair(models.Model):
    name = models.CharField(max_length=20)


class RequestModel(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    currency_pair = models.ForeignKey(CurrencyPair, on_delete=models.PROTECT)
    customer_bank = models.CharField(max_length=50, blank=True)
    changer_bank = models.CharField(max_length=50, blank=True)
    sell_rate = models.FloatField(blank=True)
    amount = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)


class ResponseModel(models.Model):
    request_id = models.ForeignKey(RequestModel, on_delete=models.PROTECT)
    customer_id = models.ForeignKey(Customer, on_delete=models.PROTECT)
    changer_id = models.ForeignKey(Changer, on_delete=models.PROTECT)
    currency_pair = models.ForeignKey(CurrencyPair, on_delete=models.PROTECT)
    customer_bank = models.CharField(max_length=50)
    changer_bank = models.CharField(max_length=50)
    customer_rate = models.FloatField(blank=True)
    buy_rate = models.FloatField()
    amount = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)


class CustomerChoice(models.Model):
    response_id = models.ForeignKey(ResponseModel, on_delete=models.PROTECT)
    customer_id = models.ForeignKey(Customer, on_delete=models.PROTECT)
    changer_id = models.ForeignKey(Changer, on_delete=models.PROTECT)
    currency_pair = models.ForeignKey(CurrencyPair, on_delete=models.PROTECT)
    customer_bank_account = models.IntegerField(null=True)
    changer_bank_account = models.IntegerField(null=True)
    customer_bank = models.CharField(max_length=50)
    changer_bank = models.CharField(max_length=50)
    amount = models.FloatField()
    agreed_rate = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    choice_id = models.OneToOneField(CustomerChoice, on_delete=models.PROTECT)
    customer_bank = models.CharField(max_length=50)
    changer_bank = models.CharField(max_length=50)
    customer_accept = models.BooleanField(default=False)
    changer_accept = models.BooleanField(default=False)
    customer_send_money_date = models.DateTimeField(auto_now_add=True)
    customer_accept_date = models.DateTimeField(null=True)
    changer_accept_date = models.DateTimeField(null=True)
    customer_proof = models.CharField(max_length=100, blank=True)
    changer_proof = models.CharField(max_length=100, blank=True)






# class Transaction(models.Model):
#     request_id = models.ForeignKey(RequestModel, on_delete=models.PROTECT)
#     response_id = models.ForeignKey(ResponseModel, on_delete=models.PROTECT)
#     choise_id = models.ForeignKey(CustomerChoice, on_delete=models.PROTECT)
#     currency_pair = models.ForeignKey(CurrencyPair, on_delete=models.PROTECT)
#     customer_id = models.ForeignKey(Customer, on_delete=models.PROTECT)
#     changer_id = models.ForeignKey(Changer, on_delete=models.PROTECT)
#     customer_bank = models.CharField(max_length=50)
#     changer_bank = models.CharField(max_length=50)
#     customer_accept = models.BooleanField(default=False)
#     changer_accept = models.BooleanField(default=False)
#     customer_send_money_date = models.DateTimeField(blank=True)
#     customer_accept_date = models.DateTimeField(blank=True)
#     changer_accept_date = models.DateTimeField(blank=True)
