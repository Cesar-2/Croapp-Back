from rest_framework import serializers
from user.serializers import UserModelSerializer
from finance.models import Finance, Cost
from django.db.models import Sum


class FinanceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    real_cost = serializers.SerializerMethodField()

    class Meta:

        model = Finance
        fields = ('user', 'name', 'real_cost', 'expected_amount')

    def get_user(self, obj):
        return UserModelSerializer(obj.user).data

    def get_real_cost(self, obj):
        real_cost = Cost.objects.filter(finance=obj).aggregate(
            total=Sum('amount_cost')).get('total')
        if not real_cost:
            return 0
        return real_cost
