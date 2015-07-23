import gc
from tenders.models import *
from project.models import Log

from django.utils import timezone


class Runner:


	name = 'Проверка дублей'
	alias = 'test-doubles'

	def __init__(self):

		# Загрузчик
		self.updater = Updater.objects.take(
			alias = self.alias,
			name  = self.name)

	def run(self):

		start = timezone.now()

		products_count = PlanGraphPositionProduct.objects.all().count()

		#
		print(products_count)

		items_on_page   = 1000

		page_max = products_count // items_on_page
		if products_count % items_on_page:
			page_max += 1

		#
		print(page_max)

		for pn in range(0, page_max):
			products = PlanGraphPositionProduct.objects.all()[pn * items_on_page : (pn + 1) * items_on_page]

			print(len(products))

			for n, product in enumerate(products):

				test = PlanGraphPositionProduct.objects.filter(
					position = product.position,
					number = product.number)

				if len(test) > 1:
					log = Log.objects.add(
						subject = "Tenders SQL",
						channel = "Critical Error",
						title = "Double Product: position.id = {}, number = {}.".format(position.id, number))

					print(log)

				else:

					print("Продукт {}{} из {}. Чисто.".format(pn, n, products_count))

		print("Обработка завершена за {}.".format(timezone.now() - start))

		return True
