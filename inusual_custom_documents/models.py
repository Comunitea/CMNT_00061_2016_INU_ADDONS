# -*- coding: utf-8 -*-

from openerp import models, fields, api 


class Manufacturing_order(models.Model): 
	_inherit = 'mrp.production'

	notes = fields.Text()


class StockPicking(models.Model):
	_inherit = 'stock.picking'
	
	comments = fields.Text()
