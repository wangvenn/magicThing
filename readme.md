ref:

http://www.aclweb.org/anthology/D08-1097

###############################

update (9th May)

parser tools

http://www.nltk.org/book/ch07.html#ref-chunkex-draw

tips:

Special cases:

1. the在开头
2. and
3. 有些答案是错误的
4. 答案从问题中的many变成了any

(11th May)
修改了lianyuz/project文件
1.对于train集合中的第一个article中的what类型的问题进行了初步的处理
2.最后打印的集合是所有可能是answer的集合
3.分词阶段加入了将连续大写单词分为一个词

16th May
Parameters for our own baseline:

For development set:

parameters used:

Accuracy of BM25 with k1: 1.1  k2: 0  b: 0.18
0.660241947884

weight for rule 1: 0.9

predict accuracy:

0.672239573764 (answer in answer_list)
0.228917876171 (answer is correct)

total: 0.151141184469

For test set:
0.18483

Update:

1. Fix a bug ---- ',' should be replaced by -COMMA-

2. better parameters:

Accuracy of BM25 with k1: 0.78  k2: 0  b: 0.5
0.68264717486


for w1:
#best when w1 = 0.7
