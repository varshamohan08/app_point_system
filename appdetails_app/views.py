from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from tasks_app.models import TaskDetails
from .models import App, AppCategory #, AppSubCategory
from .serializers import AppSerializer, AppCategorySerializer #, AppSubCategorySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class AppCategoriesAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            app_category = get_object_or_404(AppCategory, pk=pk)
            serializer = AppCategorySerializer(app_category)
            return Response({"success":True, 'details': serializer.data}, status=status.HTTP_200_OK)
        else:
            app_categories = AppCategory.objects.filter(created_by = request.user)
            serializer = AppCategorySerializer(app_categories, many=True)
            return Response({"success":True, 'details': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AppCategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            app_category = AppCategory.objects.filter(created_by = request.user)
            serializer = AppCategorySerializer(app_category, many=True)
            return Response({"success":True, 'details': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success":False, 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 

    def put(self, request):
        app_category = get_object_or_404(AppCategory, pk=request.data.get('id'))
        serializer = AppCategorySerializer(app_category, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True, 'details': serializer.data}, status=status.HTTP_200_OK)
        return Response({"success":False, 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        app_category = get_object_or_404(AppCategory, pk=request.GET.get('pk'))
        app_category.delete()
        return Response({"success":True, 'details': "Deleted Successfully"}, status=status.HTTP_200_OK)
     
class AppAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            # import pdb;pdb.set_trace()
            action = request.GET.get("action")
            if action in ["add"]:
                app_categories = AppCategory.objects.all()
                context= {
                    'title': 'Add App Page',
                    'message': 'Add new app',
                    'app_categories': app_categories,
                    'action': action
                }
                return render(request, 'add_app.html', context)
            
            elif action in ["edit"]:
                # import pdb;pdb.set_trace()
                app_id = request.GET.get("pk")
                app_instance = get_object_or_404(App, id=app_id)
                app_categories = AppCategory.objects.all()

                context = {
                    'title': 'Edit App Page',
                    'message': 'Edit app details',
                    'app': app_instance,
                    'app_categories': app_categories,
                    'action': action
                }
                return render(request, 'edit_app.html', context)
            
            elif action in ["details", "complete_task"]:
                app_id = request.GET.get("pk")
                app_instance = get_object_or_404(App, id=app_id)
                serializer = AppSerializer(app_instance)
                context = {
                    'title': 'App Details Page',
                    'message': 'App details',
                    'app': serializer.data,
                    'action': action
                }
                return render(request, 'app_details.html', context)
            
            elif action in ["not_completed"]:
                app_instances = App.objects.exclude(
                    id__in = TaskDetails.objects.filter(created_by = request.user).values_list('app_id', flat=True)
                )
                serializer = AppSerializer(app_instances, many=True)
                # return Response({"success":True, 'details': serializer.data}, status=status.HTTP_200_OK)
                context = {
                    'title': 'Taska Page',
                    'message': 'App details with task not completed.',
                    'appdetails': serializer.data,
                    'action': action
                }
                return render(request, 'home.html', context)

            else:
                app_instances = App.objects.all()
                serializer = AppSerializer(app_instances, many=True)
                # return Response({"success":True, 'details': serializer.data}, status=status.HTTP_200_OK)

                context = {
                    'title': 'Home Page',
                    'message': 'App details.',
                    'appdetails': serializer.data,
                    'email': request.user.email,
                    'user_name': request.user.first_name + ' ' + request.user.last_name,
                    'user_type': request.user.userdetails.user_type,
                    'access_token': request.COOKIES.get('access_token', None) if request.COOKIES.get('access_token') else None
                }
                return render(request, 'home.html', context)
        except:
            context = {
                'title': 'Edit App Page',
                'message': 'Edit app details',
                'error': "Something went wrong"
            }
            return render(request, 'add_app.html', context) 

    def post(self, request):
        serializer = AppSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            app_instance = App.objects.filter(created_by = request.user)
            serializer = AppSerializer(app_instance, many=True)
            # return Response({"success":True, 'details': serializer.data}, status=status.HTTP_201_CREATED)
            return redirect('appdetails')
        # return Response({"success":False, 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        context = {
            'title': 'Add App Page',
            'message': 'Add new app',
            'error': serializer.errors
        }
        return render(request, 'add_app.html', context) 


    def put(self, request):
        import pdb;pdb.set_trace()
        app_id = request.GET.get("pk")
        app_instance = get_object_or_404(App, id=app_id)
        serializer = AppSerializer(app_instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True, 'details': serializer.data}, status=status.HTTP_200_OK)
        return Response({"success":False, 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        app_instance = get_object_or_404(App, pk=request.GET.get('pk'))
        app_instance.delete()
        return Response({"success":True, 'details': "Deleted Successfully"}, status=status.HTTP_200_OK)
       