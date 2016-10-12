# for chinese render
# -*- coding: utf-8 -*-
from django.http import HttpResponse

# for loading template
from django.template.loader import get_template
from django import template

# for render_to_response
from django.shortcuts import render_to_response

def here(request):
    return HttpResponse('看得到吧！！')

def math(request, a, b):
    a = int(a) 
    b = int(b)
    s = a + b
    d = a - b
    p = a * b
    q = a / b

#    with open('templates/math.html','r') as render:
#        t = template.Template(render.read())

    # get_template 會讀取一個模板檔案，並且回傳一個模板物件
    #t = get_template('math.html')

        #html = '<html>sum={s}<br>dif={d}<br>pro={p}<br>quo={q}</html>'.format(s=s,d=d,p=p,q=q)
        #c = template.Context({'s':s, 'd':d, 'p':p, 'q':q})
    #return HttpResponse(t.render(c))
#    return render_to_response('math.html',{'s':s, 'd':d, 'p':p, 'q':q})
    return render_to_response('math.html',locals())

