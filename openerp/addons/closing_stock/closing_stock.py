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
        
        'line_ids': fields.one2many('closing_stock.line','closing_id','Line Id', size=128),
        
    }
    
    def load_stock(self, cr, uid, ids, context=None):
        cr.execute("""delete from closing_stock_line""")
        product_list = []
        
        psql1 = """select distinct product_id from stock_move """    
        cr.execute(psql1)
        pdata = cr.dictfetchall()
        
        rec = self.browse(cr, uid, ids[0])
        
        for i in pdata:
            
            pro_rec = self.pool.get('product.product').browse(cr,uid,i['product_id'])
            product_list.append(pro_rec)
        
        for item in product_list:
            in_qty = 0.00
            out_qty = 0.00
           
            in_move_obj = self.pool.get('stock.move').search(cr,uid,[('location_dest_id','=',23),('product_id','=',item.id)])
            in_move_rec = self.pool.get('stock.move').browse(cr,uid,in_move_obj)
            
            if in_move_rec:
                for i in in_move_rec:
                    in_qty +=i.product_qty
                    
           
            out_move_obj = self.pool.get('stock.move').search(cr,uid,[('location_id','=',23),('product_id','=',item.id)])
            out_move_rec = self.pool.get('stock.move').browse(cr,uid,out_move_obj)
            
            if out_move_rec:
                for j in out_move_rec:
                    out_qty +=j.product_qty
           
            close_qty = in_qty - out_qty
            
           
            if close_qty > 0:
				
                
                self.pool.get('closing_stock.line').create(cr, uid, {
                            'closing_id': rec.id,
                            'product_id': item.id,
                            'uom': item.uom_id.id,
                            
                            'receive_qty':in_qty,
                            'issued_qty': out_qty,
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
        'receive_qty': fields.float('Receive Qty'),
        'issued_qty': fields.float('Issued Qty'),
        'closing_stocks': fields.float('Closing Stocks'),
        
    }
        
closing_stock_line()

    
