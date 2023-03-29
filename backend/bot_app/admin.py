from django.contrib import admin
from .models import *



admin.site.register(Customer)
admin.site.register(Changer)
# admin.site.register(Bank)
admin.site.register(BankAccount)
admin.site.register(CurrencyPair)
admin.site.register(RequestModel)
admin.site.register(ResponseModel)
admin.site.register(CustomerChoice)
admin.site.register(Transaction)