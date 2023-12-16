import uuid
from django.db import models
from django.contrib.auth import get_user_model   # model of current authenticated user
from datetime import datetime
from PIL import Image, ImageOps

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    
    Department = (
        ('Electrical and Computer Engineering','Electrical and Computer Engineering'),
        ('Mechanical Engineering','Mechanical Engineering'),
        ('Civil Engineering','Civil Engineering'),
        ('Hydrolics Engineering','Hydrolics Engineering'),
        ('COTM','COTM')
    )
    
    Gender = (
        ('Male','Male'),
        ('Female','Female'),
        ('Unspecified','Unspecified')
    )
    
    Batch = (
        ('First Year', 'First Year'),
        ('Second Year', 'Second Year'),
        ('Third Year', 'Third Year'),
        ('Fourth Year', 'Fourth Year'),
        ('Fifth Year', 'Fifth Year')
    )
    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to = 'profile_images', default = 'blank-profile-picture.png')
    fullname = models.CharField(max_length=100, blank=True, null=True)
    phonenumber = models.CharField(max_length=14, blank=True, null=True)
    idcard = models.CharField(max_length=100, blank=True, null=True)
    batch = models.CharField(max_length=100, choices=Batch, blank=True, null=True)
    gender = models.CharField(max_length=100, choices=Gender, blank=True, null=True)
    department = models.CharField(max_length=100, choices=Department, blank=True, null=True)
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profileimg:
            img = Image.open(self.profileimg.path)
            new_img = ImageOps.exif_transpose(img)
            
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                new_img.thumbnail(output_size, Image.LANCZOS)
                new_img.save(self.profileimg.path)
    
    def __str__(self):
        return self.user.username
    
    
class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    is_liked = models.BooleanField(blank=True, null=True)
    
    
    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username     
     
     
class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user     
     
     
class ChatMessage(models.Model):
    body = models.TextField()
    msg_sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_sender")
    msg_receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_receiver")
    seen = models.BooleanField(default=False)
    
    def __str__(self):
        return self.body         
    
    
class Files(models.Model):
    Department = (
        ('Electrical and Computer Engineering','Electrical and Computer Engineering'),
        ('Mechanical Engineering','Mechanical Engineering'),
        ('Civil Engineering','Civil Engineering'),
        ('Hydrolics Engineering','Hydrolics Engineering'),
        ('COTM','COTM')
    )
    
    Batch = (
        ('First Year', 'First Year'),
        ('Second Year', 'Second Year'),
        ('Third Year', 'Third Year'),
        ('Fourth Year', 'Fourth Year'),
        ('Fifth Year', 'Fifth Year')
    )
    
    
    contributer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    pdf = models.FileField(upload_to = 'pdfs')
    title = models.CharField(max_length=500)
    department = models.CharField(max_length=100, choices=Department, blank=True, null=True)
    batch = models.CharField(max_length=100, choices=Batch, blank=True, null=True)
    
    def __str__(self):
        return self.title