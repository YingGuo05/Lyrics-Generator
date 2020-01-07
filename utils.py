from collections import Counter
import os
import sys
import numpy as np

# Start and end token
start_token=':::'
end_token=':::'

def build_dataset(filename):
    """
    build dataset, lyrics and lyrics vector
    :param filename: lyrics files
    :return:
    """
    lyrics=[]
    with open(filename,'r') as in_data:
        for lyric in in_data.readlines():
            try:
                title,content=lyric.split(':::') # title and content
                content=start_token+content+end_token
                lyrics.append(content)
            except ValueError as e:
                pass

    words_list=[word for lyric in lyrics for word in lyric]
    counter=Counter(words_list).most_common()
    words,_=zip(*counter)
    words = words + (' ',)
    word_to_int=dict(zip(words,range(len(words))))

    lyrics_vector = [list(map(lambda word: word_to_int.get(word, len(words)), lyric)) for lyric in lyrics]

    print(len(lyrics_vector))
    return lyrics_vector,word_to_int,words


def generate_batch(batch_size,lyrics_vector,word_to_int):
    num_batch=len(lyrics_vector)//batch_size
    x_batches=[]
    y_batches=[]

    for i in range(num_batch):
        start_index=i*batch_size
        end_index=(i+1)* batch_size

        batches=lyrics_vector[start_index:end_index]
        max_length=max(map(len,batches))
        x_data=np.full((batch_size,max_length),word_to_int[' '],np.int32)
        for row,batch in enumerate(batches):
            x_data[row,:len(batch)]=batch
        y_data=np.copy(x_data)
        y_data[:,:-1]=y_data[:,1:]

        """
        x:3 12 13 14 15 16
        y:12 13 14 15 16 0
        """
        x_batches.append(x_data)
        y_batches.append(y_data)

    return x_batches,y_batches

