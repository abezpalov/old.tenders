import tenders.updaters.fz44
from tenders.models import *

class Runner(tenders.updaters.fz44.Runner):

	subcategories = [
		None,
		'prevMonth',
		'currMonth']

	def __init__(self):

		super().__init__()

		self.essences = [
#			{'category' : 'nsiOKPD', 'parser' : self.parse_okpd},
#			{'category' : 'nsiOKPD2', 'parser' : self.parse_okpd2},
#			{'category' : 'nsiOKVED', 'parser' : self.parse_okved},
#			{'category' : 'nsiOKVED2', 'parser' : self.parse_okved2},
#			{'category' : 'nsiOrganization', 'parser' : self.parse_organisation},

		]

		self.region_essences = [
#			{'category' : 'plangraphs',    'parser' : self.parse_plan},
			{'category' : 'notifications', 'parser' : self.parse_notification},
		]

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
					continue

				# Обрабатываем файл
				parse = essence['parser']
				parse(tree)

#			source.complite()

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
						continue

					# Обрабатываем файл
					parse = essence['parser']
					parse(tree, region)

#				source.complite()

		return True

