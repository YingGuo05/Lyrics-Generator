from flask import Flask
from flask import (render_template, request)
from generate_lyrics import execute_generate

app = Flask(__name__)


@app.route('/')
def start_app():
    lyrics = ''
    return render_template('index.html', lyrics=lyrics)


@app.route('/load/', methods=['POST'])
def lyrics_generator():
    select_char = request.form.get('char_menu')
    begin_char = select_char.encode(encoding='UTF-8')
    lyrics = execute_generate(begin_char)
    return render_template('index.html', lyrics=lyrics)


if __name__ == '__main__':
    app.run()
