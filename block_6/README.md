gensim uses python 3.12 so you will need to either make an enviroment or use the dockerfile

First we form sentences from the train dataframe to avoid overfitting 
then we use Word2vec from gensim with the configurations that were set from the first ipynb slide
word2vec returns a list of vector_size length for each word so a word like 'cat' will have 100 values if the 
vector size is 100 we embed this in a matrix where for each index corresponding to the word will store its
word2vec vector e.g embed_matrix[3] will store the vector of the word of index (3) which was encoded in the vocabulary class we modify the embedding layer so that it doesnt generate random embeddings but instead use
our own modified embedding then that vector is passed to an encoder which has a bi-directional LSTM which processes
the information (input) in both left->right and right->left so if the output is 256 its 512 since we process both directions then the hidden state output and cell state output is sequentially passed as an intial hidden state input
cell state input for the decoder which uses the attention mechanism for each word needed to be decoded it looks up
the words relevant to it from the encoder's hidden (short term memory) outputs which results in the context vector
then in the end it passes through a linear layer then softmax..now the final output is a vector of probability for each word..each word's index corresponds to the list index so for example the output is of length 100 then output[0]
gives us the probability of word index 0 (which correspoinds to pad) then we compute the bleu score and the rogue score for the model..note that for rogue scores. Rogue 1's  is the score for 1-gram,Rogue 2 is for the 2-gram score,
Rogue L is for the longest common sub-sequence it takes the common sequence and compares..for example
reference:I love eating apples 
prediction:I really really really love eating delicious red apples
it will compare the sentence 'I love eating apples' from the prediction with the reference the score is 0.75 there
As for the results there was a slight improvement..the train accuracy was on continuous improvement however validation accuracy started to converge from the 5-6th epoch
