import os
import csv
import json
import nltk
import copy
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.spatial.distance import cosine as cos_distance
from sklearn.decomposition import TruncatedSVD
from nltk.tag import StanfordNERTagger

def create_process_tools():
    stopwords = nltk.corpus.stopwords.words('english')
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
    v = DictVectorizer(sparse=False)
    transformer = TfidfTransformer(smooth_idf=False,norm=None)
    svd = TruncatedSVD(n_components=500)
    return stopwords,lemmatizer,v,transformer,svd

def input_data():

    base_path = os.path.join('')
    data_path = os.path.join(base_path,'data')
    train_file = data_path + '/QA_train.json'
    train_data = json.load(open(train_file))
    test_file = data_path + '/QA_test.json'
    test_data = json.load(open(test_file))
    dev_file = data_path + '/QA_dev.json'
    dev_data = json.load(open(dev_file))

    return train_data,test_data,dev_data

def output_result(filename):

    predictions_file = open(filename, "wb")
    open_file_object = csv.writer(predictions_file)
    open_file_object.writerow(["id","answer"])
    # open_file_object.writerows(zip(ID, output))
    predictions_file.close()

def get_BOW(text):
    BOW = {}
    for word in text:
        BOW[word] = BOW.get(word,0) + 1
    return BOW

def lemmatize(word):
    lemma = lemmatizer.lemmatize(word,'v')
    if lemma == word:
        lemma = lemmatizer.lemmatize(word,'n')
    return lemma

def transform_doc(doc):
    return svd.fit_transform(transformer.fit_transform(v.fit_transform(doc)))

def transform_query(query_text):
    query_text = nltk.word_tokenize(query_text)
    query_text = [word.lower() for word in query_text]
    for word in query_text:
        if word in stopwords:
            query_text.remove(word)
        # the follow process will decrease accuracy
        # if not word.isalpha():
        #     query_text.remove(word)
    return svd.transform(transformer.transform(v.transform([get_BOW(query_text)])))[0]

def process_sentence(sentence):
    #token, lower, remove stopwords, get bag of words
    sentence = nltk.word_tokenize(sentence)
    sentence = [word.lower() for word in sentence]
    for word in sentence:
        if word in stopwords:
            sentence.remove(word)
    sentence = get_BOW(sentence)
    return sentence

def divide_data(data):
    #achieve sentences, questions, answers and the corresponding indexs.
    queries = []
    indexs = []
    answers = []
    qas = data['qa']
    sentences = data['sentences']
    for qa in qas:
        query = qa['question']
        queries.append(query)
        index = qa['answer_sentence']
        indexs.append(index)
        answer = qa['answer']
        answers.append(answer)
    for i in range(len(sentences)):
        sentences[i] = process_sentence(sentences[i])
    sentences = transform_doc(sentences)
    return sentences,indexs,queries,answers

def get_best_doc_num(query,sentences):
    #get the most likely documents according to the query
    min = 1
    index = 0
    for i in range(sentences.shape[0]):
        dist = cos_distance(query,sentences[i])
        if dist < min:
            min = dist
            index = i
    return index

def evaluate_article(predicts,indexs):
    #output the accuracy of predicted documents
    count = 0
    for i in range(len(predicts)):
        if predicts[i] != indexs[i]:
            count += 1
    result = 1 - float(count)/len(predicts)
    return result

def sentence_retrieval(article):
    #achieve the original sentences which are retrieved
    original_article = copy.deepcopy(article)
    sentences,indexs,queries,answers = divide_data(article)
    original_query = copy.deepcopy(queries)

    predicts = []
    for i in range(len(queries)):
        queries[i] = transform_query(queries[i])
        predict = get_best_doc_num(queries[i],sentences)
        predicts.append(predict)

    print 'retrieval accuracy is: ',evaluate_article(predicts,indexs)

    sentences_retrieval = []
    for num in predicts:
        sent = original_article['sentences'][num]
        sentences_retrieval.append(sent)
    return sentences_retrieval,original_query

def input_NER():
    stanford_dir = os.path.join('stanford-ner-2016-10-31')
    jarfile = os.path.join(stanford_dir,'stanford-ner.jar')
    modelfile = os.path.join(stanford_dir,'classifiers/english.muc.7class.distsim.crf.ser.gz')
    return modelfile,jarfile

'''input data'''
train,test,dev = input_data()
'''input data'''

'''get processing tools'''
stopwords,lemmatizer,v,transformer,svd = create_process_tools()
'''get processing tools'''

'''retrieve sentences'''
model,jar = input_NER()
st = StanfordNERTagger(model,jar)
for article in train[5:6]:
    sentences,queries = sentence_retrieval(article)
    # print st.tag_sents(sentences)
'''retrieve sentences'''

# print sentences[5]
# for query in queries:
#     print query.split()[0]
print sentences[2]
print queries[2]
entities = st.tag(nltk.word_tokenize(sentences[2]))

for query in queries:
    print query


# for i in range(len(entities)):
#     if entities[i][1] == 'ORGANIZATION':
#         entities[i][1] = 'O'
#     # if entities[i][0].isdigit():
#     #     entities[i][1] = 'NUMBER'
#     print entities[i]



# '''output data'''
# output_result("result.csv")
# '''output data'''


