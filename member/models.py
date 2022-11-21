from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Member(models.Model):
    GENDER = (
        ('Kiume', 'Kiume'),
        ('Kike', 'Kike')
    )
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    tarehe_kuzaliwa = models.DateField()
    simu = models.CharField(max_length=200)
    mahali_kuzaliwa = models.CharField(max_length=200)
    jinsia = models.CharField(max_length=200, choices=GENDER)
    kumpokea_yesu = models.DateField()
    mahali_anakotoka = models.CharField(max_length=200, help_text='mahali alikompokea yesu')
    dhehebu = models.CharField(max_length=200)
    dhehebu_alilookolea = models.CharField(max_length=200)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True, blank=True)
    tarehe_ubaatizo = models.DateField()
    mahali_ubatizo = models.CharField(max_length=200)
    maji_mengi = models.BooleanField(default=False)
    trh_kujazwa_roho_mtakatifu  = models.DateField()
    mahali_roho_mtakatifu = models.CharField(max_length=200, default='Geita')
    huduma_aliyonayo = models.CharField(max_length=200)
    anatoa_zaka = models.BooleanField(default=False)
    ameajiriwa = models.BooleanField(default=False)
    ameoa_ameolewa = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    @property
    def get_full_name(self):
        # The user is identified by their email address
        return self.name
    
    def __str__(self):
        return self.name

    def get_total_paid_fee(self):
        return sum(member.payment for member in self.member_fee.all())

    def get_absolute_url(self):
        return reverse("member_detail", kwargs={"pk": self.pk})

class FeeType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return self.name

    


class Payment(models.Model):
    member = models.ForeignKey(Member, related_name='member_fee', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment = models.DecimalField(decimal_places=2, max_digits=12)
    feetype =  models.ForeignKey(FeeType, on_delete=models.SET_NULL, null=True)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.member.name)

class Day(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Timetable(models.Model):
    day = models.ForeignKey(Day, on_delete=models.SET_NULL, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Department(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Sub_Department(models.Model):
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class DepartmentMeeting(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    sub_department = models.ForeignKey(Sub_Department, on_delete=models.SET_NULL, null=True)
    day = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


