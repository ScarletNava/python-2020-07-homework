#调用实例在main.py
import tkinter as tk
import tkinter.filedialog
import tkinter.colorchooser
from tkinter import ttk
import tkinter.messagebox
import math
import threading

def GetPictureName(path):
    '''
    #内部函数
    #获取全部图片名称
    #path：文件夹的相对路径或绝对路径 images\\"或d:\\Users\\Scarlet\\Desktop\\wallpaper\\images\\
    #返回值：文件名列表
    '''
    import os
    import re
    i=1
    NameList=[]
    for filename in os.listdir(path):#对目录下的文件进行遍历
        if os.path.isfile(os.path.join(path,filename))==True:#判断是否是文件
            file=os.path.splitext(filename)# 将文件名与后缀分割开 file[0]为文件名 file[1]为文件后缀
            if file[1]==".png"or file[1]==".jpg"or file[1]==".jpeg"or file[1]==".bmp"or file[1]==".gif":
               NameList.append(filename)
    return NameList

def GetAbsolutePath():
    '''
    #获取当前py文件的绝对路径 
    #返回值：当前py文件所在文件夹的绝对路径 d:\\Users\\Scarlet\\Desktop\\wallpaper
    '''
    abs_file=__file__
    abs_dir=abs_file[:abs_file.rfind("\\")]
    return abs_dir

def ChangePictureOnce(picturename):
    '''
    #内部函数
    #更换一次壁纸 
    #picturename：必须为图片的绝对路径
    '''
    import ctypes
    ctypes.windll.user32.SystemParametersInfoW(20, 0, picturename, 0)
   
def GetPictureRandom(path): 
    '''
    #内部函数
    #随机选取一张壁纸
    #path：必须为文件夹的绝对路径 如d:\\Users\\Scarlet\\Desktop\\wallpaper\\images\\
    #返回值：选取壁纸的绝对路径
    '''
    
    import ctypes
    import random
    Namelist=GetPictureName(path)
    number=Namelist.__len__()
    i=random.randint(1,number)
    picturename=path+Namelist[i-1]
    #ctypes.windll.user32.SystemParametersInfoW(20, 0, picturename, 0)
    return picturename

def ControlMySpider(keyword):
    '''
    此函数为内部函数  返回pn/30
    '''
    import os
    import re
    num=12#这是keyword的总数
    try:
        fp=open("data\data1.txt",'r+')
    except  FileNotFoundError:
        fp=open("data\data1.txt",'w+')
        fp.write("高清壁纸1\r动漫1\r风景1\r唯美1\r可爱1\r小清新1\r宠物1\r影视1\r游戏1\r植物1\r明星1\r名车1\r")
        fp.close()
        return 1
    data=fp.readlines()
    wordlist=[]
    numlist=[]
    for i in range(num):
            wordlist.append(re.findall(r'[\u4e00-\u9fa5]+',data[i])[0])
            numlist.append(re.findall(r'\d+',data[i])[0])
    number=0
    for i in range(num):
        if wordlist[i]==keyword:
            numlist[i]=str(int(numlist[i])+1)
            number=numlist[i]
    fp.seek(0)
    for i in range(num):
        fp.write(str(wordlist[i])+str(numlist[i])+'\r')
    fp.close()
    return number
        
def mySpider(keyword,path,width='', height=''):
    '''
    根据关键字从百度图片里获取指定规格的壁纸
    :param keyword:关键字，想要搜索的内容
    :param path:保存壁纸的地址
    :param width:壁纸规格，宽度
    :param height:壁纸规格，长度
    :return:无
    '''

    import requests
    import re
    number=int(int(ControlMySpider(keyword))*30)
    print(number)

    url = "https://image.baidu.com/search/index?tn=baiduimage&width=" + str(width)
    url += '&height=' + str(height) + '&word=' + str(keyword) + '&pn=' + str(number)
    print(url)

    response = requests.get(url)
    html = response.text
    pic_url=re.findall('"objURL":"(.*?)",',html,re.S)
    num=0
    for each in pic_url:
        try:
            if each is not None:
                if num < number:
                    pic=requests.get(each)
                    fpstring=path+r'\\'+str(num)+'.jpg'
                    with open(fpstring,'wb') as fp:
                        fp.write(pic.content)
            else:
                continue
        except BaseException:
            continue
        num+=1

def playmusic(musicname):
    '''
    #内部函数
    #播放音乐 musicname为歌曲路径，如：r"E:\Data\cloudmusic\潜鸟鸣 - Grand.mp3"
    '''
    import time
    import eyed3
    import pygame
    pygame.mixer.init()
    pygame.mixer.music.load(musicname)
    pygame.mixer.music.play(start=0.0)
    secs=int(eyed3.load(musicname).info.time_secs)
    time.sleep(secs)
    pygame.mixer.music.stop()

def choosemusic(path):
    '''
    #选取音乐 path为文件夹路径如："E:\\Data\\cloudmusic"
    '''
    import os
    import re
    for filename in os.listdir(path):#对目录下的文件进行遍历
        if os.path.isfile(os.path.join(path,filename))==True:#判断是否是文件
            file=os.path.splitext(filename)# 将文件名与后缀分割开 file[0]为文件名 file[1]为文件后缀
            if file[1]==".mp3"or file[1]==".flac"or file[1]==".cda"or file[1]==".m4a"or file[1]==".wav":
               playmusic(os.path.join(path,filename))
    
