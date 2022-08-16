from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from applications.account.serializer import RegisterSerializer, LoginSerializer, ChangePasswordSerializer, \
    ForgotPasswordCompleteSerializer, ForgotPasswordSerializer

User = get_user_model()


class RegisterApiView(APIView):

    def post(self, request):
        data = request.data
        serializers = RegisterSerializer(data=data)

        if serializers.is_valid(raise_exception=True):
            serializers.save()
            message = f'Вы успешно зарегистрированы. ' \
                      f'Подтверждение о регистрации было направлено Вам на почту.'

            return Response(message, status=201)


class LoginApiView(ObtainAuthToken):
    serializer_class = LoginSerializer


class ActivationView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.activation_code = ' '
            user.is_active = True
            user.save()
            return Response('Успешно', status=200)
        except User.DoesNotExist:
            return Response('Неверный код', status=400)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializers = ChangePasswordSerializer(data=request.data,
                                               context={'request': request})

        serializers.is_valid(raise_exception=True)
        serializers.set_new_password()
        return Response('Пароль успешно обновлен!')


class LogOutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            Token.objects.filter(user=user).delete()
            return Response('Вы успешно разлогинились')

        except:
            return Response(status=403)


class ForgotPasswordView(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response(f'Подтверждение направлено Вам на почту.')


class ForgotPasswordCompleteView(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_pass()
        return Response("Пароль обновлен")

