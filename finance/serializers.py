from rest_framework import serializers
from user.serializers import UserModelSerializer
from finance.models import Finance


class FinanceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    user = serializers.SerializerMethodField()

    class Meta:

        model = Finance
        fields = ('user', 'name')

    def get_user(self, obj):
        return UserModelSerializer(obj.user).data
