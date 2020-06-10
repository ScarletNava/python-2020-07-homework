import function
import tkinter as tk
import tkinter.messagebox
import math

firstPage = tk.Tk()
firstPage.title('WallpaperEngine(假的)')
firstPage.geometry('360x110')
firstPage.resizable(0,0)#窗口大小固定


#更换壁纸按钮及图标
changeOPho  = tk.PhotoImage(file='img/更换.png')
OnceLabel   = tk.Label(firstPage,image=changeOPho).grid(row=0,column=0)
btnO        = tk.Button(firstPage,text='更换壁纸',command=function.changeO).grid(row=1,column=0)

#随机切换壁纸按钮及图标
changeRPho  = tk.PhotoImage(file='img/随机.png')
RandLabel   = tk.Label(firstPage,image=changeRPho).grid(row=0,column=1)
btnR        = tk.Button(firstPage,text='壁纸随机',command=function.changeR).grid(row=1,column=1)

#网络获取壁纸按钮及图标
searchPho    = tk.PhotoImage(file='img/搜索.png')
searchLabel  = tk.Label(firstPage,image=searchPho).grid(row=0,column=2)
btnS         = tk.Button(firstPage,text='网络获取',command=function.searchFromWeb).grid(row=1,column=2)

#备忘录按钮及图标
NotePho      =tk.PhotoImage(file='img/备忘录.png')
NoteLabel    =tk.Label(firstPage,image=NotePho).grid(row=0,column=3)
btnNote      = tk.Button(firstPage,text='备忘录',command=function.NoteBook).grid(row=1,column=3)

#课程表按钮及图标
TablePho     =tk.PhotoImage(file='img/课程表.png')
TableLabel   =tk.Label(firstPage,image=TablePho).grid(row=0,column=4)
btnTable     = tk.Button(firstPage,text='课程表',command=function.ClassTable).grid(row=1,column=4)



firstPage.mainloop()

#函数调用实例

#print(function.GetAbsolutePath())

#function.mySpider('风景','webimages','1920','1080')

#function.choosemusic('music')

#换一张
#function.ControlTime("D:\\Users\\Scarlet\\Desktop\\wallpaper\\webimages\\0.jpg",0,'a', 40,1080-40-125-35,1920/2-100,1080/2-100,(255, 255, 255),(255, 255, 255))

#一直换
#function.ControlTime("D:\\Users\\Scarlet\\Desktop\\wallpaper\\images\\",4,'a', 40,1080-40-125-35,1920/2-100,1080/2-100,(255, 255, 255),(255, 255, 255))
