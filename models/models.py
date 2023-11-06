# -*- coding: utf-8 -*-

from odoo import models, fields, api
import xmlrpc.client
from datetime import datetime

class ModuleName(models.Model):
    _inherit = 'res.company'
    url_method = fields.Char(string='URL Servidor Method',default="https://erp.method.cl")
    bd_method=fields.Char(string='Base de Datos Method',default="method")
    user_method=fields.Char(string='Usuario Method',default="cesar@method.cl")
    password_method=fields.Char(string='Password Usuario Method',default="2010")
    dias_desactivacion = fields.Integer(string='Nro Dias', default=10,help="Nro de dias despues de la fecha de vencimento para la desactivación")
    deuda_method = fields.Integer(string='Total Faturas Impagas')
    dias_vcto = fields.Integer(string='Días Vencidos' ,default=5)
    usuario_admin = fields.Char(string='Usuario Administrador', default="cesar@method.cl")    
    

    @api.one
    def obtener_deuda_method(self):
        datos=self.search([('id','=',1)])
        url = datos.url_method
        db = datos.bd_method
        username = datos.user_method
        password = datos.password_method
        
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        uid = common.authenticate(db, username, password, {})
        rut_partner=datos.vat
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
                    ['name','=','Suscripcion'],
                    ['state','=','open']]],                    
                [])
                total_deuda=0
                fecha_actual = datetime.now()
                dias=0
                dias_mayor=0
                if deuda:
                    for d in deuda:
                        total_deuda+=d["residual"]
                        fecha_vcto = datetime.strptime(d["date_due"], "%Y-%m-%d")
                        dias= abs((fecha_actual - fecha_vcto).days)
                        if dias_mayor<dias and dias_mayor>0:
                            dias_mayor=dias
                        elif dias_mayor==0:
                            dias_mayor=dias
                    datos.deuda_method=total_deuda
                    datos.dias_vcto=dias_mayor
                    if dias_mayor>=datos.dias_desactivacion:
                        usuario=self.env['res.users'].search([('login','!=',datos.usuario_admin)])
                        usuario.write({
                            'active':False
                            })
                    else:
                        usuario=self.env['res.users'].search([('active','=',False),('id','!=',1)])                    
                        usuario.write({
                            'active':True
                            })
                else:
                    datos.deuda_method=total_deuda
                    datos.dias_vcto=dias_mayor                    
                    usuario=self.env['res.users'].search([('active','=',False),('id','!=',1)])                    
                    usuario.write({
                        'active':True
                        })

