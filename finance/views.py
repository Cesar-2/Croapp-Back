from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from finance.models import Finance, Cost
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from cerberus import Validator
from finance.serializers import FinanceSerializer
from user.util import TokenHandler

User = get_user_model()


class FinanceApi(APIView, TokenHandler):
    queryset = User.objects.filter(is_active=True)

    def post(self, request):
        payload, user = self.get_payload(request)
        if not payload:
            return Response({
                "code": "unauthorized",
                "detailed": "El token es incorrecto o expiro"
            }, status=status.HTTP_401_UNAUTHORIZED)
        validator = Validator(
            {
                "name": {"required": True, "type": "string", "maxlength": 128},
                "expected_amount": {"required": True, "type": "integer"},
            }
        )
        if not validator.validate(request.data):
            return Response(
                {"errors": validator.errors, }, status=status.HTTP_400_BAD_REQUEST
            )
        finance = Finance.objects.create(
            **request.data, user=user
        )
        return Response({
            "code": "finance_created",
            "finance": finance.id
        }, status=status.HTTP_201_CREATED)

    def delete(self, request):
        payload, user = self.get_payload(request)
        if not payload:
            return Response({
                "code": "unauthorized",
                "detailed": "El token es incorrecto o expiro"
            }, status=status.HTTP_401_UNAUTHORIZED)
        validator = Validator(
            {
                "id": {"required": True, "type": "string", "maxlength": 128}
            }
        )
        if not validator.validate(request.GET):
            return Response(
                {"errors": validator.errors, }, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            record = Finance.objects.get(id=int(request.GET.get("id")))
            if record.user != user:
                return Response({
                    "code": "this_cost_own_to_other_user",
                    "error": "this cost own to other user"
                }, status=status.HTTP_409_CONFLICT)
            record.delete()
            return Response({
                "code": "cost_deleted",
                "cost": request.GET.get("id")
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                "code": "cost_not_found",
                "error": "cost not found"
            }, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        payload, user = self.get_payload(request)
        if not payload:
            return Response({
                "code": "unauthorized",
                "detailed": "El token es incorrecto o expiro"
            }, status=status.HTTP_401_UNAUTHORIZED)
        finance = Finance.objects.filter(user=user)
        return Response({
            "count": finance.count(),
            "data": FinanceSerializer(finance, many=True).data
        }, status=status.HTTP_200_OK)


class CostApi(APIView, TokenHandler):
    queryset = User.objects.filter(is_active=True)

    def post(self, request):
        payload, user = self.get_payload(request)
        if not payload:
            return Response({
                "code": "unauthorized",
                "detailed": "El token es incorrecto o expiro"
            }, status=status.HTTP_401_UNAUTHORIZED)
        validator = Validator(
            {
                "name": {"required": True, "type": "string", "maxlength": 128},
                "amount_cost": {"required": True, "type": "integer"},
                "finance_id": {"required": True, "type": "integer"},
            }
        )
        if not validator.validate(request.data):
            return Response(
                {"errors": validator.errors, }, status=status.HTTP_400_BAD_REQUEST
            )
        finance_id = request.data.pop('finance_id')
        finance = Finance.objects.get(id=finance_id)
        cost = Cost.objects.create(**request.data, finance=finance)
        return Response({
            "code": "cost_created",
            "cost": cost.id
        }, status=status.HTTP_201_CREATED)

    def delete(self, request):
        payload, user = self.get_payload(request)
        if not payload:
            return Response({
                "code": "unauthorized",
                "detailed": "El token es incorrecto o expiro"
            }, status=status.HTTP_401_UNAUTHORIZED)
        validator = Validator(
            {
                "id": {"required": True, "type": "string", "maxlength": 128}
            }
        )
        if not validator.validate(request.GET):
            return Response(
                {"errors": validator.errors, }, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            record = Cost.objects.get(id=int(request.GET.get("id")))
            if record.user != user:
                return Response({
                    "code": "this_finance_own_to_other_user",
                    "error": "this finance own to other user"
                }, status=status.HTTP_409_CONFLICT)
            record.delete()
            return Response({
                "code": "finance_deleted",
                "finance": request.GET.get("id")
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                "code": "finance_not_found",
                "error": "finance not found"
            }, status=status.HTTP_404_NOT_FOUND)
