"""from bs4 import BeautifulSoup
import requests

url = 'https://dnd.su/spells/'


headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
r = requests.get(url=url, headers=headers)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.content, 'html5lib')
print(soup.prettify())
"""

with open('allSpells.js', 'r', encoding='utf-8') as file:
    new_text = file.read()

new_text = new_text.replace('{', '|')
new_text = new_text.replace('}', '|')

spells_list = dict()

for part in new_text.split('|'):
    if part.strip()[:2] == '"n':
        part = part.replace('\n', ':')
        min_parts = part.split(':')
        spells_list[min_parts[2].strip().replace(',', '').replace('"', '').replace('      ', '')] = {
            min_parts[i].strip().replace(',', '').replace('"', '').replace('      ', ''):
                min_parts[i+1].strip().replace(',', '').replace('"', '').replace('      ', '')
            for i in range(3, len(min_parts) - 1, 2)
        }


print(spells_list)
