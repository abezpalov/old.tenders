import requests

import datetime
from django.utils import timezone

from tenders.models import *
from project.models import Log


class Runner:


	def __init__(self):

		self.start_time = timezone.now()

		self.updater = Updater.objects.take(
			alias       = self.alias,
			name        = self.name)

		self.max_time = datetime.timedelta(0, 60*60*23, 0)

		Log.objects.add(
			subject     = "tenders.updater.{}".format(self.updater.alias),
			channel     = "start",
			title       = "Start",
			description = "Запущен загрузчик {}.".format(self.updater.name))


	def log(self):

		pass


	def get_ftp_catalog(self, host, catalog = None):
		'Возвращает содержимое папки'

		# Импортируем
		from ftplib import FTP

		# Авторизуемся
		ftp = FTP(host = host)
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


	def get_file_from_ftp(self, host, catalog, file_name):
		'Скачивает и возвращает файл с FTP-сервера'

		# Импортируем
		from ftplib import FTP
		from io import BytesIO
		from zipfile import ZipFile

		# Инициализируем переменные
		ftp = FTP(host = self.url)
		zip_file = BytesIO(b"")

		# Авторизуемся
		ftp.login(user = self.updater.login, passwd = self.updater.password)

		# Переходим в нужный каталог
		ftp.cwd(catalog)

 		# Скачиваем архив
		print("Скачиваю файл: {}".format(file_name))
		try:
			ftp.retrbinary("RETR {}".format(file_name), zip_file.write)
			zip_data  = ZipFile(zip_file)
		except:
			print("Ошибка: невозможно скачать файл. Перехожу с следующему.")
			return False

		# Возвращаем результат
		return zip_data


	def get_tree_from_zip(self, zip_data, xml_name):

		# Импортируем
		from lxml import etree

		try:
			xml_data = zip_data.open(xml_name)
		except Exception as error:
			Log.objects.add(
				subject     = "tenders.updater.{}".format(self.updater.alias),
				channel     = "error",
				title       = "Exception",
				description = "Не удалось извлечь файл {} из архива {}. {}".format(xml_name, zip_name, error))
			return False

		# Парсим
		try:
			tree = etree.parse(xml_data)
		except Exception:
			tree = None

		return tree


	def is_time_up(self):
		'Определяет не вышло ли время'

		if timezone.now() - self.start_time > self.max_time:
				print("Время вышло {}.".format(timezone.now() - self.start_time))
				return True

		else:
			return False


	def clear_tags(self, tree):

		# Чистим теги
		for element in tree.xpath('//*'):

			try:
				element.tag = element.tag.split('}')[1]
			except Exception:
				pass

			try:
				element.tag = element.tag.split(':')[1]
			except Exception:
				pass

		return tree
