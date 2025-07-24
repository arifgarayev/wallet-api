from logging import getLogger

from app.common import (
    CommonUtils,
    InsufficientFundsException,
)
from app.core.models import PointOfSale, Wallet
from django.db import transaction

logger = getLogger(__name__)


class TransactionService:

    POINT_OF_SALE_MODEL_CLS = PointOfSale
    RELATED_WALLET_MODEL_CLS = Wallet

    def __init__(self, view):
        self.view = view

    @transaction.atomic
    def wallet_to_wallet_transfer(self, request):
        serialized_data = self.view.input_serializer_cls(
            data=request.data
        )

        serialized_data.is_valid(raise_exception=True)

        locked_origin_wallet = self.RELATED_WALLET_MODEL_CLS.objects.select_for_update().get(
            id=serialized_data.validated_data.get(
                "origin_wallet_id", 0
            )
        )

        locker_destination_wallet = self.RELATED_WALLET_MODEL_CLS.objects.select_for_update().get(
            id=serialized_data.validated_data.get(
                "destination_wallet_id", 0
            )
        )

        if (
            locked_origin_wallet
            == locker_destination_wallet
        ):
            raise ValueError(
                "Origin and Destination should be distinct Wallets"
            )

        transactions: list = self._mutate_balance(
            origin_wallet=locked_origin_wallet,
            amount=serialized_data.validated_data.get(
                "amount", 0
            ),
            destination_wallet=locker_destination_wallet,
        )

        return self._prepare_response(
            model=transactions, is_many=True
        )

    @transaction.atomic
    def balance_standalone_operation(
        self, request, is_deduction=False
    ):
        serialized_data = self.view.input_serializer_cls(
            data=request.data,
            context={"skip_destination": True},
        )
        serialized_data.is_valid(raise_exception=True)

        locked_origin_wallet = self.RELATED_WALLET_MODEL_CLS.objects.select_for_update().get(
            id=serialized_data.validated_data.get(
                "origin_wallet_id", 0
            )
        )

        transaction_model = self._mutate_balance(
            origin_wallet=locked_origin_wallet,
            amount=serialized_data.validated_data.get(
                "amount", 0
            ),
            is_deduction=is_deduction,
        )

        return self._prepare_response(
            model=transaction_model
        )

    def _prepare_response(self, model, is_many=False):
        return self.view.output_serializer_cls(
            model, many=is_many
        )

    def _mutate_balance(
        self,
        origin_wallet,
        amount,
        destination_wallet=None,
        is_deduction=False,
    ):
        """destination_wallet argument is higher in priority
        than is_deduction, since business logic dictates
        if we have destintantion to where move funds from,
        we must deduct funds "from" first"""
        if not destination_wallet:
            # only top up origin wallet
            # meaning no balance movements

            updated_wallet = (
                self._arithmetic_operation(
                    wallet_model=origin_wallet,
                    amount=amount,
                )
                if not is_deduction
                else self._value_deduct(
                    wallet_model=origin_wallet,
                    amount=amount,
                )
            )

            transaction_model = self._init_transaction(
                wallet_model_to_relate=origin_wallet,
                amount=amount,
                is_deduction=is_deduction,
            )

            return transaction_model

        # should be valid both origin and destination arguments
        # should be checked against validity of the balance
        deducted_wallet = self._value_deduct(
            wallet_model=origin_wallet,
            amount=amount,
        )
        deducted_transaction_model = self._init_transaction(
            wallet_model_to_relate=deducted_wallet,
            amount=amount,
            is_deduction=True,
        )
        toptup_wallet = self._arithmetic_operation(
            wallet_model=destination_wallet, amount=amount
        )
        top_up_transaction_model = self._init_transaction(
            wallet_model_to_relate=toptup_wallet,
            amount=amount,
        )
        return [
            deducted_transaction_model,
            top_up_transaction_model,
        ]

    def _arithmetic_operation(self, wallet_model, amount):

        updated_balance = wallet_model.balance + amount

        wallet_model, _ = CommonUtils.model_update(
            wallet_model,
            fields=["balance"],
            data={"balance": updated_balance},
        )

        return wallet_model

    def _init_transaction(
        self,
        wallet_model_to_relate,
        amount,
        is_deduction=False,
    ):
        prep_kwargs = {
            "wallet": wallet_model_to_relate,
            "amount": (
                amount
                if not is_deduction
                else self._negatiate_amount(amount)
            ),
        }

        transaction_model = self._create(
            model_class=self.POINT_OF_SALE_MODEL_CLS,
            validated_data=prep_kwargs,
        )

        return transaction_model

    def _negatiate_amount(self, amount):

        return -1 * amount

    def _value_deduct(self, wallet_model, amount):
        is_valid = self._is_valid_for_deduction(
            wallet_model=wallet_model,
            desired_amount_to_deduct=amount,
        )

        if not is_valid:
            raise InsufficientFundsException(
                f"Insufficient funds in the balance. Please Deduct valid amount no greater than {wallet_model.balance}"
            )
        negatiate_amount = self._negatiate_amount(
            amount=amount
        )

        # TODO: continue from here later
        updated_wallet = self._arithmetic_operation(
            wallet_model=wallet_model,
            amount=negatiate_amount,
        )

        return updated_wallet

    def _is_valid_for_deduction(
        self, wallet_model, desired_amount_to_deduct
    ) -> bool:
        if (
            wallet_model.balance - desired_amount_to_deduct
            < 0
        ):
            return False
        return True

    def _create(self, model_class, validated_data):
        return model_class.objects.create(**validated_data)
