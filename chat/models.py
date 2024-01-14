
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, Username, password=None, **extra_fields):
        if not Username:
            raise ValueError('The Username field must be set')
        user = self.model(Username=Username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(Username, password, **extra_fields)



class Users(AbstractBaseUser, PermissionsMixin):
    Username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'Username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def send_message(self, message_text):
        new_message = Messages(sender=self, MessageText=message_text, Timestamp=timezone.now())
        new_message.save()
        print("new message success!")

    def view_sent_messages(self): 
        message_list = []
        for message in self.sent_messages.all():
            print(message.MessageText, message.Timestamp)
            message_list.append(message.MessageText)
        return message_list

    
    def __str__(self):
        return self.Username
    

class Messages(models.Model):
    MessageID = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sent_messages')
    MessageText = models.TextField()
    Timestamp = models.DateTimeField()



