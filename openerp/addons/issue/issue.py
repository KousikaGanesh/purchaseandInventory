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
        'flag_opening':fields.boolean('Opening'),
        'issue_date':fields.datetime('Issue date'),
        'department_name':fields.many2one('department_master','Department Name'),
        'department_indent_id': fields.many2one('indent','Department Indent Id'),
        'line_ids': fields.one2many('issue.line','issue_no','Line Id', size=128),
        'flag_opening':fields.boolean('Opening'),
    }
 
    _defaults = {
        'issue_no': '/',
       
       
    } 
    
    def create(self, cr, uid, vals, context=None):
        if vals.get('issue_no','/')=='/':
            vals['issue_no'] = self.pool.get('ir.sequence').get(cr, uid, 'issue') or '/'
        order =  super(issue, self).create(cr, uid, vals, context=context)
        return order
    
    def load_issue(self, cr, uid, ids, context=None):
        rec = self.browse(cr, uid, ids[0])
        self.write(cr,uid,rec.id,{'flag_opening':True})
        

        for element in rec.department_indent_id.line_ids:
            
            self.pool.get('issue.line').create(cr, uid, {
                             'issue_no': rec.id,
                                    
                              'brand': element.brand.id,
							  'indent_line':element.id,
                              'product_uom': element.product_uom.id,
                              'product_id': element.product_id.id,
                              'qty':element.qty,
                              
    
                        })
        
        return True


    def issue_stock(self, cr, uid, ids, context=None):
        move_obj = self.pool.get('stock.move')
        loc_obj = self.pool.get('stock.location').search(cr,uid,[('location_type','=','main')])
        
        rec = self.browse(cr, uid, ids[0])
        self.write(cr,uid,rec.id,{'flag_opening':False})
        for item in rec.line_ids:
            
            move_obj.create(cr, uid, {
                            'product_uos_qty': item.qty,
                            'product_uom': item.product_uom.id,
                            'product_id': item.product_id.id,
                            'name': item.product_id.name,
                            'product_qty':item.qty,
                            'price_unit':0.00,
                            'state':'done',
                            'partner_id':1,
                            'company_id':1,
                            'location_id':loc_obj[0],
                            'location_dest_id':rec.department_name.stock_location.id,
                            'move_type':'out',
    
                        })
    
        return True
    
    
issue()

class issue_line(osv.osv):

    _name = "issue.line"
    _description = "issue"

    _columns = {
        
        
        'issue_no': fields.many2one('issue','Issue No', size=128),
        
        'brand': fields.many2one('master', 'Brand'),
		'indent_line': fields.many2one('indent.line','Department Indent Id'),
        'product_uom': fields.many2one('product.uom', 'Product Unit of Measure', required=True),
        'product_id': fields.many2one('product.product', 'Product', domain=[('purchase_ok','=',True)]),
        'qty':fields.float('Qty')
        
        
    }
    
    
    
issue_line()


