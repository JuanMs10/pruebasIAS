from odoo import fields, models


class Citas(models.Model):

    num_reserva = fields.Integer(string="Numero de Reserva")
    doctor = fields.String(string="Doctor", related='')
    responsable = fields.String("Responsable")
    fecha = fields.Calendar(string="Fecha")
    hora_inicio = fields.time(String="Hora Inicio")
    hora_fin = fields.time(String="Hora Fin")
    consultorio = fields.Integer(string="Consultorio")
    costo_reserva = fields.Monetary(string="Costo Reserva")
    especialidad = fields.String(string="Especialidad")
    estado = fields.Selection([('Borrador', 'borrador'),
                               ('Confirmado', 'confirmado'),
                               ('Reservado', 'reservado')], string="Estado")
