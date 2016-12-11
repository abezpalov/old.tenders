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
		'prevMonth',
		'currMonth'
		]


	def __init__(self):

		super().__init__()

		self.url = 'ftp.zakupki.gov.ru'

		self.essences = [
			{'category' : 'nsiOkpd',           'parser' : self.parse_},

#			{'category' : 'nsiAgency',         'parser' : self.parse_},
#			{'category' : 'nsiOrganisation',   'parser' : self.parse_},
#			{'category' : 'nsiClauseType',     'parser' : self.parse_},
#			{'category' : 'nsiOkato',          'parser' : self.parse_},
#			{'category' : 'nsiOkei',           'parser' : self.parse_},
#			{'category' : 'nsiOkfs',           'parser' : self.parse_},
#			{'category' : 'nsiOkogu',          'parser' : self.parse_},
#			{'category' : 'nsiOkopf',          'parser' : self.parse_},
#			{'category' : 'nsiOkpd2',          'parser' : self.parse_},
#			{'category' : 'nsiOktmo',          'parser' : self.parse_},
#			{'category' : 'nsiOkv',            'parser' : self.parse_},
#			{'category' : 'nsiOkved',          'parser' : self.parse_},
#			{'category' : 'nsiOkved2',         'parser' : self.parse_},
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
