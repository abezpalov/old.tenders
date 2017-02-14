from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import math


def updaters(request):
	"Представление: список загрузчиков."

	from tenders.models import Updater

	if request.user.has_perm('tenders.add_updater')\
	or request.user.has_perm('tenders.change_updater')\
	or request.user.has_perm('tenders.delete_updater'):

		updaters = Updater.objects.select_related().all().order_by('name')

	return render(request, 'tenders/updaters.html', locals())



def regions(request):
	"Представление: список регионов."

	from tenders.models import Region

	if request.user.has_perm('tenders.add_region')\
	or request.user.has_perm('tenders.change_region')\
	or request.user.has_perm('tenders.delete_region'):

		regions = Region.objects.all()

	return render(request, 'tenders/regions.html', locals())



def regionkeys(request, updater_selected = 'all', region_selected = 'all'):
	"Представление: список синонимов (внешних ключей) регионов."

	from tenders.models import RegionKey, Region, Updater

	if updater_selected != 'all':
		updater_selected = int(updater_selected)
	if region_selected != 'all':
		region_selected = int(region_selected)

	if request.user.has_perm('tenders.add_regionkey')\
	or request.user.has_perm('tenders.change_regionkey')\
	or request.user.has_perm('tenders.delete_regionkey'):

		regionkeys = RegionKey.objects.select_related().all()

		if updater_selected and updater_selected != 'all':
			regionkeys = regionkey.filter(updater = updater_selected)
		if not updater_selected:
			regionkeys = regionkeys.filter(updater = None)

		if region_selected and region_selected != 'all':
			regionkeys = regionkeys.filter(region = region_selected)
		if not vendor_selected:
			regionkeys = regionkeys.filter(region = None)

		updaters = Updater.objects.all()
		regions = Region.objects.all()

	return render(request, 'tenders/regionkeys.html', locals())



def essences(request):
	"Представление: список справочников."

	# Импортируем
	# TODO from tenders.models import Essence

	# Получаем количество объектов
	# TODO essences = Essence.objects.select_related().all()

	return render(request, 'tenders/essences.html', locals())



def ajax_get(request, *args, **kwargs):
	"AJAX-представление: Get Object."

	import json
	import tenders.models

	model = tenders.models.models[kwargs['model_name']]

	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	if not request.user.has_perm('tenders.change_{}'.format(kwargs['model_name']))\
	or not request.user.has_perm('tenders.delete_{}'.format(kwargs['model_name'])):
		return HttpResponse(status = 403)

	try:
		m = model.objects.get(id = request.POST.get('id'))

		result = {
			'status'             : 'success',
			kwargs['model_name'] : m.get_dicted()}

	except model.DoesNotExist:
		result = {
			'status'  : 'alert',
			'message' : 'Ошибка: объект отсутствует в базе.',
			'id'      : request.POST.get('id')}

	return HttpResponse(json.dumps(result), 'application/javascript')


