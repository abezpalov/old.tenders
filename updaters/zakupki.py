import tenders.runner
from tenders.models import *


class Runner(tenders.runner.Runner):


	name  = 'Обновление с сайта государственных закупок России'
	alias = 'zakupki'

	black_list = ['_logs', 'fcs_undefined', 'auditresult', 'customerreports', 'regulationrules', 'requestquotation', 'dygeja_Resp']

	categories = {
		'essences' : 'fcs_nsi',
		'regions'  : 'fcs_regions'}

	subcategories = [
		None,
		'prevMonth',
		'currMonth']


	def __init__(self):

		super().__init__()

		self.url = 'ftp.zakupki.gov.ru'

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
			{'category' : 'nsiKVR',                            'parser' : self.parse_kvr},

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
#			{'category' : 'nsiModifyReasonOZ',                 'parser' : self.parse_},
#			{'category' : 'nsiPublicDiscussionDecisions',      'parser' : self.parse_},
#			{'category' : 'nsiPublicDiscussionQuestionnaries', 'parser' : self.parse_},
#			{'category' : 'nsiSingleCustomerReasonOZ',         'parser' : self.parse_},
#			{'category' : 'nsiSpecialPurchase',                'parser' : self.parse_},

#			{'category' : 'nsiOrganizationRights',             'parser' : self.parse_},
		]

		self.region_essences = [
			{'category' : 'plangraphs',    'parser' : self.parse_plan},
#			{'category' : 'notifications', 'parser' : self.parse_notification},
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

			if subcategory:
				catalog = "{}/{}/{}/{}".format(self.categories['regions'], region.alias, essence['category'], subcategory)
			else:
				catalog = "{}/{}/{}".format(self.categories['regions'], region.alias, essence['category'])	

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

			budget = Budget.objects.update(
				code       = self.get_text(element, './code'),
				name       = self.get_text(element, './name'),
				state      = self.get_bool(element, './actual'))

			print("Бюджет: {}.".format(budget))

		return True


	def parse_budget_type(self, tree):
		'Парсит типы бюджета.'

		for element in tree.xpath('.//nsiOffBudget'):

			subsystem_type = SubsystemType.objects.take(code = self.get_text(element, './subsystemType'))

			budget_type = BudgetType.objects.update(
				code           = self.get_text(element, './code'),
				name           = self.get_text(element, './name'),
				subsystem_type = subsystem_type,
				state          = self.get_bool(element, './actual'))

			print("Тип бюджета: {}.".format(budget_type))

		return True



	def parse_kbk_budget(self, tree):
		'Парсит код поступления бюджета.'

		for element in tree.xpath('.//nsiKBKBudget'):

			budget = Budget.objects.take(code = self.get_text(element, './budget'))

			kbk_budget = KBKBudget.objects.update(
				code       = self.get_text(element, './kbk'),
				budget     = budget,
				state      = self.get_bool(element, './actual'),
				start_date = self.get_datetime(element, './start_date'),
				end_date   = self.get_datetime(element, './end_date'))

			print("Код поступления бюджета: {}.".format(kbk_budget))

		return True


	def parse_organisation_type(self, tree):
		'Парсит типы организаций.'

		for element in tree.xpath('.//nsiOrganizationType'):

			organisation_type = OrganisationType.objects.update(
				code        = self.get_text(element, './code'),
				name        = self.get_text(element, './name'),
				description = self.get_text(element, './description'))

			print("Тип организации: {}".format(organisation_type))

		return True



	def parse_organisation(self, tree):
		'Парсит организации.'

		for element in tree.xpath('.//nsiOrganization'):

			factual_address = Address.objects.take(address = self.get_text(element, './factualAddress/addressLine'))
			postal_address  = Address.objects.take(address = self.get_text(element, './postalAddress'))

			email = Email.objects.take(email = self.get_text(element, './email'))
			phone = Phone.objects.take(phone = self.get_text(element, './phone'))
			fax   = Phone.objects.take(phone = self.get_text(element, './fax'))

			contact_person = Person.objects.take(
				first_name  = self.get_text(element, './contactPerson/firstName'),
				middle_name = self.get_text(element, './contactPerson/middleName'),
				last_name   = self.get_text(element, './contactPerson/lastName'),
				emails      = [email],
				phones      = [phone],
				faxes       = [fax])

			head_agency = Organisation.objects.take(
				reg_number = self.get_text(element, './headAgency/regNum'),
				full_name  = self.get_text(element, './headAgency/fullName'))

			ordering_agency = Organisation.objects.take(
				reg_number = self.get_text(element, './orderingAgency/regNum'),
				full_name  = self.get_text(element, './orderingAgency/fullName'))

			okopf = OKOPF.objects.take(
				code      = self.get_text(element, './OKOPF/code'),
				full_name = self.get_text(element, './OKOPF/fullName'))

			okogu = OKOGU.objects.take(
				code = self.get_text(element, './OKOGU/code'),
				name = self.get_text(element, './OKOGU/name'))

			organisation_role = OrganisationRole.objects.take(
				code = self.get_text(element, './organizationRole'))

			organisation_type = OrganisationType.objects.take(
				code = self.get_text(element, './organizationType/code'),
				name = self.get_text(element, './organizationType/name'))

			oktmo = OKTMO.objects.take(
				code = self.get_text(element, './OKTMO/code'))

			organisation = Organisation.objects.update(
				reg_number        = self.get_text(element, './regNumber'),
				short_name        = self.get_text(element, './shortName'),
				full_name         = self.get_text(element, './fullName'),
				inn               = self.get_text(element, './INN'),
				kpp               = self.get_text(element, './KPP'),
				ogrn              = self.get_text(element, './OGRN'),
				okpo              = self.get_text(element, './OKPO'),
				factual_address   = factual_address,
				postal_address    = postal_address,
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
				state             = self.get_bool(element, './actual'),
				register          = self.get_bool(element, './register'))

			if organisation:

				organisation.accounts.clear()
				for e in element.xpath('./accounts/account'):

					address = Address.objects.take(
						address = self.get_text(e, './bankAddress'))

					bank = Bank.objects.take(
						bik     = self.get_text(e, './bik'),
						name    = self.get_text(e, './bankName'),
						address = address)

					account = Account.objects.take(
						payment_account  = self.get_text(e, './paymentAccount'),
						corr_account     = self.get_text(e, './corrAccount'),
						personal_account = self.get_text(e, './personalAccount'),
						bank             = bank)

					link = OrganisationToAccount()
					link.organisation = organisation
					link.account      = account
					link.save()

				organisation.budgets.clear()
				for e in element.xpath('./budgets/budget'):

					budget = Budget.objects.take(
						code = self.get_text(e, './code'),
						name = self.get_text(e, './name'))

					link = OrganisationToBudget()
					link.organisation = organisation
					link.budget       = budget
					link.save()

				organisation.okveds.clear()
				for okved in self.get_text(element, './OKVED').split(';'):
					try:
						okved = OKVED.objects.get(code = okved)
						link  = OrganisationToOKVED()
						link.organisation = organisation
						link.okved        = okved
						link.save()
					except Exception:
						pass

			print('Организация: {}'.format(organisation))

		return True


	def parse_placing_way(self, tree):

		for element in tree.xpath('.//nsiPlacingWay'):

			subsystem_type = SubsystemType.objects.take(
				code = self.get_text(element, './subsystemType'))

			placing_way = PlacingWay.objects.update(
				id             = self.get_text(element, './placingWayId'),
				code           = self.get_text(element, './code'),
				name           = self.get_text(element, './name'),
				type_code      = self.get_text(element, './type'),
				subsystem_type = subsystem_type,
				state          = self.get_bool(element, './actual'))

			print(placing_way)

		return True


	def parse_plan_position_change_reason(self, tree):

		for element in tree.xpath('.//nsiPlanPositionChangeReason'):

			o = PlanPositionChangeReason.objects.update(
					id          = self.get_text(element, './id'),
					name        = self.get_text(element, './name'),
					description = self.get_text(element, './description'),
					state       = self.get_bool(element, './actual'))

			print(o)

		return True


	def parse_kvr(self, tree):

		for element in tree.xpath('.//nsiKVR'):

			o = KVR.objects.update(
				code        = self.get_text(element, './code'),
				name        = self.get_text(element, './name'),
				state       = self.get_bool(element, './actual'))

			print(o)

		return True


	def parse_contract_modification_reason(self, tree):

		for element in tree.xpath('.//nsiContractModificationReason/nsiContractModificationReason'):

			o = ContractModificationReason.objects.update(
				code  = self.get_text(element, './code'),
				name  = self.get_text(element, './name'),
				state = self.get_bool(element, './actual'))

			print(o)

		return True


	def parse_plan(self, tree, region):
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

			email = Email.objects.take(email = self.get_text(element, './responsibleContactInfo/email'))
			phone = Phone.objects.take(phone = self.get_text(element, './responsibleContactInfo/phone'))
			fax   = Phone.objects.take(phone = self.get_text(element, './responsibleContactInfo/fax'))

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
				position['max_price']       = self.get_float(pos, './commonInfo/contractMaxPrice')

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

				# TODO kvrs
#				<amountKVRsYears>
#					<KVR>
#						<code>244</code>
#						<yearsList>
#							<year>2016</year>
#							<yearAmount>458226.20</yearAmount>
#						</yearsList>
#						<yearsList>
#							<year>2017</year>
#							<yearAmount>537438.50</yearAmount>
#						</yearsList>
#				for k in pos.xpath('.//amountKVRsYears/KVR'):

				okveds = []
				for okv in pos.xpath('.//OKVEDs/OKVED'):
					try:
						okved = OKVED.objects.get(code = self.get_text(okv, './code'))
						okveds.append(okved)
					except Exception:
						pass

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
					okveds          = okveds,
					okveds2         = okveds2)

				position.products.clear()

				for prod in pos.xpath('.//products/product'):

					try:
						okpd = OKPD.objects.get(code = self.get_text(prod, './OKPD/code'))
					except Exception:
						okpd = None

					try:
						okpd2 = OKPD2.objects.get(code = self.get_text(prod, './OKPD2/code'))
					except Exception:
						okpd2 = None

					product = Product.objects.take(okpd = okpd, okpd2 = okpd2, name = self.get_text(prod, './name'))

					try:
						okei = OKEI.objects.get(code = self.get_text(prod, './OKEI/code'))
					except Exception:
						okei = None

					e = PlanPositionToProduct()
					e.plan_position = position
					e.product       = product
					e.requirement   = self.get_text(prod, './minRequirement')
					e.quantity      = self.get_float(prod, './quantity')
					e.price         = self.get_float(prod, './price')
					e.total         = self.get_float(prod, './sumMax')
					e.okei          = okei
					e.save()


	def parse_plan_cancel(self, element, region):

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


	def parse_plan_unstructured(self, element, region):

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

		email = Email.objects.take(email = self.get_text(element, './responsibleContactInfo/email'))
		phone = Phone.objects.take(phone = self.get_text(element, './responsibleContactInfo/phone'))
		fax   = Phone.objects.take(phone = self.get_text(element, './responsibleContactInfo/fax'))

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


	# TODO
	def parse_notification(self, tree, region):
		'Парсит извещения.'

		# TODO KILL
		import xml.etree.ElementTree as ET
