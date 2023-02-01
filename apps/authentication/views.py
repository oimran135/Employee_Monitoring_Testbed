from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from .models import User
from .serializers import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    PasswordSerializer,
)
from .utils import logout_user


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(APIView):

    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserView(APIView):

    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        user_id = request.user.id
        queryset = User.objects.get(pk=user_id)
        serializer = UserSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=UserSerializer)
    def patch(self, request):
        user_id = request.user.id
        queryset = User.objects.get(pk=user_id)
        serializer = UserSerializer(
            instance=queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = self.request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogoutView(APIView):

    def post(self, request):
        logout_user(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordView(APIView):

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(request_body=PasswordSerializer,)
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = PasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            password = serializer.data.get("password")
            if not self.object.check_password(password):
                return Response({"password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"message": "Password Updated Successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUsersView(APIView):

    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def delete(self, request, pk):
    #     queryset = User.objects.get(pk=pk)


