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
				name      = name,
				full_name = full_name,
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
	name      = models.TextField(null = True, default = None)
	full_name = models.TextField(null = True, default = None)
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

	name      = models.TextField(null = True, default = None)
	full_name = models.TextField(null = True, default = None)
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
	name         = models.TextField(null = True, default = None)
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
	name     = models.TextField(null = True, default = None)
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
	name     = models.TextField(null = True, default = None)
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
	full_name            = models.TextField(null = True, default = None)
	section              = models.ForeignKey(OKEISection, null = True, default = None)
	group                = models.ForeignKey(OKEIGroup, null = True, default = None)
	local_name           = models.TextField(null = True, default = None)
	international_name   = models.TextField(null = True, default = None)
	local_symbol         = models.TextField(null = True, default = None)
	international_symbol = models.TextField(null = True, default = None)
	state                = models.BooleanField(default = True)
	created              = models.DateTimeField()
	modified             = models.DateTimeField()

	objects              = OKEIManager()

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['code']


class KOSGUManager(models.Manager):

	def take(self, code, parent_code = None, name = None, parent = None, state = True):
		try:
			kosgu = self.get(code = code)
		except KOSGU.DoesNotExist:
			kosgu             = KOSGU()
			kosgu.code        = code
			kosgu.parent_code = parent_code
			kosgu.name        = name
			if parent_code:
				kosgu.parent  = self.take(parent_code)
			else:
				kosgu.parent  = None
			kosgu.state       = state
			kosgu.created     = timezone.now()
			kosgu.modified    = timezone.now()
			kosgu.save()
		return kosgu

	def update(self, code, parent_code = None, name = None, parent = None, state = True):
		try:
			kosgu             = self.get(code = code)
			kosgu.parent_code = parent_code
			kosgu.name        = name
			if parent_code:
				kosgu.parent  = self.take(parent_code)
			else:
				kosgu.parent  = None
			kosgu.state       = state
			kosgu.modified    = timezone.now()
			kosgu.save()
		except KOSGU.DoesNotExist:
			kosgu             = KOSGU()
			kosgu.code        = code
			kosgu.parent_code = parent_code
			kosgu.name        = name
			if parent_code:
				kosgu.parent  = self.take(parent_code)
			else:
				kosgu.parent  = None
			kosgu.state       = state
			kosgu.created     = timezone.now()
			kosgu.modified    = timezone.now()
			kosgu.save()
		return kosgu


class KOSGU(models.Model):

	code        = models.CharField(max_length = 10, unique = True)
	parent_code = models.CharField(max_length = 10, null = True, default = None)
	name        = models.TextField(null = True, default = None)
	parent      = models.ForeignKey('self', null = True, default = None)
	state       = models.BooleanField(default = True)
	created     = models.DateTimeField()
	modified    = models.DateTimeField()

	objects     = KOSGUManager()

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['code']


class OKOPFManager(models.Manager):

	def take(self, code, parent_code = None, full_name = None, singular_name = None, parent = None, state = True):
		try:
			okopf = self.get(code = code)
		except OKOPF.DoesNotExist:
			okopf               = OKOPF()
			okopf.code          = code
			okopf.parent_code   = parent_code
			okopf.full_name     = full_name
			okopf.singular_name = singular_name
			if parent_code:
				okopf.parent    = self.take(parent_code)
			else:
				okopf.parent    = None
			okopf.state         = state
			okopf.created       = timezone.now()
			okopf.modified      = timezone.now()
			okopf.save()
		return okopf

	def update(self, code, parent_code = None, full_name = None, singular_name = None, parent = None, state = True):
		try:
			okopf               = self.get(code = code)
			okopf.parent_code   = parent_code
			okopf.full_name     = full_name
			okopf.singular_name = singular_name
			if parent_code:
				okopf.parent    = self.take(parent_code)
			else:
				okopf.parent    = None
			okopf.state         = state
			okopf.modified      = timezone.now()
			okopf.save()
		except OKOPF.DoesNotExist:
			okopf               = OKOPF()
			okopf.code          = code
			okopf.parent_code   = parent_code
			okopf.full_name     = full_name
			okopf.singular_name = singular_name
			if parent_code:
				okopf.parent    = self.take(parent_code)
			else:
				okopf.parent    = None
			okopf.state         = state
			okopf.created       = timezone.now()
			okopf.modified      = timezone.now()
			okopf.save()
		return okopf


