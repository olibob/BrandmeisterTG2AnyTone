import bmr.tg

tg = bmr.tg.BmrTg()
tg.readBmrCsvTGExport("TalkgroupsBrandMeister.csv")
# Show all talk groups
# tg.showTalkGroups()

# Show talk group for country code 'fr'
# tg.showTalkGroups(country="fr")

# Show talk group for country code 'fr' and names containing 'est'
tg.showTalkGroups(country="fr", name="est")

# Show talk group for country code 'global', with name 'parrot' with talk group id 9990
# tg.showTalkGroups(country="global", name="parrot", tgId="9990")

# Show talk group with id 9990
# tg.showTalkGroups(tgId="9990")

# Show all talk groups
# tg.showTalkGroups()

# create an AnyTone talk group CSV file for the 'de' country code (Germany)
# tg.createAnyToneCVSForFilter(filters=[{"country": "de"}])

# create an AnyTone talk group CSV file for:
# - the 'fr' country code (France)
# - the 'de' counbtry code (Germany)
# - the talk group id 927
# - the country code 'global', with names containing 'parrot' with talk group id 9990 (specifically the global parrot talk group)
# tg.createAnyToneCVSForFilter([{"country": "fr"}, {"country": "de"}, {"tgId": "927"}, {"country": "global", "name": "parrot", "tgId": "9990"}])
