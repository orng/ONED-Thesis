#some scrapy stuff useful for wikipedia timelines
uls = response.xpath('//ul[preceding::h3[1]]')
a = []
for ul in uls:
    lis = ul.xpath('li')
    for li in lis:
        a.append(" ".join(li.xpath('descendant-or-self::*/text()').extract()))


text = []
for i in a:
    if i != '':
        text.append(i)

#now there is likely some wikipedia bullshit at the end of text
#remove it and then do
import json
with open(FILENAME, 'a') as f:
    c = 0
    for t in text:
        obj = {
                'date': c,
                'url': c,
                'text': t,
            }
        f.write(json.dumps(obj) + '\n')
        c+=1

