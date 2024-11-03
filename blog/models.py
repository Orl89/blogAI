from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

# Create your models here.

class BlogHead(models.Model):
    head_title = models.CharField(max_length=250)
    head_descr = models.CharField(max_length=500)
    head_img   = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.head_title
    
    

# Definition du manager personnalisé
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts", null=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    # images additionnels
    image1 = models.ImageField(null=True, blank=True, upload_to="images/")
    image2 = models.ImageField(null=True, blank=True, upload_to="images/")
    slug  = models.CharField(max_length=250, unique_for_date='publish')
    # body  = models.TextField()
    body   = RichTextField(blank=True, null=True)
    body2   = RichTextField(blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status  = models.CharField(max_length=3, choices=Status.choices, default=Status.DRAFT)
 

    tags    = TaggableManager()

    # default and custom manager
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
    
    def __str__(self):
        return self.title
    
    # Url canonique
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.day, 
                                                 self.publish.month,
                                                 self.publish.year,
                                                 self.slug])



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    nom = models.CharField(max_length=80)
    email = models.EmailField()
    commentaire = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes  = [models.Index(fields=["created"])]

    def __str__(self):
        return f"Commentaire par {self.nom} on {self.post}"


class SendMail(models.Model):
    name=models.CharField(max_length=30, blank=False, null=False)
    email=models.EmailField(blank=False, null=False)
    to   = models.EmailField(blank=False, null=False)
    comments = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self) -> str:
        return self.name