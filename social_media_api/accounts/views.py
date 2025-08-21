
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
	serializer_class = UserRegistrationSerializer

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		token, created = Token.objects.get_or_create(user=user)
		return Response({
			'user': UserProfileSerializer(user, context=self.get_serializer_context()).data,
			'token': token.key
		}, status=status.HTTP_201_CREATED)

class LoginView(ObtainAuthToken):
	serializer_class = UserLoginSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
		if not user:
			return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
		token, created = Token.objects.get_or_create(user=user)
		return Response({
			'user': UserProfileSerializer(user).data,
			'token': token.key
		})

class ProfileView(generics.RetrieveUpdateAPIView):
	serializer_class = UserProfileSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return self.request.user
