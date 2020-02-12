import requests, bs4, sys, time, platform, webbrowser
from guidescrape import scrapeGuide1, scrapeGuide2, scrapeGuide3

MOBAFIRE_URL = 'https://mobafire.com'
    
# process command line arguments
timeFlag = False
if len(sys.argv) > 2:
    if sys.argv[1] == '-t':
        timeFlag = True
        startTime = time.time()
    else:
        print('Invalid command line arguments')
        sys.exit()
champion = sys.argv[-1]

# handle champions with space-separated names, common alternative names, or potential misspellings
champions = dict.fromkeys(['sol', 'aurelionsol'], 'aurelion-sol')
champions.update(dict.fromkeys(['blitz'], 'blitzcrank'))
champions.update(dict.fromkeys(['cait'], 'caitlyn'))
champions.update(dict.fromkeys(['cass'], 'cassiopeia'))
champions.update(dict.fromkeys(['gath', 'cho-gath'], 'chogath'))
champions.update(dict.fromkeys(['mundo', 'drmundo'], 'dr-mundo'))
champions.update(dict.fromkeys(['eve'], 'evelynn'))
champions.update(dict.fromkeys(['ez'], 'ezreal'))
champions.update(dict.fromkeys(['fiddle'], 'fiddlesticks'))
champions.update(dict.fromkeys(['gp'], 'gangplank'))
champions.update(dict.fromkeys(['hec'], 'hecarim'))
champions.update(dict.fromkeys(['heim'], 'heimerdinger'))
champions.update(dict.fromkeys(['jarvan', 'iv'], 'jarvan-iv'))
champions.update(dict.fromkeys(['sa', 'kai-sa'], 'kaisa'))
champions.update(dict.fromkeys(['kass'], 'kassadin'))
champions.update(dict.fromkeys(['kat'], 'katarina'))
champions.update(dict.fromkeys(['zix', 'kha-zix'], 'khazix'))
champions.update(dict.fromkeys(['maw', 'kog', 'kog-maw'], 'kogmaw'))
champions.update(dict.fromkeys(['blanc', 'le-blanc'], 'leblanc'))
champions.update(dict.fromkeys(['lee', 'sin', 'leesin'], 'lee-sin'))
champions.update(dict.fromkeys(['liss'], 'lissandra'))
champions.update(dict.fromkeys(['malz'], 'malzahar'))
champions.update(dict.fromkeys(['yi', 'masteryi'], 'master-yi'))
champions.update(dict.fromkeys(['fortune', 'missfortune'], 'miss-fortune'))
champions.update(dict.fromkeys(['mord', 'morde'], 'mordekaiser'))
champions.update(dict.fromkeys(['morg'], 'morgana'))
champions.update(dict.fromkeys(['naut'], 'nautilus'))
champions.update(dict.fromkeys(['nid'], 'nidalee'))
champions.update(dict.fromkeys(['noc', 'noct'], 'nocturne'))
champions.update(dict.fromkeys(['nunu', 'willump', 'nunu-and-willump'], 'nunu-amp-willump'))
champions.update(dict.fromkeys(['ori'], 'orianna'))
champions.update(dict.fromkeys(['panth'], 'pantheon'))
champions.update(dict.fromkeys(['sai', 'rek-sai'], 'reksai'))
champions.update(dict.fromkeys(['renek'], 'renekton'))
champions.update(dict.fromkeys(['sej'], 'sejuani'))
champions.update(dict.fromkeys(['shyv'], 'shyvana'))
champions.update(dict.fromkeys(['raka'], 'soraka'))
champions.update(dict.fromkeys(['kench', 'tahmkench'], 'tahm-kench'))
champions.update(dict.fromkeys(['trist'], 'tristana'))
champions.update(dict.fromkeys(['tryn', 'trynd'], 'tryndamere'))
champions.update(dict.fromkeys(['tf', 'fate', 'twistedfate'], 'twisted-fate'))
champions.update(dict.fromkeys(['koz', 'vel-koz'], 'velkoz'))
champions.update(dict.fromkeys(['vlad'], 'vladimir'))
champions.update(dict.fromkeys(['voli'], 'volibear'))
champions.update(dict.fromkeys(['ww'], 'warwick'))
champions.update(dict.fromkeys(['wuk', 'wu-kong', 'kong'], 'wukong'))
champions.update(dict.fromkeys(['zhao', 'xinzhao', 'xin'], 'xin-zhao'))
champions.update(dict.fromkeys(['yas'], 'yasuo'))
champions.update(dict.fromkeys(['zil'], 'zilean'))

if champion in champions:
    champion = champions[champion]

# make request for mobafire
mobafireLink = MOBAFIRE_URL + '/league-of-legends/' + champion + '-guide'
mobaRes = requests.get(mobafireLink)
try:
    mobaRes.raise_for_status()
except:
    print('Page not found. Mobafire link invalid.')
    sys.exit()

mobaSoup = bs4.BeautifulSoup(mobaRes.text, 'html.parser')
guides = mobaSoup.select('.browse-list a')

# get link to top 3 guides
guide1Link = MOBAFIRE_URL + guides[0].attrs['href']
guide2Link = MOBAFIRE_URL + guides[1].attrs['href']
guide3Link = MOBAFIRE_URL + guides[2].attrs['href']

results = ['', '', '']
scrapeGuide1(guide1Link, results)
scrapeGuide2(guide2Link, results)
scrapeGuide3(guide3Link, results)

htmlFile = open('lol.html', 'w')
guide1 = '<br>'.join(results[0].split('\n'))
guide2 = '<br>'.join(results[0].split('\n'))
guide3 = '<br>'.join(results[0].split('\n'))
html = '<html><head><title>{} guides</title><style>body{{font-family:monospace;}}</style></head><body><h1>{}</h1><p>{}</p><h1>{}</h1><p>{}</p><h1>{}</h1><p>{}</p></body></html>'.format(champion, 'Guide 1', guide1, 'Guide 2', guide2, 'Guide 3', guide3)
htmlFile.write(html)
htmlFile.close()
webbrowser.open('lol.html')

endTime = time.time()

if timeFlag:
    timeFile = open('times.txt', 'a')
    timeFile.write(platform.system() + ' (serial)')
    timeFile.write('\n')
    timeFile.write(str(endTime-startTime))
    timeFile.write('\n')
    import time_analysis
