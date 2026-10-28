from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    image = models.ImageField(upload_to='image_card')
    name = models.CharField(max_length=255)
    info = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)



class ProductRequest(models.Model):
    
    user = models.ForeignKey(
    'UserProfile',
    on_delete=models.CASCADE,
    related_name='product_requests'
)
    ism = models.CharField(max_length=255)
    malumot = models.TextField(max_length=300)
    narx = models.DecimalField(max_digits=10, decimal_places=2)
    soni = models.DecimalField(max_digits=10, decimal_places=2)
    rasm = models.ImageField(upload_to='image_card')

    ulchov = models.CharField(max_length=50, default='kg')

class ProductRequestAdmin(models.Model):
    product_request = models.OneToOneField(ProductRequest, on_delete=models.CASCADE,related_name='admin_data')

    admin_comment = models.TextField(blank=True, null=True)

    tekshirgan = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tekshirgan_admin')
    
    tekshirilganvaqt = models.DateTimeField(null=True, blank=True)

class ProductRequestSystem(models.Model):
    product_request = models.OneToOneField(ProductRequest, on_delete=models.CASCADE, related_name='system_data')
    yasalganvaqt = models.DateTimeField(auto_now_add=True)
    yangilanganvaqt = models.DateTimeField(auto_now=True)
    sotuvchi = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sotuvchi_user')
        
   status = models.CharField(
    max_length=20,
    choices=[
    ('pending', 'Tekshiruvda'),
    ('approved', 'Qabul qilindi'),
    ('rejected', 'Rad etildi'),
    ('needs_fix', 'Tuzatish kerak'),
    ],
    default='pending'
    )
    
class UserProfile(models.Model):
    USER_ROLE = [
        ("admin", "Admin"),
        ("sotuvchi", "Sotuvchi"),
        ("boshliq", "Boshliq")
    ]
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    role = models.CharField(max_length=255, choices=USER_ROLE)
    raiting = models.FloatField(default=1)
    phonenumber = models.CharField(max_length=20)

    class Meta:
        db_table = 'user_profile'

    def __str__(self) ->str:
        return self.user.get_full_name()
