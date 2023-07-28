from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    title_tag = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(null=True, blank=True)
    body = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="likes_post")

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse('article-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        # Set the title field based on the title_tag before saving
        self.title_tag = self.title
        super(Post, self).save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()    


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="media/profile/")
    website_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    pintrest_url = models.CharField(max_length=255, null=True, blank=True)
    location =  models.CharField(max_length=255, null=True, blank=True)
    education = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user)
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="commments" ,on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.author)