def GetTime():
    '''
    #内部函数
    #获取时间日期函数
    #返回值为字典 {'日期': '2020-05-09', '时间': '17:45:15'}
    '''
    import time
    dictTime={
        "日期":time.strftime("%Y年%m月%d日", time.localtime()),
        "时间":time.strftime("%H:%M",time.localtime())
    }
    return dictTime

def GetHitokotoApi(key):
    '''
    #内部函数
    #获取一言函数
    #返回值为字典 {'句子': '人生最糟糕的事，一个是饿肚子，一个是孤独。', '作者': '夏日大作战'}
    '''
    import requests
    import json
    url = 'https://v1.hitokoto.cn?c=' + key + '&encode=json&charset=utf-8'
    r = requests.get(url)
    data = json.dumps(r.json())
    data = json.loads(data)
    dictHitokoto={
        "句子":data['hitokoto'],
        "作者":data['from']
    }
    return dictHitokoto

def PrintPicture(picturename,key,a,b,c,d,wordcolor,timecolor):
    '''
    #内部函数   添加文字设置壁纸函数  
    #picturename:图片名称 绝对路径
    #key:一言关键字(str) a：动画 b：漫画 c：游戏 d：文学 e：原创 f：来自网络 g：其他 h：影视 i：诗词 j：网易云 k：哲学 l：抖机灵
    #a:一言横坐标,int
    #b:一言纵坐标,int
    #c:时间横坐标,int
    #d:时间纵坐标,int
    #wordcolor:一言rgb颜色
    #timecolor:时间颜色
    '''
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont #pip install Image
    tempname=GetAbsolutePath()+"\\temp\\temp.png"
    DictHitokoto=GetHitokotoApi(key)
    iflength=False
    while iflength==False:
        if len(DictHitokoto['句子'])<=25:
            iflength=True
        else:
            DictHitokoto=GetHitokotoApi(key)
    time=GetTime()
    Word={
        1:DictHitokoto["句子"],
        2:'By:'+DictHitokoto["作者"],
        3:time["日期"],
        4:time["时间"]
    }
    img = cv2.imread(picturename)
    picwidth=img.shape[1]
    picheight=img.shape[0]
    sys=GetSystemResolution()
    syswidth=sys[0]
    sysheight=sys[1]
    img=cv2.resize(img,(syswidth*2,sysheight*2),)
    #print(syswidth)
    ratio=1080/sysheight/2
    #print(ratio)
    position=(
        40/ratio,
        880/ratio,
        syswidth-130/ratio,#/ratio,
        #syswidth,
        440/ratio,
        40/ratio,
        75/ratio)
    Font={#字号
        1:ImageFont.truetype('simhei.ttf',int(30/ratio),encoding="utf-8"),#文字
        2:ImageFont.truetype('simhei.ttf',int(25/ratio),encoding="utf-8"),#作者
        3:ImageFont.truetype('simhei.ttf',int(25/ratio),encoding="utf-8"),#日期
        4:ImageFont.truetype('simhei.ttf',int(100/ratio),encoding="utf-8")#时间
    }

    img_PIL = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_PIL)
    #调节相对位置
    draw.text((position[0]+a+1,position[1]+b+1),Word[1],font=Font[1],fill=(0,0,0))#文字
    draw.text((position[0]+a,position[1]+b),Word[1],font=Font[1],fill=wordcolor)#文字

    draw.text((position[0]+a+1,position[1]+b+position[4]+1),Word[2],font=Font[2],fill=(0,0,0))#作者
    draw.text((position[0]+a,position[1]+b+position[4]),Word[2],font=Font[2],fill=wordcolor)#作者

    draw.text((position[0]+a+1,position[1]+b+position[5]+1),Word[3],font=Font[3],fill=(0,0,0))#日期
    draw.text((position[0]+a,position[1]+b+position[5]),Word[3],font=Font[3],fill=wordcolor)#日期

    draw.text((position[2]+c+1,position[3]+d+1),Word[4],font=Font[4],fill=(0,0,0))#时间
    draw.text((position[2]+c,position[3]+d),Word[4],font=Font[4],fill=timecolor)#时间
    img = cv2.cvtColor(np.asarray(img_PIL),cv2.COLOR_RGB2BGR)
    cv2.imwrite(tempname,img)
    ChangePictureOnce(tempname)


def WritePictureName(picturename):
    import os
    try:
        fp=open("data\data2.txt",'r+')
        fp.close()
        os.remove("data\data2.txt")
        fp=open("data\data2.txt",'w+')
    except  FileNotFoundError:
        fp=open("data\data2.txt",'w+')
    fp.write(picturename)
    fp.close()

