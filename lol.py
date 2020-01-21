import requests, bs4, sys, re

LEAGUESPY_URL = 'https://www.leaguespy.gg/league-of-legends/champion/'
MOBAFIRE_URL = 'https://mobafire.com'
RUNES_TITLE_SELECTOR = '.new-runes__title'
PRIMARY_RUNES_SELECTOR = '.new-runes__primary .new-runes__item'
SECONDARY_RUNES_SELECTOR = '.new-runes__secondary .new-runes__item'
BONUSES_SELECTOR = '.new-runes__bonuses'
SPELLS_SELECTOR = '.view-guide__spells__row'
ITEMS_SELECTOR = '.view-guide__build[style="display: block;"] .view-guide__items'
GUIDE_SEPARATOR = '\n' + '*'*50 + '\n'
SECTION_SEPARATOR = '\n' + '-'*30 + '\n'

# get champion input
champion = input('Enter champion name: ')

# make request for leaguespy
spyRes = requests.get(LEAGUESPY_URL + champion + '/stats')
try:
    spyRes.raise_for_status()
except:
    print('Page not found. Make sure champion name is typed correctly.')
    sys.exit()

# get mobafire link
spySoup = bs4.BeautifulSoup(spyRes.text, 'html.parser')
mobafireButton = spySoup.select('.champ__header__left__main a')[0]
mobafireLink = mobafireButton.attrs['href']

# make request for mobafire
mobaRes = requests.get(mobafireLink)
try:
    mobaRes.raise_for_status()
except:
    print('Page not found. Mobafire link invalid.')
    sys.exit()

# get link to first guide
mobaSoup = bs4.BeautifulSoup(mobaRes.text, 'html.parser')
guides = mobaSoup.select('.browse-list a')
guide1Link = MOBAFIRE_URL + guides[0].attrs['href']

# make request for first guide
guide1Res = requests.get(guide1Link)
try:
    guide1Res.raise_for_status()
except:
    print('Page not found. Mobafire guide 1 link invalid.')
    sys.exit()

guide1Soup = bs4.BeautifulSoup(guide1Res.text, 'html.parser')

# get first guide runes
guide1Runes = ''

guide1RunesPrimaryTitle = guide1Soup.select(RUNES_TITLE_SELECTOR)[0].text
guide1Runes += guide1RunesPrimaryTitle + ': '

guide1RunesPrimary = guide1Soup.select(PRIMARY_RUNES_SELECTOR)
for rune in guide1RunesPrimary[1:5]:
    guide1Runes += rune.span.text + ', '
    
guide1Runes += '\n'

guide1RunesSecondaryTitle = guide1Soup.select(RUNES_TITLE_SELECTOR)[1].text
guide1Runes += guide1RunesSecondaryTitle + ': '

guide1RunesSecondary = guide1Soup.select(SECONDARY_RUNES_SELECTOR)
for rune in guide1RunesSecondary[1:3]:
    guide1Runes += rune.span.text + ', '
    
guide1Runes += '\n\n'

guide1RunesBonusesSection = guide1Soup.select(BONUSES_SELECTOR)[0].p.text
pattern = re.compile("\n\t+")
m = re.split(pattern, guide1RunesBonusesSection)
guide1RunesBonuses = ''
for s in m:
    if len(s) > 0:
        guide1RunesBonuses += s.strip() + '\n'
guide1Runes += guide1RunesBonuses

# get first guide spells
guide1Spells = guide1Soup.select(SPELLS_SELECTOR)[0].h4.text + ' ' + guide1Soup.select(SPELLS_SELECTOR)[1].h4.text

# get first guide items
guide1Build = guide1Soup.select(ITEMS_SELECTOR)
guide1Items = ''
for block in guide1Build:
    group = block.find_all("span", attrs={"class": None})
    guide1Items += group[0].text + ': '
    for items in group[1:]:
        guide1Items += items.text + ', '
    guide1Items += '\n'
    
# get first guide abilities
ABILITIES_SELECTOR = '.champ-build__abilities__row'

guide1Abilities = ''

