from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import math


# Updater

def updaters(request):
	"Представление: список загрузчиков."

	# Импортируем
	from tenders.models import Updater

	# Проверяем права доступа
	if request.user.has_perm('tenders.add_updater')\
	or request.user.has_perm('tenders.change_updater')\
	or request.user.has_perm('tenders.delete_updater'):

		# Получаем список
		updaters = Updater.objects.select_related().all().order_by('name')

	return render(request, 'tenders/updaters.html', locals())


def ajaxGetUpdater(request):
	"AJAX-представление: Get Updater."

	# Импортируем
	import json
	from tenders.models import Updater

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Проверяем права доступа
	if not request.user.has_perm('tenders.change_updater'):
		result = {
			'status': 'alert',
			'message': 'Ошибка 403: отказано в доступе.'}
		return HttpResponse(json.dumps(result), 'application/javascript')

	# Получаем объект
	try:
		updater = Updater.objects.get(id = request.POST.get('updater_id'))

		result = {
			'status':           'success',
			'message':          'Данные загрузчика получены.',
			'updater_id':       updater.id,
			'updater_name':     updater.name,
			'updater_alias':    updater.alias,
			'updater_login':    updater.login,
			'updater_password': updater.password,
			'updater_state':    updater.state}

	except Updater.DoesNotExist:
		result = {
			'status': 'alert',
			'message': 'Ошибка: загрузчик отсутствует в базе.'}

	return HttpResponse(json.dumps(result), 'application/javascript')


def ajaxSaveUpdater(request):
	"AJAX-представление: Save Updater."

	# Импортируем
	import json
	import unidecode
	from django.utils import timezone
	from tenders.models import Updater

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status = 400)

	# Проверяем права доступа
	try:
		updater = Updater.objects.select_related().get(id = request.POST.get('updater_id'))
		if not request.user.has_perm('tenders.change_updater'):
			return HttpResponse(status = 403)
	except Updater.DoesNotExist:
		updater = Updater()
		if not request.user.has_perm('tenders.add_updater'):
			return HttpResponse(status = 403)
		updater.created = timezone.now()

	# name
	if not request.POST.get('updater_name').strip():
		result = {
			'status': 'alert',
			'message': 'Ошибка: отсутствует наименование загрузчика.'}
		return HttpResponse(json.dumps(result), 'application/javascript')
	updater.name   = request.POST.get('updater_name').strip()[:100]

	# alias
	if request.POST.get('updater_alias').strip():
		updater.alias = unidecode.unidecode(request.POST.get('updater_alias')).strip()[:100]
	else:
		updater.alias = unidecode.unidecode(request.POST.get('updater_name')).strip()[:100]

	# login
	if request.POST.get('updater_login').strip():
		updater.login = request.POST.get('updater_login').strip()
	else:
		updater.login = ''

	# password
	if request.POST.get('updater_password').strip():
		updater.password = request.POST.get('updater_password').strip()
	else:
		updater.password = ''

	# state
	if request.POST.get('updater_state') == 'true':
		updater.state = True
	else:
		updater.state = False

	# modified
	updater.modified = timezone.now()

	# Сохраняем
	updater.save()

	# Возвращаем ответ
	result = {
		'status': 'success',
		'message': 'Загрузчик {} сохранён.'.format(updater.name)}

	return HttpResponse(json.dumps(result), 'application/javascript')


def ajaxSwitchUpdaterState(request):
	"AJAX-представление: Switch Updater State."

	# Импортируем
	import json
	from datetime import datetime
	from tenders.models import Updater

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Проверяем права доступа
	if not request.user.has_perm('tenders.change_updater'):
		result = {
			'status': 'alert',
			'message': 'Ошибка 403: отказано в доступе.'}
		return HttpResponse(json.dumps(result), 'application/javascript')

	# Проверяем корректность вводных данных
	if not request.POST.get('updater_id') or not request.POST.get('updater_state'):
		result = {'status': 'warning', 'message': 'Пожалуй, вводные данные не корректны.'}
	else:
		try:
			updater = Updater.objects.select_related().get(id=request.POST.get('updater_id'))
			if request.POST.get('updater_state') == 'true':
				updater.state = True
			else:
				updater.state = False
			updater.save()
			result = {'status': 'success', 'message': 'Статус загрузчика {} изменен на {}.'.format(updater.name, updater.state)}
		except Updater.DoesNotExist:
			result = {'status': 'alert', 'message': 'Загрузчик с идентификатором {} отсутствует в базе.'.format(request.POST.get('updater_id'))}

	# Возвращаем ответ
	return HttpResponse(json.dumps(result), 'application/javascript')


# TODO Source


# TODO Country


# Region


