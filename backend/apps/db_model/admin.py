from django.contrib import admin
from apps.db_model.models import (
    AllMongolianBanks,
    BotUser,
    Changer,
    ChangerBankAccount,
    UserBankAccount,
    ChangerOffer,
    ChangerScore,
    Currency,
    Transaction,
    CryptoRate,
    CryptoOrder,
    RateModel
)


admin.site.register(Currency)
admin.site.register(BotUser)
admin.site.register(Changer)
admin.site.register(ChangerBankAccount)
admin.site.register(UserBankAccount)
admin.site.register(ChangerOffer)
admin.site.register(AllMongolianBanks)
admin.site.register(ChangerScore)
admin.site.register(Transaction)
admin.site.register(CryptoRate)
admin.site.register(CryptoOrder)
admin.site.register(RateModel)


admin.site.site_title = 'Панель администрирования OnlineShargaBot'
admin.site.site_header = 'Панель администрирования OnlineShargaBot'
