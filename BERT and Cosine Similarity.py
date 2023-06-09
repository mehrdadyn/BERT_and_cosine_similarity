# -*- coding: utf-8 -*-
"""BERT4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d0sWOT765hi5sOxfVkDVl5BeXnVps7hV
"""

!pip install transformers

# Commented out IPython magic to ensure Python compatibility.
import torch
from transformers import BertTokenizer, BertModel

# OPTIONAL: if you want to have more information on what's happening, activate the logger as follows
import logging
#logging.basicConfig(level=logging.INFO)

import matplotlib.pyplot as plt
# % matplotlib inline

# Load pre-trained model tokenizer (vocabulary)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# This is just an example to show the output of BERT tokenizer

text = "Here is the sentence I want embeddings for."
marked_text = "[CLS] " + text + " [SEP]"

# Tokenize our sentence with the BERT tokenizer.
tokenized_text = tokenizer.tokenize(marked_text)

# Print out the tokens.
print (tokenized_text)

# Define a new example sentence 
text = "Once I heard O’Kelly talking about God to my Popo, and I felt obliged to warn him he was wasting his time, because my grandfather was an agnostic"

# Add the special tokens.
marked_text = "[CLS] " + text + " [SEP]"

# Split the sentence into tokens.
tokenized_text = tokenizer.tokenize(marked_text)

# Map the token strings to their vocabulary indeces.
indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)

# Display the words with their indeces.
for tup in zip(tokenized_text, indexed_tokens):
    print('{:<12} {:>6,}'.format(tup[0], tup[1]))

# Mark each of the 22 tokens as belonging to sentence "1".
segments_ids = [1] * len(tokenized_text)

print (segments_ids)

# Convert inputs to PyTorch tensors
tokens_tensor = torch.tensor([indexed_tokens])
segments_tensors = torch.tensor([segments_ids])

# Load pre-trained model (weights)
model = BertModel.from_pretrained('bert-base-uncased',
                                  output_hidden_states = True, # Whether the model returns all hidden-states.
                                  )

# Put the model in "evaluation" mode, meaning feed-forward operation.
model.eval()

# Run the text through BERT, and collect all of the hidden states produced
# from all 12 layers. 
with torch.no_grad():

    outputs = model(tokens_tensor, segments_tensors)

    # Evaluating the model will return a different number of objects based on 
    # how it's  configured in the `from_pretrained` call earlier. In this case, 
    # becase we set `output_hidden_states = True`, the third item will be the 
    # hidden states from all layers. See the documentation for more details:
    # https://huggingface.co/transformers/model_doc/bert.html#bertmodel
    hidden_states = outputs[2]

print ("Number of layers:", len(hidden_states), "  (initial embeddings + 12 BERT layers)")
layer_i = 0

print ("Number of batches:", len(hidden_states[layer_i]))
batch_i = 0

print ("Number of tokens:", len(hidden_states[layer_i][batch_i]))
token_i = 0

print ("Number of hidden units:", len(hidden_states[layer_i][batch_i][token_i]))

# For the 5th token in our sentence, select its feature values from layer 5.
token_i = 5
layer_i = 5
vec = hidden_states[layer_i][batch_i][token_i]

# Plot the values as a histogram to show their distribution.
plt.figure(figsize=(10,10))
plt.hist(vec, bins=200)
plt.show()

# `hidden_states` is a Python list.
print('      Type of hidden_states: ', type(hidden_states))

# Each layer in the list is a torch tensor.
print('Tensor shape for each layer: ', hidden_states[0].size())

# Concatenate the tensors for all layers. We use `stack` here to
# create a new dimension in the tensor.
token_embeddings = torch.stack(hidden_states, dim=0)

token_embeddings.size()

# Remove dimension 1, the "batches".
token_embeddings = torch.squeeze(token_embeddings, dim=1)

token_embeddings.size()

# Swap dimensions 0 and 1.
token_embeddings = token_embeddings.permute(1,0,2)

token_embeddings.size()

# Stores the token vectors, with shape [22 x 3,072]
token_vecs_cat = []

# `token_embeddings` is a [22 x 12 x 768] tensor.

# For each token in the sentence...
for token in token_embeddings:
    
    # `token` is a [12 x 768] tensor

    # Concatenate the vectors (that is, append them together) from the last 
    # four layers.
    # Each layer vector is 768 values, so `cat_vec` is length 3,072.
    cat_vec = torch.cat((token[-1], token[-2], token[-3], token[-4]), dim=0)
    
    # Use `cat_vec` to represent `token`.
    token_vecs_cat.append(cat_vec)

print ('Shape is: %d x %d' % (len(token_vecs_cat), len(token_vecs_cat[0])))

# Stores the token vectors, with shape [22 x 768]
token_vecs_sum = []

# `token_embeddings` is a [22 x 12 x 768] tensor.

