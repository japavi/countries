#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import sys
import re

import webapp2
import jinja2
import logging

import urllib
import urllib2
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'babel.zip'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pytz.zip'))

from webapp2_extras import i18n



def is_list(value):
    return isinstance(value, list)

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(extensions=['jinja2.ext.i18n', 'jinja2.ext.autoescape'], loader = jinja2.FileSystemLoader(template_dir), autoescape = True)
jinja_env.globals['is_list'] = is_list

jinja_env.install_gettext_translations(i18n)

def render_str(template, **params):
    
    t = jinja_env.get_template(template)
    return t.render(params)

AVAILABLE_LOCALES = ['en_US', 'es_ES']

class BaseHandler(webapp2.RequestHandler):

    def __init__(self, request, response):
        """ Override the initialiser in order to set the language.
        """
        self.initialize(request, response)

        self.available_locales = AVAILABLE_LOCALES

        # first, try and set locale from cookie
        locale = request.cookies.get('locale')
        self.locale = locale
        logging.error('en init locale-->%s' % locale)
        if locale in AVAILABLE_LOCALES:
            i18n.get_i18n().set_locale(locale)
        else:
            # if that failed, try and set locale from accept language header
            header = request.headers.get('Accept-Language', '')  # e.g. en-gb,en;q=0.8,es-es;q=0.5,eu;q=0.3
            locales = [locale.split(';')[0] for locale in header.split(',')]
            for locale in locales:
                if locale in AVAILABLE_LOCALES:
                    i18n.get_i18n().set_locale(locale)
                    break
            else:
                # if still no locale set, use the first available one
                i18n.get_i18n().set_locale(AVAILABLE_LOCALES[0])
    
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class All(BaseHandler):
    def get(self):

        url = 'https://restcountries.p.mashape.com/all'

        rest_call(self, url)  

def rest_call(self, url, **params):

    logging.error(url)

    key_out = ''
    value_out = ''

    for key in params.keys():
        logging.error("the key name is " + key + " and its value is " + params[key])
        key_out = key
        value_out = params[key]

    logging.error('key_out-->%s' % key_out)
    logging.error('value_out-->%s' % value_out)

    req = urllib2.Request(url)
    req.add_header('X-Mashape-Key', 'XRJ9snUjSjmshv9EOw2kG4yLy4lNp1uCWMcjsnzFpc0b660Uj5')
    req.add_header('Accept', 'application/json')
    try:
        resp = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        if e.code == 404:
            #logging.error('No se encontraron resultados para la %s %s' % params.keys()[0], params[params.keys()[0]]
            error_pais = 'No se encontraron resultados para la %s : %s' % (key_out, value_out)
            self.render('render-countries.html', error_pais = error_pais)

        else:
            logging.error('Hubo algun error al obtener resultados para la %s : %s' % (key_out, value_out))

    except urllib2.URLError as e:
        logging.error('Hubo algun error al obtener resultados para la %s : %s. El error es: %s' % (key_out, value_out, e))

    else:
        content = resp.read()

        #encoded
        data_string = json.dumps(json.JSONDecoder().decode(content))

        #logging.error('type of data_string %s' % type(data_string))

        #Decoded
        decoded = json.loads(data_string)
        logging.error('decoded[0]--> %s' % decoded[0])
        final_list = []
        #l = decoded[0].items()
        criteria = ['name', 'capital', 'currency', 'population', 'gini', 'languages', 'alpha3Code', 'translations', 'region', 'relevance', 'altSpellings', 'subregion', 'callingcode', 
            'nationality', 'isoNumericCode', 'latlng', 'area', 'timezones', 'topLevelDomain', 'alpha2Code']

        for pais in decoded:
            lista_data = pais.items()
            lista_data.sort(key = lambda x: criteria.index(x[0]))
            final_list.append(lista_data)

        logging.error(final_list)

        self.render('render-countries.html', contenido = final_list)


class Init(BaseHandler):
    def get(self):
        #locale = self.request.GET.get('locale', 'en_US')
        i18n.get_i18n().set_locale(self.locale)
        self.render('index.html')

class Capital(BaseHandler):
    def post(self):
        capital = self.request.get('capital')
        url = 'https://restcountries.p.mashape.com/capital/%s' % capital

        rest_call(self, url, capital=capital)   

class Name(BaseHandler):
    def post(self):
        name = self.request.get('name')
        url = 'https://restcountries.p.mashape.com/name/%s' % name

        rest_call(self, url, name=name)                


class Index(BaseHandler):
    """ Set the language cookie (if locale is valid), then redirect back to referrer
    """
    def get(self):
        locale = self.request.get('locale')
        logging.error('locale-->%s' % locale)
        if locale in self.available_locales:
            self.response.set_cookie('locale', locale, max_age = 15724800)  # 26 weeks' worth of seconds

        # redirect to referrer or root
        url = self.request.headers.get('Referer', '/')
        self.redirect(url)

app = webapp2.WSGIApplication([
    ('/', Init),
    ('/capital', Capital),
    ('/name', Name),
    ('/lang', Index),
    ('/all', All)], debug=True)
