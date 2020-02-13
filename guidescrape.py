import requests, bs4, sys, re

MOBAFIRE_URL = 'https://mobafire.com'
RUNE_IMAGES_SELECTOR = '.new-runes__item__circle img'
RUNES_TITLE_SELECTOR = '.new-runes__title'
PRIMARY_RUNES_SELECTOR = '.new-runes__primary .new-runes__item'
SECONDARY_RUNES_SELECTOR = '.new-runes__secondary .new-runes__item'
BONUSES_SELECTOR = '.new-runes__bonuses'
SPELL_IMAGES_SELECTOR = '.view-guide__spells__row img'
SPELLS_SELECTOR = '.view-guide__spells__row'
ITEMS_SELECTOR = '.view-guide__build[style="display: block;"] .view-guide__items'
ITEM_IMAGES_SELECTOR = '.view-guide__items__content img'
SECTION_SEPARATOR = '\n' + '-'*50
IMAGE_SIZE = '35px'

def scrapeGuide1(guide1Link, results):
    # make request for first guide
    guide1Res = requests.get(guide1Link)
    try:
        guide1Res.raise_for_status()
    except:
        print('Page not found. Mobafire guide 1 link invalid.')
        sys.exit()
        
    guide1Soup = bs4.BeautifulSoup(guide1Res.text, 'html.parser')

    # get first guide runes
    guide1RuneImages = guide1Soup.select(RUNE_IMAGES_SELECTOR)
    
    guide1Runes = ''
    
    guide1RuneImages[0].attrs['src'] = MOBAFIRE_URL + guide1RuneImages[0].attrs['src']
    guide1RuneImages[0].attrs['width'] = IMAGE_SIZE
    guide1RuneImages[0].attrs['height'] = IMAGE_SIZE

    guide1RunesPrimaryTitle = guide1Soup.select(RUNES_TITLE_SELECTOR)[0].text
    guide1Runes += str(guide1RuneImages[0]) + guide1RunesPrimaryTitle + ': '

    guide1RunesPrimary = guide1Soup.select(PRIMARY_RUNES_SELECTOR)
    for i, rune in enumerate(guide1RunesPrimary[1:5], start=1):
        guide1RuneImages[i].attrs['src'] = MOBAFIRE_URL + guide1RuneImages[i].attrs['src']
        guide1RuneImages[i].attrs['width'] = IMAGE_SIZE
        guide1RuneImages[i].attrs['height'] = IMAGE_SIZE
        guide1Runes += str(guide1RuneImages[i]) + rune.span.text + ', '

    guide1Runes += '\n'
    
    guide1RuneImages[5].attrs['src'] = MOBAFIRE_URL + guide1RuneImages[5].attrs['src']
    guide1RuneImages[5].attrs['width'] = IMAGE_SIZE
    guide1RuneImages[5].attrs['height'] = IMAGE_SIZE

    guide1RunesSecondaryTitle = guide1Soup.select(RUNES_TITLE_SELECTOR)[1].text
    guide1Runes += str(guide1RuneImages[5]) + guide1RunesSecondaryTitle + ': '

    guide1RunesSecondary = guide1Soup.select(SECONDARY_RUNES_SELECTOR)
    for j, rune in enumerate(guide1RunesSecondary[1:3], start=6):
        guide1RuneImages[j].attrs['src'] = MOBAFIRE_URL + guide1RuneImages[j].attrs['src']
        guide1RuneImages[j].attrs['width'] = IMAGE_SIZE
        guide1RuneImages[j].attrs['height'] = IMAGE_SIZE
        guide1Runes += str(guide1RuneImages[j]) + rune.span.text + ', '

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
    guide1SpellImages = guide1Soup.select(SPELL_IMAGES_SELECTOR)
    for i in range(2):
        guide1SpellImages[i].attrs['src'] = MOBAFIRE_URL + guide1SpellImages[i].attrs['src']
        guide1SpellImages[i].attrs['width'] = IMAGE_SIZE
        guide1SpellImages[i].attrs['height'] = IMAGE_SIZE
    
    guide1Spells = str(guide1SpellImages[0]) + guide1Soup.select(SPELLS_SELECTOR)[0].h4.text + ' '  + str(guide1SpellImages[1]) + guide1Soup.select(SPELLS_SELECTOR)[1].h4.text

    # get first guide items
    guide1Build = guide1Soup.select(ITEMS_SELECTOR)
    guide1ItemImages = guide1Soup.select(ITEM_IMAGES_SELECTOR)
    guide1Items = ''
    i = 0
    for block in guide1Build:
        text_group = block.find_all("span", attrs={"class": None})
        guide1Items += text_group[0].text.upper() + ': '
        for items in text_group[1:]:
            guide1ItemImages[i].attrs['src'] = MOBAFIRE_URL + guide1ItemImages[i].attrs['src']
            guide1ItemImages[i].attrs['width'] = IMAGE_SIZE
            guide1ItemImages[i].attrs['height'] = IMAGE_SIZE
            guide1Items += str(guide1ItemImages[i]) + items.text + ', '
            i += 1
        guide1Items += SECTION_SEPARATOR + '\n'

    # get first guide abilities
    ABILITIES_SELECTOR = '.champ-build__abilities__row'

    guide1Abilities = ''

    q = [str(x) for x in range(1,19)]
    w = [str(x) for x in range(1,19)]
    e = [str(x) for x in range(1,19)]
    r = [str(x) for x in range(1,19)]

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
    
    results[0] = guide1Runes + '\n\n' + guide1Spells + '\n\n' + guide1Items + '\n\n' + guide1Abilities
    
