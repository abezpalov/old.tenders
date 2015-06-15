import time
from datetime import date
from django.utils import timezone
from catalog.models import Currency
from tenders.models import *


class Runner:

	name = 'Обновление с сайта государственных закупок России'
	alias = 'zakupki-gov-ru'

	def __init__(self):

		# Загрузчик
		self.updater = Updater.objects.take(
			alias = self.alias,
			name  = self.name)

		# Основная валюта
		self.currency = {}
		self.currency['rub'] = Currency.objects.get(alias = 'RUB')
		self.currency['usd'] = Currency.objects.get(alias = 'USD')
		self.currency['eur'] = Currency.objects.get(alias = 'EUR')

		self.url = 'ftp.zakupki.gov.ru'


	def run(self):

		# Проверяем наличие параметров авторизации
		if not self.updater.login or not self.updater.password:
			print('Ошибка: Проверьте параметры авторизации. Кажется их нет.')
			return False

		# Получаем список регионов с FTP-сервера
		regions = self.getFTPCatalog('fcs_regions')
		print(regions)
		print('\n')


		for region in regions:

			if region != '_logs':
				region = Region.objects.take(alias = region, name = region, full_name = region)

				if region.state:
					content = self.getFTPCatalog('fcs_regions/{}'.format(region.alias))
					print(region.name)
					print(content)
					print('\n')

					# Ждем, чтобы не получить отбой сервера
					time.sleep(10)

		# TODO

		return True


	def getFTPCatalog(self, catalog = None):

		# Импортируем
		from ftplib import FTP

		# Подключаемся
		ftp = FTP(
			host   = self.url,
			user   = self.updater.login,
			passwd = self.updater.password)

		# Авторизуемся
		ftp.login()

		# Переходим в нужный каталог
		if catalog:
			ftp.cwd(catalog)

		# Получаем содержимое каталога
		result = ftp.nlst()

		# Закрываем соединение
		ftp.close()

		# Возвращаем результат
		return result





