from django.db import models
from django.utils.html import mark_safe

class Group(models.Model):
    category = models.CharField(max_length=50)
    
    def __str__(self):
        return self.category

class Player(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    team = models.CharField(max_length=50, null=True, blank=True)
    
    final_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='players/', null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="150" />')
        return ""
    image_tag.short_description = 'Image Preview'
    
    def __str__(self):
        return self.name
class Team(models.Model):
    name = models.CharField(max_length=100)
    remaining_funds = models.IntegerField(default=15000000)