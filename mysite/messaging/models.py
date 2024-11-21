from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
  bio = models.TextField(max_length=500, blank=True)
  location = models.CharField(max_length=100, blank=True)
  phone_number = models.CharField(max_length=15, blank=True)
  profile_picture = CloudinaryField('image', blank=True, null=True)


class Message(models.Model):
  sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
  receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
  content = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return f"{self.sender.username} to {self.receiver.username}: {self.content}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