def ajax_save(request, *args, **kwargs):
	"AJAX-представление: Save Object."

	import json
	from django.utils import timezone
	import tenders.models

	model = tenders.models.models[kwargs['model_name']]

	result = {
		'status' : 'success',
		'reload' : False}

	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status = 400)

	try:
		o = model.objects.get(id = request.POST.get('id'))
		if not request.user.has_perm('tenders.change_{}'.format(kwargs['model_name'])):
			return HttpResponse(status = 403)
	except model.DoesNotExist:
		o = model()
		result['reload'] = True
		if not request.user.has_perm('tenders.add_{}'.format(kwargs['model_name'])):
			return HttpResponse(status = 403)
		o.created = timezone.now()

	for key in request.POST:

		if key == 'name':
			if request.POST.get('name', '').strip():
				o.name = request.POST.get('name').strip()
			else:
				break

			if request.POST.get('alias', '').strip():
				o.alias = fix_alias(request.POST.get('alias'), model_name = kwargs['model_name'])
			else:
				o.alias = fix_alias(request.POST.get(key))

			if request.POST.get('name_search', '').strip():
				o.name_search = request.POST.get('name_search')[:512]
			else:
				o.name_search = request.POST.get(key)[:512]

			if request.POST.get('full_name', '').strip():
				o.full_name = request.POST.get('full_name').strip()
			else:
				o.name = request.POST.get(key)[:512]

			if request.POST.get('name_short', '').strip():
				o.name_short = request.POST.get('name_short')[:100]
			else:
				o.name_short = request.POST.get(key)[:100]

			if request.POST.get('name_short_xml', '').strip():
				o.name_short_xml = request.POST.get('name_short_xml')[:100]
			else:
				o.name_short_xml = request.POST.get(key)[:100]

		elif key == 'article':
			o.article = request.POST.get('article', '').strip()[:100]

		elif key == 'description':
			o.description = request.POST.get(key, '').strip()

		elif key == 'login':
			o.login = request.POST.get(key, '').strip()

		elif key == 'password':
			o.password = request.POST.get(key, '').strip()

		elif key == 'state':
			if 'true' == request.POST.get(key, 'true'):
				o.state = True
			else:
				o.state = False

		elif key == 'delivery_time_min':
			try:
				o.delivery_time_min = int(request.POST.get(key, 0))
			except Exception:
				o.delivery_time_min = 0

		elif key == 'delivery_time_max':
			try:
				o.delivery_time_max = int(request.POST.get(key, 0))
			except Exception:
				o.delivery_time_max = 0

		elif key == 'order':
			try:
				o.order = int(request.POST.get(key, 0))
			except Exception:
				o.order = 0

		elif key == 'rate':
			try:
				o.rate = float(request.POST.get(key).strip().replace(',', '.').replace(' ', ''))
			except Exception:
				o.rate = 1.0

		elif key == 'quantity' and kwargs['model_name'] == 'currency':
			try:
				o.quantity = float(request.POST.get(key).strip().replace(',', '.').replace(' ', ''))
			except Exception:
				o.quantity = 1.0

		elif key == 'multiplier':
			try:
				o.multiplier = float(request.POST.get(key).strip().replace(',', '.').replace(' ', ''))
			except Exception:
				o.multiplier = 1.0

		elif key == 'updater_id':
			try:
				m = catalog.models.models['updater']
				o.updater = m.objects.get(id = request.POST.get(key, ''))
			except Exception:
				o.updater = None

		elif key == 'unit_id':
			try:
				m = catalog.models.models['unit']
				o.unit = m.objects.get(id = request.POST.get(key, ''))
			except Exception:
				o.unit = None

		elif key == 'distributor_id':
			try:
				m = catalog.models.models['distributor']
				o.distributor = m.objects.get(id = request.POST.get(key, ''))
			except Exception:
				o.distributor = None

		elif key == 'vendor_id':
			try:
				m = catalog.models.models['vendor']
				o.vendor = m.objects.get(id = request.POST.get(key, ''))
			except Exception:
				o.vendor = None

		elif key == 'category_id':

			old_category = o.category

			try:
				m = catalog.models.models['category']
				o.category = m.objects.get(id = request.POST.get(key, ''))
			except Exception:
				o.category = None

			if o.category != old_category:
				result['reload'] = True

		elif key == 'parent_id' and kwargs['model_name'] == 'category':

			from django.db.models import Max

			old_parent = o.parent

			try:
				m = catalog.models.models[kwargs['model_name']]
				o.parent = m.objects.get(id = request.POST.get(key, ''))
			except Exception:
				o.parent = None
				o.level = 0

			else:

				childs = []
				childs = m.objects.getCategoryTree(childs, o)

				if o.parent in childs:
					o.parent = None
					o.level = 0
				else:
					o.level = o.parent.level + 1

			if o.parent != old_parent:
				result['reload'] = True

			o.order = m.objects.filter(parent = o.parent).aggregate(Max('order'))['order__max']

			if o.order is None:
				o.order = 0
			else:
				o.order += 1

			if o.parent:
				o.path = "{}{}/".format(o.parent.path, o.id)
			else:
				o.path = "/{}/".format(o.id)

		elif key == 'duble_id' and kwargs['model_name'] == 'product':
			try:
				m = catalog.models.models[kwargs['model_name']]
				o.duble = m.objects.get(id = request.POST.get(key, ''))
			except Exception:
				o.duble = None

		elif key == 'parametertype_id':
			result['parametertype_id'] = request.POST.get(key, '')
			try:
				m = catalog.models.models['parametertype']
				o.parametertype = m.objects.get(id = request.POST.get(key, ''))
			except Exception:
				o.parametertype = None

		elif key == 'parameter_id':
			try:
				m = catalog.models.models['parameter']
				o.parameter = m.objects.get(id = request.POST.get(key, ''))
			except Exception:
				o.parameter = None

		elif key == 'parametervalue_id':
			try:
				m = catalog.models.models['parametervalue']
				o.parametervalue = m.objects.get(id = request.POST.get(key, ''))
			except Exception:
				o.parametervalue = None

	o.modified = timezone.now()
	o.save()

	result[kwargs['model_name']] = o.get_dicted()

	return HttpResponse(json.dumps(result), 'application/javascript')


def ajax_switch_state(request, *args, **kwargs):
	"AJAX-представление: Switch State."

	import json
	from django.utils import timezone
	import catalog.models

	model = catalog.models.models[kwargs['model_name']]

	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	if not request.user.has_perm('catalog.change_{}'.format(kwargs['model_name'])):
		return HttpResponse(status=403)

	try:
		o = model.objects.get(id = request.POST.get('id'))
	except Exception:
		result = {
			'status'  : 'alert',
			'message' : 'Объект с идентификатором {} отсутствует в базе.'.format(
				request.POST.get('id'))}
		return HttpResponse(json.dumps(result), 'application/javascript')
	else:
		if 'true' == request.POST.get('state'):
			o.state = True
		else:
			o.state = False
		o.modified = timezone.now()
		o.save()

		result = {
			'status'             : 'success',
			kwargs['model_name'] : o.get_dicted()}

	return HttpResponse(json.dumps(result), 'application/javascript')


