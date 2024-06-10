# -*- coding: utf-8 -*-
from odoo import api, fields, models
import requests

class Apartment(models.Model):
    _name = 'real.estate.apartment'
    _description = 'Apartment'

    name = fields.Char(string='აპარტმენტის აღწერა',)
    square_meter = fields.Float(string='კვადრატობა',max_digits=4, decimal_places=2)
    location = fields.Char(string='ზუსტი მისამრთი')
    location_tags = fields.Many2many('real.estate.location.tag', string='ლოკაციის მინიშნებები')
    price = fields.Char(string='ფასი', required=True)
    rooms = fields.Integer(string='ოთახები')
    comment = fields.Text()
    badrooms = fields.Integer(string='ოთახები')
    available = fields.Boolean(string='ხელმისაწვდომია',default=True)
    possible_clients = fields.Many2many('real.estate.client', compute='_compute_possible_clients', string='პოტენციური კლიენტები')
    myhome_product_id = fields.Integer(string='Myhome ID')
    my_home_url = fields.Char(string='Myhome ID')
    my_my_home_id = fields.Integer(string='Myhome ID')
    floor = fields.Integer(string='Myhome ID')
    parking_id = fields.Integer(string='Myhome ID')
    canalization_id = fields.Integer(string='Myhome ID')



    
    @api.depends('square_meter', 'location_tags')
    def _compute_possible_clients(self):
        for apartment in self:
            domain = [
                ('preferred_apartments.square_preference', '>=', apartment.square_meter),
                ('preferred_apartments.location_tags', 'in', apartment.location_tags.ids)
            ]
            apartment.possible_clients = self.env['real.estate.client'].search(domain)

class Client(models.Model):
    _name = 'real.estate.client'
    _description = 'Client'

    name = fields.Char(string='კლიენტის სახელი', required=True)
    phone = fields.Char(string='კლიენტის ნომერი', required=True)
    preferred_apartments = fields.One2many('real.estate.preferredapartment', 'client_id', string='კლიენტის მოსაწონი აპარტმენტი')
    possible_apartments = fields.Many2many('real.estate.apartment', compute='_compute_possible_apartments', string='სავარაუდო აპარტმენტი')
    
    @api.depends('preferred_apartments.square_preference', 'preferred_apartments.location_tags')
    def _compute_possible_apartments(self):
        for client in self:
            apartments = self.env['real.estate.apartment'].search([])
            possible_apartments = apartments.filtered(lambda a: any(p.square_preference >= a.square_meter and 
                                                                     set(p.location_tags.ids).intersection(a.location_tags.ids) 
                                                                     for p in client.preferred_apartments))
            client.possible_apartments = possible_apartments

class PreferredApartment(models.Model):
    _name = 'real.estate.preferredapartment'
    _description = 'Preferred Apartment'

    client_id = fields.Many2one('real.estate.client', string='Client', ondelete='cascade')
    square_preference = fields.Float(string='მოსაწონი კვადრატულობა')
    # location_preference = fields.Char(string='Preferred Raw Location String')
    location_tags = fields.Many2many('real.estate.location.tag', string='მოსაწონი ლოკაციები')

class LocationTag(models.Model):
    _name = 'real.estate.location.tag'
    _description = 'Location Tag'

    name = fields.Char(string='ლოკაციის ტეგი', required=True)


class ApartmentLoadWizard(models.TransientModel):
    _name = 'import.from.myhome'

    def import_apartments(self):
        headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
                   "Accept":"application/json, text/javascript, */*; q=0.01",
                   "Cookie":"CookieAgreement=1; PHPSESSID=h83oqnek91vmal498odtr3iqt9; Lang=ka; split_test=v1",
                   "X-Requested-With":"XMLHttpRequest"
                   }
        for page in range(1,4):
            req_data=requests.get(f"https://www.myhome.ge/ka/s/?AdTypeID=3&Page={page}&Ajax=1",headers=headers)
            data = req_data.json()
            for i in data['Data']['Prs']:
                apartment_exists  = self.env['real.estate.apartment'].search([('myhome_product_id','=',int(i['product_id']))])

                if not apartment_exists:
                    apartment = self.env['real.estate.apartment'].create({
                    "name":i['comment'],
                    "square_meter":i['area_size_value'],
                    "price":i['price'],
                    # "rooms":i['rooms'],
                    # "badrooms":i["bedrooms"],
                    "comment":i['comment'],
                        
                        })





