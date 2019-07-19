import click
from bmr.tg import BmrTg
import json

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
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path(exists=False), required = False)
@click.option('--filters', '-f', help = "Search filters (e.g. [{'country': 'fr'}, {'name': 'est'}])" )
def create(input, output, filters = None):
  """
  Create AT868/AT878 talk group CSV file
  
  If the output file is not specified, a file named
  'Anytone-TGs.csv' will be created by default.
  """
  cliFilters = []

  if not output:
    output = "Anytone-TGs.csv"

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

  tg = BmrTg()
  tg.readBmrCsvTGExport(input)
  tg.createAnyToneCsvTgForFilters(outputFile = output, filters = cliFilters)

@main.command()
@click.argument('output', type=click.Path(exists=False), required = False)
def users(output):
  defaultURL = 'https://radioid.net/static/user.csv'
  if not output:
    output = 'Users.csv'

  tg = BmrTg()
  click.echo("Downloding DMR users from radioid.net ...")
  tg.dmrUserList(defaultURL, output)
  click.echo("Done.")

