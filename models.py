import uuid
from django.db import models
from django.utils import timezone



class UpdaterManager(models.Manager):


	def take(self, alias, **kwargs):

		if not alias:
			return None

		try:
			o = self.get(alias = alias)

		except Updater.DoesNotExist:
			o = Updater()
			o.alias = alias[:50]
			o.name  = kwargs.get('name', None)
			o.save()

		return o



class Updater(models.Model):

	id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	name     = models.TextField(null = True, default = None)
	alias    = models.CharField(max_length = 50, unique = True)
	login    = models.TextField(null = True, default = None)
	password = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True, db_index = True)
	updated  = models.DateTimeField(default = timezone.now)

	objects = UpdaterManager()


	def __str__(self):
		return "{}".format(self.name)



	class Meta:
		ordering = ['name']



class SourceManager(models.Manager):


	def take(self, url):

		if not url:
			return None

		try:
			o = self.get(url = url)

		except Source.DoesNotExist:
			o = Source()
			o.url = url[:2048]
			o.save()

		return o



class Source(models.Model):

	id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	url   = models.CharField(max_length = 2048, unique = True)
	state = models.BooleanField(default = False, db_index = True)

	objects = SourceManager()


	def is_parsed(self):

		if self.state:
			print("Обработан: {}.".format(self.url))
			return True
		else:
			return False


	def complite(self):

		self.state = True
		self.save()
		return True


	def __str__(self):
		return "{}".format(self.url)



	class Meta:
		ordering = ['url']



class RegionManager(models.Manager):


	def take(self, alias, **kwargs):

		if not alias:
			return False

		try:
			o = self.get(alias = alias)

		except Region.DoesNotExist:
			o = Region()
			o.alias     = alias[:50]
			o.name      = kwargs.get('name',      None)
			o.full_name = kwargs.get('full_name', None)
			o.save()

		return o



class Region(models.Model):

	id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	alias     = models.CharField(max_length = 50, unique = True)
	name      = models.TextField(null = True, default = None)
	full_name = models.TextField(null = True, default = None)
	state     = models.BooleanField(default = False, db_index = True)

	objects   = RegionManager()

	
	def __str__(self):
		return "{}".format(self.name)


	class Meta:
		ordering = ['name']



class CountryManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return False

		try:
			o = self.get(code = code)

		except Country.DoesNotExist:
			o = Country()
			o.code      = code[:10]
			o.full_name = kwargs.get('full_name', None)
			o.state     = kwargs.get('state', True)
			if kwargs.get('name', None):
				o.name = kwargs.get('name')
			else:
				o.name = kwargs.get('full_name', None)
			o.save()

		return o


	def update(self, code, **kwargs):

		if not code:
			return None

		o = self.take(code, **kwargs)

		o.full_name = kwargs.get('full_name', None)
		o.state     = kwargs.get('state',     True)

		if kwargs.get('name', None):
			o.name = kwargs.get('name')
		else:
			o.name = kwargs.get('full_name', None)

		o.save()

		return o



class Country(models.Model):

	id        = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code      = models.CharField(max_length = 10, unique = True)
	full_name = models.TextField(null = True, default = None)
	name      = models.TextField(null = True, default = None)
	state     = models.BooleanField(default = True, db_index = True)

	objects   = CountryManager()


	def __str__(self):
		return "{} {}".format(self.code, self.full_name)



	class Meta:
		ordering = ['name']



class CurrencyManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except Currency.DoesNotExist:
			o = Currency()
			o.code         = code[:10]
			o.digital_code = kwargs.get('digital_code', None)
			o.name         = kwargs.get('name',         None)
			o.state        = kwargs.get('state',        True)
			o.save()

		return o


	def update(self, code, **kwargs):

		if not code:
			return None

		o = self.take(code, **kwargs)

		o.digital_code = kwargs.get('digital_code', None)
		o.name         = kwargs.get('name',         None)
		o.state        = kwargs.get('state',        True)
		o.save()

		return o


class Currency(models.Model):

	id           = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code         = models.CharField(max_length = 10, unique = True)
	digital_code = models.CharField(max_length = 10, unique = True)
	name         = models.TextField(null = True, default = None)
	state        = models.BooleanField(default = True, db_index = True)

	objects      = CurrencyManager()

	def __str__(self):
		return "{}".format(self.code)

	class Meta:
		ordering = ['code']



class OKEISectionManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except OKEISection.DoesNotExist:
			o = OKEISection()
			o.code  = code[:10]
			o.name  = kwargs.get('name',  None)
			o.state = kwargs.get('state', True)
			o.save()

		return o


	def update(self, code, **kwargs):

		if not code:
			return None

		o = self.take(code, **kwargs)

		o.name  = kwargs.get('name',  None)
		o.state = kwargs.get('state', True)
		o.save()

		return o



