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

class issue(osv.osv):

	_name = "issue"
	_description = "issue"

	_columns = {
		
		'issue_no': fields.char('Issue No', size=128),
		
		'issue_date':fields.datetime('Issue date'),
		'department_name':fields.many2one('department_master','Department Name'),
		'department_indent_id': fields.char('Department Indent Id', size=128),
		'line_ids': fields.one2many('purchase_indent.line','indent_no','Line Id', size=128),
		
	}
	
	
	
issue()

class issue_line(osv.osv):

	_name = "issue.line"
	_description = "issue"

	_columns = {
		
		
		'indent_no': fields.many2one('purchase_indent','Indent No', size=128),
		'department': fields.many2one('department_master', 'Department', required=True),
		'brand': fields.many2one('department_master', 'Brand', domain=[('purchase_ok','=',True)]),

		'product_uom': fields.many2one('product.uom', 'Product Unit of Measure', required=True),
        'product_id': fields.many2one('product.product', 'Product', domain=[('purchase_ok','=',True)]),
        'qty':fields.float('Qty')
		
		
	}
	
	
	
issue_line()


