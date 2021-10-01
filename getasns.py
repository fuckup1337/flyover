import asyncio
import pyppeteer
import json
import argparse
import os

class m:
    INF = '[\033[94mINF\033[0m] '
    WRN = '[\033[93mWRN\033[0m] '
    ERR = '[\033[91mERR\033[0m] '

parser = argparse.ArgumentParser()
parser.add_argument('target', help='target')
parser.add_argument('-p', '--proxy', help='send traffic through a SOCKS5 proxy tunnel (ex. localhost:8089)')
args = parser.parse_args()

print('''
    ________
   / ____/ /_  ______ _   _____  _____
  / /_  / / / / / __ \ | / / _ \/ ___/
 / __/ / / /_/ / /_/ / |/ /  __/ /
/_/   /_/\__, /\____/|___/\___/_/
        /____/
''')

print('v1.0.0\n')

print(m.INF + 'Starting...')

async def main():
    print(m.INF + 'Launching spider...')

    if args.proxy:
        browserArgs = ['--proxy-server=socks5://' + args.proxy]
    else:
        browserArgs = []

    browser = await pyppeteer.launch({
        'args': browserArgs, 'headless': True
    })

    page = await browser.newPage()
    await page.goto('https://bgp.he.net/search?search%5Bsearch%5D=' + args.target.replace(' ', '+') + '&commit=Search')
    await page.waitForSelector('#search > table > tbody > tr:nth-child(1) > td:nth-child(1)')
    rows = await page.xpath('//*[@id="search"]/table/tbody/tr[td]')

    tableData = {}
    for row in rows:
        title, content = await page.evaluate('row => [...row.children].map(child => child.textContent)', row)

        if title.startswith('AS'):
            print('[\033[35m' + title + '\033[0m] ==> ' + content)
            tableData.update({ title: content })

    try:
        outputFile = './asns.json'
        if os.path.exists(outputFile):
            os.remove(outputFile)
    except OSError as err:
        print(m.ERR + err)

    try:
        file = open(outputFile, 'w')
        file.write(json.dumps(tableData, indent = 2))
        file.close()

        print(m.WRN + 'Saved data to ' + outputFile)
    except OSError as err:
        print(m.ERR + err)

    print(m.INF + 'Done. Squishing spider...')
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())