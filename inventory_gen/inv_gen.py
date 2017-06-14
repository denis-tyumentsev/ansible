#!/usr/bin/env python

# Ansible inventory files generator
# You will need to "sudo pip install jinja2" first!
# Python >=2.7
#
# Visit:
# http://jinja.pocoo.org/docs/templates/

import argparse
import xml.etree.ElementTree as ET
import jinja2
import re


def parse_xml(file):
  tree = ET.parse(file)
  servers = tree.getroot()

  out = {}
  for srv in servers:
    out[srv.tag] = {}

    for node in srv:
      out[srv.tag][node.tag] = node.text.lower()

  # FIXME: should be provided by Vlad
  out['system'] = {
    'name': re.findall('^vm-flow\.([a-zA-Z0-9\-]+)\.',
          out['FLOW']['Name'])[0].upper(),
    'domain': re.findall('([a-zA-Z0-9\-]+\.[a-zA-Z0-9\-]+)$',
          out['FLOW']['Name'])[0]
  }

  for srv in out:
    if 'Name' in out[srv]:
      out[srv]['_dns'] = re.sub('^vm-', '', out[srv]['Name'])

  return out


def render(vars, template_file, output_file):
  with open(template_file, 'r') as tfile:
    tpl = tfile.read()

  try:
    with open(output_file, 'w') as ofile:
      ofile.write(jinja2.Environment().from_string(tpl).render(vars))
  except jinja2.exceptions.UndefinedError as e:
    print('Jinja2 render error: %s' % e)
    print('Parsed vars:\n "%s"' % vars)
    raise e

  print('Successfuly rendered "%s"' % output_file)


parser = argparse.ArgumentParser(
        description='Ansible inventory files generator')
parser.add_argument('--input_file', help='input XML file', required=True)
parser.add_argument('--template_file', required=True,
        help='Jinja2 template file for XML input rendering')
parser.add_argument('--output_file', help='output file', required=True)

args = parser.parse_args()

print('Open "%s"' % args.input_file)
vars = parse_xml(args.input_file)
print('Successfuly loaded "%s"' % args.input_file)

render(vars, args.template_file, args.output_file)

print('Done!')
