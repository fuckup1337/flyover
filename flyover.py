import asyncio
import pyppeteer
import json
import argparse
import os

class m:
    INF = '[\033[94mINF\033[0m] '
    WRN = '[\033[93mWRN\033[0m] '
    ERR = '[\033[91mERR\033[0m] '

class CustomFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return metavar
        else:
            parts = []
            if action.nargs == 0:
                parts.extend(action.option_strings)
            else:
                default = action.dest.upper()
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append('%s' % option_string)
                parts[-1] += ' %s'%args_string
            return ', '.join(parts)

parser = argparse.ArgumentParser(
    description='Scrapes bgp.he.net for ASN numbers related to a query',
    prog='python3 flyover.py',
    formatter_class=CustomFormatter
)

parser.add_argument('query', help='query to search bgp.he.net')
parser.add_argument('-o', '--output', help='output to JSON file', metavar='PATH')
parser.add_argument('-s', '--script', action='store_true', help='only output ASNs for easy scripting')
parser.add_argument('-p', '--proxy', help='send traffic through a SOCKS5 proxy tunnel', metavar='IP:PORT')

args = parser.parse_args()

if not args.script:
    print('''
    ________
   / ____/ /_  ______ _   _____  _____
  / /_  / / / / / __ \ | / / _ \/ ___/
 / __/ / / /_/ / /_/ / |/ /  __/ /
/_/   /_/\__, /\____/|___/\___/_/
        /____/

''' + 'v1.0.0 - https://github.com/Perdyx/flyover\n')

async def main():
    if not args.script:
        print(m.INF + 'Launching spider...')

    if args.proxy:
        browserArgs = ['--proxy-server=socks5://' + args.proxy]
    else:
        browserArgs = []

    browser = await pyppeteer.launch({
        'args': browserArgs, 'headless': True
    })

    page = await browser.newPage()
    await page.goto('https://bgp.he.net/search?search%5Bsearch%5D=' + args.query.replace(' ', '+') + '&commit=Search')
    await page.waitForSelector('#search > table > tbody > tr:nth-child(1) > td:nth-child(1)')

    if not args.script:
        print(m.INF + 'Gathering ASN data...\n')

    rows = await page.xpath('//*[@id="search"]/table/tbody/tr[td]')
    data = {}
    for row in rows:
        title, content = await page.evaluate('row => [...row.children].map(child => child.textContent)', row)

        if title.startswith('AS'):
            if args.script:
                print(title)
            else:
                print('\033[35m' + title + '\033[0m -> ' + content)
            data.update({ title: content })

    if args.output:
        try:
            if os.path.exists(args.output):
                os.remove(args.output)

            file = open(args.output, 'w')
            file.write(json.dumps(data, indent = 2))
            file.close()

            if not args.script:
                print(m.WRN + 'Saved data to ./' + args.output)
        except OSError as err:
            print(m.ERR + err)

    if not args.script:
        print('\n' + m.INF + 'Squishing spiders...')

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

if not args.script:
    print(m.INF + 'Done')
