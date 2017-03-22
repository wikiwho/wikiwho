# -*- coding: utf-8 -*-
"""

:Authors:
    Maribel Acosta,
    Fabian Floeck,
    Andriy Rodchenko,
    Kenan Erdogan
"""


class Word(object):
    """Implementation of the structure "Word (Token)", which includes the authorship information."""
    def __init__(self):
        self.token_id = 0  # Sequential id (position) in article. Unique per article.
        self.value = ''  # The word (simple text).
        self.origin_rev_id = 0  # Revision id where the word was included.
        self.outbound = []
        self.inbound = []
        self.last_rev_id = 0  # Revision id where the word was last time used.
        self.matched = False

    def __repr__(self):
        return str(id(self))

    def to_dict(self):
        word = {self.origin_rev_id: self.value}
        return word


class Sentence(object):
    def __init__(self):
        self.hash_value = ''  # The hash value of the sentence.
        self.value = ''  # The sentence (simple text).
        self.splitted = []  # List of strings composing the sentence.
        self.words = []  # List of words in the sentence. It is an array of Word.
        self.matched = False  # Flag.

    def __repr__(self):
        return str(id(self))

    def to_dict(self):
        sentence = {}
        sentence.update({'hash': self.hash_value})

        obj_words = []
        for word in self.words:
            obj_words.append(repr(word))

        sentence.update({'obj': obj_words})
        return sentence


class Paragraph(object):
    def __init__(self):
        self.hash_value = ''  # The hash value of the paragraph.
        self.value = ''  # The text of the paragraph.
        self.sentences = {}  # Dictionary of sentences in the paragraph. {sentence_hash : [sentence_obj, ..]}
        self.ordered_sentences = []  # List with the hash of the sentences, ordered by hash appeareances.
        self.matched = False  # Flag.

    def __repr__(self):
        return str(id(self))

    def to_dict(self):
        paragraph = {}
        paragraph.update({'hash': self.hash_value})
        # paragraph.update({'sentences' : self.ordered_sentences})

        obj_sentences = []
        for sentence_hash in self.ordered_sentences:
            s = []
            for sentence in self.sentences[sentence_hash]:
                s.append(repr(sentence))
            obj_sentences.append(s)

        paragraph.update({'obj' : obj_sentences})

        return paragraph
        # str(hex(id(self)))
        # return "<'{0}'.'{1}' object at '{2}'>".format(self.__class__.__module__, self.__class__.__name__, hex(id(self)))


class Revision(object):
    def __init__(self):
        self.id = 0  # Wikipedia revision id.
        self.editor = ''  # id if id != 0 else '0|{}'.format(name)
        self.timestamp = 0
        self.paragraphs = {}  # Dictionary of paragraphs. {paragraph_hash : [paragraph_obj, ..]}.
        self.ordered_paragraphs = []  # Ordered list of paragraph hashes.
        self.length = 0  # Content length (bytes).
        self.original_adds = 0  # Number of tokens originally added in this revision.

    def __repr__(self):
        return str(id(self))
        # return str(self.id)

    def to_dict(self):
        revision = {}
        # json_revision.update({'id' : revisions[revision].id})
        # revision.update({'author' : {'id' : self.contributor_id, 'name' : self.contributor_name}})
        # json_revision.update({'length' : revisions[revision].length})
        # json_revision.update({'paragraphs' : revisions[revision].ordered_paragraphs})
        revision.update({'obj': []})
        for paragraph_hash in self.ordered_paragraphs:
            p = []
            for paragraph in self.paragraphs[paragraph_hash]:
                p.append(repr(paragraph))
            revision['obj'].append(p)

        return revision
