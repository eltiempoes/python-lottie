import urllib.request


if __name__ == "__main__":
    from lxml import etree
    uri = "https://www.w3.org/TR/css-color-3/"

    html = etree.parse(urllib.request.urlopen(uri), etree.HTMLParser())

    print("color_table = {")

    names = set()

    for row in html.findall(".//table[@class='colortable']//tr"):
        if row.find(".//dfn") is None:
            continue

        name = row.xpath(".//dfn/text()")[0]

        if name in names:
            continue

        names.add(name)
        rgb = list(map(lambda x: int(x)/255, row.xpath(".//td[last()]/text()")[0].strip().split(",")))
        rgb.append(1)
        print('    "%s": %s,' % (name, rgb))

    print("}")