class OKOPF(models.Model):

	code          = models.CharField(max_length = 10, unique = True)
	full_name     = models.TextField(null = True, default = None)
	singular_name = models.TextField(null = True, default = None)
	parent_code   = models.CharField(max_length = 10, null = True, default = None)
	parent        = models.ForeignKey('self', null = True, default = None)
	state         = models.BooleanField(default = True)
	created       = models.DateTimeField()
	modified      = models.DateTimeField()

	objects       = OKOPFManager()

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['code']


class OKPDManager(models.Manager):

	def take(self, code, parent_code = None, alias = None, name = None, state = True):
		try:
			okpd = self.get(code = code)
		except OKPD.DoesNotExist:
			okpd             = OKPD()
			okpd.code        = code
			okpd.parent_code = parent_code
			okpd.alias       = alias
			okpd.name        = name
			if parent_code:
				okpd.parent  = self.take(parent_code)
			else:
				okpd.parent  = None
			okpd.state       = state
			okpd.created     = timezone.now()
			okpd.modified    = timezone.now()
			okpd.save()
		return okpd

	def update(self, code, parent_code = None, alias = None, name = None, state = True):
		try:
			okpd             = self.get(code = code)
			okpd.parent_code = parent_code
			okpd.alias       = alias
			okpd.name        = name
			if parent_code:
				okpd.parent  = self.take(parent_code)
			else:
				okpd.parent  = None
			okpd.state       = state
			okpd.modified    = timezone.now()
			okpd.save()
		except OKPD.DoesNotExist:
			okpd             = OKPD()
			okpd.code        = code
			okpd.parent_code = parent_code
			okpd.alias       = alias
			okpd.name        = name
			if parent_code:
				okpd.parent    = self.take(parent_code)
			else:
				okpd.parent    = None
			okpd.state         = state
			okpd.created       = timezone.now()
			okpd.modified      = timezone.now()
			okpd.save()
		return okpd


class OKPD(models.Model):

	code          = models.CharField(max_length = 100, unique = True)
	alias         = models.CharField(max_length = 100, null = True, default = None)
	name          = models.TextField(null = True, default = None)
	parent_code   = models.CharField(max_length = 100, null = True, default = None)
	parent        = models.ForeignKey('self', null = True, default = None)
	state         = models.BooleanField(default = True)
	created       = models.DateTimeField()
	modified      = models.DateTimeField()

	objects       = OKPDManager()

	def __str__(self):
		return "{} {}".format(self.alias, self.name)

	class Meta:
		ordering = ['alias']


class OKTMOManager(models.Manager):

	def take(self, code, parent_code = None, full_name = None, state = True):
		try:
			oktmo = self.get(code = code)
		except OKTMO.DoesNotExist:
			oktmo             = OKTMO()
			oktmo.code        = code
			oktmo.parent_code = parent_code
			oktmo.full_name   = full_name
			if parent_code:
				oktmo.parent  = self.take(parent_code)
			else:
				oktmo.parent  = None
			oktmo.state       = state
			oktmo.created     = timezone.now()
			oktmo.modified    = timezone.now()
			oktmo.save()
		return oktmo

	def update(self, code, parent_code = None, full_name = None, state = True):
		try:
			oktmo             = self.get(code = code)
			oktmo.parent_code = parent_code
			oktmo.full_name   = full_name
			if parent_code:
				oktmo.parent  = self.take(parent_code)
			else:
				oktmo.parent  = None
			oktmo.state       = state
			oktmo.modified    = timezone.now()
			oktmo.save()
		except OKTMO.DoesNotExist:
			oktmo             = OKTMO()
			oktmo.code        = code
			oktmo.parent_code = parent_code
			oktmo.full_name   = full_name
			if parent_code:
				oktmo.parent  = self.take(parent_code)
			else:
				oktmo.parent  = None
			oktmo.state       = state
			oktmo.created     = timezone.now()
			oktmo.modified    = timezone.now()
			oktmo.save()
		return oktmo


