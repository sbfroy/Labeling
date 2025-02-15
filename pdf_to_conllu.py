
import re
import pdfplumber
import spacy

def get_text(pdf_path):
    # Extracts text from a PDF 
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                # Removes big unnecessary whitespaces
                clean_text = re.sub(r'\s+', ' ', page_text).strip()
                text.append(clean_text) 

    return ' '.join(text) # Returns text as one big string

def process_text_with_spacy(text, nlp):
    # Splits text into sentences and tokenizes them

    doc = nlp(text)
    sentences = []

    for sent in doc.sents:
        tokens = []
        for token in sent:
            # Further split tokens (punctuations) to separate symbols
            split_tokens = re.findall(r"\w+(?:[-/.]\w+)*|[^\w\s]", token.text, re.UNICODE)
            for sub_token in split_tokens:
                tokens.append(sub_token)

        sentences.append(tokens) # Each sent is a list of tokens

    return sentences # Returns a list of sentences

def to_conllu(sentences):
    # Tokenized sentences -> CoNLL-U formatted string

    conllu_lines = []
    for sent_id, tokens in enumerate(sentences, start=1):
        conllu_lines.append(f'# sent_id = {sent_id:06d}') # metadata
        conllu_lines.append(f'# text = {" ".join(tokens)}') # metadata
    
        for token_id, token in enumerate(tokens, start=1):
            lemma = upos = xpos = feats = head = deprel = deps = '_'
            misc = 'name=O'
            conllu_lines.append(
                f'{token_id}\t{token}\t{lemma}\t{upos}\t{xpos}\t{feats}\t{head}\t{deprel}\t{deps}\t{misc}'
                )
 
        conllu_lines.append('') 
       
    return '\n'.join(conllu_lines)

def main():

    # The spacy model (seems reasonable concerning acc and f1)
    nlp = spacy.load('nb_core_news_md')

    pdf = '000000'

    pdf_text = get_text(f'data/pdfs/{pdf}.pdf')
    sentences = process_text_with_spacy(pdf_text, nlp)
    conllu_data = to_conllu(sentences)

    with open(f'data/raw_conllus/{pdf}.conllu', 'w', encoding='utf-8') as f:
        f.write(conllu_data)
        print('Done!')

if __name__ == '__main__':
    main()