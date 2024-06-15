
from rest_framework import serializers
from .models import *
from companies.models import CompanySetting
from companies.serializers import CompanySerializer
from orders.models import Order, OrderPayment

class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name',read_only=True)
    added_by = serializers.CharField(read_only=True)
    updated_by = serializers.CharField(read_only=True)
    added_by_name  = serializers.CharField(source='added_by.first_name',read_only=True)
    order_totals = serializers.SerializerMethodField()
    ref_no = serializers.SerializerMethodField()
    order_payments = serializers.SerializerMethodField()

    def get_order_totals(self, obj):
        order_totals = 0
        payments = OrderPayment.objects.filter(order__id=obj.id)
        if payments:
            for payment in payments:
                    if payment.pay_type == 'normal':
                        order_totals += payment.amount
                    else:
                        order_totals -= payment.amount
        return order_totals
  
    def get_ref_no(self, obj):
        ref_no = ''
        payment = OrderPayment.objects.filter(order=obj.id).order_by('-id').first()
        if payment:
            ref_no = payment.ref_no
        return ref_no
    
    def get_order_payments(self, obj):
        payments = OrderPayment.objects.filter(order__id=obj.id)
        return OrderPaymentSerializer(payments,many=True).data
    
    class Meta:
        model = Order
        fields = '__all__'