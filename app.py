from flask import Flask,render_template,request
import nltk,re
import heapq
def sm(article_text):
    article_text = article_text.lower()
    clean_text = re.sub('[^a-zA-Z]', ' ', article_text)
    clean_text = re.sub('\s+', ' ', clean_text)
    sentence_list = nltk.sent_tokenize(article_text)
    stopwords = nltk.corpus.stopwords.words('english')
    word_frequencies = {}
    for word in nltk.word_tokenize(clean_text):
       if word not in stopwords:
          if word not in word_frequencies:
             word_frequencies[word] = 1
          else:
             word_frequencies[word] += 1

    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] = word_frequencies[word] / maximum_frequency
    sentence_scores = {}
    for sentence in sentence_list:
        for word in nltk.word_tokenize(sentence):
            if word in word_frequencies and len(sentence.split(' ')) < 30:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]

    summary = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)
    return " ".join(summary)
app = Flask(__name__)
@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        return render_template("index.html",data=request.form['inp'],val=sm(request.form['inp']))    
    else:
        return render_template("index.html",data="",val="")
if __name__=="__main__":
    app.run(debug=True)