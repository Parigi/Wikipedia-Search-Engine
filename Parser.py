import os
import xml.sax

import nltk
#nltk.download('omw-1.4')
#nltk.download('wordnet')
#nltk.download('stopwords')
#nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

wnl = nltk.WordNetLemmatizer()
porter = PorterStemmer()

#==================================================================================================================================


# Function that extracts External Links.
# From the body it searches for specific text, tokenize it, then removes stopwords and punctuation.
# Use of Lemmatizer and Stemmer.
# Returns a List.

def findExternalLinks(data):

    links = []

    PUNCTUATION = [u".", u",", u"|", u"-", u":", u";", u"?", u"(", u")", u"*", u"\"", u"\'", u"=", u'\\', u"&", u'/',
                   u"<", u">", u"[", u"]", u"{", u"}", u"#", u"!", u"%", u"redirect"]

    lines = data.split("== external links ==")
    if len(lines) > 1:
        lines = lines[1].split("\n")
        for i in range(len(lines)):
            if '* [' in lines[i] or '*[' or '* {{' or '*{{' in lines[i]:
                temp = lines[i].split(' ')
                word = [key for key in temp if 'http' not in temp]
                word = ' '.join(word)
                links.append(word)

    links = nltk.word_tokenize(''.join(links))
    fin_links = []

    for t in links:
        if ((not t in stopwords.words('english')) & (not t in PUNCTUATION)):
            t = wnl.lemmatize(t)
            t = porter.stem(t)
            fin_links.append(t)

    return fin_links

#=======================================================================================================================

# Function that extracts Infoboxes, Body and Categories.
# It searches for specific text, tokenize it, then removes stopwords and punctuation.
# Use of Lemmatizer and Stemmer.
# Return a List.

def findInfoBoxTextCategory(data):

    PUNCTUATION = [u".", u",", u"|", u"-", u":", u";", u"?", u"(", u")", u"*", u"\"", u"\'", u"=", u'\\', u"&", u'/',
                   u"<", u">", u"[", u"]", u"{", u"}", u"#", u"!", u"%", u'redirect']

    info = []
    bodyText = []
    category = []
    flagtext = 1
    lines = data.split('\n')

    for i in range(len(lines)):
        if '{{infobox' in lines[i]:
            flag = 0
            temp = lines[i].split('{{infobox')[1:]
            info.extend(temp)
            while True:
                if '{{' in lines[i]:
                    count = lines[i].count('{{')
                    flag += count
                if '}}' in lines[i]:
                    count = lines[i].count('}}')
                    flag -= count
                if flag <= 0:
                    break
                i += 1
                info.append(lines[i])

        elif flagtext:
            if '[[category' in lines[i] or '== external links ==' in lines[i]:
                flagtext = 0
            if flagtext:
                bodyText.append(lines[i])

        else:
            if "[[category" in lines[i]:
                line = data.split("[[category:")
                if len(line)>1:
                    category.extend(line[1:-1])
                    temp = line[-1].split(']]')
                    category.append(temp[0])


    info = nltk.word_tokenize(''.join(info))
    fin_info = []

    for t in info:
        if ((not t in stopwords.words('english')) & (not t in PUNCTUATION) ):
            t = wnl.lemmatize(t)
            t = porter.stem(t)
            fin_info.append(t)

    bodyText = nltk.word_tokenize(''.join(bodyText))
    fin_bodyText = []

    for t in bodyText:
        if ((not t in stopwords.words('english')) & (not t in PUNCTUATION)):
            t = wnl.lemmatize(t)
            t = porter.stem(t)
            fin_bodyText.append(t)

    category = nltk.word_tokenize(''.join(category))
    fin_category = []

    for t in category:
        if ((not t in stopwords.words('english')) & (not t in PUNCTUATION)):
            t = wnl.lemmatize(t)
            t = porter.stem(t)
            fin_category.append(t)


    return fin_info, fin_bodyText, fin_category



#=======================================================================================================================

# Function that process the parsed article.
# Return six strings about the article: title, body, category, infobox, external links, URL.

def process_article(title, text):

    text = text.lower()
    ext_links = findExternalLinks(text)

    text = text.replace('_', ' ').replace(',', '').replace('|', ' ')
    proc_title = title.replace(' ', '_')
    URL = 'https://en.wikipedia.org/wiki/' + proc_title

    infoBox, body, category = findInfoBoxTextCategory(text)

    proc_title = title.lower()
    proc_title = nltk.word_tokenize(''.join(proc_title))
    fin_title = []

    for t in proc_title:
        if (not t in stopwords.words('english')):
            t = wnl.lemmatize(t)
            t = porter.stem(t)
            fin_title.append(t)


    proc_title = ' '.join(fin_title)
    body = ' '.join(body)
    infoBox = ' '.join(infoBox)
    category = ' '.join(category)
    ext_links = ' '.join(ext_links)

    return proc_title, body, category, infoBox, ext_links, URL




#=======================================================================================================================

# SAX Parser works on XML sequentially.
# Parse XML file, call a function for processing text and create pages.

class WikiXmlHandler(xml.sax.handler.ContentHandler):
    """Content handler for Wiki XML data using SAX"""
    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._pages = []
        self._count = 0
        self._page_count = 0

    def characters(self, content):
        """Characters between opening and closing tags"""
        if self._current_tag:
            self._buffer.append(content)

    def startElement(self, name, attrs):
        """Opening tag of element"""
        if name in ('title', 'text'):
            self._current_tag = name
            self._buffer = []

    def endElement(self, name):
        """Closing tag of element"""
        if name == self._current_tag:
            self._values[name] = ''.join(self._buffer)

        if name == 'page':
            self._page_count += 1
            obj = process_article(**self._values)
            self._tempPage = self._page_count, obj[0], obj[1], obj[2], obj[3], obj[4], obj[5]
            self._pages.append(self._tempPage)

    def getPage(self):
        return self._pages



#=======================================================================================================================

script_dir = os.path.dirname(__file__)
rel_path = "dump"
abs_file_path = os.path.join(script_dir, rel_path)

def getParsedPage():
    """ Initialize the parser"""
    parser = xml.sax.make_parser()
    handler = WikiXmlHandler()
    parser.setContentHandler(handler)

    for filename in os.listdir(abs_file_path):
        name = os.path.join(abs_file_path, filename)
        parser.parse(name)
        #if handler._page_count > 10:
           #break

    return handler.getPage()

if __name__=='__main__':
    pages = getParsedPage()
    n = 0

    # Checking Parser.py
    for i in pages:
        print('page nr: ', n)
        print('id: ', i[0])
        print('title: ', i[1])
        print('body: ', i[2])
        print('category:', i[3])
        print('infobox: ', i[4])
        print('links: ', i[5])
        print('URL: ', i[6])

        n += 1








