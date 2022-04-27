from tkinter import *
from whoosh.fields import Schema, ID, TEXT, NUMERIC
from whoosh import scoring, qparser
import whoosh.index as index
import webbrowser

import nltk
#nltk.download('wordnet')
#nltk.download('stopwords')
#nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

#=======================================================================================================================

# Defining Schema and Scoring Algorithm
schema = Schema(id=NUMERIC, title=TEXT, body=TEXT, category=TEXT, infobox=TEXT, links=TEXT, URL=ID(stored=True))
w = scoring.TF_IDF()

index = index.open_dir("index")
wnl = nltk.WordNetLemmatizer()
porter = PorterStemmer()

#=======================================================================================================================

# Graphic Interface

def urljump (event):
    widget = event.widget
    ind = int(widget.curselection()[0])
    url = widget.get(ind)
    if 'https://' in url:
        webbrowser.open_new(url)

# Window
root = Tk()
root.geometry("900x900")
root.title("Wikipedia-Search-Engine".upper())
root.resizable(True,True)
root.configure(background="white")

# Ask for terms
label_campi_ricerca = Label(root, background="white", text="Enter Query".upper(), font=("helvetica",15))
label_campi_ricerca.pack(anchor="center",padx=20, pady=20)

# Input box
input = Entry(background="white", font=("helvetica",15))
input.pack(anchor="center", pady=20)

# Function that takes a free text as an input query, analyze it and search for results.
# Print the URLs of the first 30 results (sorted by score).
def searchF():

    results_list.delete(0, END)
    text_input = input.get()

    urls = []
    with index.searcher(weighting=w) as searcher:
        results_list.insert(END, "Results for query '" + text_input + "': \n")
        qp = qparser.MultifieldParser(["id", "title", "body", "category", "infobox", "links"], index.schema)
        qs = []
        text_input = nltk.word_tokenize(''.join(text_input))

        for t in text_input:
            if (not t in stopwords.words('english')):
                t = wnl.lemmatize(t)
                t = porter.stem(t)
                qs.append(t)

        text_input = ' '.join(qs)
        query = qp.parse(text_input)


        results = searcher.search(query, terms=True, limit=10)


        if results.is_empty():
            results_list.insert(END, "No documents matched")
            results_list.insert(END, "\n")

        else:
            results_list.insert(END, str(len(results)) + " documents matched")
            results_list.insert(END, "URL redirect to the related Wikipedia page")
            results_list.insert(END, "\n")

            i = 0
            while i < results.scored_length():
                t = str(results[i]).replace("<Hit {'URL': '", "")
                t = t.replace("'}>", " ")
                results_list.insert(END, str(i+1))
                results_list.insert(END, t)
                results_list.insert(END, "\n")
                print(str(i+1) + " " + t + " " + str(results[i].score))
                i += 1




# Button
button=Button(root,background="white",font=("helvetica",15),text="Search!".upper(),command=searchF)
button.pack(anchor="center")

# Label
label2=Label(root,background="white",font=("helvetica",15),text="Results".upper())
label2.pack(anchor="center",pady=20)

# Listbox with results (URLs)
results_list=Listbox(root,background="white",font=("helvetica",12),width=100,height=20)
results_list.bind("<<ListboxSelect>>", urljump)
results_list.pack(anchor="center",padx=20,pady=20)

#=======================================================================================================================

if __name__ == "__main__":
    root.mainloop()