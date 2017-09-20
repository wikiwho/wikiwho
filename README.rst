WikiWho
=======
An algorithm to identify the revision origin of - and all changes ever applied to - the tokens of a revisioned Wiki document. This enables, e.g., detecting authorship and editor interactions.

Also check out the `WikiWho API <https://www.wikiwho.net/api/v1.0.0-beta/>`_ for current data from Wikipedia.

Requirements and Installation
=============================
WikiWho runs both on python 2 and 3.

`requests <http://docs.python-requests.org/en/master/>`_ package is required to get revision meta data and text from Wikipedia api.

`mwxml <https://github.com/mediawiki-utilities/python-mwxml>`_ package is required to get revision meta data and text from xml dumps. This package runs on only python 3.

Install WikiWho package using `pip`::

    pip install git+git://github.com/wikiwho/WikiWho.git@master#egg=WikiWho

Running WikiWho
===============
You can check example scripts under `WikiWho/WikiWho/examples <https://github.com/wikiwho/WikiWho/tree/master/WikiWho/examples>`_ to see how to run WikiWho.

Contact
=======
* Fabian Floeck: fabian.floeck[.]gesis.org
* Maribel Acosta: maribel.acosta[.]kit.edu
* Kenan Erdogan: kenan.erdogan[.]gesis.org

License
=======
This work is licensed under MIT.

**Developed at Karlsruhe Institute of Technology and GESIS - Leibniz Institute for the Social Sciences**

