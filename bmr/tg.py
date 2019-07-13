import csv
from collections import OrderedDict
import unidecode

class BmrTg:
  tgList = []

  def readBmrCsvTGExport(self, file):
    tmpList = list(csv.DictReader(open('TalkgroupsBrandMeister.csv')))
    self.tgList = tmpList

  def showTalkGroups(self, country = None, name = None, tgId = None):
    tmpList = self.__findTalkGroups(country=country, name=name, tgId=tgId)
    self.__printHeader()
    self.__printTalkGroup(tmpList)

  def __printHeader(self):
    print(f'{"-"*8:<8}|{"-"*11:<11}|{"-"*30}' )
    print(f'{"Country":<8}| {"Talkgroup":^10}| {"Name"}')
    print(f'{"-"*51}')
  
  def __printFooter(self):
    print(f'{"-"*51}')

  def __printTalkGroup(self, talkGroupList):
    for row in talkGroupList:
      print(f'{row["Country"]:<8}| {row["Talkgroup"]:^10}| {row["Name"]}')
    self.__printFooter()


  def __findTalkGroups(self, country = None, name = None, tgId = None):
    if country:
      if name:
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

  def createAnyToneCsvTgForFilters(self, filters = []):
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

    # self.__printTalkGroup(resList)
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

    keys = atList[0].keys()
    with open('AnyTone-Talk-Groups.csv', 'w') as outputFile:
      dictWriter = csv.DictWriter(outputFile, keys)
      dictWriter.writeheader()
      dictWriter.writerows(atList)