def scrapeGuide2(guide2Link, results):
    # make request for second guide
    guide2Res = requests.get(guide2Link)
    try:
        guide2Res.raise_for_status()
    except:
        print('Page not found. Mobafire guide 2 link invalid.')
        sys.exit()
        
    guide2Soup = bs4.BeautifulSoup(guide2Res.text, 'html.parser')

    # get second guide runes
    guide2RuneImages = guide2Soup.select(RUNE_IMAGES_SELECTOR)
    
    guide2Runes = ''
    
    guide2RuneImages[0].attrs['src'] = MOBAFIRE_URL + guide2RuneImages[0].attrs['src']
    guide2RuneImages[0].attrs['width'] = IMAGE_SIZE
    guide2RuneImages[0].attrs['height'] = IMAGE_SIZE

    guide2RunesPrimaryTitle = guide2Soup.select(RUNES_TITLE_SELECTOR)[0].text
    guide2Runes += str(guide2RuneImages[0]) + guide2RunesPrimaryTitle + ': '

    guide2RunesPrimary = guide2Soup.select(PRIMARY_RUNES_SELECTOR)
    for i, rune in enumerate(guide2RunesPrimary[1:5], start=1):
        guide2RuneImages[i].attrs['src'] = MOBAFIRE_URL + guide2RuneImages[i].attrs['src']
        guide2RuneImages[i].attrs['width'] = IMAGE_SIZE
        guide2RuneImages[i].attrs['height'] = IMAGE_SIZE
        guide2Runes += str(guide2RuneImages[i]) + rune.span.text + ', '

    guide2Runes += '\n'
    
    guide2RuneImages[5].attrs['src'] = MOBAFIRE_URL + guide2RuneImages[5].attrs['src']
    guide2RuneImages[5].attrs['width'] = IMAGE_SIZE
    guide2RuneImages[5].attrs['height'] = IMAGE_SIZE

    guide2RunesSecondaryTitle = guide2Soup.select(RUNES_TITLE_SELECTOR)[1].text
    guide2Runes += str(guide2RuneImages[5]) + guide2RunesSecondaryTitle + ': '

    guide2RunesSecondary = guide2Soup.select(SECONDARY_RUNES_SELECTOR)
    for j, rune in enumerate(guide2RunesSecondary[1:3], start=6):
        guide2RuneImages[j].attrs['src'] = MOBAFIRE_URL + guide2RuneImages[j].attrs['src']
        guide2RuneImages[j].attrs['width'] = IMAGE_SIZE
        guide2RuneImages[j].attrs['height'] = IMAGE_SIZE
        guide2Runes += str(guide2RuneImages[j]) + rune.span.text + ', '

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
    guide2SpellImages = guide2Soup.select(SPELL_IMAGES_SELECTOR)
    for i in range(2):
        guide2SpellImages[i].attrs['src'] = MOBAFIRE_URL + guide2SpellImages[i].attrs['src']
        guide2SpellImages[i].attrs['width'] = IMAGE_SIZE
        guide2SpellImages[i].attrs['height'] = IMAGE_SIZE
    guide2Spells = str(guide2SpellImages[0]) + guide2Soup.select(SPELLS_SELECTOR)[0].h4.text + ' ' + str(guide2SpellImages[1]) + guide2Soup.select(SPELLS_SELECTOR)[1].h4.text

    # get second guide items
    guide2Build = guide2Soup.select(ITEMS_SELECTOR)
    guide2ItemImages = guide2Soup.select(ITEM_IMAGES_SELECTOR)
    guide2Items = ''
    i = 0
    for block in guide2Build:
        text_group = block.find_all("span", attrs={"class": None})
        guide2Items += text_group[0].text.upper() + ': '
        for items in text_group[1:]:
            guide2ItemImages[i].attrs['src'] = MOBAFIRE_URL + guide2ItemImages[i].attrs['src']
            guide2ItemImages[i].attrs['width'] = IMAGE_SIZE
            guide2ItemImages[i].attrs['height'] = IMAGE_SIZE
            guide2Items += str(guide2ItemImages[i]) + items.text + ', '
            i += 1
        guide2Items += '\n'

    # get second guide abilities
    guide2Abilities = ''

    q = [str(x) for x in range(1,19)]
    w = [str(x) for x in range(1,19)]
    e = [str(x) for x in range(1,19)]
    r = [str(x) for x in range(1,19)]

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
    
    results[1] = guide2Runes + '\n\n' + guide2Spells + '\n\n' + guide2Items + '\n\n' + guide2Abilities
    
