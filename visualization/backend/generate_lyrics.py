import tensorflow as tf
from model import char_rnn
from utils import build_dataset
import numpy as np

start_token = ':::'
end_token = ':'
model_dir = 'result/lyric'
corpus_file = 'data/lyrics.txt'

lr = 0.0002


def to_word(predict, vocabs):
    predict = predict[0]
    predict /= np.sum(predict)
    sample = np.random.choice(np.arange(len(predict)), p=predict)
    if sample > len(vocabs):
        return vocabs[-1]
    else:
        return vocabs[sample]


def gen_lyric(begin_word):
    batch_size = 1
    print('## loading corpus from %s' % model_dir)
    lyrics_vector, word_int_map, vocabularies = build_dataset(corpus_file)

    input_data = tf.placeholder(tf.int32, [batch_size, None])

    end_points = char_rnn(model='lstm', input_data=input_data, output_data=None, vocab_size=len(
        vocabularies), rnn_size=128, num_layers=2, batch_size=64, learning_rate=lr)

    saver = tf.train.Saver(tf.global_variables())
    init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
    with tf.Session() as sess:
        sess.run(init_op)

        checkpoint = tf.train.latest_checkpoint(model_dir)
        saver.restore(sess, checkpoint)

        x = np.array([list(map(word_int_map.get, start_token))])

        [predict, last_state] = sess.run([end_points['prediction'], end_points['last_state']],
                                         feed_dict={input_data: x})
        if begin_word:
            word = begin_word
        else:
            word = to_word(predict, vocabularies)
        lyric_ = ''

        i = 0
        while word != end_token:
            if ord(word) > 128 or ord(word) < 0:
                break
            lyric_ += word
            i += 1
            if i >= 1200:
                break
            x = np.zeros((1, 1))
            x[0, 0] = word_int_map[word]
            [predict, last_state] = sess.run([end_points['prediction'], end_points['last_state']],
                                             feed_dict={input_data: x, end_points['initial_state']: last_state})
            word = to_word(predict, vocabularies)
        return lyric_


def pretty_print_lyric(lyric_):
    lyric_sentences = lyric_.split('.')
    str = ''
    for s in lyric_sentences:
        if s != '' and s != end_token:
            str = str + s + '<br>'
    return str
            

def execute_generate(begin_char):
    lyric = gen_lyric(begin_char)
    return pretty_print_lyric(lyric_=lyric)
