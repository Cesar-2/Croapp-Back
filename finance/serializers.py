from rest_framework import serializers
from user.serializers import UserModelSerializer
from finance.models import Finance, Cost
from django.db.models import Sum


class CostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cost
        fields = "__all__"


class FinanceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    real_cost = serializers.SerializerMethodField()
    costs = serializers.SerializerMethodField()

    class Meta:

        model = Finance
        fields = ('id', 'user', 'name', 'real_cost',
                  'expected_amount', 'costs')

    def get_user(self, obj):
        return UserModelSerializer(obj.user).data

    def get_real_cost(self, obj):
        real_cost = Cost.objects.filter(finance=obj).aggregate(
            total=Sum('amount_cost')).get('total')
        if not real_cost:
            return 0
        return real_cost

    def get_costs(self, obj):
        return CostSerializer(Cost.objects.filter(finance=obj)).data
