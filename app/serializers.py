from rest_framework import serializers

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import User, UserInterest

class UserRegistrationSerializer(serializers.ModelSerializer):
	"""User Registration Serilaizer"""
	
	class Meta:
		model = User
		fields = ['id','full_name','email_address','password','is_active']
		extra_kwargs = {'password': {'write_only': True}}

class UserLoginSerializer(serializers.Serializer):
	email_address = serializers.EmailField()
	password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

	def validate(self, data):
		email = data.get('email_address')
		password = data.get('password')
		if email and password:
			userObj = User.objects.filter(email_address=email)
			if userObj.exists():
				if userObj[0].is_active:
					user = authenticate(request=self.context.get('request'), username= userObj[0].email_address,
					password= password
					)
				else:
					msg = {
						'detail': 'User is inactive',
						'status': False,
					}
					raise ValidationError(msg,code='Unauthorized')
			else:
				msg = {
				    'detail': 'Email not found',
				    'status': False,
				}
				raise ValidationError(msg)
			if not user:
				msg = {
				    'detail': 'Credentials do not match',
				    'status': False,
				}
				raise ValidationError(msg, code='authorization')
		else:
			msg = {
				'detail': 'Credentials not found',
				'status': False,
			}
			raise ValidationError(msg, code='authorization')
		data['user'] = user
		return data 


class UserIntertestSerializer(serializers.ModelSerializer):
	"""User Intertest Serializer"""

	user_intertest = UserRegistrationSerializer(read_only=True)

	class Meta:
		model = UserInterest
		fields = ['id','interest','added','updated','user_intertest']