def ajax_delete(request, *args, **kwargs):
	"AJAX-представление: Delete Object."

	import json
	import catalog.models

	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status = 400)

	if not request.user.has_perm('catalog.delete_{}'.format(kwargs['model_name'])):
		return HttpResponse(status = 403)

	model = catalog.models.models[kwargs['model_name']]

	try:
		m = model.objects.get(id = request.POST.get('id'))
	except Exception:
		result = {
			'status'  : 'alert',
			'message' : 'Ошибка: объект отсутствует в базе.',
			'id'      : request.POST.get('id')}
	else:
		m.delete()
		result = {
			'status' : 'success',
			'id'     : request.POST.get('id')}

	return HttpResponse(json.dumps(result), 'application/javascript')


def ajax_link_same_foreign(request, *args, **kwargs):
	"AJAX-представление: Link Model to Same Foreign."

	import json
	from django.utils import timezone
	import catalog.models

	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	if not request.user.has_perm('catalog.change_{}'.format(kwargs['model_name']))\
	or not request.user.has_perm('catalog.add_{}'.format(kwargs['model_name'])):
		return HttpResponse(status = 403)

	model   = catalog.models.models[kwargs['model_name']]
	foreign = catalog.models.models[kwargs['foreign_name']]

	try:
		o = model.objects.get(id = request.POST.get('id'))
	except Exception:
		result = {
			'status': 'alert',
			'message': 'Ошибка: объект отсутствует в базе.'}
		return HttpResponse(json.dumps(result), 'application/javascript')

	name = o.name

	alias = fix_alias(name)

	try:
		f = foreign.objects.get(alias = alias)
	except Exception:
		f = foreign()
		f.name = name
		f.alias = alias
		f.created = timezone.now()
		f.modified = timezone.now()
		if kwargs['foreign_name'] == 'parametervalue':
			f.order = 0
			f.parameter = o.parameter

		f.save()

	if kwargs['foreign_name'] == 'vendor':
		o.vendor   = f
	elif kwargs['foreign_name'] == 'category':
		o.category = f
	elif kwargs['foreign_name'] == 'parameter':
		o.parameter = f
	elif kwargs['foreign_name'] == 'parametervalue':
		o.parametervalue = f

	o.modified = timezone.now()
	o.save()

	result = {
		'status'               : 'success',
		kwargs['model_name']   : o.get_dicted(),
		kwargs['foreign_name'] : foreign.objects.get_all_dicted()
	}

	return HttpResponse(json.dumps(result), 'application/javascript')






def fix_alias(alias, model_name = None):

	import unidecode

	if model_name == 'currency':
		alias = alias.upper()
	else:
		alias = alias.lower()

	alias = unidecode.unidecode(alias)

	alias = alias.replace(' ', '-')
	alias = alias.replace('&', 'and')
	alias = alias.replace('\'', '')
	alias = alias.replace('(', '')
	alias = alias.replace(')', '')

	alias = alias.strip()[:100]

	return alias















#########################
# TODO Need refactoring #
#########################

# OKEI
def OKEIs(request):
	"Представление: ОКЕИ."

	# Импортируем
	from tenders.models import OKEI

	# Получаем объекты
	okeis = OKEI.objects.select_related().filter(state = True)

	return render(request, 'tenders/okei.html', locals())






def ajaxGetOKEI(request):
	"AJAX-представление: Get OKEI."

	# Импортируем
	import json
	from tenders.models import OKEI

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Получаем объект
	try:
		o = OKEI.objects.select_related().get(id = request.POST.get('okei_id'))

		okei                         = {}
		okei['id']                   = o.id
		okei['code']                 = o.code
		okei['full_name']            = o.full_name
		okei['section']              = str(o.section)
		okei['group']                = str(o.group)
		okei['local_name']           = o.local_name
		okei['international_name']   = o.international_name
		okei['local_symbol']         = o.local_symbol
		okei['international_symbol'] = o.international_symbol
		okei['state']                = o.state

		result = {
			'status':  'success',
			'message': 'Данные позиции получены.',
			'okei':    okei
		}

	except OKEI.DoesNotExist:
		result = {
			'status': 'alert',
			'message': 'Ошибка: объект отсутствует в базе.'}

	return HttpResponse(json.dumps(result), 'application/javascript')


def ajaxSearchOKEIs(request):
	"AJAX-представление: Search OKEIs."

	# Импортируем
	import json
	from django.db.models import Q
	from tenders.models import OKEI

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Получаем слова поиска
	words = request.POST.get('search_text').split(' ')

	# Получаем объекты
	os = []
	for n, word in enumerate(words):
		if not n:
			new_okeis = OKEI.objects.filter(Q(full_name__icontains=word) | Q(local_name__icontains=word)).filter(state=True)
		else:
			new_okeis = new_okeis.filter(Q(full_name__icontains=word) | Q(local_name__icontains=word)).filter(state=True)
		os.extend(new_okeis)

	okeis = []

	for o in os:

		okei               = {}
		okei['id']         = o.id
		okei['full_name']  = o.full_name
		okei['local_name'] = o.local_name

		okeis.append(okei)

	result = {
		'status':  'success',
		'message': 'Данные дочерних объектов получены.',
		'okeis':   okeis}

	return HttpResponse(json.dumps(result), 'application/javascript')


