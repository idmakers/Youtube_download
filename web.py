from flask import Flask, request, render_template
from youtube_download import Download
from youtube_download import playlist
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/submit', methods=['POST'])
def link():
    if request.method == 'POST':
        if request.form['playlist']=="on":
            link = request.form['link']
            no= request.form['no']
            playlist(link,int(no))
        else:
            link = request.form['link']
            Download(link)
    return render_template("index.html") 
#test 
if __name__ == '__main__':
    app.run()
