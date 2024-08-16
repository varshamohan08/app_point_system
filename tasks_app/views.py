from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from appdetails_app.models import App
from appdetails_app.serializers import AppSerializer
from .models import TaskDetails
from .serializers import TaskSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum

# Create your views here.
class TaskAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        # import pdb;pdb.set_trace()
        action = request.GET.get("action")
        if action in ["points"]:
            total_points = TaskDetails.objects.filter(created_by=request.user).aggregate(Sum('app__points')).get('app__points__sum', 0) or 0
            task_instances = TaskDetails.objects.filter(created_by = request.user).order_by('-created_at')
            serializer = TaskSerializer(task_instances, many=True)
            # return Response({"success":True, 'details': serializer.data}, status=status.HTTP_200_OK)
            context = {
                'title': 'Points Page',
                'message': 'Details of the points earned by the user',
                'taskdetails': serializer.data,
                'action': action,
                'total_points': total_points
            }
            return render(request, 'points.html', context)
        
        elif pk:
            task_instance = get_object_or_404(TaskDetails, pk=pk)
            serializer = TaskSerializer(task_instance)
            return Response({"success":True, 'details': serializer.data}, status=status.HTTP_200_OK)
        
        else:
            app_instances = App.objects.exclude(
                id__in = TaskDetails.objects.filter(created_by = request.user).values_list('app_id', flat=True)
            )
            serializer = AppSerializer(app_instances, many=True)
            context = {
                'title': 'Tasks Page',
                'message': 'App details with task not completed.',
                'appdetails': serializer.data,
                'action': "not_completed"
            }
            return render(request, 'home.html', context)
            # task_instances = TaskDetails.objects.filter(created_by = request.user)
            # serializer = TaskSerializer(task_instances, many=True)
            # return Response({"success":True, 'details': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            # import pdb;pdb.set_trace()
            serializer = TaskSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                task_instance = TaskDetails.objects.filter(created_by = request.user)
                serializer = TaskSerializer(task_instance, many=True)
                # return Response({"success":True, 'details': serializer.data}, status=status.HTTP_201_CREATED)
                app_instances = App.objects.exclude(
                    id__in = TaskDetails.objects.filter(created_by = request.user).values_list('app_id', flat=True)
                )
                app_serializer = AppSerializer(app_instances, many=True)
                context = {
                    'title': 'Tasks Page',
                    'message': 'App details with task not completed.',
                    'appdetails': app_serializer.data,
                    'action': "not_completed"
                }
                return render(request, 'home.html', context)
            # return Response({"success":False, 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
            
            app_id = request.data.get('app_id')
            app_instance = get_object_or_404(App, id=app_id)
            app_serializer = AppSerializer(app_instance)
            context = {
                'title': 'App Details Page',
                'message': 'App details',
                'app': app_serializer.data,
                'action': "complete_task",
                'error': serializer.errors
            }
            return render(request, 'app_details.html', context)
        except:
            app_id = request.data.get('app_id')
            app_instance = get_object_or_404(App, id=app_id)
            app_serializer = AppSerializer(app_instance)
            context = {
                'title': 'App Details Page',
                'message': 'App details',
                'app': app_serializer.data,
                'action': "complete_task",
                'error': "An error occured while completing the task"
            }
            return render(request, 'app_details.html', context)

    def put(self, request):
        task_instance = get_object_or_404(TaskDetails, pk=request.data.get('id'))
        serializer = TaskSerializer(task_instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True, 'details': serializer.data}, status=status.HTTP_200_OK)
        return Response({"success":False, 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # import pdb;pdb.set_trace()
        task_instance = get_object_or_404(TaskDetails, pk=request.data.get('task_id'))
        task_instance.delete()
        return JsonResponse({"success":True, 'details': "Deleted Successfully"}, status=status.HTTP_200_OK)