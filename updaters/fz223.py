import datetime

import tenders.runner
from tenders.models import *


class Runner(tenders.runner.Runner):


	name  = 'Zakupki.gov.ru FZ223'
	alias = 'fz223'

	black_list = []

	categories = {
		'essences' : 'out/nsi',
		'regions'  : 'out/published'}

	subcategories = [
		None,
		'daily'
		]


	def __init__(self):

		super().__init__()

		self.max_time = datetime.timedelta(0, 60*60*23, 0)

		self.url = 'ftp.zakupki.gov.ru'

		self.essences = [
			{'category' : 'nsiOkdp',           'parser' : self.parse_okdp},
			{'category' : 'nsiOkato',          'parser' : self.parse_okato},

			{'category' : 'nsiOkei',           'parser' : self.parse_okei},


#			{'category' : 'nsiAgency',         'parser' : self.parse_agency},
#			{'category' : 'nsiClauseType',     'parser' : self.parse_},
#			{'category' : 'nsiOkfs',           'parser' : self.parse_},
#			{'category' : 'nsiOkogu',          'parser' : self.parse_},
#			{'category' : 'nsiOkopf',          'parser' : self.parse_},
#			{'category' : 'nsiOkpd2',          'parser' : self.parse_},
#			{'category' : 'nsiOktmo',          'parser' : self.parse_},
#			{'category' : 'nsiOkv',            'parser' : self.parse_},
#			{'category' : 'nsiOkved',          'parser' : self.parse_},
#			{'category' : 'nsiOkved2',         'parser' : self.parse_},
#			{'category' : 'nsiOrganisation',   'parser' : self.parse_},
#			{'category' : 'nsiProtokol',       'parser' : self.parse_},
#			{'category' : 'nsiPurchaseMethod', 'parser' : self.parse_},
		]

		self.region_essences = [
#			{'category' : 'plangraphs',    'parser' : self.parse_plan},
#			{'category' : 'notifications', 'parser' : self.parse_notification},
		]


	def run(self):


		if not self.updater.login or not self.updater.password:
			print('Ошибка: Проверьте параметры авторизации. Кажется их нет.')
			return False

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

		for subcategory in self.subcategories:

			if subcategory:
				catalog = "{}/{}/{}".format(self.categories['essences'], essence['category'], subcategory)
			else:
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
						continue

					# Обрабатываем файл
					parse = essence['parser']
					parse(tree)

				source.complite()

		return True


	def parse_okdp(self, tree):
		'Парсит ОКДП.'

		# TODO KILL
		import xml.etree.ElementTree as ET
#		print(ET.tostring(element, encoding = 'unicode'))


		for element in tree.xpath('.//item'):

			parent = OKDP.objects.take(code = self.get_text(element, './nsiOkdpData/parentCode'))

			okdp = OKDP.objects.update(
				code = self.get_text(element, './nsiOkdpData/code'),
				name = self.get_text(element, './nsiOkdpData/name'),
				parent        = parent,
				state         = True)
			print("ОКДП: {}.".format(okdp))

			ext_key = OKDPExtKey.objects.update(
				updater = self.updater,
				ext_key = self.get_text(element, './guid'),
				okdp = okdp)

			ext_key = OKDPExtKey.objects.update(
				updater = self.updater,
				ext_key = self.get_text(element, './nsiOkdpData/guid'),
				okdp = okdp)

		return True



	def parse_okato(self, tree):
		'Парсит ОКАТО (классификация населённых пунктов'

		for element in tree.xpath('.//item'):

			parent = OKATO.objects.take(code = self.get_text(element, './nsiOkatoData/parentCode'))

			okato = OKATO.objects.update(
				code = self.get_text(element, './nsiOkatoData/code'),
				name = self.get_text(element, './nsiOkatoData/name'),
				parent        = parent,
				state         = True)
			print("ОКАТО: {}.".format(okato))

			ext_key = OKATOExtKey.objects.update(
				updater = self.updater,
				ext_key = self.get_text(element, './guid'),
				okato   = okato)

		return True



	def parse_okei(self, tree):
		'Парсит ОКЕИ (единицы измерения)'

		for element in tree.xpath('.//item'):

			section = OKEISection.objects.take(
				code  = self.get_text(element, './nsiOkeiData/section/code'),
				name  = self.get_text(element, './nsiOkeiData/section/name'),
				state = True)

			group = OKEIGroup.objects.take(
				code  = self.get_text(element, './nsiOkeiData/group/code'),
				name  = self.get_text(element, './nsiOkeiData/group/name'),
				state = True)

			okei = OKEI.objects.update(
				code    = self.get_text(element, './nsiOkeiData/code'),
				section = section,
				group   = group,
				name    = self.get_text(element, './nsiOkeiData/name'),
				symbol  = self.get_text(element, './nsiOkeiData/symbol'))
			print("Единица измерения: {}.".format(okei))

			ext_key = OKEIExtKey.objects.update(
				updater = self.updater,
				ext_key = self.get_text(element, './guid'),
				okei    = okei)

		return True







# TODO END
















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
