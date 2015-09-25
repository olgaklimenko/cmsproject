import datetime
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import admin
from markdown import markdown

VIEWABLE_STATUS =[3,4]

class ViewableManager(models.Manager):
    def get_query_set(self):
        default_queryset = super(ViewableManager, self).get_query_set()
        return default_queryset.filter(status__in=VIEWABLE_STATUS)

class Category(models.Model):
    label = models.CharField(blank=True, max_length=50)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "categories"  
    
    def __unicode__(self):
        return self.label

class Story(models.Model):
    STATUS_CHOICES = (
        (1, "Needs Edit"),
        (2, "Needs Approval"),
        (3, "Published"),
        (4, "Archived"),
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    category = models.ForeignKey(Category)
    markdown_content = models.TextField()
    html_content = models.TextField(editable=False)
    owner = models.ForeignKey(User)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(default = datetime.datetime.now)

    class Meta:
        ordering = ['modified']
        verbose_name_plural = "stories"
    
    admin_objects = models.Manager()
    objects = ViewableManager()  
    
    def save(self):
        self.html_content = markdown(self.markdown_content)
        self.modified = datetime.datetime.now()  
        super(Story, self).save()

    def get_absolute_url(self):
        return reverse('cms-story', kwargs={'slug':self.slug})

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('label',)}

class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'created', 'modified')
    search_fields = ('title', 'content')
    list_filter = ('status', 'owner', 'created', 'modified')
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Category, CategoryAdmin)  
admin.site.register(Story, StoryAdmin)