#		print(ET.tostring(element, encoding = 'unicode'))
		ok = False

		for element in tree.xpath('.//fcsNotificationZK'):
			self.parse_notification_get_universal(element, region)
			ok = True

		for element in tree.xpath('.//fcsNotificationEP'):
			self.parse_notification_get_universal(element, region)
			ok = True

		for element in tree.xpath('.//fcsNotificationEF'):
			self.parse_notification_get_universal(element, region)
			ok = True

		for element in tree.xpath('.//fcsNotificationOK'):
			self.parse_notification_get_universal(element, region)
			ok = True

		for element in tree.xpath('.//fcsNotificationZP'):
			self.parse_notification_get_universal(element, region)
			ok = True

		for element in tree.xpath('.//fcsNotificationOKOU'):
			self.parse_notification_get_universal(element, region)
			ok = True

		for element in tree.xpath('.//fcsNotificationCancel'):
			self.parse_notification_cancel(element, region)
			ok = True

		if not ok:
			print(ET.tostring(tree.getroot(), encoding = 'unicode'))
			exit()


	def parse_notification_cancel(self, element, region):

		purchase = Purchase.objects.take(number = self.get_text(element, './purchaseNumber'))

		notification = Notification.objects.take(
			id       = self.get_int(element, './id'),
			url      = self.get_text(element, './printForm/url'),
			purchase = purchase)

		purchase.cancel()


	def parse_notification_get_universal(self, element, region):

		responsible = Organisation.objects.take(reg_number = self.get_text(element, './purchaseResponsible/responsibleOrg/regNum'))
		specialised = Organisation.objects.take(reg_number = self.get_text(element, './purchaseResponsible/specializedOrg/regNum'))

		# TODO TEST
		import xml.etree.ElementTree as ET
		if not responsible:
			print(ET.tostring(element, encoding = 'unicode'))
			print('Ответственного нет!!!')

		email = Email.objects.take(email = self.get_text(element, './purchaseResponsible/responsibleInfo/contactEMail'))
		phone = Phone.objects.take(phone = self.get_text(element, './purchaseResponsible/responsibleInfo/contactPhone'))

		contact_person = Person.objects.take(
			first_name  = self.get_text(element, './purchaseResponsible/responsibleInfo/contactPerson/firstName'),
			middle_name = self.get_text(element, './purchaseResponsible/responsibleInfo/contactPerson/middleName'),
			last_name   = self.get_text(element, './purchaseResponsible/responsibleInfo/contactPerson/lastName'),
			emails      = [email],
			phones      = [phone])

		try:
			placing_way = PlacingWay.objects.get(
				code = self.get_text(element, './placingWay/code'),
				state = True)
		except Exception:
			placing_way = None

		grant_place            = Address.objects.take(address = self.get_text(element, './purchaseDocumentation/grantPlace'))
		collecting_place       = Address.objects.take(address = self.get_text(element, './procedureInfo/collecting/place'))
		opening_place          = Address.objects.take(address = self.get_text(element, './procedureInfo/opening/place'))
		prequalification_place = Address.objects.take(address = self.get_text(element, './procedureInfo/prequalification/place'))
		scoring_place          = Address.objects.take(address = self.get_text(element, './procedureInfo/scoring/place'))

		etp = ETP.objects.take(
			code = self.get_text(element, './ETP/code'),
			name = self.get_text(element, './ETP/name'),
			url  = self.get_text(element, './ETP/url'))

		purchase = Purchase.objects.update(
			number                 = self.get_text(element, './purchaseNumber'),
			name                   = self.get_text(element, './purchaseObjectInfo'),
			url                    = self.get_text(element, './href'),
			published              = self.get_datetime(element, './docPublishDate'),
			region                 = region,
			responsible            = responsible,
			specialised            = specialised,
			contact_person         = contact_person,
			placing_way            = placing_way,
			grant_start_time       = self.get_datetime(element, './purchaseDocumentation/grantStartDate'),
			grant_end_time         = self.get_datetime(element, './purchaseDocumentation/grantEndDate'),
			collecting_start_time  = self.get_datetime(element, './procedureInfo/collecting/startDate'),
			collecting_end_time    = self.get_datetime(element, './procedureInfo/collecting/endDate'),
			opening_time           = self.get_datetime(element, './procedureInfo/opening/date'),
			prequalification_time  = self.get_datetime(element, './procedureInfo/prequalification/date'),
			scoring_time           = self.get_datetime(element, './procedureInfo/scoring/date'),
			grant_place            = grant_place,
			collecting_place       = collecting_place,
			opening_place          = opening_place,
			prequalification_place = prequalification_place,
			scoring_place          = scoring_place,
			etp                    = etp)
		print(purchase)

		notification = Notification.objects.take(
			id       = self.get_int(element, './id'),
			url      = self.get_text(element, './printForm/url'),
			purchase = purchase)

		purchase.attachments.clear()
		for a in element.xpath('.//attachments/attachment'):

			attachment = Attachment.objects.take(
				url         = self.get_text(a, './url'),
				name        = self.get_text(a, './fileName'),
				size        = self.get_text(a, './fileSize'),
				description = self.get_text(a, './docDescription'))

			link = PurchaseToAttachment()
			link.purchase   = purchase
			link.attachment = attachment
			link.save()


		for n, l in enumerate(element.xpath('.//lot')):

			currency = Currency.objects.take(code = self.get_text(l, './currency/code'))

			# TODO ??
			#plan_number     = self.get_text(l, './customerRequirements/tenderPlanInfo/planNumber')
			#position_number = self.get_text(l, './customerRequirements/tenderPlanInfo/positionNumber')
			if self.get_int(l, './lotNumber'):
				number = self.get_int(l, './lotNumber')
			else:
				number = n

			lot = Lot.objects.update(
				purchase       = purchase,
				number         = number,
				name           = self.get_text(l, './lotObjectInfo'),
				finance_source = self.get_text(l, './financeSource'),
				max_price      = self.get_float(l, './maxPrice'))

			if lot:

				lot.products.clear()
				for p in l.xpath('./purchaseObjects/purchaseObject'):

					try:
						okpd = OKPD.objects.get(code = self.get_text(p, './OKPD/code'))
					except Exception:
						okpd = None

					try:
						okpd2 = OKPD2.objects.get(code = self.get_text(p, './OKPD2/code'))
					except Exception:
						okpd2 = None

					product = Product.objects.take(
						okpd  = okpd,
						okpd2 = okpd2,
						name  = self.get_text(p, './name'))

					okei = OKEI.objects.take(
						code = self.get_text(p, './OKEI/code'))

					link = LotToProduct()
					link.lot      = lot
					link.product  = product
					link.quantity = self.get_float(p, './quantity')
					link.okei     = okei
					link.price    = self.get_float(p, './price')
					link.total    = self.get_float(p, './sum')
					link.currency = currency
					link.save()

				lot.customers.clear()
				for c in l.xpath('./customerRequirements/customerRequirement/customer'):

					customer = Organisation.objects.take(
						reg_number = self.get_text(c, './regNum'))

					link = LotToCustomer()
					link.lot      = lot
					link.customer = customer
					link.save()



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

	def get_bool(self, element, query):

		try:
			if element.xpath(query)[0].text == 'true':
				result = True
			else:
				result = False
		except Exception:
			result = False

		return result


	def get_datetime(self, element, query):

		try:
			result = element.xpath(query)[0].text.strip()
		except Exception:
			result = None

		return result


	def get_int(self, element, query):

		try:
			result = int(element.xpath(query)[0].text.strip())
		except Exception:
			result = None

		return result


	def get_float(self, element, query):

		try:
			result = float(element.xpath(query)[0].text.strip())
		except Exception:
			result = None

		return result
