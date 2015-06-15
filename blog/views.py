# -*- coding:utf-8 -*-
import json
import os
import time
import Image
from pydub import AudioSegment
from decimal import *
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout



from blog.models import User, Account,Queston

# Create your views here.
def index(request):
    return render(request,'blog/login.html','')

#验证用户是否登录及用户角色
def auth_login(request):
    username = request.session.get('username','anybody')
    role = request.session.get('role','anybody')
    if username and role:
        if role == 'user':
           return 1
        if role == 'admin':
           return 2
    else:
        return 0



def login(request):
    if request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        print username
        print password
        try:
            #compare with the Database
            uname=User.objects.filter(username=username,password=password)
            if uname:

                uname=User.objects.get(username=username,password=password)
                print uname.role
                request.session['username'] = username
                if uname.role == 'user':
                    request.session['role'] = 'user'
                    return render(request,'blog/addQuestion.html',{'user':username})
                if uname.role == 'admin':
                    request.session['role'] = 'admin'
                    return dashbord(request)
            else:
                print 'false'
                return render(request,'blog/login.html',{'login_result':'用户名密码错误!'})
        except Exception as e:
            print e


#@login_required
def logout(request):
    if auth_login(request) !=0:
        if request.session['username'] and request.session['role']:
            del request.session['username']
            del request.session['role']
    # 注销
    return render(request,'blog/login.html','')


#@login_required
def dashbord(request):
    if auth_login(request) ==2:
        resultArray=[]
        user=request.session.get('username','anybody')
        try:
            queslist=Queston.objects.all()
            id=1
            for item in queslist:
                #将类型解析成中文
                retype=''
                option=''

                imgattachsrc=""
                audattachsrc=""


                if item.type == '#addpicture':
                    retype='猜风景'
                    if item.attach:
                        imgattachsrc="../"+item.attach

                if item.type == '#addmusic':
                    retype='猜歌曲'
                    if item.attach:
                        audattachsrc="../"+item.attach

                if item.type == '#addidiom':
                    retype='猜成语'

                if item.adopt == 0:
                    status="待审"
                if item.adopt == 1:
                    status="通过"
                if item.adopt == -1:
                    status="否决"



                resultArray.append(
                    {'uid':item.id,'id': id, 'author':item.username,'type': retype,'title': item.title,'option':item.options,
                     'answer':item.answer,'imgattach':imgattachsrc,'audattach':audattachsrc,'adopt':status}
                )
                id=id+1
            print resultArray
        except Exception as e:
            print e
        return render(request,'blog/dashbord.html',{'question_list': resultArray,'user':user})
    else:
        return render(request,'blog/login.html','')




#@login_required
def myQuestion(request):
    if auth_login(request) ==1:
        resultArray=[]
        try:
            username=request.session.get('username','anybody')
            queslist=Queston.objects.filter(username=username)
            if queslist:
                id=1
                for item in queslist:
                    #将类型解析成中文
                    retype=''
                    option=''

                    imgattachsrc=""
                    audattachsrc=""


                    if item.type == '#addpicture':
                        retype='猜风景'
                        if item.attach:
                            imgattachsrc="../"+item.attach

                    if item.type == '#addmusic':
                        retype='猜歌曲'
                        if item.attach:
                            audattachsrc="../"+item.attach

                    if item.type == '#addidiom':
                        retype='猜成语'

                    if item.adopt == 0:
                        status="待审"
                    if item.adopt == 1:
                        status="通过"
                    if item.adopt == -1:
                        status="否决"



                    resultArray.append(
                        {'uid':item.id,'id': id, 'author':item.username,'type': retype,'title': item.title,'option':item.options,
                         'answer':item.answer,'imgattach':imgattachsrc,'audattach':audattachsrc,'adopt':status}
                    )
                    id=id+1
                print resultArray
        except Exception as e:
            print e
        return render(request,'blog/myQuestions.html',{'question_list': resultArray,'user':username})

    else:
        return render(request,'blog/login.html','')