# TODO KOSGU
# TODO OKOPF


# OKPD
def OKPDs(request):
	"Представление: ОКПД."

	# Импортируем
	from tenders.models import OKPD

	# TODO Исправить модель - не строки, а целые положительные числа
	# Получаем количество объектов
	okpds = OKPD.objects.select_related().filter(parent = None, state = True)

	for okpd in okpds:
		okpd.childs_count = OKPD.objects.filter(parent = okpd).count()

	return render(request, 'tenders/okpd.html', locals())


def ajaxGetOKPDChildrens(request):
	"AJAX-представление: Get OKPD Childrens."

	# Импортируем
	import json
	from tenders.models import OKPD

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Получаем объект
	try:
		okpd = OKPD.objects.get(id = request.POST.get('okpd_id'))

		os = OKPD.objects.filter(parent = okpd, state = True)

		okpds = []

		for o in os:

			okpd                 = {}
			okpd['id']           = o.id
			okpd['code']         = o.code
			okpd['name']         = o.name
			okpd['childs_count'] = OKPD.objects.filter(parent = o).count()

			okpds.append(okpd)

		result = {
			'status':  'success',
			'message': 'Данные дочерних объектов получены.',
			'okpds':   okpds}

	except OKPD.DoesNotExist:
		result = {
			'status': 'alert',
			'message': 'Ошибка: объект {} отсутствует в базе.'.format(request.POST.get('okpd_id'))}

	return HttpResponse(json.dumps(result), 'application/javascript')


def ajaxGetOKPDThread(request):
	"AJAX-представление: Get OKPD Thread."

	# Импортируем
	import json
	from tenders.models import OKPD

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Получаем объекты
	try:
		okpd = OKPD.objects.get(id = request.POST.get('okpd_id'))

		thread = [okpd]
		i = 0

		while(len(thread) > i):

			childs = OKPD.objects.filter(parent = thread[i], state = True)

			for child in childs:
				thread.append(child)

			i += 1

		okpds = []

		for o in thread:

			okpd                 = {}
			okpd['id']           = o.id
			okpd['code']         = o.code
			okpd['name']         = o.name

			okpds.append(okpd)

		result = {
			'status':  'success',
			'message': 'Данные ветви объектов получены.',
			'okpds':   okpds}

	except OKPD.DoesNotExist:
		result = {
			'status': 'alert',
			'message': 'Ошибка: объект {} отсутствует в базе.'.format(request.POST.get('okpd_id'))}

	return HttpResponse(json.dumps(result), 'application/javascript')


def ajaxSearchOKPDs(request):
	"AJAX-представление: Search OKPDs."

	# Импортируем
	import json
	from django.db.models import Q
	from tenders.models import OKPD

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Получаем слова поиска
	words = request.POST.get('search_text').split(' ')

	# Получаем объекты
	os = []
	for n, word in enumerate(words):
		if not n:
			new_okpds = OKPD.objects.filter(Q(code__icontains=word) | Q(name__icontains=word)).filter(state=True)
		else:
			new_okpds = new_okpds.filter(Q(code__icontains=word) | Q(name__icontains=word)).filter(state=True)
		os.extend(new_okpds)

	okpds = []

	for o in os:

		okpd                 = {}
		okpd['id']           = o.id
		okpd['code']         = o.code
		okpd['name']         = o.name

		okpds.append(okpd)

	result = {
		'status':  'success',
		'message': 'Данные дочерних объектов получены.',
		'okpds':   okpds}

	return HttpResponse(json.dumps(result), 'application/javascript')


# TODO OKTMO
# TODO OKVED Section
# TODO OKVED SubSection


# OKVED
def OKVEDs(request):
	"Представление: ОКВЭД."

	# Импортируем
	from tenders.models import OKVED

	# TODO Исправить модель - не строки, а целые положительные числа
	# Получаем количество объектов
	okveds = OKVED.objects.select_related().filter(parent = None, state = True)

	for okved in okveds:
		okved.childs_count = OKVED.objects.filter(parent = okved).count()

	return render(request, 'tenders/okved.html', locals())


