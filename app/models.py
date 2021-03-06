# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import validate_ipv4_address
from app.cmd import LocalCommand, RemoteCommand


class ServerConfValues(models.Model):

    class Meta:
        verbose_name = 'Server configuration Value'
        verbose_name_plural = 'Servers configuration Values'

    question_id = models.CharField(max_length=5, unique=True, verbose_name='question_id')
    variable_name = models.CharField(max_length=60, unique=True, verbose_name='variable_name')
    variable_value = models.CharField(max_length=512, verbose_name='variable_value')

    def __str__(self):
        return '{}:{}'.format(self.name, self.value)
		
class ScriptList(models.Model):

    class Meta:
        verbose_name = 'Script'
        verbose_name_plural = 'Scripts'

    path = models.CharField(max_length=512, verbose_name='Path')

    def __str__(self):
        return '{}'.format(self.path)


class FileList(models.Model):

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'

    path = models.CharField(max_length=512, verbose_name='Path')

    def __str__(self):
        return '{}'.format(self.path)


class ServiceList(models.Model):

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    name = models.CharField(max_length=256, verbose_name='Name')

    def __str__(self):
        return '{}'.format(self.name)


class ServerConf(models.Model):

    class Meta:
        verbose_name = 'Server configuration'
        verbose_name_plural = 'Servers configuration'

    #name = models.CharField(max_length=512, unique=True, verbose_name='Hostname')
    name = models.CharField(max_length=100, unique=True, verbose_name='Hostname')
    port = models.CharField(max_length=512, verbose_name='Port')
    user = models.CharField(max_length=512, verbose_name='User')
    password = models.CharField(max_length=32, blank=True, verbose_name='Password')
    service_list = models.ManyToManyField(ServiceList, verbose_name='Services', blank=True)
    file_list = models.ManyToManyField(FileList, verbose_name='Files', blank=True)
    script_list = models.ManyToManyField(ScriptList, verbose_name='Scripts', blank=True)

    def __str__(self):
        return '{}@{}:{}'.format(self.user, self.name, self.port)


class NetworkConf(models.Model):

    class Meta:
        verbose_name = 'Interface configuration'
        verbose_name_plural = 'Interfaces configuration'


    lc = LocalCommand()
    if_list = lc.get_if_list()
    interface = models.CharField(max_length=16, verbose_name='Interface', choices=if_list)
    address = models.CharField(max_length=128, verbose_name='Address', validators=[validate_ipv4_address])
    netmask = models.CharField(max_length=128, verbose_name='Netmask', validators=[validate_ipv4_address])
    network = models.CharField(max_length=128, verbose_name='Network', validators=[validate_ipv4_address])
    broadcast = models.CharField(max_length=128, verbose_name='Broadcast', validators=[validate_ipv4_address])
    gateway = models.CharField(max_length=128, verbose_name='Gateway', validators=[validate_ipv4_address])

    def __str__(self):
        return '{} {}/{}'.format(self.interface, self.address, self.netmask)

    def save(self, *args, **kwargs):
        super(NetworkConf, self).save(*args, **kwargs)
        lc = LocalCommand()
        data = '''# The loopback network interface
auto lo
iface lo inet loopback

'''
        for i in NetworkConf.objects.all():
            data += '''
# The {} network interface
auto {}
iface {} inet static
    address {}
    netmask {}
    network {}
    broadcast {}
    gateway {}

'''.format(i.interface, i.interface, i.interface,
        i.address, i.netmask, i.network, i.broadcast, i.gateway)
        lc.write(data, '/tmp/_interfaces_test')



    
class LoginDetail(models.Model):
    class Meta:
        verbose_name = 'LoginDetail'
        verbose_name_plural = 'LoginDetails'
    username = models.CharField(max_length=30)
    first_time_login = models.CharField(max_length=10, default='false')
    after_login_network = models.CharField(max_length=30)
    logon_default_server = models.CharField(max_length=10,default='true')
    
    
class ConfigType(models.Model):        
    SERVER_TYPE =(
             ("Server","Server"),
             ("Sensor","Sensor"),
             ("Standalone","Standalone"),
             ("IndexNode","IndexNode"),             
        )
    config_name = models.CharField( max_length=30, choices = SERVER_TYPE, primary_key=True)
    
    def __str__(self):
        return self.config_name
    
    class Meta:
        verbose_name = 'ConfigType'
        verbose_name_plural = 'ConfigTypes'
        

class ConfigPath(models.Model):
    class Meta:
        verbose_name = 'ConfigPath'
        verbose_name_plural = 'ConfigPaths'
    config_name = models.ForeignKey(ConfigType)
    dirpath = models.CharField(max_length=300)
    scriptname = models.CharField(max_length=60)
    status = models.CharField(max_length=15,default='stopped', blank=True)
    pid = models.CharField(max_length=15,default='0' , blank=True)
    remarks = models.CharField(max_length=100,blank=True)


class MachineDetail(models.Model):    
    ipaddress = models.CharField(max_length=30,primary_key=True)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    def __str__(self):
        return self.ipaddress
    class Meta:
        verbose_name = 'MachineDetail'
        verbose_name_plural = 'MachineDetails'

class ScriptPath(models.Model):
    class Meta:
        verbose_name = 'ScriptPath'
        verbose_name_plural = 'ScriptPaths'
    ipaddress = models.ForeignKey(MachineDetail)
    dirpath = models.CharField(max_length=300)
    scriptname = models.CharField(max_length=60)
    status = models.CharField(max_length=15,default='new', blank=True)
    pid = models.CharField(max_length=15,default='0' , blank=True)
    remarks = models.CharField(max_length=200,blank=True)        
                   
