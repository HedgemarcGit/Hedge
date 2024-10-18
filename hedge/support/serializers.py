from rest_framework import serializers
from django.contrib.auth.models import User
from support.models import Support_query, Support_query_message

from authmodule.serializers import *

class Support_querySerializer(serializers.ModelSerializer):
    joined_date = serializers.DateTimeField(source='date_time', format='%Y-%m-%d')
    user = UserSerializer() 
    class Meta:
        model = Support_query
        fields = '__all__'

class Support_query_messageSerializer(serializers.ModelSerializer):
    joined_date = serializers.DateTimeField(source='date_time', format='%Y-%m-%d')
    user = UserSerializer() 
    class Meta:
        model = Support_query_message
        fields = ['message_id', 'message', 'user', 'joined_date']