def ajaxGetOKVEDChildrens(request):
	"AJAX-представление: Get OKVED Childrens."

	# Импортируем
	import json
	from tenders.models import OKVED

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Получаем объект
	try:
		okved = OKVED.objects.get(id = request.POST.get('okved_id'))

		os = OKVED.objects.filter(parent = okved, state = True)

		okveds = []

		for o in os:

			okved                 = {}
			okved['id']           = o.id
			okved['code']         = o.code
			okved['name']         = o.name
			okved['childs_count'] = OKVED.objects.filter(parent = o).count()

			okveds.append(okved)

		result = {
			'status':  'success',
			'message': 'Данные дочерних объектов получены.',
			'okveds':   okveds}

	except OKVED.DoesNotExist:
		result = {
			'status': 'alert',
			'message': 'Ошибка: объект {} отсутствует в базе.'.format(request.POST.get('okved_id'))}

	return HttpResponse(json.dumps(result), 'application/javascript')


def ajaxGetOKVEDThread(request):
	"AJAX-представление: Get OKVED Thread."

	# Импортируем
	import json
	from tenders.models import OKVED

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Получаем объекты
	try:
		okved = OKVED.objects.get(id = request.POST.get('okved_id'))

		thread = [okved]
		i = 0

		while(len(thread) > i):

			childs = OKVED.objects.filter(parent = thread[i], state = True)

			for child in childs:
				thread.append(child)

			i += 1

		okveds = []

		for o in thread:

			okved                 = {}
			okved['id']           = o.id
			okved['code']         = o.code
			okved['name']         = o.name

			okveds.append(okved)

		result = {
			'status':  'success',
			'message': 'Данные ветви объектов получены.',
			'okveds':   okveds}

	except OKVED.DoesNotExist:
		result = {
			'status': 'alert',
			'message': 'Ошибка: объект {} отсутствует в базе.'.format(request.POST.get('okved_id'))}

	return HttpResponse(json.dumps(result), 'application/javascript')


def ajaxSearchOKVEDs(request):
	"AJAX-представление: Search OKVEDs."

	# Импортируем
	import json
	from django.db.models import Q
	from tenders.models import OKVED

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Получаем слова поиска
	words = request.POST.get('search_text').split(' ')

	# Получаем объекты
	os = []
	for n, word in enumerate(words):
		if not n:
			new_okveds = OKVED.objects.filter(Q(code__icontains=word) | Q(name__icontains=word)).filter(state=True)
		else:
			new_okveds = new_okveds.filter(Q(code__icontains=word) | Q(name__icontains=word)).filter(state=True)
		os.extend(new_okveds)

	okveds = []

	for o in os:

		okved                 = {}
		okved['id']           = o.id
		okved['code']         = o.code
		okved['name']         = o.name

		okveds.append(okved)

	result = {
		'status':  'success',
		'message': 'Данные дочерних объектов получены.',
		'okveds':  okveds}

	return HttpResponse(json.dumps(result), 'application/javascript')


# TODO Subsystem Type
# TODO Organisation Type
# TODO Budget
# TODO Budget Type
# TODO KBK Budget
# TODO OKOGU


# TODO Organisation
def organisations(request):
	"Представление: список организаций."

	# Импортируем
	from tenders.models import Organisation

	# Проверяем права доступа
	if request.user.has_perm('tenders.add_organisation')\
	or request.user.has_perm('tenders.change_organisation')\
	or request.user.has_perm('tenders.delete_organisation'):

		# Получаем список объектов
		organisations = Organisation.objects.select_related().filter(state = True)[0:100]

	return render(request, 'tenders/organisations.html', locals())


def ajaxGetOrganisation(request):
	"AJAX-представление: Organisation."

	# Импортируем
	import json
	from tenders.models import Organisation

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Проверяем права доступа
	if not request.user.has_perm('tenders.change_organisation'):
		result = {
			'status': 'alert',
			'message': 'Ошибка 403: отказано в доступе.'}
		return HttpResponse(json.dumps(result), 'application/javascript')

	# Получаем объект
	try:
		o = Organisation.objects.select_related().get(id = request.POST.get('organisation_id'))

		organisation = {}
		organisation['id']        = o.id
		organisation['name']      = o.short_name
		organisation['full_name'] = o.full_name
		organisation['state']     = o.state

		result = {
			'status':      'success',
			'message':     'Данные позиции получены.',
			'organisation': organisation
		}

	except Organisation.DoesNotExist:
		result = {
			'status': 'alert',
			'message': 'Ошибка: организация отсутствует в базе.'}

	return HttpResponse(json.dumps(result), 'application/javascript')


# TODO Organisation Right
# TODO Plasing Way
# TODO Plan Position Change Reason
# TODO Contact Person


# PlanGraph

# TODO Написать нормальное представление и шаблоны
def planGraphs(request):
	"Представление: список планов-графиков."

	# Импортируем
	from tenders.models import PlanGraph

	# Проверяем права доступа
	if request.user.has_perm('tenders.add_plangraph')\
	or request.user.has_perm('tenders.change_plangraph')\
	or request.user.has_perm('tenders.delete_plangraph'):

		# Получаем количество объектов
		plangraphs = PlanGraph.objects.select_related().filter(state = True)[0:100]

	return render(request, 'tenders/plan-graphs.html', locals())


