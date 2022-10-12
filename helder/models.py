from django.db import models
from django.contrib.auth.models import User
# from PILL import Image



class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    tb=models.CharField(max_length=100,null=False, blank=False)


    def __str__(self):
        return self.name

class Pattern(models.Model):
    class Meta:
        verbose_name = 'Pattern'
        verbose_name_plural = 'Patterns'

    pattern = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.pattern
class Type(models.Model):
    class Meta:
        verbose_name = 'Type'
        verbose_name_plural = 'Types'

    types = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.types


class Photo(models.Model):
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
    pattern=models.ForeignKey(Pattern,on_delete=models.SET_NULL,null=True,blank=True)
    types=models.ForeignKey(Type,on_delete=models.SET_NULL,null=True,blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    tbname=models.CharField(max_length=100,null=False, blank=False)
    image = models.ImageField(null=True, blank=True)
    image1 = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    image3= models.ImageField(null=True, blank=True)
    image4= models.ImageField(null=True, blank=True)
    imgname=models.CharField(max_length=500)
    date=models.CharField(max_length=100)
    size=models.CharField(max_length=500)
    price=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    detail1=models.CharField(max_length=500)
    detail2=models.CharField(max_length=500)
    detail3=models.CharField(max_length=500)
    detail4=models.CharField(max_length=500,null=True)
    detail5=models.CharField(max_length=500)
    # def save(self,*args,**kwargs):
    #     super().save(*args,**kwargs)
    #     img=Image.open(self.image1.path)

    #     if img.height>400 or img.width >400:
    #         output_size=(400)
    #         img.thumbnail(output_size)
    #         img.save(self.image1.path)
    def __str__(self):
        return self.imgname