def SetWallpaper(filename,retime,key,a,b,c,d,wordcolor,timecolor):
    '''
    #更换多张壁纸 控制时间设置壁纸函数
    #filename:retime不为0时为壁纸所在目录绝对路径,末尾带斜杠  retime为0是为图片绝对路径
    #retime不为0时为更换时间，单位为秒 大概  为0是为更换一张壁纸
    #key:一言关键字(str) a：动画 b：漫画 c：游戏 d：文学 e：原创 f：来自网络 g：其他 h：影视 i：诗词 j：网易云 k：哲学 l：抖机灵
    #a:一言横坐标,int
    #b:一言纵坐标,int
    #c:时间横坐标,int
    #d:时间纵坐标,int
    #wordcolor:一言rgb颜色
    #timecolor:时间颜色
    '''
    import time
    if retime!=0:
        while True:
            picturename=GetPictureRandom(filename)
            print(picturename)
            ThisTime=time.strftime("%H:%M",time.localtime())
            PrintPicture(picturename,key,a,b,c,d,wordcolor,timecolor)
            WritePictureName(picturename)
            for i in range(retime):
                if ThisTime!=time.strftime("%H:%M",time.localtime()):
                    PrintPicture(picturename,key,a,b,c,d,wordcolor,timecolor)
                    ThisTime=time.strftime("%H:%M",time.localtime())
                    WritePictureName(picturename)
                    i=i+1
                else:
                    time.sleep(1)
    else:
        picturename=filename
        ThisTime=time.strftime("%H:%M",time.localtime())
        PrintPicture(picturename,key,a,b,c,d,wordcolor,timecolor)
        while True:
            if ThisTime!=time.strftime("%H:%M",time.localtime()):
                PrintPicture(picturename,key,a,b,c,d,wordcolor,timecolor)
                ThisTime=time.strftime("%H:%M",time.localtime())
            else:
                time.sleep(1)

def GetSystemResolution():
    import tkinter
    win=tkinter.Tk()
    x=win.winfo_screenwidth()
    y=win.winfo_screenheight()
    return x,y

def MyFavorite(newpath):
    '''
    #newpath为保存收藏图片所在文件夹路径
    #可以设置初值：newpath=GetAbsolutePath()+'\\myfavorites\\'
    '''
    import os
    import shutil
    fp=open("data\data2.txt",'r')
    picturename=fp.read()
    shutil.copy(picturename,newpath)
    fp.close()
#------------------------------------------------------------------

def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建

    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()

def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def select(windowName,key,a,b,c,d,wordcolor,timecolor,times=0):
    '''
    根据调用函数的窗口执行获取文件路径或文件夹路径并执行相应的操作
    :param windowName: 调用窗口名
    :param key: 一言关键字(str) a：动画 b：漫画 c：游戏 d：文学 e：原创 f：来自网络 g：其他 h：影视 i：诗词 j：网易云 k：哲学 l：抖机灵
    :param a: 一言横坐标,int
    :param b: 一言纵坐标,int
    :param c: 时间横坐标,int
    :param d: 时间纵坐标,int
    :param wordcolor: 一言rgb颜色，tuple
    :param timecolor: 时间rgb颜色tuple
    :param times: 不为0时为更换时间，单位为秒   为0是为更换一张壁纸
    :return:
    '''
    if windowName=='更换壁纸':
        fileName = tk.filedialog.askopenfilename()#获取壁纸路径
        if is_contain_chinese(fileName):
            tk.messagebox.showwarning('警告','壁纸路径必须为纯英文！')
        else:
            thread_it(SetWallpaper,fileName,0,key,a,b,c,d,wordcolor,timecolor)
            #print(windowName,fileName,key,a,b,c,d,wordcolor,timecolor)
    elif windowName=='随机切换':
        pathName=tk.filedialog.askdirectory()#获取文件夹路径
        if is_contain_chinese(pathName):
            tk.messagebox.showwarning('警告','文件夹路径必须为纯英文！')
        else:
            thread_it(SetWallpaper,pathName+'/',times,key,a,b,c,d,wordcolor,timecolor)
            print(times,pathName)