# PlanGraph Position
def planGraphPositions(request, page = 1, query = None):
	"Представление: список планов-графиков."

	# TODO Добавить взможность использования фильтров

	# Импортируем
	from tenders.models import PlanGraphPosition

	try:
		page = int(page)
	except TypeError:
		page = 1

	# Проверяем права доступа
	if request.user.has_perm('tenders.add_plangraph')\
	or request.user.has_perm('tenders.change_plangraph')\
	or request.user.has_perm('tenders.delete_plangraph'):

		# TODO Готовим запрос
		# Если указан запрос - загружаем его параметры
		# Если указаны параметры выборки - готовим запрос на их основании

		# Paging
		url             = '/tenders/plan-graph-positions/'
		pages           = []
		positions_count = PlanGraphPosition.objects.filter(state = True).count()
		items_on_page   = 100

		# Формируем ссылки
		page_max = positions_count // items_on_page
		if positions_count % items_on_page:
			page_max += 1

		for n in range(1, page_max + 1):
			if n < 4 or n-3 < page < n+3 or n > page_max - 3:
				pages.append(n)
			elif (n == 4 or n == page_max - 4) and pages[len(pages)-1]:
				pages.append(0)

		# Определяем номера предыдущих и последующих страниц
		page_prev = page - 1
		if page == page_max:
			page_next = 0
		else:
			page_next = page + 1

		# Получаем список объектов
		positions = PlanGraphPosition.objects.select_related().filter(state = True)[(page - 1) * items_on_page : page * items_on_page]

		# Нумеруем элементы списка
		for n, position in enumerate(positions):
			position.n = (page - 1) * items_on_page + n + 1

	return render(request, 'tenders/plan-graph-positions.html', locals())


def ajaxGetPlanGraphPosition(request):
	"AJAX-представление: Get Plan Graph Position."

	# Импортируем
	import json
	from tenders.models import PlanGraphPosition, PlanGraphPositionProduct

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Проверяем права доступа
	if not request.user.has_perm('tenders.change_plangraphposition'):
		result = {
			'status': 'alert',
			'message': 'Ошибка 403: отказано в доступе.'}
		return HttpResponse(json.dumps(result), 'application/javascript')

	# Получаем объект
	try:
		o = PlanGraphPosition.objects.select_related().get(id = request.POST.get('position_id'))

		position = {}
		position['id']      = o.id
		position['number']  = o.number
		position['name']    = o.subject_name
		position['price']   = o.price_str
		position['placing'] = o.placing_str
		position['state']   = o.state

		position['okveds'] = []
		subs = o.okveds.all()
		for sub in subs:
			okved = {
				'code': sub.code,
				'name': sub.name
			}
			position['okveds'].append(okved)

		position['okpds'] = []
		subs = o.okpds.all()
		for sub in subs:
			okpd = {
				'code': sub.code,
				'name': sub.name
			}
			position['okpds'].append(okpd)

		position['plan_graph'] = {}
		try:
			position['plan_graph']['id'] = o.plan_graph.id
		except AttributeError:
			position['plan_graph']['id'] = 0

		position['customer'] = {}
		try:
			position['customer']['id'] = o.plan_graph.customer.id
		except AttributeError:
			position['customer']['id'] = 0
		try:
			position['customer']['name'] = o.plan_graph.customer.short_name
		except AttributeError:
			position['customer']['name'] = ''

		position['placing_way'] = {}
		try:
			position['placing_way']['id'] = o.placing_way.id
		except AttributeError:
			position['placing_way']['id'] = 0

		position['change_reason'] = {}
		try:
			position['change_reason']['id'] = o.change_reason.id
		except AttributeError:
			position['change_reason']['id'] = 0


		position['products'] = []
		subs = PlanGraphPositionProduct.objects.select_related().filter(position = o)
		for sub in subs:

			product = {}

			product['number']   = sub.number + 1
			product['name']     = sub.name
			product['quantity'] = sub.quantity_str
			product['price']    = sub.price_str
			product['max_sum']  = sub.max_sum_str
			product['okpd']     = str(sub.okpd)

			position['products'].append(product)

		result = {
			'status':  'success',
			'message': 'Данные позиции получены.',
			'position': position
		}

	except PlanGraphPosition.DoesNotExist:
		result = {
			'status': 'alert',
			'message': 'Ошибка: позиция отсутствует в базе.'}

	return HttpResponse(json.dumps(result), 'application/javascript')


# TODO Plan Graph Position Product


# Query Filter
def queryFilters(request):
	"Представление: список фильтров запросов."

	# Импортируем
	from tenders.models import QueryFilter, Region, OKVED, OKPD

	# Фильтры запросов
	queryfilters = QueryFilter.objects.select_related().all()

	# Справочник регионов
	regions = Region.objects.select_related().filter(state = True)

	# Справочник ОКВЭД
	okveds = OKVED.objects.select_related().filter(parent = None, state = True)
	for okved in okveds:
		okved.childs_count = OKVED.objects.filter(parent = okved).count()

	# Справочник ОКПД
	okpds = OKPD.objects.select_related().filter(parent = None, state = True)
	for okpd in okpds:
		okpd.childs_count = OKPD.objects.filter(parent = okpd).count()


	return render(request, 'tenders/queryfilters.html', locals())


