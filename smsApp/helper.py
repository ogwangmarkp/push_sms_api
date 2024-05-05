from .models import *
from django.db.models import Sum
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
import requests
import json
from decouple import config

def sendSMSData(phone_numbers, message, user,send_type):
        message  = message.encode().decode('UTF-8')
        sms_cost = 50
        ''' balance = get_account_sms_balance(user.company)
        sms_cost = user.company.sms_cost
        if balance == 0:
            return Response({"message":"Insufficient balance"}, status=status.HTTP_200_OK)

        if (len(phone_numbers) * sms_cost) > balance:
            return Response({"message":"Insufficient balance to send all messages"}, status=status.HTTP_200_OK) '''
        
        sending_mode = 'bulk' if len(phone_numbers) > 1 else 'single'
        for phone_number in phone_numbers:
                phone_number = f'256{phone_number[-9:]}'
                smsData = {
                    'user':user,
                    'send_type':send_type,
                    'sms_cost':sms_cost,
                    'phone_number':phone_number,
                    'message':message,
                    'sending_mode':sending_mode
                }
                send_sms(smsData)

        #return Response({"message":""})


def send_sms(smsData):
        response     = "failed"
        message      = smsData['message']
        sms_cost     = smsData['sms_cost']
        phone_number = str(smsData['phone_number'])
        user         = smsData['user']
        sending_mode = smsData['sending_mode']
        contact      = User.objects.filter(phone_number = phone_number).first()
        print("contact1",contact)
        if contact is None:
            contact = User.objects.create(first_name=phone_number,user_branch=user.user_branch,gender='O',phone_number=phone_number, user_type='Contact',user_added_by=contact)
        print("contact",contact)
        # send sms
        sms_tran = UserSms.objects.create(sms_cost=sms_cost, message=message, provider=config('ACTIVE_SMS_PROVIDER'),sending_mode=sending_mode, telephone= phone_number, status='pending', company=user.user_branch.company, sent_by=user,recieved_by=contact)

        ''' if config('ACTIVE_SMS_PROVIDER') == 'EGO':
            data = {'method':'SendSms',
                    'userdata':{
                        'username':config('EGO_USER_NAME'),
                        'password' :config('EGO_PASSWORD')
                    },
                    'msgdata': [ {'number':new_number, 'message': message, 'senderid':'Egosms' } ]}
            send_sms = requests.post(config('EGO_SMS_URL'), json = data)

            if send_sms.status_code == 200 or send_sms.status_code == '200':
                send_resp = json.loads(send_sms.text)
                if send_resp['Status'] == 'OK':
                    sms_tran.status = 'sent'
                    sms_tran.save()
                    response = "sent"
                else:
                    sms_tran.status = 'failed'
                    sms_tran.save()
            else:
                sms_tran.status = 'failed'
                sms_tran.save()
        return response '''
        
        #return Response({"message":"success"}, status=status.HTTP_200_OK)    

def get_account_sms_balance(company):
    purchases = SmsRequest.objects.filter(status='success', company=company).aggregate(total_amount = Sum('amount') )
    sms_transactions = UserSms.objects.filter(company=company, status='sent').aggregate(total_sms_cost = Sum('sms_cost') )
    total_payments = purchases['total_amount'] if purchases['total_amount'] else 0
    total_sms_transactions = sms_transactions['total_sms_cost'] if sms_transactions['total_sms_cost'] else 0
    balance = total_payments - total_sms_transactions

    return balance if balance > 0 else 0