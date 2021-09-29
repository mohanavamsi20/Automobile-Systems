from django.db import models

from home.models import State, City, Dealer, User
from models.models import Make, Model, Variant
from django.db import models

# Create your models here.
class SellCar(models.Model):
    fullname = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False)
    mobile=models.CharField(max_length=15,blank=False)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    make = models.ForeignKey(Make, on_delete=models.SET_NULL, blank=True, null=True)
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, blank=True, null=True)
    variant = models.ForeignKey(Variant, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='shop/', blank=True)
    image1 = models.ImageField(upload_to='shop/', blank=True,null=True)
    image2 = models.ImageField(upload_to='shop/', blank=True,null=True)
    image3 = models.ImageField(upload_to='shop/', blank=True,null=True)
    image4 = models.ImageField(upload_to='shop/', blank=True,null=True)
    image5 = models.ImageField(upload_to='shop/', blank=True,null=True)
    image6 = models.ImageField(upload_to='shop/', blank=True,null=True)
    description = models.TextField()
    year = models.CharField(max_length=4, blank=False)
    mileage = models.CharField(max_length=20, blank=False)
    fuel = models.CharField(max_length=20, blank=False)
    engine_size = models.CharField(max_length=20, blank=False)
    power = models.CharField(max_length=20, blank=False)
    gear_box = models.CharField(max_length=20, blank=False)
    seats = models.CharField(max_length=20, blank=False)
    doors = models.CharField(max_length=20, blank=False)
    colors = models.CharField(max_length=100, blank=False)
    price = models.CharField(max_length=100, blank=False)
    kilometer = models.CharField(max_length=100, blank=False)
    reg_no = models.CharField(max_length=20, blank=False)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('id',)
        
    def remove_on_image_update(self):
        try:
            obj = SellCar.objects.get(id=self.id)
        except SellCar.DoesNotExist:
            return
        if obj.image and self.image and obj.image != self.image:
            obj.image.delete()

    def delete(self, *args, **kwargs):
        self.image.delete()
        return super(SellCar, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.remove_on_image_update()
        return super(SellCar, self).save(*args, **kwargs)

    def __str__(self):
        return self.fullname+' '+str(self.reg_no)+' '+str(self.make)+' '+str(self.model)+' '+str(self.variant)+' '+str(self.reg_no)

class BuyCar(models.Model):
    car = models.ForeignKey(SellCar, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True) 