def scrapeGuide3(guide3Link, results):
    # make request for third guide
    guide3Res = requests.get(guide3Link)
    try:
        guide3Res.raise_for_status()
    except:
        print('Page not found. Mobafire guide 3 link invalid.')
        sys.exit()
        
    guide3Soup = bs4.BeautifulSoup(guide3Res.text, 'html.parser')

    # get third guide runes
    guide3RuneImages = guide3Soup.select(RUNE_IMAGES_SELECTOR)
    
    guide3Runes = ''
    
    guide3RuneImages[0].attrs['src'] = MOBAFIRE_URL + guide3RuneImages[0].attrs['src']
    guide3RuneImages[0].attrs['width'] = IMAGE_SIZE
    guide3RuneImages[0].attrs['height'] = IMAGE_SIZE

    guide3RunesPrimaryTitle = guide3Soup.select(RUNES_TITLE_SELECTOR)[0].text
    guide3Runes += str(guide3RuneImages[0]) + guide3RunesPrimaryTitle + ': '

    guide3RunesPrimary = guide3Soup.select(PRIMARY_RUNES_SELECTOR)
    for i, rune in enumerate(guide3RunesPrimary[1:5], start=1):
        guide3RuneImages[i].attrs['src'] = MOBAFIRE_URL + guide3RuneImages[i].attrs['src']
        guide3RuneImages[i].attrs['width'] = IMAGE_SIZE
        guide3RuneImages[i].attrs['height'] = IMAGE_SIZE
        guide3Runes += str(guide3RuneImages[i]) + rune.span.text + ', '

    guide3Runes += '\n'
    
    guide3RuneImages[5].attrs['src'] = MOBAFIRE_URL + guide3RuneImages[5].attrs['src']
    guide3RuneImages[5].attrs['width'] = IMAGE_SIZE
    guide3RuneImages[5].attrs['height'] = IMAGE_SIZE

    guide3RunesSecondaryTitle = guide3Soup.select(RUNES_TITLE_SELECTOR)[1].text
    guide3Runes += str(guide3RuneImages[5]) + guide3RunesSecondaryTitle + ': '

    guide3RunesSecondary = guide3Soup.select(SECONDARY_RUNES_SELECTOR)
    for j, rune in enumerate(guide3RunesSecondary[1:3], start=6):
        guide3RuneImages[j].attrs['src'] = MOBAFIRE_URL + guide3RuneImages[j].attrs['src']
        guide3RuneImages[j].attrs['width'] = IMAGE_SIZE
        guide3RuneImages[j].attrs['height'] = IMAGE_SIZE
        guide3Runes += str(guide3RuneImages[j]) + rune.span.text + ', '

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
    guide3SpellImages = guide3Soup.select(SPELL_IMAGES_SELECTOR)
    for i in range(2):
        guide3SpellImages[i].attrs['src'] = MOBAFIRE_URL + guide3SpellImages[i].attrs['src']
        guide3SpellImages[i].attrs['width'] = IMAGE_SIZE
        guide3SpellImages[i].attrs['height'] = IMAGE_SIZE
    guide3Spells = str(guide3SpellImages[0]) + guide3Soup.select(SPELLS_SELECTOR)[0].h4.text + ' ' + str(guide3SpellImages[1]) + guide3Soup.select(SPELLS_SELECTOR)[1].h4.text

    # get third guide items
    guide3Build = guide3Soup.select(ITEMS_SELECTOR)
    guide3ItemImages = guide3Soup.select(ITEM_IMAGES_SELECTOR)
    guide3Items = ''
    i = 0
    for block in guide3Build:
        text_group = block.find_all("span", attrs={"class": None})
        guide3Items += text_group[0].text + ': '
        for items in text_group[1:]:
            guide3ItemImages[i].attrs['src'] = MOBAFIRE_URL + guide3ItemImages[i].attrs['src']
            guide3ItemImages[i].attrs['width'] = IMAGE_SIZE
            guide3ItemImages[i].attrs['height'] = IMAGE_SIZE
            guide3Items += str(guide3ItemImages[i]) + items.text + ', '
            i += 1
        guide3Items += '\n'

    # get third guide abilities
    guide3Abilities = ''

    q = [str(x) for x in range(1,19)]
    w = [str(x) for x in range(1,19)]
    e = [str(x) for x in range(1,19)]
    r = [str(x) for x in range(1,19)]

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
    
    results[2] = guide3Runes + '\n\n' + guide3Spells + '\n\n' + guide3Items + '\n\n' + guide3Abilities