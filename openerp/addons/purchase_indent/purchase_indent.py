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
dt_time = a.strftime('%d/%m/%Y')

class purchase_indent(osv.osv):

    _name = "purchase_indent"
    _description = "purchase_indent"

    _columns = {
        
        'name': fields.char('Indent No', readonly=True),
        
        'indent_date':fields.date('Indent date',required=True),
        'expected_date':fields.date('Expected date',required=True),
        'purchase': fields.many2one('department_master','Purchase', required=True),
        'line_ids': fields.one2many('purchase_indent.line','indent_no','Line Id', size=128),
        
    }
    
    _defaults = {
        'name': '/',
        'indent_date':fields.date.context_today,
       
    }
    
    
    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'indent') or '/'
        order =  super(indent, self).create(cr, uid, vals, context=context)
        return order
        
    
purchase_indent()

class purchase_indent_line(osv.osv):

    _name = "purchase_indent.line"
    _description = "purchase_indent"

    _columns = {
        
        'indent_no': fields.many2one('purchase_indent','Indent No', size=128),
        'department': fields.many2one('department_master', 'Department', required=True),
        'brand': fields.many2one('master', 'Brand'),

        'product_uom': fields.many2one('product.uom', 'Product Unit of Measure', required=True),
        'product_id': fields.many2one('product.product', 'Product', domain=[('purchase_ok','=',True)]),
        'qty':fields.float('Qty')
        
        
    }
    
    def onchange_product_uom(self, cr, uid, ids, product_id, context=None):
        value = {'product_uom' : ''}
        if context is None:
            context = {}
        if product_id:
            product_rec = self.pool.get('product.product').browse(cr,uid,product_id)
            value={'product_uom' : product_rec.uom_id or False}
        return value
    
    
purchase_indent_line()


