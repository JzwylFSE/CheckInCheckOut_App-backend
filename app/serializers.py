from rest_framework import serializers
from .models import User, Activity

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'created_at']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user', 'is_active', 'timestamp', 'end_time']
    def validate(self, data):
        """
        Custom validation to ensure the user cannot check out without checking in first.
        """
        user = data.get('user')
        is_active = data.get('is_active')

        if not is_active:
            last_activity = Activity.objects.filter(user=user, is_active=True).order_by('-timestamp').first()
            if not last_activity or last_activity.end_time is not None:
                raise serializers.ValidationError("You cannot check out without checking in first.")
        
        return data
