#import gc
import tenders.runner
from tenders.models import *


class Runner(tenders.runner.Runner):


	name  = 'Обновление с сайта государственных закупок России'
	alias = 'zakupki-gov-ru'

	black_list = ['_logs', 'fcs_undefined', 'auditresult', 'customerreports']


	def __init__(self):

		super().__init__()

		self.url = 'ftp.zakupki.gov.ru'

		self.categories = {
			'essences'                    : 'fcs_nsi',
			'regions'                     : 'fcs_regions',

			'plangraph'                   : 'plangraphs',
			# TODO

			'prev_month'                  : 'prevMonth',
			'curr_month'                  : 'currMonth'
		}

		self.essences = [
			{'category' : 'nsiOKSM',                           'parser' : self.parse_country},
			{'category' : 'nsiCurrency',                       'parser' : self.parse_currency},
			{'category' : 'nsiContractCurrencyCBRF',           'parser' : self.parse_currency},
			{'category' : 'nsiOKEI',                           'parser' : self.parse_okei},
			{'category' : 'nsiKOSGU',                          'parser' : self.parse_kosgu},
			{'category' : 'nsiOKOPF',                          'parser' : self.parse_okopf},
			{'category' : 'nsiOKPD',                           'parser' : self.parse_okpd},
			{'category' : 'nsiOKPD2',                          'parser' : self.parse_okpd2},
			{'category' : 'nsiOKTMO',                          'parser' : self.parse_oktmo},
			{'category' : 'nsiOKVED',                          'parser' : self.parse_okved},
			{'category' : 'nsiOKVED2',                         'parser' : self.parse_okved2},
			{'category' : 'nsiBudget',                         'parser' : self.parse_budget},
			{'category' : 'nsiOffBudgetType',                  'parser' : self.parse_budget_type},
			{'category' : 'nsiKBKBudget',                      'parser' : self.parse_kbk_budget},
			{'category' : 'nsiOrganizationType',               'parser' : self.parse_organisation_type},

			{'category' : 'nsiOrganization',                   'parser' : self.parse_organisation},

#			{'category' : 'nsiPlacingWay',                     'parser' : self.parse_},
#			{'category' : 'nsiPlanPositionChangeReason',       'parser' : self.parse_},
#			{'category' : 'nsiPurchaseDocumentTypes',          'parser' : self.parse_},
#			{'category' : 'nsiPurchasePreferences',            'parser' : self.parse_},
#			{'category' : 'nsiPurchaseRejectReason',           'parser' : self.parse_},

#			{'category' : 'fcsStandardContract',               'parser' : self.parse_},
#			{'category' : 'fcsStandardContractInvalid',        'parser' : self.parse_},
#			{'category' : 'nsiAbandonedReason',                'parser' : self.parse_},
#			{'category' : 'nsiAuditActionSubjects',            'parser' : self.parse_},
#			{'category' : 'nsiBankGuaranteeRefusalReason',     'parser' : self.parse_},
#			{'category' : 'nsiBusinessControls',               'parser' : self.parse_},
#			{'category' : 'nsiCalendarDays',                   'parser' : self.parse_},
#			{'category' : 'nsiCommission',                     'parser' : self.parse_},
#			{'category' : 'nsiCommissionRole',                 'parser' : self.parse_},
#			{'category' : 'nsiContractExecutionDoc',           'parser' : self.parse_},
#			{'category' : 'nsiContractModificationReason',     'parser' : self.parse_},
#			{'category' : 'nsiContractOKOPFExtraBudget',       'parser' : self.parse_},
#			{'category' : 'nsiContractPenaltyReason',          'parser' : self.parse_},
#			{'category' : 'nsiContractPriceChangeReason',      'parser' : self.parse_},
#			{'category' : 'nsiContractRefusalReason',          'parser' : self.parse_},
#			{'category' : 'nsiContractReparationDoc',          'parser' : self.parse_},
#			{'category' : 'nsiContractSingleCustomerReason',   'parser' : self.parse_},
#			{'category' : 'nsiContractTerminationReason',      'parser' : self.parse_},
#			{'category' : 'nsiDeviationFactFoundation',        'parser' : self.parse_},
#			{'category' : 'nsiEvalCriterion',                  'parser' : self.parse_},
#			{'category' : 'nsiKVR',                            'parser' : self.parse_},
#			{'category' : 'nsiModifyReasonOZ',                 'parser' : self.parse_},
#			{'category' : 'nsiPublicDiscussionDecisions',      'parser' : self.parse_},
#			{'category' : 'nsiPublicDiscussionQuestionnaries', 'parser' : self.parse_},
#			{'category' : 'nsiSingleCustomerReasonOZ',         'parser' : self.parse_},
#			{'category' : 'nsiSpecialPurchase',                'parser' : self.parse_},

#			{'category' : 'nsiOrganizationRights',             'parser' : self.parse_},

		]

	def run(self):

		# Обновляем справочники
		for essence in self.essences:

			# Проверяем не вышло ли время
			if self.is_time_up():
				return True

			self.update_essence(essence)

		# Получаем список регионов с FTP-сервера
		for region in self.get_ftp_catalog(self.url, self.categories['regions']):

			try:
				self.get_ftp_catalog(self.url, '{}/{}'.format(self.categories['regions'], region))
				if not region in self.black_list:
					region = Region.objects.take(
						alias = region,
						name = region,
						full_name = region)
					print("Обновлён регион: {}.".format(region))
			except Exception:
				print('.')

		# Получаем спиисок "нужных" регионов
		regions = Region.objects.filter(state = True)