# For each token in the sentence...
for token in token_embeddings:

    # `token` is a [12 x 768] tensor

    # Sum the vectors from the last four layers.
    sum_vec = torch.sum(token[-4:], dim=0)
    
    # Use `sum_vec` to represent `token`.
    token_vecs_sum.append(sum_vec)

print ('Shape is: %d x %d' % (len(token_vecs_sum), len(token_vecs_sum[0])))

for i, token_str in enumerate(tokenized_text):
  print (i, token_str)

print('First 5 vector values for each instance')
print('')
print("grandfather   ", str(token_vecs_sum[30][:5]))

Eng1 = token_vecs_sum[30]

Eng2 = token_vecs_sum[5]

Eng3 = token_vecs_sum[2]

Eng4 = token_vecs_sum[17]

Eng5 = token_vecs_sum[7]

Per1 = token_vecs_sum[18]

Per2 = token_vecs_sum[4]

Per3 = token_vecs_sum[5]

Per4 = token_vecs_sum[4]

Per5 = token_vecs_sum[16]

#English similarity
from scipy.spatial.distance import cosine

# Calculate the cosine similarity for English

Eng1_Eng2 = 1 - cosine(Eng1, Eng2)
Eng1_Eng3 = 1 - cosine(Eng1, Eng3)
Eng1_Eng4 = 1 - cosine(Eng1, Eng4)
Eng1_Eng5 = 1 - cosine(Eng1, Eng5)
Eng2_Eng3 = 1 - cosine(Eng2, Eng3)
Eng2_Eng4 = 1 - cosine(Eng2, Eng4)
Eng2_Eng5 = 1 - cosine(Eng2, Eng5)
Eng3_Eng4 = 1 - cosine(Eng3, Eng4)
Eng3_Eng5 = 1 - cosine(Eng3, Eng5)
Eng4_Eng5 = 1 - cosine(Eng4, Eng5)




print('Vector similarity for  Eng1 & Eng2:  %.2f' % Eng1_Eng2)
print('Vector similarity for  Eng1 & Eng3:  %.2f' % Eng1_Eng3)
print('Vector similarity for  Eng1 & Eng4:  %.2f' % Eng1_Eng4)
print('Vector similarity for  Eng1 & Eng5:  %.2f' % Eng1_Eng5)
print('Vector similarity for  Eng2 & Eng3:  %.2f' % Eng2_Eng3)
print('Vector similarity for  Eng2 & Eng4:  %.2f' % Eng2_Eng4)
print('Vector similarity for  Eng2 & Eng5:  %.2f' % Eng2_Eng5)
print('Vector similarity for  Eng3 & Eng4:  %.2f' % Eng3_Eng4)
print('Vector similarity for  Eng3 & Eng5:  %.2f' % Eng3_Eng5)
print('Vector similarity for  Eng4 & Eng5:  %.2f' % Eng4_Eng5)

import statistics
Eng_data = [Eng1_Eng2, Eng1_Eng3, Eng1_Eng4, Eng1_Eng5, Eng2_Eng3, Eng2_Eng4, Eng2_Eng5, Eng3_Eng4, Eng3_Eng5, Eng4_Eng5]
Eng_average = statistics.mean(Eng_data)
print(Eng_average)

#Persian similarity
from scipy.spatial.distance import cosine

# Calculate the cosine similarity for Persian
Per1_Per2 = 1 - cosine(Per1, Per2)
Per1_Per3 = 1 - cosine(Per1, Per3)
Per1_Per4 = 1 - cosine(Per1, Per4)
Per1_Per5 = 1 - cosine(Per1, Per5)
Per2_Per3 = 1 - cosine(Per2, Per3)
Per2_Per4 = 1 - cosine(Per2, Per4)
Per2_Per5 = 1 - cosine(Per2, Per5)
Per3_Per4 = 1 - cosine(Per3, Per4)
Per3_Per5 = 1 - cosine(Per3, Per5)
Per4_Per5 = 1 - cosine(Per4, Per5)



print('Vector similarity for  Per1 & Per2:  %.2f' % Per1_Per2)
print('Vector similarity for  Per1 & Per3:  %.2f' % Per1_Per3)
print('Vector similarity for  Per1 & Per4:  %.2f' % Per1_Per4)
print('Vector similarity for  Per1 & Per5:  %.2f' % Per1_Per5)
print('Vector similarity for  Per2 & Per3:  %.2f' % Per2_Per3)
print('Vector similarity for  Per2 & Per4:  %.2f' % Per2_Per4)
print('Vector similarity for  Per2 & Per5:  %.2f' % Per2_Per5)
print('Vector similarity for  Per3 & Per4:  %.2f' % Per3_Per4)
print('Vector similarity for  Per3 & Per5:  %.2f' % Per3_Per5)
print('Vector similarity for  Per4 & Per5:  %.2f' % Per4_Per5)

import statistics
Per_data = [Per1_Per2, Per1_Per3, Per1_Per4, Per1_Per5, Per2_Per3, Per2_Per4, Per2_Per5, Per3_Per4, Per3_Per5, Per4_Per5]
Per_average = statistics.mean(Per_data)
print(Per_average)

