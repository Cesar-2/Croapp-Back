from django.conf import settings

import datetime as dt
import jwt

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from user.serializers import UserLoginSerializer, UserModelSerializer
from user.models import Auth
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from cerberus import Validator
from django.views.decorators.csrf import csrf_protect
from user.util import TokenHandler
# Create your views here.

User = get_user_model()


class UserApi(APIView):
    queryset = User.objects.filter(is_active=True)

    def post(self, request):
        validator = Validator(
            {
                "citizen_code": {"required": True, "type": "string", "maxlength": 11, "regex": r'[0-9]+'},
                "first_name": {"required": True, "type": "string", "maxlength": 128},
                "second_name": {"required": False, "type": "string", "maxlength": 128},
                "last_name": {"required": True, "type": "string", "maxlength": 128},
                "email": {
                    "required": True, "type": "string", "regex": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                },
                "phone_number": {"required": True, "type": "string", "maxlength": 15, "regex": r'[0-9]+'},
                "password": {"required": True, "type": "string", "maxlength": 128, "regex": r'^\w+$'},
            }
        )
        if not validator.validate(request.data):
            return Response(
                {"errors": validator.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(email=request.data.get("email")).first():
            return Response({
                "code": "user_already_exist",
                "error": "user already exist in the platform"
            }, status=status.HTTP_409_CONFLICT)
        user = User.objects.create_user(
            **request.data, username=request.data.get("email"))
        return Response({
            "code": "user_created",
            "user": user.id
        }, status=status.HTTP_201_CREATED)


class UserLoginApi(APIView):
    def post(self, request):

        validator = Validator({
            "email": {"required": True, "type": "string"},
            "password": {"required": True, "type": "string", "minlength": 7},
            "keep_logged_in": {"required": True, "type": "boolean"}
        })
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_filtering_params",
                "detailed": "Parámetros de búsqueda inválidos",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(
            email=request.data["email"]
        ).first()

        if not user:
            return Response({
                "code": "user_not_found",
                "detailed": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        if not check_password(request.data["password"], user.password):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        refresh = get_random_string(30)

        token = jwt.encode({
            'expiration_date': str(
                (
                    dt.datetime.now() +
                    dt.timedelta(
                        days=settings.TOKEN_EXP_DAYS
                        if not request.data['keep_logged_in']
                        else settings.KEEP_LOGGED_IN_TOKEN_EXP_DAYS
                    )
                )
            ),
            'email': request.data["email"],
            'profiles': [val.names for val in user.profile.all()],
            'refresh': refresh
        }, settings.SECRET_KEY, algorithm='HS256')

        User.objects.filter(
            email=request.data['email']
        ).update(last_login=timezone.now())
        Auth.objects.create(token=token)

        return Response({
            "token": token,
            "refresh": refresh,
            "id": user.pk,
            "email": user.email,
            "amount_expense": user.amount_expense,
            "profiles": [val.names for val in user.profile.all()]
        }, status=status.HTTP_201_CREATED)


class UserEarnApi(APIView, TokenHandler):

    def patch(self, request):
        payload, user = self.get_payload(request)
        if not payload:
            return Response({
                "code": "unauthorized",
                "detailed": "El token es incorrecto o expiro"
            }, status=status.HTTP_401_UNAUTHORIZED)
        validator = Validator(
            {
                "amount_expense": {"required": True, "type": "integer", "regex": r'[0-9]+'},
            }
        )
        if not validator.validate(request.data):
            return Response(
                {"errors": validator.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        user.amount_expense = request.data.get('amount_expense')
        user.save(update_fields=["amount_expense"])
        return Response(data, status=status.HTTP_200_OK)
