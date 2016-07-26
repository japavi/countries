

Python 2.7
Jinja2
Babel

- Install Jinja2:

$ pip install jinja2

If there are problems installing Jinja2, downgrade setuptools:

$ pip install setuptools==21.2.1

- Install Babel:

$ pip install babel

download babel 1.3
$ wget https://github.com/mitsuhiko/babel/archive/1.3.zip

# unzip and enter babel source directory
$ unzip 1.3.zip
$ cd babel-1.3/

# create babel.zip for zipimport
$ zip -r babel.zip babel/*

# move babel.zip to your project root directory

Install pytz:

# download gaepytz 2011h
$ wget https://pypi.python.org/packages/source/g/gaepytz/gaepytz-2011h.tar.gz#md5=b7abe173cd98b417fab3e91c1498cdd2

# unzip and enter gaepytz source directory
$ tar xvzf gaepytz-2011h.tar.gz
$ cd gaepytz-2011h/

# create pytz.zip for zipimport
$ zip -r pytz.zip pytz/*

# move pytz.zip to your project root directory

babel.cfg (config for Babel extraction): This babel.cfg tells babel to extract all translations from all HTML files in your webapp and the encoding of HTML files are utf-8. 

Extract and compile translations

By default, webapp2 looks for pot and po files in locale directory under your project root directory, so first create a directory named locale:

# in your project root directory:
$ mkdir locale

Then extract all translations (create pot file):

# in your project root directory:
$ pybabel extract -F ./babel.cfg -o ./locale/messages.pot ./templates

#Then initialize the directory for each locale that your webapp will support:
$ pybabel init -l es_ES -d ./locale -i ./locale/messages.pot
$ pybabel init -l en_US -d ./locale -i ./locale/messages.pot

Translate only non-default-language po files:

====================================================
# Spanish (Spain) translations for PROJECT.
# Copyright (C) 2016 ORGANIZATION
# This file is distributed under the same license as the PROJECT project.
# FIRST AUTHOR <EMAIL@ADDRESS>, 2016.
#
msgid ""
msgstr ""
"Project-Id-Version: PROJECT VERSION\n"
"Report-Msgid-Bugs-To: EMAIL@ADDRESS\n"
"POT-Creation-Date: 2016-07-25 20:14+0100\n"
"PO-Revision-Date: 2016-07-25 20:14+0100\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language: es_ES\n"
"Language-Team: es_ES <LL@li.org>\n"
"Plural-Forms: nplurals=2; plural=(n != 1)\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=utf-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: Babel 2.3.4\n"

#: templates/base.html:19 templates/base.html:26 templates/index.html:5
msgid "searchcountries"
msgstr "Buscar Paìses"

#: templates/base.html:47
msgid "developedby"
msgstr "Desarrollado Por"
====================================================

After all translations done, compile po file with the following command:

# in your project root directory:
$ pybabel compile -f -d ./locale



