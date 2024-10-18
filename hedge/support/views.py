from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
import jwt
import json
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import Support_query, Support_query_message
from authmodule.models import *
from django.core.serializers.json import DjangoJSONEncoder
from support.serializers import Support_querySerializer, Support_query_messageSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO 8601 format
        return super().default(obj)

class SupportView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view
    def post(self, request, *args, **kwargs):
        user = request.user
        print(request.data)
        if user.is_authenticated and user.is_active:
            try:
                title = request.data.get('query')
                name = request.data.get('name')
                Issue_type = request.data.get('Issue_type')
                mobile = request.data.get('mobile')
                call_time = request.data.get('call_time')
                description = request.data.get('description')
                image = request.FILES.get('file')
                p = Profile.objects.filter(user = user).first()
                support_instance = Support_query(
                    user=user,
                    title = title,
                    Issue_type=Issue_type,
                    mobile=p.mobile_no,
                    call_time=call_time,
                    name=f"{user.first_name} {user.last_name}",
                    description=description,
                    image=image
                )
                support_instance.save()

                return JsonResponse({'message': 'Data and image saved successfully.'}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'Invalid request.'}, status=201)
        return JsonResponse({"success": False, "error": "Unauthorized"}, status=401)

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            data = Support_query.objects.all().order_by('-date_time')
        else:
            data = Support_query.objects.filter(Q(user=user) & ~Q(status="Deleted")).order_by('-date_time')
        support_serializer = Support_querySerializer(data, many=True)
        serialized_support = support_serializer.data
        print(serialized_support)
        data = {
            'support': serialized_support,
        }
        return JsonResponse(data, status=200)



class SupportDataDetailsView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def get(self, request, support_id, *args, **kwargs):
        user = request.user
        
        if user.is_authenticated and user.is_active:
            if user.is_superuser and user.is_staff:
                data = Support_query.objects.filter(Q(support_id=support_id) & ~Q(status="Deleted")).order_by('-date_time')
            else:
                data = Support_query.objects.filter(Q(user=user) & Q(support_id=support_id) & ~Q(status="Deleted")).order_by('-date_time')
            support_serializer = Support_querySerializer(data, many=True)
            return JsonResponse({'support': support_serializer.data}, status=200)

        return JsonResponse({"success": False, "error": "Unauthorized"}, status=401)



class SupportDataDeleteView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def delete(self, request, support_id, *args, **kwargs):
        user = request.user

        if user.is_authenticated and user.is_active:
            try:
                if user.is_superuser and user.is_staff:
                    data = Support_query.objects.filter(support_id=support_id).first()
                else:
                    data = Support_query.objects.filter(user=user, support_id=support_id).first()

                data.status = "Deleted"
                data.save()

                return JsonResponse({'success': True, 'message': 'Query deleted successfully.'}, status=200)
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)}, status=201)
        return JsonResponse({"success": False, "error": "Unauthorized"}, status=401)



class SupportDataChangeStatusView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_active:
            try:
                if user.is_superuser and user.is_staff:
                    data_json = json.loads(request.body.decode('utf-8'))
                    support_id = data_json['SupportId']
                    new_status = data_json['status']
                    support = Support_query.objects.filter(support_id=support_id).first()
                    support.status = new_status
                    support.save()

                return JsonResponse({'success': True, 'message': 'Status updated successfully.'}, status=200)
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)}, status=201)
        return JsonResponse({"success": False, "error": "Unauthorized"}, status=401)



class SaveSupportMessageView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def post(self, request, support_id, *args, **kwargs):
        user = request.user

        if user.is_authenticated and user.is_active:
            message = request.POST.get('message')
            support = Support_query.objects.filter(support_id=support_id).first()
            support_instance = Support_query_message(user=user, support=support, message=message)
            support_instance.save()

            return JsonResponse({'message': 'Message saved successfully.'}, status=200)



class SupportDataMessageView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def get(self, request, support_id, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_active:
            support = Support_query.objects.filter(support_id=support_id).first()
            if user.is_superuser and user.is_staff:
                data = Support_query_message.objects.filter(support=support)
            else:
                data = Support_query_message.objects.filter(user=user, support=support)
            support_serializer = Support_query_messageSerializer(data, many=True)

            return JsonResponse({'support': support_serializer.data}, status=200)




@csrf_exempt
def support_data_details(request, support_id):
    authorization_header = request.META.get('HTTP_AUTHORIZATION')

    # Decode the token and get the user ID
    print(authorization_header)

    if authorization_header is None:
        return JsonResponse({"success": False, "error": "login"}, status = 201)
    try:
        token = authorization_header.split(" ")[1]
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        print(decoded_token)
        user_id = decoded_token["user_id"]
        print(user_id)
        user = User.objects.filter(id = user_id).first()
        if user is None:
            return JsonResponse({"success": False, "error": "login"}, status = 201)
        
    except jwt.InvalidTokenError:
        print("Invalid token")
        print(authorization_header)
    try:
        if request.method == 'OPTIONS':
            response = JsonResponse({'message': 'Preflight request received.'}, status=200)
            response["Access-Control-Allow-Origin"] = "https://portal.ltnorthern.com"
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            return response

        elif request.method == 'GET':
            if user.is_authenticated and user.is_active:
                if user.is_superuser and user.is_staff:
                    data = Support_query.objects.filter(Q(support_id = support_id) & ~Q(status="Deleted")).order_by('-date_time')
                else:
                    data = Support_query.objects.filter(Q(user=user) & Q(support_id = support_id) & ~Q(status="Deleted")).order_by('-date_time')
                support_serializer = Support_querySerializer(data, many=True)
                serialized_support = support_serializer.data
                print(serialized_support)
                data = {
                    'support': serialized_support,
                }
                return JsonResponse(data, status=200)
                
            return JsonResponse({"success": False, "error": "login"}, status=401)
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Invalid request.'}, status=500)



@csrf_exempt
def support_data_delete(request, support_id):
    authorization_header = request.META.get('HTTP_AUTHORIZATION')

    # Decode the token and get the user ID
    print(authorization_header)

    if authorization_header is None:
        return JsonResponse({"success": False, "error": "login"}, status = 201)
    try:
        token = authorization_header.split(" ")[1]
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        print(decoded_token)
        user_id = decoded_token["user_id"]
        print(user_id)
        user = User.objects.filter(id = user_id).first()
        if user is None:
            return JsonResponse({"success": False, "error": "login"}, status = 201)
        
    except jwt.InvalidTokenError:
        print("Invalid token")
        print(authorization_header)
    try:
        if request.method == "DELETE" and user.is_authenticated and user.is_active: 
            print(user)
            try:
                if user.is_superuser and user.is_staff:
                    data = Support_query.objects.filter(support_id = support_id).first()
                else:
                    data = Support_query.objects.filter(user=user, support_id = support_id).first()
                print(data)
                data.status = "Deleted"
                data.save()
                
                return JsonResponse({'success': True, 'message': 'Query deleted successfully.'}, status = 200)
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)}, status = 201)
        else:
            return JsonResponse({"success": False, "error": "Invalid request method"}, status = 201)
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Invalid request.'}, status=500)

