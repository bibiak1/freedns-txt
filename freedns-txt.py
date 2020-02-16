#!/usr/bin/env python3
#author: marcin@biczan.pl

# default variables - you can edit it if you want
_site_url = ('https://freedns.42.pl')
_user = ''
_pass = ''
_zone = ''

# do not touch starting now
from urllib.request import urlopen
from lxml.html import parse, tostring, submit_form
from optparse import OptionParser
import sys

parser = OptionParser()
parser.add_option('-d', '--delete', action='store_true', dest='delete', default=False)
parser.add_option('-a', '--add', action='store_true', dest='add', default=False)
parser.add_option('-f', '--field', action='store', dest='field', default='_acme-challenge')
parser.add_option('-v', '--value', action='store', type='string', dest='value', default='')
parser.add_option('-U', '--user', action='store', type='string', dest='user', default=_user)
parser.add_option('-P', '--pass', action='store', type='string', dest='password', default=_pass)
parser.add_option('-Z', '--zone', action='store', type='string', dest='zone', default=_zone)

(options, args) = parser.parse_args()

if not len(options.user) or not len(options.password) or not len(options.zone):
    sys.exit()

if not options.delete and not options.add:
    sys.exit()

# get root page
try:
    page = parse(_site_url).getroot()
except IOError:
    page = parse(urlopen(_site_url)).getroot()

# login
page.forms[0].fields['login'] = options.user
page.forms[0].fields['password'] = options.password
page = parse(submit_form(page.forms[0])).getroot()

# get zone page
page.make_links_absolute(page.base_url)
find = page.xpath('//table["zonelisttable"]//a[contains(@href, "zones.php") and contains(@href, "%s")]' % (options.zone))
if len(find) != 1:
     print("zone %s not found!" % (options.zone))
     sys.exit()

mylink = find[0].attrib['href'].replace('zones.php', 'modify.php')
try:
    page = parse(mylink).getroot()
except IOError:
    page = parse(urlopen(mylink)).getroot()

# do the job
if options.add:
    tr = page.xpath('//td[text()="%s"]' % (options.field))
    if tr and len(tr) == 1:
        field = tr[0].getparent().xpath('td/input')[0]
        page.forms[0].inputs[field.name].checked = True
    page.forms[0].fields['txt1'] = options.field
    page.forms[0].fields['txtstring1'] = options.value
    page.forms[0].fields['txtttl1'] = '1'
    page = parse(submit_form(page.forms[0])).getroot()
    #print(tostring(page.xpath('//div["mainbox_content"]')[0]))
    print("add :: done")

elif options.delete:
    tr = page.xpath('//td[text()="%s"]' % (options.field))
    if tr and len(tr) == 1:
        field = tr[0].getparent().xpath('td/input')[0]
        page.forms[0].inputs[field.name].checked = True
        page = parse(submit_form(page.forms[0])).getroot()
	#print(tostring(page.xpath('//div["mainbox_content"]')[0]))
    print("delete :: done")
