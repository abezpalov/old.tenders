import tenders.updaters.fz223
from tenders.models import *


class Runner(tenders.updaters.fz223.Runner):


	subcategories = [
		None,
		'daily'
		]


	def __init__(self):

		super().__init__()


	def run(self):


		t1 = Updater.objects.get(alias = self.alias)
		t2 = Updater.objects.get(alias = self.alias)

		print(t1)
		print(t2)

		if t1 == t2:
			print('==')
		else:
			print('no((')
