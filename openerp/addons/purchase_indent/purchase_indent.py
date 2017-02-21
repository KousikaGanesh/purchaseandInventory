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

class purchase_indent(osv.osv):

	_name = "purchase_indent"
	_description = "purchase_indent"

	_columns = {
		
		'name': fields.char('Indent No', size=128),
		
		'indent_date':fields.datetime('Indent date'),
		'expected_date':fields.datetime('Expected date'),
		'purchase': fields.char('Purchase', size=128),
		'line_ids': fields.one2many('indent.line','indent_id','Line Id', size=128),
		
	}
	
	
	
purchase_indent()