q = [str(x)+'' for x in range(1,19)]
w = [str(x)+'' for x in range(1,19)]
e = [str(x)+'' for x in range(1,19)]
r = [str(x)+'' for x in range(1,19)]

guide1AbilityRows = guide1Soup.find_all(level=True)
for i in range(len(guide1AbilityRows[:18])):
    if 'class' not in guide1AbilityRows[:18][i].attrs:
        q[i] = ' '
for i in range(len(guide1AbilityRows[18:36])):
    if 'class' not in guide1AbilityRows[18:36][i].attrs:
        w[i] = ' '
for i in range(len(guide1AbilityRows[36:54])):
    if 'class' not in guide1AbilityRows[36:54][i].attrs:
        e[i] = ' '
for i in range(len(guide1AbilityRows[54:72])):
    if 'class' not in guide1AbilityRows[54:72][i].attrs:
        r[i] = ' '

guide1Abilities += 'q: ' + str(q) + '\nw: ' + str(w) + '\ne: ' + str(e) + '\nr: ' + str(r)

# get link to second guide
guide2Link = MOBAFIRE_URL + guides[1].attrs['href']

# make request for second guide
guide2Res = requests.get(guide2Link)
try:
    guide2Res.raise_for_status()
except:
    print('Page not found. Mobafire guide 2 link invalid.')
    sys.exit()

guide2Soup = bs4.BeautifulSoup(guide2Res.text, 'html.parser')

# get second guide runes
guide2Runes = ''

guide2RunesPrimaryTitle = guide2Soup.select(RUNES_TITLE_SELECTOR)[0].text
guide2Runes += guide2RunesPrimaryTitle + ': '

guide2RunesPrimary = guide2Soup.select(PRIMARY_RUNES_SELECTOR)
for rune in guide2RunesPrimary[1:5]:
    guide2Runes += rune.span.text + ', '
    
guide2Runes += '\n'

guide2RunesSecondaryTitle = guide2Soup.select(RUNES_TITLE_SELECTOR)[1].text
guide2Runes += guide2RunesSecondaryTitle + ': '

guide2RunesSecondary = guide2Soup.select(SECONDARY_RUNES_SELECTOR)
for rune in guide2RunesSecondary[1:3]:
    guide2Runes += rune.span.text + ', '
    
guide2Runes += '\n\n'

guide2RunesBonusesSection = guide2Soup.select(BONUSES_SELECTOR)[0].p.text
pattern = re.compile("\n\t+")
m = re.split(pattern, guide2RunesBonusesSection)
guide2RunesBonuses = ''
for s in m:
    if len(s) > 0:
        guide2RunesBonuses += s.strip() + '\n'
guide2Runes += guide2RunesBonuses

# get second guide spells
guide2Spells = guide2Soup.select(SPELLS_SELECTOR)[0].h4.text + ' ' + guide2Soup.select(SPELLS_SELECTOR)[1].h4.text

# get second guide items
guide2Build = guide2Soup.select(ITEMS_SELECTOR)
guide2Items = ''
for block in guide2Build:
    group = block.find_all("span", attrs={"class": None})
    guide2Items += group[0].text + ': '
    for items in group[1:]:
        guide2Items += items.text + ', '
    guide2Items += '\n'
    
# get second guide abilities
guide2Abilities = ''

q = [str(x)+'' for x in range(1,19)]
w = [str(x)+'' for x in range(1,19)]
e = [str(x)+'' for x in range(1,19)]
r = [str(x)+'' for x in range(1,19)]

guide2AbilityRows = guide2Soup.find_all(level=True)
for i in range(len(guide2AbilityRows[:18])):
    if 'class' not in guide2AbilityRows[:18][i].attrs:
        q[i] = ' '
for i in range(len(guide2AbilityRows[18:36])):
    if 'class' not in guide2AbilityRows[18:36][i].attrs:
        w[i] = ' '
for i in range(len(guide2AbilityRows[36:54])):
    if 'class' not in guide2AbilityRows[36:54][i].attrs:
        e[i] = ' '
for i in range(len(guide2AbilityRows[54:72])):
    if 'class' not in guide2AbilityRows[54:72][i].attrs:
        r[i] = ' '

