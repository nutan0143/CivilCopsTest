import pdb

from django.shortcuts import render
from django.contrib.auth import login

from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token


from .models import User, UserInterest
from .serializers import *

class UserRegistrationView(generics.CreateAPIView):
	"""User Registreation View"""
	serializer_class = UserRegistrationSerializer
	queryset = User.objects.all()

	def perform_create(self, serializer_class):
		user = serializer_class.save()
		user.set_password(self.request.data['password'])
		user.is_active = True
		user.save()

class LoginView(APIView):
	"""Login Api View"""
	def post(self, request, format=None):
		serializer = UserLoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		login(request, user)
		token, created = Token.objects.get_or_create(user=user)
		response = {
		    'email': user.email_address,
		    'is_active': user.is_active,
		    'token': str(token)
		}
		return Response({
		    "user": response,
		}, status=status.HTTP_201_CREATED)

class UserInterestView(APIView):
	"""User intertest view"""

	def post(self,request):
		try:
			params = request.data
			if 'interest' not in params or params['interest'] == "" or params['interest'] is None:
				return Response({"message":"Interest is required."},status=status.HTTP_400_BAD_REQUEST)
			obj,create = UserInterest.objects.get_or_create(user_id=request.user.id,interest=params['interest'])
			serializer = UserIntertestSerializer(obj)
			return Response({"data":serializer.data},status=status.HTTP_200_OK)
		except Exception as e:
			return Response({"message":e.__str__()},status=status.HTTP_400_BAD_REQUEST)

	def get(self,request):
		try:
			obj = UserInterest.objects.filter(user_id=request.user.id)
			serializer = UserIntertestSerializer(obj,many=True)
			return Response({"data":serializer.data},status=status.HTTP_200_OK)
		except Exception as e:
			return Response({"message":e.__str__()},status=status.HTTP_400_BAD_REQUEST)

	def patch(self,request):
		try:
			params = request.data
			if 'interest' not in params or params['interest'] == "" or params['interest'] is None:
				return Response({"message":"Interest is required."},status=status.HTTP_400_BAD_REQUEST)
			if 'id' not in params or params['id'] == "" or params['id'] is None:
				return Response({"message":"Id is required."},status=status.HTTP_400_BAD_REQUEST)
			obj = UserInterest.objects.filter(id=params['id']).first()
			if obj:
				obj.interest = params['interest']
				obj.save()
				serializer = UserIntertestSerializer(obj)
				return Response({"data":serializer.data},status=status.HTTP_200_OK)
			return Response({"message":"No intertest Found."},status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response({"message":e.__str__()},status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self,request):
		try:
			id = request.GET.get('id')
			obj = UserInterest.objects.filter(id=id).delete()
			return Response({"message":"Interest of User deleted successfully."},status=status.HTTP_200_OK)
		except Exception as e:
			return Response({"message":e.__str__()},status=status.HTTP_400_BAD_REQUEST)