def myAccount(request):
    if auth_login(request) ==1:
        resultArray={}
        try:
            username=request.session.get('username','anybody')
            account=Account.objects.get(username=username)
            nums=Queston.objects.filter(username=username).count()
            access=Queston.objects.filter(username=username,adopt=1).count()
            pend=Queston.objects.filter(username=username,adopt=0).count()
            deny=Queston.objects.filter(username=username,adopt=-1).count()
            if account:
                resultArray={'uid':account.id, 'author':account.username,'account':account.account,'nums':nums,'access':access,'pend':pend,'deny':deny}
        except Exception as e:
            print e
        return render(request,'blog/myAccount.html',{'myAccount': resultArray,'user':username})

    else:
        return render(request,'blog/login.html','')



def usermanage(request):
    if auth_login(request) ==2:
        username=request.session.get('username','anybody')
        resultArray=[]
        try:
            userlist=User.objects.filter(role='user')
            if userlist:
                id=1
                for item in userlist:
                    account=Account.objects.get(username=item)
                    nums=Queston.objects.filter(username=item).count()
                    access=Queston.objects.filter(username=item,adopt=1).count()
                    pend=Queston.objects.filter(username=item,adopt=0).count()
                    deny=Queston.objects.filter(username=item,adopt=-1).count()
                    resultArray.append({'uid':account.id, 'id':id,'author':account.username,'account':account.account,
                                        'nums':nums,'access':access,'pend':pend,'deny':deny})
                    id=id+1
                print resultArray
        except Exception as e:
            print e
        return render(request,'blog/manageUser.html',{'user_list': resultArray,'user':username})
    else:
        return render(request,'blog/login.html','')



def do_access(request):
    if request.method == 'POST':
        qid=request.POST.get('uid')
        print qid
        ques=Queston.objects.get(id=qid)
        account=Account.objects.get(username=ques.username)

        if ques and account:
            try:
                ques.adopt=1
                account.account=account.account+Decimal("0.1")
                ques.save()
                account.save()
                username = request.session.get('username','anybody')
                result={'data':'true'}
                jresult=json.dumps(result)
                return HttpResponse(jresult)
            except Exception as e:
                print e


def do_deny(request):
    if request.method == 'POST':
        qid=request.POST.get('uid')
        ques=Queston.objects.get(id=qid)
        account=Account.objects.get(username=ques.username)
        if ques and account:
            if account.account>0:
                try:
                    ques.adopt=-1
                    ques.save()
                    account.account=account.account-Decimal("0.1")
                    account.save()
                    username = request.session.get('username','anybody')
                except Exception as e:
                    print e
            result={'data':'true'}
            jresult=json.dumps(result)
            return HttpResponse(jresult)



def registerPage(request):
    return render(request,'blog/register.html','')




def register(request):
    if request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        print username
        print password
        #compare with the Database
        try:
            if User.objects.filter(username=username):
                return render(request,'blog/register.html',{'result':'registered'})
            user = User(username=username, password=password,role='user')
            user.save()
            account=Account(username=user,account=0.00)
            account.save()
            return render(request,'blog/success.html',{'user':user})
        except Exception as e:
            print e
            return render(request,'blog/register.html',{'result':'error'})


#@login_required
def addQuestion(request):
    if auth_login(request) == 1:
        username = request.session.get('username','anybody')
        return render(request,'blog/addQuestion.html',{'user':username})
    else:
        return render(request,'blog/login.html','')

