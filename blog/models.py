from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

#QuerySet manager for getting published posts
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .filter(status=Post.Status.PUBLISHED)

# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED= 'PB', 'Published'

    #Post title
    title = models.CharField(max_length=250)
    #Post slug for urls,
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    #Post body
    body = models.TextField()
    #The author of the post
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    #Published Field. Represents the post publishing timestamp
    publish = models.DateTimeField(default=timezone.now)
    #Created Field. Represents the Post Creation timestamp
    created = models.DateTimeField(auto_now_add=True)
    #Updated Field. Represents the Last updation timestamp
    updated = models.DateTimeField(auto_now=True)
    #The Status Field
    status = models.CharField(max_length=2,choices=Status.choices,default=Status.DRAFT)
    
    objects = models.Manager()
    published = PublishedManager()
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

#Model for comments
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=25)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateField(auto_now=True)
    active=models.BooleanField(default=True)
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self) -> str:
        return f"Comment by {self.name} on post {self.post}"