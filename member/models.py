from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Member(models.Model):
    GENDER = (
        ('Kiume', 'Kiume'),
        ('Kike', 'Kike')
    )

    AJIRA = (
        ('Ameajiriwa', 'Ameajiriwa'),
        ('Amejiajiri', 'Amejiajiri'),
        ('Hana Kazi', 'Hana Kazi'),
    )

    MAHUSIANO = (
        ('Ameoa', 'Ameoa'),
        ('Ameolewa', 'Ameolewa'),
        ('Hajaolewa', 'Hajaolewa'),
        ('Hajaoa', 'Hajaoa')
    )

    UBAATIZO = (
        ('Maji Mengi', 'Maji Mengi'),
        ('Maji Kidogo', 'Maji Kidogo')
    )

    
    ZAKA = (
        ('Anatoa Zaka', 'Anatoa Zaka'),
        ('Hatoi Zaka', 'Hatoi Zaka')
    )

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True)
    tarehe_kuzaliwa = models.DateField()
    simu = models.CharField(max_length=200, null=True)
    mahali_kuzaliwa = models.CharField(max_length=200, null=True)
    jinsia = models.CharField(max_length=200, choices=GENDER, null=True)
    kumpokea_yesu = models.DateField()
    mahali_anakotoka = models.CharField(max_length=200, help_text='mahali alikompokea yesu', null=True)
    dhehebu = models.CharField(max_length=200)
    dhehebu_alikookokea = models.CharField(max_length=200)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True, blank=True)
    tarehe_ubaatizo = models.DateField()
    mahali_ubatizo = models.CharField(max_length=200, null=True)
    maji_mengi = models.CharField(max_length=200, choices=UBAATIZO, null=True)
    trh_kujazwa_roho_mtakatifu  = models.DateField()
    mahali_roho_mtakatifu = models.CharField(max_length=200, default='Geita')
    huduma_aliyonayo = models.CharField(max_length=200, null=True)
    namba_ya_zaka = models.CharField(max_length=200, blank=True, null=True)
    anatoa_zaka = models.CharField(max_length=200, choices=ZAKA, null=True)
    ameajiriwa = models.CharField(max_length=200, choices=AJIRA, null=True)
    ameoa_ameolewa = models.CharField(max_length=200, choices=MAHUSIANO, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    @property
    def get_full_name(self):
        # The user is identified by their email address
        return self.name
    
    def __str__(self):
        return self.name

    

    def get_absolute_url(self):
        return reverse("member_detail", kwargs={"pk": self.pk})

class Offering(models.Model):
    member = models.ForeignKey(Member, related_name='offerings', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.DecimalField(decimal_places=2, max_digits=12,null=True)
    paid_all = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def offering_amount(self):
        return self.amount
    
    def total_paid(self):
        return sum(payment.payment for payment in self.payments.all())
    
    def remaining_amount(self):
        total_fee = self.offering_amount()
        total_paid = self.total_paid()

        return total_fee - total_paid

    


class Payment(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE, null=True, related_name='payments')
    created_at = models.DateTimeField(auto_now_add=True)
    payment = models.DecimalField(decimal_places=2, max_digits=12)
    
    
    
    def __str__(self):
        return f"Payment of {self.payment} for {self.offering.name} by {self.offering.member.name}"
    

    # @property
    # def remaining_amount(self):
    #     # Calculate remaining amount for the member based on the offering fee and total payment amount
    #     return self.offering.amount - self.payment

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


class Zaka(models.Model):
    member = models.ForeignKey(Member, related_name='zakas', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment = models.DecimalField(decimal_places=2, max_digits=12)
    
    
    def __str__(self):
        return f"Payment of {self.payment} by {self.member.name}"