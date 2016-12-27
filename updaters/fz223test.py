import tenders.updaters.fz223
from tenders.models import *


class Runner(tenders.updaters.fz223.Runner):


	subcategories = [
		None,
		'daily'
		]


	def __init__(self):

		super().__init__()

		self.url = 'ftp.zakupki.gov.ru'

		self.essences = [
#			{'category' : 'nsiOkdp',           'parser' : self.parse_okdp},
#			{'category' : 'nsiOkato',          'parser' : self.parse_okato},
			{'category' : 'nsiOkei',           'parser' : self.parse_okei},

#			{'category' : 'nsiAgency',         'parser' : self.parse_agency},
#			{'category' : 'nsiClauseType',     'parser' : self.parse_},
#			{'category' : 'nsiOkfs',           'parser' : self.parse_},
#			{'category' : 'nsiOkogu',          'parser' : self.parse_},
#			{'category' : 'nsiOkopf',          'parser' : self.parse_},
#			{'category' : 'nsiOkpd2',          'parser' : self.parse_},
#			{'category' : 'nsiOktmo',          'parser' : self.parse_},
#			{'category' : 'nsiOkv',            'parser' : self.parse_},
#			{'category' : 'nsiOkved',          'parser' : self.parse_},
#			{'category' : 'nsiOkved2',         'parser' : self.parse_},
#			{'category' : 'nsiOrganisation',   'parser' : self.parse_},
#			{'category' : 'nsiProtokol',       'parser' : self.parse_},
#			{'category' : 'nsiPurchaseMethod', 'parser' : self.parse_},
		]

		self.region_essences = [
#			{'category' : 'plangraphs',    'parser' : self.parse_plan},
#			{'category' : 'notifications', 'parser' : self.parse_notification},
		]
