from mwxml import Dump
from mwtypes.files import reader

from wikiwho.wikiwho import Wikiwho


def process_xml_dump(xml_file_path):
    # more info about reading xml dumps: https://github.com/mediawiki-utilities/python-mwxml
    dump = Dump.from_file(reader(xml_file_path))
    for page in dump:
        wikiwho = Wikiwho(page.title)
        wikiwho.analyse_article_from_xml_dump(page)
        break  # process only first page
    return wikiwho

if __name__ == '__main__':
    # link to xml dumps: https://dumps.wikimedia.org/enwiki/
    xml_file_path = 'path/to/xml'
    xml_file_path = '/home/kenan/PycharmProjects/wikiwho_api/wikiwho/tests/test_jsons/enwiki-20161101-pages-meta-history5.xml-p000420318p000440017.7z'
    wikiwho_obj = process_xml_dump(xml_file_path)
    print(wikiwho_obj.title)
    print(wikiwho_obj.ordered_revisions)