def changeR():
    tk.messagebox.showinfo('提示', '轮换类操作只有主页面关闭后才会结束')
    randPage=tk.Toplevel()
    randPage.geometry('400x300')
    randPage.title('随机切换')
    randPage.resizable(0,0)

    def askColor(text):
        try:
            color = tk.colorchooser.askcolor()
            if text == '选择一言颜色':
                wordColor[0] = math.floor(color[0][0])  # 向下取整
                wordColor[1] = math.floor(color[0][1])  # 向下取整
                wordColor[2] = math.floor(color[0][2])  # 向下取整
                Label2['fg'] = color[1]
            elif text == '选择时间颜色':
                timeColor[0] = math.floor(color[0][0])  # 向下取整
                timeColor[1] = math.floor(color[0][1])  # 向下取整
                timeColor[2] = math.floor(color[0][2])  # 向下取整
                Label3['fg'] = color[1]
        except TypeError:
            pass

    def countTime(value):
        try:
            if int(value) <= 10:
                ttime = 10 + int(value) * 5
                list[0]=ttime
                label7['text'] = str(ttime)+'s'
            elif int(value) <= 20:
                ttime = (int(value) - 10) * 180
                list[0]=ttime
                label7['text'] = str(ttime // 60) + 'min'
            else:
                ttime = 1800 + (int(value) - 20) * 600
                list[0] = ttime
                label7['text'] = str(ttime // 60) + 'min'
        except BaseException:
            print("没有选择项")

    ttime=10
    list=[10]
    defaultValueX1 = tk.IntVar()
    defaultValueY1 = tk.IntVar()
    defaultValueX2 = tk.IntVar()
    defaultValueY2 = tk.IntVar()

    label1 = tk.Label(randPage,text='一言横坐标').grid(row=0,column=0)
    ent1   = tk.Entry(randPage,width=10,textvariable=defaultValueX1)
    ent1.insert(0,0)
    ent1.grid(row=0,column=1,pady=5)#一言x

    label2 = tk.Label(randPage, text='一言纵坐标').grid(row=0, column=2)
    ent2   = tk.Entry(randPage,width=10,textvariable=defaultValueY1)
    ent2.insert(0,0)
    ent2.grid(row=0,column=3,pady=5)#一言y

    label3 = tk.Label(randPage, text='时间横坐标').grid(row=1, column=0)
    ent3   = tk.Entry(randPage,width=10,textvariable=defaultValueX2)
    ent3.insert(0,0)
    ent3.grid(row=1,column=1,pady=5)#时间x

    label4 = tk.Label(randPage, text='时间纵坐标').grid(row=1, column=2)
    ent4   = tk.Entry(randPage,width=10,textvariable=defaultValueY2)
    ent4.insert(0,0)
    ent4.grid(row=1,column=3,pady=5)#时间y

    label5 = tk.Label(randPage,text='一言主题').grid(row=2,column=0)
    cmb    = ttk.Combobox(randPage,width=10)
    cmb['value']=('动画','漫画','游戏','文学','原创','来自网络','其他','影视','诗词','网易云','哲学','抖机灵')
    cmb.current(0)
    cmb.grid(row=2,column=1,pady=5)

    label6=tk.Label(randPage,text='切换间隔').grid(row=3,column=0,pady=5)
    scale = tk.Scale(randPage, from_=0, to=23, orient=tk.HORIZONTAL, length=200, showvalue=0, resolution=1,command=countTime)
    scale.grid(row=3, column=1, columnspan=2, pady=5)
    label7 = tk.Label(randPage, text='10s')
    label7.grid(row=3, column=3)

    #Label1 = tk.Label(randPage, text='点击按钮以选择壁纸').grid(row=5,column=0)#tkinter colorchooser选颜色 combobox下拉单选框
    btn1 = tk.Button(randPage, text='选择文件夹',bg='SkyBlue',command=lambda :select(randPage.title(),chr(cmb.current()+97),int(ent1.get()),int(ent2.get()),int(ent3.get()),int(ent4.get()),tuple(wordColor),tuple(timeColor),times=list[0])).grid(row=6,column=1,pady=5)

    wordColor=[255,255,255]
    btn2 = tk.Button(randPage, text='选择一言颜色', bg='#82c4c3', command=lambda: askColor(btn2['text']))
    btn2.grid(row=4, column=0, pady=5)
    Label2 = tk.Label(randPage, text='文字效果预览')
    Label2.grid(row=5, column=0, pady=5)

    timeColor=[255,255,255]
    btn3 = tk.Button(randPage, text='选择时间颜色', bg='#f37121', command=lambda: askColor(btn3['text']))
    btn3.grid(row=4, column=2, pady=5)
    Label3 = tk.Label(randPage, text='时间效果预览')
    Label3.grid(row=5, column=2, pady=5)

    label8=tk.Label(randPage,text='为获得最佳体验，建议坐标设置为默认值\nPS:屏幕中心为原点，路径必须为纯英文',fg='red').grid(row=7,column=1,columnspan=2,pady=20)

    randPage.mainloop()

def changeO():
    tk.messagebox.showinfo('提示', '轮换类操作只有主页面关闭后才会结束')
    oncePage=tk.Toplevel()
    oncePage.geometry('400x300')
    oncePage.title('更换壁纸')
    oncePage.resizable(0,0)

    def askColor(text):
        try:
            color = tk.colorchooser.askcolor()
            if text == '选择一言颜色':
                wordColor[0] = math.floor(color[0][0])  # 向下取整
                wordColor[1] = math.floor(color[0][1])  # 向下取整
                wordColor[2] = math.floor(color[0][2])  # 向下取整
                Label2['fg'] = color[1]
            elif text == '选择时间颜色':
                timeColor[0] = math.floor(color[0][0])  # 向下取整
                timeColor[1] = math.floor(color[0][1])  # 向下取整
                timeColor[2] = math.floor(color[0][2])  # 向下取整
                Label3['fg'] = color[1]
        except TypeError:
            pass

    defaultValueX1 = tk.IntVar()
    defaultValueY1 = tk.IntVar()
    defaultValueX2 = tk.IntVar()
    defaultValueY2 = tk.IntVar()

    label1 = tk.Label(oncePage,text='一言横坐标').grid(row=0,column=0)
    ent1   = tk.Entry(oncePage,width=10,textvariable=defaultValueX1)
    ent1.insert(0,0)
    ent1.grid(row=0,column=1,pady=5)#一言x

    label2 = tk.Label(oncePage, text='一言纵坐标').grid(row=0, column=2)
    ent2   = tk.Entry(oncePage,width=10,textvariable=defaultValueY1)
    ent2.insert(0,0)
    ent2.grid(row=0,column=3,pady=5)#一言y

    label3 = tk.Label(oncePage, text='时间横坐标').grid(row=1, column=0)
    ent3   = tk.Entry(oncePage,width=10,textvariable=defaultValueX2)
    ent3.insert(0,0)
    ent3.grid(row=1,column=1,pady=5)#时间x

    label4 = tk.Label(oncePage, text='时间纵坐标').grid(row=1, column=2)
    ent4   = tk.Entry(oncePage,width=10,textvariable=defaultValueY2)
    ent4.insert(0,0)
    ent4.grid(row=1,column=3,pady=5)#时间y

    label5 = tk.Label(oncePage,text='一言主题').grid(row=2,column=0)
    cmb    = ttk.Combobox(oncePage,width=10)
    cmb['value']=('动画','漫画','游戏','文学','原创','来自网络','其他','影视','诗词','网易云','哲学','抖机灵')
    cmb.current(0)
    cmb.grid(row=2,column=1,pady=5)

    #Label1 = tk.Label(oncePage, text='点击按钮以选择壁纸').grid(row=5,column=0)#tkinter colorchooser选颜色 combobox下拉单选框
    btn1 = tk.Button(oncePage, text='选择壁纸',bg='SkyBlue',command=lambda :select(oncePage.title(),chr(cmb.current()+97),int(ent1.get()),int(ent2.get()),int(ent3.get()),int(ent4.get()),tuple(wordColor),tuple(timeColor))).grid(row=5,column=1,pady=5)

    wordColor=[0,0,0]
    btn2 = tk.Button(oncePage, text='选择一言颜色', bg='#82c4c3', command=lambda: askColor(btn2['text']))
    btn2.grid(row=3, column=0, pady=5)
    Label2 = tk.Label(oncePage, text='文字效果预览')
    Label2.grid(row=4, column=0, pady=5)

    timeColor=[0,0,0]
    btn3 = tk.Button(oncePage, text='选择时间颜色', bg='#f37121', command=lambda: askColor(btn3['text']))
    btn3.grid(row=3, column=2, pady=5)
    Label3 = tk.Label(oncePage, text='时间效果预览')
    Label3.grid(row=4, column=2, pady=5)

    label6=tk.Label(oncePage,text='为获得最佳体验，建议坐标设置为默认值\nPS:屏幕中心为原点，路径必须为纯英文',fg='red').grid(row=6,column=1,columnspan=2,pady=50)
    oncePage.mainloop()

def searchFromWeb():
    tk.messagebox.showinfo('提示','获取壁纸需要一定的时间，请耐心等待')
    searchPage = tk.Toplevel()
    searchPage.geometry('400x400')
    searchPage.title('网络获取')
    searchPage.resizable(0,0)
    def countTime(value):
        try:
            if int(value) <= 10:
                ttime = 10 + int(value) * 5
                list[0]=ttime
                label7['text'] = str(ttime)+'s'
            elif int(value) <= 20:
                ttime = (int(value) - 10) * 180
                list[0]=ttime
                label7['text'] = str(ttime // 60) + 'min'
            else:
                ttime = 1800 + (int(value) - 20) * 600
                list[0] = ttime
                label7['text'] = str(ttime // 60) + 'min'
        except BaseException:
            print("没有选择项")

    def combo(keyword, width, height,times,key,a,b,c,d,wordcolor,timecolor):
        tipLabel['text'] = '请稍等。。。'
        pathName = 'webimages'  # 获取文件夹路径
        AbsPathName=GetAbsolutePath()+'\\webimages\\'
        print(AbsPathName)
        mySpider(keyword, pathName, width, height)  # 获取壁纸
        tk.messagebox.showinfo('完成','壁纸获取完毕')
        tipLabel['text']='壁纸获取完毕'
        thread_it(SetWallpaper,AbsPathName,times,key,a,b,c,d,wordcolor,timecolor)


    def askColor(text):
        try:
            color = tk.colorchooser.askcolor()
            if text == '选择一言颜色':
                wordColor[0] = math.floor(color[0][0])  # 向下取整
                wordColor[1] = math.floor(color[0][1])  # 向下取整
                wordColor[2] = math.floor(color[0][2])  # 向下取整
                Label2['fg'] = color[1]
            elif text == '选择时间颜色':
                timeColor[0] = math.floor(color[0][0])  # 向下取整
                timeColor[1] = math.floor(color[0][1])  # 向下取整
                timeColor[2] = math.floor(color[0][2])  # 向下取整
                Label3['fg'] = color[1]
        except TypeError:
            pass

    ttime=10
    list=[10]
    defaultValueX1 = tk.IntVar()
    defaultValueY1 = tk.IntVar()
    defaultValueX2 = tk.IntVar()
    defaultValueY2 = tk.IntVar()

    label1 = tk.Label(searchPage,text='一言横坐标').grid(row=2,column=0)
    ent1   = tk.Entry(searchPage,width=10,textvariable=defaultValueX1)
    ent1.insert(0,0)
    ent1.grid(row=2,column=1,pady=5)#一言x

    label2 = tk.Label(searchPage, text='一言纵坐标').grid(row=2, column=2)
    ent2   = tk.Entry(searchPage,width=10,textvariable=defaultValueY1)
    ent2.insert(0,0)
    ent2.grid(row=2,column=3,pady=5)#一言y

    label3 = tk.Label(searchPage, text='时间横坐标').grid(row=3, column=0)
    ent3   = tk.Entry(searchPage,width=10,textvariable=defaultValueX2)
    ent3.insert(0,0)
    ent3.grid(row=3,column=1,pady=5)#时间x

    label4 = tk.Label(searchPage, text='时间纵坐标').grid(row=3, column=2)
    ent4   = tk.Entry(searchPage,width=10,textvariable=defaultValueY2)
    ent4.insert(0,0)
    ent4.grid(row=3,column=3,pady=5)#时间y

    label5 = tk.Label(searchPage,text='一言主题').grid(row=4,column=0)
    cmb    = ttk.Combobox(searchPage,width=10)
    cmb['value']=('动画','漫画','游戏','文学','原创','来自网络','其他','影视','诗词','网易云','哲学','抖机灵')
    cmb.current(0)
    cmb.grid(row=4,column=1,pady=5)

    label6 = tk.Label(searchPage, text='切换间隔').grid(row=5, column=0, pady=5)
    scale = tk.Scale(searchPage, from_=0, to=23, orient=tk.HORIZONTAL, length=200, showvalue=0, resolution=1,
                     command=countTime)
    scale.grid(row=5, column=1, columnspan=2, pady=5)
    label7 = tk.Label(searchPage, text='10s')
    label7.grid(row=5, column=3)

    wordColor=[255,255,255]
    btn2 = tk.Button(searchPage, text='选择一言颜色', bg='#82c4c3',command=lambda: askColor(btn2['text']))
    btn2.grid(row=6, column=0, pady=5)
    Label2 = tk.Label(searchPage, text='文字效果预览')
    Label2.grid(row=7, column=0, pady=5)

    timeColor=[255,255,255]
    btn3 = tk.Button(searchPage, text='选择时间颜色', bg='#f37121',command=lambda: askColor(btn3['text']))
    btn3.grid(row=6, column=2, pady=5)
    Label3 = tk.Label(searchPage, text='时间效果预览')
    Label3.grid(row=7, column=2, pady=5)

    keyLabel=tk.Label(searchPage,text='请选择关键字').grid(row=0,column=0)
    S_cmb1=ttk.Combobox(searchPage,width=10)#获取关键字
    S_cmb1['value']=('动漫','风景','高清壁纸','唯美','可爱','小清新','宠物','影视','游戏','植物','明星','名车')
    S_cmb1.current(0)

    widthLabel=tk.Label(searchPage,text='请输入壁纸的宽度').grid(row=1,column=0)
    S_ent2 = tk.Entry(searchPage, width=10)#获取宽度
    S_ent2.insert(0,1920)

    heightLabel = tk.Label(searchPage, text='高度').grid(row=1,column=2)
    S_ent3 = tk.Entry(searchPage, width=10)#获取高度
    S_ent3.insert(0,1080)

    S_btn1=tk.Button(searchPage,text='点击获取',bg='SkyBlue',command=lambda :combo(S_cmb1.get(),str(S_ent2.get()),str(S_ent3.get()),list[0],chr(cmb.current()+97),int(ent1.get()),int(ent2.get()),int(ent3.get()),int(ent4.get()),tuple(wordColor),tuple(timeColor)))
    S_cmb1.grid(row=0,column=1,pady=5)
    #ent2.grid(row=1,column=1)
    S_ent2.grid(row=1,column=1)
    S_ent3.grid(row=1,column=3)
    S_btn1.grid(row=10,column=1,pady=5)
    S_btn_save=tk.Button(searchPage,text='收藏当前壁纸',bg='#eb6383',command=lambda :MyFavorite(GetAbsolutePath()+'\\myfavorites\\')).grid(row=11,column=1,pady=5)

    psLabel=tk.Label(searchPage,text='为获得最佳体验，建议坐标设置为默认值\nPS:屏幕中心为原点，路径必须为纯英文',fg='red').grid(row=12,column=1,pady=5,columnspan=2)

    tipLabel=tk.Label(searchPage,text='',fg='Violet')
    tipLabel.grid(row=10,column=2)


    searchPage.mainloop()

def NoteBook():
    NotePage=tk.Toplevel()
    NotePage.geometry('400x500')
    NotePage.title('备忘录')
    NotePage.resizable(0,0)

    def create(thing,time,pos):
        thl='事件：'
        tml='时间：'
        fg='#ffffff'
        if pos == 0:
            x = 4
            thl = 'No.1 ' + thl
            fg = '#d92027'
        elif pos == 1:
            x = 5
            thl = 'No.2 ' + thl
            fg='#ff9c71'
        elif pos == 2:
            x = 6
            thl = 'No.3 ' + thl
            fg = '#fbd46d'
        elif pos == 3:
            x = 7
            thl = 'No.4 ' + thl
            fg = '#32e0c4'
        elif pos == 4:
            x = 8
            thl = 'No.5 ' + thl
            fg = '#f54291'
        frm=tk.Frame(NotePage)
        thlabel1=tk.Label(frm,text=thl,fg=fg).grid(row=0,column=0)
        thlabel2=tk.Label(frm,text=thing,fg=fg).grid(row=0,column=1)
        tmlabel1=tk.Label(frm,text=tml,fg=fg).grid(row=1,column=0)
        tmlabel2=tk.Label(frm,text=time,fg=fg).grid(row=1,column=1,pady=3)
        frm.grid(row=x,column=1)

    label1 = tk.Label(NotePage,text='提醒事件').grid(row=0,column=0)
    ent1   = tk.Entry(NotePage,width=20)#输入事件
    label2 = tk.Label(NotePage,text='提醒时间').grid(row=1,column=0)
    ent2   = tk.Entry(NotePage,width=20)#输入提醒时间
    btn1   = tk.Button(NotePage,text='添加',command=lambda :create(ent1.get(),ent2.get(),cmb.current())).grid(row=3,column=1)
    label2 = tk.Label(NotePage,text='优先级').grid(row=2,column=0)

    ClockPho   = tk.PhotoImage(file='img/闹钟.png')
    ClockLabel = tk.Label(NotePage, image=ClockPho).grid(row=0, column=2,columnspan=2,rowspan=2)

    cmb=ttk.Combobox(NotePage,width=10)
    cmb['value'] = ('No.1', 'No.2', 'No.3', 'No.4', 'No.5')
    cmb.current(0)
    cmb.grid(row=2, column=1,pady=5)
    ent1.grid(row=0, column=1,pady=5)
    ent2.grid(row=1, column=1,pady=5)

    NotePage.mainloop()

def ClassTable():
    TablePage = tk.Toplevel()
    TablePage.geometry('650x750')
    TablePage.title('课程表')
    TablePage.resizable(0,0)
    #TablePage['bg'] = '#aacdbe'

    timefrm0 = tk.Frame(TablePage)
    timelabel1 = tk.Label(timefrm0, text='时间/日期').grid(row=0, column=0)
    timefrm0.grid(row=0, column=0, pady=2, padx=1)

    timefrm = tk.Frame(TablePage)
    timelabel1 = tk.Label(timefrm, text='第一节\n08:00-8:45').grid(row=0, column=0)
    timefrm.grid(row=1, column=0)

    timefrm = tk.Frame(TablePage)
    timelabel1 = tk.Label(timefrm, text='第二节\n08:50-9:35').grid(row=0, column=0)
    timefrm.grid(row=2, column=0)

    timefrm = tk.Frame(TablePage)
    timelabel1 = tk.Label(timefrm, text='第三节\n09:50-10:35').grid(row=0, column=0)
    timefrm.grid(row=3, column=0)

    timefrm = tk.Frame(TablePage)
    timelabel1 = tk.Label(timefrm, text='第四节\n10:40-11:25').grid(row=0, column=0)
    timefrm.grid(row=4, column=0)

    timefrm = tk.Frame(TablePage)
    timelabel1 = tk.Label(timefrm, text='第五节\n11:30-12:15').grid(row=0, column=0)
    timefrm.grid(row=5, column=0)

    timefrm = tk.Frame(TablePage)
    timelabel1 = tk.Label(timefrm, text='第六节\n13:00-13:45').grid(row=0, column=0)
    timefrm.grid(row=6, column=0)

    timefrm = tk.Frame(TablePage)
    timelabel1 = tk.Label(timefrm, text='第七节\n13:50-14:35').grid(row=0, column=0)
    timefrm.grid(row=7, column=0)

    timefrm = tk.Frame(TablePage)
    timelabel1 = tk.Label(timefrm, text='第八节\n14:45-15:30').grid(row=0, column=0)
    timefrm.grid(row=8, column=0)

    timefrm = tk.Frame(TablePage)
    timelabel1 = tk.Label(timefrm, text='第九节\n15:40-16:25').grid(row=0, column=0)
    timefrm.grid(row=9, column=0)

    timefrm = tk.Frame(TablePage)
    timelabel1 = tk.Label(timefrm, text='第十节\n16:35-17:20').grid(row=0, column=0)
    timefrm.grid(row=10, column=0)

    timefrm = tk.Frame(TablePage)
    timelabel1 = tk.Label(timefrm, text='第十一节\n17:25-18:10').grid(row=0, column=0)
    timefrm.grid(row=11, column=0)

    timefrm = tk.Frame(TablePage)
    timelabel1 = tk.Label(timefrm, text='第十二节\n18:30-19:15').grid(row=0, column=0)
    timefrm.grid(row=12, column=0)

    timefrm = tk.Frame(TablePage)
    timelabel1 = tk.Label(timefrm, text='第十三节\n19:20-20:05').grid(row=0, column=0)
    timefrm.grid(row=13, column=0)

    timefrm = tk.Frame(TablePage)
    timelabel1 = tk.Label(timefrm, text='第十四节\n20:00-20:55').grid(row=0, column=0)
    timefrm.grid(row=14, column=0)

    weekfrm1 = tk.Frame(TablePage)
    weeklabel1 = tk.Label(weekfrm1, text='周一', width=10).grid(row=0, column=0, pady=2, padx=1)
    weekfrm1.grid(row=0, column=1, pady=2, padx=1)

    weekfrm1 = tk.Frame(TablePage)
    weeklabel1 = tk.Label(weekfrm1, text='周二', width=10).grid(row=0, column=0, pady=2, padx=1)
    weekfrm1.grid(row=0, column=2, pady=2, padx=1)

    weekfrm1 = tk.Frame(TablePage)
    weeklabel1 = tk.Label(weekfrm1, text='周三', width=10).grid(row=0, column=0, pady=2, padx=1)
    weekfrm1.grid(row=0, column=3, pady=2, padx=1)

    weekfrm1 = tk.Frame(TablePage)
    weeklabel1 = tk.Label(weekfrm1, text='周四', width=10).grid(row=0, column=0, pady=2, padx=1)
    weekfrm1.grid(row=0, column=4, pady=2, padx=1)

    weekfrm1 = tk.Frame(TablePage)
    weeklabel1 = tk.Label(weekfrm1, text='周五', width=10).grid(row=0, column=0, pady=2, padx=1)
    weekfrm1.grid(row=0, column=5, pady=2, padx=1)

    frm1 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm1, text='电子电路基础').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm1, text=' S109').grid(row=1, column=0)
    frm1.grid(row=1, column=2, pady=2, padx=1)

    frm2 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm2, text='电子电路基础').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm2, text=' S109').grid(row=1, column=0)
    frm2.grid(row=2, column=2, pady=2, padx=1)

    frm3 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm3, text='听说英语').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm3, text=' N412').grid(row=1, column=0)
    frm3.grid(row=1, column=3, pady=2, padx=1)

    frm4 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm4, text='听说英语').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm4, text=' N412').grid(row=1, column=0)
    frm4.grid(row=2, column=3, pady=2, padx=1)

    frm5 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm5, text='大学物理（上）').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm5, text=' N307').grid(row=1, column=0)
    frm5.grid(row=1, column=4, pady=2, padx=1)

    frm6 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm6, text='大学物理（上）').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm6, text=' N307').grid(row=1, column=0)
    frm6.grid(row=2, column=4, pady=2, padx=1)

    frm7 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm7, text='形势与政策2').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm7, text=' 办一层多功能厅').grid(row=1, column=0)
    frm7.grid(row=3, column=1, pady=2, padx=1)

    frm8 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm8, text='形势与政策2').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm8, text=' 办一层多功能厅').grid(row=1, column=0)
    frm8.grid(row=4, column=1, pady=2, padx=1)

    frm9 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm9, text='数学分析（下）').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm9, text=' N104').grid(row=1, column=0)
    frm9.grid(row=3, column=2, pady=2, padx=1)

    frm10 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm10, text='数学分析（下）').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm10, text=' N104').grid(row=1, column=0)
    frm10.grid(row=4, column=2, pady=2, padx=1)

    frm11 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm11, text='电子电路基础实验（上）').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm11, text=' 电路中心01').grid(row=1, column=0)
    frm11.grid(row=3, column=4, pady=2, padx=1)

    frm12 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm12, text='电子电路基础实验（上）').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm12, text=' 电路中心01').grid(row=1, column=0)
    frm12.grid(row=4, column=4, pady=2, padx=1)

    frm13 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm13, text='电子电路基础实验（上）').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm13, text=' 电路中心01').grid(row=1, column=0)
    frm13.grid(row=5, column=4, pady=2, padx=1)

    frm14 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm14, text='综合英语（B）').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm14, text=' N308').grid(row=1, column=0)
    frm14.grid(row=8, column=1, pady=2, padx=1)

    frm15 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm15, text='综合英语（B').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm15, text=' N308').grid(row=1, column=0)
    frm15.grid(row=9, column=1, pady=2, padx=1)

    frm16 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm16, text='python编程与实践').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm16, text=' S114').grid(row=1, column=0)
    frm16.grid(row=10, column=1, pady=2, padx=1)

    frm17 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm17, text='python编程与实践').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm17, text=' S114').grid(row=1, column=0)
    frm17.grid(row=11, column=1, pady=2, padx=1)

    frm18 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm18, text='数据结构与算法导论').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm18, text=' N103').grid(row=1, column=0)
    frm18.grid(row=6, column=2, pady=2, padx=1)

    frm19 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm19, text='数据结构与算法导论').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm19, text=' N103').grid(row=1, column=0)
    frm19.grid(row=7, column=2, pady=2, padx=1)

    frm20 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm20, text='数据结构与算法导论').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm20, text=' N103').grid(row=1, column=0)
    frm20.grid(row=8, column=2, pady=2, padx=1)

    frm21 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm21, text='数学分析（下）').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm21, text=' N104').grid(row=1, column=0)
    frm21.grid(row=6, column=4, pady=2, padx=1)

    frm22 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm22, text='数学分析（下）').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm22, text=' N104').grid(row=1, column=0)
    frm22.grid(row=7, column=4, pady=2, padx=1)

    frm23 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm23, text='数学分析（下）').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm23, text=' N104').grid(row=1, column=0)
    frm23.grid(row=8, column=4, pady=2, padx=1)

    frm24 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm24, text='中国近现代史纲要').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm24, text=' S302').grid(row=1, column=0)
    frm24.grid(row=9, column=2, pady=2, padx=1)

    frm25 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm25, text='中国近现代史纲要').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm25, text=' S302').grid(row=1, column=0)
    frm25.grid(row=10, column=2, pady=2, padx=1)

    frm26 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm26, text='中国近现代史纲要').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm26, text=' S302').grid(row=1, column=0)
    frm26.grid(row=11, column=2, pady=2, padx=1)

    frm27 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm27, text='电子电路基础').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm27, text=' S113').grid(row=1, column=0)
    frm27.grid(row=9, column=4, pady=2, padx=1)

    frm28 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm28, text='电子电路基础').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm28, text=' S113').grid(row=1, column=0)
    frm28.grid(row=10, column=4, pady=2, padx=1)

    frm33 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm33, text='电子电路基础').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm33, text=' S113').grid(row=1, column=0)
    frm33.grid(row=11, column=4, pady=2, padx=1)

    frm29 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm29, text='体育基础（上）').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm29, text=' 体育场').grid(row=1, column=0)
    frm29.grid(row=8, column=5, pady=2, padx=1)

    frm30 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm30, text='体育基础（上）').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm30, text=' 体育场').grid(row=1, column=0)
    frm30.grid(row=8, column=5, pady=2, padx=1)

    frm31 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm31, text='音乐概论').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm31, text=' N104').grid(row=1, column=0)
    frm31.grid(row=13, column=2, pady=2, padx=1)

    frm32 = tk.Frame(TablePage)
    classNameLabel1 = tk.Label(frm32, text='音乐概论').grid(row=0, column=0)
    classTimeLabel1 = tk.Label(frm32, text=' N104').grid(row=1, column=0)
    frm32.grid(row=13, column=2, pady=2, padx=1)

    TablePage.mainloop()

