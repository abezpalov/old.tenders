import uuid
from django.db import models
from django.utils import timezone


class UpdaterManager(models.Manager):

	def take(self, alias, name):
		try:
			o = self.get(alias = alias)
		except Updater.DoesNotExist:
			o = Updater(
				alias    = alias[:100],
				name     = name[:100],
				created  = timezone.now(),
				modified = timezone.now(),
				updated  = timezone.now())
			o.save()
		return o


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
		return "{}".format(self.name)

	class Meta:
		ordering = ['name']

class SourceManager(models.Manager):

	def take(self, url, state = False):
		try:
			o = self.get(url = url)
		except Source.DoesNotExist:
			o          = Source()
			o.url      = url[:2048]
			o.state    = state
			o.created  = timezone.now()
			o.modified = timezone.now()
			o.save()
		return o

class Source(models.Model):

	url      = models.CharField(max_length = 2048)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField()
	modified = models.DateTimeField()

	objects  = SourceManager()

	def complite(self):
		self.state    = True
		self.modified = timezone.now()
		self.save()
		return self

	def __str__(self):
		return "{}".format(self.name)


class CountryManager(models.Manager):

	def take(self, code, full_name, name = None, state = True):
		try:
			o = self.get(code = code)
		except Country.DoesNotExist:
			o = Country(
				code      = code[:100],
				name      = name,
				full_name = full_name,
				created   = timezone.now(),
				modified  = timezone.now())
			o.save()
		return o

	def update(self, code, full_name, name = None, state = True):
		try:
			o           = self.get(code = code)
			if name:
				o.name  = name
			o.full_name = full_name
			o.state     = state
			o.modified  = timezone.now()
			o.save()
		except Country.DoesNotExist:
			o = self.take(
				code      = code,
				full_name = full_name,
				name      = name,
				state     = state)
		return o


class Country(models.Model):

	code      = models.CharField(max_length = 10, unique = True)
	name      = models.TextField(null = True, default = None)
	full_name = models.TextField(null = True, default = None)
	state     = models.BooleanField(default = True)
	created   = models.DateTimeField()
	modified  = models.DateTimeField()

	objects   = CountryManager()

	def __str__(self):
		return "{} {}".format(self.code, self.full_name)

	class Meta:
		ordering = ['name']

class RegionManager(models.Manager):

	def take(self, alias, name, full_name):
		try:
			o = self.get(alias = alias)
		except Region.DoesNotExist:
			o = Region(
				alias     = alias[:100],
				name      = name[:100],
				full_name = full_name[:100],
				created   = timezone.now(),
				modified  = timezone.now())
			o.save()
		return o


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
		return "{}".format(self.name)

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
		return "{} {}".format(self.code, self.name)

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
		return "{} {}".format(self.code, self.name)

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
		return "{} {}".format(self.code, self.name)

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
		return "{}".format(self.local_symbol)

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
		return "{} {}".format(self.code, self.name)

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
		return "{} {}".format(self.code, self.full_name)

	class Meta:
		ordering = ['code']


class OKPDManager(models.Manager):

	def take(self, oos_id, parent_oos_id = None, code = None, name = None, state = True):
		try:
			okpd = self.get(oos_id = oos_id)
		except OKPD.DoesNotExist:
			okpd               = OKPD()
			okpd.oos_id        = oos_id
			okpd.parent_oos_id = parent_oos_id
			okpd.code          = code
			okpd.name          = name
			if parent_oos_id:
				okpd.parent  = self.take(oos_id = parent_oos_id)
			else:
				okpd.parent  = None
			okpd.state       = state
			okpd.created     = timezone.now()
			okpd.modified    = timezone.now()
			okpd.save()
		return okpd

	def update(self, oos_id, parent_oos_id = None, code = None, name = None, state = True):
		try:
			okpd = self.get(oos_id = oos_id)
			okpd.parent_oos_id = parent_oos_id
			okpd.code          = code
			okpd.name          = name
			if parent_oos_id:
				okpd.parent  = self.take(oos_id = parent_oos_id)
			else:
				okpd.parent  = None
			okpd.state       = state
			okpd.modified    = timezone.now()
			okpd.save()
		except OKPD.DoesNotExist:
			okpd = OKPD()
			okpd.oos_id        = oos_id
			okpd.parent_oos_id = parent_oos_id
			okpd.code          = code
			okpd.name          = name
			if parent_oos_id:
				okpd.parent    = self.take(oos_id = parent_oos_id)
			else:
				okpd.parent    = None
			okpd.state         = state
			okpd.created       = timezone.now()
			okpd.modified      = timezone.now()
			okpd.save()
		return okpd


