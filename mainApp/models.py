from django.db import models


class UserDetail(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=10)
    phone = models.CharField(max_length=15,default=None, null=True, blank=True)
    email = models.EmailField(max_length=30,default=None, null=True, blank=True)
    pincode = models.CharField(max_length=8,default=None, null=True, blank=True)
    city = models.CharField(max_length=20,default=None, null=True, blank=True)
    state = models.CharField(max_length=20,default=None, null=True, blank=True)
    address = models.TextField(max_length=200,default=None, null=True, blank=True)
    pic = models.FileField(upload_to="image",default=None, null=True, blank=True)

    def __str__(self):
        return self.username

class NewsLatter(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=30,unique=True)

contacatStatusChoice = ((1,"Active"),(2,"Done"))
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=20)
    subject = models.TextField(max_length=50)
    message = models.TextField(max_length=50)
    status = models.IntegerField(choices=contacatStatusChoice,default=1)

class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    pic = models.FileField(upload_to="image",default=None, null=True, blank=True)

    def __str__(self):
        return self.name

fundStatusChoice = ((1,"Pending"),(2,"Done"))
class Fund(models.Model):
    id = models.AutoField(primary_key=True)
    fund_title = models.CharField(max_length=500)
    fund_description = models.TextField()
    status = models.IntegerField(choices=fundStatusChoice,default=1)
    date = models.DateField(auto_now=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    username = models.ForeignKey(UserDetail,on_delete=models.CASCADE)
    pic = models.FileField(upload_to="meadia/image",default=None, null=True, blank=True)
