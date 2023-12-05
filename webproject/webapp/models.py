from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class WebAppModel(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="images/")
    description = models.TextField(max_length=200)  
    
    def __str__(self):
        return f"Username: {self.username} Description: {self.description}, Image: {self.image}"

class UserProfile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500 ,blank=True)
    profile_picture = models.ImageField(upload_to="profilepics/", blank=True, null=True)
    hobies = models.TextField(max_length=500, null=True)

    def __str__(self):
        return f"Username: {self.username} Bio: {self.bio}, ProfilePic: {self.profile_picture}, Hobies: {self.hobies}"
    # def __str__(self):
    #     return self.user.username

class UserComments(models.Model):
    comment = models.TextField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    web_app_model = models.ForeignKey(WebAppModel, on_delete=models.CASCADE)
    
    def __str__(self) :
        return f"comment{self.comment}, user: {self.user}, web_app_model: {self.web_app_model}"
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(WebAppModel, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.post}"  
     
    @classmethod
    def like_count(cls, post):
        return cls.objects.filter(post=post).count()