class OKPD(models.Model):

	oos_id        = models.CharField(max_length = 100, unique = True)
	code          = models.CharField(max_length = 100, null = True, default = None)
	name          = models.TextField(null = True, default = None)
	parent_oos_id = models.CharField(max_length = 100, null = True, default = None)
	parent        = models.ForeignKey('self', null = True, default = None)
	state         = models.BooleanField(default = True)
	created       = models.DateTimeField()
	modified      = models.DateTimeField()

	objects       = OKPDManager()

	def __str__(self):
		return "{}".format(self.code)

	class Meta:
		ordering = ['code']


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
		return "{} {}".format(self.code, self.full_name)

	class Meta:
		ordering = ['code']


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
		return "{}".format(self.name)

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
		return "{}".format(self.name)

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


class OrganisationTypeManager(models.Manager):

	def take(self, code, name = None, description = None):
		try:
			o = self.get(code = code)
		except OrganisationType.DoesNotExist:
			o             = OrganisationType()
			o.code        = code
			o.name        = name
			o.description = description
			o.created     = timezone.now()
			o.modified    = timezone.now()
			o.save()
		return o

	def update(self, code, name = None, description = None):
		try:
			o             = self.get(code = code)
			o.name        = name
			o.description = description
			o.modified    = timezone.now()
			o.save()
		except OrganisationType.DoesNotExist:
			o = self.take(
				code        = code,
				name        = name,
				description = description)
		return o


class OrganisationType(models.Model):

	code        = models.CharField(max_length = 20, unique = True)
	name        = models.TextField(null = True, default = None)
	description = models.TextField(null = True, default = None)
	created     = models.DateTimeField()
	modified    = models.DateTimeField()

	objects     = OrganisationTypeManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']


class BudgetManager(models.Manager):

	def take(self, code, name = None, state = True):
		try:
			o = self.get(code = code)
		except Budget.DoesNotExist:
			o          = Budget()
			o.code     = code
			o.name     = name
			o.state    = state
			o.created  = timezone.now()
			o.modified = timezone.now()
			o.save()
		return o

	def update(self, code, name = None, state = True):
		try:
			o          = self.get(code = code)
			o.name     = name
			o.state    = state
			o.modified = timezone.now()
			o.save()
		except Budget.DoesNotExist:
			o = self.take(
				code  = code,
				name  = name,
				state = state)
		return o


