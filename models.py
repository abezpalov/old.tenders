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
	updated  = models.DateTimeField(default = timezone.now)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

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

	state       = models.BooleanField(default = False, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects = SourceManager()


	def is_parsed(self):

		if self.state:
			print("Обработан: {}.".format(self.url))
			return True
		else:
			return False


	def complite(self, updater = None):

		from project.models import Log

		if updater:
			subject = 'tenders.updater.{}'.format(updater.alias)
		else:
			subject = 'source.complite'

		Log.objects.add(
			subject     = subject,
			channel     = 'info',
			title       = 'complite',
			description = self.url)

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

	state       = models.BooleanField(default = False, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

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


	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if o.full_name != kwargs.get('full_name', None):
			o.full_name = kwargs.get('full_name', None)
			need_save = True

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if kwargs.get('name', None) and o.name != kwargs.get('name'):
			o.name = kwargs.get('name')
			need_save = True
		elif o.name != kwargs.get('full_name', None):
			o.name = kwargs.get('full_name', None)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class Country(models.Model):

	id        = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code      = models.CharField(max_length = 10, unique = True)
	full_name = models.TextField(null = True, default = None)
	name      = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

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


	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if o.digital_code != kwargs.get('digital_code', None):
			o.digital_code = kwargs.get('digital_code', None)
			need_save = True

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o


class Currency(models.Model):

	id           = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code         = models.CharField(max_length = 10, unique = True)
	digital_code = models.CharField(max_length = 10, unique = True)
	name         = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

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


	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKEISection(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code     = models.CharField(max_length = 10, unique = True)
	name     = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

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


	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKEIGroup(models.Model):

	id      = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code    = models.CharField(max_length = 10, unique = True)
	name    = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

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
			o.code = code[:10]
			if kwargs.get('name', None):
				o.name = kwargs.get('name', None)
			if kwargs.get('section', None):
				o.section = kwargs.get('section', None)
			if kwargs.get('group', None):
				o.group = kwargs.get('group', None)
			if kwargs.get('local_name', None):
				o.local_name = kwargs.get('local_name', None)
			if kwargs.get('international_name', None):
				o.international_name = kwargs.get('international_name', None)
			if kwargs.get('symbol', None):
				o.symbol = kwargs.get('symbol', None)
			if kwargs.get('local_symbol', None):
				o.local_symbol = kwargs.get('local_symbol', None)
			if kwargs.get('international_symbol', None):
				o.international_symbol = kwargs.get('international_symbol', None)
			o.state = kwargs.get('state', True)
			o.save()

		return o

	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if kwargs.get('name', None) and o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if kwargs.get('section', None) and o.section != kwargs.get('section', None):
			o.section = kwargs.get('section', None)
			need_save = True

		if kwargs.get('group', None) and o.group != kwargs.get('group', None):
			o.group = kwargs.get('group', None)
			need_save = True

		if kwargs.get('local_name', None) and o.local_name != kwargs.get('local_name', None):
			o.local_name = kwargs.get('local_name', None)
			need_save = True

		if kwargs.get('international_name', None) and o.international_name != kwargs.get('international_name', None):
			o.international_name = kwargs.get('international_name', None)
			need_save = True

		if kwargs.get('symbol', None) and o.symbol != kwargs.get('symbol', None):
			o.symbol = kwargs.get('symbol', None)
			need_save = True

		if kwargs.get('local_symbol', None) and o.local_symbol != kwargs.get('local_symbol', None):
			o.local_symbol = kwargs.get('local_symbol', None)
			need_save = True

		if kwargs.get('international_symbol', None) and o.international_symbol != kwargs.get('international_symbol', None):
			o.international_symbol = kwargs.get('international_symbol', None)
			need_save = True

		if o.state != kwargs.get('state', True):
			o.state = True
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKEI(models.Model):

	id                   = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	section              = models.ForeignKey(OKEISection, related_name='+', on_delete = models.CASCADE, null = True, default = None)
	group                = models.ForeignKey(OKEIGroup,   related_name='+', on_delete = models.CASCADE, null = True, default = None)

	code                 = models.CharField(max_length = 10, unique = True)
	name                 = models.TextField(null = True, default = None)
	local_name           = models.TextField(null = True, default = None)
	international_name   = models.TextField(null = True, default = None)
	symbol               = models.TextField(null = True, default = None)
	local_symbol         = models.TextField(null = True, default = None)
	international_symbol = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects              = OKEIManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['code']



class OKEIExtKeyManager(models.Manager):


	def take(self, updater, ext_key, okei = None):

		if not updater or not ext_key:
			return None

		try:
			o = self.get(updater = updater, ext_key = ext_key)

		except OKEIExtKey.DoesNotExist:

			if okei:
				o = OKEIExtKey()
				o.updater = updater
				o.ext_key = ext_key
				o.okei    = okei
				o.save()
			else:
				return None

		return o


	def write(self, updater, ext_key, okei):

		if not updater or not ext_key or not okei:
			return None

		need_save = False

		o = self.take(updater, ext_key, okei)

		if o.okei != okei:
			o.okei = okei
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKEIExtKey(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	updater  = models.ForeignKey(Updater, related_name='+', on_delete = models.CASCADE)
	okei     = models.ForeignKey(OKEI,    related_name='+', on_delete = models.CASCADE)

	ext_key  = models.CharField(max_length = 50, null = True, default = None, db_index = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects  = OKEIExtKeyManager()

	def __str__(self):
		return "{}".format(self.ext_key)

	class Meta:
		db_table        = 'tenders_okei_ext_key'
		ordering        = ['ext_key']
		unique_together = ('updater', 'ext_key')



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


	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if o.parent != kwargs.get('parent', None):
			o.parent = kwargs.get('parent', None)
			need_save = True

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state',  True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class KOSGU(models.Model):

	id          = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	parent      = models.ForeignKey('self', related_name='+', on_delete = models.CASCADE, null = True, default = None)

	code        = models.CharField(max_length = 10, unique = True)
	name        = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

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


	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if o.full_name != kwargs.get('full_name', None):
			o.full_name = kwargs.get('full_name', None)
			need_save = True

		if o.singular_name != kwargs.get('singular_name', None):
			o.singular_name = kwargs.get('singular_name', None)
			need_save = True
		if o.parent != kwargs.get('parent', None):
			o.parent = kwargs.get('parent', None)
			need_save = True

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKOPF(models.Model):

	id            = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	parent        = models.ForeignKey('self', related_name='+', on_delete = models.CASCADE, null = True, default = None)

	code          = models.CharField(max_length = 10, unique = True)
	full_name     = models.TextField(null = True, default = None)
	singular_name = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects       = OKOPFManager()

	def __str__(self):
		return "{} {}".format(self.code, self.full_name)

	class Meta:
		ordering = ['code']



class OKDPManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except OKDP.DoesNotExist:
			o = OKDP()
			o.code   = code[:50]
			o.name   = kwargs.get('name',   None)
			o.parent = kwargs.get('parent', None)
			o.state  = kwargs.get('state',  True)
			o.save()

		return o


	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			nedd_save = True

		if o.parent != kwargs.get('parent', None):
			o.parent = kwargs.get('parent', None)
			need_Save = True

		if o.state != kwargs.get('state',  True):
			o.state = kwargs.get('state',  True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKDP(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	parent   = models.ForeignKey('self', related_name='+', on_delete = models.CASCADE, null = True, default = None)

	code     = models.CharField(max_length = 50, null = True, default = None, unique = True)
	name     = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects  = OKDPManager()

	def __str__(self):
		return "{}".format(self.code)

	class Meta:
		ordering = ['code']


class OKDPExtKeyManager(models.Manager):


	def take(self, updater, ext_key, okdp = None):

		if not updater or not ext_key:
			return None

		try:
			o = self.get(updater = updater, ext_key = ext_key)

		except OKDPExtKey.DoesNotExist:

			if okdp:
				o = OKDPExtKey()
				o.updater = updater
				o.ext_key = ext_key
				o.okdp    = okdp
				o.save()
			else:
				return None

		return o


	def write(self, updater, ext_key, okdp):

		if not updater or not ext_key or not okdp:
			return None

		need_save = False

		o = self.take(updater, ext_key, okdp)

		if o.okdp != okdp:
			o.okdp = okdp
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKDPExtKey(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	updater  = models.ForeignKey(Updater, related_name='+', on_delete = models.CASCADE)
	okdp     = models.ForeignKey(OKDP,    related_name='+', on_delete = models.CASCADE)

	ext_key  = models.CharField(max_length = 50, null = True, default = None, db_index = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects  = OKDPExtKeyManager()

	def __str__(self):
		return "{}".format(self.ext_key)

	class Meta:
		db_table        = 'tenders_okdp_ext_key'
		ordering        = ['ext_key']
		unique_together = ('updater', 'ext_key')



class OKPDManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except OKPD.DoesNotExist:
			o = OKPD()
			o.code   = code[:50]
			o.name   = kwargs.get('name',   None)
			o.parent = kwargs.get('parent', None)
			o.state  = kwargs.get('state',  True)
			o.save()

		return o


	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if o.parent != kwargs.get('parent', None):
			o.parent = kwargs.get('parent', None)
			need_save = True

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKPD(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	parent   = models.ForeignKey('self', related_name='+', on_delete = models.CASCADE, null = True, default = None)

	code     = models.CharField(max_length = 50, null = True, default = None, unique = True)
	name     = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects  = OKPDManager()

	def __str__(self):
		return "{}".format(self.code)

	class Meta:
		ordering = ['code']


class OKPDExtKeyManager(models.Manager):


	def take(self, updater, ext_key, okpd = None):

		if not updater or not ext_key:
			return None

		try:
			o = self.get(updater = updater, ext_key = ext_key)

		except OKPDExtKey.DoesNotExist:

			if okpd:
				o = OKPDExtKey()
				o.updater = updater
				o.ext_key = ext_key
				o.okpd    = okpd
				o.save()
			else:
				return None

		return o


	def write(self, updater, ext_key, okpd):

		if not updater or not ext_key or not okpd:
			return None

		need_save = False

		o = self.take(updater, ext_key, okpd)

		if o.okpd != okpd:
			o.okpd = okpd
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKPDExtKey(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	updater  = models.ForeignKey(Updater, related_name='+', on_delete = models.CASCADE)
	okpd     = models.ForeignKey(OKPD,    related_name='+', on_delete = models.CASCADE)

	ext_key  = models.CharField(max_length = 50, null = True, default = None, db_index = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects  = OKPDExtKeyManager()

	def __str__(self):
		return "{}".format(self.ext_key)

	class Meta:
		db_table        = 'tenders_okpd_ext_key'
		ordering        = ['ext_key']
		unique_together = ('updater', 'ext_key')



class OKPD2Manager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except OKPD2.DoesNotExist:
			o = OKPD2()
			o.code     = code[:50]
			o.name     = kwargs.get('name',   None)
			o.parent   = kwargs.get('parent', None)
			o.state    = kwargs.get('state',  True)
			o.save()

		return o


	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if o.parent != kwargs.get('parent', None):
			o.parent = kwargs.get('parent', None)
			need_save = True

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKPD2(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	parent   = models.ForeignKey('self', related_name='+', on_delete = models.CASCADE, null = True, default = None)

	code     = models.CharField(max_length = 50, null = True, default = None, unique = True)
	name     = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects  = OKPD2Manager()

	def __str__(self):
		return "{}".format(self.code)

	class Meta:
		ordering = ['code']



class OKPD2ExtKeyManager(models.Manager):


	def take(self, updater, ext_key, okpd2 = None):

		if not updater or not ext_key:
			return None

		try:
			o = self.get(updater = updater, ext_key = ext_key)

		except OKPD2ExtKey.DoesNotExist:

			if okpd2:
				o = OKPD2ExtKey()
				o.updater = updater
				o.ext_key = ext_key
				o.okpd2   = okpd2
				o.save()
			else:
				return None

		return o


	def write(self, updater, ext_key, okpd2):

		if not updater or not ext_key or not okpd2:
			return None

		need_save = False

		o = self.take(updater, ext_key, okpd2)

		if o.okpd2 != okpd2:
			o.okpd2 = okpd2
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKPD2ExtKey(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	updater  = models.ForeignKey(Updater, related_name='+', on_delete = models.CASCADE)
	okpd2    = models.ForeignKey(OKPD2,   related_name='+', on_delete = models.CASCADE)

	ext_key  = models.CharField(max_length = 50, null = True, default = None, db_index = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects  = OKPD2ExtKeyManager()

	def __str__(self):
		return "{}".format(self.ext_key)

	class Meta:
		db_table        = 'tenders_okpd2_ext_key'
		ordering        = ['ext_key']
		unique_together = ('updater', 'ext_key')



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


	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if o.parent != kwargs.get('parent', None):
			o.parent = kwargs.get('parent', None)
			need_save = True

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKTMO(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	parent   = models.ForeignKey('self', related_name='+', on_delete = models.CASCADE, null = True, default = None)

	code     = models.CharField(max_length = 20, unique = True)
	name     = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects = OKTMOManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class OKATOManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except OKATO.DoesNotExist:
			o = OKATO()
			o.code   = code[:20]
			o.name   = kwargs.get('name',   None)
			o.parent = kwargs.get('parent', None)
			o.state  = kwargs.get('state',  True)
			o.save()

		return o


	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if o.parent != kwargs.get('parent', None):
			o.parent = kwargs.get('parent', None)
			need_save = True

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKATO(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	parent   = models.ForeignKey('self', related_name='+', on_delete = models.CASCADE, null = True, default = None)

	code     = models.CharField(max_length = 20, unique = True)
	name     = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects = OKATOManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class OKATOExtKeyManager(models.Manager):


	def take(self, updater, ext_key, okato = None):

		if not updater or not ext_key:
			return None

		try:
			o = self.get(updater = updater, ext_key = ext_key)

		except OKATOExtKey.DoesNotExist:

			if okato:
				o = OKATOExtKey()
				o.updater = updater
				o.ext_key = ext_key
				o.okato   = okato
				o.save()
			else:
				return None

		return o


	def write(self, updater, ext_key, okato):

		if not updater or not ext_key or not okato:
			return None

		need_save = False

		o = self.take(updater, ext_key, okato)

		if o.okato != okato:
			o.okato = okato
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKATOExtKey(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	updater  = models.ForeignKey(Updater, related_name='+', on_delete = models.CASCADE)
	okato    = models.ForeignKey(OKATO,   related_name='+', on_delete = models.CASCADE)

	ext_key  = models.CharField(max_length = 50, null = True, default = None, db_index = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects  = OKATOExtKeyManager()

	def __str__(self):
		return "{}".format(self.ext_key)

	class Meta:
		db_table        = 'tenders_okato_ext_key'
		ordering        = ['ext_key']
		unique_together = ('updater', 'ext_key')



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

	def write(self, name, **kwargs):

		if not name:
			return None

		need_save = False

		o = self.take(name, **kwargs)

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKVEDSection(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	name     = models.TextField(unique = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

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


	def write(self, name, **kwargs):

		if not name:
			return None

		need_save = False

		o = self.take(name, **kwargs)

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKVEDSubSection(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	name     = models.TextField(unique = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects  = OKVEDSubSectionManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['name']



class OKVEDManager(models.Manager):

	def take(self, code, **kwargs):


		if not code:
			return None

		try:
			o = self.get(code = code)

		except OKVED.DoesNotExist:
			o = OKVED()
			o.code       = code[:100]
			o.section    = kwargs.get('section',    None)
			o.subsection = kwargs.get('subsection', None)
			o.parent     = kwargs.get('parent',     None)
			o.name       = kwargs.get('name',       None)
			o.state      = kwargs.get('state',      True)
			o.save()

		return o

	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if o.code != code[:100]:
			o.code = code[:100]
			need_save = True

		if o.section != kwargs.get('section', None):
			o.section = kwargs.get('section', None)
			need_save = True

		if o.subsection != kwargs.get('subsection', None):
			o.subsection = kwargs.get('subsection', None)
			need_save = True

		if o.parent != kwargs.get('parent', None):
			o.parent = kwargs.get('parent', None)
			need_save = True

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKVED(models.Model):

	id         = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	section    = models.ForeignKey(OKVEDSection,    related_name='+', on_delete = models.CASCADE, null = True, default = None)
	subsection = models.ForeignKey(OKVEDSubSection, related_name='+', on_delete = models.CASCADE, null = True, default = None)
	parent     = models.ForeignKey('self',          related_name='+', on_delete = models.CASCADE, null = True, default = None)

	code       = models.CharField(max_length = 100, null = True, default = None, db_index = True)
	name       = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects = OKVEDManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class OKVEDExtKeyManager(models.Manager):


	def take(self, updater, ext_key, okved = None):

		if not updater or not ext_key:
			return None

		try:
			o = self.get(updater = updater, ext_key = ext_key)

		except OKVEDExtKey.DoesNotExist:

			if okved:
				o = OKVEDExtKey()
				o.updater = updater
				o.ext_key = ext_key
				o.okved   = okved
				o.save()
			else:
				return None

		return o


	def write(self, updater, ext_key, okved):

		if not updater or not ext_key or not okved:
			return None

		need_save = False

		o = self.take(updater, ext_key, okved)

		if o.okved != okved:
			o.okved = okved
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKVEDExtKey(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	updater  = models.ForeignKey(Updater, related_name='+', on_delete = models.CASCADE)
	okved    = models.ForeignKey(OKVED,   related_name='+', on_delete = models.CASCADE)

	ext_key  = models.CharField(max_length = 50, null = True, default = None, db_index = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects  = OKVEDExtKeyManager()

	def __str__(self):
		return "{}".format(self.ext_key)

	class Meta:
		db_table        = 'tenders_okved_ext_key'
		ordering        = ['ext_key']
		unique_together = ('updater', 'ext_key')



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


	def write(self, name, state = True):

		if not name:
			return None

		need_save = False

		o = self.take(name, **kwargs)

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()


		return o



class OKVED2Section(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	name     = models.TextField(unique = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects = OKVED2SectionManager()


	def __str__(self):
		return "{}".format(self.name)



	class Meta:
		ordering = ['name']



class OKVED2Manager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except OKVED2.DoesNotExist:
			o = OKVED2()
			o.code    = code[:100]
			o.section = kwargs.get('section', None)
			o.parent  = kwargs.get('parent',  None)
			o.name    = kwargs.get('name',    None)
			o.comment = kwargs.get('comment', None)
			o.state   = kwargs.get('state',   True)
			o.save()

		return o


	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if o.section != kwargs.get('section', None):
			o.section = kwargs.get('section', None)
			need_save = True

		if o.parent != kwargs.get('parent', None):
			o.parent = kwargs.get('parent', None)
			need_save = True

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if o.comment != kwargs.get('comment', None):
			o.comment = kwargs.get('comment', None)
			need_save = True

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKVED2(models.Model):

	id      = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	section = models.ForeignKey(OKVED2Section, related_name='+', on_delete = models.CASCADE, null = True, default = None)
	parent  = models.ForeignKey('self',        related_name='+', on_delete = models.CASCADE, null = True, default = None)

	code    = models.CharField(max_length = 100, null = True, default = None, unique = True)
	name    = models.TextField(null = True, default = None)
	comment = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects = OKVED2Manager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class OKVED2ExtKeyManager(models.Manager):


	def take(self, updater, ext_key, okved2 = None):

		if not updater or not ext_key:
			return None

		try:
			o = self.get(updater = updater, ext_key = ext_key)

		except OKVED2ExtKey.DoesNotExist:

			if okved2:
				o = OKVED2ExtKey()
				o.updater = updater
				o.ext_key = ext_key
				o.okved2  = okved2
				o.save()
			else:
				return None

		return o


	def write(self, updater, ext_key, okved2):

		if not updater or not ext_key or not okved2:
			return None

		need_save = False

		o = self.take(updater, ext_key, okved2)

		if o.okved2 != okved2:
			o.okved2 = okved2
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OKVED2ExtKey(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	updater  = models.ForeignKey(Updater, related_name='+', on_delete = models.CASCADE)
	okved2   = models.ForeignKey(OKVED2,  related_name='+', on_delete = models.CASCADE)

	ext_key  = models.CharField(max_length = 50, null = True, default = None, db_index = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects  = OKVED2ExtKeyManager()

	def __str__(self):
		return "{}".format(self.ext_key)

	class Meta:
		db_table        = 'tenders_okved2_ext_key'
		ordering        = ['ext_key']
		unique_together = ('updater', 'ext_key')



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


	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class Budget(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code     = models.CharField(max_length = 20, unique = True)
	name     = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

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

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

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


	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if o.subsystem_type != kwargs.get('subsystem_type', None):
			o.subsystem_type = kwargs.get('subsystem_type', None)
			need_save = True

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o


class BudgetType(models.Model):

	id             = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	subsystem_type = models.ForeignKey(SubsystemType, related_name='+', on_delete = models.CASCADE, null = True, default = None)

	code           = models.CharField(max_length = 20, unique = True)
	name           = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

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


#	def write(self, code, **kwargs):
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
#	budget     = models.ForeignKey(Budget, related_name='+', on_delete = models.CASCADE, null = True, default = None)
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

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

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

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

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

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

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

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

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

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects = PhoneManager()

	def __str__(self):
		return "{}".format(self.phone)

	class Meta:
		ordering = ['phone']



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
#	address  = models.ForeignKey(Address, related_name='+', on_delete = models.CASCADE, null = True, default = None)
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
#	bank             = models.ForeignKey(Bank, related_name='+', on_delete = models.CASCADE, null = True, default = None)
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

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

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


	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code = code)

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if o.description != kwargs.get('description', None):
			o.description = kwargs.get('description', None)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class OrganisationType(models.Model):

	id          = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code        = models.CharField(max_length = 20, unique = True)
	name        = models.TextField(null = True, default = None)
	description = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects     = OrganisationTypeManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class PersonManager(models.Manager):


	def take(self, first_name, middle_name, last_name, email = None, **kwargs):

		try:
			o = self.get(first_name = first_name, middle_name = middle_name, last_name = last_name, email = email)
		except Exception:
			o = Person()
			o.first_name   = first_name
			o.middle_name  = middle_name
			o.last_name    = last_name
			o.email        = email
			o.phone        = kwargs.get('phone', None)
			o.fax          = kwargs.get('fax',   None)
			o.state        = kwargs.get('state', True)
			o.save()

		return o



class Person(models.Model):

	id           = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	email        = models.ForeignKey(Email,        related_name='+', on_delete = models.CASCADE, null = True, default = None)
	phone        = models.ForeignKey(Phone,        related_name='+', on_delete = models.CASCADE, null = True, default = None)
	fax          = models.ForeignKey(Phone,        related_name='+', on_delete = models.CASCADE, null = True, default = None)

	first_name  = models.TextField(null = True, default = None, db_index = True)
	middle_name = models.TextField(null = True, default = None, db_index = True)
	last_name   = models.TextField(null = True, default = None, db_index = True)
	position    = models.TextField(null = True, default = None)
	description = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects = PersonManager()


	def __str__(self):
		return "{} {} {}".format(self.first_name, self.middle_name, self.last_name)



	class Meta:
		ordering = ['first_name', 'middle_name', 'last_name']




class OrganisationManager(models.Manager):


	def take(self, inn, kpp = None, **kwargs):

		if not inn:
			return None

		try:
			o = self.get(inn = inn, kpp = kpp)

		except Organisation.DoesNotExist:
			o = Organisation()
			o.inn = inn
			o.kpp = kpp

			if kwargs.get('state', True) or not o.state:

				if kwargs.get('short_name', None):
					o.short_name = kwargs.get('short_name', None)

				if kwargs.get('full_name', None):
					o.full_name = kwargs.get('full_name', None)

				if kwargs.get('ogrn', None):
					o.ogrn = kwargs.get('ogrn', None)

				if kwargs.get('okpo', None):
					o.okpo = kwargs.get('okpo', None)

				if kwargs.get('factual_address', None):
					o.factual_address = kwargs.get('factual_address', None)

				if kwargs.get('postal_address', None):
					o.postal_address = kwargs.get('postal_address',    None)

				if kwargs.get('email', None):
					o.email = kwargs.get('email', None)

				if kwargs.get('phone', None):
					o.phone = kwargs.get('phone', None)

				if kwargs.get('fax', None):
					o.fax = kwargs.get('fax', None)

				if kwargs.get('contact_person', None):
					o.contact_person = kwargs.get('contact_person', None)

				if kwargs.get('head_agency', None):
					o.head_agency = kwargs.get('head_agency', None)

				if kwargs.get('ordering_agency', None):
					o.ordering_agency = kwargs.get('ordering_agency', None)

				if kwargs.get('okopf', None):
					o.okopf = kwargs.get('okopf', None)

				if kwargs.get('okogu', None):
					o.okogu = kwargs.get('okogu', None)

				if kwargs.get('organisation_role', None):
					o.organisation_role = kwargs.get('organisation_role', None)

				if kwargs.get('organisation_type', None):
					o.organisation_type = kwargs.get('organisation_type', None)

				if kwargs.get('oktmo', None):
					o.oktmo = kwargs.get('oktmo', None)

				if kwargs.get('state', False):
					o.state = kwargs.get('state', False)

				if kwargs.get('register', False):
					o.register = kwargs.get('register', False)

				if kwargs.get('name', None):
					o.name = kwargs.get('name', None)
				else:
					o.name = kwargs.get('full_name', None)

			o.save()

		return o


	def write(self, inn, kpp = None, **kwargs):

		if not inn:
			return None

		need_save = False

		o = self.take(inn, kpp, **kwargs)

		if kwargs.get('state', True) or not o.state:


			if kwargs.get('short_name', None) and o.short_name != kwargs.get('short_name', None):
				o.short_name = kwargs.get('short_name', None)
				need_save = True

			if kwargs.get('full_name', None):
				o.full_name = kwargs.get('full_name', None)
				need_save = True

			if kwargs.get('ogrn', None):
				o.ogrn = kwargs.get('ogrn', None)
				need_save = True

			if kwargs.get('okpo', None):
				o.okpo = kwargs.get('okpo', None)
				need_save = True

			if kwargs.get('factual_address', None):
				o.factual_address = kwargs.get('factual_address', None)
				need_save = True

			if kwargs.get('postal_address', None):
				o.postal_address = kwargs.get('postal_address',    None)
				need_save = True

			if kwargs.get('email', None):
				o.email = kwargs.get('email', None)
				need_save = True

			if kwargs.get('phone', None):
				o.phone = kwargs.get('phone', None)
				need_save = True

			if kwargs.get('fax', None):
				o.fax = kwargs.get('fax', None)
				need_save = True

			if kwargs.get('contact_person', None):
				o.contact_person = kwargs.get('contact_person', None)
				need_save = True

			if kwargs.get('head_agency', None):
				o.head_agency = kwargs.get('head_agency', None)
				need_save = True

			if kwargs.get('ordering_agency', None):
				o.ordering_agency = kwargs.get('ordering_agency', None)
				need_save = True

			if kwargs.get('okopf', None):
				o.okopf = kwargs.get('okopf', None)
				need_save = True

			if kwargs.get('okogu', None):
				o.okogu = kwargs.get('okogu', None)
				need_save = True

			if kwargs.get('organisation_role', None):
				o.organisation_role = kwargs.get('organisation_role', None)
				need_save = True

			if kwargs.get('organisation_type', None) and o.organisation_type != kwargs.get('organisation_type', None):
				o.organisation_type = kwargs.get('organisation_type', None)
				need_save = True

			if kwargs.get('oktmo', None) and o.oktmo != kwargs.get('oktmo', None):
				o.oktmo = kwargs.get('oktmo', None)
				need_save = True

			if kwargs.get('state', False) and o.state != kwargs.get('state', False):
				o.state = kwargs.get('state', False)
				need_save = True

			if kwargs.get('register', False) and o.register != kwargs.get('register', False):
				o.register = kwargs.get('register', False)
				need_save = True

			if kwargs.get('name', None) and o.name != kwargs.get('name', None):
				o.name = kwargs.get('name', None)
				need_save = True
			elif kwargs.get('full_name', None) and o.name != kwargs.get('full_name', None):
				o.name = kwargs.get('full_name', None)
				need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class Organisation(models.Model):

	id                = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	factual_address   = models.ForeignKey(Address,          related_name='+', on_delete = models.CASCADE, null = True, default = None)
	postal_address    = models.ForeignKey(Address,          related_name='+', on_delete = models.CASCADE, null = True, default = None)
	email             = models.ForeignKey(Email,            related_name='+', on_delete = models.CASCADE, null = True, default = None)
	phone             = models.ForeignKey(Phone,            related_name='+', on_delete = models.CASCADE, null = True, default = None)
	fax               = models.ForeignKey(Phone,            related_name='+', on_delete = models.CASCADE, null = True, default = None)
	contact_person    = models.ForeignKey(Person,           related_name='+', on_delete = models.CASCADE, null = True, default = None)
	head_agency       = models.ForeignKey('self',           related_name='+', on_delete = models.CASCADE, null = True, default = None)
	ordering_agency   = models.ForeignKey('self',           related_name='+', on_delete = models.CASCADE, null = True, default = None)
	okopf             = models.ForeignKey(OKOPF,            related_name='+', on_delete = models.CASCADE, null = True, default = None)
	okogu             = models.ForeignKey(OKOGU,            related_name='+', on_delete = models.CASCADE, null = True, default = None)
	organisation_role = models.ForeignKey(OrganisationRole, related_name='+', on_delete = models.CASCADE, null = True, default = None)
	organisation_type = models.ForeignKey(OrganisationType, related_name='+', on_delete = models.CASCADE, null = True, default = None)
	oktmo             = models.ForeignKey(OKTMO,            related_name='+', on_delete = models.CASCADE, null = True, default = None)

	name              = models.TextField(null = True, default = None, db_index = True)
	short_name        = models.TextField(null = True, default = None)
	full_name         = models.TextField(null = True, default = None)
	inn               = models.CharField(max_length = 20, null = True, default = None, db_index = True)
	kpp               = models.CharField(max_length = 20, null = True, default = None, db_index = True)
	ogrn              = models.CharField(max_length = 20, null = True, default = None)
	okpo              = models.CharField(max_length = 20, null = True, default = None)
	register          = models.BooleanField(default = False, db_index = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

# TODO сотрудники
#           = models.ManyToManyField(Account, through = 'OrganisationToAccount', through_fields = ('organisation', 'account'))
#	accounts          = models.ManyToManyField(Account, through = 'OrganisationToAccount', through_fields = ('organisation', 'account'))
#	budgets           = models.ManyToManyField(Budget,  through = 'OrganisationToBudget',  through_fields = ('organisation', 'budget'))
#	okveds            = models.ManyToManyField(OKVED,   through = 'OrganisationToOKVED',   through_fields = ('organisation', 'okved'))

	objects           = OrganisationManager()

	def __str__(self):
		return "{} {} {} {}".format(self.ogrn, self.inn, self.kpp, self.name)

	class Meta:
		ordering = ['name']
		unique_together = ('inn', 'kpp')




class OrganisationExtKeyManager(models.Manager):


	def take(self, updater, ext_key, organisation = None):

		if not updater or not ext_key:
			return None

		try:
			o = self.get(updater = updater, ext_key = ext_key)

		except OrganisationExtKey.DoesNotExist:

			if organisation:
				o = OrganisationExtKey()
				o.updater = updater
				o.ext_key = ext_key
				o.organisation  = organisation
				o.save()
			else:
				return None

		return o


	def write(self, updater, ext_key, organisation):

		if not updater or not ext_key or not organisation:
			return None

		need_save = False

		o = self.take(updater, ext_key, organisation)

		if o.organisation != organisation:
			o.organisation = organisation
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o

	def get_organisation(self, updater, ext_key):

		ext_key = self.take(updater = updater, ext_key = ext_key)

		if ext_key:
			return ext_key.organisation
		else:
			return None



class OrganisationExtKey(models.Model):

	id           = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	updater      = models.ForeignKey(Updater, related_name='+', on_delete = models.CASCADE)
	organisation = models.ForeignKey(Organisation,   related_name='+', on_delete = models.CASCADE)

	ext_key  = models.CharField(max_length = 50, null = True, default = None, db_index = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects  = OrganisationExtKeyManager()

	def __str__(self):
		return "{}".format(self.ext_key)

	class Meta:
		db_table        = 'tenders_organisation_ext_key'
		ordering        = ['ext_key']
		unique_together = ('updater', 'ext_key')



class PlacingWayManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)
		except Exception:
			o = PlacingWay()
			o.code = code
			if kwargs.get('state', False) or not o.state:
				if kwargs.get('name', None):
					o.name = kwargs.get('name', None)
				if kwargs.get('type_code', None):
					o.type_code = kwargs.get('type_code', None)
				if kwargs.get('subsystem_type', None):
					o.subsystem_type = kwargs.get('subsystem_type', None)
				o.state = kwargs.get('state', False)

			o.save()

		return o


	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if kwargs.get('state', False) or not o.state:

			if kwargs.get('name', None) and o.name != kwargs.get('name', None):
				o.name = kwargs.get('name', None)
				need_save = True

			if kwargs.get('type_code', None) and o.type_code != kwargs.get('type_code', None):
				o.type_code = kwargs.get('type_code', None)
				need_save = True

			if kwargs.get('subsystem_type', None) and o.subsystem_type != kwargs.get('subsystem_type', None):
				o.subsystem_type = kwargs.get('subsystem_type', None)
				need_save = True

			if o.state != kwargs.get('state', False):
				o.state = kwargs.get('state', False)
				need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class PlacingWay(models.Model):

	id             = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	subsystem_type = models.ForeignKey(SubsystemType, related_name='+', on_delete = models.CASCADE, null = True, default = None)

	code           = models.TextField(null = True, default = None, unique = True)
	name           = models.TextField(null = True, default = None)
	type_code      = models.CharField(max_length = 20, null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects = PlacingWayManager()

	def __str__(self):
		return "{} {}".format(self.code, self.name)

	class Meta:
		ordering = ['code']



class PlacingWayExtKeyManager(models.Manager):


	def take(self, updater, ext_key, placingway = None):

		if not updater or not ext_key:
			return None

		try:
			o = self.get(updater = updater, ext_key = ext_key)

		except PlacingWayExtKey.DoesNotExist:

			if placingway:
				o = PlacingWayExtKey()
				o.updater = updater
				o.ext_key = ext_key
				o.placingway = placingway
				o.save()
			else:
				return None

		return o


	def write(self, updater, ext_key, placingway):

		if not updater or not ext_key or not placingway:
			return None

		need_save = False

		o = self.take(updater, ext_key, placingway)

		if o.placingway != placingway:
			o.placingway = placingway

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class PlacingWayExtKey(models.Model):

	id         = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	updater    = models.ForeignKey(Updater, related_name='+', on_delete = models.CASCADE)
	placingway = models.ForeignKey(PlacingWay, related_name='+', on_delete = models.CASCADE)

	ext_key  = models.CharField(max_length = 50, null = True, default = None, db_index = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects  = PlacingWayExtKeyManager()

	def __str__(self):
		return "{}".format(self.ext_key)

	class Meta:
		db_table        = 'tenders_placingway_ext_key'
		ordering        = ['ext_key']
		unique_together = ('updater', 'ext_key')



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

	code     = models.TextField(null = True, default = None, unique = True)
	name     = models.TextField(null = True, default = None)
	url      = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects = ETPManager()

	def __str__(self):
		return "{} ({})".format(self.name, self.url)

	class Meta:
		ordering = ['name']



class PlanPositionChangeReasonManager(models.Manager):


	def take(self, name, **kwargs):

		if not name:
			return None

		try:
			o = self.get(name = name)

		except Exception:
			o = PlanPositionChangeReason()
			o.name = name
			if kwargs.get('state', True) or not o.state:
				if kwargs.get('description', None):
					o.description = kwargs.get('description', None)
				o.state = kwargs.get('state', True)

			o.save()

		return o


	def write(self, name, **kwargs):

		if not name:
			return None

		need_save = False

		o = self.take(name, **kwargs)

		if kwargs.get('state', True) or not o.state:

			if kwargs.get('description', None) and o.description != kwargs.get('description', None):
				o.description = kwargs.get('description', None)
				need_save = True

			if o.state != kwargs.get('state', True):
				o.state = kwargs.get('state', True)
				need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class PlanPositionChangeReason(models.Model):

	id          = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	name        = models.TextField(null = True, default = None, unique = True)
	description = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects     = PlanPositionChangeReasonManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['name']



class PlanPositionChangeReasonExtKeyManager(models.Manager):


	def take(self, updater, ext_key, planpositionchangereason = None):

		if not updater or not ext_key:
			return None

		try:
			o = self.get(updater = updater, ext_key = ext_key)

		except PlanPositionChangeReasonExtKey.DoesNotExist:

			if planpositionchangereason:
				o = PlanPositionChangeReasonExtKey()
				o.updater = updater
				o.ext_key = ext_key
				o.planpositionchangereason = planpositionchangereason
				o.save()
			else:
				return None

		return o


	def write(self, updater, ext_key, planpositionchangereason):

		if not updater or not ext_key or not planpositionchangereason:
			return None

		need_save = False

		o = self.take(updater, ext_key, planpositionchangereason)

		if o.planpositionchangereason != planpositionchangereason:
			o.planpositionchangereason = planpositionchangereason
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o


	def get_change_reason(self, updater, ext_key):

		ext_key = self.take(
			updater = updater,
			ext_key = ext_key)

		if ext_key:
			return ext_key.planpositionchangereason
		else:
			return None



class PlanPositionChangeReasonExtKey(models.Model):

	id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	updater = models.ForeignKey(Updater, related_name='+', on_delete = models.CASCADE)
	planpositionchangereason = models.ForeignKey(PlanPositionChangeReason, related_name='+', on_delete = models.CASCADE)

	ext_key = models.CharField(max_length = 50, null = True, default = None, db_index = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects = PlanPositionChangeReasonExtKeyManager()

	def __str__(self):
		return "{}".format(self.ext_key)

	class Meta:
		db_table        = 'tenders_planpositionchangereason_ext_key'
		ordering        = ['ext_key']
		unique_together = ('updater', 'ext_key')



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


	def write(self, code, **kwargs):

		if not code:
			return None

		need_save = False

		o = self.take(code, **kwargs)

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class ContractModificationReason(models.Model):

	id          = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	code        = models.TextField(unique = True)
	name        = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects     = ContractModificationReasonManager()

	def __str__(self):
		return "{} {}".format(self.id, self.name)

	class Meta:
		ordering = ['id']



#class KVRManager(models.Manager):

#	def take(self, code, **kwargs):
#		if not code:
#			return None
#		try:
#			o = self.get(code = code)
#		except Exception:
#			o = KVR()
#			o.code  = code
#			o.name  = kwargs.get('name',  None)
#			o.state = kwargs.get('state', True)
#			o.save()
#		return o

#	def write(self, code, **kwargs):
#		if not code:
#			return None
#		o = self.take(code, **kwargs)
#		o.name  = kwargs.get('name', None)
#		o.state = kwargs.get('state', True)
#		o.save()
#		return o



#class KVR(models.Model):

#	id          = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

#	code        = models.TextField(unique = True)
#	name        = models.TextField(null = True, default = None)
#	state       = models.BooleanField(default = True, db_index = True)

#	objects     = KVRManager()

#	def __str__(self):
#		return "{} {}".format(self.code, self.name)

#	class Meta:
#		ordering = ['code']



class PlanManager(models.Manager):


	def take(self, number, version, **kwargs):

		if not number or not version:
			return None

		try:
			o = self.get(number = number, version = version)

		except Exception:
			o = Plan()
			o.number         = number
			o.version        = version
			o.year           = kwargs.get('year',           None)
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


	def write(self, number, version, **kwargs):

		if not number or not version:
			return None

		need_save = False

		o = self.take(number, version, **kwargs)

		if o.year != kwargs.get('year', None):
			o.year = kwargs.get('year', None)
			need_save = True

		if o.description != kwargs.get('description', None):
			o.description = kwargs.get('description', None)
			need_save = True

		if o.url != kwargs.get('url', None):
			o.url = kwargs.get('url', None)
			need_save = True

		if o.region != kwargs.get('region', None):
			o.region = kwargs.get('region', None)
			need_save = True

		if o.owner != kwargs.get('owner', None):
			o.owner = kwargs.get('owner', None)
			need_save = True

		if o.customer != kwargs.get('customer', None):
			o.customer = kwargs.get('customer', None)
			need_save = True

		if o.contact_person != kwargs.get('contact_person', None):
			o.contact_person = kwargs.get('contact_person', None)
			need_save = True

		if o.state != kwargs.get('state', True):
			o.state = kwargs.get('state', True)
			need_save = True

		if o.created != kwargs.get('created', timezone.now()):
			o.created = kwargs.get('created', timezone.now())
			need_save = True

		if o.confirmed != kwargs.get('confirmed', None):
			o.confirmed = kwargs.get('confirmed', None)
			need_save = True

		if o.published != kwargs.get('published', None):
			o.published = kwargs.get('published', None)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		self.filter(number = o.number, version__lt = o.version).update(state = False)

		return o



class Plan(models.Model):

	id             = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	region         = models.ForeignKey(Region,       related_name='+', on_delete = models.CASCADE, null = True, default = None)
	owner          = models.ForeignKey(Organisation, related_name='+', on_delete = models.CASCADE, null = True, default = None)
	customer       = models.ForeignKey(Organisation, related_name='+', on_delete = models.CASCADE, null = True, default = None)
	contact_person = models.ForeignKey(Person,       related_name='+', on_delete = models.CASCADE, null = True, default = None)

	number         = models.CharField(max_length = 20, db_index = True)
	year           = models.IntegerField(null = True, default = None, db_index = True)
	version        = models.IntegerField(null = True, default = None, db_index = True)
	description    = models.TextField(null = True, default = None)
	url            = models.TextField(null = True, default = None, db_index = True)
	confirmed      = models.DateTimeField(null = True, default = None)
	published      = models.DateTimeField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)


	objects        = PlanManager()

	def __str__(self):
		return "{} {}".format(self.year, self.customer)

	class Meta:
		ordering = ['year', 'number', 'version']
		unique_together = ('number', 'version')


class PlanExtKeyManager(models.Manager):


	def take(self, updater, ext_key, plan = None):

		if not updater or not ext_key:
			return None

		try:
			o = self.get(updater = updater, ext_key = ext_key)

		except PlanExtKey.DoesNotExist:

			if plan:
				o = PlanExtKey()
				o.updater = updater
				o.ext_key = ext_key
				o.plan = plan
				o.save()
			else:
				return None

		return o


	def write(self, updater, ext_key, plan):

		if not updater or not ext_key or not plan:
			return None

		need_save = False

		o = self.take(updater, ext_key, plan)

		if o.plan != plan:
			o.plan = plan
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class PlanExtKey(models.Model):

	id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	updater = models.ForeignKey(Updater, related_name='+', on_delete = models.CASCADE)
	plan = models.ForeignKey(Plan, related_name='+', on_delete = models.CASCADE)

	ext_key = models.CharField(max_length = 50, null = True, default = None, db_index = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects = PlanExtKeyManager()

	def __str__(self):
		return "{}".format(self.ext_key)

	class Meta:
		db_table        = 'tenders_plan_ext_key'
		ordering        = ['ext_key']
		unique_together = ('updater', 'ext_key')



class ProductManager(models.Manager):


	def take(self, okdp = None, okpd = None, okpd2 = None, name = None):

		if not okdp and not okpd and not okpd2 and not name:
			return None

		try:
			o = self.get(okdp = okdp, okpd = okpd, okpd2 = okpd2, name = name)

		except Exception:
			o = Product()
			o.okdp  = okdp
			o.okpd  = okpd
			o.okpd2 = okpd2
			o.name  = name
			o.save()

		return o



class Product(models.Model):

	id    = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	okdp  = models.ForeignKey(OKDP,  related_name='+', on_delete = models.CASCADE, null = True, default = None)
	okpd  = models.ForeignKey(OKPD,  related_name='+', on_delete = models.CASCADE, null = True, default = None)
	okpd2 = models.ForeignKey(OKPD2, related_name='+', on_delete = models.CASCADE, null = True, default = None)

	name  = models.TextField(null = True, default = None, db_index = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects = ProductManager()

	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['name']
		unique_together = ('okdp', 'okpd', 'okpd2', 'name')



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


	def write(self, plan, number, **kwargs):

		if not plan or not number:
			return None

		need_save = False

		o = self.take(plan, number, **kwargs)

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if o.purchase_month != kwargs.get('purchase_month', None):
			o.purchase_month = kwargs.get('purchase_month', None)
			need_save = True

		if o.purchase_year != kwargs.get('purchase_year', None):
			o.purchase_year = kwargs.get('purchase_year', None)
			need_save = True

		if o.execution_month != kwargs.get('execution_month', None):
			o.execution_month = kwargs.get('execution_month', None)
			need_save = True

		if o.execution_year != kwargs.get('execution_year', None):
			o.execution_year = kwargs.get('execution_year', None)
			need_save = True

		if o.max_price != kwargs.get('max_price', None):
			o.max_price = kwargs.get('max_price', None)
			need_save = True

		if o.currency != kwargs.get('currency', None):
			o.currency = kwargs.get('currency', None)
			need_save = True

		if o.placing_way != kwargs.get('placing_way', None):
			o.placing_way = kwargs.get('placing_way', None)
			need_save = True

		if o.change_reason != kwargs.get('change_reason', None):
			o.change_reason = kwargs.get('change_reason', None)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class PlanPosition(models.Model):

	id            = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	plan          = models.ForeignKey(Plan,                     related_name='+', on_delete = models.CASCADE)
	currency      = models.ForeignKey(Currency,                 related_name='+', on_delete = models.CASCADE, null = True, default = None)
	placing_way   = models.ForeignKey(PlacingWay,               related_name='+', on_delete = models.CASCADE, null = True, default = None)
	change_reason = models.ForeignKey(PlanPositionChangeReason, related_name='+', on_delete = models.CASCADE, null = True, default = None)

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

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects = PlanPositionManager()

	def __str__(self):
		return "{} {}".format(self.number, self.name)

	def add_product(self, product, **kwargs):
		pass


class PlanPositionToOKVED(models.Model):

	id            = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	plan_position = models.ForeignKey(PlanPosition, related_name='+', on_delete = models.CASCADE)
	okved         = models.ForeignKey(OKVED,        related_name='+', on_delete = models.CASCADE)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	class Meta:
		db_table = 'tenders_planposition_to_okved'



class PlanPositionToOKVED2(models.Model):

	id            = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	plan_position = models.ForeignKey(PlanPosition, related_name='+', on_delete = models.CASCADE)
	okved2        = models.ForeignKey(OKVED2,       related_name='+', on_delete = models.CASCADE)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	class Meta:
		db_table = 'tenders_planposition_to_okved2'



class PlanPositionToProduct(models.Model):

	id            = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	plan_position = models.ForeignKey(PlanPosition, related_name='+', on_delete = models.CASCADE)
	product       = models.ForeignKey(Product,      related_name='+', on_delete = models.CASCADE, null = True, default = None)
	okei          = models.ForeignKey(OKEI,         related_name='+', on_delete = models.CASCADE, null = True, default = None)

	requirement   = models.TextField(null = True, default = None)
	quantity      = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	price         = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	total         = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None, db_index = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

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
			o.number = number
			o.save()

		return o


	def write(self, number, **kwargs):

		if not number:
			return None

		need_save = False

		o = self.take(number, **kwargs)


		if o.region != kwargs.get('region', None):
			o.region = kwargs.get('region', None)
			need_save = True

		if o.responsible != kwargs.get('responsible', None):
			o.responsible = kwargs.get('responsible', None)
			need_save = True

		if o.specialised != kwargs.get('specialised', None):
			o.specialised = kwargs.get('specialised', None)
			need_save = True

		if o.contact_person != kwargs.get('contact_person', None):
			o.contact_person = kwargs.get('contact_person', None)
			need_save = True

		if o.placing_way != kwargs.get('placing_way', None):
			o.placing_way = kwargs.get('placing_way', None)
			need_save = True

		if o.grant_place != kwargs.get('grant_place', None):
			o.grant_place = kwargs.get('grant_place', None)
			need_save = True

		if o.collecting_place != kwargs.get('collecting_place', None):
			o.collecting_place = kwargs.get('collecting_place', None)
			need_save = True

		if o.opening_place != kwargs.get('opening_place', None):
			o.opening_place = kwargs.get('opening_place', None)
			need_save = True

		if o.final_opening_place != kwargs.get('final_opening_place', None):
			o.final_opening_place = kwargs.get('final_opening_place', None)
			need_save = True

		if o.prequalification_place != kwargs.get('prequalification_place', None):
			o.prequalification_place = kwargs.get('prequalification_place', None)
			need_save = True

		if o.selecting_place != kwargs.get('selecting_place', None):
			o.selecting_place = kwargs.get('selecting_place', None)
			need_save = True

		if o.scoring_place != kwargs.get('scoring_place', None):
			o.scoring_place = kwargs.get('scoring_place', None)
			need_save = True

		if o.collecting_st1_place != kwargs.get('collecting_st1_place', None):
			o.collecting_st1_place = kwargs.get('collecting_st1_place', None)
			need_save = True

		if o.opening_st1_place != kwargs.get('opening_st1_place', None):
			o.opening_st1_place = kwargs.get('opening_st1_place', None)
			need_save = True

		if o.scoring_st1_place != kwargs.get('scoring_st1_place', None):
			o.scoring_st1_place = kwargs.get('scoring_st1_place', None)
			need_save = True

		if o.collecting_st2_place != kwargs.get('collecting_st2_place', None):
			o.collecting_st2_place = kwargs.get('collecting_st2_place', None)
			need_save = True

		if o.opening_st2_place != kwargs.get('opening_st2_place', None):
			o.opening_st2_place = kwargs.get('opening_st2_place', None)
			need_save = True

		if o.scoring_st2_place != kwargs.get('scoring_st2_place', None):
			o.scoring_st2_place = kwargs.get('scoring_st2_place', None)
			need_save = True

		if o.etp != kwargs.get('etp', None):
			o.etp = kwargs.get('etp', None)
			need_save = True

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if o.url != kwargs.get('url', None):
			o.url = kwargs.get('url', None)
			need_save = True

		if o.published != kwargs.get('published', None):
			o.published = kwargs.get('published', None)
			need_save = True

		if o.grant_start_time != kwargs.get('grant_start_time', None):
			o.grant_start_time = kwargs.get('grant_start_time', None)
			need_save = True

		if o.grant_end_time != kwargs.get('grant_end_time', None):
			o.grant_end_time = kwargs.get('grant_end_time', None)
			need_save = True

		if o.collecting_start_time != kwargs.get('collecting_start_time', None):
			o.collecting_start_time = kwargs.get('collecting_start_time', None)
			need_save = True

		if o.collecting_end_time != kwargs.get('collecting_end_time', None):
			o.collecting_end_time = kwargs.get('collecting_end_time', None)
			need_save = True

		if o.opening_time != kwargs.get('opening_time', None):
			o.opening_time = kwargs.get('opening_time', None)
			need_save = True

		if o.final_opening_time != kwargs.get('final_opening_time', None):
			o.final_opening_time = kwargs.get('final_opening_time', None)
			need_save = True

		if o.prequalification_time != kwargs.get('prequalification_time', None):
			o.prequalification_time = kwargs.get('prequalification_time', None)
			need_save = True

		if o.selecting_time != kwargs.get('selecting_time', None):
			o.selecting_time = kwargs.get('selecting_time', None)
			need_save = True

		if o.scoring_time != kwargs.get('scoring_time', None):
			o.scoring_time = kwargs.get('scoring_time', None)
			need_save = True

		if o.bidding_time != kwargs.get('bidding_time', None):
			o.bidding_time = kwargs.get('bidding_time', None)
			need_save = True

		if o.collecting_st1_start_time != kwargs.get('collecting_st1_start_time', None):
			o.collecting_st1_start_time = kwargs.get('collecting_st1_start_time', None)
			need_save = True

		if o.collecting_st1_end_time != kwargs.get('collecting_st1_end_time', None):
			o.collecting_st1_end_time = kwargs.get('collecting_st1_end_time', None)
			need_save = True

		if o.opening_st1_time != kwargs.get('opening_st1_time', None):
			o.opening_st1_time = kwargs.get('opening_st1_time', None)
			need_save = True

		if o.scoring_st1_time != kwargs.get('scoring_st1_time', None):
			o.scoring_st1_time = kwargs.get('scoring_st1_time', None)
			need_save = True

		if o.collecting_st2_start_time != kwargs.get('collecting_st2_start_time', None):
			o.collecting_st2_start_time = kwargs.get('collecting_st2_start_time', None)
			need_save = True

		if o.collecting_st2_end_time != kwargs.get('collecting_st2_end_time', None):
			o.collecting_st2_end_time = kwargs.get('collecting_st2_end_time', None)
			need_save = True

		if o.opening_st2_time != kwargs.get('opening_st2_time', None):
			o.opening_st2_time = kwargs.get('opening_st2_time', None)
			need_save = True

		if o.scoring_st2_time != kwargs.get('scoring_st2_time', None):
			o.scoring_st2_time = kwargs.get('scoring_st2_time', None)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class Purchase(models.Model):

	id                     = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	number                 = models.CharField(max_length = 50, unique = True)

	region                 = models.ForeignKey(Region,       related_name='+', on_delete = models.CASCADE, null = True, default = None)
	responsible            = models.ForeignKey(Organisation, related_name='+', on_delete = models.CASCADE, null = True, default = None)
	specialised            = models.ForeignKey(Organisation, related_name='+', on_delete = models.CASCADE, null = True, default = None)
	contact_person         = models.ForeignKey(Person,       related_name='+', on_delete = models.CASCADE, null = True, default = None)
	placing_way            = models.ForeignKey(PlacingWay,   related_name='+', on_delete = models.CASCADE, null = True, default = None)
	grant_place            = models.ForeignKey(Address,      related_name='+', on_delete = models.CASCADE, null = True, default = None)
	collecting_place       = models.ForeignKey(Address,      related_name='+', on_delete = models.CASCADE, null = True, default = None)
	opening_place          = models.ForeignKey(Address,      related_name='+', on_delete = models.CASCADE, null = True, default = None)
	final_opening_place    = models.ForeignKey(Address,      related_name='+', on_delete = models.CASCADE, null = True, default = None)
	prequalification_place = models.ForeignKey(Address,      related_name='+', on_delete = models.CASCADE, null = True, default = None)
	selecting_place        = models.ForeignKey(Address,      related_name='+', on_delete = models.CASCADE, null = True, default = None)
	scoring_place          = models.ForeignKey(Address,      related_name='+', on_delete = models.CASCADE, null = True, default = None)
	bidding_time           = models.ForeignKey(Address,      related_name='+', on_delete = models.CASCADE, null = True, default = None)
	collecting_st1_place   = models.ForeignKey(Address,      related_name='+', on_delete = models.CASCADE, null = True, default = None)
	opening_st1_place      = models.ForeignKey(Address,      related_name='+', on_delete = models.CASCADE, null = True, default = None)
	scoring_st1_place      = models.ForeignKey(Address,      related_name='+', on_delete = models.CASCADE, null = True, default = None)
	collecting_st2_place   = models.ForeignKey(Address,      related_name='+', on_delete = models.CASCADE, null = True, default = None)
	opening_st2_place      = models.ForeignKey(Address,      related_name='+', on_delete = models.CASCADE, null = True, default = None)
	scoring_st2_place      = models.ForeignKey(Address,      related_name='+', on_delete = models.CASCADE, null = True, default = None)
	etp                    = models.ForeignKey(ETP,          related_name='+', on_delete = models.CASCADE, null = True, default = None)

	name                   = models.TextField(null = True, default = None)
	url                    = models.TextField(null = True, default = None)
	published              = models.DateTimeField(null = True, default = None, db_index = True)
	grant_start_time       = models.DateTimeField(null = True, default = None, db_index = True)
	grant_end_time         = models.DateTimeField(null = True, default = None, db_index = True)
	collecting_start_time  = models.DateTimeField(null = True, default = None, db_index = True)
	collecting_end_time    = models.DateTimeField(null = True, default = None, db_index = True)
	opening_time           = models.DateTimeField(null = True, default = None, db_index = True)
	final_opening_time     = models.DateTimeField(null = True, default = None, db_index = True)
	prequalification_time  = models.DateTimeField(null = True, default = None, db_index = True)
	selecting_time         = models.DateTimeField(null = True, default = None, db_index = True)
	scoring_time           = models.DateTimeField(null = True, default = None, db_index = True)
	bidding_time           = models.DateTimeField(null = True, default = None, db_index = True)

	collecting_st1_start_time  = models.DateTimeField(null = True, default = None, db_index = True)
	collecting_st1_end_time    = models.DateTimeField(null = True, default = None, db_index = True)
	opening_st1_time           = models.DateTimeField(null = True, default = None, db_index = True)
	scoring_st1_time           = models.DateTimeField(null = True, default = None, db_index = True)
	collecting_st2_start_time  = models.DateTimeField(null = True, default = None, db_index = True)
	collecting_st2_end_time    = models.DateTimeField(null = True, default = None, db_index = True)
	opening_st2_time           = models.DateTimeField(null = True, default = None, db_index = True)
	scoring_st2_time           = models.DateTimeField(null = True, default = None, db_index = True)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	attachments = models.ManyToManyField(Attachment, through = 'PurchaseToAttachment', through_fields = ('purchase', 'attachment'))

	objects = PurchaseManager()

	def cancel(self):

		self.state = False
		self.save()

		Lot.objects.filter(purchase = self).update(state = False)

	def __str__(self):
		return "{} {}".format(self.region, self.number)

	class Meta:
		ordering = ['number']


class DocTypeManager(models.Manager):


	def take(self, code, **kwargs):

		if not code:
			return None

		try:
			o = self.get(code = code)

		except Exception:
			o = DocType()
			o.code = code
			o.name = kwargs.get('name', None)
			o.save()

		return o



class DocType(models.Model):

	id   = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	code = models.CharField(max_length = 50, db_index = True)
	name = models.TextField(null = True, default = None)

	state    = models.BooleanField(default = True, db_index = True)
	created  = models.DateTimeField(default = timezone.now, db_index = True)
	modified = models.DateTimeField(default = timezone.now, db_index = True)

	objects = DocTypeManager()



class PurchaseToAttachmentManager(models.Manager):

	def take(self, purchase, attachment, doc_type = None, **kwargs):

		if not purchase or not attachment:
			return None

		try:
			o = self.get(purchase = purchase, attachment = attachment)

		except Exception:
			o = DocType()
			o.purchase   = purchase
			o.attachment = attachment
			o.doc_type   = doc_type
			o.save()

		return o



	def write(self, purchase, attachment, doc_type = None, **kwargs):

		if not purchase or not attachment:
			return None

		need_save = False

		o = self.take(purchase, attachment, doc_type, **kwargs)

		if o.doc_type != kwargs.get('doc_type', None):
			o.doc_type = kwargs.get('doc_type', None)
			need_save = True

		if need_save:
			o.save()

		return o



class PurchaseToAttachment(models.Model):

	id         = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	purchase   = models.ForeignKey(Purchase,   related_name='+', on_delete = models.CASCADE)
	attachment = models.ForeignKey(Attachment, related_name='+', on_delete = models.CASCADE)
	doc_type   = models.ForeignKey(DocType,    related_name='+', on_delete = models.CASCADE)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects = PurchaseToAttachmentManager()

	class Meta:
		db_table = 'tenders_purchase_to_attachment'






# TODO
class NotificationManager(models.Manager):

	def take(self, updater, code, **kwargs):

		if not updater or not code:
			return None

		try:
			o = self.get(updater = updater, code = code)

		except Exception:
			o = Notification()
			o.updater  = updater
			o.code     = code
			o.url      = kwargs.get('url', None)
			o.purchase = kwargs.get('purchase', None)
			o.save()

		return o



class Notification(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

	updater  = models.ForeignKey(Updater,  related_name='+', on_delete = models.CASCADE, null = True, default = None)
	purchase = models.ForeignKey(Purchase, related_name='+', on_delete = models.CASCADE, null = True, default = None)

	code     = models.CharField(max_length = 50, null = True, default = None, db_index = True)
	url      = models.TextField(null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects = NotificationManager()


	def __str__(self):
		return "{}".format(self.code)



	class Meta:
		ordering = ['code']
		unique_together = ('updater', 'code')



class LotManager(models.Manager):


	def take(self, purchase, number = None, **kwargs):

		if not purchase:
			return None

		try:
			o = self.get(purchase = purchase, number = number)

		except Exception:
			o = Lot()
			o.purchase       = purchase
			o.number         = number
			o.name           = kwargs.get('name', None)
			o.finance_source = kwargs.get('finance_source', None)
			o.max_price      = kwargs.get('max_price', None)
			o.currency       = kwargs.get('currency', None)

			o.save()

		return o


	def write(self, purchase, number = None, **kwargs):

		if not purchase:
			return None

		need_save = False

		o = self.take(purchase, number = None, **kwargs)

		if o.name != kwargs.get('name', None):
			o.name = kwargs.get('name', None)
			need_save = True

		if o.finance_source != kwargs.get('finance_source', None):
			o.finance_source = kwargs.get('finance_source', None)
			need_save = True

		if o.max_price != kwargs.get('max_price', None):
			o.max_price = kwargs.get('max_price', None)
			need_save = True

		if o.currency != kwargs.get('currency', None):
			o.currency = kwargs.get('currency', None)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class Lot(models.Model):

	id             = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	purchase       = models.ForeignKey(Purchase, related_name='+', on_delete = models.CASCADE, null = True, default = None)
	currency       = models.ForeignKey(Currency, related_name='+', on_delete = models.CASCADE, null = True, default = None)

	number         = models.IntegerField(null = True, default = None, db_index = True)
	name           = models.TextField(null = True, default = None)
	finance_source = models.TextField(null = True, default = None)
	max_price      = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)

	products       = models.ManyToManyField(Product,      through = 'LotToProduct',  through_fields = ('lot', 'product'))
	customers      = models.ManyToManyField(Organisation, through = 'LotToCustomer', through_fields = ('lot', 'customer'))

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects        = LotManager()

	def __str__(self):
		return "Lot: {}".format(self.id)


	def cancel(self):
		self.update(state = False)



class LotToProduct(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	lot      = models.ForeignKey(Lot,      related_name='+', on_delete = models.CASCADE)
	product  = models.ForeignKey(Product,  related_name='+', on_delete = models.CASCADE)
	okei     = models.ForeignKey(OKEI,     related_name='+', on_delete = models.CASCADE, null = True, default = None)
	currency = models.ForeignKey(Currency, related_name='+', on_delete = models.CASCADE, null = True, default = None)

	quantity = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	price    = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	total    = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	class Meta:
		db_table = 'tenders_lot_to_product'



class LotToCustomer(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	lot      = models.ForeignKey(Lot,          related_name='+', on_delete = models.CASCADE)
	customer = models.ForeignKey(Organisation, related_name='+', on_delete = models.CASCADE)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	class Meta:
		db_table = 'tenders_lot_to_customer'


class ContractManager(models.Manager):


	def take(self, purchase, customer, number, **kwargs):

		if not purchase or not customer or not number:
			return None

		try:
			o = self.get(purchase = purchase, customer = customer, number = number)

		except Exception:
			o = Contract()
			o.purchase  = purchase
			o.customer  = customer
			o.number    = number
			o.currency  = kwargs.get('currency',  None)
			o.price     = kwargs.get('price',     None)
			o.price_rub = kwargs.get('price_rub', None)
			o.sign_date = kwargs.get('sign_date', None)

			o.save()

		return o


	def write(self, purchase, number = None, **kwargs):

		if not purchase:
			return None

		need_save = False

		o = self.take(purchase, customer, number, **kwargs)

		if o.currency != kwargs.get('currency', None):
			o.currency = kwargs.get('currency', None)
			need_save = True

		if o.price != kwargs.get('price', None):
			o.price = kwargs.get('price', None)
			need_save = True

		if o.price_rub != kwargs.get('price_rub', None):
			o.price_rub = kwargs.get('price_rub', None)
			need_save = True

		if o.sign_date != kwargs.get('sign_date', None):
			o.sign_date = kwargs.get('sign_date', None)
			need_save = True

		if need_save:
			o.modified = timezone.now()
			o.save()

		return o



class Contract(models.Model):

	id         = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	purchase   = models.ForeignKey(Purchase,     related_name='+', on_delete = models.CASCADE, null = True, default = None)
	customer   = models.ForeignKey(Organisation, related_name='+', on_delete = models.CASCADE, null = True, default = None)
	currency   = models.ForeignKey(Currency,     related_name='+', on_delete = models.CASCADE, null = True, default = None)

	number     = models.CharField(max_length = 50, null = True, default = None, db_index = True)
	price      = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	price_rub  = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
	sign_date  = models.DateField(null = True, default = None, db_index = True)

	state      = models.BooleanField(default = True, db_index = True)
	created    = models.DateTimeField(default = timezone.now, db_index = True)
	modified   = models.DateTimeField(default = timezone.now, db_index = True)

	suppliers  = models.ManyToManyField(Organisation, through = 'ContractToSupplier', through_fields = ('contract', 'supplier'))

	objects    = ContractManager()

	def __str__(self):
		return "{} {} {}".format(self.number, self.price, self.currency)


class ContractToSupplierManager(models.Manager):

	def take(self, contract, supplier, **kwargs):

		if not contract or not supplier:
			return None

		try:
			link = self.get(contract = contract, supplier = supplier)

		except Exception:
			link = ContractToSupplier()
			link.contract = contract
			link.supplier = supplier
			link.contact  = kwargs.get('contact', None)
			link.save()

		return link


class ContractToSupplier(models.Model):

	id       = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	contract = models.ForeignKey(Contract,     related_name='+', on_delete = models.CASCADE)
	supplier = models.ForeignKey(Organisation, related_name='+', on_delete = models.CASCADE)
	contact  = models.ForeignKey(Person,       related_name='+', on_delete = models.CASCADE, null = True, default = None)

	state       = models.BooleanField(default = True, db_index = True)
	created     = models.DateTimeField(default = timezone.now, db_index = True)
	modified    = models.DateTimeField(default = timezone.now, db_index = True)

	objects    = ContractToSupplierManager()

	def __str__(self):
		return "{} | {} | {}".format(self.contract, self.supplier, self.contact)

	class Meta:
		db_table = 'tenders_contract_to_supplier'


