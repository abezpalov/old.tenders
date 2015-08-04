import gc
import datetime
from tenders.models import *
from django.utils import timezone


class Runner:


	name = 'Обновление с сайта государственных закупок России'
	alias = 'zakupki-gov-ru'
	urls = {
		'base':                        'ftp.zakupki.gov.ru',
		'essences':                    'fcs_nsi',
		'regions':                     'fcs_regions',
		'country':                     'nsiOKSM',
		'currency':                    'nsiCurrency',
		'okei':                        'nsiOKEI',
		'kosgu':                       'nsiKOSGU',
		'okopf':                       'nsiOKOPF',
		'okpd':                        'nsiOKPD',
		'oktmo':                       'nsiOKTMO',
		'okved':                       'nsiOKVED',
		'budget':                      'nsiBudget',
		'budget_type':                 'nsiOffBudgetType',
		'kbk_budget':                  'nsiKBKBudget',
		'organisation_type':           'nsiOrganizationType',
		'organisation':                'nsiOrganization',
		'placing_way':                 'nsiPlacingWay',
		'plan_position_change_reason': 'nsiPlanPositionChangeReason',
		'purchase_document_type':      'nsiPurchaseDocumentTypes',
		'purchase_preference':         'nsiPurchasePreferences',
		'purchase_reject_reason':      'nsiPurchaseRejectReason',
		'plangraph':                   'plangraphs',
		'prev_month':                  'prevMonth',
		'curr_month':                  'currMonth'}

	essences = [
		'country',
		'currency',
		'okei',
		'kosgu',
		'okopf',
		'okpd',
		'oktmo',
		'okved',
		'budget',
		'budget_type',
		'kbk_budget',
		'organisation_type',
		'organisation',
		'placing_way',
		'plan_position_change_reason']

	max_time = datetime.timedelta(0, 82800, 0)

	def __init__(self):

		# Загрузчик
		self.updater = Updater.objects.take(
			alias = self.alias,
			name  = self.name)

		self.parsers = {

			'country':                     self.parseCountry,
			'currency':                    self.parseCurrency,
			'okei':                        self.parseOKEI,
			'kosgu':                       self.parseKOSGU,
			'okopf':                       self.parseOKOPF,
			'okpd':                        self.parseOKPD,
			'oktmo':                       self.parseOKTMO,
			'okved':                       self.parseOKVED,
			'budget':                      self.parseBudget,
			'budget_type':                 self.parseBudgetType,
			'kbk_budget':                  self.parseKBKBudget,
			'organisation_type':           self.parseOrganisationType,
			'organisation':                self.parseOrganisation,
			'placing_way':                 self.parsePlacingWay,
			'plan_position_change_reason': self.parsePlanPositionChangeReason,

			'plangraph':                   self.parsePlanGraph
		}


	def run(self):

		self.start = timezone.now()

		# Проверяем наличие параметров авторизации
		if not self.updater.login or not self.updater.password:
			print('Ошибка: Проверьте параметры авторизации. Кажется их нет.')
			return False

		# Обновляем справочники
		for essence in self.essences:

			# Проверяем не вышло ли время
			if timezone.now() - self.start > self.max_time:
				print("Время вышло {}.".format(timezone.now() - self.start))
				return True

			self.updateEssence(essence)

		# Обновляем информацию по регионам
		self.updateRegions()

		# Получаем спиисок "нужных" регионов
		regions = Region.objects.filter(state = True)

		for region in regions:

			catalogs = [
				"{}/{}/{}/{}".format(
					self.urls['regions'],
					region.alias,
					self.urls['plangraph'],
					self.urls['prev_month']),
				"{}/{}/{}/{}".format(
					self.urls['regions'],
					region.alias,
					self.urls['plangraph'],
					self.urls['curr_month'])]

			for catalog in catalogs:

				# Обрабатываем планы-графики
				self.updateEssence(
					essence = 'plangraph',
					catalog = catalog,
					region = region)

				# TODO Обновляем тендеры регионов

		print("Обработки завершены за {}.".format(timezone.now() - self.start))
		return True


	def getFTPCatalog(self, catalog = None):
		'Возвращает содержимое папки'

		# Импортируем
		from ftplib import FTP

		# Авторизуемся
		ftp = FTP(host = self.urls['base'])
		ftp.login(user = self.updater.login, passwd = self.updater.password)

		# Переходим в нужный каталог
		if catalog:
			ftp.cwd(catalog)

		# Получаем содержимое каталога
		result = ftp.nlst()

		# Закрываем соединение
		ftp.close()

		# Возвращаем результат
		return result


	def getZipFromFTP(self, file_name, catalog = None):
		'Скачивает и возвращает файл с FTP-сервера'

		# Импортируем
		from ftplib import FTP
		from io import BytesIO
		from zipfile import ZipFile

		# Инициализируем переменные
		ftp = FTP(host = self.urls['base'])
		zip_file = BytesIO(b"")

		# Авторизуемся
		ftp.login(user = self.updater.login, passwd = self.updater.password)

		# Переходим в нужный каталог
		if catalog:
			ftp.cwd(catalog)

		# Скачиваем файл
		try:
			ftp.retrbinary("RETR {}".format(file_name), zip_file.write)
			zip_data  = ZipFile(zip_file)
		except:
			return False

		# Возвращаем результат
		return zip_data


	def updateEssence(self, essence, catalog = None, region = None):
		'Получает файлы сущностей для анализа и обработки'

		# Импортируем
		from io import TextIOWrapper

		# Получаем список файлов
		if catalog is None:
			catalog = "{}/{}".format(self.urls['essences'], self.urls[essence])

		zip_names = self.getFTPCatalog(catalog)

		# Записываем источники в базу
		for zip_name in zip_names:

			source = Source.objects.take(
				url = "{}/{}/{}".format(
					self.urls['base'],
					catalog,
					zip_name))

		# Загружаем архивы
		for zip_name in zip_names:

			# Проверяем не вышло ли время
			if timezone.now() - self.start > self.max_time:
				print("Время вышло {}.".format(timezone.now() - self.start))
				return True
			else:
				print("Времени прошло {}.".format(timezone.now() - self.start))

			# Проверяем источник
			source = Source.objects.take(
				url = "{}/{}/{}".format(
					self.urls['base'],
					catalog,
					zip_name))

			if source.state:
				print("Файл уже обработан: {}.".format(zip_name))
				continue

			# Скачиваем архив
			print("Скачиваю файл: {}".format(zip_name))
			zip_data = self.getZipFromFTP(zip_name, catalog)

			if not zip_data:
				print("Ошибка: невозможно скачать файл. Перехожу с следующему.")
				continue

			# Получаем список файлов в архиве
			xml_names = zip_data.namelist()
			for xml_name in xml_names:

				# Извлекаем файл из архива
				xml_data = zip_data.open(xml_name)

				# Парсим файл
				parse = self.parsers[essence]
				parse(xml_data, region)

			print("Все файлы архива обработаны.")
			source.complite()

		return True


	def parseCountry(self, xml_data, region = None):
		'Парсит страны'

		# Импортируем
		from lxml import etree

		# Парсим
		tree = etree.parse(xml_data)

		# Чистим теги
		for element in tree.xpath('.//*'):
			element.tag = element.tag.split('}')[1]

		elements = tree.xpath('.//nsiOKSM')

		for element in elements:

			o              = {}
			o['code']      = element.xpath('./countryCode')[0].text
			o['full_name'] = element.xpath('./countryFullName')[0].text

			if element.xpath('./actual')[0].text == 'true':
				o['state'] = True
			else:
				o['state'] = False

			country = Country.objects.update(
				code         = o['code'],
				full_name    = o['full_name'],
				state        = o['state'])

			print("Страна: {}.".format(country))

		return True


	def parseCurrency(self, xml_data, region = None):
		'Парсит валюты'

		# Импортируем
		from lxml import etree

		# Парсим
		tree = etree.parse(xml_data)

		# Чистим теги
		for element in tree.xpath('.//*'):
			element.tag = element.tag.split('}')[1]

		elements = tree.xpath('.//nsiCurrency')

		for element in elements:

			o                 = {}
			o['code']         = element.xpath('./code')[0].text
			o['digital_code'] = element.xpath('./digitalCode')[0].text
			o['name']         = element.xpath('./name')[0].text

			if element.xpath('./actual')[0].text == 'true':
				o['state'] = True
			else:
				o['state'] = False

			# Обновляем информацию в базе
			currency = Currency.objects.update(
				code         = o['code'],
				digital_code = o['digital_code'],
				name         = o['name'],
				state        = o['state'])

			print("Валюта: {}.".format(currency))

		return True


	def parseOKEI(self, xml_data, region = None):
		'Парсит единицы измерения'

		# Импортируем
		from lxml import etree

		# Парсим
		tree = etree.parse(xml_data)

		# Чистим теги
		for element in tree.xpath('.//*'):
			element.tag = element.tag.split('}')[1]

		elements = tree.xpath('.//nsiOKEI')

		for element in elements:

			o                         = {}
			o['code']                 = element.xpath('./code')[0].text
			o['full_name']            = element.xpath('./fullName')[0].text
			o['section_code']         = element.xpath('./section/code')[0].text
			o['section_name']         = element.xpath('./section/name')[0].text
			o['group_code']           = element.xpath('./group/id')[0].text
			o['group_name']           = element.xpath('./group/name')[0].text
			o['local_name']           = element.xpath('./localName')[0].text
			o['international_name']   = element.xpath('./internationalName')[0].text
			o['local_symbol']         = element.xpath('./localSymbol')[0].text
			o['international_symbol'] = element.xpath('./internationalSymbol')[0].text

			if element.xpath('./actual')[0].text == 'true':
				o['state'] = True
			else:
				o['state'] = False

			# Обновляем информацию в базе
			okei_section = OKEISection.objects.update(
				code  = o['section_code'],
				name  = o['section_name'],
				state = True)
			okei_group = OKEIGroup.objects.update(
				code  = o['group_code'],
				name  = o['group_name'],
				state = True)
			okei = OKEI.objects.update(
				code                 = o['code'],
				full_name            = o['full_name'],
				section              = okei_section,
				group                = okei_group,
				local_name           = o['local_name'],
				international_name   = o['international_name'],
				local_symbol         = o['local_symbol'],
				international_symbol = o['international_symbol'],
				state                = o['state'])

			print("Единица измерения: {}.".format(okei))

		return True


	def parseKOSGU(self, xml_data, region = None):
		'Парсит классификатор операций сектора государственного управления.'

		# Импортируем
		from lxml import etree

		# Парсим
		tree = etree.parse(xml_data)

		# Чистим теги
		for element in tree.xpath('.//*'):
			element.tag = element.tag.split('}')[1]

		elements = tree.xpath('.//nsiKOSGU')

		for element in elements:

			o = {}
			o['code']        = element.xpath('./code')[0].text
			o['name']        = element.xpath('./name')[0].text

			try:
				o['parent_code'] = element.xpath('./parentCode')[0].text
			except IndexError:
				o['parent_code'] = None

			if o['parent_code'] == '000':
				o['parent_code'] = None

			if element.xpath('./actual')[0].text == 'true':
				o['state'] = True
			else:
				o['state'] = False

			kosgu = KOSGU.objects.update(
				code        = o['code'],
				parent_code = o['parent_code'],
				name        = o['name'],
				state       = o['state'])

			print("КОСГУ: {}.".format(kosgu))

		return True


	def parseOKOPF(self, xml_data, region = None):
		'Парсит ОКОПФ.'

		# Импортируем
		from lxml import etree

		# Парсим
		tree = etree.parse(xml_data)

		# Чистим теги
		for element in tree.xpath('.//*'):
			element.tag = element.tag.split('}')[1]

		elements = tree.xpath('.//nsiOKOPF')

		for element in elements:

			o                  = {}
			o['code']          = element.xpath('./code')[0].text
			o['full_name']     = element.xpath('./fullName')[0].text
			o['singular_name'] = element.xpath('./singularName')[0].text

			try:
				o['parent_code'] = element.xpath('./parentCode')[0].text
			except IndexError:
				o['parent_code'] = None

			if element.xpath('./actual')[0].text == 'true':
				o['state'] = True
			else:
				o['state'] = False

			okopf = OKOPF.objects.update(
				code          = o['code'],
				parent_code   = o['parent_code'],
				full_name     = o['full_name'],
				singular_name = o['singular_name'],
				state         = o['state'])

			print("ОКОПФ: {}.".format(okopf))

		return True


	def parseOKPD(self, xml_data, region = None):
		'Парсит ОКПД.'

		# Импортируем
		from lxml import etree

		# Парсим
		tree = etree.parse(xml_data)

		# Получаем корневой элемент
		root = tree.getroot()

		# Получаем список
		for element_list in root:

			# Получаем элемент
			for element in element_list:

				# Инициируем пустой справочник элемента
				e = {}

				# Обрабатываем значения полей
				for value in element:

					# code
					if value.tag.endswith('id'):
						e['oos_id'] = value.text

					# parent_code
					elif value.tag.endswith('parentId'):
						if not value.text:
							e['parent_oos_id'] = None
						else:
							e['parent_oos_id'] = value.text

					# alias
					elif value.tag.endswith('code'):
						e['code'] = value.text	

					# name
					elif value.tag.endswith('name'):
						e['name'] = value.text

					# state
					elif value.tag.endswith('actual'):
						if value.text == 'true':
							e['state'] = True
						else:
							e['state'] = False

				# Обновляем информацию в базе
				try:
					e['parent_oos_id'] = e['parent_oos_id']
				except KeyError:
					e['parent_oos_id'] = None

				okpd = OKPD.objects.update(
					oos_id        = e['oos_id'],
					parent_oos_id = e['parent_oos_id'],
					code          = e['code'],
					name          = e['name'],
					state         = e['state'])

				print("Обновлён элемент ОКПД: {}.".format(okpd))

		return True


	def parseOKTMO(self, xml_data, region = None):
		'Парсит ОКТМО.'

		# Импортируем
		from lxml import etree

		# Парсим
		tree = etree.parse(xml_data)

		# Получаем корневой элемент
		root = tree.getroot()

		# Получаем список
		for element_list in root:

			# Получаем элемент
			for element in element_list:

				# Инициируем пустой справочник элемента
				e = {}

				# Обрабатываем значения полей
				for value in element:

					# code
					if value.tag.endswith('code'):
						e['code'] = value.text

					# parent_code
					elif value.tag.endswith('parentCode'):
						if not value.text:
							e['parent_code'] = None
						else:
							e['parent_code'] = value.text

					# full_name
					elif value.tag.endswith('fullName'):
						e['full_name'] = value.text

					# state
					elif value.tag.endswith('actual'):
						if value.text == 'true':
							e['state'] = True
						else:
							e['state'] = False

				# Обновляем информацию в базе
				try:
					e['parent_code'] = e['parent_code']
				except KeyError:
					e['parent_code'] = None

				oktmo = OKTMO.objects.update(
					code        = e['code'],
					parent_code = e['parent_code'],
					full_name   = e['full_name'],
					state       = e['state'])

				print("Обновлён элемент ОКТМО: {}.".format(oktmo))

		return True


	def parseOKVED(self, xml_data, region = None):
		'Парсит ОКВЭД.'

		# Импортируем
		from lxml import etree

		# Парсим
		tree = etree.parse(xml_data)

		# Получаем корневой элемент
		root = tree.getroot()

		# Получаем список
		for element_list in root:

			# Получаем элемент
			for element in element_list:

				# Инициируем пустой справочник элемента
				e = {}

				# Обрабатываем значения полей
				for value in element:

					# oos_id
					if value.tag.endswith('id'):
						e['oos_id'] = value.text

					# parent_oos_id
					elif value.tag.endswith('parentId'):
						if not value.text:
							e['parent_oos_id'] = None
						else:
							e['parent_oos_id'] = value.text

					# code
					elif value.tag.endswith('code'):
						e['code'] = value.text

					# section
					elif value.tag.endswith('section'):
						e['section'] = value.text

					# subsection
					elif value.tag.endswith('subsection'):
						e['subsection'] = value.text

					# name
					elif value.tag.endswith('name'):
						e['name'] = value.text

					# state
					elif value.tag.endswith('actual'):
						if value.text == 'true':
							e['state'] = True
						else:
							e['state'] = False

				# Корректируем
				try:
					e['parent_oos_id'] = e['parent_oos_id']
				except KeyError:
					e['parent_oos_id'] = None

				try:
					e['section'] = e['section']
				except KeyError:
					e['section'] = None

				try:
					e['subsection'] = e['subsection']
				except KeyError:
					e['subsection'] = None

				# Обновляем информацию в базе
				okved = OKVED.objects.update(
					oos_id        = e['oos_id'],
					parent_oos_id = e['parent_oos_id'],
					code          = e['code'],
					section       = e['section'],
					subsection    = e['subsection'],
					name          = e['name'],
					state         = e['state'])

				print("Обновлён элемент ОКВЭД: {}.".format(okved))

		return True


	def parseBudget(self, xml_data, region = None):
		'Парсит бюджет.'

		# Импортируем
		from lxml import etree

		# Парсим
		tree = etree.parse(xml_data)

		# Получаем корневой элемент
		root = tree.getroot()

		# Получаем список
		for element_list in root:

			# Получаем элемент
			for element in element_list:

				# Инициируем пустой справочник элемента
				e = {}

				# Обрабатываем значения полей
				for value in element:

					# code
					if value.tag.endswith('code'):
						e['code'] = value.text

					# name
					elif value.tag.endswith('name'):
						e['name'] = value.text

					# state
					elif value.tag.endswith('actual'):
						if value.text == 'true':
							e['state'] = True
						else:
							e['state'] = False


				# Обновляем информацию в базе
				budget = Budget.objects.update(
					code  = e['code'],
					name  = e['name'],
					state = e['state'])

				print("Обновлён элемент Бюджет: {}.".format(budget))

		return True


	def parseBudgetType(self, xml_data, region = None):
		'Парсит типы бюджета.'

		# Импортируем
		from lxml import etree

		# Парсим
		tree = etree.parse(xml_data)

		# Получаем корневой элемент
		root = tree.getroot()

		# Получаем список
		for element_list in root:

			# Получаем элемент
			for element in element_list:

				# Инициируем пустой справочник элемента
				e = {}

				# Обрабатываем значения полей
				for value in element:

					# code
					if value.tag.endswith('code'):
						e['code'] = value.text

					# name
					elif value.tag.endswith('name'):
						e['name'] = value.text

					# subsystem_type
					elif value.tag.endswith('subsystemType'):
						e['subsystem_type'] = value.text

					# state
					elif value.tag.endswith('actual'):
						if value.text == 'true':
							e['state'] = True
						else:
							e['state'] = False

				# Обрабатываем зависимости
				try:
					if e['subsystem_type']:
						e['subsystem_type'] = SubsystemType.objects.take(e['subsystem_type'])
				except KeyError:
					e['subsystem_type'] = None
				except SubsystemType.DoesNotExist:
					e['subsystem_type'] = None

				# Обновляем информацию в базе
				budget_type = BudgetType.objects.update(
					code           = e['code'],
					name           = e['name'],
					subsystem_type = e['subsystem_type'],
					state          = e['state'])

				print("Обновлён элемент Тип бюджета: {}.".format(budget_type))

		return True


	def parseKBKBudget(self, xml_data, region = None):
		'Парсит код поступления бюджета.'

		# Импортируем
		from lxml import etree

		# Парсим
		tree = etree.parse(xml_data)

		# Получаем корневой элемент
		root = tree.getroot()

		# Получаем список
		for element_list in root:

			# Получаем элемент
			for element in element_list:

				# Инициируем пустой справочник элемента
				e = {}

				# Обрабатываем значения полей
				for value in element:

					# code
					if value.tag.endswith('kbk'):
						e['code'] = value.text

					# budget
					elif value.tag.endswith('budget'):
						e['budget'] = value.text

					# state
					elif value.tag.endswith('actual'):
						if value.text == 'true':
							e['state'] = True
						else:
							e['state'] = False

				# Обрабатываем зависимости
				try:
					e['budget'] = Budget.objects.take(code = e['budget'])
				except KeyError:
					e['budget'] = None
				except SubsystemType.DoesNotExist:
					e['budget'] = None

				# Обновляем информацию в базе
				kbk_budget = KBKBudget.objects.update(
					code   = e['code'],
					budget = e['budget'],
					state  = e['state'])

				print("Обновлён элемент Код поступления бюджета: {}.".format(kbk_budget))

		return True


	def parseOrganisationType(self, xml_data, region = None):
		'Парсит типы организаций.'

		# Импортируем
		from lxml import etree

		# Парсим
		tree = etree.parse(xml_data)

		# Получаем корневой элемент
		root = tree.getroot()

		# Получаем список
		for element_list in root:

			# Получаем элемент
			for element in element_list:

				# Инициируем пустой справочник элемента
				e = {}

				# Обрабатываем значения полей
				for value in element:

					# code
					if value.tag.endswith('code'):
						e['code'] = value.text

					# name
					elif value.tag.endswith('name'):
						e['name'] = value.text

					# description
					elif value.tag.endswith('description'):
						e['description'] = value.text


				# Обновляем информацию в базе
				organisation_type = OrganisationType.objects.update(
					code        = e['code'],
					name        = e['name'],
					description = e['description'])

				print("Обновлён элемент Тип организации: {}.".format(organisation_type))

		return True


	def parseOrganisation(self, xml_data, region = None):
		'Парсит организации.'

		# Импортируем
		from lxml import etree

		# Парсим
		tree = etree.parse(xml_data)

		# Получаем корневой элемент
		root = tree.getroot()

		# Получаем список
		for element_list in root:

			# Получаем элемент
			for element in element_list:

				# Инициируем пустой справочник элемента
				e = {}

				# Обрабатываем значения полей
				for value in element:

					if value.tag.endswith('regNumber'):
						e['reg_number'] = value.text

					elif value.tag.endswith('shortName'):
						e['short_name'] = value.text

					elif value.tag.endswith('fullName'):
						e['full_name'] = value.text

					elif value.tag.endswith('headAgency'):
						for sub in element:
							if value.tag.endswith('regNum'):
								e['head_agency'] = sub.text

					elif value.tag.endswith('orderingAgency'):
						for sub in element:
							if value.tag.endswith('regNum'):
								e['ordering_agency'] = sub.text

					elif value.tag.endswith('OKOGU'):
						e['okogu'] = value.text

					elif value.tag.endswith('INN'):
						e['inn'] = value.text

					elif value.tag.endswith('KPP'):
						e['kpp'] = value.text

					elif value.tag.endswith('OKPO'):
						e['okpo'] = value.text

					elif value.tag.endswith('organizationType'):
						for sub in element:
							if value.tag.endswith('code'):
								e['organisation_type'] = sub.text

					elif value.tag.endswith('OKTMO'):
						for sub in element:
							if value.tag.endswith('code'):
								e['oktmo'] = sub.text

					elif value.tag.endswith('actual'):
						if value.text == 'true':
							e['state'] = True
						else:
							e['state'] = False

					elif value.tag.endswith('register'):
						if value.text == 'true':
							e['register'] = True
						else:
							e['register'] = False

				# Обрабатываем зависимости
				try:
					if e['head_agency']:
						e['head_agency'] = Organisation.objects.take(e['head_agency'])
				except KeyError:
					e['head_agency'] = None
				except Organisation.DoesNotExist:
					e['head_agency'] = None


				try:
					if e['ordering_agency']:
						e['ordering_agency'] = Organisation.objects.take(e['ordering_agency'])
				except KeyError:
					e['ordering_agency'] = None
				except Organisation.DoesNotExist:
					e['ordering_agency'] = None

				try:
					if e['organisation_type']:
						e['organisation_type'] = OrganisationType.objects.take(e['organisation_type'])
				except KeyError:
					e['organisation_type'] = None
				except Organisation.DoesNotExist:
					e['organisation_type'] = None

				try:
					if e['oktmo']:
						e['oktmo'] = OKTMO.objects.take(e['oktmo'])
				except KeyError:
					e['oktmo'] = None
				except Organisation.DoesNotExist:
					e['oktmo'] = None

				try:
					if e['okogu']:
						e['okogu'] = OKOGU.objects.take(e['okogu'])
				except KeyError:
					e['okogu'] = None
				except Organisation.DoesNotExist:
					e['okogu'] = None

				# Обновляем информацию в базе
				organisation = Organisation.objects.update(
					reg_number        = e['reg_number'],
					short_name        = e['short_name'],
					full_name         = e['full_name'],
					head_agency       = e['head_agency'],
					ordering_agency   = e['ordering_agency'],
					okogu             = e['okogu'],
					inn               = e['inn'],
					kpp               = e['kpp'],
					okpo              = e['okpo'],
					organisation_type = e['organisation_type'],
					oktmo             = e['oktmo'],
					state             = e['state'],
					register          = e['register'])

				print("Обновлён элемент Организация: {}.".format(organisation))

		return True


	def parsePlacingWay(self, xml_data, region = None):
		'Парсит пути размещения.'

		# Импортируем
		from lxml import etree

		# Парсим
		tree = etree.parse(xml_data)

		# Получаем корневой элемент
		root = tree.getroot()

		# Получаем список
		for element_list in root:

			# Получаем элемент
			for element in element_list:

				# Инициируем пустой справочник элемента
				e = {}

				# Обрабатываем значения полей
				for value in element:

					# placing_way_id
					if value.tag.endswith('placingWayId'):
						e['placing_way_id'] = value.text

					# code
					elif value.tag.endswith('code'):
						e['code'] = value.text

					# name
					elif value.tag.endswith('name'):
						e['name'] = value.text

					# type
					elif value.tag.endswith('type'):
						e['placing_way_type'] = value.text

					# subsystem_type
					elif value.tag.endswith('subsystemType'):
						e['subsystem_type'] = value.text

					# state
					elif value.tag.endswith('actual'):
						if value.text == 'true':
							e['state'] = True
						else:
							e['state'] = False

				# Обновляем информацию в базе
				placing_way = PlacingWay.objects.update(
					placing_way_id   = e['placing_way_id'],
					code             = e['code'],
					name             = e['name'],
					placing_way_type = e['placing_way_type'],
					subsystem_type   = e['subsystem_type'],
					state            = e['state'])

				print("Обновлён элемент Путь размещения: {}.".format(placing_way))

		return True


	def parsePlanPositionChangeReason(self, xml_data, region = None):
		'Парсит пути причины изменения позиций планов закупок.'

		# Импортируем
		from lxml import etree

		# Парсим
		tree = etree.parse(xml_data)

		# Получаем корневой элемент
		root = tree.getroot()

		# Получаем список
		for element_list in root:

			# Получаем элемент
			for element in element_list:

				# Инициируем пустой справочник элемента
				e = {}

				# Обрабатываем значения полей
				for value in element:

					# oos_id
					if value.tag.endswith('id'):
						e['oos_id'] = value.text

					# name
					elif value.tag.endswith('name'):
						e['name'] = value.text

					# description
					elif value.tag.endswith('description'):
						e['description'] = value.text

					# state
					elif value.tag.endswith('actual'):
						if value.text == 'true':
							e['state'] = True
						else:
							e['state'] = False

				# Обновляем информацию в базе
				plan_position_change_reason = PlanPositionChangeReason.objects.update(
					oos_id      = e['oos_id'],
					name        = e['name'],
					description = e['description'],
					state       = e['state'])

				print("Обновлён элемент Причина изменения позиции плана: {}.".format(plan_position_change_reason))

		return True


	def parsePlanGraph(self, xml_data, region = None):
		'Парсит планы-графики.'

		# Импортируем
		from lxml import etree

		# Парсим
		tree = etree.parse(xml_data)

		# Чистим теги
		for element in tree.xpath('.//*'):
			element.tag = element.tag.split('}')[1]

		# Планы-графики
		pgs = tree.xpath('.//tenderPlan')

		for pg in pgs:

			# План-график
			plan_graph = {}

			plan_graph['oos_id']                     = pg.xpath('./commonInfo/id')[0].text
			plan_graph['number']                     = pg.xpath('./commonInfo/planNumber')[0].text
			plan_graph['year']                       = pg.xpath('./commonInfo/year')[0].text
			plan_graph['version']                    = pg.xpath('./commonInfo/versionNumber')[0].text
			plan_graph['owner_reg_number']           = pg.xpath('./commonInfo/owner/regNum')[0].text
			plan_graph['create_date']                = pg.xpath('./commonInfo/createDate')[0].text
			plan_graph['description']                = pg.xpath('./commonInfo/description')[0].text.strip()
			plan_graph['confirm_date']               = pg.xpath('./commonInfo/confirmDate')[0].text
			plan_graph['publish_date']               = pg.xpath('./commonInfo/publishDate')[0].text
			plan_graph['customer_reg_number']        = pg.xpath('./customerInfo/customer/regNum')[0].text
			plan_graph['oktmo_code']                 = pg.xpath('./customerInfo/OKTMO/code')[0].text
			plan_graph['contact_person_last_name']   = pg.xpath('./responsibleContactInfo/lastName')[0].text
			plan_graph['contact_person_first_name']  = pg.xpath('./responsibleContactInfo/firstName')[0].text
			plan_graph['contact_person_middle_name'] = pg.xpath('./responsibleContactInfo/middleName')[0].text
			try:
				plan_graph['contact_person_phone']   = pg.xpath('./responsibleContactInfo/phone')[0].text
			except IndexError:
				plan_graph['contact_person_phone']   = None
			try:
				plan_graph['contact_person_fax']     = pg.xpath('./responsibleContactInfo/fax')[0].text
			except IndexError:
				plan_graph['contact_person_fax']     = None
			try:
				plan_graph['contact_person_email']   = pg.xpath('./responsibleContactInfo/email')[0].text
			except:
				plan_graph['contact_person_email']   = None

			plan_graph['owner'] = Organisation.objects.take(
				reg_number = plan_graph['owner_reg_number'])

			plan_graph['customer'] = Organisation.objects.take(
				reg_number = plan_graph['customer_reg_number'])

			try:
				plan_graph['oktmo'] = OKTMO.objects.get(
					code = plan_graph['oktmo_code'])
			except OKTMO.DoesNotExist:
				plan_graph['oktmo'] = None


			plan_graph['contact_person'] = ContactPerson.objects.take(
				last_name   = plan_graph['contact_person_last_name'],
				first_name  = plan_graph['contact_person_first_name'],
				middle_name = plan_graph['contact_person_middle_name'],
				email       = plan_graph['contact_person_email'],
				phone       = plan_graph['contact_person_phone'],
				fax         = plan_graph['contact_person_fax'])

			plan_graph = PlanGraph.objects.update(
				oos_id         = plan_graph['oos_id'],
				number         = plan_graph['number'],
				year           = plan_graph['year'],
				version        = plan_graph['version'],
				region         = region,
				owner          = plan_graph['owner'],
				create_date    = plan_graph['create_date'],
				description    = plan_graph['description'],
				confirm_date   = plan_graph['confirm_date'],
				publish_date   = plan_graph['publish_date'],
				customer       = plan_graph['customer'],
				oktmo          = plan_graph['oktmo'],
				contact_person = plan_graph['contact_person'])

			msg = "План-график: {}.".format(plan_graph)
			print(msg)

			# Позиции планов-графиков
			ps = pg.xpath('./providedPurchases/positions/position')

			for p in ps:

				# Позиция плана-графика
				position = {}

				position['number']               = p.xpath('./commonInfo/positionNumber')[0].text
				try:
					position['ext_number']       = p.xpath('./commonInfo/extNumber')[0].text
				except IndexError:
					position['ext_number']       = None

				# TODO KBKs Бюджетирование по годам?

				position['okveds']                   = p.xpath('./commonInfo/OKVEDs/OKVED/code')
				position['okpds']                    = p.xpath('./products/product/OKPD/code')

				try:
					position['subject_name']     = p.xpath('./commonInfo/contractSubjectName')[0].text.strip()
				except AttributeError:
					position['subject_name']     = 'None'

				position['max_price']                = p.xpath('./commonInfo/contractMaxPrice')[0].text
				try:
					position['payments']         = p.xpath('./commonInfo/payments')[0].text
				except IndexError:
					position['payments']         = None
				position['currency_code']            = p.xpath('./commonInfo/contractCurrency/code')[0].text
				position['placing_way_code']         = p.xpath('./commonInfo/placingWay/code')[0].text
				try:
					position['change_reason_id']     = p.xpath('./commonInfo/positionModification/changeReason/id')[0].text
				except IndexError:
					position['change_reason_id']     = None
				try:
					position['publish_date']         = p.xpath('./commonInfo/positionPublishDate')[0].text
				except IndexError:
					position['publish_date']         = plan_graph.publish_date
				try:
					position['no_public_discussion'] = p.xpath('./commonInfo/noPublicDiscussion')[0].text
				except IndexError:
					position['no_public_discussion'] = False
				try:
					position['placing_year']         = p.xpath('./purchaseConditions/purchaseGraph/purchasePlacingTerm/year')[0].text
				except IndexError:
					position['placing_year']         = None
				try:
					position['placing_month']        = p.xpath('./purchaseConditions/purchaseGraph/purchasePlacingTerm/month')[0].text
				except IndexError:
					position['placing_month']        = None
				try:
					position['execution_year']       = p.xpath('./purchaseConditions/purchaseGraph/contractExecutionTerm/year')[0].text
				except IndexError:
					position['execution_year']       = None
				try:
					position['execution_month']      = p.xpath('./purchaseConditions/purchaseGraph/contractExecutionTerm/month')[0].text
				except IndexError:
					position['execution_month']      = None

				for n, okved in enumerate(position['okveds']):
					try:
						position['okveds'][n] = OKVED.objects.get(
							code = okved.text)
					except OKVED.DoesNotExist:
						position['okveds'][n] = None

				for n, okpd in enumerate(position['okpds']):
					try:
						position['okpds'][n] = OKPD.objects.get(
							code = okpd.text)
					except OKPD.DoesNotExist:
						position['okpds'][n] = None

				try:
					position['currency'] = Currency.objects.get(
						code = position['currency_code'])
				except Currency.DoesNotExist:
					position['currency'] = None

				position['placing_way'] = PlacingWay.objects.take(
					code = position['placing_way_code'])

				try:
					position['change_reason'] = PlanPositionChangeReason.objects.get(
						oos_id = position['change_reason_id'])
				except PlanPositionChangeReason.DoesNotExist:
					position['change_reason'] = None

				if position['no_public_discussion'] == 'true':
					position['public_discussion'] = False
				else:
					position['public_discussion'] = True

				position = PlanGraphPosition.objects.update(
					plan_graph        = plan_graph,
					number            = position['number'],
					ext_number        = position['ext_number'],
					okveds            = position['okveds'],
					okpds             = position['okpds'],
					subject_name      = position['subject_name'],
					max_price         = position['max_price'],
					payments          = position['payments'],
					currency          = position['currency'],
					placing_way       = position['placing_way'],
					change_reason     = position['change_reason'],
					publish_date      = position['publish_date'],
					public_discussion = position['public_discussion'],
					placing_year      = position['placing_year'],
					placing_month     = position['placing_month'],
					execution_year    = position['execution_year'],
					execution_month   = position['execution_month'],
					state             = True)

				print(".", end = "")

				# Продукты
				prs = p.xpath('./products/product')

				for number, pr in enumerate(prs):

					# Продукт
					product = {}

					product['okpd_code']                 = pr.xpath('./OKPD/code')[0].text
					product['name']                      = pr.xpath('./name')[0].text
					product['min_requirement']           = pr.xpath('./minRequirement')[0].text
					try:
						product['okei_code']             = pr.xpath('./OKEI/code')[0].text
					except IndexError:
						product['okei_code']             = None
					try:
						product['max_sum']               = pr.xpath('./sumMax')[0].text
					except IndexError:
						product['max_sum']               = None
					try:
						product['price']                 = pr.xpath('./price')[0].text
					except IndexError:
						product['price']                 = None
					product['quantity_undefined']        = pr.xpath('./quantityUndefined')[0].text
					try:
						product['quantity']              = pr.xpath('./quantity')[0].text
					except IndexError:
						product['quantity']              = None
					try:
						product['quantity_current_year'] = pr.xpath('./quantityCurrentYear')[0].text
					except IndexError:
						product['quantity_current_year'] = None

					try:
						product['okpd'] = OKPD.objects.get(
							code = product['okpd_code'])
					except OKPD.DoesNotExist:
						product['okpd'] = None

					try:
						product['okei'] = OKEI.objects.get(
							code = product['okei_code'])
					except OKEI.DoesNotExist:
						product['okei'] = None

					product = PlanGraphPositionProduct.objects.update(
						position              = position,
						number                = number,
						okpd                  = product['okpd'],
						name                  = product['name'],
						min_requirement       = product['min_requirement'],
						okei                  = product['okei'],
						max_sum               = product['max_sum'],
						price                 = product['price'],
						quantity_undefined    = product['quantity_undefined'],
						quantity              = product['quantity'],
						quantity_current_year = product['quantity_current_year'],
						state                 = True)

					print(".", end = "")

			print("\n")

		# Отмена планов-графиков
		pgs = tree.xpath('.//tenderPlanCancel')

		for pg in pgs:

			# План-график
			plan_graph = {}

			plan_graph['oos_id'] = pg.xpath('./id')[0].text
			plan_graph['number'] = pg.xpath('./planNumber')[0].text

			plan_graph = PlanGraph.objects.cancel(
				oos_id = plan_graph['oos_id'],
				number = plan_graph['number'])

			msg = "Отменен план-график."
			print(msg)

		# Планы-графики (неструктурированные)
		pgs = tree.xpath('.//tenderPlanUnstructured')

		for pg in pgs:

			# План-график
			plan_graph = {}

			plan_graph['oos_id']                     = pg.xpath('./commonInfo/id')[0].text
			plan_graph['number']                     = pg.xpath('./commonInfo/planNumber')[0].text
			plan_graph['year']                       = pg.xpath('./commonInfo/year')[0].text
			plan_graph['version']                    = pg.xpath('./commonInfo/versionNumber')[0].text
			plan_graph['owner_reg_number']           = pg.xpath('./commonInfo/owner/regNum')[0].text
			plan_graph['create_date']                = pg.xpath('./commonInfo/createDate')[0].text
			plan_graph['description']                = pg.xpath('./commonInfo/description')[0].text.strip()
			plan_graph['confirm_date']               = pg.xpath('./commonInfo/confirmDate')[0].text
			plan_graph['publish_date']               = pg.xpath('./commonInfo/publishDate')[0].text
			plan_graph['customer_reg_number']        = pg.xpath('./customerInfo/customer/regNum')[0].text
			plan_graph['oktmo_code']                 = pg.xpath('./customerInfo/OKTMO/code')[0].text
			plan_graph['contact_person_last_name']   = pg.xpath('./responsibleContactInfo/lastName')[0].text
			plan_graph['contact_person_first_name']  = pg.xpath('./responsibleContactInfo/firstName')[0].text
			plan_graph['contact_person_middle_name'] = pg.xpath('./responsibleContactInfo/middleName')[0].text
			try:
				plan_graph['contact_person_phone']   = pg.xpath('./responsibleContactInfo/phone')[0].text
			except IndexError:
				plan_graph['contact_person_phone']   = None
			try:
				plan_graph['contact_person_fax']     = pg.xpath('./responsibleContactInfo/fax')[0].text
			except IndexError:
				plan_graph['contact_person_fax']     = None
			try:
				plan_graph['contact_person_email']   = pg.xpath('./responsibleContactInfo/email')[0].text
			except:
				plan_graph['contact_person_email']   = None

			plan_graph['owner'] = Organisation.objects.take(
				reg_number = plan_graph['owner_reg_number'])

			plan_graph['customer'] = Organisation.objects.take(
				reg_number = plan_graph['customer_reg_number'])

			try:
				plan_graph['oktmo'] = OKTMO.objects.get(
					code = plan_graph['oktmo_code'])
			except OKTMO.DoesNotExist:
				plan_graph['oktmo'] = None

			plan_graph['contact_person'] = ContactPerson.objects.take(
				last_name   = plan_graph['contact_person_last_name'],
				first_name  = plan_graph['contact_person_first_name'],
				middle_name = plan_graph['contact_person_middle_name'],
				email       = plan_graph['contact_person_email'],
				phone       = plan_graph['contact_person_phone'],
				fax         = plan_graph['contact_person_fax'])

			plan_graph = PlanGraph.objects.update(
				oos_id         = plan_graph['oos_id'],
				number         = plan_graph['number'],
				year           = plan_graph['year'],
				version        = plan_graph['version'],
				region         = region,
				owner          = plan_graph['owner'],
				create_date    = plan_graph['create_date'],
				description    = plan_graph['description'],
				confirm_date   = plan_graph['confirm_date'],
				publish_date   = plan_graph['publish_date'],
				customer       = plan_graph['customer'],
				oktmo          = plan_graph['oktmo'],
				contact_person = plan_graph['contact_person'])

			msg = "План-график (неструктурированный): {}.\n".format(plan_graph)
			print(msg)

		# Чистим мусор
		del tree
		gc.collect()

		return True


	def updateRegions(self):
		'Обновляет список регионов'

		# Черный лист
		black_list = ['_logs']

		# Получаем список регионов с FTP-сервера
		regions = self.getFTPCatalog(self.urls['regions'])
		print('Получен список регионов.')

		for region in regions:

			if not region in black_list:
				region = Region.objects.take(
					alias = region,
					name = region,
					full_name = region)

		return True


