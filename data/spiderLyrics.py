import json
import requests
import re
import urllib
from bs4 import *
myurl = "http://music.163.com/playlist?id=2538771433"
headers = {"Host":" music.163.com",
"User-Agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
}
request = urllib.request.Request(myurl,headers=headers)
response = urllib.request.urlopen(request)
#不decode的话text是十六进制，不是中文
html = response.read().decode('utf-8','ignore')
soup = BeautifulSoup(html,'lxml')
#print(soup.prettify())
f=open('poems1.txt','w',encoding='utf-8')
for item in soup.ul.children:
    #取出歌单里歌曲的id  形式为：/song?id=11111111
    song_id = item('a')[0].get("href",None)
    #歌曲名称
    song_name = item.string
    #利用正则表达式提取出song_id的数字部分sid
    pat = re.compile(r'[0-9].*$')#提取模式为全都为数字的字符串
    sid = re.findall(pat,song_id)[0]#提取歌曲ID
    #打印歌曲ID以及名称
    #print(sid+"-"+song_name)    
    url = "http://music.163.com/api/song/lyric?"+"id="+str(sid)+"&lv=1&kv=1&tv=-1"
    html = requests.post(url)
    json_obj = html.text
    #歌词是一个json对象 解析它
    j = json.loads(json_obj)
    try:
        lyric = j['lrc']['lyric']
        #tlyric = j['tlyric']['lyric']
        #print(lyric)
        #print(tlyric)
    except KeyError:
        lyric = ""
    pat = re.compile(r'\[.*\]')
    lrc = re.sub(pat,"",lyric)
    #tlrc = re.sub(pat,"",tlyric)
    if lyric != "":
        lrc = sid+"-"+song_name+':::'+lrc.replace('\n','.')+'\n'#+tlrc.strip()+'\n'
        #lrc = lrc.replace('.','\n')
        pat = re.compile(r'作.*?\.')
        lrc = re.sub(pat,"",lrc)
        print(lrc)
        #print (type(lrc))
        f.write(lrc)
f.close()