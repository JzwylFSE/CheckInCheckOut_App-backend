from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import User, Activity
from .serializers import UserSerializer, ActivitySerializer

# Views
def home(request):
    return render(request, 'index.html')

def database_view(request):
    users = User.objects.all()
    activities = Activity.objects.select_related('user')
    # print(users)
    # print(activities)
    context = {
        'users': users,
        'activities': activities,
    }
    return render(request, 'database.html', context)

class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, user_id=None):
        
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(
                    {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )
        
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id=None):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class ActivityView(APIView):
    def post(self, request):
        user_id = request.data.get('user')
        activity = Activity.objects.filter(user=user_id).first()
        if activity and activity.is_active:
            return Response({"error": "User already checked in!"}, status=status.HTTP_400_BAD_REQUEST)

        request.data['is_active'] = True
        request.data['timestamp'] = timezone.now()
        
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            new_activity = serializer.save()
            return Response(ActivitySerializer(new_activity).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, user_id=None):
        if user_id:
            activity = Activity.objects.filter(user_id=user_id, is_active=True).first()
            if activity:
                return Response(ActivitySerializer(activity).data, status=status.HTTP_200_OK)
            return Response({"message": "User is not checked in."}, status=status.HTTP_404_NOT_FOUND)

        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id=None):
        try:
            activity = Activity.objects.get(user_id=user_id, is_active=True)
        except Activity.DoesNotExist:
            return Response({"error": "Activity not found or user has already checked out."}, status=status.HTTP_404_NOT_FOUND)

        # Set end_time and mark activity as inactive
        activity.end_time = timezone.now()
        activity.is_active = False
        activity.save()

        # Return the updated activity status
        return Response(ActivitySerializer(activity).data, status=status.HTTP_200_OK)



class ApiRootView(APIView):
    def get(self, request):
        return render(request, 'api_root.html', {})
