import csv
from collections import OrderedDict
import unidecode
import urllib.request
import shutil

class BmrTg:
  tgList = []

  def readBmrCsvTGExport(self, file):
    """Reads a CSV file and creates a list od oredered dictionaries"""
    tmpList = list(csv.DictReader(open(file)))
    self.tgList = tmpList

  def showTalkGroups(self, country = None, name = None, tgId = None):
    """Prints a text table of talkgroups according to search parameters: country, name and tgId (talkgroup ID)"""
    tmpList = self.__findTalkGroups(country=country, name=name, tgId=tgId)
    self.__printHeader()
    self.__printTalkGroup(tmpList)

  def __printHeader(self):
    """Prints a text table header"""
    print(f'{"-"*8:<8}|{"-"*11:<11}|{"-"*30}' )
    print(f'{"Country":<8}| {"Talkgroup":^10}| {"Name"}')
    print(f'{"-"*51}')
  
  def __printFooter(self):
    """Prints a text table footer"""
    print(f'{"-"*51}')

  def __printTalkGroup(self, talkGroupList):
    """Prints a list of talkgroups formated as a text table"""
    for row in talkGroupList:
      print(f'{row["Country"]:<8}| {row["Talkgroup"]:^10}| {row["Name"]}')
    self.__printFooter()


  def __findTalkGroups(self, country = None, name = None, tgId = None):
    """
    Finds all talkgroups according to search parameters: country, name and tgId (talkgroup ID)
    """
    if country:
      # Case insensitive search
      country = country.lower()
      if name:
        # Case insensitive search
        name = name.lower()
        if tgId:
          tmpList = [row for row in self.tgList if (country == row['Country'].lower()) and (name in row['Name'].lower()) and (tgId == row['Talkgroup'])]
        else:
          tmpList = [row for row in self.tgList if (country == row['Country'].lower()) and (name in row['Name'].lower())]
      else:
        if tgId:
          tmpList =[row for row in self.tgList if (country == row['Country'].lower()) and (tgId == row['Talkgroup'])]
        else:
          tmpList =[row for row in self.tgList if country == row['Country'].lower()]
    else:
      if name:
        if tgId:
          tmpList = [row for row in self.tgList if (name in row['Name'].lower()) and (tgId == row['Talkgroup'])]
        else:
          tmpList = [row for row in self.tgList if name in row['Name'].lower()]
      else:
        if tgId:
          tmpList = [row for row in self.tgList if tgId == row['Talkgroup']]
        else:
          tmpList = self.tgList
    
    return tmpList

  def createAnyToneTgListForFilters(self, filters = []):
    """
    Formats talkgroup list ready to be writen to a CSV file (compatible with AnyTone radios)

    The filters argument is a dictionary of filters.

    A filter can have a maximum of 3 keys: 'country', 'name' and 'tgId' (talkgroup ID)
    """
    counter = 1
    resList = []
    if filters:
      for filter in filters:
        if 'country' in filter.keys():
          country = filter['country']
        else:
          country = None
        if 'name' in filter.keys():
          name = filter['name']
        else:
          name = None
        if 'tgId' in filter.keys():
          tgId = filter['tgId']
        else:
          tgId = None
          
        tmpList = self.__findTalkGroups(country=country, name=name, tgId=tgId)
        resList += tmpList
    else:
      resList = self.tgList

    # convert reslist (bmr) to AnyTone
    atList = []
    for row in resList:
      od = OrderedDict()
      od['No.'] = counter
      od['Radio ID'] = row['Talkgroup']
      od['Name'] = unidecode.unidecode(row['Name'])
      od['Call Type'] = "Group Call"
      od['Call Alert'] = "None"
      counter += 1
      atList.append(od)

    return atList

  def dmrUserList(self, url, outputFile):
    # Download the file from `url` and save it locally under `file_name`:
    with urllib.request.urlopen(url) as response, open(outputFile, 'wb') as out_file:
      shutil.copyfileobj(response, out_file)