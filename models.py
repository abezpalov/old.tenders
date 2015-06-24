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

	def update(self, code, full_name, name = None, state = True):
		try:
			country           = self.get(code = code)
			country.full_name = full_name
			country.state     = state
			country.modified  = timezone.now()
			if name:
				country.name  = name
			country.save()
		except Country.DoesNotExist:
			country           = Country()
			country.code      = code
			country.name      = name
			country.full_name = full_name
			country.state     = state
			country.created   = timezone.now()
			country.modified  = timezone.now()
			country.save()
		return country


class Country(models.Model):
	code      = models.CharField(max_length = 10, unique = True)
	name      = models.CharField(max_length = 100, null = True, default = None)
	full_name = models.CharField(max_length = 100, null = True, default = None)
	state     = models.BooleanField(default = True)
	created   = models.DateTimeField()
	modified  = models.DateTimeField()

	objects   = CountryManager()

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


class CurrencyManager(models.Manager):

	def take(self, code, digital_code, name = None, state = True):
		try:
			currency = self.get(code = code)
		except Currency.DoesNotExist:
			currency              = Currency()
			currency.code         = code
			currency.digital_code = digital_code
			currency.name         = name
			currency.state        = state
			currency.created      = timezone.now()
			currency.modified     = timezone.now()
			currency.save()
		return currency

	def update(self, code, digital_code, name = None, state = True):
		try:
			currency = self.get(code = code)
			currency.digital_code = digital_code
			currency.name         = name
			currency.state        = state
			currency.modified     = timezone.now()
			currency.save()
		except Currency.DoesNotExist:
			currency              = Currency()
			currency.code         = code
			currency.digital_code = digital_code
			currency.name         = name
			currency.state        = state
			currency.created      = timezone.now()
			currency.modified     = timezone.now()
			currency.save()
		return currency


class Currency(models.Model):
	code         = models.CharField(max_length = 10, unique = True)
	digital_code = models.CharField(max_length = 10, unique = True)
	name         = models.CharField(max_length = 100, null = True, default = None)
	state        = models.BooleanField(default = True)
	created      = models.DateTimeField()
	modified     = models.DateTimeField()

	objects      = CurrencyManager()

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['code']


class OKEISectionManager(models.Manager):

	def take(self, code, name = None, state = True):
		try:
			okei_section = self.get(code = code)
		except OKEISection.DoesNotExist:
			okei_section          = OKEISection()
			okei_section.code     = code
			okei_section.name     = name
			okei_section.state    = state
			okei_section.created  = timezone.now()
			okei_section.modified = timezone.now()
			okei_section.save()
		return okei_section

	def update(self, code, name = None, state = True):
		try:
			okei_section          = self.get(code = code)
			okei_section.name     = name
			okei_section.state    = state
			okei_section.modified = timezone.now()
			okei_section.save()
		except OKEISection.DoesNotExist:
			okei_section          = OKEISection()
			okei_section.code     = code
			okei_section.name     = name
			okei_section.state    = state
			okei_section.created  = timezone.now()
			okei_section.modified = timezone.now()
			okei_section.save()
		return okei_section


class OKEISection(models.Model):
	code     = models.CharField(max_length = 10, unique = True)
	name     = models.CharField(max_length = 100, null = True, default = None)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField()
	modified = models.DateTimeField()

	objects  = OKEISectionManager()

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['code']


class OKEIGroupManager(models.Manager):

	def take(self, code, name = None, state = True):
		try:
			okei_group = self.get(code = code)
		except OKEIGroup.DoesNotExist:
			okei_group          = OKEIGroup()
			okei_group.code     = code
			okei_group.name     = name
			okei_group.state    = state
			okei_group.created  = timezone.now()
			okei_group.modified = timezone.now()
			okei_group.save()
		return okei_group

	def update(self, code, name = None, state = True):
		try:
			okei_group          = self.get(code = code)
			okei_group.name     = name
			okei_group.state    = state
			okei_group.modified = timezone.now()
			okei_group.save()
		except OKEIGroup.DoesNotExist:
			okei_group          = OKEIGroup()
			okei_group.code     = code
			okei_group.name     = name
			okei_group.state    = state
			okei_group.created  = timezone.now()
			okei_group.modified = timezone.now()
			okei_group.save()
		return okei_group


class OKEIGroup(models.Model):
	code     = models.CharField(max_length = 10, unique = True)
	name     = models.CharField(max_length = 100, null = True, default = None)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField()
	modified = models.DateTimeField()
	objects  = OKEIGroupManager()

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['code']


class OKEIManager(models.Manager):

	def take(self, code, full_name = None, section = None, group = None, local_name = None, international_name = None, local_symbol = None, international_symbol = None, state = True):
		try:
			okei = self.get(code = code)
		except OKEI.DoesNotExist:
			okei                      = OKEI()
			okei.code                 = code
			okei.full_name            = full_name
			okei.section              = section
			okei.group                = group
			okei.local_name           = local_name
			okei.international_name   = international_name
			okei.local_symbol         = local_symbol
			okei.international_symbol = international_symbol
			okei.state                = state
			okei.created              = timezone.now()
			okei.modified             = timezone.now()
			okei.save()
		return okei

	def update(self, code, full_name = None, section = None, group = None, local_name = None, international_name = None, local_symbol = None, international_symbol = None, state = True):
		try:
			okei                      = self.get(code = code)
			okei.full_name            = full_name
			okei.section              = section
			okei.group                = group
			okei.local_name           = local_name
			okei.international_name   = international_name
			okei.local_symbol         = local_symbol
			okei.international_symbol = international_symbol
			okei.state                = state
			okei.modified             = timezone.now()
			okei.save()
		except OKEI.DoesNotExist:
			okei                      = OKEI()
			okei.code                 = code
			okei.full_name            = full_name
			okei.section              = section
			okei.group                = group
			okei.local_name           = local_name
			okei.international_name   = international_name
			okei.local_symbol         = local_symbol
			okei.international_symbol = international_symbol
			okei.state                = state
			okei.created              = timezone.now()
			okei.modified             = timezone.now()
			okei.save()
		return okei


class OKEI(models.Model):
	code                 = models.CharField(max_length = 10, unique = True)
	full_name            = models.CharField(max_length = 100, null = True, default = None)
	section              = models.ForeignKey(OKEISection, null = True, default = None)
	group                = models.ForeignKey(OKEIGroup, null = True, default = None)
	local_name           = models.CharField(max_length = 100, null = True, default = None)
	international_name   = models.CharField(max_length = 100, null = True, default = None)
	local_symbol         = models.CharField(max_length = 100, null = True, default = None)
	international_symbol = models.CharField(max_length = 100, null = True, default = None)
	state                = models.BooleanField(default = True)
	created              = models.DateTimeField()
	modified             = models.DateTimeField()

	objects              = OKEIManager()

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['code']























