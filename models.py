import uuid
from django.db import models
from django.utils import timezone


class UpdaterManager(models.Manager):

	def take(self, alias, name):
		try:
			updater = self.get(alias = alias)
		except Updater.DoesNotExist:
			updater = Updater(
				alias    = alias[:100],
				name     = name[:100],
				created  = timezone.now(),
				modified = timezone.now(),
				updated  = timezone.now())
			updater.save()
		return updater


class Updater(models.Model):
	name     = models.CharField(max_length = 100)
	alias    = models.CharField(max_length = 100, unique = True)
	login    = models.CharField(max_length = 100)
	password = models.CharField(max_length = 100)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField()
	modified = models.DateTimeField()
	updated  = models.DateTimeField()
	objects  = UpdaterManager()

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']


class CountryManager(models.Manager):

	def take(self, alias, name, full_name):
		try:
			country = self.get(alias = alias)
		except Country.DoesNotExist:
			country = Country(
				alias     = alias[:100],
				name      = name[:100],
				full_name = full_name[:100],
				created   = timezone.now(),
				modified  = timezone.now())
			country.save()
		return country


class Country(models.Model):
	name      = models.CharField(max_length = 100)
	full_name = models.CharField(max_length = 100)
	alias     = models.CharField(max_length = 100, unique = True)
	state     = models.BooleanField(default = True)
	created   = models.DateTimeField()
	modified  = models.DateTimeField()
	objects   = CountryManager()
	
	def __init__(self):

		self.RUS = Country.objects.take(
			alias     = 'RUS',
			name      = 'Россия',
			full_name = 'Российская федерация')

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']

class RegionManager(models.Manager):

	def take(self, alias, name, full_name):
		try:
			region = self.get(alias = alias)
		except Region.DoesNotExist:
			region = Region(
				alias     = alias[:100],
				name      = name[:100],
				full_name = full_name[:100],
				created   = timezone.now(),
				modified  = timezone.now())
			region.save()
		return region


class Region(models.Model):
	name      = models.CharField(max_length = 100)
	full_name = models.CharField(max_length = 100)
	alias     = models.CharField(max_length = 100, unique = True)
	country   = models.ForeignKey(Country, null = True, default = None)
	state     = models.BooleanField(default = False)
	created   = models.DateTimeField()
	modified  = models.DateTimeField()
	updated   = models.DateTimeField(null = True, default = None)
	objects   = RegionManager()
	
	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']





