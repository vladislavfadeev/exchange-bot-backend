from django.urls import path, include
from rest_framework import routers
from bot_app.views import *

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'customer', CustomerViewSet, basename='customer')
router.register(r'request', RequestViewSet, basename='request')
router.register(r'response', ResponseViewSet, basename='response')
router.register(r'changer-bank-account', ChangerBankAccountAPIViewSet, basename='changer-bank-account')
router.register(r'customer-choice',CustomerChoiseViewSet, basename='customer-choice')
router.register(r'transaction', TransactionViewSet, basename='transaction')


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/curr-pair', CurrencyPairAPIList.as_view()),
    path('api/v1/changers-list', ChangerAPIList.as_view()),
    # path('api/v1/response/<int:pk>', ResponseViewSet.as_view({'get': 'list'})),
    # path('api/v1/response/<int:pk>', ResponseViewSet.as_view())
    # path('api/vq/changer-bank-account', ChangerBankAccountAPIViewSet.as_view())
]
