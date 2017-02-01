import facebook
import requests
import os
from Tkinter import *
import tkMessageBox

from time import sleep
from time import strftime
from random import randint

from facebook import GraphAPIError
from pprint import pprint as pp

#GLOBALS VSTAVIT' KOD V access_token MEZHDU KAVYCHKAMI
access_token = 'Вставить свой токен'
errors=0


#FRAME

def takechecked():
    global grlist
    grlist[:]=[]
    for i in range(11):
        if eval('var'+str(i+1)+'.get()')!=0:
            grlist.append(eval('var'+str(i+1)+'.get()'))
    print grlist
    
def takeblogurl():
    global blogurl
    blogurl=url_entry.get()+' \n'
    print blogurl
    
def start():
    takechecked()
    takeblogurl()
    root.destroy()

def quitses():
    root.destroy()
    quit()
## frame

root = Tk()
root.title(u"Постинг Facebook для Дмитрия Леонова")
frame = Frame(root)
frame.grid(row=0, column=0)
frame2 = Frame(root, bd=5)
frame2.grid(row=0, column=1)
url_label = Label(frame2, width=25, text=u'Адрес внешней ссылки')
url_label.grid(row=1,column=0, sticky=N+W)
url_entry = Entry(frame2, width=50)
url_entry.grid(row=1, column=1, columnspan=2, sticky=E) #окошко ввода


paste_button = Button(frame2, text="Вставить ссылку из буффера", width=30,
                     command=lambda: frame2.focus_get().event_generate('<<Paste>>'))
paste_button.grid(row=0,column=1,padx=(100, 1), pady=(10,20)) 

var1=IntVar()
var2=IntVar()
var3=IntVar()
var4=IntVar()
var5=IntVar()
var6=IntVar()
var7=IntVar()
var8=IntVar()
var9=IntVar()
var10=IntVar()
var11=IntVar()

check1=Checkbutton(frame,   text=u'1HR',variable=var1,onvalue=1,offvalue=0)
check2=Checkbutton(frame,  text=u'2JOB',variable=var2,onvalue=2,offvalue=0)
check3=Checkbutton(frame,  text=u'3Coaching',variable=var3,onvalue=3,offvalue=0)
check4=Checkbutton(frame,  text=u'4Books',variable=var4,onvalue=4,offvalue=0)
check5=Checkbutton(frame,  text=u'5Reatail',variable=var5,onvalue=5,offvalue=0)
check6=Checkbutton(frame,  text=u'6Trainings',variable=var6,onvalue=6,offvalue=0)
check7=Checkbutton(frame,  text=u'7e-Retail',variable=var7,onvalue=7,offvalue=0)
check8=Checkbutton(frame,  text=u'8Контсалтинг',variable=var8,onvalue=8,offvalue=0)
check9=Checkbutton(frame,  text=u'9FMCG',variable=var9,onvalue=9,offvalue=0)
check10=Checkbutton(frame,  text=u'10Руководители',variable=var10,onvalue=10,offvalue=0)
check11=Checkbutton(frame,  text=u'11Переговоры',variable=var11,onvalue=11,offvalue=0)
grlist=[]
blogurl=''
for i in range(11):
    eval('check'+str(i+1)+'.grid(row='+str(i+3)+', column=0, sticky=W)')

eval_button = Button(frame2, text="Start", width=10,
                     command=start)
eval_button.grid(row=15,column=1, padx=(0,30), pady=(10,10)) #кнопка калькулейт

exit_button = Button(frame2, text="Exit", width=10,
                     command=quitses)
exit_button.grid(row=15, column=2,padx=(0,20), pady=(10,10))#кнопка выход



root.mainloop()


print 'G:',grlist
print 'B:',blogurl


##read all group urls
f = open('aliasfb.txt', 'r')
urllist= f.readlines()
f.close()
#print (urllist)
print ("\n\n")

##divide all on each special group
list1=[]
list2=[]
list3=[]
list4=[]
list5=[]
list6=[]
list7=[]
list8=[]
list9=[]
list10=[]
list11=[]
listerr=[]
for urlstr in urllist:
    if(urlstr[0:2]=='1/'):
        list1.append(urlstr[2:-2])
    if(urlstr[0:2]=='2/'):
        list2.append(urlstr[2:-2])
    if(urlstr[0:2]=='3/'):
        list3.append(urlstr[2:-2])
    if(urlstr[0:2]=='4/'):
        list4.append(urlstr[2:-2])
    if(urlstr[0:2]=='5/'):
        list5.append(urlstr[2:-2])
    if(urlstr[0:2]=='6/'):
        list6.append(urlstr[2:-2])
    if(urlstr[0:2]=='7/'):
        list7.append(urlstr[2:-2])
    if(urlstr[0:2]=='8/'):
        list8.append(urlstr[2:-2])
    if(urlstr[0:2]=='9/'):
        list9.append(urlstr[2:-2])
    if(urlstr[0:3]=='10/'):
        list10.append(urlstr[3:-2])
    if(urlstr[0:3]=='11/'):
        list11.append(urlstr[3:-2])


#FB API SDK
graph = facebook.GraphAPI(access_token)
def findidbyal(alias):
    info=graph.get_object('search', q=alias, type='group')
    group_id = info['data'][0]['id']
    return str(group_id)


def postlink(gid, link):
    global errors
    try:
        resp = graph.put_object(gid,'feed', link=link)
        print 'Post ID: '+resp['id']
    except GraphAPIError as e:
        errors=errors+1
        print 'Link: '+ link+' Error: '+str(e)


#POST TO GROUPS
for grnum in grlist:
    print grnum
    for gr in eval('list'+str(grnum)):
        try:
            int(gr)
            postlink(str(gr), blogurl)
            #print gr
            sleep(4)
        except ValueError:
            postlink(str(findidbyal(gr)), blogurl)
            #print findidbyal(gr)
            sleep(4)
#POST TO PROFILE

try:
    resp = graph.put_object('me','feed', link=blogurl)
    print 'Post ID: '+resp['id']
except GraphAPIError as e:
    errors=errors+1
    print 'Link: '+ blogurl+' Error: '+str(e)



if(errors):
    tkMessageBox.showwarning('Error', u'На каких-то страницах пост не сделан. Посмотрите лог работы.')