guide2Abilities += 'q: ' + str(q) + '\nw: ' + str(w) + '\ne: ' + str(e) + '\nr: ' + str(r)

# get link to third guide
guide3Link = MOBAFIRE_URL + guides[2].attrs['href']

# make request for third guide
guide3Res = requests.get(guide3Link)
try:
    guide3Res.raise_for_status()
except:
    print('Page not found. Mobafire guide 3 link invalid.')
    sys.exit()

guide3Soup = bs4.BeautifulSoup(guide3Res.text, 'html.parser')

# get third guide runes
guide3Runes = ''

guide3RunesPrimaryTitle = guide3Soup.select(RUNES_TITLE_SELECTOR)[0].text
guide3Runes += guide3RunesPrimaryTitle + ': '

guide3RunesPrimary = guide3Soup.select(PRIMARY_RUNES_SELECTOR)
for rune in guide3RunesPrimary[1:5]:
    guide3Runes += rune.span.text + ', '
    
guide3Runes += '\n'

guide3RunesSecondaryTitle = guide3Soup.select(RUNES_TITLE_SELECTOR)[1].text
guide3Runes += guide3RunesSecondaryTitle + ': '

guide3RunesSecondary = guide3Soup.select(SECONDARY_RUNES_SELECTOR)
for rune in guide3RunesSecondary[1:3]:
    guide3Runes += rune.span.text + ', '
    
guide3Runes += '\n\n'

guide3RunesBonusesSection = guide3Soup.select(BONUSES_SELECTOR)[0].p.text
pattern = re.compile("\n\t+")
m = re.split(pattern, guide3RunesBonusesSection)
guide3RunesBonuses = ''
for s in m:
    if len(s) > 0:
        guide3RunesBonuses += s.strip() + '\n'
guide3Runes += guide3RunesBonuses

# get third guide spells
guide3Spells = guide3Soup.select(SPELLS_SELECTOR)[0].h4.text + ' ' + guide3Soup.select(SPELLS_SELECTOR)[1].h4.text

# get third guide items
guide3Build = guide3Soup.select(ITEMS_SELECTOR)
guide3Items = ''
for block in guide3Build:
    group = block.find_all("span", attrs={"class": None})
    guide3Items += group[0].text + ': '
    for items in group[1:]:
        guide3Items += items.text + ', '
    guide3Items += '\n'
    
# get third guide abilities
guide3Abilities = ''

q = [str(x)+'' for x in range(1,19)]
w = [str(x)+'' for x in range(1,19)]
e = [str(x)+'' for x in range(1,19)]
r = [str(x)+'' for x in range(1,19)]

guide3AbilityRows = guide3Soup.find_all(level=True)
for i in range(len(guide3AbilityRows[:18])):
    if 'class' not in guide3AbilityRows[:18][i].attrs:
        q[i] = ' '
for i in range(len(guide3AbilityRows[18:36])):
    if 'class' not in guide3AbilityRows[18:36][i].attrs:
        w[i] = ' '
for i in range(len(guide3AbilityRows[36:54])):
    if 'class' not in guide3AbilityRows[36:54][i].attrs:
        e[i] = ' '
for i in range(len(guide3AbilityRows[54:72])):
    if 'class' not in guide3AbilityRows[54:72][i].attrs:
        r[i] = ' '

guide3Abilities += 'q: ' + str(q) + '\nw: ' + str(w) + '\ne: ' + str(e) + '\nr: ' + str(r)


# prepare and print output
output = GUIDE_SEPARATOR + guide1Runes + SECTION_SEPARATOR + guide1Spells + SECTION_SEPARATOR + guide1Items + SECTION_SEPARATOR + guide1Abilities + GUIDE_SEPARATOR + guide2Runes + SECTION_SEPARATOR + guide2Spells + SECTION_SEPARATOR + guide2Items + SECTION_SEPARATOR + guide2Abilities + GUIDE_SEPARATOR + guide3Runes + SECTION_SEPARATOR + guide3Spells + SECTION_SEPARATOR + guide3Items + SECTION_SEPARATOR + guide3Abilities + GUIDE_SEPARATOR
print(output)