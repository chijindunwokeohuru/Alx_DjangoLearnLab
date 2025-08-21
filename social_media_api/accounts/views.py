from .models import CustomUser
class FollowUserView(generics.GenericAPIView):
	queryset = CustomUser.objects.all()
	permission_classes = [IsAuthenticated]

	def post(self, request, user_id):
		user_to_follow = self.get_object()
		if user_to_follow == request.user:
			return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
		request.user.following.add(user_to_follow)
		user_to_follow.followers.add(request.user)
		return Response({'detail': f'You are now following {user_to_follow.username}.'}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
	queryset = CustomUser.objects.all()
	permission_classes = [IsAuthenticated]

	def post(self, request, user_id):
		user_to_unfollow = self.get_object()
		if user_to_unfollow == request.user:
			return Response({'detail': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
		request.user.following.remove(user_to_unfollow)
		user_to_unfollow.followers.remove(request.user)
		return Response({'detail': f'You have unfollowed {user_to_unfollow.username}.'}, status=status.HTTP_200_OK)

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import permissions
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
	serializer_class = UserRegistrationSerializer
	permission_classes = [permissions.IsAuthenticated]
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
	permission_classes = [permissions.IsAuthenticated]
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

	permission_classes = [permissions.IsAuthenticated]
	serializer_class = UserProfileSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return self.request.user
