# WIKIPEDIA-SEARCH-ENGINE

Wikipedia-Search-Engine is a project created for the course Information Management, University of Modena (year 2019/2020), taught by the professor Federica Mandreoli.

The aim is to **return Wikipedia pages relevant to a submitted query**, with the results ordered with respect to relevance.

----------------------------------------------------------------------------------------

## INSTALLATION

Requires Python 3.8 (or newer).

Makes use of the libraries:	
	xml.sax
	whoosh
	webbrowser
	tkinter
	nltk


Create a project containing:
	- the 3 code files --> Python.py , Indexer.py , Searcher.py
	- the directory containing the XML files on which to create the index --> dump 
	- the directory with an index ready to be used by Searcher--> index

----------------------------------------------------------------------------------------

## USE

Start Parser.py to see how the XML files are parsed and how the text is processed.

Start Indexer.py to create the index from the dump (via Parser.py).
Disclaimer: requires around one hour.

Run Searcher.py to enter queries through a graphical interface, searching the index. 
You can just try to run this script and see how our index works.


----------------------------------------------------------------------------------------

## CODE

1) Parser.py --> Parses the XML files inside the "dump" directory. 
Contains the WikiXmlHandler class for parsing XML files through SAX.
Contains functions that process the text of each page, extracting any External Links,
Categories and Infoboxes.
It makes use of the NLTK library to obtain lexemes and eliminate unnecessary words (stopowords).


2) Indexer.py --> Creates the index, adding the documents passed by the Parser.py getParsedPages() function.


3) Searcher.py --> It is possible to insert queries to search for terms and phrases. 
It makes use of a graphical interface that displays the URLs of the ten most relevant results for the
query submitted. Clicking on the URLs redirects you to the relevant Wikipedia page.

![Searcher](https://user-images.githubusercontent.com/54531753/165717760-2896d342-ee9a-438d-9da4-7a844ca8e1e6.png)


----------------------------------------------------------------------------------------


## AUTHORS

Bordini Luca

Parigi Luca