def ajaxGetQueryFilter(request):
	"AJAX-представление: Get QueryFilter."

	# Импортируем
	import json
	from tenders.models import QueryFilter

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Проверяем права доступа
	if not request.user.has_perm('tenders.change_queryfilter')\
	and not request.user.has_perm('tenders.delete_queryfilter'):
		result = {
			'status': 'alert',
			'message': 'Ошибка 403: отказано в доступе.'}
		return HttpResponse(json.dumps(result), 'application/javascript')

	# Получаем объект
	try:
		o = QueryFilter.objects.select_related().get(id = request.POST.get('queryfilter_id'))

		queryfilter = {}
		queryfilter['id']     = o.id
		queryfilter['name']   = o.name
		queryfilter['state']  = o.state
		queryfilter['public'] = o.public

		queryfilter['regions'] = []
		for r in o.regions.all():
			region         = {}
			region['id']   = r.id
			region['name'] = r.name
			queryfilter['regions'].append(region)

		queryfilter['customers'] = []
		for r in o.customers.all():
			customer         = {}
			customer['id']   = r.id
			customer['name'] = r.short_name
			queryfilter['customers'].append(customer)

		queryfilter['owners'] = []
		for r in o.owners.all():
			owner         = {}
			owner['id']   = r.id
			owner['name'] = r.short_name
			queryfilter['owners'].append(owner)

		queryfilter['okveds'] = []
		for r in o.okveds.all():
			okved         = {}
			okved['id']   = r.id
			okved['code'] = r.code
			okved['name'] = r.name
			queryfilter['okveds'].append(okved)

		queryfilter['okpds'] = []
		for r in o.okpds.all():
			okpd         = {}
			okpd['id']   = r.id
			okpd['code'] = r.code
			okpd['name'] = r.name
			queryfilter['okpds'].append(okpd)

		queryfilter['words'] = []
		for r in o.words.all():
			word         = {}
			word['id']   = r.id
			word['word'] = r.word
			queryfilter['words'].append(word)

		queryfilter['regions_in']   = o.regions_in
		queryfilter['customers_in'] = o.customers_in
		queryfilter['owners_in']    = o.owners_in
		queryfilter['okveds_in']    = o.okveds_in
		queryfilter['okpds_in']     = o.okpds_in
		queryfilter['words_in']     = o.words_in

		result = {
			'status':      'success',
			'message':     'Данные фильтра запросов получены.',
			'queryfilter': queryfilter}

	except QueryFilter.DoesNotExist:
		result = {
			'status': 'alert',
			'message': 'Ошибка: фильтр запросов {} отсутствует в базе.'.format(request.POST.get('queryfilter_id'))}

	return HttpResponse(json.dumps(result), 'application/javascript')


