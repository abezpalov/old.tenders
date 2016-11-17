#import gc
import tenders.runner
from tenders.models import *


class Runner(tenders.runner.Runner):


	name  = 'Обновление с сайта государственных закупок России'
	alias = 'zakupki-gov-ru'

	black_list = ['_logs', 'fcs_undefined', 'auditresult', 'customerreports', 'regulationrules', 'requestquotation']


	def __init__(self):

		super().__init__()

		self.url = 'ftp.zakupki.gov.ru'

		self.categories = {
			'essences'                    : 'fcs_nsi',
			'regions'                     : 'fcs_regions',
		}

		self.subcategories = [
			'prevMonth',
			'currMonth'
		]

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
			{'category' : 'nsiPlacingWay',                     'parser' : self.parse_placing_way},
			{'category' : 'nsiPlanPositionChangeReason',       'parser' : self.parse_plan_position_change_reason},
			{'category' : 'nsiContractModificationReason',     'parser' : self.parse_contract_modification_reason},

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

		self.region_essences = [
			{'category' : 'plangraphs',       'parser' : self.parse_tenderplan},

		]

	def run(self):

		# Обновляем справочники
		for essence in self.essences:

			# Проверяем не вышло ли время
			if self.is_time_up():
				return True

			self.update_essence(essence)

		# Обновляем данные с регионов
		for region in self.get_ftp_catalog(self.url, self.categories['regions']):

			if (not region in self.black_list) and (not '.'in region):
				try:
					self.get_ftp_catalog(self.url, '{}/{}'.format(self.categories['regions'], region))
					region = Region.objects.take(
						alias = region,
						name = region,
						full_name = region)
					print(region)
	
				except Exception:
					continue

				if region.state:

					for essence in self.region_essences:
						self.update_region_essence(region, essence)



		print("Завершил за {}.".format(timezone.now() - self.start_time))
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

			source.complite()

		return True


	def update_region_essence(self, region, essence):
		'Получает файлы сущностей для анализа и обработки'

		for subcategory in self.subcategories:

			catalog = "{}/{}/{}/{}".format(self.categories['regions'], region.alias, essence['category'], subcategory)

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
					parse(tree, region)

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

			print("ОКПД: {}.".format(okpd))

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

			print("ОКПД2: {}.".format(okpd2))

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

			print("ОКТМО: {}.".format(oktmo))

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

			print("ОКВЭД: {}.".format(okved))

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

			print("ОКВЭД2: {}.".format(okved))

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

			print("Бюджет: {}.".format(budget))

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

			print("Тип бюджета: {}.".format(budget_type))

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

			print("Код поступления бюджета: {}.".format(kbk_budget))

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

			print("Тип организации: {}".format(organisation_type))

		return True



	def parse_organisation(self, tree):
		'Парсит организации.'

		for element in tree.xpath('.//nsiOrganization'):

			o = {}

			o['reg_number']      = self.get_text(element, './regNumber')
			o['short_name']      = self.get_text(element, './shortName')
			o['full_name']       = self.get_text(element, './fullName')
			o['factual_address'] = self.get_text(element, './factualAddress/addressLine')
			o['postal_address']  = self.get_text(element, './postalAddress')
			o['inn']             = self.get_text(element, './INN')
			o['kpp']             = self.get_text(element, './KPP')
			o['ogrn']            = self.get_text(element, './OGRN')
			o['okpo']            = self.get_text(element, './OKPO')

			email = self.get_text(element, './email')
			if email:
				email = Email.objects.take(email = email)
			else:
				email = None

			phone = self.get_text(element, './phone')
			if phone:
				phone = Phone.objects.take(phone = phone)
			else:
				phone = None

			fax = self.get_text(element, './fax')
			if fax:
				fax = Phone.objects.take(phone = fax)
			else:
				fax = None

			contact_person = {}
			contact_person['first_name']  = self.get_text(element, './contactPerson/firstName')
			contact_person['middle_name'] = self.get_text(element, './contactPerson/middleName')
			contact_person['last_name']   = self.get_text(element, './contactPerson/lastName')
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
			head_agency['reg_number'] = self.get_text(element, './headAgency/regNum')
			head_agency['full_name']  = self.get_text(element, './headAgency/fullName')
			if head_agency['reg_number']:
				head_agency = Organisation.objects.take(
						reg_number = head_agency['reg_number'],
						full_name  = head_agency['full_name'])
			else:
				head_agency = None

			ordering_agency = {}
			ordering_agency['reg_number'] = self.get_text(element, './orderingAgency/regNum')
			ordering_agency['full_name']  = self.get_text(element, './orderingAgency/fullName')
			if ordering_agency['reg_number']:
				ordering_agency = Organisation.objects.take(
						reg_number = ordering_agency['reg_number'],
						full_name  = ordering_agency['full_name'])
			else:
				ordering_agency = None

			okopf = {}
			okopf['code']      = self.get_text(element, './OKOPF/code')
			okopf['full_name'] = self.get_text(element, './OKOPF/fullName')
			if okopf['code']:
				okopf = OKOPF.objects.take(code = okopf['code'], full_name = okopf['full_name'])
			else:
				okopf = None

			okogu = {}
			okogu['code'] = self.get_text(element, './OKOGU/code')
			okogu['name'] = self.get_text(element, './OKOGU/name')
			if okogu['code']:
				okogu = OKOGU.objects.take(code = okogu['code'], name = okogu['name'])
			else:
				okogu = None

			organisation_role = self.get_text(element, './organizationRole')
			if organisation_role:
				organisation_role = OrganisationRole.objects.take(code = organisation_role)
			else:
				organisation_role = None

			organisation_type = {}
			organisation_type['code'] = self.get_text(element, './organizationType/code')
			organisation_type['name'] = self.get_text(element, './organizationType/name')
			if organisation_type['code']:
				organisation_type = OrganisationType.objects.take(
						code = organisation_type['code'],
						name = organisation_type['name'])
			else:
				organisation_type = None

			oktmo = self.get_text(element, './OKTMO/code')
			if oktmo:
				oktmo = OKTMO.objects.take(code = oktmo)
			else:
				oktmo = None

			accounts = []
			for e in element.xpath('./accounts/account'):

				bank = {}
				bank['bik']     = self.get_text(e, './bik')
				bank['name']    = self.get_text(e, './bankName')
				bank['address'] = self.get_text(e, './bankAddress')
				bank = Bank.objects.take(
					bik     = bank['bik'],
					name    = bank['name'],
					address = bank['address'])

				account = {}
				account['payment_account']  = self.get_text(e, './paymentAccount')
				account['corr_account']     = self.get_text(e, './corrAccount')
				account['personal_account'] = self.get_text(e, './personalAccount')
				account = Account.objects.take(
					payment_account  = account['payment_account'],
					corr_account     = account['corr_account'],
					personal_account = account['personal_account'],
					bank             = bank)

				accounts.append(account)

			budgets = []
			for e in element.xpath('./budgets/budget'):

				budget = {}
				budget['code'] = self.get_text(e, './code')
				budget['name'] = self.get_text(e, './name')
				budget = Budget.objects.take(
					code = budget['code'],
					name = budget['name'])

				budgets.append(budget)

			okveds = []
			for okved in self.get_text(element, './OKVED').split(';'):
				try:
					okved = OKVED.objects.get(code = okved)
					okveds.append(okved)
				except Exception:
					pass

			if self.get_text(element, './actual') == 'true':
				o['state'] = True
			else:
				o['state'] = False

			if self.get_text(element, './register') == 'true':
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

			print('Организация: {}'.format(organisation))

		return True


	def parse_placing_way(self, tree):

		for element in tree.xpath('.//nsiPlacingWay'):

			o = {}

			o['id']        = self.get_text(element, './placingWayId')
			o['code']      = self.get_text(element, './code')
			o['name']      = self.get_text(element, './name')
			o['type_code'] = self.get_text(element, './type')

			o['subsystem_type'] = self.get_text(element, './subsystemType')
			if o['subsystem_type']:
				subsystem_type = SubsystemType.objects.take(
						code = o['subsystem_type'])
			else:
				subsystem_type = None

			if self.get_text(element, './actual') == 'true':
				o['state'] = True
			else:
				o['state'] = False

			# Обновляем информацию в базе
			placing_way = PlacingWay.objects.update(
				id             = o['id'],
				code           = o['code'],
				name           = o['name'],
				type_code      = o['type_code'],
				subsystem_type = subsystem_type,
				state          = o['state'])

			print(placing_way)

		return True


	def parse_plan_position_change_reason(self, tree):

		for element in tree.xpath('.//nsiPlanPositionChangeReason'):

			o = {}

			o['id']          = self.get_text(element, './id')
			o['name']        = self.get_text(element, './name')
			o['description'] = self.get_text(element, './description')

			if self.get_text(element, './actual') == 'true':
				o['state'] = True
			else:
				o['state'] = False

			# Обновляем информацию в базе
			o = PlanPositionChangeReason.objects.update(
					id          = o['id'],
					name        = o['name'],
					description = o['description'],
					state       = o['state'])

			print(o)

		return True


	def parse_contract_modification_reason(self, tree):

		for element in tree.xpath('.//nsiContractModificationReason/nsiContractModificationReason'):

			o = {}

			o['code'] = self.get_text(element, './code')
			o['name'] = self.get_text(element, './name')

			if self.get_text(element, './actual') == 'true':
				o['state'] = True
			else:
				o['state'] = False

			# Обновляем информацию в базе
			o = ContractModificationReason.objects.update(
					code        = o['code'],
					name        = o['name'],
					state       = o['state'])

			print(o)

		return True


	def parse_tenderplan(self, tree, region):
		'Парсит планы-графики.'

		# TODO KILL
		import xml.etree.ElementTree as ET

		for element in tree.xpath('.//tenderPlanCancel'):
			self.parse_tenderplan_cancel(element, region)

		for element in tree.xpath('.//tenderPlanUnstructured'):
			self.parse_tenderplan_unstructured(element, region)

		for element in tree.xpath('.//tenderPlan'):

			plan = {}
			plan['id']          = self.get_text(element, './commonInfo/id')
			plan['number']      = self.get_text(element, './commonInfo/planNumber')
			plan['year']        = self.get_text(element, './commonInfo/year')
			plan['version']     = self.get_text(element, './commonInfo/versionNumber')
			plan['description'] = self.get_text(element, './commonInfo/description')
			plan['created']     = self.get_text(element, './commonInfo/createDate')
			plan['confirmed']   = self.get_text(element, './commonInfo/confirmDate')
			plan['published']   = self.get_text(element, './commonInfo/publishDate')
			plan['url']         = self.get_text(element, './printForm/url')

			try:
				owner = Organisation.objects.get(
					reg_number = self.get_text(element, './commonInfo/owner/regNum'))
			except Exception:
				owner = None

			try:
				customer = Organisation.objects.get(
					reg_number = self.get_text(element, './customerInfo/customer/regNum'))
			except Exception:
				customer = None

			try:
				email = Email.objects.take(email = self.get_text(element, './responsibleContactInfo/email'))
			except Exception:
				email = None

			try:
				phone = Phone.objects.take(phone = self.get_text(element, './responsibleContactInfo/phone'))
			except Exception:
				phone = None

			try:
				fax = Phone.objects.take(phone = self.get_text(element, './responsibleContactInfo/fax'))
			except Exception:
				fax = None

			contact_person = Person.objects.take(
				first_name  = self.get_text(element, './responsibleContactInfo/firstName'),
				middle_name = self.get_text(element, './responsibleContactInfo/middleName'),
				last_name   = self.get_text(element, './responsibleContactInfo/lastName'),
				emails      = [email],
				phones      = [phone],
				faxes       = [fax])

			plan = Plan.objects.update(
					id             = plan['id'],
					number         = plan['number'],
					year           = plan['year'],
					version        = plan['version'],
					description    = plan['description'],
					url            = plan['url'],
					created        = plan['created'],
					confirmed      = plan['confirmed'],
					published      = plan['published'],
					region         = region,
					owner          = owner,
					customer       = customer,
					contact_person = contact_person)
			print(plan)

			positions = []
			for pos in element.xpath('.//positions/position'):

				position = {}
				position['number']          = self.get_text(pos, './commonInfo/positionNumber')
				position['name']            = self.get_text(pos, './commonInfo/contractSubjectName')
				position['purchase_month']  = self.get_int(pos, './purchaseConditions/purchaseGraph/purchasePlacingTerm/month')
				position['purchase_year']   = self.get_int(pos, './purchaseConditions/purchaseGraph/purchasePlacingTerm/year')
				position['execution_month'] = self.get_int(pos, './purchaseConditions/purchaseGraph/contractExecutionTerm/month')
				position['execution_year']  = self.get_int(pos, './purchaseConditions/purchaseGraph/contractExecutionTerm/year')
				position['max_price']       = self.get_text(pos, './commonInfo/contractMaxPrice')

				try:
					currency = Currency.objects.get(code = self.get_text(pos, './commonInfo/contractCurrency/code'))
				except Exception:
					currency = None

				try:
					placing_way = PlacingWay.objects.get(
						code = self.get_text(pos, './commonInfo/placingWay/code'))
				except Exception:
					placing_way = None

				try:
					change_reason = PlanPositionChangeReasonManager.objects.get(
						id = self.get_text(pos, './commonInfo/positionModification/changeReason/id'))
				except Exception:
					change_reason = None

				okveds2 = []
				for okv2 in pos.xpath('.//OKVEDs/OKVED2'):
					try:
						okved2 = OKVED2.objects.get(code = self.get_text(okv2, './code'))
						okveds2.append(okved2)
					except Exception:
						pass

				position = PlanPosition.objects.update(
					plan            = plan,
					number          = position['number'],
					name            = position['name'],
					purchase_month  = position['purchase_month'],
					purchase_year   = position['purchase_year'],
					execution_month = position['execution_month'],
					execution_year  = position['execution_year'],
					max_price       = position['max_price'],
					currency        = currency,
					placing_way     = placing_way,
					change_reason   = change_reason,
					okveds2         = okveds2)

				print('\t{}'.format(position))

				position.products.clear()

				for prod in pos.xpath('.//products/product'):

					try:
						okpd2 = OKPD2.objects.get(code = self.get_text(prod, './OKPD2/code'))
					except Exception:
						okpd2 = None

					product = Product.objects.take(okpd2 = okpd2, name = self.get_text(prod, './name'))

					try:
						okei = OKPD2.objects.get(code = self.get_text(prod, './OKEI/code'))
					except Exception:
						okei = None

					e = PlanPositionToProduct()
					e.plan_position = position
					e.product       = product
					e.requirement   = self.get_text(prod, './minRequirement')
					e.quantity      = self.get_text(prod, './quantity')
					e.price         = self.get_text(prod, './price')
					e.total         = self.get_text(prod, './sumMax')
					e.okei          = okei
					e.save()

					print('\t\t{}'.format(e))


	def parse_tenderplan_cancel(self, element, region):

		plan = {}
		plan['id']          = self.get_text(element, './id')
		plan['number']      = self.get_text(element, './planNumber')
		plan['year']        = self.get_text(element, './year')
		plan['version']     = self.get_text(element, './versionNumber')
		plan['description'] = self.get_text(element, './description')
		plan['created']     = self.get_text(element, './cancelDate')
		plan['url']         = self.get_text(element, './printForm/url')

		try:
			customer = Organisation.objects.get(
				reg_number = self.get_text(element, './customerInfo/regNum'))
		except Exception:
			customer = None

		plan = Plan.objects.update(
				id             = plan['id'],
				number         = plan['number'],
				year           = plan['year'],
				version        = plan['version'],
				description    = plan['description'],
				url            = plan['url'],
				created        = plan['created'],
				region         = region,
				customer       = customer,
				state          = False)

		Plan.objects.filter(number = plan.number).update(state = False)
		print('Отменён: {}.'.format(plan.number))


	def parse_tenderplan_unstructured(self, element, region):

		plan = {}
		plan['id']          = self.get_text(element, './commonInfo/id')
		plan['number']      = self.get_text(element, './commonInfo/planNumber')
		plan['year']        = self.get_text(element, './commonInfo/year')
		plan['version']     = self.get_text(element, './commonInfo/versionNumber')
		plan['description'] = self.get_text(element, './commonInfo/description')
		plan['created']     = self.get_text(element, './commonInfo/createDate')
		plan['confirmed']   = self.get_text(element, './commonInfo/confirmDate')
		plan['published']   = self.get_text(element, './commonInfo/publishDate')
		plan['url']         = self.get_text(element, './printForm/url')

		try:
			owner = Organisation.objects.get(
				reg_number = self.get_text(element, './commonInfo/owner/regNum'))
		except Exception:
			owner = None

		try:
			customer = Organisation.objects.get(
				reg_number = self.get_text(element, './customerInfo/customer/regNum'))
		except Exception:
			customer = None

		try:
			email = Email.objects.take(email = self.get_text(element, './responsibleContactInfo/email'))
		except Exception:
			email = None

		try:
			phone = Phone.objects.take(phone = self.get_text(element, './responsibleContactInfo/phone'))
		except Exception:
			phone = None

		try:
			fax = Phone.objects.take(phone = self.get_text(element, './responsibleContactInfo/fax'))
		except Exception:
			fax = None

		contact_person = Person.objects.take(
			first_name  = self.get_text(element, './responsibleContactInfo/firstName'),
			middle_name = self.get_text(element, './responsibleContactInfo/middleName'),
			last_name   = self.get_text(element, './responsibleContactInfo/lastName'),
			emails      = [email],
			phones      = [phone],
			faxes       = [fax])

		plan = Plan.objects.update(
			id             = plan['id'],
			number         = plan['number'],
			year           = plan['year'],
			version        = plan['version'],
			description    = plan['description'],
			url            = plan['url'],
			created        = plan['created'],
			confirmed      = plan['confirmed'],
			published      = plan['published'],
			region         = region,
			owner          = owner,
			customer       = customer,
			contact_person = contact_person)

		print(plan)



	def clear_tags(self, tree):

		# Чистим теги
		for element in tree.xpath('.//*'):
			element.tag = element.tag.split('}')[1]

		return tree



	def get_text(self, element, query):

		try:
			result = element.xpath(query)[0].text.strip()
		except Exception:
			result = ''

		return result


	def get_int(self, element, query):

		try:
			result = int(element.xpath(query)[0].text.strip())
		except Exception:
			result = None

		return result