@csrf_exempt
def support_data_change_status(request):
    authorization_header = request.META.get('HTTP_AUTHORIZATION')

    # Decode the token and get the user ID
    print(authorization_header)

    if authorization_header is None:
        return JsonResponse({"success": False, "error": "login"}, status = 201)
    try:
        token = authorization_header.split(" ")[1]
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        print(decoded_token)
        user_id = decoded_token["user_id"]
        print(user_id)
        user = User.objects.filter(id = user_id).first()
        if user is None:
            return JsonResponse({"success": False, "error": "login"}, status = 201)
        
    except jwt.InvalidTokenError:
        print("Invalid token")
        print(authorization_header)
    try:
        if request.method == "POST" and user.is_authenticated and user.is_active: 
            print(user)
            try:
                if user.is_superuser and user.is_staff:
                    data = request.body.decode('utf-8')  # Decode bytes to string
                    data_json = json.loads(data)  # Parse string as JSON
                    support_id = data_json['SupportId']
                    new_status = data_json['status']
                    data = Support_query.objects.filter(support_id = support_id).first()
                    print(data)
                    data.status = new_status
                    data.save()
                
                return JsonResponse({'success': True, 'message': 'Query deleted successfully.'}, status = 200)
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)}, status = 201)
        else:
            return JsonResponse({"success": False, "error": "Invalid request method"}, status = 201)
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Invalid request.'}, status=500)

@csrf_exempt
def save_support_message(request, support_id): 
    authorization_header = request.META.get('HTTP_AUTHORIZATION')

    # Decode the token and get the user ID
    print(authorization_header)

    if authorization_header is None:
        return JsonResponse({"success": False, "error": "login"}, status = 201)
    try:
        token = authorization_header.split(" ")[1]
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        print(decoded_token)
        user_id = decoded_token["user_id"]
        print(user_id)
        user = User.objects.filter(id = user_id).first()
        if user is None:
            return JsonResponse({"success": False, "error": "login"}, status = 201)
        
    except jwt.InvalidTokenError:
        print("Invalid token")
        print(authorization_header)

    try:
        if request.method == 'OPTIONS':
            response = JsonResponse({'message': 'Preflight request received.'}, status=200)
            response["Access-Control-Allow-Origin"] = "https://portal.ltnorthern.com"
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, DELETE"
            response["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            return response
            
        elif request.method == 'POST' and user.is_authenticated and user.is_active:
            message = request.POST.get('message')
            s = Support_query.objects.filter(support_id = support_id).first()
            support_instance = Support_query_message(user = user, support = s, message = message)
            support_instance.save()

            response =  JsonResponse({'message': 'Data saved successfully.'}, status=200)
            return response
    except Exception as e:
        print(e)
        response = JsonResponse({'error': 'Invalid request.'}, status=201)
        return response

@csrf_exempt
def support_data_message(request, support_id):
    authorization_header = request.META.get('HTTP_AUTHORIZATION')

    # Decode the token and get the user ID
    print(authorization_header)

    if authorization_header is None:
        return JsonResponse({"success": False, "error": "login"}, status = 201)
    try:
        token = authorization_header.split(" ")[1]
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        print(decoded_token)
        user_id = decoded_token["user_id"]
        print(user_id)
        user = User.objects.filter(id = user_id).first()
        if user is None:
            return JsonResponse({"success": False, "error": "login"}, status = 201)
        
    except jwt.InvalidTokenError:
        print("Invalid token")
        print(authorization_header)
    try:
        print(user)
        if request.method == 'OPTIONS':
            response = JsonResponse({'message': 'Preflight request received.'}, status=200)
            response["Access-Control-Allow-Origin"] = "https://portal.ltnorthern.com"
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            return response

        elif request.method == 'GET':
            if user.is_authenticated and user.is_active:
                s = Support_query.objects.filter(support_id = support_id).first()
                if user.is_superuser and user.is_staff:
                    data = Support_query_message.objects.filter(support=s)
                else:
                    data = Support_query_message.objects.filter(user=user, support=s)
                support_serializer = Support_query_messageSerializer(data, many=True)
                serialized_support = support_serializer.data
                print(serialized_support)
                data = {
                    'support': serialized_support,
                }
                return JsonResponse(data, status=200)
                
            return JsonResponse({"success": False, "error": "login"}, status=401)
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Invalid request.'}, status=500)
