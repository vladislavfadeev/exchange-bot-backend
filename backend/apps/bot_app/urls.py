from django.urls import path, include
from rest_framework import routers
from apps.bot_app.views import (
    AllBankNameView,
    ChangerBankAccountView,
    ChangerProfileView,
    CurrencyListView,
    OfferView,
    TransactionsView,
    UserBankAccountView,
    UserInitView,
)

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"offer", OfferView),
router.register(r"changer_banks", ChangerBankAccountView),
router.register(r"user_banks", UserBankAccountView),
router.register(r"changer_profile", ChangerProfileView),
router.register(r"transactions", TransactionsView),


urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/user", UserInitView.as_view()),
    path("api/v1/banks_name_list", AllBankNameView.as_view()),
    path("api/v1/currency", CurrencyListView.as_view()),
]
