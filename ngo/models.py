from django.db import models

# Create your models here.
class NGO(models.Model):

    user=models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, related_name='ngo_profile')

    name = models.CharField(max_length=255)
    description = models.TextField()

    email = models.EmailField(unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)

    logo = models.ImageField( upload_to='ngo_logos/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name