from flask import Flask, request, render_template
from youtube_download import Download
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/submit', methods=['POST'])
def link():
    if request.method == 'POST':
        link = request.form['link']
        Download(link)
        

if __name__ == '__main__':
    app.run()
