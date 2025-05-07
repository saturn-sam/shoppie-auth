
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # refresh = RefreshToken.for_user(user)
            
            # return Response({
            #     'user': UserSerializer(user).data,
            #     'token': str(refresh.access_token),
            #     'refresh': str(refresh),
            # }, status=status.HTTP_201_CREATED)


            from .token import get_tokens_for_user

            tokens = get_tokens_for_user(user)

            return Response({
                'user': UserSerializer(user).data,
                'token': tokens['access'],
                'refresh': tokens['refresh'],
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            
            if user:
                # refresh = RefreshToken.for_user(user)
                
                # return Response({
                #     'user': UserSerializer(user).data,
                #     'token': str(refresh.access_token),
                #     'refresh': str(refresh),
                # })
                
                from .token import get_tokens_for_user

                tokens = get_tokens_for_user(user)

                return Response({
                    'user': UserSerializer(user).data,
                    'token': tokens['access'],
                    'refresh': tokens['refresh'],
                })
            
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ValidateTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        return Response(UserSerializer(request.user).data)

class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response(UserSerializer(request.user).data)
