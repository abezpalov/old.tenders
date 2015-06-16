import time
from datetime import date
from django.utils import timezone
from tenders.models import *


class Runner:

	name = 'Обновление с сайта государственных закупок России'
	alias = 'zakupki-gov-ru'

	urls = {
		'base':    'ftp.zakupki.gov.ru',
		'lists':   'fcs_nsi',
		'regions': 'fcs_regions'
	}

	def __init__(self):

		# Загрузчик
		self.updater = Updater.objects.take(
			alias = self.alias,
			name  = self.name)

	def run(self):

		# Проверяем наличие параметров авторизации
		if not self.updater.login or not self.updater.password:
			print('Ошибка: Проверьте параметры авторизации. Кажется их нет.')
			return False

		print("login: {}".format(self.updater.login))
		print("password: {}".format(self.updater.password))


		# Получаем список регионов с FTP-сервера
		regions = self.getFTPCatalog('fcs_regions')
		print(regions)
		print('\n')


		for region in regions:

			if region != '_logs':
				region = Region.objects.take(
					alias = region,
					name = region,
					full_name = region)

				if region.state:

					# Ждем, чтобы не получить отбой сервера
					time.sleep(10)

					# Получаем содержимое каталога
					content = self.getFTPCatalog('{}/{}'.format(self.urls['regions'], region.alias))
					print(region.name)
					print(content)
					print('\n')

		# TODO

		return True


	def getFTPCatalog(self, catalog = None):

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