class OKTMO(models.Model):

	code        = models.CharField(max_length = 20, unique = True)
	full_name   = models.TextField(null = True, default = None)
	parent_code = models.CharField(max_length = 20, null = True, default = None)
	parent      = models.ForeignKey('self', null = True, default = None)
	state       = models.BooleanField(default = True)
	created     = models.DateTimeField()
	modified    = models.DateTimeField()

	objects       = OKTMOManager()

	def __str__(self):
		return self.full_name

	class Meta:
		ordering = ['code']


# TODO DEV


class OKVEDSectionManager(models.Manager):

	def take(self, name, state = True):
		try:
			okved_section = self.get(name = name)
		except OKVEDSection.DoesNotExist:
			okved_section          = OKVEDSection()
			okved_section.name     = name
			okved_section.state    = state
			okved_section.created  = timezone.now()
			okved_section.modified = timezone.now()
			okved_section.save()
		return okved_section

	def update(self, name, state = True):
		try:
			okved_section          = self.get(name = name)
			okved_section.state    = state
			okved_section.modified = timezone.now()
			okved_section.save()
		except OKVEDSection.DoesNotExist:
			okved_section          = OKVEDSection()
			okved_section.name     = name
			okved_section.state    = state
			okved_section.created  = timezone.now()
			okved_section.modified = timezone.now()
			okved_section.save()
		return okved_section


class OKVEDSection(models.Model):

	name     = models.CharField(max_length = 20, unique = True)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField()
	modified = models.DateTimeField()

	objects  = OKVEDSectionManager()

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']


class OKVEDSubSectionManager(models.Manager):

	def take(self, name, state = True):
		try:
			okved_subsection = self.get(name = name)
		except OKVEDSubSection.DoesNotExist:
			okved_subsection          = OKVEDSubSection()
			okved_subsection.name     = name
			okved_subsection.state    = state
			okved_subsection.created  = timezone.now()
			okved_subsection.modified = timezone.now()
			okved_subsection.save()
		return okved_subsection

	def update(self, name, state = True):
		try:
			okved_subsection          = self.get(name = name)
			okved_subsection.state    = state
			okved_subsection.modified = timezone.now()
			okved_subsection.save()
		except OKVEDSubSection.DoesNotExist:
			okved_subsection          = OKVEDSubSection()
			okved_subsection.name     = name
			okved_subsection.state    = state
			okved_subsection.created  = timezone.now()
			okved_subsection.modified = timezone.now()
			okved_subsection.save()
		return okved_subsection


class OKVEDSubSection(models.Model):

	name     = models.CharField(max_length = 20, unique = True)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField()
	modified = models.DateTimeField()

	objects  = OKVEDSubSectionManager()

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']


class OKVEDManager(models.Manager):

	def take(self, oos_id, parent_oos_id = None, code = None, section = None, subsection = None, name = None, state = True):
		try:
			okved = self.get(oos_id = oos_id)
		except OKVED.DoesNotExist:
			okved                = OKVED()
			okved.oos_id         = oos_id
			okved.parent_oos_id  = parent_oos_id
			if parent_oos_id:
				okved.parent     = self.take(oos_id = parent_oos_id)
			else:
				okved.parent     = None
			okved.code           = code
			if section:
				okved.section    = OKVEDSection.objects.take(name = section)
			else:
				okved.section    = None
			if subsection:
				okved.subsection = OKVEDSubSection.objects.take(name = subsection)
			else:
				okved.subsection = None
			okved.name           = name
			okved.state          = state
			okved.created        = timezone.now()
			okved.modified       = timezone.now()
			okved.save()
		return okved

	def update(self, oos_id, parent_oos_id = None, code = None, section = None, subsection = None, name = None, state = True):
		try:
			okved             = self.get(oos_id = oos_id)
			okved.parent_oos_id  = parent_oos_id
			if parent_oos_id:
				okved.parent     = self.take(oos_id = parent_oos_id)
			else:
				okved.parent     = None
			okved.code           = code
			if section:
				okved.section    = OKVEDSection.objects.take(name = section)
			else:
				okved.section    = None
			if subsection:
				okved.subsection = OKVEDSubSection.objects.take(name = subsection)
			else:
				okved.subsection = None
			okved.name           = name
			okved.state          = state
			okved.modified       = timezone.now()
			okved.save()
		except OKVED.DoesNotExist:
			okved                = OKVED()
			okved.oos_id         = oos_id
			okved.parent_oos_id  = parent_oos_id
			if parent_oos_id:
				okved.parent     = self.take(oos_id = parent_oos_id)
			else:
				okved.parent     = None
			okved.code           = code
			if section:
				okved.section    = OKVEDSection.objects.take(name = section)
			else:
				okved.section    = None
			if subsection:
				okved.subsection = OKVEDSubSection.objects.take(name = subsection)
			else:
				okved.subsection = None
			okved.name           = name
			okved.state          = state
			okved.created        = timezone.now()
			okved.modified       = timezone.now()
			okved.save()
		return okved


