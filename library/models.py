from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Library(models.Model):
    lib_name = models.CharField(max_length=30,verbose_name="library")
    lib_city = models.CharField(max_length=30,verbose_name="City")
    lib_password = models.CharField(max_length=300,verbose_name="Password")
    lib_logged_in = models.BooleanField(default=False)
    def __str__(self):
        return self.lib_name
    class Meta:
        ordering = ["lib_name","lib_city"]
    
class Books(models.Model):
    lib_name = models.CharField(max_length=30,verbose_name="Library Name")
    lib_city = models.CharField(null=True,max_length=30,verbose_name="Library City")
    book_name = models.CharField(max_length=30,verbose_name="Book Name")
    book_author = models.CharField(null=True,max_length=30,verbose_name="Book Author")
    avaible = models.BooleanField(default=True,verbose_name="Avaibility")
    buyer_name = models.CharField(blank=True,null=True,max_length=30,verbose_name="Buyer Name")
    buyer_phone = models.CharField(blank=True,null=True,max_length=15,verbose_name="Buyer's Phone")
    buyer_email = models.EmailField(blank=True,null=True)
    buying_date = models.DateTimeField(blank=True,null=True,verbose_name="Buying Date")
    receive_date = models.DateTimeField(blank=True,null=True,verbose_name="Receiving Date")
        