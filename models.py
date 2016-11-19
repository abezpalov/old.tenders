import uuid
from django.db import models
from django.utils import timezone



class UpdaterManager(models.Manager):

	def take(self, alias, name):
		try:
			o = self.get(alias = alias)
		except Updater.DoesNotExist:
			o = Updater()
			o.alias = alias[:100]
			o.name  = name[:100]
			o.save()
		return o



class Updater(models.Model):

	name     = models.CharField(max_length = 100)
	alias    = models.CharField(max_length = 100, unique = True)
	login    = models.CharField(max_length = 100)
	password = models.CharField(max_length = 100)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField(default = timezone.now)
	modified = models.DateTimeField(default = timezone.now)
	updated  = models.DateTimeField(default = timezone.now)

	objects  = UpdaterManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['name']



class SourceManager(models.Manager):

	def take(self, url):
		try:
			o = self.get(url = url)
		except Source.DoesNotExist:
			o          = Source()
			o.url      = url[:2048]
			o.save()
		return o



class Source(models.Model):

	url      = models.CharField(max_length = 2048)
	state    = models.BooleanField(default = False)
	created  = models.DateTimeField(default = timezone.now)
	modified = models.DateTimeField(default = timezone.now)

	objects  = SourceManager()


	def is_parsed(self):

		if self.state:
			print("Обработан: {}.".format(self.url))
			return True
		else:
			return False


	def complite(self):

		self.state    = True
		self.modified = timezone.now()
		self.save()
		return self


	def __str__(self):
		return "{}".format(self.url)



class RegionManager(models.Manager):

	def take(self, alias, name, full_name):
		try:
			o = self.get(alias = alias)
		except Region.DoesNotExist:
			o = Region()
			o.alias     = alias[:100]
			o.name      = name[:100]
			o.full_name = full_name[:100]
			o.save()
		return o



class Region(models.Model):

	name      = models.TextField(null = True, default = None)
	full_name = models.TextField(null = True, default = None)
	alias     = models.CharField(max_length = 100, unique = True)
	state     = models.BooleanField(default = False)
	created   = models.DateTimeField(default = timezone.now)
	modified  = models.DateTimeField(default = timezone.now)
	updated   = models.DateTimeField(null = True, default = None)

	objects   = RegionManager()
	
	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['name']



class CountryManager(models.Manager):


	def take(self, code, full_name, name = None, state = True):
		try:
			o = self.get(code = code)
		except Country.DoesNotExist:
			o = Country()
			o.code      = code[:100]
			o.state     = state
			o.full_name = full_name
			if name:
				o.name  = name
			else:
				o.name  = full_name
			o.save()
		return o


	def update(self, code, full_name, name = None, state = True):
		try:
			o           = self.get(code = code)
			o.full_name = full_name
			if name:
				o.name  = name
			elif not o.name:
				o.name  = full_name
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
	full_name = models.TextField(null = True, default = None)
	name      = models.TextField(null = True, default = None)
	state     = models.BooleanField(default = True)
	created   = models.DateTimeField(default = timezone.now)
	modified  = models.DateTimeField(default = timezone.now)

	objects   = CountryManager()

	def __str__(self):
		return "{} {}".format(self.code, self.full_name)

	class Meta:
		ordering = ['name']



class CurrencyManager(models.Manager):


	def take(self, code, digital_code = None, name = None, state = True):
		try:
			o = self.get(code = code)
		except Currency.DoesNotExist:
			o              = Currency()
			o.code         = code
			o.digital_code = digital_code
			o.name         = name
			o.state        = state
			o.save()
		return o


	def update(self, code, digital_code = None, name = None, state = True):
		try:
			o              = self.get(code = code)
			o.digital_code = digital_code
			o.name         = name
			o.state        = state
			o.modified     = timezone.now()
			o.save()
		except Currency.DoesNotExist:
			o = self.take(
				code         = code,
				digital_code = digital_code,
				name         = name,
				state        = state)
		return o


class Currency(models.Model):

	code         = models.CharField(max_length = 10, unique = True)
	digital_code = models.CharField(max_length = 10, unique = True)
	name         = models.TextField(null = True, default = None)
	state        = models.BooleanField(default = True)
	created      = models.DateTimeField(default = timezone.now)
	modified     = models.DateTimeField(default = timezone.now)

	objects      = CurrencyManager()

	def __str__(self):
		return "{}".format(self.code)

	class Meta:
		ordering = ['code']



class OKEISectionManager(models.Manager):


	def take(self, code, name = None, state = True):
		try:
			o = self.get(code = code)
		except OKEISection.DoesNotExist:
			o          = OKEISection()
			o.code     = code[:10]
			o.name     = name
			o.state    = state
			o.save()
		return o


	def update(self, code, name = None, state = True):
		try:
			o          = self.get(code = code)
			o.name     = name
			o.state    = state
			o.modified = timezone.now()
			o.save()
		except OKEISection.DoesNotExist:
			o = self.take(
				code  = code,
				name  = name,
				state = state)
		return o



