from __future__ import unicode_literals

from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class CarSkin(models.Model):
    name = models.CharField(max_length=64)
    car = models.ForeignKey(Car)

    def __unicode__(self):
        return self.name


class Track(models.Model):
    name = models.CharField(max_length=64)
    subversion = models.CharField(max_length=64, null=True, blank=True)

    def __unicode__(self):
        if self.subversion:
            return self.name + ' -> ' + self.subversion
        else:
            return self.name


class TrackDynamism(models.Model):
    name = models.CharField(max_length=64)
    session_start = models.IntegerField()
    randomness = models.IntegerField()
    session_transfer = models.IntegerField()
    lap_gain = models.IntegerField()

    def __unicode__(self):
        return self.name


class Weather(models.Model):
    name = models.CharField(max_length=64)
    graphics = models.CharField(max_length=64)
    base_temperature_ambient = models.IntegerField(default=20, verbose_name='base ambient temperature')
    variation_ambient = models.IntegerField(default=2, verbose_name='ambient variation')
    base_temperature_road = models.IntegerField(default=7, verbose_name='base road temperature')
    variation_road = models.IntegerField(default=2, verbose_name='road variation')

    def __unicode__(self):
        return self.name


class ServerSetting(models.Model):
    name = models.CharField(max_length=64, help_text='A common name for your server - this forms a prefix in the Assetto Corsa server listing, followed-by the running race-preset name')
    welcome_message = models.TextField(default='Welcome!')
    udp_port = models.IntegerField(default=9600, help_text='UDP port number which the ACServer binds to')
    tcp_port = models.IntegerField(default=9600, help_text='TCP port number which the ACServer binds to')
    http_port = models.IntegerField(default=8081, help_text='HTTP port number which Lobby binds to')
    send_buffer_size = models.IntegerField(default=0)
    recv_buffer_size = models.IntegerField(default=0)
    client_send_interval = models.IntegerField(default=15)

    def __unicode__(self):
        return self.name
