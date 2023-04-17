from apps.bot_app.views import *
from apps.bot_app.models import *
from datetime import datetime

class ResponseViewDataActions:

    def all_responses(request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        queryset = ResponseModel.objects.filter(
                        changer_id_id = pk
                        )
        return queryset

    def create_action(request):
        customer_info = Customer.objects.get(
                        requestmodel__id = request.data['request_id']
        )
        request_info = RequestModel.objects.get(
                        pk=request.data['request_id']
        )
        currency_info = CurrencyPair.objects.get(
                        requestmodel__id = request.data['request_id']
        )
        data = {
            "request_id": request.data['request_id'],
            "customer_id": customer_info.tg_id,
            "changer_id": request.data['changer_id'],
            "currency_pair_id": currency_info.id,
            "customer_bank": request_info.customer_bank,
            "changer_bank": request.data['changer_bank'],
            "customer_rate": request_info.sell_rate,
            "buy_rate": request.data['buy_rate'],
            "amount": request_info.amount
        }
        return data
    

class ChoiseViewDataActions:

    def create_action(request):
        choice_data = ResponseModel.objects.get(
                        pk = request.data['response_id']
        )
        
        data = {
            "response_id": choice_data.id,
            "customer_id": choice_data.customer_id.tg_id,
            "changer_id": choice_data.changer_id.tg_id,
            "currency_pair_id": choice_data.currency_pair.id,
            "customer_bank_account": request.data['cust_bank_account'],
            "changer_bank_account": request.data['changer_account'],
            "customer_bank": choice_data.customer_bank,
            "changer_bank": choice_data.changer_bank,
            "amount": choice_data.amount,
            "agreed_rate": choice_data.buy_rate
        }

        return data


class TransactionViewDataActions:

    def create_action(request):
        transaction_data = CustomerChoice.objects.get(
                        pk = request.data['post_choice_id']
        )
        data = {
            "post_choice_id": transaction_data.id,
            "customer_bank": transaction_data.
                                        response_id.
                                        customer_bank,
            "changer_bank": transaction_data.
                                        response_id.
                                        changer_bank,
            "customer_send_money_date": datetime.now(),
            "customer_proof": request.data['user_proof']
        }

        return data