class OKEISection(models.Model):

	code     = models.CharField(max_length = 10, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField(default = timezone.now)
	modified = models.DateTimeField(default = timezone.now)

	objects  = OKEISectionManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['code']



class OKEIGroupManager(models.Manager):


	def take(self, code, name = None, state = True):
		try:
			o = self.get(code = code)
		except OKEIGroup.DoesNotExist:
			o          = OKEIGroup()
			o.code     = code[:10]
			o.name     = name
			o.state    = state
			o.save()
		return o


	def update(self, code, name = None, state = True):
		try:
			o          = self.get(code = code)
			o.name     = name
			o.state    = state
			o.modified = timezone.now()
			o.save()
		except OKEIGroup.DoesNotExist:
			o = self.take(
				code  = code,
				name  = name,
				state = state)
		return o



class OKEIGroup(models.Model):

	code     = models.CharField(max_length = 10, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField(default = timezone.now)
	modified = models.DateTimeField(default = timezone.now)
	objects  = OKEIGroupManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['code']



class OKEIManager(models.Manager):

	def take(self, code, full_name = None, section = None, group = None, local_name = None, international_name = None, local_symbol = None, international_symbol = None, state = True):
		try:
			o = self.get(code = code)
		except OKEI.DoesNotExist:
			o                      = OKEI()
			o.code                 = code
			o.full_name            = full_name
			o.section              = section
			o.group                = group
			o.local_name           = local_name
			o.international_name   = international_name
			o.local_symbol         = local_symbol
			o.international_symbol = international_symbol
			o.state                = state
			o.created              = timezone.now()
			o.modified             = timezone.now()
			o.save()
		return o

	def update(self, code, full_name = None, section = None, group = None, local_name = None, international_name = None, local_symbol = None, international_symbol = None, state = True):
		try:
			o                      = self.get(code = code)
			o.full_name            = full_name
			o.section              = section
			o.group                = group
			o.local_name           = local_name
			o.international_name   = international_name
			o.local_symbol         = local_symbol
			o.international_symbol = international_symbol
			o.state                = state
			o.modified             = timezone.now()
			o.save()
		except OKEI.DoesNotExist:
			o = self.take(
				code                 = code,
				full_name            = full_name,
				section              = section,
				group                = group,
				local_name           = local_name,
				international_name   = international_name,
				local_symbol         = local_symbol,
				international_symbol = international_symbol,
				state                = state)
		return o



class OKEI(models.Model):
	'Единицы измерения'

	code                 = models.CharField(max_length = 10, unique = True)
	full_name            = models.TextField(null = True, default = None)
	local_name           = models.TextField(null = True, default = None)
	international_name   = models.TextField(null = True, default = None)
	local_symbol         = models.TextField(null = True, default = None)
	international_symbol = models.TextField(null = True, default = None)
	state                = models.BooleanField(default = True)
	created              = models.DateTimeField(default = timezone.now)
	modified             = models.DateTimeField(default = timezone.now)

	section              = models.ForeignKey(OKEISection, null = True, default = None)
	group                = models.ForeignKey(OKEIGroup, null = True, default = None)

	objects              = OKEIManager()

	def __str__(self):
		return "{}".format(self.full_name)

	class Meta:
		ordering = ['code']



class KOSGUManager(models.Manager):


	def take(self, code, name = None, parent = None, state = True):
		try:
			o = self.get(code = code)
		except KOSGU.DoesNotExist:
			o          = KOSGU()
			o.code     = code[:10]
			o.name     = name
			o.parent   = parent
			o.state    = state
			o.save()
		return o


	def update(self, code, name = None, parent = None, state = True):
		try:
			o             = self.get(code = code)
			o.name        = name
			o.parent      = parent
			o.state       = state
			o.modified    = timezone.now()
			o.save()
		except KOSGU.DoesNotExist:
			o = self.take(
				code   = code,
				name   = name,
				parent = parent,
				state  = state)
		return o



class KOSGU(models.Model):
	'Операции сектора государственного управления'

	code        = models.CharField(max_length = 10, unique = True)
	name        = models.TextField(null = True, default = None)
	state       = models.BooleanField(default = True)
	created     = models.DateTimeField(default = timezone.now)
	modified    = models.DateTimeField(default = timezone.now)

	parent      = models.ForeignKey('self', null = True, default = None)

	objects     = KOSGUManager()

	def __str__(self):
		return "{}".format(self.code)

	class Meta:
		ordering = ['code']



class OKOPFManager(models.Manager):

	def take(self, code, full_name = None, singular_name = None, parent = None, state = True):
		try:
			o = self.get(code = code)
		except OKOPF.DoesNotExist:
			o               = OKOPF()
			o.code          = code[:10]
			o.full_name     = full_name
			o.singular_name = singular_name
			o.parent        = parent
			o.state         = state
			o.save()
		return o

	def update(self, code, full_name = None, singular_name = None, parent = None, state = True):
		try:
			o               = self.get(code = code)
			o.full_name     = full_name
			o.singular_name = singular_name
			o.parent        = parent
			o.state         = state
			o.modified      = timezone.now()
			o.save()
		except OKOPF.DoesNotExist:
			o = self.take(
				code          = code,
				full_name     = full_name,
				singular_name = singular_name,
				parent        = parent,
				state         = state)
		return o



class OKOPF(models.Model):

	code          = models.CharField(max_length = 10, unique = True)
	full_name     = models.TextField(null = True, default = None)
	singular_name = models.TextField(null = True, default = None)
	state         = models.BooleanField(default = True)
	created       = models.DateTimeField(default = timezone.now)
	modified      = models.DateTimeField(default = timezone.now)

	parent        = models.ForeignKey('self', null = True, default = None)

	objects       = OKOPFManager()

	def __str__(self):
		return "{} {}".format(self.code, self.full_name)

	class Meta:
		ordering = ['code']



class OKPDManager(models.Manager):


	def take(self, id, code = None, name = None, parent = None, state = True):
		try:
			o = self.get(id = id)
		except OKPD.DoesNotExist:
			o          = OKPD()
			o.id       = id
			o.code     = code
			o.name     = name
			o.parent   = parent
			o.state    = state
			o.save()
		return o


	def update(self, id, code = None, name = None, parent = None, state = True):
		try:
			o          = self.get(id = id)
			o.code     = code
			o.name     = name
			o.parent   = parent
			o.state    = state
			o.modified = timezone.now()
			o.save()
		except OKPD.DoesNotExist:
			o = self.take(
				id     = id,
				code   = code,
				name   = name,
				parent = parent,
				state  = state)
		return o



class OKPD(models.Model):

	id       = models.IntegerField(primary_key = True, editable = False)
	code     = models.CharField(max_length = 50, null = True, default = None, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField(default = timezone.now)
	modified = models.DateTimeField(default = timezone.now)

	parent   = models.ForeignKey('self', null = True, default = None)

	objects  = OKPDManager()

	def __str__(self):
		return "{}".format(self.code)

	class Meta:
		ordering = ['code']



class OKPD2Manager(models.Manager):


	def take(self, id, code = None, name = None, parent = None, state = True):
		try:
			o = self.get(id = id)
		except OKPD2.DoesNotExist:
			o          = OKPD2()
			o.id       = id
			o.code     = code
			o.name     = name
			o.parent   = parent
			o.state    = state
			o.save()
		return o


	def update(self, id, code = None, name = None, parent = None, state = True):
		try:
			o          = self.get(id = id)
			o.code     = code
			o.name     = name
			o.parent   = parent
			o.state    = state
			o.modified = timezone.now()
			o.save()
		except OKPD2.DoesNotExist:
			o = self.take(
				id     = id,
				code   = code,
				name   = name,
				parent = parent,
				state  = state)
		return o



class OKPD2(models.Model):

	id       = models.IntegerField(primary_key = True, editable = False)
	code     = models.CharField(max_length = 50, null = True, default = None, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField(default = timezone.now)
	modified = models.DateTimeField(default = timezone.now)

	parent   = models.ForeignKey('self', null = True, default = None)

	objects  = OKPD2Manager()

	def __str__(self):
		return "{}".format(self.code)

	class Meta:
		ordering = ['code']



class OKTMOManager(models.Manager):


	def take(self, code, name = None, parent = None, state = True):
		try:
			o = self.get(code = code)
		except OKTMO.DoesNotExist:
			o          = OKTMO()
			o.code     = code
			o.name     = name
			o.parent   = parent
			o.state    = state
			o.save()
		return o


	def update(self, code, name = None, parent = None, state = True):
		try:
			o          = self.get(code = code)
			o.name     = name
			o.parent   = parent
			o.state    = state
			o.modified = timezone.now()
			o.save()
		except OKTMO.DoesNotExist:
			o = self.take(
				code   = code,
				name   = name,
				parent = parent,
				state  = state)
		return o



class OKTMO(models.Model):

	code     = models.CharField(max_length = 20, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField(default = timezone.now)
	modified = models.DateTimeField(default = timezone.now)

	parent   = models.ForeignKey('self', null = True, default = None)

	objects       = OKTMOManager()

	def __str__(self):
		return "{}".format(self.code)

	class Meta:
		ordering = ['code']



class OKVEDSectionManager(models.Manager):


	def take(self, name, state = True):
		try:
			o = self.get(name = name)
		except OKVEDSection.DoesNotExist:
			o          = OKVEDSection()
			o.name     = name[:100]
			o.state    = state
			o.save()
		return o

	def update(self, name, state = True):
		try:
			o          = self.get(name = name)
			o.state    = state
			o.modified = timezone.now()
			o.save()
		except OKVEDSection.DoesNotExist:
			o = self.take(
				name  = name,
				state = state)
		return o



class OKVEDSection(models.Model):

	name     = models.CharField(max_length = 100, unique = True)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField(default = timezone.now)
	modified = models.DateTimeField(default = timezone.now)

	objects  = OKVEDSectionManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['name']



class OKVEDSubSectionManager(models.Manager):


	def take(self, name, state = True):
		try:
			o = self.get(name = name)
		except OKVEDSubSection.DoesNotExist:
			o          = OKVEDSubSection()
			o.name     = name[:100]
			o.state    = state
			o.save()
		return o


	def update(self, name, state = True):
		try:
			o          = self.get(name = name)
			o.state    = state
			o.modified = timezone.now()
			o.save()
		except OKVEDSubSection.DoesNotExist:
			o = self.take(
				name  = name,
				state = state)
		return o



class OKVEDSubSection(models.Model):

	name     = models.CharField(max_length = 100, unique = True)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField(default = timezone.now)
	modified = models.DateTimeField(default = timezone.now)

	objects  = OKVEDSubSectionManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['name']



class OKVEDManager(models.Manager):

	def take(self, id, code = None, section = None, subsection = None, parent = None, name = None, state = True):
		try:
			o = self.get(id = id)
		except OKVED.DoesNotExist:
			o            = OKVED()
			o.id         = id
			o.code       = code
			o.section    = section
			o.subsection = subsection
			o.parent     = parent
			o.name       = name
			o.state      = state
			o.save()
		return o

	def update(self, id, code = None, section = None, subsection = None, parent = None, name = None, state = True):
		try:
			o            = self.get(id = id)
			o.code       = code
			o.section    = section
			o.subsection = subsection
			o.parent     = parent
			o.name       = name
			o.state      = state
			o.modified   = timezone.now()
			o.save()
		except OKVED.DoesNotExist:
			o = self.take(
				id         = id,
				code       = code,
				section    = section,
				subsection = subsection,
				parent     = parent,
				name       = name,
				state      = state)
		return o



class OKVED(models.Model):

	id            = models.IntegerField(primary_key = True, editable = False)
	code          = models.CharField(max_length = 100, null = True, default = None)
	name          = models.TextField(null = True, default = None)
	state         = models.BooleanField(default = True)
	created       = models.DateTimeField(default = timezone.now)
	modified      = models.DateTimeField(default = timezone.now)

	section       = models.ForeignKey(OKVEDSection, null = True, default = None)
	subsection    = models.ForeignKey(OKVEDSubSection, null = True, default = None)
	parent        = models.ForeignKey('self', null = True, default = None)

	objects       = OKVEDManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class OKVED2SectionManager(models.Manager):


	def take(self, name, state = True):
		try:
			o = self.get(name = name)
		except OKVED2Section.DoesNotExist:
			o          = OKVED2Section()
			o.name     = name[:100]
			o.state    = state
			o.save()
		return o

	def update(self, name, state = True):
		try:
			o          = self.get(name = name)
			o.state    = state
			o.modified = timezone.now()
			o.save()
		except OKVED2Section.DoesNotExist:
			o = self.take(
				name  = name,
				state = state)
		return o



class OKVED2Section(models.Model):

	name     = models.CharField(max_length = 100, unique = True)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField(default = timezone.now)
	modified = models.DateTimeField(default = timezone.now)

	objects  = OKVED2SectionManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['name']



class OKVED2Manager(models.Manager):

	def take(self, code, oos_id = None, section = None, parent = None, name = None, comment = None, state = True):
		try:
			o = self.get(code = code)
		except OKVED2.DoesNotExist:
			o            = OKVED2()
			o.code       = code
			o.oos_id     = oos_id
			o.section    = section
			o.parent     = parent
			o.name       = name
			o.comment    = comment
			o.state      = state
			o.save()
		return o

	def update(self, code, oos_id = None, section = None, parent = None, name = None, comment = None, state = True):
		try:
			o            = self.get(code = code)
			o.oos_id     = oos_id
			o.section    = section
			o.parent     = parent
			o.name       = name
			o.comment    = comment
			o.state      = state
			o.modified   = timezone.now()
			o.save()
		except OKVED2.DoesNotExist:
			o = self.take(
				code       = code,
				oos_id     = oos_id,
				section    = section,
				parent     = parent,
				name       = name,
				comment    = comment,
				state      = state)
		return o



class OKVED2(models.Model):

	code          = models.CharField(max_length = 100, null = True, default = None, unique = True)
	oos_id        = models.CharField(max_length = 10, null = True, default = None)
	name          = models.TextField(null = True, default = None)
	comment       = models.TextField(null = True, default = None)
	state         = models.BooleanField(default = True)
	created       = models.DateTimeField(default = timezone.now)
	modified      = models.DateTimeField(default = timezone.now)

	section       = models.ForeignKey(OKVED2Section, null = True, default = None)
	parent        = models.ForeignKey('self', null = True, default = None)

	objects       = OKVED2Manager()

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
	created  = models.DateTimeField(default = timezone.now)
	modified = models.DateTimeField(default = timezone.now)

	objects  = BudgetManager()

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
			o.save()
		return o



class SubsystemType(models.Model):

	code     = models.CharField(max_length = 20, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField(default = timezone.now)
	modified = models.DateTimeField(default = timezone.now)

	objects  = SubsystemTypeManager()

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
	state          = models.BooleanField(default = True)
	created        = models.DateTimeField(default = timezone.now)
	modified       = models.DateTimeField(default = timezone.now)

	subsystem_type = models.ForeignKey(SubsystemType, null = True, default = None)

	objects        = BudgetTypeManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class KBKBudgetManager(models.Manager):

	def take(self, code, budget = None, start_date = None, end_date = None, state = True):
		try:
			o = self.get(code = code)
		except KBKBudget.DoesNotExist:
			o            = KBKBudget()
			o.code       = code
			o.budget     = budget
			o.start_date = start_date
			o.end_date   = end_date
			o.state      = state
			o.save()
		return o

	def update(self, code, budget = None, start_date = None, end_date = None, state = True):
		try:
			o            = self.get(code = code)
			o.budget     = budget
			o.start_date = start_date
			o.end_date   = end_date
			o.state      = state
			o.modified   = timezone.now()
			o.save()
		except KBKBudget.DoesNotExist:
			o = self.take(
				code       = code,
				budget     = budget,
				start_date = start_date,
				end_date   = end_date,
				state      = state)
		return o



class KBKBudget(models.Model):

	id         = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	code       = models.CharField(max_length = 50, unique = True)
	start_date = models.DateTimeField(null = True, default = None)
	end_date   = models.DateTimeField(null = True, default = None)
	state      = models.BooleanField(default = True)
	created    = models.DateTimeField(default = timezone.now)
	modified   = models.DateTimeField(default = timezone.now)

	budget   = models.ForeignKey(Budget, null = True, default = None)

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
			o          = OKOGU()
			o.code     = code
			o.name     = name
			o.state    = state
			o.save()
		return o



class OKOGU(models.Model):

	code     = models.CharField(max_length = 20, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField(default = timezone.now)
	modified = models.DateTimeField(default = timezone.now)

	objects  = OKOGUManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class AddressManager(models.Manager):


	def take(self, address, state = True):
		if not address:
			return None
		try:
			o = self.get(address = address)
		except Address.DoesNotExist:
			o         = Address()
			o.address = address
			o.state   = state
			o.save()
		return o



class Address(models.Model):

	address  = models.TextField(unique = True)
	state    = models.BooleanField(default = True)

	objects  = AddressManager()

	def __str__(self):
		return "{}".format(self.address)

	class Meta:
		ordering = ['address']



class EmailManager(models.Manager):


	def take(self, email, state = True):
		if not email:
			return None
		try:
			o = self.get(email = email)
		except Email.DoesNotExist:
			o       = Email()
			o.email = email[:256]
			o.state = state
			o.save()
		return o



class Email(models.Model):

	email    = models.CharField(max_length = 256, unique = True)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField(default = timezone.now)
	modified = models.DateTimeField(default = timezone.now)

	objects  = EmailManager()

	def __str__(self):
		return "{}".format(self.email)

	class Meta:
		ordering = ['email']



class PhoneManager(models.Manager):

	def take(self, phone, state = True):
		if not phone:
			return None
		try:
			o = self.get(phone = phone)
		except Phone.DoesNotExist:
			o       = Phone()
			o.phone = phone[:128]
			o.state = state
			o.save()
		return o



class Phone(models.Model):

	phone    = models.CharField(max_length = 128, unique = True)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField(default = timezone.now)
	modified = models.DateTimeField(default = timezone.now)

	objects  = PhoneManager()

	def __str__(self):
		return "{}".format(self.phone)

	class Meta:
		ordering = ['phone']



class PersonManager(models.Manager):


	def take(self, first_name, middle_name, last_name, **kwargs):

		os = self.filter(first_name = first_name, middle_name = middle_name, last_name = last_name)

		for o in os:

			for email in o.emails.all():
				if email in kwargs.get('emails', []):
					return o

			for phone in o.phones.all():
				if phone in kwargs.get('phones', []):
					return o

			for fax in o.faxes.all():
				if fax in kwargs.get('faxes', []):
					return o

		o = Person()

		try:
			o.first_name = first_name[:128]
		except Exception:
			o.first_name = ''

		try:
			o.middle_name = middle_name[:128]
		except Exception:
			o.middle_name = ''

		try:
			o.last_name = last_name[:128]
		except Exception:
			o.last_name = ''

		o.state       = kwargs.get('state', True)
		o.save()

		for email in kwargs.get('emails', []):

			if email:

				try:
					o.emails.get(email = email)
				except Exception:
					e = PersonToEmail()
					e.person = o
					e.email  = email
					e.save()

		for phone in kwargs.get('phones', []):

			if phone:

				try:
					o.phones.get(phone = phone)
				except Exception:
					e = PersonToPhone()
					e.person = o
					e.phone  = phone
					e.save()

		for fax in kwargs.get('faxes', []):

			if fax:

				try:
					o.faxes.get(fax = fax)
				except Exception:
					e = PersonToFax()
					e.person = o
					e.fax    = fax
					e.save()

		return o



class Person(models.Model):

	first_name  = models.CharField(max_length = 128)
	middle_name = models.CharField(max_length = 128)
	last_name   = models.CharField(max_length = 128)
	position    = models.CharField(max_length = 128, null = True, default = None)
	description = models.TextField(null = True, default = None)

	emails      = models.ManyToManyField(Email, related_name = 'person_email', through = 'PersonToEmail', through_fields = ('person', 'email'))
	phones      = models.ManyToManyField(Phone, related_name = 'person_phone', through = 'PersonToPhone', through_fields = ('person', 'phone'))
	faxes       = models.ManyToManyField(Phone, related_name = 'person_fax',   through = 'PersonToFax',   through_fields = ('person', 'fax'))

	state       = models.BooleanField(default = True)
	created     = models.DateTimeField(default = timezone.now)
	modified    = models.DateTimeField(default = timezone.now)

	objects = PersonManager()

	def __str__(self):
		return "{} {} {}".format(self.first_name, self.middle_name, self.last_name)

	class Meta:
		ordering = ['first_name', 'middle_name', 'last_name']



class PersonToEmail(models.Model):

	id     = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	person = models.ForeignKey(Person, on_delete = models.CASCADE)
	email  = models.ForeignKey(Email,  on_delete = models.CASCADE)

	class Meta:
		db_table = 'tenders_person_to_email'



class PersonToPhone(models.Model):

	id     = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	person = models.ForeignKey(Person, on_delete = models.CASCADE)
	phone  = models.ForeignKey(Phone,  on_delete = models.CASCADE)

	class Meta:
		db_table = 'tenders_person_to_phone'



class PersonToFax(models.Model):

	id     = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	person = models.ForeignKey(Person, on_delete = models.CASCADE)
	fax    = models.ForeignKey(Phone,  on_delete = models.CASCADE)

	class Meta:
		db_table = 'tenders_person_to_fax'



class BankManager(models.Manager):

	def take(self, bik, name = None, address = None, state = True):
		try:
			o = self.get(bik = bik)
		except Bank.DoesNotExist:
			o         = Bank()
			o.bik     = bik
			o.name    = name
			o.address = address
			o.state   = state
			o.save()
		return o



class Bank(models.Model):

	bik      = models.CharField(max_length = 10, unique = True)
	name     = models.TextField(null = True, default = None)
	address  = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField(default = timezone.now)
	modified = models.DateTimeField(default = timezone.now)

	objects  = BankManager()

	def __str__(self):
		return "{} {}".format(self.bik, self.name)

	class Meta:
		ordering = ['bik']





class AccountManager(models.Manager):

	def take(self, payment_account, corr_account, personal_account, bank, state = True):
		try:
			o = self.get(payment_account = payment_account, corr_account = corr_account,
					personal_account = personal_account, bank = bank)
		except Account.DoesNotExist:
			o       = Account()
			o.payment_account  = payment_account
			o.corr_account     = corr_account
			o.personal_account = personal_account
			o.bank             = bank
			o.state            = state
			o.save()
		return o



class Account(models.Model):

	payment_account  = models.CharField(max_length = 32, null = True, default = None)
	corr_account     = models.CharField(max_length = 32, null = True, default = None)
	personal_account = models.CharField(max_length = 32, null = True, default = None)
	bank             = models.ForeignKey(Bank, null = True, default = None)
	state            = models.BooleanField(default = True)
	created          = models.DateTimeField(default = timezone.now)
	modified         = models.DateTimeField(default = timezone.now)

	objects = AccountManager()

	def __str__(self):
		return "{}".format(self.payment_account)

	class Meta:
		ordering = ['payment_account']



class OrganisationRoleManager(models.Manager):

	def take(self, code, name = None, state = True):
		try:
			o = self.get(code = code)
		except OrganisationRole.DoesNotExist:
			o       = OrganisationRole()
			o.code  = code[:20]
			o.name  = name
			o.state = state
			o.save()
		return o



class OrganisationRole(models.Model):

	code     = models.CharField(max_length = 20, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True)
	created  = models.DateTimeField(default = timezone.now)
	modified = models.DateTimeField(default = timezone.now)

	objects  = OrganisationRoleManager()

	def __str__(self):
		return "{}".format(self.code)

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
	created     = models.DateTimeField(default = timezone.now)
	modified    = models.DateTimeField(default = timezone.now)

	objects     = OrganisationTypeManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class OrganisationManager(models.Manager):


	def take(self, reg_number, **kwargs):
		try:
			o = self.get(reg_number = reg_number)
		except Organisation.DoesNotExist:
			o                   = Organisation()
			o.reg_number        = reg_number

			if kwargs.get('name', None):
				o.name = kwargs.get('name', None)
			else:
				o.name = kwargs.get('full_name', None)

			o.short_name        = kwargs.get('short_name', None)
			o.full_name         = kwargs.get('full_name', None)
			o.inn               = kwargs.get('inn', None)
			o.kpp               = kwargs.get('kpp', None)
			o.ogrn              = kwargs.get('ogrn', None)
			o.okpo              = kwargs.get('okpo', None)
			o.factual_address   = kwargs.get('factual_address', None)
			o.postal_address    = kwargs.get('postal_address', None)
			o.email             = kwargs.get('email', None)
			o.phone             = kwargs.get('phone', None)
			o.fax               = kwargs.get('fax', None)
			o.contact_person    = kwargs.get('contact_person', None)
			o.head_agency       = kwargs.get('head_agency', None)
			o.ordering_agency   = kwargs.get('ordering_agency', None)
			o.okopf             = kwargs.get('okopf', None)
			o.okogu             = kwargs.get('okogu', None)
			o.organisation_role = kwargs.get('organisation_role', None)
			o.organisation_type = kwargs.get('organisation_type', None)
			o.oktmo             = kwargs.get('oktmo', None)
			o.state             = kwargs.get('state', True)
			o.register          = kwargs.get('register', True)

			o.save()

			for account in kwargs.get('accounts', []):
				if account:
					try:
						o.accounts.get(account = account)
					except Exception:
						e = OrganisationToAccount()
						e.organisation = o
						e.account      = account
						e.save()

			for budget in kwargs.get('budgets', []):
				if budget:
					try:
						o.budgets.get(budget = budget)
					except Exception:
						e = OrganisationToBudget()
						e.organisation = o
						e.budget       = budget
						e.save()

			for okved in kwargs.get('okveds', []):
				if okved:
					try:
						o.okveds.get(okved = okved)
					except Exception:
						e = OrganisationToOKVED()
						e.organisation = o
						e.okved        = okved
						e.save()

		return o


	def update(self, reg_number, **kwargs):

		try:
			o = self.get(reg_number = reg_number)

			if kwargs.get('name', None):
				o.name = kwargs.get('name', None)
			else:
				o.name = kwargs.get('full_name', None)

			o.short_name        = kwargs.get('short_name', None)
			o.full_name         = kwargs.get('full_name', None)
			o.inn               = kwargs.get('inn', None)
			o.kpp               = kwargs.get('kpp', None)
			o.ogrn              = kwargs.get('ogrn', None)
			o.okpo              = kwargs.get('okpo', None)

			o.factual_address   = kwargs.get('factual_address', None)
			o.postal_address    = kwargs.get('postal_address', None)
			o.email             = kwargs.get('email', None)
			o.phone             = kwargs.get('phone', None)
			o.fax               = kwargs.get('fax', None)
			o.contact_person    = kwargs.get('contact_person', None)
			o.head_agency       = kwargs.get('head_agency', None)
			o.ordering_agency   = kwargs.get('ordering_agency', None)
			o.okopf             = kwargs.get('okopf', None)
			o.okogu             = kwargs.get('okogu', None)
			o.organisation_role = kwargs.get('organisation_role', None)
			o.organisation_type = kwargs.get('organisation_type', None)
			o.oktmo             = kwargs.get('oktmo', None)
			o.state             = kwargs.get('state', True)
			o.register          = kwargs.get('register', True)

			o.save()

			o.accounts.clear()
			for account in kwargs.get('accounts', []):
				if account:
					try:
						o.accounts.get(account = account)
					except Exception:
						e = OrganisationToAccount()
						e.organisation = o
						e.account      = account
						e.save()

			o.budgets.clear()
			for budget in kwargs.get('budgets', []):
				if budget:
					try:
						o.budgets.get(budget = budget)
					except Exception:
						e = OrganisationToBudget()
						e.organisation = o
						e.budget       = budget
						e.save()

			o.okveds.clear()
			for okved in kwargs.get('okveds', []):
				if okved:
					try:
						o.okveds.get(okved = okved)
					except Exception:
						e = OrganisationToOKVED()
						e.organisation = o
						e.okved        = okved
						e.save()

		except Organisation.DoesNotExist:
			o = self.take(reg_number, **kwargs)
		return o



class Organisation(models.Model):

	reg_number        = models.CharField(max_length = 20, unique = True)
	name              = models.TextField(null = True, default = None)
	short_name        = models.TextField(null = True, default = None)
	full_name         = models.TextField(null = True, default = None)

	inn               = models.CharField(max_length = 20, null = True, default = None)
	kpp               = models.CharField(max_length = 20, null = True, default = None)
	ogrn              = models.CharField(max_length = 20, null = True, default = None)
	okpo              = models.CharField(max_length = 20, null = True, default = None)

	factual_address   = models.ForeignKey(Address,          related_name = 'organisation_factual_address', null = True, default = None)
	postal_address    = models.ForeignKey(Address,          related_name = 'organisation_postal_address',  null = True, default = None)
	email             = models.ForeignKey(Email,            related_name = 'organisation_email',           null = True, default = None)
	phone             = models.ForeignKey(Phone,            related_name = 'organisation_phone',           null = True, default = None)
	fax               = models.ForeignKey(Phone,            related_name = 'organisation_fax',             null = True, default = None)

	contact_person    = models.ForeignKey(Person,           related_name = 'organisation_contact_person',  null = True, default = None)
	head_agency       = models.ForeignKey('self',           related_name = 'organisation_head_agency',     null = True, default = None)
	ordering_agency   = models.ForeignKey('self',           related_name = 'organisation_ordering_agency', null = True, default = None)
	okopf             = models.ForeignKey(OKOPF,            related_name = 'organisation_okopf',           null = True, default = None)
	okogu             = models.ForeignKey(OKOGU,            related_name = 'organisation_okogu',           null = True, default = None)
	organisation_role = models.ForeignKey(OrganisationRole, related_name = 'organisation_role',            null = True, default = None)
	organisation_type = models.ForeignKey(OrganisationType, related_name = 'organisation_type',            null = True, default = None)
	oktmo             = models.ForeignKey(OKTMO,            related_name = 'organisation_oktmo',           null = True, default = None)

	accounts          = models.ManyToManyField(Account, through = 'OrganisationToAccount', through_fields = ('organisation', 'account'))
	budgets           = models.ManyToManyField(Budget,  through = 'OrganisationToBudget',  through_fields = ('organisation', 'budget'))
	okveds            = models.ManyToManyField(OKVED,   through = 'OrganisationToOKVED',   through_fields = ('organisation', 'okved'))

	state             = models.BooleanField(default = True)
	register          = models.BooleanField(default = True)

	created           = models.DateTimeField(default = timezone.now)
	modified          = models.DateTimeField(default = timezone.now)

	objects           = OrganisationManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['reg_number']



class OrganisationToAccount(models.Model):

	id           = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	organisation = models.ForeignKey(Organisation, on_delete = models.CASCADE)
	account      = models.ForeignKey(Account, on_delete = models.CASCADE)

	class Meta:
		db_table = 'tenders_organisation_to_account'



class OrganisationToBudget(models.Model):

	id           = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	organisation = models.ForeignKey(Organisation, on_delete = models.CASCADE)
	budget       = models.ForeignKey(Budget, on_delete = models.CASCADE)

	class Meta:
		db_table = 'tenders_organisation_to_budget'



class OrganisationToOKVED(models.Model):

	id           = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	organisation = models.ForeignKey(Organisation, on_delete = models.CASCADE)
	okved        = models.ForeignKey(OKVED, on_delete = models.CASCADE)

	class Meta:
		db_table = 'tenders_organisation_to_okved'



class PlacingWayManager(models.Manager):


	def take(self, id, **kwargs):
		try:
			o = self.get(id = id)
		except Exception:
			o = PlacingWay()
			o.id              = id
			o.code            = kwargs.get('code', None)
			o.name            = kwargs.get('name', None)
			o.type_code       = kwargs.get('type_code', None)
			o.subsystem_type  = kwargs.get('subsystem_type', None)
			o.state           = kwargs.get('state', True)
			o.save()
		return o


	def update(self, id, **kwargs):
		try:
			o = self.get(id = id)
			o.code            = kwargs.get('code', None)
			o.name            = kwargs.get('name', None)
			o.type_code       = kwargs.get('type_code', None)
			o.subsystem_type  = kwargs.get('subsystem_type', None)
			o.state           = kwargs.get('state', True)
			o.modified        = timezone.now()
			o.save()
		except PlacingWay.DoesNotExist:
			o = self.take(id, **kwargs)
		return o



class PlacingWay(models.Model):

	id              = models.IntegerField(primary_key = True, editable = False)
	code            = models.TextField(null = True, default = None)
	name            = models.TextField(null = True, default = None)
	type_code       = models.CharField(max_length = 20, null = True, default = None)

	subsystem_type  = models.ForeignKey(SubsystemType, null = True, default = None)

	state           = models.BooleanField(default = True)
	created         = models.DateTimeField(default = timezone.now)
	modified        = models.DateTimeField(default = timezone.now)

	objects         = PlacingWayManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']


class PlanPositionChangeReasonManager(models.Manager):


	def take(self, id, **kwargs):
		try:
			o = self.get(id = id)
		except Exception:
			o                 = PlanPositionChangeReason()
			o.id              = id
			o.name            = kwargs.get('name', None)
			o.description     = kwargs.get('description', None)
			o.state           = kwargs.get('state', True)
			o.save()
		return o


	def update(self, id, **kwargs):
		try:
			o = self.get(id = id)
			o.name            = kwargs.get('name', None)
			o.description     = kwargs.get('description', None)
			o.state           = kwargs.get('state', True)
			o.modified        = timezone.now()
			o.save()
		except PlanPositionChangeReason.DoesNotExist:
			o = self.take(id, **kwargs)
		return o



class PlanPositionChangeReason(models.Model):

	id          = models.IntegerField(primary_key = True, editable = False)
	name        = models.TextField(null = True, default = None)
	description = models.TextField(null = True, default = None)
	state       = models.BooleanField(default = True)
	created     = models.DateTimeField(default = timezone.now)
	modified    = models.DateTimeField(default = timezone.now)

	objects     = PlanPositionChangeReasonManager()

	def __str__(self):
		return "{} {}".format(self.id, self.name)

	class Meta:
		ordering = ['id']



class ContractModificationReasonManager(models.Manager):


	def take(self, code, **kwargs):
		try:
			o = self.get(code = code)
		except Exception:
			o       = ContractModificationReason()
			o.code  = code
			o.name  = kwargs.get('name', None)
			o.state = kwargs.get('state', True)
			o.save()
		return o


	def update(self, code, **kwargs):
		o          = self.take(code, **kwargs)
		o.name     = kwargs.get('name', None)
		o.state    = kwargs.get('state', True)
		o.modified = timezone.now()
		o.save()
		return o



class ContractModificationReason(models.Model):

	code        = models.TextField(unique = True)
	name        = models.TextField(null = True, default = None)
	state       = models.BooleanField(default = True)
	created     = models.DateTimeField(default = timezone.now)
	modified    = models.DateTimeField(default = timezone.now)

	objects     = ContractModificationReasonManager()

	def __str__(self):
		return "{} {}".format(self.id, self.name)

	class Meta:
		ordering = ['id']







class KVRManager(models.Manager):


	def take(self, code, **kwargs):
		try:
			o = self.get(code = code)
		except Exception:
			o       = KVR()
			o.code  = code
			o.name  = kwargs.get('name', None)
			o.state = kwargs.get('state', True)
			o.save()
		return o


	def update(self, code, **kwargs):
		o          = self.take(code, **kwargs)
		o.name     = kwargs.get('name', None)
		o.state    = kwargs.get('state', True)
		o.save()
		return o



class KVR(models.Model):

	code        = models.TextField(unique = True)
	name        = models.TextField(null = True, default = None)
	state       = models.BooleanField(default = True)

	objects     = KVRManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class PlanManager(models.Manager):


	def take(self, id, **kwargs):
		try:
			o = self.get(id = id)
		except Exception:
			o = Plan()
			o.id             = id
			o.number         = kwargs.get('number', None)
			o.year           = kwargs.get('year', None)
			o.version        = kwargs.get('version', None)
			o.description    = kwargs.get('description', None)
			o.url            = kwargs.get('url', None)
			o.region         = kwargs.get('region', None)
			o.owner          = kwargs.get('owner', None)
			o.customer       = kwargs.get('customer', None)
			o.contact_person = kwargs.get('contact_person', None)
			o.state          = kwargs.get('state', True)
			o.created        = kwargs.get('created', timezone.now())
			o.confirmed      = kwargs.get('confirmed', timezone.now())
			o.published      = kwargs.get('published', timezone.now())
			o.save()

			self.filter(number = o.number, version__lt = o.version).update(state = False)

		return o


	def update(self, id, **kwargs):
		o = self.take(id, **kwargs)
		o.number         = kwargs.get('number', None)
		o.year           = kwargs.get('year', None)
		o.version        = kwargs.get('version', None)
		o.description    = kwargs.get('description', None)
		o.url            = kwargs.get('url', None)
		o.region         = kwargs.get('region', None)
		o.owner          = kwargs.get('owner', None)
		o.customer       = kwargs.get('customer', None)
		o.contact_person = kwargs.get('contact_person', None)
		o.state          = kwargs.get('state', True)
		o.created        = kwargs.get('created', timezone.now())
		o.confirmed      = kwargs.get('confirmed', timezone.now())
		o.published      = kwargs.get('published', timezone.now())
		o.modified       = timezone.now()
		o.save()

		self.filter(number = o.number, version__lt = o.version).update(state = False)

		return o



class Plan(models.Model):

	id             = models.IntegerField(primary_key = True, editable = False)
	number         = models.CharField(max_length = 20)
	year           = models.IntegerField(null = True, default = None)
	version        = models.IntegerField(null = True, default = None)
	description    = models.TextField(null = True, default = None)
	url            = models.TextField(null = True, default = None)

	state          = models.BooleanField(default = True)
	created        = models.DateTimeField(default = timezone.now)
	confirmed      = models.DateTimeField(default = timezone.now)
	published      = models.DateTimeField(default = timezone.now)
	modified       = models.DateTimeField(default = timezone.now)

	region         = models.ForeignKey(Region,       related_name = 'tenderplan_region',         null = True, default = None)
	owner          = models.ForeignKey(Organisation, related_name = 'tenderplan_owner',          null = True, default = None)
	customer       = models.ForeignKey(Organisation, related_name = 'tenderplan_customer',       null = True, default = None)
	contact_person = models.ForeignKey(Person,       related_name = 'tenderplan_contact_person', null = True, default = None)

	objects        = PlanManager()

	def __str__(self):
		return "{} {} ".format(self.year, self.customer)

	class Meta:
		ordering = ['year', 'number', 'version']



class ProductManager(models.Manager):

	def take(self, okpd, okpd2, name):
		try:
			o = self.get(okpd = okpd, okpd2 = okpd2, name = name)
		except Exception:
			o = Product()
			o.okpd  = okpd
			o.okpd2 = okpd2
			o.name  = name
			o.save()
		return o



class Product(models.Model):

	id    = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	okpd  = models.ForeignKey(OKPD,  null = True, default = None)
	okpd2 = models.ForeignKey(OKPD2, null = True, default = None)
	name  = models.TextField(null = True, default = None)

	objects = ProductManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['name']
		unique_together = ('okpd', 'okpd2', 'name')



class PlanPositionManager(models.Manager):

	def take(self, plan, number, **kwargs):
		try:
			o = self.get(plan = plan, number = number)
		except Exception:
			o = PlanPosition()
			o.plan            = plan
			o.number          = number
			o.name            = kwargs.get('name', None)
			o.purchase_month  = kwargs.get('purchase_month', None)
			o.purchase_year   = kwargs.get('purchase_year', None)
			o.execution_month = kwargs.get('execution_month', None)
			o.execution_year  = kwargs.get('execution_year', None)
			o.max_price       = kwargs.get('max_price', None)
			o.currency        = kwargs.get('currency', None)
			o.placing_way     = kwargs.get('placing_way', None)
			o.change_reason   = kwargs.get('change_reason', None)

			o.save()

		return o

	def update(self, plan, number, **kwargs):
		o = self.take(plan, number, **kwargs)
		o.name            = kwargs.get('name', None)
		o.purchase_month  = kwargs.get('purchase_month', None)
		o.purchase_year   = kwargs.get('purchase_year', None)
		o.execution_month = kwargs.get('execution_month', None)
		o.execution_year  = kwargs.get('execution_year', None)
		o.max_price       = kwargs.get('max_price', None)
		o.currency        = kwargs.get('currency', None)
		o.placing_way     = kwargs.get('placing_way', None)
		o.change_reason   = kwargs.get('change_reason', None)
		o.save()

		o.okveds.clear()
		for okved in kwargs.get('okveds', []):
			if okved:
				try:
					o.okveds.get(okved = okved)
				except Exception:
					e = PlanPositionToOKVED()
					e.plan_position = o
					e.okved = okved
					e.save()

		o.okveds2.clear()
		for okved2 in kwargs.get('okveds2', []):
			if okved2:
				try:
					o.okveds2.get(okved2 = okved2)
				except Exception:
					e = PlanPositionToOKVED2()
					e.plan_position = o
					e.okved2 = okved2
					e.save()

		return o



class PlanPosition(models.Model):

	id              = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	plan            = models.ForeignKey(Plan)
	number          = models.CharField(max_length = 50)
	name            = models.TextField(null = True, default = None)
	purchase_month  = models.IntegerField(null = True, default = None)
	purchase_year   = models.IntegerField(null = True, default = None)
	execution_month = models.IntegerField(null = True, default = None)
	execution_year  = models.IntegerField(null = True, default = None)
	max_price       = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)

	currency      = models.ForeignKey(Currency,                 null = True, default = None)
	placing_way   = models.ForeignKey(PlacingWay,               null = True, default = None)
	change_reason = models.ForeignKey(PlanPositionChangeReason, null = True, default = None)

	okveds   = models.ManyToManyField(OKVED,   through = 'PlanPositionToOKVED',   through_fields = ('plan_position', 'okved'))
	okveds2  = models.ManyToManyField(OKVED2,  through = 'PlanPositionToOKVED2',  through_fields = ('plan_position', 'okved2'))
	products = models.ManyToManyField(Product, through = 'PlanPositionToProduct', through_fields = ('plan_position', 'product'))

	objects = PlanPositionManager()

	def __str__(self):
		return "{} {}".format(self.number, self.name)

	def add_product(self, product, **kwargs):
		pass


class PlanPositionToOKVED(models.Model):

	id            = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	plan_position = models.ForeignKey(PlanPosition, on_delete = models.CASCADE)
	okved         = models.ForeignKey(OKVED, on_delete = models.CASCADE)

	class Meta:
		db_table = 'tenders_planposition_to_okved'



class PlanPositionToOKVED2(models.Model):

	id            = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	plan_position = models.ForeignKey(PlanPosition, on_delete = models.CASCADE)
	okved2        = models.ForeignKey(OKVED2, on_delete = models.CASCADE)

	class Meta:
		db_table = 'tenders_planposition_to_okved2'



class PlanPositionToProduct(models.Model):

	id            = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	plan_position = models.ForeignKey(PlanPosition, on_delete = models.CASCADE)
	product       = models.ForeignKey(Product, on_delete = models.CASCADE)
	requirement   = models.TextField(null = True, default = None)
	quantity      = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	okei          = models.ForeignKey(OKEI, null = True, default = None)
	price         = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	total         = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)

	def __str__(self):
		return "{} {}".format(self.product, self.quantity)

	class Meta:
		db_table = 'tenders_planposition_to_product'





#class PlanGraphPositionProductManager(models.Manager):

#	def take(self, position, number, okpd = None, name = None,
#			min_requirement = None, okei = None, max_sum = None, price = None,
#			quantity_undefined = None, quantity = None,
#			quantity_current_year = None, state = True):
#		try:
#			o = self.get(position = position, number = number)
#		except PlanGraphPositionProduct.DoesNotExist:
#			o                       = PlanGraphPositionProduct()
#			o.position              = position
#			o.number                = number
#			o.okpd                  = okpd
#			o.name                  = name
#			o.min_requirement       = min_requirement
#			o.okei                  = okei
#			o.max_sum               = max_sum
#			o.price                 = price
#			o.quantity_undefined    = quantity_undefined
#			o.quantity              = quantity
#			o.quantity_current_year = quantity_current_year
#			o.state                 = state
#			o.created               = timezone.now()
#			o.modified              = timezone.now()
#			o.save()
#		return o

#	def update(self, position, number, okpd = None, name = None,
#			min_requirement = None, okei = None, max_sum = None, price = None,
#			quantity_undefined = None, quantity = None,
#			quantity_current_year = None, state = True):
#		try:
#			o = self.get(position = position, number = number)
#			o.okpd                  = okpd
#			o.name                  = name
#			o.min_requirement       = min_requirement
#			o.okei                  = okei
#			o.max_sum               = max_sum
#			o.price                 = price
#			o.quantity_undefined    = quantity_undefined
#			o.quantity              = quantity
#			o.quantity_current_year = quantity_current_year
#			o.state                 = state
#			o.state             = state
#			o.modified          = timezone.now()
#			o.save()
#		except PlanGraphPositionProduct.DoesNotExist:
#			o = self.take(
#				position              = position,
#				number                = number,
#				okpd                  = okpd,
#				name                  = name,
#				min_requirement       = min_requirement,
#				okei                  = okei,
#				max_sum               = max_sum,
#				price                 = price,
#				quantity_undefined    = quantity_undefined,
#				quantity              = quantity,
#				quantity_current_year = quantity_current_year,
#				state                 = state)
#		return o


#class PlanGraphPositionProduct(models.Model):

#	position              = models.ForeignKey(PlanGraphPosition)
#	number                = models.IntegerField()
#	okpd                  = models.ForeignKey(OKPD, null = True, default = None)
#	name                  = models.TextField(null = True, default = None)
#	min_requipment        = models.TextField(null = True, default = None)
#	okei                  = models.ForeignKey(OKEI, null = True, default = None)
#	max_sum               = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
#	price                 = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
#	quantity_undefined    = models.BooleanField(default = True)
#	quantity              = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
#	quantity_current_year = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
#	state                 = models.BooleanField(default = True)
#	created               = models.DateTimeField()
#	modified              = models.DateTimeField()

#	objects               = PlanGraphPositionProductManager()

#	def __str__(self):
#		return "{}".format(self.name)

#	def _get_max_sum_str(self):

#		try:
#			max_sum  = self.max_sum
#			currency = self.position.currency
#		except: return '-'

#		if max_sum:
#			max_sum = '{:,}'.format(round(max_sum, 2))
#			max_sum = max_sum.replace(',', '\u00a0')
#			max_sum = max_sum.replace('.', ',')
#			max_sum = '{}\u00a0{}'.format(max_sum, currency.code)
#			return max_sum
#		else:
#			return '-'

#	max_sum_str = property(_get_max_sum_str)

#	def _get_price_str(self):

#		try:
#			price    = self.price
#			currency = self.position.currency
#		except: return '-'

#		if price:
#			price = '{:,}'.format(round(price, 2))
#			price = price.replace(',', '\u00a0')
#			price = price.replace('.', ',')
#			price = '{}\u00a0{}'.format(price, currency.code)
#			return price
#		else:
#			return '-'

#	price_str = property(_get_price_str)

#	def _get_quantity_str(self):

#		try:
#			quantity = self.quantity
#			unit     = self.okei
#		except: return '-'

#		if quantity:
#			quantity = '{:,}'.format(round(quantity, 2))
#			quantity = quantity.replace(',', '\u00a0')
#			quantity = quantity.replace('.', ',')
#			quantity = '{}\u00a0{}'.format(quantity, unit.local_symbol)
#			return quantity
#		else:
#			return '-'

#	quantity_str = property(_get_quantity_str)

#	class Meta:
#		ordering = ['number']
#		unique_together = ("position", "number")


#class Word(models.Model):

#	word     = models.CharField(max_length = 100, unique = True)
#	created  = models.DateTimeField()
#	modified = models.DateTimeField()

#	def __str__(self):
#		return "{}".format(self.word)

#	class Meta:
#		ordering = ['word']


#class QueryFilter(models.Model):

#	name         = models.CharField(max_length = 100)

#	regions      = models.ManyToManyField(Region,       db_table = 'tenders_queryfilter_to_region',   related_name = 'queryfilter_region')
#	customers    = models.ManyToManyField(Organisation, db_table = 'tenders_queryfilter_to_customer', related_name = 'queryfilter_customer')
#	owners       = models.ManyToManyField(Organisation, db_table = 'tenders_queryfilter_to_owner',    related_name = 'queryfilter_owner')
#	okveds       = models.ManyToManyField(OKVED,        db_table = 'tenders_queryfilter_to_okved',    related_name = 'queryfilter_okved')
#	okpds        = models.ManyToManyField(OKPD,         db_table = 'tenders_queryfilter_to_okpd',     related_name = 'queryfilter_okpd')
#	words        = models.ManyToManyField(Word,         db_table = 'tenders_queryfilter_to_word',     related_name = 'queryfilter_word')

#	regions_in   = models.BooleanField(default=True)
#	customers_in = models.BooleanField(default=True)
#	owners_in    = models.BooleanField(default=True)
#	okveds_in    = models.BooleanField(default=True)
#	okpds_in     = models.BooleanField(default=True)
#	words_in     = models.BooleanField(default=True)

#	state        = models.BooleanField(default=True)
#	public       = models.BooleanField(default=False)

#	created      = models.DateTimeField()
#	created_by   = models.CharField(max_length=100, null=True, default=None)
#	modified     = models.DateTimeField()
#	modified_by  = models.CharField(max_length=100, null=True, default=None)

#	def __str__(self):
#		return "{}".format(self.name)

#	class Meta:
#		ordering = ['name']
