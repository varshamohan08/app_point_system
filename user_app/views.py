from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.contrib.auth.models import User

from user_app.models import UserDetails

from .serializers import UserSerializer


{
    "email":"user1@test.com",
    "password":"test@123"
}
{
    "email":"user1@test.com",
    "password":"test@123",
    "first_name":"user",
    # "user_type": "admin",
    "last_name":"1"
}
class userLogin(APIView):
    def get(self, request):
        context = {
            'title': 'Login Page',
            'message': 'Please enter your credentials to log in.'
        }
        return render(request, 'login.html', context)

    def post(self, request):
        username = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            user_details = {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type': request.user.userdetails.user_type
            }
            # Optionally store the tokens in session or cookies instead of rendering
            request.session['access_token'] = access_token
            request.session['user_details'] = user_details

            response = redirect('appdetails')
            response.set_cookie('access_token', access_token)
            # response.set_cookie('user_details', user_details)
            return response

        else:
            # Authentication failed, return to login page with error message
            context = {
                'title': 'Login Page',
                'message': 'Please enter your credentials to log in.',
                'error': ['Invalid username or password.']
            }
            return render(request, 'login.html', context)

      
class userLogout(APIView):
    def get(self, request):
        logout(request)
        return Response({'details': 'Success'}, status=status.HTTP_200_OK)

class userSignUp(APIView):
    def get(self, request):
        context = {
            'title': 'Create User Page',
            'message': 'Please enter your details to sign up.'
        }
        return render(request, 'signup.html', context)
    def post(self, request):
        with transaction.atomic():
            # import pdb;pdb.set_trace()
            user_serializer = UserSerializer(data=request.data)
            
            if user_serializer.is_valid():
                user_serializer.save()
                user = authenticate(username=request.data.get('email'), password=request.data.get('password'))

                if user:
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    user_details = {
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'user_type': user.userdetails.user_type
                    }
                    # return Response({"success":True, 'details': 'Success', 'access_token': access_token, 'userdetails': user_details}, status=status.HTTP_200_OK)
                    context = {
                        'title': 'Create User Page',
                        'message': 'Please enter your details to sign up.',
                        'user_details': user_details,
                        'access_token': access_token
                    }
                    # return render(request, 'home.html', context)
                    # Optionally store the tokens in session or cookies instead of rendering
                    request.session['access_token'] = access_token
                    request.session['user_details'] = user_details

                    # Redirect to home page or another route
                    return redirect('appdetails')
                
            # return Response({"success":False, 'details': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            context = {
                'title': 'Create User Page',
                'message': 'Please enter your details to sign up.',
                'error': user_serializer.errors
            }
            return render(request, 'signup.html', context)
        

class userApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # import pdb;pdb.set_trace()
        user_instance = User.objects.get(id = request.user.id)
        serializer = UserSerializer(user_instance)
        # return Response({"success":True, 'user': serializer.data}, status=status.HTTP_200_OK)
        context = {
            'title': 'User profile Page',
            'message': 'User details',
            'user': serializer.data,
        }
        return render(request, 'user_profile.html', context)
        
    def delete(self, request):
        with transaction.atomic():
            User.objects.filter(id = request.user.id).delete()
            logout(request)
            return Response({"success":True, "details": "Successfully deleted the user and the blogs authored by the user."}, status = status.HTTP_200_OK)
        
        
    def put(self, request):
        user_instance = User.objects.get(id=request.user.id)
        
        user_serializer = UserSerializer(instance=user_instance, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({"success":True, 'details': user_serializer.data}, status=status.HTTP_200_OK)
        
        return Response({"success":False, 'details': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request):
        current_password = request.data['current_password']
        new_password = request.data['new_password']

        user = request.user
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            return Response({"success":True}, status=status.HTTP_200_OK)
        else:
            return Response({"success":False, 'details': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        