class Budget(models.Model):

	code     = models.CharField(max_length = 20, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField()
	modified = models.DateTimeField()

	objects  = BudgetManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']


class BudgetTypeManager(models.Manager):

	def take(self, code, name = None, subsystem_type = None, state = True):
		try:
			o = self.get(code = code)
		except BudgetType.DoesNotExist:
			o                = BudgetType()
			o.code           = code
			o.name           = name
			o.subsystem_type = subsystem_type
			o.state          = state
			o.created        = timezone.now()
			o.modified       = timezone.now()
			o.save()
		return o

	def update(self, code, name = None, subsystem_type = None, state = True):
		try:
			o                = self.get(code = code)
			o.name           = name
			o.subsystem_type = subsystem_type
			o.state          = state
			o.modified       = timezone.now()
			o.save()
		except BudgetType.DoesNotExist:
			o = self.take(
				code           = code,
				name           = name,
				subsystem_type = subsystem_type,
				state          = state)
		return o


class BudgetType(models.Model):

	code           = models.CharField(max_length = 20, unique = True)
	name           = models.TextField(null = True, default = None)
	subsystem_type = models.ForeignKey(SubsystemType, null = True, default = None)
	state          = models.BooleanField(default = True)
	created        = models.DateTimeField()
	modified       = models.DateTimeField()

	objects  = BudgetTypeManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']


class KBKBudgetManager(models.Manager):

	def take(self, code, budget = None, state = True):
		try:
			o = self.get(code = code)
		except KBKBudget.DoesNotExist:
			o          = KBKBudget()
			o.code     = code
			o.budget   = budget
			o.state    = state
			o.created  = timezone.now()
			o.modified = timezone.now()
			o.save()
		return o

	def update(self, code, budget = None, state = True):
		try:
			o          = self.get(code = code)
			o.budget   = budget
			o.state    = state
			o.modified = timezone.now()
			o.save()
		except KBKBudget.DoesNotExist:
			o = self.take(
				code   = code,
				budget = budget,
				state  = state)
		return o


class KBKBudget(models.Model):

	code     = models.CharField(max_length = 50, unique = True)
	budget   = models.ForeignKey(Budget, null = True, default = None)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField()
	modified = models.DateTimeField()

	objects  = KBKBudgetManager()

	def __str__(self):
		return "{} {}".format(self.code, self.budget)

	class Meta:
		ordering = ['code']


class OKOGUManager(models.Manager):

	def take(self, code, name = None, state = True):
		try:
			o = self.get(code = code)
		except OKOGU.DoesNotExist:
			o          = Budget()
			o.code     = code
			o.name     = name
			o.state    = state
			o.created  = timezone.now()
			o.modified = timezone.now()
			o.save()
		return o


class OKOGU(models.Model):

	code     = models.CharField(max_length = 20, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField()
	modified = models.DateTimeField()

	objects  = OKOGUManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']


class OrganisationManager(models.Manager):

	def take(self, reg_number, short_name = None, full_name = None, head_agency = None, ordering_agency = None, okogu = None, inn = None, kpp = None, okpo = None, organisation_type = None, oktmo = None, state = True, register = True):
		try:
			o = self.get(reg_number = reg_number)
		except Organisation.DoesNotExist:
			o                       = Organisation()
			o.reg_number            = reg_number
			o.short_name            = short_name
			o.full_name             = full_name
			o.head_agency           = head_agency
			o.ordering_agency       = ordering_agency
			o.okogu                 = okogu
			o.inn                   = inn
			o.kpp                   = kpp
			o.okpo                  = okpo
			o.organisation_type     = organisation_type
			o.oktmo                 = oktmo
			o.state                 = state
			o.register              = register
			o.created               = timezone.now()
			o.modified              = timezone.now()
			o.save()
		return o

	def update(self, reg_number, short_name = None, full_name = None, head_agency = None, ordering_agency = None, okogu = None, inn = None, kpp = None, okpo = None, organisation_type = None, oktmo = None, state = True, register = True):
		try:
			o                       = self.get(reg_number = reg_number)
			o.short_name            = short_name
			o.full_name             = full_name
			o.head_agency           = head_agency
			o.ordering_agency       = ordering_agency
			o.okogu                 = okogu
			o.inn                   = inn
			o.kpp                   = kpp
			o.okpo                  = okpo
			o.organisation_type     = organisation_type
			o.oktmo                 = oktmo
			o.state                 = state
			o.register              = register
			o.modified              = timezone.now()
			o.save()
		except Organisation.DoesNotExist:
			o = self.take(
				reg_number        = reg_number,
				short_name        = short_name,
				full_name         = full_name,
				head_agency       = head_agency,
				ordering_agency   = ordering_agency,
				okogu             = okogu,
				inn               = inn,
				kpp               = kpp,
				okpo              = okpo,
				organisation_type = organisation_type,
				oktmo             = oktmo,
				state             = state,
				register          = register)
		return o


class Organisation(models.Model):

	reg_number        = models.CharField(max_length = 20, unique = True)
	short_name        = models.TextField(null = True, default = None)
	full_name         = models.TextField(null = True, default = None)
	# factual_address
	# postal_address
	# email
	# phone
	# fax
	# contact_person
	# accounts
	# budgets
	head_agency       = models.ForeignKey('self', related_name = 'organisation_head_agency', null = True, default = None)
	ordering_agency   = models.ForeignKey('self', related_name = 'organisation_ordering_agency', null = True, default = None)
	okogu             = models.ForeignKey(OKOGU, null = True, default = None)
	inn               = models.CharField(max_length = 20, null = True, default = None)
	kpp               = models.CharField(max_length = 20, null = True, default = None)
	okpo              = models.CharField(max_length = 20, null = True, default = None)
	# okved
	organisation_type = models.ForeignKey(OrganisationType, null = True, default = None)
	oktmo             = models.ForeignKey(OKTMO, null = True, default = None)
	state             = models.BooleanField(default = True)
	register          = models.BooleanField(default = True)
	created           = models.DateTimeField()
	modified          = models.DateTimeField()

	objects     = OrganisationManager()

	def __str__(self):
		return "{} {}".format(self.reg_number, self.short_name)

	class Meta:
		ordering = ['reg_number']


# TODO OrganisationRight


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
			o = self.take(
				code             = code,
				placing_way_id   = placing_way_id,
				name             = name,
				placing_way_type = placing_way_type,
				subsystem_type   = subsystem_type,
				state            = state)
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


class PlanPositionChangeReasonManager(models.Manager):

	def take(self, oos_id, name = None, description = None, state = True):
		try:
			o = self.get(oos_id = oos_id)
		except PlanPositionChangeReason.DoesNotExist:
			o             = PlanPositionChangeReason()
			o.oos_id      = oos_id
			o.name        = name
			o.description = description
			o.state       = state
			o.created     = timezone.now()
			o.modified    = timezone.now()
			o.save()
		return o

	def update(self, oos_id, name = None, description = None, state = True):
		try:
			o             = self.get(oos_id = oos_id)
			o.name        = name
			o.description = description
			o.state       = state
			o.modified    = timezone.now()
			o.save()
		except PlanPositionChangeReason.DoesNotExist:
			o = self.take(
				oos_id      = oos_id,
				name        = name,
				description = description,
				state       = state)
		return o


class PlanPositionChangeReason(models.Model):

	oos_id      = models.CharField(max_length = 20, null = True, default = None)
	name        = models.TextField(null = True, default = None)
	description = models.TextField(null = True, default = None)
	state       = models.BooleanField(default = True)
	created     = models.DateTimeField()
	modified    = models.DateTimeField()

	objects     = PlanPositionChangeReasonManager()

	def __str__(self):
		return "{} {}".format(self.oos_id, self.name)

	class Meta:
		ordering = ['oos_id']


class ContactPersonManager(models.Manager):

	def take(self, first_name, middle_name, last_name, email, phone, fax = None, position = None, description = None, state = True):
		try:
			o = self.get(
				first_name  = first_name,
				middle_name = middle_name,
				last_name   = last_name,
				email       = email)
		except ContactPerson.DoesNotExist:
			o             = ContactPerson()
			o.first_name  = first_name
			o.middle_name = middle_name
			o.last_name   = last_name
			o.email       = email
			o.phone       = phone
			o.fax         = fax
			o.position    = position
			o.description = description
			o.state       = state
			o.created     = timezone.now()
			o.modified    = timezone.now()
			o.save()
		return o

	def update(self, first_name, middle_name, last_name, email, phone = None, fax = None, position = None, description = None, state = True):
		try:
			o = self.get(
				first_name  = first_name,
				middle_name = midle_name,
				last_name   = last_name,
				email       = email)
			o.phone       = phone
			o.fax         = fax
			o.position    = position
			o.description = description
			o.state       = state
			o.modified    = timezone.now()
			o.save()
		except ContactPerson.DoesNotExist:
			o = self.take(
				first_name  = first_name,
				middle_name = middle_name,
				last_name   = last_name,
				email       = email,
				phone       = phone,
				fax         = fax,
				position    = position,
				description = description,
				state       = state)
		return o


class ContactPerson(models.Model):

	first_name  = models.CharField(max_length = 100, null = True, default = None)
	middle_name = models.CharField(max_length = 100, null = True, default = None)
	last_name   = models.CharField(max_length = 100, null = True, default = None)
	email       = models.CharField(max_length = 100, null = True, default = None)
	phone       = models.CharField(max_length = 100,  null = True, default = None)
	fax         = models.CharField(max_length = 100,  null = True, default = None)
	position    = models.CharField(max_length = 100, null = True, default = None)
	description = models.TextField(null = True, default = None)
	state       = models.BooleanField(default = True)
	created     = models.DateTimeField()
	modified    = models.DateTimeField()

	objects     = ContactPersonManager()

	def __str__(self):
		return "{} {} {]".format(self.first_name, self.middle_name, self.last_name)

	class Meta:
		ordering = ['first_name', 'middle_name', 'last_name']


class PlanGraphManager(models.Manager):

	def take(self, oos_id, number = None, year = None, version = None,
			region = None, owner = None, create_date = None, description = None,
			confirm_date = None, publish_date = None, customer = None,
			oktmo = None, contact_person = None):
		try:
			o = self.get(oos_id = oos_id, number = number, version = version)
		except PlanGraph.DoesNotExist:
			o                = PlanGraph()
			o.oos_id         = oos_id
			o.number         = number
			o.year           = year
			o.version        = version
			o.region         = region
			o.owner          = owner
			o.create_date    = create_date
			o.description    = description
			o.confirm_date   = confirm_date
			o.publish_date   = publish_date
			o.customer       = customer
			o.oktmo          = oktmo
			o.contact_person = contact_person
			o.modified       = timezone.now()
			o.created        = timezone.now()
			o.save()
		return o

	def update(self, oos_id, number = None, year = None, version = None,
			region = None, owner = None, create_date = None, description = None,
			confirm_date = None, publish_date = None, customer = None,
			oktmo = None, contact_person = None):
		try:
			o = self.get(oos_id = oos_id, number = number, version = version)
			o.year           = year
			o.region         = region
			o.owner          = owner
			o.create_date    = create_date
			o.description    = description
			o.confirm_date   = confirm_date
			o.publish_date   = publish_date
			o.customer       = customer
			o.oktmo          = oktmo
			o.contact_person = contact_person
			o.modified       = timezone.now()
			o.save()

		except PlanGraph.DoesNotExist:
			o = self.take(
				oos_id         = oos_id,
				number         = number,
				year           = year,
				version        = version,
				region         = region,
				owner          = owner,
				create_date    = create_date,
				description    = description,
				confirm_date   = confirm_date,
				publish_date   = publish_date,
				customer       = customer,
				oktmo          = oktmo,
				contact_person = contact_person)

		# Корректируем статусы устаревших версий
		self.filter(number = number, version__lt = version).update(state = False)

		plan_graphs = self.filter(number = number, version__lt = version)
		PlanGraphPosition.objects.filter(plan_graph__in = plan_graphs).update(state = False)

		return o

	def cancel(self, oos_id, number):

		self.filter(number = number).update(state = False)

		return True


class PlanGraph(models.Model):

	oos_id         = models.CharField(max_length = 20)
	number         = models.CharField(max_length = 20)
	year           = models.IntegerField(null = True, default = None)
	version        = models.IntegerField()
	region         = models.ForeignKey(Region, related_name = 'plan_graph_region', null = True, default = None)
	owner          = models.ForeignKey(Organisation, related_name = 'plan_graph_owner', null = True, default = None)
	create_date    = models.DateTimeField(null = True, default = None)
	description    = models.TextField(null = True, default = None)
	confirm_date   = models.DateTimeField(null = True, default = None)
	publish_date   = models.DateTimeField(null = True, default = None)
	customer       = models.ForeignKey(Organisation, related_name = 'plan_graph_customer', null = True, default = None)
	oktmo          = models.ForeignKey(OKTMO, null = True, default = None)
	contact_person = models.ForeignKey(ContactPerson, null = True, default = None)
	state          = models.BooleanField(default = True)
	created        = models.DateTimeField()
	modified       = models.DateTimeField()

	objects        = PlanGraphManager()

	def __str__(self):
		return "{} {} v{} {} ".format(self.year, self.number, self.version, self.customer)

	class Meta:
		ordering = ['year', 'number', 'version']
		unique_together = ("oos_id", "number", "version")


class PlanGraphPositionManager(models.Manager):

	def take(self, plan_graph, number, ext_number = None, okveds = None,
			okpds = None, subject_name = None, max_price = None,
			payments = None, currency = None, placing_way = True,
			change_reason = None, publish_date = None,
			public_discussion = False, placing_year = None,
			placing_month = None, execution_year = None, execution_month = None,
			state = True):
		try:
			o = self.get(plan_graph = plan_graph, number = number)
		except PlanGraphPosition.DoesNotExist:
			o                   = PlanGraphPosition()
			o.plan_graph        = plan_graph
			o.number            = number
			o.ext_number        = ext_number
			o.subject_name      = subject_name
			o.max_price         = max_price
			o.payments          = payments
			o.currency          = currency
			o.placing_way       = placing_way
			o.change_reason     = change_reason
			o.publish_date      = publish_date
			o.public_discussion = public_discussion
			o.placing_year      = placing_year
			o.placing_month     = placing_month
			o.execution_year    = execution_year
			o.execution_month   = execution_month
			o.state             = state
			o.created           = timezone.now()
			o.modified          = timezone.now()
			o.save()

			try:
				o.okveds = okveds
			except:
				print("Ошибка связей.")


			try:
				o.okpds = okpds
			except:
				print("Ошибка связей.")

		return o

	def update(self, plan_graph, number, ext_number = None, okveds = None,
			okpds = None, subject_name = None, max_price = None,
			payments = None, currency = None, placing_way = True,
			change_reason = None, publish_date = None,
			public_discussion = False, placing_year = None,
			placing_month = None, execution_year = None, execution_month = None,
			state = True):
		try:
			o = self.get(plan_graph = plan_graph, number = number)
			o.ext_number        = ext_number
			o.subject_name      = subject_name
			o.max_price         = max_price
			o.payments          = payments
			o.currency          = currency
			o.placing_way       = placing_way
			o.change_reason     = change_reason
			o.publish_date      = publish_date
			o.public_discussion = public_discussion
			o.placing_year      = placing_year
			o.placing_month     = placing_month
			o.execution_year    = execution_year
			o.execution_month   = execution_month
			o.state             = state
			o.modified          = timezone.now()
			o.save()

			try:
				o.okveds = okveds
			except:
				print("Ошибка связей.")


			try:
				o.okpds = okpds
			except:
				print("Ошибка связей.")

			o.save()
		except PlanGraphPosition.DoesNotExist:
			o = self.take(
				plan_graph        = plan_graph,
				number            = number,
				ext_number        = ext_number,
				okveds            = okveds,
				okpds             = okpds,
				subject_name      = subject_name,
				max_price         = max_price,
				payments          = payments,
				currency          = currency,
				placing_way       = placing_way,
				change_reason     = change_reason,
				publish_date      = publish_date,
				public_discussion = public_discussion,
				placing_year      = placing_year,
				placing_month     = placing_month,
				execution_year    = execution_year,
				execution_month   = execution_month,
				state             = state)
		return o


class PlanGraphPosition(models.Model):

	plan_graph        = models.ForeignKey(PlanGraph)
	number            = models.CharField(max_length = 50)
	ext_number        = models.CharField(max_length = 50, null = True, default = None)
	okveds            = models.ManyToManyField(OKVED, db_table = 'tenders_plan_graph_position_to_okved', related_name = 'plan_graph_position_okved')
	okpds             = models.ManyToManyField(OKPD, db_table = 'tenders_plan_graph_position_to_okpd', related_name = 'plan_graph_position_okpd')
	subject_name      = models.TextField(null = True, default = None)
	max_price         = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	payments          = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	currency          = models.ForeignKey(Currency, null = True, default = None)
	placing_way       = models.ForeignKey(PlacingWay, null = True, default = None)
	change_reason     = models.ForeignKey(PlanPositionChangeReason, null = True, default = None)
	publish_date      = models.DateTimeField(null = True, default = None)
	public_discussion = models.BooleanField(default = True)
	placing_year      = models.IntegerField(null = True, default = None)
	placing_month     = models.IntegerField(null = True, default = None)
	execution_year    = models.IntegerField(null = True, default = None)
	execution_month   = models.IntegerField(null = True, default = None)
	state             = models.BooleanField(default = True)
	created           = models.DateTimeField()
	modified          = models.DateTimeField()

	objects           = PlanGraphPositionManager()

	def __str__(self):
		return "{} {}".format(self.number, self.subject_name)

	def _get_price_str(self):

		try:
			price = self.max_price
			currency = self.currency
		except: return ''

		if price:
			price = '{:,}'.format(round(price, 2))
			price = price.replace(',', '\u00a0')
			price = price.replace('.', ',')
			price = price + '\u00a0' + currency.code
		else: return ''

		return price

	price_str = property(_get_price_str)

	def _get_placing_str(self):

		result = ""

		if self.placing_month:
			if   self.placing_month == 1:  result += "январь"
			elif self.placing_month == 2:  result += "февраль"
			elif self.placing_month == 3:  result += "март"
			elif self.placing_month == 4:  result += "апрель"
			elif self.placing_month == 5:  result += "май"
			elif self.placing_month == 6:  result += "июнь"
			elif self.placing_month == 7:  result += "июль"
			elif self.placing_month == 8:  result += "август"
			elif self.placing_month == 9:  result += "сентябрь"
			elif self.placing_month == 10: result += "октябрь"
			elif self.placing_month == 11: result += "ноябрь"
			elif self.placing_month == 12: result += "декабрь"

		if self.placing_year and self.placing_month:
			result += " "

		if self.placing_year:
			result += str(self.placing_year)

		return result

	placing_str = property(_get_placing_str)

	class Meta:
		ordering = ['number']
		unique_together = ("plan_graph", "number")


class PlanGraphPositionProductManager(models.Manager):

	def take(self, position, number, okpd = None, name = None,
			min_requirement = None, okei = None, max_sum = None, price = None,
			quantity_undefined = None, quantity = None,
			quantity_current_year = None, state = True):
		try:
			o = self.get(position = position, number = number)
		except PlanGraphPositionProduct.DoesNotExist:
			o                       = PlanGraphPositionProduct()
			o.position              = position
			o.number                = number
			o.okpd                  = okpd
			o.name                  = name
			o.min_requirement       = min_requirement
			o.okei                  = okei
			o.max_sum               = max_sum
			o.price                 = price
			o.quantity_undefined    = quantity_undefined
			o.quantity              = quantity
			o.quantity_current_year = quantity_current_year
			o.state                 = state
			o.created               = timezone.now()
			o.modified              = timezone.now()
			o.save()
		return o

	def update(self, position, number, okpd = None, name = None,
			min_requirement = None, okei = None, max_sum = None, price = None,
			quantity_undefined = None, quantity = None,
			quantity_current_year = None, state = True):
		try:
			o = self.get(position = position, number = number)
			o.okpd                  = okpd
			o.name                  = name
			o.min_requirement       = min_requirement
			o.okei                  = okei
			o.max_sum               = max_sum
			o.price                 = price
			o.quantity_undefined    = quantity_undefined
			o.quantity              = quantity
			o.quantity_current_year = quantity_current_year
			o.state                 = state
			o.state             = state
			o.modified          = timezone.now()
			o.save()
		except PlanGraphPositionProduct.DoesNotExist:
			o = self.take(
				position              = position,
				number                = number,
				okpd                  = okpd,
				name                  = name,
				min_requirement       = min_requirement,
				okei                  = okei,
				max_sum               = max_sum,
				price                 = price,
				quantity_undefined    = quantity_undefined,
				quantity              = quantity,
				quantity_current_year = quantity_current_year,
				state                 = state)
		return o


class PlanGraphPositionProduct(models.Model):

	position              = models.ForeignKey(PlanGraphPosition)
	number                = models.IntegerField()
	okpd                  = models.ForeignKey(OKPD, null = True, default = None)
	name                  = models.TextField(null = True, default = None)
	min_requipment        = models.TextField(null = True, default = None)
	okei                  = models.ForeignKey(OKEI, null = True, default = None)
	max_sum               = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	price                 = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	quantity_undefined    = models.BooleanField(default = True)
	quantity              = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	quantity_current_year = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	state                 = models.BooleanField(default = True)
	created               = models.DateTimeField()
	modified              = models.DateTimeField()

	objects               = PlanGraphPositionProductManager()

	def __str__(self):
		return "{}".format(self.name)

	def _get_max_sum_str(self):

		try:
			max_sum  = self.max_sum
			currency = self.position.currency
		except: return '-'

		if max_sum:
			max_sum = '{:,}'.format(round(max_sum, 2))
			max_sum = max_sum.replace(',', '\u00a0')
			max_sum = max_sum.replace('.', ',')
			max_sum = '{}\u00a0{}'.format(max_sum, currency.code)
			return max_sum
		else:
			return '-'

	max_sum_str = property(_get_max_sum_str)

	def _get_price_str(self):

		try:
			price    = self.price
			currency = self.position.currency
		except: return '-'

		if price:
			price = '{:,}'.format(round(price, 2))
			price = price.replace(',', '\u00a0')
			price = price.replace('.', ',')
			price = '{}\u00a0{}'.format(price, currency.code)
			return price
		else:
			return '-'

	price_str = property(_get_price_str)

	def _get_quantity_str(self):

		try:
			quantity = self.quantity
			unit     = self.okei
		except: return '-'

		if quantity:
			quantity = '{:,}'.format(round(quantity, 2))
			quantity = quantity.replace(',', '\u00a0')
			quantity = quantity.replace('.', ',')
			quantity = '{}\u00a0{}'.format(quantity, unit.local_symbol)
			return quantity
		else:
			return '-'

	quantity_str = property(_get_quantity_str)

	class Meta:
		ordering = ['number']
		unique_together = ("position", "number")


class Word(models.Model):

	word     = models.CharField(max_length = 100, unique = True)
	created  = models.DateTimeField()
	modified = models.DateTimeField()

	def __str__(self):
		return "{}".format(self.word)

	class Meta:
		ordering = ['word']


class QueryFilter(models.Model):

	name        = models.CharField(max_length = 100)
	regions     = models.ManyToManyField(Region,       db_table = 'tenders_queryfilter_to_region',   related_name = 'queryfilter_region')
	customers   = models.ManyToManyField(Organisation, db_table = 'tenders_queryfilter_to_customer', related_name = 'queryfilter_customer')
	owners      = models.ManyToManyField(Organisation, db_table = 'tenders_queryfilter_to_owner',    related_name = 'queryfilter_owner')
	okveds      = models.ManyToManyField(OKVED,        db_table = 'tenders_queryfilter_to_okved',    related_name = 'queryfilter_okved')
	okpds       = models.ManyToManyField(OKPD,         db_table = 'tenders_queryfilter_to_okpd',     related_name = 'queryfilter_okpd')
	words       = models.ManyToManyField(Word,         db_table = 'tenders_queryfilter_to_word',     related_name = 'queryfilter_word')

	regions_in  = models.BooleanField(default=True)
	customer_in = models.BooleanField(default=True)
	owner_in    = models.BooleanField(default=True)
	okveds_in   = models.BooleanField(default=True)
	okpds_in    = models.BooleanField(default=True)
	words_in    = models.BooleanField(default=True)

	state       = models.BooleanField(default=True)
	public      = models.BooleanField(default=False)

	created     = models.DateTimeField()
	created_by  = models.CharField(max_length=100, null=True, default=None)
	modified    = models.DateTimeField()
	modified_by = models.CharField(max_length=100, null=True, default=None)

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['name']
