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

		products = PlanGraphPositionProduct.objects.all()

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
				print("Продукт {} из {}. Чисто.".format(n, len(products)))

		print("Обработка завершена за {}.".format(timezone.now() - start))

		return True
