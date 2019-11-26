from django.db import models

# Create your models here.
#账号
class Users(models.Model):
    users_image = models.CharField(max_length=50)
    users_name = models.CharField(max_length=180)
    users_no = models.CharField(max_length=180,primary_key=True)
    users_password = models.CharField(max_length=180)
    users_major = models.CharField(max_length=180)
    users_isactive = models.CharField(max_length=5)

class Users_message(models.Model):
    balance = models.FloatField()
    disciplinary_offence = models.CharField(max_length=180)
    book_leading = models.CharField(max_length=180)