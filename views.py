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
		updaters = Updater.objects.all().order_by('name')

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
		updater = Updater.objects.get(id = request.POST.get('updater_id'))
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
			updater = Updater.objects.get(id=request.POST.get('updater_id'))
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
		regions   = Region.objects.all()
		countries = Country.objects.all()

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
		r = Region.objects.get(id = request.POST.get('region_id'))

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
	except region.DoesNotExist:
		result = {'status': 'alert', 'message': 'Загрузчик с идентификатором {} отсутствует в базе.'.format(request.POST.get('region_id'))}

	# Возвращаем ответ
	return HttpResponse(json.dumps(result), 'application/javascript')
