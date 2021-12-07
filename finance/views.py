from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from finance.models import Finance
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from cerberus import Validator
from finance.serializers import FinanceSerializer

User = get_user_model()


class FinanceApi(APIView):
    queryset = User.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        validator = Validator(
            {
                "name": {"required": True, "type": "string", "maxlength": 128}
            }
        )
        if not validator.validate(request.data):
            return Response(
                {"errors": validator.errors, }, status=status.HTTP_400_BAD_REQUEST
            )
        finance = Finance.objects.create(
            **request.data, user=request.user
        )
        return Response({
            "code": "finance_created",
            "finance": finance.id
        }, status=status.HTTP_201_CREATED)

    def delete(self, request):
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
            if record.user != request.user:
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

    def get(self, request):
        finance = Finance.objects.filter(user=request.user)
        return Response({
            "count": finance.count(),
            "data": FinanceSerializer(finance, many=True).data
        }, status=status.HTTP_200_OK)