def do_addQuestion(request):
    type=request.POST.get('type', '')
    title = request.POST.get('title', '')
    optionA = request.POST.get('optionA', '')
    optionB = request.POST.get('optionB', '')
    optionC = request.POST.get('optionC', '')
    optionD = request.POST.get('optionD', '')
    answer = request.POST.get('answer', '')
    attachment = request.POST.get('attach', '')


    #option={'A':optionA,'B':optionB,'C':optionC,'D':optionD}
    #optionlist=json.dumps(option, encoding='UTF-8', ensure_ascii=False)
    #optionlist="{'A':"+optionA+",'B':"+optionB+",'C':"+optionC+",'D':"+optionD+"}"
    optionlist="A:"+optionA+"<br>B:"+optionB+"<br>C:"+optionC+"<br>D:"+optionD
    adopt=0

    user = request.session.get('username','anybody')
    username=user


    try:
        uname=User.objects.get(username=username)
        que=Queston(username=uname,type=type,title=title,options=optionlist,answer=answer,attach=attachment,adopt=adopt)
        que.save()
        result={'data':'true'}
        jresult=json.dumps(result)
        return HttpResponse(jresult)
    except Exception as e:
        print e


#上传文件，返回文件路径
def do_upload(request):
  if request.method == 'POST':
      type = request.POST.get('type')
      file = request.FILES.get("file_data",None)

      if file and type:
          mediafile=handle_uploaded_file(file,type)
          result={'files':mediafile}
          jresult=json.dumps(result)
      return HttpResponse(jresult)



#上传文件，返回文件路径
def do_imgreplace(request):
  print "start replace:"
  if request.method == 'POST':
      marginTop=0
      marginLeft=0
      width=0
      height=0
      file_name = request.POST.get('imgfile')[3:]
      print file_name
      marginTop= int(float(request.POST.get('marginTop')))
      marginLeft= int(float(request.POST.get('marginLeft')))
      width= int(float(request.POST.get('width')))
      height= int(float(request.POST.get('height')))
      # marginTop=int(request.POST.get('marginTop'))
      # print marginTop
      # marginLeft=int(request.POST.get('marginLeft'))
      # print marginLeft
      # width=int(request.POST.get('width'))
      # print width
      # height=int(request.POST.get('height'))
      #print height
      #剪切
      try:
          originfile=Image.open(file_name)
          xsize,ysize=originfile.size
          print 'image size:'+str(xsize)+":"+str(ysize)
          #box变量是一个四元组(左，上，右，下)。
          box=(marginLeft,marginTop,marginLeft+width,marginTop+height)
          print box
          originfile.crop(box).save(file_name)
      except Exception, e:
          print e
      result={'files':file_name}
      jresult=json.dumps(result)

      return HttpResponse(jresult)


def handle_uploaded_file(f,type):
    file_name = ""

    try:
        print str(type)
        if type =='picture':

            path = "media/picture" + time.strftime('/%Y-%m-%d/')
        else:
            path = "media/audio" + time.strftime('/%Y-%m-%d/')
        if not os.path.exists(path):
            os.makedirs(path)
        file_name = path + f.name
        if not os.path.exists(file_name):
            destination = open(file_name, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()

        if type =='picture':
            if os.path.exists(file_name):
                #获取文件扩展名
                file_ext=file_name[file_name.rfind('.'):]
                if file_ext != '.png':
                    file_png=file_name[:file_name.rfind('.')]+'.png'
                    try:
                        #用PIL库将图片转换成png格式
                        originfile=Image.open(file_name)
                        originfile.save(file_png)
                        #删除原图片
                        os.remove(file_name)
                        file_name=file_png



                    except Exception, e:
                        print e
        else:
            ##音乐，截取10秒
            if os.path.exists(file_name):
                #获取文件扩展名
                file_pre=file_name[:file_name.rfind('.')]

                try:
                    song1 = AudioSegment.from_file(file_name)
                    #用更换文件
                    file_name=file_pre+"-10.mp3"
                    song1 = song1[0:10000]
                    song1.export(file_name, format="mp3")
                    #删除原文件
                    #os.remove(file_name)
                except Exception, e:
                    print e
    except Exception, e:
        print e

    return file_name
