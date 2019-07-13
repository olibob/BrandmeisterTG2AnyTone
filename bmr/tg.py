import csv

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
          [row for row in self.tgList if (country == row['Country'].lower()) and (tgId == row['Talkgroup'])]
        else:
          [row for row in self.tgList if country == row['Country'].lower()]
    else:
      if name:
        if tgId:
          tmpList = [row for row in self.tgList if (name in row['Name'].lower()) and (tgId == row['Talkgroup'])]
        else:
          tmpList = [row for row in self.tgList if name in row['Name'].lower()]
      else:
        tmpList = self.tgList
    
    return tmpList