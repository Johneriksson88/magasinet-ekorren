from django.db import models
from django.contrib.auth.models import User

SizeChoices = (
    ('5 m2', '5 m2'),
    ('6 m2', '6 m2'),
    ('10 m2', '10 m2'),
    ('12 m2', '12 m2'),
)

FloorChoices = (
    ('1st', '1st'),
    ('2nd', '2nd')
)

NameChoices = (
    ('Small 1st floor', 'Small 1st floor'),
    ('Medium 1st floor', 'Medium 1st floor'),
    ('Large 1st floor', 'Large 1st floor'),
    ('Small 2nd floor', 'Small 2nd floor'),
    ('Medium 2nd floor', 'Medium 2nd floor'),
    ('Large 2nd floor', 'Large 2nd floor'),
    ('X-Large 2nd floor', 'X-Large 2nd floor')

)


class StorageUnit(models.Model):
    name = models.CharField(choices=NameChoices, max_length=100)
    size = models.CharField(choices=SizeChoices, max_length=100)
    floor = models.CharField(choices=FloorChoices, max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    fullname = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=100)
    person_or_org_nr = models.CharField(max_length=100)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return str(self.pk) + " " + self.fullname


class Order(models.Model):
    order_date = models.DateField(auto_now=True)
    start_date = models.DateField()
    storage_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return 'Order ' + str(self.pk)


