import datetime
from catalog.models import Updater
from project.models import Log
from django.utils import timezone


class Runner:

	name  = 'Anodos-tenders: ежедневный запуск'
	alias = 'anodos-tenders-everyday'

	updaters = ['zakupki-gov-ru']

	def __init__(self):

		# Загрузчик
		self.updater = Updater.objects.take(
			alias       = self.alias,
			name        = self.name)


	def run(self):

		start = datetime.datetime.now()

		for updater in self.updaters:

			# Выполняем необходимый загрузчик
			try:
				print("Пробую выполнить загрузчик {}".format(updater))
				Updater = __import__('tenders.updaters.{}'.format(updater), fromlist=['Runner'])
				runner = Updater.Runner()
				if runner.updater.state:
					if runner.run():
						runner.updater.updated = timezone.now()
						runner.updater.save()
			except Exception as error:
				Log.objects.add(
					subject    = "Tenders Updater Everyday: {}".format(updater),
					channel    = "error",
					title      = "Exception",
					description = error)

		print("Обработки завершены за {}.".format(datetime.datetime.now() - start))

		return True
