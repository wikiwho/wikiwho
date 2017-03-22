# -*- coding: utf-8 -*-
"""

:Authors:
    Maribel Acosta,
    Fabian Floeck,
    Kenan Erdogan
"""
from __future__ import division
from __future__ import unicode_literals
import hashlib
from collections import Counter
import re


regex_dot = re.compile(r"([^\s\.=][^\s\.=][^\s\.=]\.) ")
regex_url = re.compile(r"(http.*?://.*?[ \|<>\n\r])")
# regex_url = re.compile(r"(http[s]?://.*?[ \|<>\n\r])")


def calculate_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def split_into_paragraphs(text):
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # html table syntax
    text = text.replace('<table>', '\n\n<table>').replace('</table>', '</table>\n\n')
    text = text.replace('<tr>', '\n\n<tr>').replace('</tr>', '</tr>\n\n')
    # wp table syntax
    text = text.replace('{|', '\n\n{|').replace('|}', '|}\n\n')
    text = text.replace('|-\n', '\n\n|-\n')
    return text.split('\n\n')


def split_into_sentences(text):
    text = text.replace('\n', '\n@@@@')
    # punctuation = ('. ', '\n', '; ', '? ', '! ', ': ', )
    # text = text.replace('. ', '.@@@@')
    text = regex_dot.sub(r'\1@@@@', text)
    text = text.replace('; ', ';@@@@')
    text = text.replace('? ', '?@@@@')
    text = text.replace('! ', '!@@@@')
    text = text.replace(': ', ':@@@@')
    text = text.replace('\t', '\t@@@@')
    # comments as sentence
    text = text.replace('<!--', '@@@@<!--')
    text = text.replace('-->', '-->@@@@')
    # references as sentence. ex: <ref name="...">{{ ... }}</ref>
    # text = text.replace('>{', '>@@@@{')
    # text = text.replace('}<', '}@@@@<')
    text = text.replace('<ref', '@@@@<ref')
    text = text.replace('/ref>', '/ref>@@@@')
    # urls as sentence
    text = regex_url.sub(r'@@@@\1@@@@', text)

    # text = text.replace('.{', '.||{')
    # text = text.replace('!{', '!||{')
    # text = text.replace('?{', '?||{')
    # text = text.replace('.[', '.||[')
    # text = text.replace('.]]', '.]]||')
    # text = text.replace('![', '!||[')
    # text = text.replace('?[', '?||[')

    while '@@@@@@@@' in text:
        text = text.replace('@@@@@@@@', '@@@@')
    return text.split('@@@@')


def split_into_tokens(text):
    text = text.replace('|', '||ææææ||')  # use | as delimiter

    text = text.replace('\n', '||').replace(' ', '||')

    symbols = ['.', ',', ';', ':', '?', '!', '-', '_', '/', '\\', '(', ')', '[', ']', '{', '}', '*', '#', '@',
               '&', '=', '+', '%', '~', '$', '^', '<', '>', '"', '\'', '´', '`', '¸', '˛', '’',
               '¤', '₳', '฿', '₵', '¢', '₡', '₢', '₫', '₯', '֏', '₠', '€', 'ƒ', '₣', '₲', '₴', '₭', '₺',
               '₾', 'ℳ', '₥', '₦', '₧', '₱', '₰', '£', '៛', '₽', '₹', '₨', '₪', '৳', '₸', '₮', '₩', '¥',
               '§', '‖', '¦', '⟨', '⟩', '–', '—', '¯', '»', '«', '”', '÷', '×', '′', '″', '‴', '¡',
               '¿', '©', '℗', '®', '℠', '™']
    # currency_symbols_long = '¢,£,¤,¥,֏,؋,৲,৳,৻,૱,௹,฿,៛,₠,₡,₢,₣,₤,₥,₦,₧,₨,₩,₪,₫,€,₭,₮,₯,₰,₱,₲,₳,₴,₵' \
    #                    ',₶,₷,₸,₹,₺,꠸,﷼,﹩,＄,￠,￡,￥,￦'.split(',')
    for c in symbols:
        text = text.replace(c, '||{}||'.format(c))

    # re-construct some special character groups as they are tokens
    text = text.replace('[||||[', '[[').replace(']||||]', ']]')
    text = text.replace('{||||{', '{{').replace('}||||}', '}}')
    # text = text.replace('||.||||.||||.||', '...')
    # text = text.replace('/||||>', '/>').replace('<||||/', '</')
    # text = text.replace('-||||-', '--')
    # text = text.replace('<||||!||||--||', '||<!--||').replace('||--||||>', '||-->||')
    text = text.replace('<||||!||||-||||-||', '||<!--||').replace('||-||||-||||>', '||-->||')

    while '||||' in text:
        text = text.replace('||||', '||')

    tokens = filter(lambda a: a != '', text.split('||'))  # filter empty strings
    tokens = ['|' if w == 'ææææ' else w for w in tokens]  # insert back the |s
    return tokens


def compute_avg_word_freq(token_list):
    c = Counter(token_list)  # compute count of each token in the list
    # remove some tokens
    remove_list = ('<', '>', 'tr', 'td', '[', ']', '"', '*', '==', '{', '}', '|', '-')  # '(', ')'
    for t in remove_list:
        if t in c:
            del c[t]

    return sum(c.values()) / len(c) if c else 0


def iter_rev_tokens(revision):
    """Yield tokens of the revision in order."""
    # from copy import deepcopy
    # ps_copy = deepcopy(revision.paragraphs)
    tmp = {'p': [], 's': []}
    for hash_paragraph in revision.ordered_paragraphs:
        # paragraph = ps_copy[hash_paragraph].pop(0)
        if len(revision.paragraphs[hash_paragraph]) > 1:
            tmp['p'].append(hash_paragraph)
            paragraph = revision.paragraphs[hash_paragraph][tmp['p'].count(hash_paragraph)-1]
        else:
            paragraph = revision.paragraphs[hash_paragraph][0]
        tmp['s'][:] = []
        for hash_sentence in paragraph.ordered_sentences:
            if len(paragraph.sentences[hash_sentence]) > 1:
                # tmp['s'].append('{}-{}'.format(hash_paragraph, hash_sentence))  # and dont do tmp['s'][:] = []
                tmp['s'].append(hash_sentence)
                sentence = paragraph.sentences[hash_sentence][tmp['s'].count(hash_sentence)-1]
            else:
                sentence = paragraph.sentences[hash_sentence][0]
            # sentence = paragraph.sentences[hash_sentence].pop(0)
            for word in sentence.words:
                yield word


# def iter_wikiwho_tokens(wikiwho):
#     """Yield tokens of the article in order."""
#     article_token_ids = set()
#     for rev_id in wikiwho.ordered_revisions:
#         for word in iter_rev_tokens(wikiwho.revisions[rev_id]):
#             if word.token_id not in article_token_ids:
#                 article_token_ids.add(word.token_id)
#                 yield word
