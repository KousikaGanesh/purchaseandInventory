from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import re
from operator import itemgetter
from itertools import groupby
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import netsvc
from openerp import tools
from openerp.tools import float_compare, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)
a = datetime.now()
dt_time = a.strftime('%m/%d/%Y %H:%M:%S')

class department_master(osv.osv):

	_name = "department_master"
	_description = "department_master"

	_columns = {
		
		'name': fields.char('Name', size=128),
		'creation_date':fields.datetime('Creation date'),
		
		'stock_location': fields.many2one('stock.location', 'Stock location'),
		'main_location': fields.many2one('stock.location', 'Main location'),
		'used_location': fields.many2one('stock.location', 'Used location'),


	}
department_master()


