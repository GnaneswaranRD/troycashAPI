from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, get_user_model, login, logout
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import re
from troycashAPI import error_messages
from datetime import timedelta


# Create your views here.
class RegisterNewUser(APIView):
    """
    Class based view to register a new user.

    method: POST
    params: {
        "username": <username>,
        "password": <password>,
        "email": <email>,
        "name": <name>,
    }

    status_code: 200
    response:
        {"success": "User created"}

    Developer: Pall Pandiyan.S
    """

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["username", "password", "email", "name"],
        )
    )
    def post(self, request: Request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")

        # Strip out everything after '+' in email if it exists
        email = re.sub(r"\+.*?(?=@)", "", email)

        # Then use a basic email validation regex
        if not bool(
            re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        ):
            return Response(
                {
                    "email": email,
                    "error": error_messages.invalid_email,
                    "status_code": 400,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        old_users = get_user_model().objects.filter(email=email)
        if old_users:
            return Response(
                {
                    "error": error_messages.user_exists_already,
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = get_user_model().objects.create_user(
                username=email, password=password, email=email, first_name=name
            )
            # logger.debug(f"the user {email} is created")
        except Exception as e:
            print(e)
            return Response(
                {
                    "error": error_messages.user_creation_failed,
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "status": "success",
                "status_code": 200,
                "message": "user created successfully",
                "username": email,
                "name": name,
                "email": email,
                "token": token.key,
            }
        )


class LoginView(APIView):
    """
    Login View.

    Get method will only return the username.
    method: GET
    params: None

    status_code: 200
    output: { "user": <username> }


    Post method is for logging in.
    method: POST
    params: { "username": <username>, "password": <password>, "remember_me": true|false }

    status_code: 200
    output: {
        "success": "Successfully logged in",
        "API_TOKEN": <API-key>,
        "token": <user-token>,
        "user": <username>
    }

    Developer: Pall Pandiyan.S
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request: Request):
        content = {"user": str(request.user)}
        return Response(data=content)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["username", "password"],
        )
    )
    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")
        remember_me = request.data.get("remember_me")

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response(
                {"error": error_messages.invalid_user_credentials},
                status=status.HTTP_400_BAD_REQUEST,
            )

        login(request, user)
        if remember_me:
            request.session.set_expiry(timedelta(hours=12))
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "success": "Successfully logged in",
                "status_code": 200,
                "token": token.key,
                "username": username,
                "name": user.first_name,
                "email": user.email,
            }
        )


class LogoutView(APIView):
    """
    Class Based view for Logout.

    Get method will log out the user (user needs to be logged in to logout actually!).
    method: GET
    params: None

    status_code: 200
    output: {"status": "success"}

    Developer: Pall Pandiyan.S
    """

    # authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_superuser:
            Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response({"status": "success"})
