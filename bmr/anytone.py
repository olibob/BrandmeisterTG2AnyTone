import click
from bmr.tg import BmrTg

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
def find(country, name, tgid):
  """Find talk groups in Brandmeister CSV export with search arguments"""
  # !Bug: a search with Ré fails
  # TODO: create tg and read TG file in main, use context to transfer object
  tg = BmrTg()
  tg.readBmrCsvTGExport("TalkgroupsBrandMeister.csv")
  tg.showTalkGroups(country = country, name = name, tgId = tgid)

@main.command()
@click.argument('output', type = click.File('w'), default = 'Anytone-TGs.csv', required = False)
@click.option('--filters', '-f', help = "Search filters (e.g. [{'country': 'fr'}, {'name': 'est'}])" )
def create(output, filters):
  """
  Create AT868/AT878 talk group CSV file
  
  If the output file is not specified, a file named
  'Anytone-TGs.csv' will be created by default.
  """
  # TODO 
  pass