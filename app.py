from flask import Flask, flash, redirect, render_template, request, url_for
import os
import speech_recognition as sr
import spacy
from spacy.lang.en import English
from spacy.pipeline import Sentencizer
from collections import Counter
import heapq

nlp = English()
sentencizer = Sentencizer()
nlp.add_pipe('sentencizer')


app = Flask(__name__)

# # Define the punctuator function
# def punctuator(text):
#     # load the spacy model for English language
#     nlp = spacy.load("en_core_web_sm")

#     # create a Doc object from the text
#     doc = nlp(text)

#     # initialize an empty string to hold the punctuated text
#     punctuated_text = ""

#     # loop through each token in the Doc
#     for token in doc:
#         # concatenate the token text and the token's trailing whitespace to the punctuated text
#         punctuated_text += token.text_with_ws
#         # if the token ends with punctuation other than an ellipsis, add a space after it
#         if token.text != "..." and token.text.endswith((".", "?", "!")):
#             punctuated_text += " "
    
#     return punctuated_text

# Define the TextRank algorithm for sentence scoring
def textrank(document):
    # Tokenize the document
    doc = nlp(document)
    # Collect word counts
    word_counts = Counter()
    for token in doc:
        if not token.is_stop and not token.is_punct:
            word_counts[token.lemma_] += 1
    # Calculate the maximum word count
    max_count = max(word_counts.values()) if len(word_counts) > 0 else 1
    # Calculate the word scores
    word_scores = {word: count/max_count for word, count in word_counts.items()}
    # Collect sentence scores
    sentence_scores = []
    for sent in doc.sents:
        score = sum([word_scores.get(token.lemma_, 0) for token in sent if not token.is_stop])
        sentence_scores.append((sent, score))
    # Select the top sentences
    top_sentences = heapq.nlargest(3, sentence_scores, key=lambda x: x[1])
    # Sort the top sentences in their original order
    top_sentences.sort(key=lambda x: doc.text.index(x[0].text))
    # Return the top sentences as a string
    return ' '.join([sent.text for sent, score in top_sentences])

# Define the summarizer function
def summarizer(text):
    # Create a Doc object from the text
    doc = nlp(text)
    # Concatenate the text of each sentence into a single string
    sentence_text = [sent.text for sent in doc.sents]
    document = ' '.join(sentence_text)
    # Score and select the top sentences using TextRank
    summary = textrank(document)
    # Return the summary
    return summary

@app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an empty file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        # Convert audio file to text using Google Speech Recognition
        # r = sr.Recognizer()
        # with sr.AudioFile(file_path) as source:
        #     audio_text = r.listen(source, timeout=10) 
        #     try:
        #         text = r.recognize_google(audio_text)

        #     except sr.UnknownValueError:
        #         text = "Could not understand audio"
        #     except sr.RequestError as e:
        #         text = "Could not request results; {0}".format(e)
        
        # text = """Ok, so let's start by going over the minutes from the last meeting. Does anyone have any update for Chennai? We were originally planning to use XYZ software for this project, but I did some research and found that there might be a better option out there. Really? Are you thinking of some additional features that could be really useful for this project? And it's actually more cost-effective than XYZ? That's great! So we should update the project plan to reflect the changes. Yes, I think that would be a good idea. And while we are at it, we should also make sure we are still on track with the timelines and deliverables. Are we available to check in on our progress with the initial design specs? Are we still on target to have those completed by the end of the week? Yes, we are. I spoke with the client yesterday and they are expecting to see those specs by Friday at least. Ok, so we should make sure we have everything finalized and ready to present by then. Agreed. And we should also start thinking about how we are going to approach the testing and QA phase of this project. Point. Let's plan to discuss that at the next meeting. And in the meantime, let's make sure we are communicating regularly and keeping each other updated on our progress. We are all on the same page and working towards the same goals. Absolutely. Communication and collaboration are key to the success of this project."""
        text = """Ok so let's start by going over the minutes from the last meeting does anyone have any update for chennai do we were originally planning to use xyz software for this project but i did some research and found that there might be a better option out there really are you thinking of some additional features that could be really useful for this project in its actually more cost-effective than xyz that great so we should update the project plan to reflect the changes yes i think that would be a good idea and while we are at it we should also make sure we are still on track with the timelines and deliverables of their available i wanted to check in on our progress with the initial design specs are we still your target to have those completed by the end of the week yes we are i spoke with the client yesterday and they are expecting to see those texts by friday at least ok so we should make sure we have everything finalized and ready to present by them agreed in hindi and we should also start thinking about how we are going to approach the testing and qa phase of this project point let's plan to discuss that at the next meeting and in the meantime let's make sure we are communicating regularly and keeping each other updated on a progress we are all on the same page and working towards the same goals solutely communication and collaboration at key to success of this project."""
        # Punctuate the text using the punctuator
        # punctuated_text = punctuator(text)  
        
        # Summarize the text using the summarizer
        summary = summarizer(text)          
        
        # Redirect to success page with the converted text
        return redirect(url_for('success', text=text, summary=summary))
    
    return render_template('index.html')

@app.route('/success')
def success():
    text = request.args.get('text')
    summary = request.args.get('summary')
    return render_template('success.html', text=text,summary=summary)
if __name__ == '__main__':
    # Define the folder where uploaded files will be stored
    app.config['UPLOAD_FOLDER'] = 'uploads'
    # Run the app
    app.run(debug=True)
