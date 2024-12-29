from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=now)
    end_time = models.DateTimeField(null=True, blank=True)

def save(self, *args, **kwargs):
    # If the activity is being marked as checked out (i.e., is_active = False)
    if not self.is_active:  # User wants to check out
        # Get the most recent active activity for this user
        last_activity = Activity.objects.filter(user=self.user, is_active=True).order_by('-timestamp').first()
        
        # If there's no active session or the last session is already checked out, raise an error
        if not last_activity:
            raise ValidationError("You cannot check out without checking in first.")
        
        if last_activity.end_time is not None:
            raise ValidationError("You cannot check out if the last session has already been ended.")

        # Set the end_time for the last active session
        last_activity.end_time = timezone.now()
        last_activity.is_active = False
        last_activity.save()  # Save the last activity as checked out

    # Save the current instance (e.g., activity being created or updated)
    super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.user.name} is {'Active!✔️⚡' if self.is_active else 'Inactive❌'}"
