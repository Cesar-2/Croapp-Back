from django.shortcuts import render
from landingpage.models import LandingPage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.


class LandingPageApi(APIView):
    def post(self, request):
        validator = Validator(
            {
                "name": {"required": True, "type": "string", "maxlength": 128},
                "last_name": {"required": True, "type": "string", "maxlength": 128},
                "password": {"required": True, "type": "string", "maxlength": 1000},
            }
        )
        if not validator.validate(request.data):
            return Response(
                {"errors": validator.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        LandingPage.objects.create(**request.data)
        return Response({
            "code": "content_created"
        }, status=status.HTTP_201_CREATED)
