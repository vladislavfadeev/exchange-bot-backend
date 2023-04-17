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
router.register(r'offer', OfferView),
router.register(r'changer_banks', ChangerBankAccountView),
router.register(r'user_banks', UserBankAccountView),
router.register(r'changer_profile', ChangerProfileView),
router.register(r'transactions', TransactionsView),
# router.register(r'request', RequestViewSet, basename='request')
# router.register(r'response', ResponseViewSet, basename='response')
# router.register(r'changer-bank-account', ChangerBankAccountAPIViewSet, basename='changer-bank-account')
# router.register(r'customer-choice',CustomerChoiseViewSet, basename='customer-choice')
# router.register(r'transaction', TransactionViewSet, basename='transaction')


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/user', UserInitView.as_view()),
    path('api/v1/user/<int:pk>', UserInitView.as_view()),
    path('api/v1/banks_name_list', AllBankNameView.as_view()),
    path('api/v1/currency', CurrencyListView.as_view()),
    # path('api/v1/changers-list', ChangerAPIList.as_view()),
    # path('api/v1/index', Index.as_view())
    # path('api/v1/response/<int:pk>', ResponseViewSet.as_view({'get': 'list'})),
    # path('api/v1/response/<int:pk>', ResponseViewSet.as_view())
    # path('api/vq/changer-bank-account', ChangerBankAccountAPIViewSet.as_view())
]