#English vs. Persian similarity
from scipy.spatial.distance import cosine

# Calculate the cosine similarity for English-Persian
Eng1_Per1 = 1 - cosine(Eng1, Per1)
Eng1_Per2 = 1 - cosine(Eng1, Per2)
Eng1_Per3 = 1 - cosine(Eng1, Per3)
Eng1_Per4 = 1 - cosine(Eng1, Per4)
Eng1_Per5 = 1 - cosine(Eng1, Per5)

Eng2_Per1 = 1 - cosine(Eng2, Per1)
Eng2_Per2 = 1 - cosine(Eng2, Per2)
Eng2_Per3 = 1 - cosine(Eng2, Per3)
Eng2_Per4 = 1 - cosine(Eng2, Per4)
Eng2_Per5 = 1 - cosine(Eng2, Per5)

Eng3_Per1 = 1 - cosine(Eng3, Per1)
Eng3_Per2 = 1 - cosine(Eng3, Per2)
Eng3_Per3 = 1 - cosine(Eng3, Per3)
Eng3_Per4 = 1 - cosine(Eng3, Per4)
Eng3_Per5 = 1 - cosine(Eng3, Per5)

Eng4_Per1 = 1 - cosine(Eng4, Per1)
Eng4_Per2 = 1 - cosine(Eng4, Per2)
Eng4_Per3 = 1 - cosine(Eng4, Per3)
Eng4_Per4 = 1 - cosine(Eng4, Per4)
Eng4_Per5 = 1 - cosine(Eng4, Per5)

Eng5_Per1 = 1 - cosine(Eng5, Per1)
Eng5_Per2 = 1 - cosine(Eng5, Per2)
Eng5_Per3 = 1 - cosine(Eng5, Per3)
Eng5_Per4 = 1 - cosine(Eng5, Per4)
Eng5_Per5 = 1 - cosine(Eng5, Per5)



print('Vector similarity for  Eng1 & Per1:  %.2f' % Eng1_Per1)
print('Vector similarity for  Eng1 & Per2:  %.2f' % Eng1_Per2)
print('Vector similarity for  Eng1 & Per3:  %.2f' % Eng1_Per3)
print('Vector similarity for  Eng1 & Per4:  %.2f' % Eng1_Per4)
print('Vector similarity for  Eng1 & Per5:  %.2f' % Eng1_Per5)

print('Vector similarity for  Eng2 & Per1:  %.2f' % Eng2_Per1)
print('Vector similarity for  Eng2 & Per2:  %.2f' % Eng2_Per2)
print('Vector similarity for  Eng2 & Per3:  %.2f' % Eng2_Per3)
print('Vector similarity for  Eng2 & Per4:  %.2f' % Eng2_Per4)
print('Vector similarity for  Eng2 & Per5:  %.2f' % Eng2_Per5)

print('Vector similarity for  Eng3 & Per1:  %.2f' % Eng3_Per1)
print('Vector similarity for  Eng3 & Per2:  %.2f' % Eng3_Per2)
print('Vector similarity for  Eng3 & Per3:  %.2f' % Eng3_Per3)
print('Vector similarity for  Eng3 & Per4:  %.2f' % Eng3_Per4)
print('Vector similarity for  Eng3 & Per5:  %.2f' % Eng3_Per5)

print('Vector similarity for  Eng4 & Per1:  %.2f' % Eng4_Per1)
print('Vector similarity for  Eng4 & Per2:  %.2f' % Eng4_Per2)
print('Vector similarity for  Eng4 & Per3:  %.2f' % Eng4_Per3)
print('Vector similarity for  Eng4 & Per4:  %.2f' % Eng4_Per4)
print('Vector similarity for  Eng4 & Per5:  %.2f' % Eng4_Per5)

print('Vector similarity for  Eng5 & Per1:  %.2f' % Eng5_Per1)
print('Vector similarity for  Eng5 & Per2:  %.2f' % Eng5_Per2)
print('Vector similarity for  Eng5 & Per3:  %.2f' % Eng5_Per3)
print('Vector similarity for  Eng5 & Per4:  %.2f' % Eng5_Per4)
print('Vector similarity for  Eng5 & Per5:  %.2f' % Eng5_Per5)

#English vs. Persian Similarity Average
import statistics
Eng_Per_data = [Eng1_Per1, Eng1_Per2, Eng1_Per3, Eng1_Per4, Eng1_Per5, Eng2_Per1, Eng2_Per2, Eng2_Per3, Eng2_Per4, Eng2_Per5, Eng3_Per1, Eng3_Per2, Eng3_Per3, Eng3_Per4, Eng3_Per5, Eng4_Per1, Eng4_Per2, Eng4_Per3, Eng4_Per4, Eng4_Per5, Eng5_Per1, Eng5_Per2, Eng5_Per3, Eng5_Per4, Eng5_Per5]
Eng_Per_average = statistics.mean(Eng_Per_data)
print(Eng_Per_average)