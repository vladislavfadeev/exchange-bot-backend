from django.contrib import admin
from apps.db_model.models import (
    AllMongolianBanks,
    BotUser,
    Changer,
    ChangerBankAccount,
    UserBankAccount,
    ChangerOffer,
    Currency,
    Transaction,
)


admin.site.register(Currency)
admin.site.register(BotUser)
admin.site.register(Changer)
admin.site.register(ChangerBankAccount)
admin.site.register(UserBankAccount)
admin.site.register(ChangerOffer)
admin.site.register(AllMongolianBanks)


admin.site.site_title = 'Панель администрирования OnlineShargaBot'
admin.site.site_header = 'Панель администрирования OnlineShargaBot'
