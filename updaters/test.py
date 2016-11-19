import tenders.updaters.zakupki

class Runner(tenders.updaters.zakupki.Runner):

	subcategories = [
#		None,
#		'prevMonth',
		'currMonth']

	def __init__(self):

		super().__init__()

		self.essences = [
#			{'category' : 'nsiKVR', 'parser' : self.parse_kvr},
		]

		self.region_essences = [
#			{'category' : 'plangraphs',    'parser' : self.parse_tenderplan},
			{'category' : 'notifications', 'parser' : self.parse_notification},
		]
