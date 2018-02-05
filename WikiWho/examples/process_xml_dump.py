from mwxml import Dump
from mwtypes.files import reader

from WikiWho.wikiwho import Wikiwho


def process_xml_dump(xml_file_path):
    """
    Link to xml dumps: https://dumps.wikimedia.org/enwiki/

    Example usage:

    from WikiWho.examples.process_xml_dump import process_xml_dump

    xml_file_path = '/home/kenan/Downloads/enwiki-20180101-pages-meta-history1.xml-p5753p7728.7z'
    wikiwho_obj = process_xml_dump(xml_file_path)
    print(wikiwho_obj.title)
    print(wikiwho_obj.ordered_revisions)

    :param xml_file_path:
    :return: WikiWho object.
    """
    # more info about reading xml dumps: https://github.com/mediawiki-utilities/python-mwxml
    dump = Dump.from_file(reader(xml_file_path))
    for page in dump:
        wikiwho = Wikiwho(page.title)
        wikiwho.analyse_article_from_xml_dump(page)
        break  # process only first page
    return wikiwho