class OKVED(models.Model):

	oos_id        = models.CharField(max_length = 20, unique = True)
	parent_oos_id = models.CharField(max_length = 20, null = True, default = None)
	parent        = models.ForeignKey('self', null = True, default = None)
	code          = models.CharField(max_length = 100, null = True, default = None)
	section       = models.ForeignKey(OKVEDSection, null = True, default = None)
	subsection    = models.ForeignKey(OKVEDSubSection, null = True, default = None)
	name          = models.TextField(null = True, default = None)
	state         = models.BooleanField(default = True)
	created       = models.DateTimeField()
	modified      = models.DateTimeField()

	objects       = OKVEDManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']


class SubsystemTypeManager(models.Manager):

	def take(self, code, name = None, state = True):
		try:
			o = self.get(code = code)
		except SubsystemType.DoesNotExist:
			o          = SubsystemType()
			o.code     = code
			o.name     = name
			o.state    = state
			o.created  = timezone.now()
			o.modified = timezone.now()
			o.save()
		return o


class SubsystemType(models.Model):

	code     = models.CharField(max_length = 20, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField()
	modified = models.DateTimeField()

	objects  = SubsystemTypeManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']


class PlacingWayManager(models.Manager):

	def take(self, code, placing_way_id = None, name = None, placing_way_type = None, subsystem_type = None, state = True):
		try:
			o = self.get(code = code)
		except PlacingWay.DoesNotExist:
			o                    = PlacingWay()
			o.code               = code
			o.placing_way_id     = placing_way_id
			o.name               = name
			o.placing_way_type   = placing_way_type
			if subsystem_type:
				o.subsystem_type = SubsystemType.objects.take(code = subsystem_type)
			else:
				o.subsystem_type = None
			o.state              = state
			o.created            = timezone.now()
			o.modified           = timezone.now()
			o.save()
		return o

	def update(self, code, placing_way_id = None, name = None, placing_way_type = None, subsystem_type = None, state = True):
		try:
			o                    = self.get(code = code)
			o.placing_way_id     = placing_way_id
			o.name               = name
			o.placing_way_type   = placing_way_type
			if subsystem_type:
				o.subsystem_type = SubsystemType.objects.take(code = subsystem_type)
			else:
				o.subsystem_type = None
			o.state              = state
			o.modified           = timezone.now()
			o.save()
		except PlacingWay.DoesNotExist:
			o                    = PlacingWay()
			o.code               = code
			o.placing_way_id     = placing_way_id
			o.name               = name
			o.placing_way_type   = placing_way_type
			if subsystem_type:
				o.subsystem_type = SubsystemType.objects.take(code = subsystem_type)
			else:
				o.subsystem_type = None
			o.state              = state
			o.created            = timezone.now()
			o.modified           = timezone.now()
			o.save()
		return o


class PlacingWay(models.Model):

	placing_way_id   = models.CharField(max_length = 20, null = True, default = None)
	code             = models.CharField(max_length = 20, null = True, default = None)
	name             = models.TextField(null = True, default = None)
	palcing_way_type = models.CharField(max_length = 20, null = True, default = None)
	subsistem_type   = models.ForeignKey(SubsystemType, null = True, default = None)
	state            = models.BooleanField(default = True)
	created          = models.DateTimeField()
	modified         = models.DateTimeField()

	objects          = PlacingWayManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



