def ajaxSaveQueryFilter(request):
	"AJAX-представление: Save QueryFilter."

	# Импортируем
	import json
	import unidecode
	from django.utils import timezone
	from tenders.models import QueryFilter, Region, Organisation, OKVED, OKPD, Word

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status = 400)

	# Проверяем права доступа
	try:
		queryfilter = QueryFilter.objects.get(id = request.POST.get('queryfilter_id'))
		if not request.user.has_perm('tenders.change_queryfilter'):
			return HttpResponse(status = 403)
	except QueryFilter.DoesNotExist:
		queryfilter = QueryFilter()
		if not request.user.has_perm('tenders.add_queryfilter'):
			return HttpResponse(status = 403)
		queryfilter.created = timezone.now()
		queryfilter.created_by = "{} {}".format(request.user.first_name, request.user.last_name)

	# name
	if not request.POST.get('queryfilter_name').strip():
		result = {
			'status': 'alert',
			'message': 'Ошибка: отсутствует наименование.'}
		return HttpResponse(json.dumps(result), 'application/javascript')
	queryfilter.name = request.POST.get('queryfilter_name').strip()[:100]

	# regions
	regions = []
	for o in request.POST.get('queryfilter_regions_ids').split(','):
		try:
			region = Region.objects.get(id = int(o))
			regions.append(region)
		except Region.DoesNotExist: continue
		except ValueError: continue
	queryfilter.regions = regions
	del(regions)

	# customers
	customers = []
	for o in request.POST.get('queryfilter_customers_ids').split(','):
		try:
			customer = Organisation.objects.get(id = int(o))
			customers.append(customer)
		except Organisation.DoesNotExist: continue
		except ValueError: continue
	queryfilter.customers = customers
	del(customers)

	# owners
	owners = []
	for o in request.POST.get('queryfilter_owners_ids').split(','):
		try:
			owner = Organisation.objects.get(id = int(o))
			owners.append(owner)
		except Organisation.DoesNotExist: continue
		except ValueError: continue
	queryfilter.owners = owners
	del(owners)

	# okveds
	okveds = []
	for o in request.POST.get('queryfilter_okveds_ids').split(','):
		try:
			okved = OKVED.objects.get(id = int(o))
			okveds.append(okved)
		except OKVED.DoesNotExist: continue
		except ValueError: continue
	queryfilter.okveds = okveds
	del(okveds)

	# okpds
	okpds = []
	for o in request.POST.get('queryfilter_okpds_ids').split(','):
		try:
			okpd = OKPD.objects.get(id = int(o))
			okpds.append(okpd)
		except OKPD.DoesNotExist: continue
		except ValueError: continue
	queryfilter.okpds = okpds
	del(okpds)

	# words
	words = []
	for o in request.POST.get('queryfilter_words_ids').split(','):
		try:
			word = Word.objects.get(id = int(o))
			words.append(word)
		except Word.DoesNotExist: continue
		except ValueError: continue
	queryfilter.words = words
	del(words)

	# regions_in
	if request.POST.get('queryfilter_regions_in') == 'true':
		queryfilter.region_in = True
	else:
		queryfilter.region_in = False

	# customers_in
	if request.POST.get('queryfilter_customers_in') == 'true':
		queryfilter.customers_in = True
	else:
		queryfilter.customers_in = False

	# owners_in
	if request.POST.get('queryfilter_owners_in') == 'true':
		queryfilter.owners_in = True
	else:
		queryfilter.owners_in = False

	# okveds_in
	if request.POST.get('queryfilter_okveds_in') == 'true':
		queryfilter.okveds_in = True
	else:
		queryfilter.okveds_in = False

	# okpds_in
	if request.POST.get('queryfilter_okpds_in') == 'true':
		queryfilter.okpds_in = True
	else:
		queryfilter.okpds_in = False

	# words_in
	if request.POST.get('queryfilter_words_in') == 'true':
		queryfilter.words_in = True
	else:
		queryfilter.words_in = False

	# state
	if request.POST.get('queryfilter_state') == 'true':
		queryfilter.state = True
	else:
		queryfilter.state = False

	# public
	if request.POST.get('queryfilter_public') == 'true':
		queryfilter.public = True
	else:
		queryfilter.public = False

	# modified
	queryfilter.modified = timezone.now()
	queryfilter.modified_by = "{} {}".format(request.user.first_name, request.user.last_name)

	# Сохраняем
	queryfilter.save()

	# Возвращаем ответ
	result = {
		'status': 'success',
		'message': 'Фильтр запросов {} сохранён.'.format(queryfilter.name)}

	return HttpResponse(json.dumps(result), 'application/javascript')


def ajaxSwitchQueryFilterState(request):
	"AJAX-представление: Switch QueryFilter State."

	# Импортируем
	import json
	from datetime import datetime
	from tenders.models import QueryFilter

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Проверяем права доступа
	if not request.user.has_perm('tenders.change_queryfilter'):
		result = {
			'status': 'alert',
			'message': 'Ошибка 403: отказано в доступе.'}
		return HttpResponse(json.dumps(result), 'application/javascript')

	# Проверяем корректность вводных данных
	try:
		queryfilter = QueryFilter.objects.get(id = request.POST.get('queryfilter_id'))
		if request.POST.get('queryfilter_state') == 'true':
			queryfilter.state = True
		else:
			queryfilter.state = False
		queryfilter.save()
		result = {'status': 'success', 'message': 'Статус фильтра запросов {} изменен на {}.'.format(queryfilter.name, queryfilter.state)}
	except QueryFilter.DoesNotExist:
		result = {'status': 'alert', 'message': 'Статус фильтра запросов с идентификатором {} отсутствует в базе.'.format(request.POST.get('queryfilter_id'))}

	# Возвращаем ответ
	return HttpResponse(json.dumps(result), 'application/javascript')


def ajaxSwitchQueryFilterPublic(request):
	"AJAX-представление: Switch QueryFilter Public."

	# Импортируем
	import json
	from datetime import datetime
	from tenders.models import QueryFilter

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Проверяем права доступа
	if not request.user.has_perm('tenders.change_queryfilter'):
		result = {
			'status': 'alert',
			'message': 'Ошибка 403: отказано в доступе.'}
		return HttpResponse(json.dumps(result), 'application/javascript')

	# Проверяем корректность вводных данных
	try:
		queryfilter = QueryFilter.objects.get(id = request.POST.get('queryfilter_id'))
		if request.POST.get('queryfilter_public') == 'true':
			queryfilter.public = True
		else:
			queryfilter.public = False
		queryfilter.save()
		result = {'status': 'success', 'message': 'Статус "публичности" фильтра запросов {} изменен на {}.'.format(queryfilter.name, queryfilter.public)}
	except QueryFilter.DoesNotExist:
		result = {'status': 'alert', 'message': 'Статус "публичности" фильтра запросов с идентификатором {} отсутствует в базе.'.format(request.POST.get('queryfilter_id'))}

	# Возвращаем ответ
	return HttpResponse(json.dumps(result), 'application/javascript')


# Essences

