from django.db import models

# Create your models here.
class NGO(models.Model):

    user=models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, related_name='ngo_profile')

    name = models.CharField(max_length=255)
    description = models.TextField()

    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)
    city = models.CharField(max_length=100 , blank=True, null=True)

    logo = models.ImageField( upload_to='ngo_logos/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Campaign(models.Model):

    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE, related_name='campaigns')

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)

    current_volunteers = models.PositiveIntegerField(default=0)
    required_volunteers = models.PositiveIntegerField()

    logo = models.ImageField( upload_to='ngo_campaigns/', blank=True, null=True)


    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title