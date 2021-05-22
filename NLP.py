#import spacy

#nlp = spacy.load("en_core_web_sm")
from spacy.lang.en import English
nlp = English()  # just the language with no model
sentencizer = nlp.create_pipe("sentencizer")
nlp.add_pipe(sentencizer)

text=" HI th╫♣ere ,  HOw AREYOU"

def Clean(text):
    doc=nlp(text)
    cleaned_text=""
    for token in doc.sents:
        cleaned_text+=token.text
    return cleaned_text

print(Clean(text))