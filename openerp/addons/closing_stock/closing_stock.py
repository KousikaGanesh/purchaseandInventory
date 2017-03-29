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

class closing_stock(osv.osv):

    _name = "closing_stock"
    _description = "closing_stock"

    _columns = {
        
        
        'date':fields.datetime('Date'),
        
        'line_ids': fields.one2many('closing_stock.line','product_id','Line Id', size=128),
        
    }
    
    def load_stock(self, cr, uid, ids, context=None):
        rec = self.browse(cr, uid, ids[0])
        pro_obj = self.pool.get('product.product').search(cr,uid,[('active','=',True)])
        pro_rec = self.pool.get('product.product').browse(cr,uid,pro_obj)

        for item in pro_rec:
            in_qty = 0.0
            out_qty = 0.0
            print "------------------------",item
            in_move_obj = self.pool.get('stock.move').search(cr,uid,[('location_dest_id','=',23),('product_id','=',item.id)])
            in_move_rec = self.pool.get('stock.move').browse(cr,uid,in_move_obj)
            
            if in_move_rec:
                for i in in_move_rec:
                    in_qty +=i.product_qty
            out_move_obj = self.pool.get('stock.move').search(cr,uid,[('location_id','=',23),('product_id','=',item.id)])
            out_move_rec = self.pool.get('stock.move').browse(cr,uid,out_move_obj)
            if out_move_rec:
                for j in out_move_rec:
                    out_qty +=i.product_qty
            
            close_qty = in_qty - out_qty
            self.pool.get('closing_stock.line').create(cr, uid, {
                             'closing_id': rec.id,
                                    
                              'brand': False,

                              'uom': item.uom_id.id,
                              'product_id': item.id,
                              'product_id': item.id,
                              'receive_qty':in_qty,
                              'issued_qty':out_qty,
                              'closing_stocks':close_qty,
    
                        })
    
        return True 
    
    
closing_stock()



class closing_stock_line(osv.osv):

    _name = "closing_stock.line"
    _description = "closing stock"

    _columns = {
        
        'closing_id': fields.many2one('closing_stock','Closing Id', size=128),
        'product_id': fields.many2one('product.product','Product Id', size=128),
        'uom': fields.many2one('product.uom', 'Product Unit of Measure', required=True),
        'receive_qty': fields.char('Receive Qty'),
        'issued_qty': fields.char('Issued Qty'),
        'closing_stocks': fields.char('Closing Stocks'),
        
    }
        
closing_stock_line()

    
