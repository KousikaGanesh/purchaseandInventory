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

class grn(osv.osv):

	_name = "grn"
	_description = "grn"

	_columns = {
		
		'created_by': fields.char('Created By', size=128),
		
		'grn_no':fields.char('GRN No'),
		'dc_no':fields.char('DC No'),
		'inward_type': fields.char('Inward Type', size=128),
	'billing_type': fields.char('Billing Type', size=128),
	'created_date': fields.datetime('Created Date', size=128),
	'grn_date':fields.datetime('GRN Date'),
	'dc_date':fields.datetime('DC Date'),
	'payment_type': fields.char('Payment Type', size=128),
	'supplier': fields.char('Supplier', size=128),
	'supplier_invoice_no':fields.char('Supplier Invoice No'),
	'supplier_invoice_date':fields.datetime('Supplier Invoice Date'),	
    'line_ids': fields.one2many('grn.line', 'grn_id', 'GRN Id'),

	}
	
grn()



class grn_line(osv.osv):

	_name = "grn.line"
	_description = "grn"

	_columns = {
		
		'grn_id': fields.many2one('grn','GRN No', size=128),
		'product_uom': fields.many2one('product.uom', 'Product Unit of Measure', required=True),
        'product_id': fields.many2one('product.product', 'Product'),
        'brand': fields.many2one('master', 'Brand', ),
        'qty':fields.float('Qty')
		
	}
	
	
	
	
grn_line()



