import click
from bmr.tg import BmrTg
import json
import csv
from ruamel.yaml import YAML
import sys

v = 'v0.0.1'

@click.group()
def main():
  pass

@main.command()
def version():
  global v
  click.echo('Version {0}'.format(v))

@main.command()
@click.option('--country', '-c', help = "A country code (e.g. 'FR'" )
@click.option('--name', '-n', help = "A talk group name or partial name.")
@click.option('--tgid', '-t', help = "A talk group ID.")
@click.option('--brandmeister-csv', '-b', default = 'TalkgroupsBrandMeister.csv', help = "Brandmeister CSV talkgroup file (defaults to 'TalkgroupsBrandMeister.csv')")
def find(brandmeister_csv, country, name, tgid):
  """Find talk groups in Brandmeister CSV export with search arguments"""
  tg = BmrTg()
  if brandmeister_csv:
    tg.readBmrCsvTGExport(brandmeister_csv)
  else:
    tg.readBmrCsvTGExport('TalkgroupsBrandMeister.csv')
  tg.showTalkGroups(country = country, name = name, tgId = tgid)

@main.command()
@click.option('--brandmeister-csv', '-b', default = 'TalkgroupsBrandMeister.csv', help = "Brandmeister CSV talkgroup file (defaults to 'TalkgroupsBrandMeister.csv')")
@click.option('--input-filters', '-i', help = "filter aggregation in a yaml file")
@click.argument('output', type=click.Path(exists=False), required = False)
@click.option('--filters', '-f', help = "Search filters (e.g. [{'country': 'fr'}, {'name': 'est'}])" )
def generate(brandmeister_csv, input_filters, output, filters = None):
  """
  Generate AT868/AT878 talk group CSV file
  
  If the output file is not specified, a file named
  'Anytone-TGs.csv' will be created by default.
  """
  cliFilters = []

  # These options are mutually exclusive
  if filters and input_filters:
    click.echo("Error: '--filters' and '--input-filters' are mutually exclusive.")
    sys.exit(-1)

  if not output:
    output = "Anytone-TGs.csv"

  # A json array containing filter dictionaries is used
  if filters:
    tmpFilters = filters.split(',')

    for talkGroupFilter in tmpFilters:
      talkGroupFilter = talkGroupFilter.strip()
      try:
        json.loads(talkGroupFilter)
      except Exception as  err:
        click.echo("Error: One or more filters are not formated as valid JSON")
        os._exit(1)

      validatedTalkGroupFilter = eval(talkGroupFilter)
      cliFilters.append(validatedTalkGroupFilter)
  else:
    cliFilters = None
  
  # A yaml file containing input filters is used
  if input_filters:
    with open(input_filters, 'r') as file:
      try:
        yaml=YAML(typ='safe', pure = True)
        cliFilters = yaml.load(file)
      except yaml.YAMLError as err:
        click.echo(err)

  tg = BmrTg()
  if brandmeister_csv:
    tg.readBmrCsvTGExport(brandmeister_csv)
  else:
    tg.readBmrCsvTGExport('TalkgroupsBrandMeister.csv')
  atList = tg.createAnyToneTgListForFilters(filters = cliFilters)
  
  keys = atList[0].keys()
  with open(output, 'w') as f:
    dictWriter = csv.DictWriter(f, keys)
    dictWriter.writeheader()
    dictWriter.writerows(atList)

@main.command()
@click.argument('output', type=click.Path(exists=False), required = False)
def users(output):
  """Download the DMR user database in CSV format"""
  defaultURL = 'https://radioid.net/static/user.csv'
  if not output:
    output = 'Users.csv'

  tg = BmrTg()
  click.echo("Downloding DMR users from radioid.net ...")
  tg.dmrUserList(defaultURL, output)
  click.echo("Done.")