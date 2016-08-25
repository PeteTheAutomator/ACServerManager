from django.db import models


class CarTag(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=64)
    brand = models.CharField(max_length=64)
    clarse = models.CharField(max_length=64, verbose_name='class')
    tags = models.ManyToManyField(CarTag)
    dirname = models.CharField(max_length=64)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class CarSkin(models.Model):
    name = models.CharField(max_length=64)
    car = models.ForeignKey(Car)

    def __unicode__(self):
        return self.name


class Track(models.Model):
    name = models.CharField(max_length=128)
    dirname = models.CharField(max_length=64)
    subversion = models.CharField(max_length=64, null=True, blank=True)
    run = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    pitboxes = models.IntegerField(default=0)
    description = models.CharField(max_length=128)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class TrackDynamism(models.Model):
    name = models.CharField(max_length=64)
    session_start = models.IntegerField()
    randomness = models.IntegerField()
    session_transfer = models.IntegerField()
    lap_gain = models.IntegerField()

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.name


class Weather(models.Model):
    name = models.CharField(max_length=64)
    graphics = models.CharField(max_length=64)
    base_temperature_ambient = models.IntegerField(default=20, verbose_name='base ambient temperature')
    variation_ambient = models.IntegerField(default=2, verbose_name='ambient variation')
    base_temperature_road = models.IntegerField(default=7, verbose_name='base road temperature')
    variation_road = models.IntegerField(default=2, verbose_name='road variation')
    realistic_road_temp = models.IntegerField(default=7, verbose_name='realistic road temperature')

    def __unicode__(self):
        return self.name


class AssetCollection(models.Model):
    docfile = models.FileField(upload_to='assetcollections/%Y/%m/%d')

    def __unicode__(self):
        return self.docfile
