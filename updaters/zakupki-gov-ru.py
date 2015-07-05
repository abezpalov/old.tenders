from tenders.models import *


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
			'organisation_type':           self.parseOrganisationType,
			'organisation':                self.parseOrganisation,
			'placing_way':                 self.parsePlacingWay,
			'plan_position_change_reason': self.parsePlanPositionChangeReason,

			'plangraph':                   self.parsePlanGraph
		}


	def run(self):

		# Проверяем наличие параметров авторизации
		if not self.updater.login or not self.updater.password:
			print('Ошибка: Проверьте параметры авторизации. Кажется их нет.')
			return False

		# Обновляем справочники
		self.getEssencesList()

		self.updateEssence('country')
		self.updateEssence('currency')
		self.updateEssence('okei')
		self.updateEssence('kosgu')
		self.updateEssence('okopf')
		self.updateEssence('okpd')
		self.updateEssence('oktmo')
		self.updateEssence('okved')

		self.updateEssence('budget')
		self.updateEssence('budget_type')

		self.updateEssence('organisation_type')
		self.updateEssence('organisation')

		self.updateEssence('placing_way')
		self.updateEssence('plan_position_change_reason')

		self.updateEssence('purchase_document_type')
		self.updateEssence('purchase_preference')
		self.updateEssence('purchase_reject_reason')

		# Обновляем планы регионов
		self.updateRegions()

		# Получаем спиисок "нужных" регионов
		regions = Region.objects.filter(state = True)

		for region in regions:

			# TODO Обработка планов-графиков
			catalogs = [
#				"{}/{}/{}".format(
#					self.urls['regions'],
#					region.alias,
#					self.urls['plangraph']),
#				"{}/{}/{}/{}".format(
#					self.urls['regions'],
#					region.alias,
#					self.urls['plangraph'],
#					self.urls['prev_month']),
				"{}/{}/{}/{}".format(
					self.urls['regions'],
					region.alias,
					self.urls['plangraph'],
					self.urls['prev_month'])]

			for catalog in catalogs:
				self.updateEssence(essence = 'plangraph', catalog = catalog)

			print(catalog)


		# Обновляем тендеры регионов
		# TODO

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


	def getEssencesList(self):
		'Получает список сущностей для тестирования'

		essences = self.getFTPCatalog(self.urls['essences'])

		return essences


	def updateEssence(self, essence, catalog = None):
		'Получает файлы сущностей для анализа и обработки'

		# Импортируем
		from io import TextIOWrapper

		# Получаем список файлов
		if catalog is None:
			catalog = "/{}/{}".format(self.urls['essences'], self.urls[essence])

		zip_names = self.getFTPCatalog(catalog)

		# Загружаем архивы
		for zip_name in zip_names:

			# Скачиваем архив
			zip_data = self.getZipFromFTP(zip_name, catalog)
			print("Скачал файл {}.".format(zip_name))

			if not zip_data:
				print("Ошибка: невозможно скачать файл. Перехожу с следующему.")
				continue

			# Получаем список файлов в архиве
			xml_names = zip_data.namelist()
			for xml_name in xml_names:

				# Извлекаем файл из архива
				xml_data = zip_data.open(xml_name)
				print("Извлек файл {}.".format(xml_name))

				# Парсим файл
				try:
					parse = self.parsers[essence]
				except KeyError:
					print('Ошибка: отсутствует парсер для сущности {}.'.format(essence))
					continue

				parse(xml_data)
				print("Файл {} обработан.".format(xml_name))

		return True


	def parseCountry(self, xml_data):
		'Парсит страны'

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
					if   value.tag.endswith('countryCode'):
						e['code'] = value.text
					elif value.tag.endswith('countryFullName'):
						e['full_name'] = value.text
					elif value.tag.endswith('actual'):
						if value.text == 'true':
							e['state'] = True
						else:
							e['state'] = False

				# Обновляем информацию в базе
				country = Country.objects.update(
					code         = e['code'],
					full_name    = e['full_name'],
					state        = e['state'])

				print("Обновлена страна: {}.".format(country))

		return True


	def parseCurrency(self, xml_data):
		'Парсит валюты'

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
					if   value.tag.endswith('code'):
						e['code'] = value.text
					elif value.tag.endswith('digitalCode'):
						e['digital_code'] = value.text
					elif value.tag.endswith('name'):
						e['name'] = value.text
					elif value.tag.endswith('actual'):
						if value.text == 'true':
							e['state'] = True
						else:
							e['state'] = False

				# Обновляем информацию в базе
				currency = Currency.objects.update(
					code         = e['code'],
					digital_code = e['digital_code'],
					name         = e['name'],
					state        = e['state'])

				print("Обновлена валюта.".format(currency))

		return True


	def parseOKEI(self, xml_data):
		'Парсит единицы измерения'

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

					# full_name
					elif value.tag.endswith('fullName'):
						e['full_name'] = value.text

					# section
					elif value.tag.endswith('section'):

						for section_value in value:

							if section_value.tag.endswith('code'):
								e['section_code'] = section_value.text
							elif section_value.tag.endswith('name'):
								e['section_name'] = section_value.text

					# group
					elif value.tag.endswith('group'):

						for group_value in value:

							if group_value.tag.endswith('id'):
								e['group_code'] = group_value.text
							elif group_value.tag.endswith('name'):
								e['group_name'] = group_value.text

					# local_name
					elif value.tag.endswith('localName'):
						e['local_name'] = value.text

					# international_name
					elif value.tag.endswith('internationalName'):
						e['international_name'] = value.text

					# local_symbol
					elif value.tag.endswith('localSymbol'):
						e['local_symbol'] = value.text

					# international_symbol
					elif value.tag.endswith('internationalSymbol'):
						e['international_symbol'] = value.text

					# state
					elif value.tag.endswith('actual'):
						if value.text == 'true':
							e['state'] = True
						else:
							e['state'] = False

				# Обновляем информацию в базе
				okei_section = OKEISection.objects.update(
					code         = e['section_code'],
					name         = e['section_name'],
					state        = True)
				okei_group = OKEIGroup.objects.update(
					code         = e['group_code'],
					name         = e['group_name'],
					state        = True)
				okei = OKEI.objects.update(
					code                 = e['code'],
					full_name            = e['full_name'],
					section              = okei_section,
					group                = okei_group,
					local_name           = e['local_name'],
					international_name   = e['international_name'],
					local_symbol         = e['local_symbol'],
					international_symbol = e['international_symbol'],
					state                = e['state'])

				print("Обновлена единица измерения: {}.".format(okei))

		return True


	def parseKOSGU(self, xml_data):
		'Парсит классификатор операций сектора государственного управления.'

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
						if not value.text or value.text == '000':
							e['parent_code'] = None
						else:
							e['parent_code'] = value.text
	
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
					e['parent_code'] = e['parent_code']
				except KeyError:
					e['parent_code'] = None

				kosgu = KOSGU.objects.update(
					code        = e['code'],
					parent_code = e['parent_code'],
					name        = e['name'],
					state       = e['state'])

				print("Обновлён элемент КОСГУ: {}.".format(kosgu))

		return True


	def parseOKOPF(self, xml_data):
		'Парсит ОКОПФ.'

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

					# singular_name
					elif value.tag.endswith('singularName'):
						e['singular_name'] = value.text

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


				okopf = OKOPF.objects.update(
					code          = e['code'],
					parent_code   = e['parent_code'],
					full_name     = e['full_name'],
					singular_name = e['singular_name'],
					state         = e['state'])

				print("Обновлён элемент ОКОПФ: {}.".format(okopf))

		return True


	def parseOKPD(self, xml_data):
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
						e['code'] = value.text

					# parent_code
					elif value.tag.endswith('parentId'):
						if not value.text:
							e['parent_code'] = None
						else:
							e['parent_code'] = value.text

					# alias
					elif value.tag.endswith('code'):
						e['alias'] = value.text	

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
					e['parent_code'] = e['parent_code']
				except KeyError:
					e['parent_code'] = None

				okpd = OKPD.objects.update(
					code        = e['code'],
					parent_code = e['parent_code'],
					alias       = e['alias'],
					name        = e['name'],
					state       = e['state'])

				print("Обновлён элемент ОКДП: {}.".format(okpd))

		return True


	def parseOKTMO(self, xml_data):
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


	def parseOKVED(self, xml_data):
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


	def parseBudget(self, xml_data):
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


	def parseBudgetType(self, xml_data):
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


	def parseOrganisationType(self, xml_data):
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

	# TODO parseOrganisation

	def parseOrganisation(self, xml_data):
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


	def parsePlacingWay(self, xml_data):
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


	def parsePlanPositionChangeReason(self, xml_data):
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


	def parsePlanGraph(self, xml_data):
		'Парсит планы-графики.'

		# Импортируем
		from lxml import etree

		# Парсим
		tree = etree.parse(xml_data)

		# Получаем корневой элемент
		root = tree.getroot()

		# Получаем список
		for element_list in root:

			# План
			if element_list.tag.endswith('tenderPlan'):

				# Инициируем пустой справочник элемента
				e = {}

				for element in element_list:

					# Основная информация о плане
					if element.tag.endswith('commonInfo'):

						for value in element:

							if   value.tag.endswith('id'):            e['plan_oos_id']       = value.text
							elif value.tag.endswith('planNumber'):    e['plan_number']       = value.text
							elif value.tag.endswith('year'):          e['plan_year']         = value.text
							elif value.tag.endswith('versionNumber'): e['plan_version']      = value.text
							elif value.tag.endswith('createDate'):    e['plan_created']      = value.text
							elif value.tag.endswith('confirmDate'):   e['plan_confirmed']    = value.text
							elif value.tag.endswith('publishDate'):   e['plan_published']    = value.text
							elif value.tag.endswith('description'):   e['plan_description']  = value.text

							# Владелец
							elif value.tag.endswith('owner'):
								for sub in value:
									if sub.tag.endswith('regNum'):
										e['owner'] = sub.text

					# Информация о заказчике
					elif element.tag.endswith('customerInfo'):
						for value in element:

							# Заказчик
							if value.tag.endswith('customer'):
								for sub in value:
									if sub.tag.endswith('regNum'):
										e['customer'] = sub.text

							# ОКТМО
							elif value.tag.endswith('OKTMO'):
								for sub in value:
									if sub.tag.endswith('code'):
										e['oktmo_code'] = sub.text

					# Контактное лицо
					elif element.tag.endswith('responsibleContactInfo'):
						for value in element:
							if value.tag.endswith('firstName'):    e['contact_person_first_name']  = value.text
							elif value.tag.endswith('lastName'):   e['contact_person_last_name']   = value.text
							elif value.tag.endswith('middleName'): e['contact_person_middle_name'] = value.text
							elif value.tag.endswith('email'):      e['contact_person_email']       = value.text
							elif value.tag.endswith('phone'):      e['contact_person_phone']       = value.text
							elif value.tag.endswith('fax'):        e['contact_person_fax']         = value.text

					# Сопровождаемые данные?
					elif element.tag.endswith('providedPurchases'):

						for value in element:

							# Список позиций
							if value.tag.endswith('positions'):

								e['positions'] = []

								# Позиция
								for position in value:

									p = {}

									for position_element in position:

										if position_element.tag.endswith('commonInfo'):

											for position_sub in position_element:

												if position_sub.tag.endswith('positionNumber'):

													p['position_number'] = position_sub.text

												# Amounts KBKs
												elif position_sub.tag.endswith('amountKBKs'):
													p['kbks'] = []
													for kbk_element in position_sub:
														k = {}
														for kbk_value in kbk_element:
															if kbk_value.tag.endswith('code'):
																k['code'] = kbk_value.text
														p['kbks'].append(k)

												# ОКВЭД
												elif position_sub.tag.endswith('OKVEDs'):
													p['okveds'] = []
													for okved_element in position_sub:
														o = {}
														for okved_value in okved_element:
															if okved_value.tag.endswith('code'):
																o['code'] = okved_value.text
														p['okveds'].append(o)

												elif position_sub.tag.endswith('contractSubjectName'):
													p['position_subject_name'] = position_sub.text

												elif position_sub.tag.endswith('contractMaxPrice'):
													p['position_max_price'] = position_sub.text

												elif position_sub.tag.endswith('payments'):
													p['payments'] = position_sub.text

												elif position_sub.tag.endswith('contractCurrency'):
													for currency_value in position_sub:
														if currency_value.tag.endswith('code'):
															p['currency_code'] = currency_value.text

												elif position_sub.tag.endswith('placingWay'):
													for placing_way_value in position_sub:
														if placing_way_value.tag.endswith('code'):
															p['placing_way_code'] = placing_way_value.text

												elif position_sub.tag.endswith('positionModification'):
													for position_modification_value in position_sub:

														if position_modification_value.tag.endswith('changeReason'):
															for change_reason_value in position_modification_value:
																if change_reason_value.tag.endswith('id'):
																	p['change_reason_id'] = change_reason_value.text

										# Продукты
										elif position_element.tag.endswith('products'):

											p['products'] = []

											for product_element in position_element:

												pr = {}

												for product_value in product_element:

													if product_value.tag.endswith('OKPD'):
														for okpd_value in product_value:
															if okpd_value.tag.endswith('code'):
																pr['okpd_code'] = okpd_value.text

													elif product_value.tag.endswith('name'):
														pr['name'] = product_value.text

													elif product_value.tag.endswith('minRequirement'):
														pr['min_requirement'] = product_value.text

													elif product_value.tag.endswith('OKEI'):
														for okei_value in product_value:
															if okei_value.tag.endswith('code'):
																pr['okei_code'] = okei_value.text

													elif product_value.tag.endswith('sumMax'):
														pr['sum_max'] = product_value.text

													elif product_value.tag.endswith('price'):
														pr['price'] = product_value.text

													elif product_value.tag.endswith('quantityUndefined'):
														pr['quantity_undefined'] = product_value.text

													elif product_value.tag.endswith('quantity'):
														pr['quantity'] = product_value.text

												p['products'].append(pr)

									e['positions'].append(p)

				# Записываем в базу
				print('\n')
				print(e)
				print('\n')

				try:
					e['owner'] = Organisation.objects.take(e['owner'])
				except KeyError:
					e['owner'] = None
				except Organisation.DoesNotExist:
					e['owner'] = None

				try:
					e['customer'] = Organisation.objects.take(e['customer'])
				except KeyError:
					e['customer'] = None
				except Organisation.DoesNotExist:
					e['customer'] = None

				try:
					e['oktmo'] = OKTMO.objects.take(e['oktmo'])
				except KeyError:
					e['oktmo'] = None
				except OKTMO.DoesNotExist:
					e['oktmo'] = None

				try:
					e['contact_person_email'] = e['contact_person_email']
				except KeyError:
					e['contact_person_email'] = None

				try:
					e['contact_person_phone'] = e['contact_person_phone']
				except KeyError:
					e['contact_person_phone'] = None

				try:
					e['contact_person_fax'] = e['contact_person_fax']
				except KeyError:
					e['contact_person_fax'] = None

				try:
					e['contact_person'] = ContactPerson.objects.take(
						first_name  = e['contact_person_first_name'],
						middle_name = e['contact_person_middle_name'],
						last_name   = e['contact_person_last_name'],
						email       = e['contact_person_email'],
						phone       = e['contact_person_phone'],
						fax         = e['contact_person_fax'])
				except KeyError:
					e['contact_person'] = None
				except OKTMO.DoesNotExist:
					e['contact_person'] = None

				# Обновляем информацию в базе
				plan_graph = PlanGraph.objects.update(
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




			# Tender Plan Cancel
			elif element_list.tag.endswith('tenderPlanCancel'):
				print('Tender Plan Cancel')

			# Tender Plan Unstructured
			elif element_list.tag.endswith('tenderPlanUnstructured'):
				print('Tender Plan Cancel')






		return True
























	# TODO Parser
	# TODO Parser
	# TODO Parser
	# TODO Parser
	# TODO Parser
	# TODO Parser
	# TODO Parser
	# TODO Parser
	# TODO Parser
	# TODO Parser
	# TODO Parser
	# TODO Parser
	# TODO Parser
	# TODO Parser
	# TODO Parser
	# TODO Parser
	# TODO Parser
	# TODO Parser


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


