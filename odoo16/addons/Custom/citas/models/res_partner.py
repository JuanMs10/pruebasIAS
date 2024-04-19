from odoo import fields, models
import requests


class ResPartner(models.Model):

    name = fields.String(compute='_compute_name_doctor')

    r = requests.get('https://api-colombia.com/api/v1/President/{id}')

    def _compute_name_doctor(self, id):
        