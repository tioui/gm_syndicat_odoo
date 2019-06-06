# -*- coding: utf-8 -*-
# =============================================================================
# title           :models.py
# description     :Classes used in the gm_syndicat addon
# author          :Louis Marchand
# date            :20180301
# version         :0.1
# notes           :
# python_version  :2.7.12
# =============================================================================


from openerp import models, fields, api, _

class Member(models.Model):
    """Represent a member of the syndicate"""
    _name = 'gm_syndicat.member'

    name = fields.Char(string="Nom", required=True)
    first_name = fields.Char(string="Prenom", required=True)
    employee_id = fields.Integer(string="Numéro d'employé")
    is_active = fields.Boolean(string="Actif", default=True)
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
        ('lecturer', 'Chargé de cours'), ('retired', 'Retraité')], 'Statut')
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

    full_name = fields.Char(string="Nom complet", compute='_full_name', store=True)
    full_address = fields.Char(string="Adresse complète", compute='_full_address', store=True)
    full_city = fields.Char(string="Ville complète", compute='_full_city', store=True)

    @api.depends('name', 'first_name')
    def _full_name(self):
        """Setting `full_name' attribute using `name' and `first_name'"""
        for la_object in self:
            la_object.full_name = la_object.name + ", " + la_object.first_name

    def _get_full_city(self,a_object):
        """
            Full city name using the `city', `province' and `country' names.
        """
        l_value = ""
        if a_object.city_id:
            l_value = a_object.city_id.name_with_province
        return l_value

    @api.depends('address', 'full_city')
    def _full_address(self):
        """
            Setting `full_address' with `address', `city', `province' and
            `country'.
        """
        for la_object in self:
            l_value = ""
            if la_object.address:
                l_value = l_value + la_object.address + ", "
            l_value = l_value + self._get_full_city(la_object)
            la_object.full_address = l_value.strip(" ,")

    @api.depends('address', 'city_id', 'city_id.name_with_province')
    def _full_city(self):
        """
            Setting `full_city' name using `city', province and country names.
        """
        for la_object in self:
            la_object.full_city = self._get_full_city(la_object)

    @api.depends('intervention_ids')
    def _intervention_attachment_ids(self):
        """
            Setting a list of every attachment of every `intervention_ids'
            in `intervention_attachment_ids'
        """
        for la_object in self:
            ids = None
            for la_intervention in la_object.intervention_ids:
                if ids:
                    ids |= la_intervention.attachment_ids
                else:
                    ids = la_intervention.attachment_ids
            la_object.intervention_attachment_ids = ids

class City(models.Model):
    """
        An address city.
    """
    _name = 'gm_syndicat.city'

    name = fields.Char(string="Nom", require=True)
    province_id = fields.Many2one('gm_syndicat.province',
            string='Province', ondelete="cascade", required=True)
    country_id = fields.Many2one('res.country', string="Pays",
            compute='_country_id')
    name_with_province = fields.Char(string="Ville complète",
            compute='_name_with_province', store=True)
    _rec_name = 'name_with_province'

    @api.depends('province_id', 'province_id.country_id')
    def _country_id(self):
        """
            Setting `country_id' using the `province_id'
        """
        for la_object in self:
            la_object.country_id = la_object.province_id.country_id

    @api.depends('name', 'province_id', 'province_id.country_id', 'province_id.country_id.name')
    def _name_with_province(self):
        """
            Setting `name_with_province' with the names of `self',
            province and country
        """
        for la_object in self:
            la_object.name_with_province = la_object.name + ", " + \
                la_object.province_id.name + ", " +\
                la_object.province_id.country_id.name

class Province(models.Model):
    """
        A province to be used in addresses.
    """
    _name = 'gm_syndicat.province'

    name = fields.Char(string="Nom", require=True)
    country_id = fields.Many2one('res.country', string='Country',
                    store=True, ondelete="cascade")
    name_with_country = fields.Char(string="Province complète",
            compute='_name_with_country', store=True)
    _rec_name = 'name_with_country'
    @api.depends('name', 'country_id', 'country_id.name')
    def _name_with_country(self):
        """
            Setting `name_with_country' with the `country_id'
        """
        for la_object in self:
            la_object.name_with_country = la_object.name + ", " + \
                la_object.country_id.name


class Discipline(models.Model):
    """
        Teaching domain.
    """
    _name = 'gm_syndicat.discipline'

    name = fields.Char(string="Nom", require=True)
    number = fields.Integer(string="Numéro", require=True)

class Member_attachment(models.Model):
    """
        File attachment of a member.
    """
    _name = 'gm_syndicat.member_attachment'
    member_id = fields.Many2one('gm_syndicat.member', string="Membre", ondelete="cascade")
    _inherit = 'ir.attachment'

class Intervention_attachment(models.Model):
    """
        File attachment of an Intervention
    """
    _name = 'gm_syndicat.intervention_attachment'
    intervention_id = fields.Many2one('gm_syndicat.intervention', string="Intervention", ondelete="cascade")
    _inherit = 'ir.attachment'

class Intervention(models.Model):
    """
        An intervention with a Member.
    """
    _name = 'gm_syndicat.intervention'
    name = fields.Char(string="Description courte", required=True)
    date = fields.Date(string="Date", required=True)
    description = fields.Text(string="Description longue")
    attachment_ids = fields.One2many('gm_syndicat.intervention_attachment',
            'intervention_id', string="Pièces jointes")
    creator_id = fields.Many2one('res.users', string="Créateur",
            default= lambda self: self.env.user.id,
            readonly=True, ondelete="cascade")
    member_id = fields.Many2one('gm_syndicat.member', string="Membre")

    @api.multi
    def close(self):
        """
            Use when closing a form for `self'
        """
        return {'type': 'ir.actions.act_window_close'}
