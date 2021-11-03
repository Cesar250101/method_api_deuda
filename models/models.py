# -*- coding: utf-8 -*-

from odoo import models, fields, api
import xmlrpc.client
from datetime import datetime

class ModuleName(models.Model):
    _inherit = 'res.company'
    url_method = fields.Char(string='URL Servidor Method',default="http://3.129.134.37:8069")
    bd_method=fields.Char(string='Base de Datos Method',default="method")
    user_method=fields.Char(string='Usuario Method',default="cesar@method.cl")
    password_method=fields.Char(string='Password Usuario Method',default="2010")
    dias_desactivacion = fields.Integer(string='Nro Dias', default=10,help="Nro de dias despues de la fecha de vencimento para la desactivación")
    deuda_method = fields.Integer(string='Total Faturas Impagas')
    dias_vcto = fields.Integer(string='Días Vencidos')
    usuario_admin = fields.Char(string='Usuario Administrador', default="cesar@method.cl")    
    

    @api.one
    def obtener_dte_email(self):
        url = self.url_method
        db = self.bd_method
        username = self.user_method
        password = self.password_method
        
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        uid = common.authenticate(db, username, password, {})
        rut_partner=self.vat
        if rut_partner:
            partner_id=models.execute_kw(db, uid, password,
                'res.partner', 'search_read',
                [[['vat', '=', rut_partner]]],
                [])
            partner_id=partner_id[0]["id"]
            if partner_id:
                deuda=models.execute_kw(db, uid, password,
                'account.invoice', 'search_read',
                [[['commercial_partner_id', '=', partner_id],
                    ['type','=','out_invoice'],
                    ['state','=','open']]],
                [])
                total_deuda=0
                fecha_actual = datetime.now()
                dias=0
                dias_mayor=0
                for d in deuda:
                    total_deuda+=d["residual"]
                    fecha_vcto = datetime.strptime(d["date_due"], "%Y-%m-%d")
                    dias= abs((fecha_actual - fecha_vcto).days)
                    if dias_mayor<dias and dias_mayor>0:
                        dias_mayor=dias
                    elif dias_mayor==0:
                        dias_mayor=dias
                self.deuda_method=total_deuda
                self.dias_vcto=dias_mayor
                if dias_mayor>=self.dias_desactivacion:
                    usuario=self.env['res.users'].search([('login','!=',self.usuario_admin)])
                    usuario.write({
                        'active':False
                        })
