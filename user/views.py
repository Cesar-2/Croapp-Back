from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from user.serializers import UserLoginSerializer, UserModelSerializer

from django.contrib.auth import get_user_model, login
from django.shortcuts import get_object_or_404
from cerberus import Validator
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
    queryset = User.objects.filter(is_active=True)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        validator = Validator(
            {
                "email": {
                    "required": True, "type": "string", "regex": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                },
                "password": {"required": True, "type": "string", "maxlength": 128, "regex": r'^\w+$'},
            }
        )
        if not validator.validate(request.data):
            return Response(
                {"errors": validator.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        login(request, user)
        return Response(data, status=status.HTTP_201_CREATED)