def regions(request):
	"Представление: список загрузчиков."

	# Импортируем
	from tenders.models import Region, Country

	# Проверяем права доступа
	if request.user.has_perm('tenders.add_region')\
	or request.user.has_perm('tenders.change_region')\
	or request.user.has_perm('tenders.delete_region'):

		# Получаем списки объектов
		regions   = Region.objects.select_related().all()
		countries = Country.objects.select_related().all()

	return render(request, 'tenders/regions.html', locals())


def ajaxGetRegion(request):
	"AJAX-представление: Get Region."

	# Импортируем
	import json
	from tenders.models import Region

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Проверяем права доступа
	if not request.user.has_perm('tenders.change_region')\
	and not request.user.has_perm('tenders.delete_region'):
		result = {
			'status': 'alert',
			'message': 'Ошибка 403: отказано в доступе.'}
		return HttpResponse(json.dumps(result), 'application/javascript')

	# Получаем объект
	try:
		r = Region.objects.select_related().get(id = request.POST.get('region_id'))

		region = {}
		region['id']        = r.id
		region['name']      = r.name
		region['full_name'] = r.full_name
		region['alias']     = r.alias
		region['state']     = r.state

		if r.country:
			region['country'] = {}
			region['country']['id']    = r.country.id
			region['country']['name']  = r.counry.name
			region['country']['alias'] = r.counry.alias
			region['country']['state'] = r.counry.state
		else:
			region['country'] = {}
			region['country']['id'] = 0
			region['country']['name']  = ''
			region['country']['alias'] = ''
			region['country']['state'] = ''

		result = {
			'status':  'success',
			'message': 'Данные региона получены.',
			'region':  region}

	except Region.DoesNotExist:
		result = {
			'status': 'alert',
			'message': 'Ошибка: регион отсутствует в базе.'}

	return HttpResponse(json.dumps(result), 'application/javascript')


def ajaxSaveRegion(request):
	"AJAX-представление: Save Region."

	# Импортируем
	import json
	import unidecode
	from django.utils import timezone
	from tenders.models import Region, Country

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status = 400)

	# Проверяем права доступа
	try:
		region = Region.objects.get(id = request.POST.get('region_id'))
		if not request.user.has_perm('tenders.change_region'):
			return HttpResponse(status = 403)
	except Region.DoesNotExist:
		region = Region()
		if not request.user.has_perm('tenders.add_region'):
			return HttpResponse(status = 403)
		region.created = timezone.now()

	# name
	if not request.POST.get('region_name').strip():
		result = {
			'status': 'alert',
			'message': 'Ошибка: отсутствует наименование.'}
		return HttpResponse(json.dumps(result), 'application/javascript')
	region.name   = request.POST.get('region_name').strip()[:100]

	# full_name
	if request.POST.get('region_full_name').strip():
		region.full_name = request.POST.get('region_full_name').strip()[:100]
	else:
		region.full_name = request.POST.get('region_name').strip()[:100]

	# alias
	if request.POST.get('region_alias').strip():
		region.alias = unidecode.unidecode(request.POST.get('region_alias')).strip()[:100]
	else:
		region.alias = unidecode.unidecode(request.POST.get('region_name')).strip()[:100]

	# country
	try:
		region.country = Country.objects.get(id = request.POST.get('region_country_id'))
	except Country.DoesNotExist:
		region.country = None

	# state
	if request.POST.get('region_state') == 'true':
		region.state = True
	else:
		region.state = False

	# modified
	region.modified = timezone.now()

	# Сохраняем
	region.save()

	# Возвращаем ответ
	result = {
		'status': 'success',
		'message': 'Регион {} сохранён.'.format(region.name)}

	return HttpResponse(json.dumps(result), 'application/javascript')


def ajaxSwitchRegionState(request):
	"AJAX-представление: Switch Region State."

	# Импортируем
	import json
	from datetime import datetime
	from tenders.models import Region

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Проверяем права доступа
	if not request.user.has_perm('tenders.change_region'):
		result = {
			'status': 'alert',
			'message': 'Ошибка 403: отказано в доступе.'}
		return HttpResponse(json.dumps(result), 'application/javascript')

	# Проверяем корректность вводных данных
	try:
		region = Region.objects.get(id = request.POST.get('region_id'))
		if request.POST.get('region_state') == 'true':
			region.state = True
		else:
			region.state = False
		region.save()
		result = {'status': 'success', 'message': 'Статус региона {} изменен на {}.'.format(region.name, region.state)}
	except Region.DoesNotExist:
		result = {'status': 'alert', 'message': 'Загрузчик с идентификатором {} отсутствует в базе.'.format(request.POST.get('region_id'))}

	# Возвращаем ответ
	return HttpResponse(json.dumps(result), 'application/javascript')



# TODO Currency
# TODO OKEI Section
# TODO OKEI Group


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
def essences(request):
	"Представление: список справочников."

	# Импортируем
	# TODO from tenders.models import Essence

	# Получаем количество объектов
	# TODO essences = Essence.objects.select_related().all()

	return render(request, 'tenders/essences.html', locals())
