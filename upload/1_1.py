#!/usr/bin/python3
from urllib.parse import urlsplit

urls = [
"http://www.google.com/a.txt",
"http://www.google.com.tw/a.txt",
"http://www.google.com/download/c.jpg",
"http://www.google.co.jp/a.txt",
"http://www.google.com/b.txt",
"https://facebook.com/movie/b.txt",
"http://yahoo.com/123/000/c.jpg",
"http://gliacloud.com/haha.png",
]

check = [
        urlsplit(urls[0]).path.replace("/","")[-5:],
        urlsplit(urls[1]).path.replace("/","")[-5:],
        urlsplit(urls[2]).path.replace("/","")[-5:],
        urlsplit(urls[3]).path.replace("/","")[-5:],
        urlsplit(urls[4]).path.replace("/","")[-5:],
        urlsplit(urls[5]).path.replace("/","")[-5:],
        urlsplit(urls[6]).path.replace("/","")[-5:],
        urlsplit(urls[7]).path.replace("/","")[-5:],
]

list0 = sorted(check)
number = 0
for i in range(len(list0)-1):
    if list0[i+1] == list0[i]:
        print(list0[i]," ",end = '')
        number = number + 1
        print(number)
