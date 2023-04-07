
from pytube import YouTube
from pytube import Playlist
import threading
import time
import os
import subprocess




fileobj = {}
download_count = 1

#lock = threading.Lock()
def onProgress(stream, chunk, remains):
        total = stream.filesize
        percent = (total-remains) / total * 100
        print('下載中… {:05.2f}%'.format(percent), end='\r',file=sys.stderr)

def get_list(playlist) -> Playlist:
    p = Playlist(playlist)
    return p

def Download(link):
    global youtubeObject
    youtubeObject = YouTube(link,on_progress_callback=onProgress,on_complete_callback=onComplete)


    try:
       youtubeObject.streams.filter(subtype='mp4',resolution="1080p")[0].download()
    except:
        print("Download is error")
      
            
    print("Download is completed successfully")
# 檢查影片檔是否包含聲音
def check_media(filename):
    r = subprocess.Popen(["ffmpeg\\bin\\ffprobe", filename],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = r.communicate()

    if (out.decode('utf-8').find('Audio') == -1):
        return -1  # 沒有聲音
    else:
        return 1

# 合併影片檔
def merge_media():
    temp_video = os.path.join(fileobj['dir'], 'temp_video.mp4')
    temp_audio = os.path.join(fileobj['dir'], 'temp_audio.mp4')
    temp_output = os.path.join(fileobj['dir'], 'output.mp4')

    cmd = f'"ffmpeg\\bin\\ffmpeg" -i "{temp_video}" -i "{temp_audio}" \
        -map 0:v -map 1:a -c copy -y "{temp_output}"'
    try:
        subprocess.call(cmd, shell=True)
        # 視訊檔重新命名
        os.rename(temp_output, os.path.join(fileobj['dir'], fileobj['name']))
        os.remove(temp_audio)
        os.remove(temp_video)
        print('視訊和聲音合併完成')
    except:
        print('視訊和聲音合併失敗')

def download_sound():
    try:
        youtubeObject.streams.filter(type="audio").first().download()
    except:
        print('下載影片時發生錯誤，請確認網路連線和YouTube網址無誤。')
        return

# 檔案下載的回呼函式y
def onComplete(stream, file_path):
    global download_count, fileobj
    fileobj['name'] = os.path.basename(file_path)
    fileobj['dir'] = os.path.dirname(file_path)
    print('\r')

    if download_count == 1:
        if check_media(file_path) == -1:
            print('此影片沒有聲音')
            download_count += 1
            try:
                # 視訊檔重新命名
                os.rename(file_path, os.path.join(
                    fileobj['dir'], 'temp_video.mp4'))
            except:
                print('視訊檔重新命名失敗')
                return

            print('準備下載聲音檔')
            download_sound()          # 下載聲音
        else:
            print('此影片有聲音，下載完畢！')
    else:
        try:
            # 聲音檔重新命名
            os.rename(file_path, os.path.join(
                fileobj['dir'], 'temp_audio.mp4'))
        except:
            print("聲音檔重新命名失敗")
        # 合併聲音檔
        merge_media()
       
def playlist(downloadbypl,link):
    if downloadbypl == "y":
        
        playlist = input("pleas enter the playlist\n")
        p= get_list(playlist)
        no=int(input("the number of start\n1 start from first\n"))
        if no == 1:
            for url in p.video_urls: 
                download_count = 1
                Download(url,0)
        else:
            no = no-1
            for i in range (no,len(p.video_urls)):
                download_count = 1
                Download(p.video_urls[i],0) 
            
    elif downloadbypl == "n":
        link = input("Enter the YouTube video URL: ")
        Download(link)


