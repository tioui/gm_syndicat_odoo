# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

class Member(models.Model):
    _name = 'gm_syndicat.member'

    name = fields.Char(string="Nom", required=True)
    first_name = fields.Char(string="Prenom", required=True)
    employee_id = fields.Integer(string="Numéro d'employé")
    is_member = fields.Boolean(string="Membre")
    is_regular = fields.Boolean(string="Formation régulière")
    is_continuing_education = fields.Boolean(string="Formation continue")
    is_permanent = fields.Boolean(string="Permanent")
    years_of_schooling = fields.Integer(string="Années de scolarité")
    years_of_service = fields.Float(digits=(2,4), string="Années d'ancienneté")
    salary_grade = fields.Integer(string="Échelon salarial")
    experience = fields.Float(digits=(2,4), string="Expérience")
    discipline_ids = fields.Many2many('gm_syndicat.discipline',
            string="Discipline")
    workload = fields.Float(digits=(1,4), string="Charge")
    address = fields.Char(string="Adresse")
    postal_code = fields.Char(string="Code Postal")
    city_id = fields.Many2one('gm_syndicat.city',
            string='Ville', ondelete="set null")
    email = fields.Char(string="Courriel")
    phone_number = fields.Char(string="Numéro de téléphone")
    gender = fields.Selection([('male', 'Homme'), ('female', 'Femme'),
        ('other', 'Autre')], 'Sexe', required=True)
    status = fields.Selection([('full_time', 'Temps plein'), ('part_time', 'Temps partiel'),
        ('lecturer', 'Chargé de cours')], 'Statut')
    date_of_birth = fields.Date(string="Date de naissance")
    comment = fields.Text(string="Commentaires")
    attachment_ids = fields.One2many('gm_syndicat.member_attachment',
            'member_id', string="Pièces jointes")
    intervention_ids = fields.One2many('gm_syndicat.intervention',
            'member_id', string="Interventions")
    intervention_attachment_ids = fields.One2many(
            'gm_syndicat.intervention_attachment',
            string="Pièce jointe d'interventions",
            readonly=True,
            compute='_intervention_attachment_ids')

    creator_id = fields.Many2one('res.users', string="Créateur",
            default= lambda self: self.env.user.id,
            readonly=True, ondelete="set null")

    full_name = fields.Char(string="Nom complet", compute='_full_name')
    full_address = fields.Char(string="Adresse complète", compute='_full_address')
    full_city = fields.Char(string="Ville complète", compute='_full_city')

    @api.depends('name', 'first_name')
    def _full_name(self):
        for la_object in self:
            la_object.full_name = la_object.first_name + ' ' + la_object.name

    def _get_full_city(self,a_object):
        l_value = ""
        if a_object.city_id:
            l_value = a_object.city_id.name_with_province
        return l_value

    @api.multi
    def _full_address(self):
        for la_object in self:
            l_value = ""
            if la_object.address:
                l_value = l_value + la_object.address + ", "
            l_value = l_value + self._get_full_city(la_object)
            la_object.full_address = l_value.strip(" ,")

    @api.multi
    def _full_city(self):
        for la_object in self:
            la_object.full_city = self._get_full_city(la_object)

    @api.depends('intervention_ids')
    def _intervention_attachment_ids(self):
        for la_object in self:
            ids = None
            for la_intervention in la_object.intervention_ids:
                if ids:
                    ids |= la_intervention.attachment_ids
                else:
                    ids = la_intervention.attachment_ids
            la_object.intervention_attachment_ids = ids

    @api.multi
    def new_intervention(self):
        res = {
           'type': 'ir.actions.act_window',
           'name': _('gm_syndicat.member.intervention'),
           'res_model': 'gm_syndicat.intervention',
           'view_type': 'form',
           'view_mode': 'form',
           'view_id': False,
           'nodestroy': False,
           'target': 'new',
           'flags': {'form': {'action_buttons': True}},
           'context':{'default_member_id': self.id}
        }
    
        return res

class City(models.Model):
    _name = 'gm_syndicat.city'

    name = fields.Char(string="Nom", require=True)
    province_id = fields.Many2one('gm_syndicat.province',
            string='Province', ondelete="cascade", required=True)
    name_with_province = fields.Char(string="Province complète",
            compute='_name_with_province')
    _rec_name = 'name_with_province'

    @api.multi
    def _name_with_province(self):
        for la_object in self:
            la_object.name_with_province = la_object.name + ", " + \
                la_object.province_id.name + ", " +\
                la_object.province_id.country_id.name

class Province(models.Model):
    _name = 'gm_syndicat.province'

    name = fields.Char(string="Nom", require=True)
    country_id = fields.Many2one('res.country', string='Country',
                    store=True)

class Discipline(models.Model):
    _name = 'gm_syndicat.discipline'

    name = fields.Char(string="Nom", require=True)
    number = fields.Integer(string="Numéro", require=True)

class Member_attachment(models.Model):
    _name = 'gm_syndicat.member_attachment'
    member_id = fields.Many2one('gm_syndicat.member', string="Membre")
    _inherit = 'ir.attachment'

class Intervention_attachment(models.Model):
    _name = 'gm_syndicat.intervention_attachment'
    intervention_id = fields.Many2one('gm_syndicat.intervention', string="Intervention")
    _inherit = 'ir.attachment'

class Intervention(models.Model):
    _name = 'gm_syndicat.intervention'
    name = fields.Char(string="Description courte", required=True)
    date = fields.Date(string="Date", required=True)
    description = fields.Text(string="Description longue")
    attachment_ids = fields.One2many('gm_syndicat.intervention_attachment',
            'intervention_id', string="Pièces jointes")
    creator_id = fields.Many2one('res.users', string="Créateur",
            default= lambda self: self.env.user.id,
            readonly=True, ondelete="set null")
    member_id = fields.Many2one('gm_syndicat.member', string="Membre")

    @api.multi
    def close(self):
        return {'type': 'ir.actions.act_window_close'}