#		for region in regions:

#			catalogs = [
#				"{}/{}/{}/{}".format(
#					self.urls['regions'],
#					region.alias,
#					self.urls['plangraph'],
#					self.urls['prev_month']),
#				"{}/{}/{}/{}".format(
#					self.urls['regions'],
#					region.alias,
#					self.urls['plangraph'],
#					self.urls['curr_month'])]

#			for catalog in catalogs:

				# Обрабатываем планы-графики
#				self.updateEssence(
#					essence = 'plangraph',
#					catalog = catalog,
#					region = region)

				# TODO Обновляем тендеры регионов

		print("Обработки завершены за {}.".format(timezone.now() - self.start_time))
		return True


	def update_essence(self, essence):
		'Получает файлы сущностей для анализа и обработки'

		catalog = "{}/{}".format(self.categories['essences'], essence['category'])

		zip_names = self.get_ftp_catalog(self.url, catalog)

		# Загружаем архивы
		for zip_name in zip_names:

			# Проверяем, не вышло ли время
			if self.is_time_up():
				return True

			# Проверяем, не обработан ли файл
			source = Source.objects.take(url = "{}/{}/{}".format(self.url, catalog, zip_name))
			if source.is_parsed():
				continue

			# Скачиваем архив
			zip_data = self.get_file_from_ftp(self.url, catalog, zip_name)

			if not zip_data:
				continue

			# Проходим по всем файлам в архиве
			for xml_name in zip_data.namelist():

				# Извлекаем данные
				tree = self.get_tree_from_zip(zip_data, xml_name)
				if tree:
					tree = self.clear_tags(tree)
				else:
					return False

				# Обрабатываем файл
				parse = essence['parser']
				parse(tree)

			print("Все файлы архива обработаны.")

			source.complite()

		return True


	def parse_country(self, tree):
		'Парсит страны.'

		for element in tree.xpath('.//nsiOKSM'):

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


	def parse_currency(self, tree):
		'Парсит валюты.'

		for element in tree.xpath('.//nsiCurrency'):

			o                 = {}
			o['code']         = element.xpath('./code')[0].text
			o['digital_code'] = element.xpath('./digitalCode')[0].text
			o['name']         = element.xpath('./name')[0].text

			if element.xpath('./actual')[0].text == 'true':
				o['state'] = True
			else:
				o['state'] = False

			currency = Currency.objects.update(
				code         = o['code'],
				digital_code = o['digital_code'],
				name         = o['name'],
				state        = o['state'])

			print("Валюта: {}.".format(currency))

		for element in tree.xpath('.//currency'):

			o                 = {}
			o['code']         = element.xpath('./code')[0].text
			o['digital_code'] = element.xpath('./digitalCode')[0].text
			o['name']         = element.xpath('./name')[0].text

			currency = Currency.objects.update(
				code         = o['code'],
				digital_code = o['digital_code'],
				name         = o['name'])

			print("Валюта: {}.".format(currency))

		return True


	def parse_okei(self, tree):
		'Парсит единицы измерения.'

		for element in tree.xpath('.//nsiOKEI'):

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

			# Получаем дополнительные объекты
			okei_section = OKEISection.objects.take(
				code  = o['section_code'],
				name  = o['section_name'],
				state = True)

			okei_group = OKEIGroup.objects.take(
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


	def parse_kosgu(self, tree):
		'Парсит классификатор операций сектора государственного управления.'

		for element in tree.xpath('.//nsiKOSGU'):

			o         = {}
			o['code'] = element.xpath('./code')[0].text
			o['name'] = element.xpath('./name')[0].text

			try:
				o['parent_code'] = element.xpath('./parentCode')[0].text
				if o['parent_code'] == '000':
					o['parent_code'] = None
			except IndexError:
				o['parent_code'] = None

			if element.xpath('./actual')[0].text == 'true':
				o['state'] = True
			else:
				o['state'] = False

			# Получаем дополнительные объекты
			if o['parent_code']:
				parent = KOSGU.objects.take(code = o['parent_code'])
			else:
				parent = None

			kosgu = KOSGU.objects.update(
				code   = o['code'],
				parent = parent,
				name   = o['name'],
				state  = o['state'])

			print("КОСГУ: {}.".format(kosgu))

		return True


	def parse_okopf(self, tree):
		'Парсит ОКОПФ.'

		for element in tree.xpath('.//nsiOKOPF'):

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

			# Получаем дополнительные объекты
			if o['parent_code']:
				parent = OKOPF.objects.take(code = o['parent_code'])
			else:
				parent = None

			okopf = OKOPF.objects.update(
				code          = o['code'],
				full_name     = o['full_name'],
				singular_name = o['singular_name'],
				parent        = parent,
				state         = o['state'])

			print("ОКОПФ: {}.".format(okopf))

		return True


	def parse_okpd(self, tree):
		'Парсит ОКПД.'

		for element in tree.xpath('.//nsiOKPD'):

			o         = {}
			o['id']   = element.xpath('./id')[0].text
			o['code'] = element.xpath('./code')[0].text
			o['name'] = element.xpath('./name')[0].text

			try:
				o['parent_id'] = element.xpath('./parentId')[0].text
			except IndexError:
				o['parent_id'] = None

			if element.xpath('./actual')[0].text == 'true':
				o['state'] = True
			else:
				o['state'] = False

			# Получаем дополнительные объекты
			if o['parent_id']:
				parent = OKPD.objects.take(id = o['parent_id'])
			else:
				parent = None

			okpd = OKPD.objects.update(
				id     = o['id'],
				parent = parent,
				code   = o['code'],
				name   = o['name'],
				state  = o['state'])

			print("Обновлён элемент ОКПД: {}.".format(okpd))

		return True


	def parse_okpd2(self, tree):
		'Парсит ОКПД2.'

		for element in tree.xpath('.//nsiOKPD2'):

			o         = {}
			o['id']   = element.xpath('./id')[0].text
			o['code'] = element.xpath('./code')[0].text
			o['name'] = element.xpath('./name')[0].text

			try:
				o['parent_id'] = element.xpath('./parentId')[0].text
			except IndexError:
				o['parent_id'] = None

			if element.xpath('./actual')[0].text == 'true':
				o['state'] = True
			else:
				o['state'] = False

			# Получаем дополнительные объекты
			if o['parent_id']:
				parent = OKPD2.objects.take(id = o['parent_id'])
			else:
				parent = None

			okpd2 = OKPD2.objects.update(
				id     = o['id'],
				parent = parent,
				code   = o['code'],
				name   = o['name'],
				state  = o['state'])

			print("Обновлён элемент ОКПД2: {}.".format(okpd2))

		return True



	def parse_oktmo(self, tree):
		'Парсит ОКТМО.'

		for element in tree.xpath('.//nsiOKTMO'):

			o         = {}
			o['code'] = element.xpath('./code')[0].text
			o['name'] = element.xpath('./fullName')[0].text

			try:
				o['parent_code'] = element.xpath('./parentCode')[0].text
			except IndexError:
				o['parent_code'] = None

			if element.xpath('./actual')[0].text == 'true':
				o['state'] = True
			else:
				o['state'] = False

			# Получаем дополнительные объекты
			if o['parent_code']:
				parent = OKTMO.objects.take(code = o['parent_code'])
			else:
				parent = None


			oktmo = OKTMO.objects.update(
				code   = o['code'],
				parent = parent,
				name   = o['name'],
				state  = o['state'])

			print("Обновлён элемент ОКТМО: {}.".format(oktmo))

		return True



	def parse_okved(self, tree):
		'Парсит ОКВЭД.'

		for element in tree.xpath('.//nsiOKVED'):

			o         = {}
			o['id']   = element.xpath('./id')[0].text
			o['code'] = element.xpath('./code')[0].text
			o['name'] = element.xpath('./name')[0].text

			try:
				o['section_name'] = element.xpath('./section')[0].text
			except IndexError:
				o['section_name'] = None

			try:
				o['subsection_name'] = element.xpath('./subsection')[0].text
			except IndexError:
				o['subsection_name'] = None

			try:
				o['parent_id'] = element.xpath('./parentId')[0].text
			except IndexError:
				o['parent_id'] = None

			if element.xpath('./actual')[0].text == 'true':
				o['state'] = True
			else:
				o['state'] = False

			# Получаем дополнительные объекты
			if o['section_name']:
				section = OKVEDSection.objects.take(name = o['section_name'])
			else:
				section = None

			if o['subsection_name']:
				subsection = OKVEDSubSection.objects.take(name = o['subsection_name'])
			else:
				subsection = None

			if o['parent_id']:
				parent = OKVED.objects.take(id = o['parent_id'])
			else:
				parent = None

			# Обновляем информацию в базе
			okved = OKVED.objects.update(
				id         = o['id'],
				code       = o['code'],
				section    = section,
				subsection = subsection,
				parent     = parent,
				name       = o['name'],
				state      = o['state'])

			print("Обновлён элемент ОКВЭД: {}.".format(okved))

		return True


	def parse_okved2(self, tree):
		'Парсит ОКВЭД2.'

		for element in tree.xpath('.//nsiOKVED2'):

			o            = {}
			o['id']      = element.xpath('./id')[0].text
			o['code']    = element.xpath('./code')[0].text
			o['name']    = element.xpath('./name')[0].text

			try:
				o['section_name'] = element.xpath('./section')[0].text
			except IndexError:
				o['section_name'] = None

			try:
				o['parent_code'] = element.xpath('./parentCode')[0].text
			except IndexError:
				o['parent_code'] = None

			try:
				o['comment'] = element.xpath('./comment')[0].text
			except IndexError:
				o['comment'] = None

			if element.xpath('./actual')[0].text == 'true':
				o['state'] = True
			else:
				o['state'] = False

			# Получаем дополнительные объекты
			if o['section_name']:
				section = OKVED2Section.objects.take(name = o['section_name'])
			else:
				section = None

			if o['parent_code']:
				parent = OKVED2.objects.take(code = o['parent_code'])
			else:
				parent = None

			# Обновляем информацию в базе
			okved = OKVED2.objects.update(
				code       = o['code'],
				oos_id     = o['id'],
				section    = section,
				parent     = parent,
				name       = o['name'],
				state      = o['state'])

			print("Обновлён элемент ОКВЭД2: {}.".format(okved))

		return True


	def parse_budget(self, tree):
		'Парсит бюджет.'

		for element in tree.xpath('.//nsiBudget'):

			o            = {}
			o['code']    = element.xpath('./code')[0].text
			o['name']    = element.xpath('./name')[0].text

			if element.xpath('./actual')[0].text == 'true':
				o['state'] = True
			else:
				o['state'] = False

			# Обновляем информацию в базе
			budget = Budget.objects.update(
				code       = o['code'],
				name       = o['name'],
				state      = o['state'])

			print("Обновлён элемент Бюджет: {}.".format(budget))

		return True


	def parse_budget_type(self, tree):
		'Парсит типы бюджета.'

		for element in tree.xpath('.//nsiOffBudget'):

			o                        = {}
			o['code']                = element.xpath('./code')[0].text
			o['name']                = element.xpath('./name')[0].text

			try:
				o['subsystem_type_code'] = element.xpath('./subsystemType')[0].text
			except IndexError:
				o['subsystem_type_code'] = None

			if element.xpath('./actual')[0].text == 'true':
				o['state'] = True
			else:
				o['state'] = False

			# Получаем дополнительные объекты
			if o['subsystem_type_code']:
				subsystem_type = SubsystemType.objects.take(code = o['subsystem_type_code'])
			else:
				subsystem_type = None

			# Обновляем информацию в базе
			budget_type = BudgetType.objects.update(
				code           = o['code'],
				name           = o['name'],
				subsystem_type = subsystem_type,
				state          = o['state'])

			print("Обновлён элемент Тип бюджета: {}.".format(budget_type))

		return True



	def parse_kbk_budget(self, tree):
		'Парсит код поступления бюджета.'

		for element in tree.xpath('.//nsiKBKBudget'):

			o               = {}
			o['code']       = element.xpath('./kbk')[0].text

			try:
				o['start_date'] = element.xpath('./start_date')[0].text
			except IndexError:
				o['start_date'] = None

			try:
				o['end_date'] = element.xpath('./end_date')[0].text
			except IndexError:
				o['end_date'] = None

			try:
				o['budget_code'] = element.xpath('./budget')[0].text
			except IndexError:
				o['budget_code'] = None

			if element.xpath('./actual')[0].text == 'true':
				o['state'] = True
			else:
				o['state'] = False

			# Получаем дополнительные объекты
			if o['budget_code']:
				budget = Budget.objects.take(code = o['budget_code'])
			else:
				budget = None

			# Обновляем информацию в базе
			kbk_budget = KBKBudget.objects.update(
				code       = o['code'],
				budget     = budget,
				state      = o['state'],
				start_date = o['start_date'],
				end_date   = o['end_date'])

			print("Обновлён элемент Код поступления бюджета: {}.".format(kbk_budget))

		return True


	def parse_organisation_type(self, tree):
		'Парсит типы организаций.'

		for element in tree.xpath('.//nsiOrganizationType'):

			o                = {}
			o['code']        = element.xpath('./code')[0].text
			o['name']        = element.xpath('./name')[0].text
			o['description'] = element.xpath('./description')[0].text

			# Обновляем информацию в базе
			organisation_type = OrganisationType.objects.update(
				code        = o['code'],
				name        = o['name'],
				description = o['description'])

			print(organisation_type)

		return True



	# TODO
	def parse_organisation(self, tree):
		'Парсит организации.'

		for element in tree.xpath('.//nsiOrganization'):

			o                    = {}

			o['reg_number']      = self.get_data_from_element(element, './regNumber')
			o['short_name']      = self.get_data_from_element(element, './shortName')
			o['full_name']       = self.get_data_from_element(element, './fullName')
			o['factual_address'] = self.get_data_from_element(element, './factualAddress/addressLine')
			o['postal_address']  = self.get_data_from_element(element, './postalAddress')
			o['inn']             = self.get_data_from_element(element, './INN')
			o['kpp']             = self.get_data_from_element(element, './KPP')
			o['ogrn']            = self.get_data_from_element(element, './OGRN')
			o['okpo']            = self.get_data_from_element(element, './OKPO')

			email = self.get_data_from_element(element, './email')
			if email:
				email = Email.objects.take(email = email)
			else:
				email = None

			phone = self.get_data_from_element(element, './phone')
			if phone:
				phone = Phone.objects.take(phone = phone)
			else:
				phone = None

			fax = self.get_data_from_element(element, './fax')
			if fax:
				fax = Phone.objects.take(phone = fax)
			else:
				fax = None

			contact_person = {}
			contact_person['first_name']  = self.get_data_from_element(element, './contactPerson/firstName')
			contact_person['middle_name'] = self.get_data_from_element(element, './contactPerson/middleName')
			contact_person['last_name']   = self.get_data_from_element(element, './contactPerson/lastName')
			if contact_person['first_name']:
				contact_person = Person.objects.take(
						first_name  = contact_person['first_name'],
						middle_name = contact_person['middle_name'],
						last_name   = contact_person['last_name'],
						emails      = [email],
						phones      = [phone],
						faxes       = [fax])
			else:
				contact_person = None

			head_agency = {}
			head_agency['reg_number'] = self.get_data_from_element(element, './headAgency/regNum')
			head_agency['full_name']  = self.get_data_from_element(element, './headAgency/fullName')
			if head_agency['reg_number']:
				head_agency = Organisation.objects.take(
						reg_number = head_agency['reg_number'],
						full_name  = head_agency['full_name'])
			else:
				head_agency = None

			ordering_agency = {}
			ordering_agency['reg_number'] = self.get_data_from_element(element, './orderingAgency/regNum')
			ordering_agency['full_name']  = self.get_data_from_element(element, './orderingAgency/fullName')
			if ordering_agency['reg_number']:
				ordering_agency = Organisation.objects.take(
						reg_number = ordering_agency['reg_number'],
						full_name  = ordering_agency['full_name'])
			else:
				ordering_agency = None

			okopf = {}
			okopf['code']      = self.get_data_from_element(element, './OKOPF/code')
			okopf['full_name'] = self.get_data_from_element(element, './OKOPF/fullName')
			if okopf['code']:
				okopf = OKOPF.objects.take(code = okopf['code'], full_name = okopf['full_name'])
			else:
				okopf = None

			okogu = {}
			okogu['code'] = self.get_data_from_element(element, './OKOGU/code')
			okogu['name'] = self.get_data_from_element(element, './OKOGU/name')
			if okogu['code']:
				okogu = OKOGU.objects.take(code = okogu['code'], name = okogu['name'])
			else:
				okogu = None

			organisation_role = self.get_data_from_element(element, './organizationRole')
			if organisation_role:
				organisation_role = OrganisationRole.objects.take(code = organisation_role)
			else:
				organisation_role = None

			organisation_type = {}
			organisation_type['code'] = self.get_data_from_element(element, './organizationType/code')
			organisation_type['name'] = self.get_data_from_element(element, './organizationType/name')
			if organisation_type['code']:
				organisation_type = OrganisationType.objects.take(
						code = organisation_type['code'],
						name = organisation_type['name'])
			else:
				organisation_type = None

			oktmo = self.get_data_from_element(element, './OKTMO/code')
			if oktmo:
				oktmo = OKTMO.objects.take(code = oktmo)
			else:
				oktmo = None

			# accounts
			accounts = []
			for e in element.xpath('./accounts/account'):

				bank = {}
				bank['bik']     = self.get_data_from_element(e, './bik')
				bank['name']    = self.get_data_from_element(e, './bankName')
				bank['address'] = self.get_data_from_element(e, './bankAddress')
				bank = Bank.objects.take(
					bik     = bank['bik'],
					name    = bank['name'],
					address = bank['address'])

				account = {}
				account['payment_account']  = self.get_data_from_element(e, './paymentAccount')
				account['corr_account']     = self.get_data_from_element(e, './corrAccount')
				account['personal_account'] = self.get_data_from_element(e, './personalAccount')
				account = Account.objects.take(
					payment_account  = account['payment_account'],
					corr_account     = account['corr_account'],
					personal_account = account['personal_account'],
					bank             = bank)

				accounts.append(account)

			# budgets
			budgets = []
			for e in element.xpath('./budgets/budget'):

				budget = {}
				budget['code'] = self.get_data_from_element(e, './code')
				budget['name'] = self.get_data_from_element(e, './name')
				budget = Budget.objects.take(
					code = budget['code'],
					name = budget['name'])

				budgets.append(budget)

			# okveds
			okveds = []
			for okved in self.get_data_from_element(element, './OKVED').split(';'):
				try:
					okved = OKVED.objects.get(code = okved)
					okveds.append(okved)
				except Exception:
					pass

			if self.get_data_from_element(element, './actual') == 'true':
				o['state'] = True
			else:
				o['state'] = False

			if self.get_data_from_element(element, './register') == 'true':
				o['register'] = True
			else:
				o['register'] = False

			# Обновляем информацию в базе
			organisation = Organisation.objects.update(
				reg_number        = o['reg_number'],
				short_name        = o['short_name'],
				full_name         = o['full_name'],
				factual_address   = o['factual_address'],
				postal_address    = o['postal_address'],
				inn               = o['inn'],
				kpp               = o['kpp'],
				ogrn              = o['ogrn'],
				okpo              = o['okpo'],

				email             = email,
				phone             = phone,
				fax               = fax,
				contact_person    = contact_person,
				head_agency       = head_agency,
				ordering_agency   = ordering_agency,
				okopf             = okopf,
				okogu             = okogu,
				organisation_role = organisation_role,
				organisation_type = organisation_type,
				oktmo             = oktmo,

				accounts          = accounts,
				budgets           = budgets,
				okveds            = okveds)

			print(organisation)

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






	def clear_tags(self, tree):

		# Чистим теги
		for element in tree.xpath('.//*'):
			element.tag = element.tag.split('}')[1]

		return tree



	def get_data_from_element(self, element, query):

		try:
			result = element.xpath(query)[0].text
		except Exception:
			result = ''

		return result