class OKEISection(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code     = models.CharField(max_length = 10, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True, db_index = True)

	objects  = OKEISectionManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['code']



class OKEIGroupManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except OKEIGroup.DoesNotExist:
			o          = OKEIGroup()
			o.code     = code[:10]
			o.name     = kwargs.get('name',  None)
			o.state    = kwargs.get('state', True)
			o.save()

		return o


	def update(self, code, **kwargs):

		if not code:
			return None

		o = self.take(code, **kwargs)

		o.name  = kwargs.get('name',  None)
		o.state = kwargs.get('state', True)
		o.save()

		return o



class OKEIGroup(models.Model):

	id      = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code    = models.CharField(max_length = 10, unique = True)
	name    = models.TextField(null = True, default = None)
	state   = models.BooleanField(default = True, db_index = True)

	objects = OKEIGroupManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['code']



class OKEIManager(models.Manager):

	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except OKEI.DoesNotExist:
			o = OKEI()
			o.code                 = code[:10]
			o.full_name            = kwargs.get('full_name',            None)
			o.section              = kwargs.get('section',              None)
			o.group                = kwargs.get('group',                None)
			o.local_name           = kwargs.get('local_name',           None)
			o.international_name   = kwargs.get('international_name',   None)
			o.local_symbol         = kwargs.get('local_symbol',         None)
			o.international_symbol = kwargs.get('international_symbol', None)
			o.state                = kwargs.get('state',                True)
			o.save()

		return o

	def update(self, code, **kwargs):

		if not code:
			return None

		o = self.take(code, **kwargs)

		o.full_name            = kwargs.get('full_name',            None)
		o.section              = kwargs.get('section',              None)
		o.group                = kwargs.get('group',                None)
		o.local_name           = kwargs.get('local_name',           None)
		o.international_name   = kwargs.get('international_name',   None)
		o.local_symbol         = kwargs.get('local_symbol',         None)
		o.international_symbol = kwargs.get('international_symbol', None)
		o.state                = kwargs.get('state',                True)
		o.save()

		return o



class OKEI(models.Model):

	id                   = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	section              = models.ForeignKey(OKEISection, on_delete = models.CASCADE, null = True, default = None)
	group                = models.ForeignKey(OKEIGroup,   on_delete = models.CASCADE, null = True, default = None)

	code                 = models.CharField(max_length = 10, unique = True)
	full_name            = models.TextField(null = True, default = None)
	local_name           = models.TextField(null = True, default = None)
	international_name   = models.TextField(null = True, default = None)
	local_symbol         = models.TextField(null = True, default = None)
	international_symbol = models.TextField(null = True, default = None)
	state                = models.BooleanField(default = True, db_index = True)

	objects              = OKEIManager()

	def __str__(self):
		return "{}".format(self.full_name)

	class Meta:
		ordering = ['code']



class KOSGUManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except KOSGU.DoesNotExist:
			o          = KOSGU()
			o.code     = code[:10]
			o.name     = kwargs.get('name',   None)
			o.parent   = kwargs.get('parent', None)
			o.state    = kwargs.get('state',  True)
			o.save()

		return o


	def update(self, code, **kwargs):

		if not code:
			return None

		o = self.take(code, **kwargs)
		o.name   = kwargs.get('name',   None)
		o.parent = kwargs.get('parent', None)
		o.state  = kwargs.get('state',  True)
		o.save()

		return o



class KOSGU(models.Model):

	id          = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	parent      = models.ForeignKey('self', on_delete = models.CASCADE, null = True, default = None)

	code        = models.CharField(max_length = 10, unique = True)
	name        = models.TextField(null = True, default = None)
	state       = models.BooleanField(default = True, db_index = True)

	objects     = KOSGUManager()

	def __str__(self):
		return "{}".format(self.code)

	class Meta:
		ordering = ['code']



class OKOPFManager(models.Manager):


	def take(self, code, **kwargs):
		if not code:
			return None
		try:
			o = self.get(code = code)
		except OKOPF.DoesNotExist:
			o = OKOPF()
			o.code          = code[:10]
			o.full_name     = kwargs.get('full_name',     None)
			o.singular_name = kwargs.get('singular_name', None)
			o.parent        = kwargs.get('parent',        None)
			o.state         = kwargs.get('state',         True)
			o.save()
		return o


	def update(self, code, **kwargs):
		if not code:
			return None
		o = self.take(code, **kwargs)
		o.full_name     = kwargs.get('full_name',     None)
		o.singular_name = kwargs.get('singular_name', None)
		o.parent        = kwargs.get('parent',        None)
		o.state         = kwargs.get('state',         True)
		o.save()
		return o



class OKOPF(models.Model):

	id            = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	parent        = models.ForeignKey('self', on_delete = models.CASCADE, null = True, default = None)

	code          = models.CharField(max_length = 10, unique = True)
	full_name     = models.TextField(null = True, default = None)
	singular_name = models.TextField(null = True, default = None)
	state         = models.BooleanField(default = True, db_index = True)

	objects       = OKOPFManager()

	def __str__(self):
		return "{} {}".format(self.code, self.full_name)

	class Meta:
		ordering = ['code']



class OKPDManager(models.Manager):


	def take(self, oos_id = None, code = None, **kwargs):

		if not oos_id and not code:
			return None

		try:
			if oos_id:
				o = self.get(oos_id = oos_id)
			else:
				o = self.get(code = code)

		except OKPD.DoesNotExist:
			o = OKPD()
			o.oos_id = oos_id
			if code:
				o.code = code[:50]
			o.name   = kwargs.get('name',   None)
			o.parent = kwargs.get('parent', None)
			o.state  = kwargs.get('state',  True)
			o.save()

		return o


	def update(self, oos_id, code = None, **kwargs):

		if not code:
			return None

		o = self.take(oos_id, code, **kwargs)
		o.code     = code[:50]
		o.name     = kwargs.get('name',   None)
		o.parent   = kwargs.get('parent', None)
		o.state    = kwargs.get('state',  True)
		o.save()

		return o



class OKPD(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	parent   = models.ForeignKey('self', on_delete = models.CASCADE, null = True, default = None)

	oos_id   = models.IntegerField(null = True, default = None)
	code     = models.CharField(max_length = 50, null = True, default = None, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True, db_index = True)

	objects  = OKPDManager()

	def __str__(self):
		return "{}".format(self.code)

	class Meta:
		ordering = ['code']



class OKPD2Manager(models.Manager):


	def take(self, oos_id, code = None, **kwargs):

		if not oos_id and not code:
			return None

		try:
			if oos_id:
				o = self.get(oos_id = oos_id)
			else:
				o = self.get(code = code)

		except OKPD2.DoesNotExist:
			o = OKPD2()
			o.oos_id       = oos_id
			o.code     = code[:50]
			o.name     = kwargs.get('name',   None)
			o.parent   = kwargs.get('parent', None)
			o.state    = kwargs.get('state',  True)
			o.save()

		return o


	def update(self, oos_id, code, **kwargs):

		if not oos_id:
			return None

		o = self.take(oos_id, code, **kwargs)
		o.code   = code[:50]
		o.name   = kwargs.get('name',   None)
		o.parent = kwargs.get('parent', None)
		o.state  = kwargs.get('state',  True)
		o.save()

		return o



class OKPD2(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	parent   = models.ForeignKey('self', on_delete = models.CASCADE, null = True, default = None)

	oos_id   = models.IntegerField(null = True, default = None)
	code     = models.CharField(max_length = 50, null = True, default = None, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True, db_index = True)

	objects  = OKPD2Manager()

	def __str__(self):
		return "{}".format(self.code)

	class Meta:
		ordering = ['code']



class OKTMOManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except OKTMO.DoesNotExist:
			o = OKTMO()
			o.code   = code[:20]
			o.name   = kwargs.get('name',   None)
			o.parent = kwargs.get('parent', None)
			o.state  = kwargs.get('state',  True)
			o.save()

		return o


	def update(self, code, **kwargs):

		if not code:
			return None

		o = self.take(code, **kwargs)
		o.name     = kwargs.get('name',   None)
		o.parent   = kwargs.get('parent', None)
		o.state    = kwargs.get('state',  True)
		o.save()

		return o



class OKTMO(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	parent   = models.ForeignKey('self', on_delete = models.CASCADE, null = True, default = None)

	code     = models.CharField(max_length = 20, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True, db_index = True)

	objects = OKTMOManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class OKVEDSectionManager(models.Manager):


	def take(self, name, **kwargs):

		if not name:
			return None

		try:
			o = self.get(name = name)

		except OKVEDSection.DoesNotExist:
			o          = OKVEDSection()
			o.name     = name
			o.state    = kwargs.get('state', True)
			o.save()

		return o

	def update(self, name, **kwargs):

		if not name:
			return None

		o = self.take(name, **kwargs)
		o.state = kwargs.get('state', True)
		o.save()

		return o



class OKVEDSection(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	name     = models.TextField(unique = True)
	state    = models.BooleanField(default = True, db_index = True)

	objects  = OKVEDSectionManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['name']



class OKVEDSubSectionManager(models.Manager):


	def take(self, name, **kwargs):

		if not name:
			return None

		try:
			o = self.get(name = name)

		except OKVEDSubSection.DoesNotExist:
			o          = OKVEDSubSection()
			o.name     = name
			o.state    = kwargs.get('state', True)
			o.save()

		return o


	def update(self, name, **kwargs):

		if not name:
			return None

		o = self.take(name, **kwargs)
		o.state = kwargs.get('state', True)
		o.save()

		return o



class OKVEDSubSection(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	name     = models.TextField(unique = True)
	state    = models.BooleanField(default = True, db_index = True)

	objects  = OKVEDSubSectionManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['name']



class OKVEDManager(models.Manager):

	def take(self, oos_id = None, code = None, **kwargs):


		if not oos_id and not code:
			return None

		try:
			if oos_id:
				o = self.get(oos_id = oos_id)
			else:
				o = self.get(code = code)

		except OKVED.DoesNotExist:
			o = OKVED()
			o.oos_id = oos_id
			if code:
				o.code = code[:100]
			o.section    = kwargs.get('section',    None)
			o.subsection = kwargs.get('subsection', None)
			o.parent     = kwargs.get('parent',     None)
			o.name       = kwargs.get('name',       None)
			o.state      = kwargs.get('state',      True)
			o.save()

		return o

	def update(self, oos_id, code = None, **kwargs):

		if not oos_id:
			return None

		o = self.take(oos_id, code, **kwargs)
		o.code       = code[:100]
		o.section    = kwargs.get('section',    None)
		o.subsection = kwargs.get('subsection', None)
		o.parent     = kwargs.get('parent',     None)
		o.name       = kwargs.get('name',       None)
		o.state      = kwargs.get('state',      True)
		o.save()

		return o



class OKVED(models.Model):

	id         = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	section    = models.ForeignKey(OKVEDSection,    on_delete = models.CASCADE, null = True, default = None)
	subsection = models.ForeignKey(OKVEDSubSection, on_delete = models.CASCADE, null = True, default = None)
	parent     = models.ForeignKey('self',          on_delete = models.CASCADE, null = True, default = None)

	oos_id     = models.IntegerField(null = True, default = None)
	code       = models.CharField(max_length = 100, null = True, default = None, db_index = True)
	name       = models.TextField(null = True, default = None)
	state      = models.BooleanField(default = True, db_index = True)

	objects = OKVEDManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class OKVED2SectionManager(models.Manager):


	def take(self, name, **kwargs):

		if not name:
			return None

		try:
			o = self.get(name = name)

		except OKVED2Section.DoesNotExist:
			o = OKVED2Section()
			o.name  = name
			o.state = kwargs.get('state', True)
			o.save()

		return o


	def update(self, name, state = True):

		if not name:
			return None

		o = self.take(name, **kwargs)
		o.state = kwargs.get('state', True)
		o.save()

		return o



class OKVED2Section(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	name     = models.TextField(unique = True)
	state    = models.BooleanField(default = True, db_index = True)

	objects = OKVED2SectionManager()


	def __str__(self):
		return "{}".format(self.name)



	class Meta:
		ordering = ['name']



class OKVED2Manager(models.Manager):


	def take(self, code, oos_id = None, **kwargs):

		if not code and not oos_id:
			return None

		try:
			if code:
				o = self.get(code = code)
			else:
				o = self.get(oos_id = oos_id)

		except OKVED2.DoesNotExist:
			o = OKVED2()
			o.oos_id  = oos_id
			o.code    = code[:100]
			o.section = kwargs.get('section', None)
			o.parent  = kwargs.get('parent',  None)
			o.name    = kwargs.get('name',    None)
			o.comment = kwargs.get('comment', None)
			o.state   = kwargs.get('state',   True)
			o.save()

		return o


	def update(self, code, oos_id, **kwargs):

		if not code or not oos_id:
			return None

		o = self.take(code, oos_id, **kwargs)
		o.oos_id         = oos_id
		o.section    = kwargs.get('section', None)
		o.parent     = kwargs.get('parent',  None)
		o.name       = kwargs.get('name',    None)
		o.comment    = kwargs.get('comment', None)
		o.state      = kwargs.get('state',   True)
		o.save()

		return o



class OKVED2(models.Model):

	id      = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	section = models.ForeignKey(OKVED2Section, on_delete = models.CASCADE, null = True, default = None)
	parent  = models.ForeignKey('self',        on_delete = models.CASCADE, null = True, default = None)

	oos_id  = models.BigIntegerField(null = True, default = None)
	code    = models.CharField(max_length = 100, null = True, default = None, unique = True)
	name    = models.TextField(null = True, default = None)
	comment = models.TextField(null = True, default = None)
	state   = models.BooleanField(default = True, db_index = True)

	objects = OKVED2Manager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class BudgetManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except Budget.DoesNotExist:
			o = Budget()
			o.code     = code[:20]
			o.name     = kwargs.get('name',  None)
			o.state    = kwargs.get('state', False)
			o.save()

		return o


	def update(self, code, **kwargs):

		if not code:
			return None

		o = self.take(code, **kwargs)
		o.name  = kwargs.get('name',  None)
		o.state = kwargs.get('state', True)
		o.save()

		return o



class Budget(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code     = models.CharField(max_length = 20, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True, db_index = True)

	objects  = BudgetManager()


	def __str__(self):
		return "{} {}".format(self.code, self.name)



	class Meta:
		ordering = ['code']



class SubsystemTypeManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except SubsystemType.DoesNotExist:
			o = SubsystemType()
			o.code     = code[:20]
			o.name     = kwargs.get('name',  None)
			o.state    = kwargs.get('state', True)
			o.save()

		return o



class SubsystemType(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code     = models.CharField(max_length = 20, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True, db_index = True)

	objects  = SubsystemTypeManager()


	def __str__(self):
		return "{} {}".format(self.code, self.name)



	class Meta:
		ordering = ['code']



class BudgetTypeManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except BudgetType.DoesNotExist:
			o = BudgetType()
			o.code           = code[:20]
			o.name           = kwargs.get('name',           None)
			o.subsystem_type = kwargs.get('subsystem_type', None)
			o.state          = kwargs.get('state',          True)
			o.save()

		return o


	def update(self, code, **kwargs):

		if not code:
			return None

		o = self.take(code, **kwargs)
		o.name           = kwargs.get('name',           None)
		o.subsystem_type = kwargs.get('subsystem_type', None)
		o.state          = kwargs.get('state',          True)
		o.save()

		return o


class BudgetType(models.Model):

	id             = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	subsystem_type = models.ForeignKey(SubsystemType, on_delete = models.CASCADE, null = True, default = None)

	code           = models.CharField(max_length = 20, unique = True)
	name           = models.TextField(null = True, default = None)
	state          = models.BooleanField(default = True, db_index = True)

	objects = BudgetTypeManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



#class KBKBudgetManager(models.Manager):


#	def take(self, code, **kwargs):
#		if not code:
#			return None
#		try:
#			o = self.get(code = code)
#		except KBKBudget.DoesNotExist:
#			o = KBKBudget()
#			o.code       = code
#			o.budget     = kwargs.get('budget',     None)
#			o.start_date = kwargs.get('start_date', None)
#			o.end_date   = kwargs.get('end_date',   None)
#			o.state      = kwargs.get('state',      True)
#			o.save()
#		return o


#	def update(self, code, **kwargs):
#		if not code:
#			return None
#		o = self.take(code, **kwargs)
#		o.budget     = kwargs.get('budget',     None)
#		o.start_date = kwargs.get('start_date', None)
#		o.end_date   = kwargs.get('end_date',   None)
#		o.state      = kwargs.get('state',      True)
#		o.save()
#		return o



#class KBKBudget(models.Model):

#	id         = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
#	budget     = models.ForeignKey(Budget, on_delete = models.CASCADE, null = True, default = None)
#	code       = models.CharField(max_length = 50, unique = True)
#	start_date = models.DateTimeField(null = True, default = None)
#	end_date   = models.DateTimeField(null = True, default = None)
#	state      = models.BooleanField(default = True, db_index = True)
#	objects = KBKBudgetManager()

#	def __str__(self):
#		return "{} {}".format(self.code, self.budget)

#	class Meta:
#		ordering = ['code']



class OKOGUManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except OKOGU.DoesNotExist:
			o          = OKOGU()
			o.code     = code[:20]
			o.name     = kwargs.get('name', None)
			o.state    = kwargs.get('state', True)
			o.save()

		return o



class OKOGU(models.Model):

	id      = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code    = models.CharField(max_length = 20, unique = True)
	name    = models.TextField(null = True, default = None)
	state   = models.BooleanField(default = True, db_index = True)

	objects = OKOGUManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class AttachmentManager(models.Manager):


	def take(self, url, **kwargs):

		if not url:
			return None

		try:
			o = self.get(url = url)

		except Attachment.DoesNotExist:
			o = Attachment()
			o.url         = url
			o.name        = kwargs.get('name', None)
			o.size        = kwargs.get('size', None)
			o.description = kwargs.get('description', None)
			o.save()

		return o



class Attachment(models.Model):

	id          = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	url         = models.TextField(unique = True)
	name        = models.TextField(null = True, default = None)
	size        = models.TextField(null = True, default = None)
	description = models.TextField(null = True, default = None)

	objects = AttachmentManager()

	def __str__(self):
		return "Attachment: {}".format(self.url)



class AddressManager(models.Manager):


	def take(self, address, **kwargs):

		if not address:
			return None

		try:
			o = self.get(address = address)

		except Address.DoesNotExist:
			o         = Address()
			o.address = address
			o.state   = kwargs.get('state', True)
			o.save()

		return o



class Address(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	address  = models.TextField(unique = True)
	state    = models.BooleanField(default = True, db_index = True)

	objects  = AddressManager()

	def __str__(self):
		return "{}".format(self.address)

	class Meta:
		ordering = ['address']



class EmailManager(models.Manager):

	def take(self, email, **kwargs):

		if not email:
			return None

		try:
			o = self.get(email = email)

		except Email.DoesNotExist:
			o       = Email()
			o.email = email
			o.state = kwargs.get('state', True)
			o.save()

		return o



class Email(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	email    = models.TextField(unique = True)
	state    = models.BooleanField(default = True, db_index = True)

	objects  = EmailManager()

	def __str__(self):
		return "{}".format(self.email)

	class Meta:
		ordering = ['email']



class PhoneManager(models.Manager):

	def take(self, phone, **kwargs):

		if not phone:
			return None

		try:
			o = self.get(phone = phone)

		except Phone.DoesNotExist:
			o = Phone()
			o.phone = phone
			o.state = kwargs.get('state', True)
			o.save()

		return o



class Phone(models.Model):

	id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	phone = models.TextField(unique = True)
	state = models.BooleanField(default = True, db_index = True)

	objects = PhoneManager()

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

		o.first_name  = first_name
		o.middle_name = middle_name
		o.last_name   = last_name
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

	id          = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	first_name  = models.TextField(null = True, default = None, db_index = True)
	middle_name = models.TextField(null = True, default = None, db_index = True)
	last_name   = models.TextField(null = True, default = None, db_index = True)
	position    = models.TextField(null = True, default = None)
	description = models.TextField(null = True, default = None)
	state       = models.BooleanField(default = True, db_index = True)

	emails      = models.ManyToManyField(Email, related_name = 'person_email', through = 'PersonToEmail', through_fields = ('person', 'email'))
	phones      = models.ManyToManyField(Phone, related_name = 'person_phone', through = 'PersonToPhone', through_fields = ('person', 'phone'))
	faxes       = models.ManyToManyField(Phone, related_name = 'person_fax',   through = 'PersonToFax',   through_fields = ('person', 'fax'))

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



#class BankManager(models.Manager):

#	def take(self, bik, **kwargs):
#		if not bik:
#			return None
#		try:
#			o = self.get(bik = bik)
#		except Bank.DoesNotExist:
#			o = Bank()
#			o.bik     = bik
#			o.name    = kwargs.get('name', None)
#			o.address = kwargs.get('address', None)
#			o.state   = kwargs.get('state', True)
#			o.save()
#		return o



#class Bank(models.Model):

#	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
#	address  = models.ForeignKey(Address, on_delete = models.CASCADE, null = True, default = None)
#	bik      = models.CharField(max_length = 10, unique = True)
#	name     = models.TextField(null = True, default = None)
#	state    = models.BooleanField(default = True, db_index = True)

#	objects  = BankManager()

#	def __str__(self):
#		return "{} {}".format(self.bik, self.name)

#	class Meta:
#		ordering = ['bik']



#class AccountManager(models.Manager):

#	def take(self, payment_account, corr_account, personal_account, bank, **kwargs):
#		if not payment_account and not corr_account and not personal_account and not bank:
#			return None
#		try:
#			o = self.get(
#				payment_account  = payment_account,
#				corr_account     = corr_account,
#				personal_account = personal_account,
#				bank             = bank)
#		except Account.DoesNotExist:
#			o = Account()
#			o.payment_account  = payment_account
#			o.corr_account     = corr_account
#			o.personal_account = personal_account
#			o.bank             = bank
#			o.state            = kwargs.get('state', True)
#			o.save()
#		return o



#class Account(models.Model):

#	id               = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
#	bank             = models.ForeignKey(Bank, on_delete = models.CASCADE, null = True, default = None)
#	payment_account  = models.CharField(max_length = 32, null = True, default = None, db_index = True)
#	corr_account     = models.CharField(max_length = 32, null = True, default = None, db_index = True)
#	personal_account = models.CharField(max_length = 32, null = True, default = None, db_index = True)
#	state            = models.BooleanField(default = True, db_index = True)

#	objects = AccountManager()

#	def __str__(self):
#		return "{}".format(self.payment_account)

#	class Meta:
#		ordering = ['payment_account']



class OrganisationRoleManager(models.Manager):

	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except OrganisationRole.DoesNotExist:
			o = OrganisationRole()
			o.code  = code[:20]
			o.name  = kwargs.get('name', None)
			o.state = kwargs.get('state', True)
			o.save()

		return o



class OrganisationRole(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code     = models.CharField(max_length = 20, unique = True)
	name     = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True, db_index = True)

	objects  = OrganisationRoleManager()

	def __str__(self):
		return "{}".format(self.code)

	class Meta:
		ordering = ['code']



class OrganisationTypeManager(models.Manager):


	def take(self, code, **kwargs):
		if not code:
			return None
		try:
			o = self.get(code = code)
		except OrganisationType.DoesNotExist:
			o = OrganisationType()
			o.code        = code
			o.name        = kwargs.get('name', None)
			o.description = kwargs.get('description', None)
			o.save()
		return o


	def update(self, code, **kwargs):
		if not code:
			return None
		o = self.take(code = code)
		o.name        = kwargs.get('name', None)
		o.description = kwargs.get('description', None)
		o.save()
		return o



class OrganisationType(models.Model):

	id          = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code        = models.CharField(max_length = 20, unique = True)
	name        = models.TextField(null = True, default = None)
	description = models.TextField(null = True, default = None)

	objects     = OrganisationTypeManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class OrganisationManager(models.Manager):


	def take(self, oos_number, **kwargs):

		if not oos_number:
			return None

		try:
			o = self.get(oos_number = oos_number)

		except Organisation.DoesNotExist:
			o = Organisation()
			o.oos_number        = oos_number
			o.short_name        = kwargs.get('short_name',        None)
			o.full_name         = kwargs.get('full_name',         None)
			o.inn               = kwargs.get('inn',               None)
			o.kpp               = kwargs.get('kpp',               None)
			o.ogrn              = kwargs.get('ogrn',              None)
			o.okpo              = kwargs.get('okpo',              None)
			o.factual_address   = kwargs.get('factual_address',   None)
			o.postal_address    = kwargs.get('postal_address',    None)
			o.email             = kwargs.get('email',             None)
			o.phone             = kwargs.get('phone',             None)
			o.fax               = kwargs.get('fax',               None)
			o.contact_person    = kwargs.get('contact_person',    None)
			o.head_agency       = kwargs.get('head_agency',       None)
			o.ordering_agency   = kwargs.get('ordering_agency',   None)
			o.okopf             = kwargs.get('okopf',             None)
			o.okogu             = kwargs.get('okogu',             None)
			o.organisation_role = kwargs.get('organisation_role', None)
			o.organisation_type = kwargs.get('organisation_type', None)
			o.oktmo             = kwargs.get('oktmo',             None)
			o.state             = kwargs.get('state',             True)
			o.register          = kwargs.get('register',          True)

			if kwargs.get('name', None):
				o.name = kwargs.get('name', None)
			else:
				o.name = kwargs.get('full_name', None)

			o.save()

		return o


	def update(self, oos_number, **kwargs):

		if not oos_number:
			return None

		o = self.take(oos_number, **kwargs)
		o.short_name        = kwargs.get('short_name',        None)
		o.full_name         = kwargs.get('full_name',         None)
		o.inn               = kwargs.get('inn',               None)
		o.kpp               = kwargs.get('kpp',               None)
		o.ogrn              = kwargs.get('ogrn',              None)
		o.okpo              = kwargs.get('okpo',              None)
		o.factual_address   = kwargs.get('factual_address',   None)
		o.postal_address    = kwargs.get('postal_address',    None)
		o.email             = kwargs.get('email',             None)
		o.phone             = kwargs.get('phone',             None)
		o.fax               = kwargs.get('fax',               None)
		o.contact_person    = kwargs.get('contact_person',    None)
		o.head_agency       = kwargs.get('head_agency',       None)
		o.ordering_agency   = kwargs.get('ordering_agency',   None)
		o.okopf             = kwargs.get('okopf',             None)
		o.okogu             = kwargs.get('okogu',             None)
		o.organisation_role = kwargs.get('organisation_role', None)
		o.organisation_type = kwargs.get('organisation_type', None)
		o.oktmo             = kwargs.get('oktmo',             None)
		o.state             = kwargs.get('state',             True)
		o.register          = kwargs.get('register',          True)

		if kwargs.get('name', None):
			o.name = kwargs.get('name', None)
		else:
			o.name = kwargs.get('full_name', None)

		o.save()

		return o



class Organisation(models.Model):

	id                = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	factual_address   = models.ForeignKey(Address,          on_delete = models.CASCADE, related_name = 'organisation_factual_address', null = True, default = None)
	postal_address    = models.ForeignKey(Address,          on_delete = models.CASCADE, related_name = 'organisation_postal_address',  null = True, default = None)
	email             = models.ForeignKey(Email,            on_delete = models.CASCADE, related_name = 'organisation_email',           null = True, default = None)
	phone             = models.ForeignKey(Phone,            on_delete = models.CASCADE, related_name = 'organisation_phone',           null = True, default = None)
	fax               = models.ForeignKey(Phone,            on_delete = models.CASCADE, related_name = 'organisation_fax',             null = True, default = None)
	contact_person    = models.ForeignKey(Person,           on_delete = models.CASCADE, related_name = 'organisation_contact_person',  null = True, default = None)
	head_agency       = models.ForeignKey('self',           on_delete = models.CASCADE, related_name = 'organisation_head_agency',     null = True, default = None)
	ordering_agency   = models.ForeignKey('self',           on_delete = models.CASCADE, related_name = 'organisation_ordering_agency', null = True, default = None)
	okopf             = models.ForeignKey(OKOPF,            on_delete = models.CASCADE, related_name = 'organisation_okopf',           null = True, default = None)
	okogu             = models.ForeignKey(OKOGU,            on_delete = models.CASCADE, related_name = 'organisation_okogu',           null = True, default = None)
	organisation_role = models.ForeignKey(OrganisationRole, on_delete = models.CASCADE, related_name = 'organisation_role',            null = True, default = None)
	organisation_type = models.ForeignKey(OrganisationType, on_delete = models.CASCADE, related_name = 'organisation_type',            null = True, default = None)
	oktmo             = models.ForeignKey(OKTMO,            on_delete = models.CASCADE, related_name = 'organisation_oktmo',           null = True, default = None)

	oos_number        = models.CharField(max_length = 20, null = True, default = None, db_index = True)
	name              = models.TextField(null = True, default = None, db_index = True)
	short_name        = models.TextField(null = True, default = None)
	full_name         = models.TextField(null = True, default = None)
	inn               = models.CharField(max_length = 20, null = True, default = None, db_index = True)
	kpp               = models.CharField(max_length = 20, null = True, default = None, db_index = True)
	ogrn              = models.CharField(max_length = 20, null = True, default = None)
	okpo              = models.CharField(max_length = 20, null = True, default = None)
	state             = models.BooleanField(default = True, db_index = True)
	register          = models.BooleanField(default = True, db_index = True)

#	accounts          = models.ManyToManyField(Account, through = 'OrganisationToAccount', through_fields = ('organisation', 'account'))
	budgets           = models.ManyToManyField(Budget,  through = 'OrganisationToBudget',  through_fields = ('organisation', 'budget'))
	okveds            = models.ManyToManyField(OKVED,   through = 'OrganisationToOKVED',   through_fields = ('organisation', 'okved'))

	objects           = OrganisationManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['oos_number']



#class OrganisationToAccount(models.Model):

#	id           = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
#	organisation = models.ForeignKey(Organisation, on_delete = models.CASCADE)
#	account      = models.ForeignKey(Account,      on_delete = models.CASCADE)

#	class Meta:
#		db_table = 'tenders_organisation_to_account'



class OrganisationToBudget(models.Model):

	id           = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	organisation = models.ForeignKey(Organisation, on_delete = models.CASCADE)
	budget       = models.ForeignKey(Budget,       on_delete = models.CASCADE)

	class Meta:
		db_table = 'tenders_organisation_to_budget'



class OrganisationToOKVED(models.Model):

	id           = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	organisation = models.ForeignKey(Organisation, on_delete = models.CASCADE)
	okved        = models.ForeignKey(OKVED,        on_delete = models.CASCADE)

	class Meta:
		db_table = 'tenders_organisation_to_okved'



class PlacingWayManager(models.Manager):


	def take(self, oos_id, **kwargs):

		if not oos_id:
			return None

		try:
			o = self.get(oos_id = oos_id)

		except Exception:
			o = PlacingWay()
			o.oos_id          = oos_id
			o.code            = kwargs.get('code', None)
			o.name            = kwargs.get('name', None)
			o.type_code       = kwargs.get('type_code', None)
			o.subsystem_type  = kwargs.get('subsystem_type', None)
			o.state           = kwargs.get('state', True)
			o.save()

		return o


	def update(self, oos_id, **kwargs):

		if not oos_id:
			return None

		o = self.take(oos_id, **kwargs)
		o.code           = kwargs.get('code', None)
		o.name           = kwargs.get('name', None)
		o.type_code      = kwargs.get('type_code', None)
		o.subsystem_type = kwargs.get('subsystem_type', None)
		o.state          = kwargs.get('state', True)
		o.save()

		return o



class PlacingWay(models.Model):

	id             = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	subsystem_type = models.ForeignKey(SubsystemType, on_delete = models.CASCADE, null = True, default = None)

	oos_id         = models.IntegerField(null = True, default = None, db_index = True)
	code           = models.TextField(null = True, default = None)
	name           = models.TextField(null = True, default = None)
	type_code      = models.CharField(max_length = 20, null = True, default = None)
	state          = models.BooleanField(default = True, db_index = True)

	objects = PlacingWayManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class ETPManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except Exception:
			o = ETP()
			o.code  = code
			o.name  = kwargs.get('name', None)
			o.url   = kwargs.get('url', None)
			o.state = kwargs.get('state', True)
			o.save()

		return o



class ETP(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code     = models.TextField(null = True, default = None, db_index = True)
	name     = models.TextField(null = True, default = None)
	url      = models.TextField(null = True, default = None)
	state    = models.BooleanField(default = True)

	objects = ETPManager()

	def __str__(self):
		return "{} ({})".format(self.name, self.url)

	class Meta:
		ordering = ['name']



class PlanPositionChangeReasonManager(models.Manager):


	def take(self, oos_id, **kwargs):

		if not oos_id:
			return None

		try:
			o = self.get(oos_id = oos_id)

		except Exception:
			o = PlanPositionChangeReason()
			o.oos_id      = oos_id
			o.name        = kwargs.get('name',        None)
			o.description = kwargs.get('description', None)
			o.state       = kwargs.get('state',       True)
			o.save()

		return o


	def update(self, oos_id, **kwargs):

		if not oos_id:
			return None

		o = self.take(oos_id, **kwargs)
		o.name        = kwargs.get('name',        None)
		o.description = kwargs.get('description', None)
		o.state       = kwargs.get('state',       True)
		o.save()

		return o



class PlanPositionChangeReason(models.Model):

	id          = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	oos_id      = models.IntegerField(null = True, default = None, db_index = True)
	name        = models.TextField(null = True, default = None)
	description = models.TextField(null = True, default = None)
	state       = models.BooleanField(default = True, db_index = True)

	objects     = PlanPositionChangeReasonManager()

	def __str__(self):
		return "{} {}".format(self.id, self.name)

	class Meta:
		ordering = ['oos_id']



class ContractModificationReasonManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except Exception:
			o = ContractModificationReason()
			o.code  = code
			o.name  = kwargs.get('name',  None)
			o.state = kwargs.get('state', True)
			o.save()

		return o


	def update(self, code, **kwargs):

		if not code:
			return None

		o = self.take(code, **kwargs)
		o.name  = kwargs.get('name', None)
		o.state = kwargs.get('state', True)
		o.save()

		return o



class ContractModificationReason(models.Model):

	id          = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code        = models.TextField(unique = True)
	name        = models.TextField(null = True, default = None)
	state       = models.BooleanField(default = True, db_index = True)

	objects     = ContractModificationReasonManager()

	def __str__(self):
		return "{} {}".format(self.id, self.name)

	class Meta:
		ordering = ['id']



class KVRManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except Exception:
			o = KVR()
			o.code  = code
			o.name  = kwargs.get('name',  None)
			o.state = kwargs.get('state', True)
			o.save()

		return o


	def update(self, code, **kwargs):

		if not code:
			return None

		o = self.take(code, **kwargs)
		o.name  = kwargs.get('name', None)
		o.state = kwargs.get('state', True)
		o.save()

		return o



class KVR(models.Model):

	id          = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code        = models.TextField(unique = True)
	name        = models.TextField(null = True, default = None)
	state       = models.BooleanField(default = True, db_index = True)

	objects     = KVRManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class PlanManager(models.Manager):


	def take(self, oss_id, **kwargs):

		if not oss_id:
			return None

		try:
			o = self.get(oss_id = oss_id)

		except Exception:
			o = Plan()
			o.oss_id             = oss_id
			o.number         = kwargs.get('number',         None)
			o.year           = kwargs.get('year',           None)
			o.version        = kwargs.get('version',        None)
			o.description    = kwargs.get('description',    None)
			o.url            = kwargs.get('url',            None)
			o.region         = kwargs.get('region',         None)
			o.owner          = kwargs.get('owner',          None)
			o.customer       = kwargs.get('customer',       None)
			o.contact_person = kwargs.get('contact_person', None)
			o.state          = kwargs.get('state',          True)
			o.created        = kwargs.get('created',        None)
			o.confirmed      = kwargs.get('confirmed',      None)
			o.published      = kwargs.get('published',      None)
			o.save()

			self.filter(number = o.number, version__lt = o.version).update(state = False)

		return o


	def update(self, oss_id, **kwargs):

		if not oss_id:
			return None

		o = self.take(oss_id, **kwargs)
		o.number         = kwargs.get('number',         None)
		o.year           = kwargs.get('year',           None)
		o.version        = kwargs.get('version',        None)
		o.description    = kwargs.get('description',    None)
		o.url            = kwargs.get('url',            None)
		o.region         = kwargs.get('region',         None)
		o.owner          = kwargs.get('owner',          None)
		o.customer       = kwargs.get('customer',       None)
		o.contact_person = kwargs.get('contact_person', None)
		o.state          = kwargs.get('state',          True)
		o.created        = kwargs.get('created',        None)
		o.confirmed      = kwargs.get('confirmed',      None)
		o.published      = kwargs.get('published',      None)
		o.save()

		self.filter(number = o.number, version__lt = o.version).update(state = False)

		return o



class Plan(models.Model):

	id             = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	oss_id         = models.BigIntegerField(null = True, default = None, db_index = True)
	region         = models.ForeignKey(Region,       on_delete = models.CASCADE, related_name = 'tenderplan_region',         null = True, default = None)
	owner          = models.ForeignKey(Organisation, on_delete = models.CASCADE, related_name = 'tenderplan_owner',          null = True, default = None)
	customer       = models.ForeignKey(Organisation, on_delete = models.CASCADE, related_name = 'tenderplan_customer',       null = True, default = None)
	contact_person = models.ForeignKey(Person,       on_delete = models.CASCADE, related_name = 'tenderplan_contact_person', null = True, default = None)

	number         = models.CharField(max_length = 20, db_index = True)
	year           = models.IntegerField(null = True, default = None, db_index = True)
	version        = models.IntegerField(null = True, default = None, db_index = True)
	description    = models.TextField(null = True, default = None)
	url            = models.TextField(null = True, default = None, db_index = True)

	state          = models.BooleanField(default = True, db_index = True)
	created        = models.DateTimeField(null = True, default = None)
	confirmed      = models.DateTimeField(null = True, default = None)
	published      = models.DateTimeField(null = True, default = None)


	objects        = PlanManager()

	def __str__(self):
		return "{} {} ".format(self.year, self.customer)

	class Meta:
		ordering = ['year', 'number', 'version']



class ProductManager(models.Manager):


	def take(self, okpd, okpd2, name):

		if not okpd and not okpd2 and not name:
			return None

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
	okpd  = models.ForeignKey(OKPD,  on_delete = models.CASCADE, null = True, default = None)
	okpd2 = models.ForeignKey(OKPD2, on_delete = models.CASCADE, null = True, default = None)

	name  = models.TextField(null = True, default = None, db_index = True)

	objects = ProductManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['name']
		unique_together = ('okpd', 'okpd2', 'name')



class PlanPositionManager(models.Manager):


	def take(self, plan, number, **kwargs):

		if not plan or not number:
			return None

		try:
			o = self.get(plan = plan, number = number)

		except Exception:
			o = PlanPosition()
			o.plan            = plan
			o.number          = number
			o.name            = kwargs.get('name',            None)
			o.purchase_month  = kwargs.get('purchase_month',  None)
			o.purchase_year   = kwargs.get('purchase_year',   None)
			o.execution_month = kwargs.get('execution_month', None)
			o.execution_year  = kwargs.get('execution_year',  None)
			o.max_price       = kwargs.get('max_price',       None)
			o.currency        = kwargs.get('currency',        None)
			o.placing_way     = kwargs.get('placing_way',     None)
			o.change_reason   = kwargs.get('change_reason',   None)

			o.save()

		return o


	def update(self, plan, number, **kwargs):

		if not plan or not number:
			return None

		o = self.take(plan, number, **kwargs)
		o.name            = kwargs.get('name',            None)
		o.purchase_month  = kwargs.get('purchase_month',  None)
		o.purchase_year   = kwargs.get('purchase_year',   None)
		o.execution_month = kwargs.get('execution_month', None)
		o.execution_year  = kwargs.get('execution_year',  None)
		o.max_price       = kwargs.get('max_price',       None)
		o.currency        = kwargs.get('currency',        None)
		o.placing_way     = kwargs.get('placing_way',     None)
		o.change_reason   = kwargs.get('change_reason',   None)
		o.save()

		return o



class PlanPosition(models.Model):

	id            = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	plan          = models.ForeignKey(Plan,                     on_delete = models.CASCADE)
	currency      = models.ForeignKey(Currency,                 on_delete = models.CASCADE, null = True, default = None)
	placing_way   = models.ForeignKey(PlacingWay,               on_delete = models.CASCADE, null = True, default = None)
	change_reason = models.ForeignKey(PlanPositionChangeReason, on_delete = models.CASCADE, null = True, default = None)

	number          = models.CharField(max_length = 50, db_index = True)
	name            = models.TextField(null = True, default = None)
	purchase_month  = models.IntegerField(null = True, default = None, db_index = True)
	purchase_year   = models.IntegerField(null = True, default = None, db_index = True)
	execution_month = models.IntegerField(null = True, default = None, db_index = True)
	execution_year  = models.IntegerField(null = True, default = None, db_index = True)
	max_price       = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None, db_index = True)

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
	okved         = models.ForeignKey(OKVED,        on_delete = models.CASCADE)

	class Meta:
		db_table = 'tenders_planposition_to_okved'



class PlanPositionToOKVED2(models.Model):

	id            = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	plan_position = models.ForeignKey(PlanPosition, on_delete = models.CASCADE)
	okved2        = models.ForeignKey(OKVED2,       on_delete = models.CASCADE)

	class Meta:
		db_table = 'tenders_planposition_to_okved2'



class PlanPositionToProduct(models.Model):

	id            = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	plan_position = models.ForeignKey(PlanPosition, on_delete = models.CASCADE)
	product       = models.ForeignKey(Product,      on_delete = models.CASCADE)
	okei          = models.ForeignKey(OKEI,         on_delete = models.CASCADE, null = True, default = None)

	requirement   = models.TextField(null = True, default = None)
	quantity      = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	price         = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	total         = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None, db_index = True)

	def __str__(self):
		return "{} {}".format(self.product, self.quantity)

	class Meta:
		db_table = 'tenders_planposition_to_product'



class PurchaseManager(models.Manager):


	def take(self, number, **kwargs):

		if not number:
			return None

		try:
			o = self.get(number = number)

		except Exception:
			o = Purchase()
			o.number                 = number
			o.name                   = kwargs.get('name',                   None)
			o.url                    = kwargs.get('url',                    None)
			o.published              = kwargs.get('published',              None)
			o.region                 = kwargs.get('region',                 None)
			o.responsible            = kwargs.get('responsible',            None)
			o.specialised            = kwargs.get('specialised',            None)
			o.contact_person         = kwargs.get('contact_person',         None)
			o.placing_way            = kwargs.get('placing_way',            None)
			o.grant_start_time       = kwargs.get('grant_start_time',       None)
			o.grant_end_time         = kwargs.get('grant_end_time',         None)
			o.collecting_start_time  = kwargs.get('collecting_start_time',  None)
			o.collecting_end_time    = kwargs.get('collecting_end_time',    None)
			o.opening_time           = kwargs.get('opening_time',           None)
			o.prequalification_time  = kwargs.get('prequalification_time',  None)
			o.scoring_time           = kwargs.get('scoring_time',           None)
			o.grant_place            = kwargs.get('grant_place',            None)
			o.collecting_place       = kwargs.get('collecting_place',       None)
			o.opening_place          = kwargs.get('opening_place',          None)
			o.prequalification_place = kwargs.get('prequalification_place', None)
			o.scoring_place          = kwargs.get('scoring_place',          None)
			o.etp                    = kwargs.get('etp',                    None)
			o.save()

		return o


	def update(self, number, **kwargs):

		if not number:
			return None

		o = self.take(number, **kwargs)
		o.name                   = kwargs.get('name',                   None)
		o.url                    = kwargs.get('url',                    None)
		o.published              = kwargs.get('published',              None)
		o.region                 = kwargs.get('region',                 None)
		o.responsible            = kwargs.get('responsible',            None)
		o.specialised            = kwargs.get('specialised',            None)
		o.contact_person         = kwargs.get('contact_person',         None)
		o.placing_way            = kwargs.get('placing_way',            None)
		o.grant_start_time       = kwargs.get('grant_start_time',       None)
		o.grant_end_time         = kwargs.get('grant_end_time',         None)
		o.collecting_start_time  = kwargs.get('collecting_start_time',  None)
		o.collecting_end_time    = kwargs.get('collecting_end_time',    None)
		o.opening_time           = kwargs.get('opening_time',           None)
		o.prequalification_time  = kwargs.get('prequalification_time',  None)
		o.scoring_time           = kwargs.get('scoring_time',           None)
		o.grant_place            = kwargs.get('grant_place',            None)
		o.collecting_place       = kwargs.get('collecting_place',       None)
		o.opening_place          = kwargs.get('opening_place',          None)
		o.prequalification_place = kwargs.get('prequalification_place', None)
		o.scoring_place          = kwargs.get('scoring_place',          None)
		o.etp                    = kwargs.get('etp',                    None)
		o.save()

		return o



class Purchase(models.Model):

	id                     = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	region                 = models.ForeignKey(Region,       on_delete = models.CASCADE, related_name = 'purchase_region',                 null = True, default = None)
	responsible            = models.ForeignKey(Organisation, on_delete = models.CASCADE, related_name = 'purchase_responsible',            null = True, default = None)
	specialised            = models.ForeignKey(Organisation, on_delete = models.CASCADE, related_name = 'purchase_specialised',            null = True, default = None)
	contact_person         = models.ForeignKey(Person,       on_delete = models.CASCADE, related_name = 'purchase_contact_person',         null = True, default = None)
	placing_way            = models.ForeignKey(PlacingWay,   on_delete = models.CASCADE, related_name = 'purchase_placing_way',            null = True, default = None)
	grant_place            = models.ForeignKey(Address,      on_delete = models.CASCADE, related_name = 'purchase_grant_place',            null = True, default = None)
	collecting_place       = models.ForeignKey(Address,      on_delete = models.CASCADE, related_name = 'purchase_collecting_place',       null = True, default = None)
	opening_place          = models.ForeignKey(Address,      on_delete = models.CASCADE, related_name = 'purchase_opening_place',          null = True, default = None)
	prequalification_place = models.ForeignKey(Address,      on_delete = models.CASCADE, related_name = 'purchase_prequalification_place', null = True, default = None)
	scoring_place          = models.ForeignKey(Address,      on_delete = models.CASCADE, related_name = 'purchase_scoring_place',          null = True, default = None)
	etp                    = models.ForeignKey(ETP,          on_delete = models.CASCADE, related_name = 'purchase_etp',                    null = True, default = None)

	number                = models.CharField(max_length = 50, unique = True)
	name                  = models.TextField(null = True, default = None)
	url                   = models.TextField(null = True, default = None)
	published             = models.DateTimeField(null = True, default = None, db_index = True)
	grant_start_time      = models.DateTimeField(null = True, default = None, db_index = True)
	grant_end_time        = models.DateTimeField(null = True, default = None, db_index = True)
	collecting_start_time = models.DateTimeField(null = True, default = None, db_index = True)
	collecting_end_time   = models.DateTimeField(null = True, default = None, db_index = True)
	opening_time          = models.DateTimeField(null = True, default = None, db_index = True)
	prequalification_time = models.DateTimeField(null = True, default = None, db_index = True)
	scoring_time          = models.DateTimeField(null = True, default = None, db_index = True)
	state                 = models.BooleanField(default = True, db_index = True)

	attachments = models.ManyToManyField(Attachment, through = 'PurchaseToAttachment', through_fields = ('purchase', 'attachment'))

	objects        = PurchaseManager()

	def cancel(self):
		self.state    = False
		self.save()

	def __str__(self):
		return "Закупка: {} {} ".format(self.region, self.number)

	class Meta:
		ordering = ['number']



class PurchaseToAttachment(models.Model):

	id         = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	purchase   = models.ForeignKey(Purchase,   on_delete = models.CASCADE)
	attachment = models.ForeignKey(Attachment, on_delete = models.CASCADE)

	class Meta:
		db_table = 'tenders_purchase_to_attachment'



class NotificationManager(models.Manager):

	def take(self, oss_id, **kwargs):

		if not oss_id:
			return None

		try:
			o = self.get(oss_id = oss_id)

		except Exception:
			o = Notification()
			o.oss_id   = oss_id
			o.url      = kwargs.get('url', None)
			o.purchase = kwargs.get('purchase', None)
			o.save()

		return o



class Notification(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	oss_id   = models.BigIntegerField(null = True, default = None, db_index = True)
	purchase = models.ForeignKey(Purchase, on_delete = models.CASCADE, null = True, default = None)

	url      = models.TextField(null = True, default = None)

	objects = NotificationManager()


	def __str__(self):
		return "Уведомление: {}".format(self.oss_id)



	class Meta:
		ordering = ['oss_id']



class LotManager(models.Manager):


	def take(self, purchase, number = None, **kwargs):

		if not purchase:
			return None

		try:
			o = self.get(purchase = purchase, number = number)

		except Exception:
			o = Lot()
			o.name           = kwargs.get('name', None)
			o.finance_source = kwargs.get('finance_source', None)
			o.max_price      = kwargs.get('max_price', None)
			o.currency       = kwargs.get('currency', None)

			o.save()

		return o


	def update(self, purchase, number = None, **kwargs):

		if not purchase:
			return None

		o = self.take(purchase, number = None, **kwargs)
		o.name           = kwargs.get('name',           None)
		o.finance_source = kwargs.get('finance_source', None)
		o.max_price      = kwargs.get('max_price',      None)
		o.currency       = kwargs.get('currency',       None)
		o.save()

		return o



class Lot(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	purchase = models.ForeignKey(Purchase, null = True, default = None, on_delete = models.CASCADE)
	currency = models.ForeignKey(Currency, null = True, default = None, on_delete = models.CASCADE)

	number         = models.IntegerField(null = True, default = None, db_index = True)
	name           = models.TextField(null = True, default = None)
	finance_source = models.TextField(null = True, default = None)
	max_price      = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)

	products  = models.ManyToManyField(Product,      through = 'LotToProduct',  through_fields = ('lot', 'product'))
	customers = models.ManyToManyField(Organisation, through = 'LotToCustomer', through_fields = ('lot', 'customer'))

	objects = LotManager()

	def __str__(self):
		return "Lot: {}".format(self.id)



class LotToProduct(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	lot      = models.ForeignKey(Lot,     on_delete = models.CASCADE)
	product  = models.ForeignKey(Product, on_delete = models.CASCADE)
	okei     = models.ForeignKey(OKEI,     null = True, default = None, on_delete = models.CASCADE)
	currency = models.ForeignKey(Currency, null = True, default = None, on_delete = models.CASCADE)

	quantity = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	price    = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	total    = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)

	created  = models.DateTimeField(default = timezone.now)

	class Meta:
		db_table = 'tenders_lot_to_product'



class LotToCustomer(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	lot      = models.ForeignKey(Lot,          on_delete = models.CASCADE)
	customer = models.ForeignKey(Organisation, on_delete = models.CASCADE)

	class Meta:
		db_table = 'tenders_lot_to_customer'



class Contract(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	purchase = models.ForeignKey(Purchase, null = True, default = None, on_delete = models.CASCADE)
	currency = models.ForeignKey(Currency, null = True, default = None, on_delete = models.CASCADE)
	customer = models.ForeignKey(Organisation, null = True, default = None, on_delete = models.CASCADE)

	number         = models.CharField(max_length = 50, null = True, default = None, db_index = True)
	finance_source = models.TextField(null = True, default = None)
	max_price      = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)





