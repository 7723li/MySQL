import sys
sys.path.append(r'D:\python安装\自写模块')
import pytosql

from tkinter import *
import os
LoInroot=Tk()

def Register():#进入注册程序
    LoInroot.destroy()
    os.system(r'C:\Users\Administrator\Desktop\新建文件夹\注册界面.py')
    
def LoginInterface():
    def IdReadListConfig():
        list1=[]
        a=pytosql.pytosql()
        a.use('账号密码')
        IdRead=a.read('select 身份证号码 from 账号密码')
        for each in IdRead:
            for each1 in each:
                list1.append(each1)
        return list1
        
    def IdExistCheck():
        if Idin.get() in IdReadList:
            Account.set('√')
            return True
        else:
            Idin.delete(0,END)
            Account.set('号码填写错误或未注册')
            return False

    def PassCheck():
        a=pytosql.pytosql()
        a.use('账号密码')
        if Idin.get() and Idin.get().isalnum():
            command="select 密码 from 账号密码 where 身份证号码='"+str(Idin.get())+"'"
            PassRead=a.read(command)
            #print(PassRead[0][0])
            if Passin.get()==PassRead[0][0]:
                Password.set('√')
                return True
            else:
                Password.set('密码错误')
                return False
        else:
            pass

    def Login():#进入检索与检测界面
        if IdExistCheck() and PassCheck():
            #此处为登陆程序的关键代码，写入登陆的账号，方便检索与检测界面的操作
            file=open(r'C:\Users\Administrator\Desktop\新建文件夹\登陆者.txt','w')
            file.write(Idin.get())
            file.close()
            LoInroot.destroy()
            os.system(r'C:\Users\Administrator\Desktop\新建文件夹\选择界面.py')
        else:
            LoInroot.title('账号密码错误！')

    #主框架设计   
    LoInroot.title('登录界面')
    IdReadList=IdReadListConfig()#获取已注册的账号列表

    Id=StringVar()
    Pass=StringVar()

    Account=StringVar()
    Password=StringVar()
    Account.set('账号')
    Password.set('密码')

    frame1=Frame(LoInroot)
    frame2=Frame(LoInroot)
    frame3=Frame(LoInroot)

    IdLabel=Label(frame1,textvariable=Account)
    PassLabel=Label(frame2,textvariable=Password)
    IdLabel.pack(side=LEFT)
    PassLabel.pack(side=LEFT,pady=10)
    
    #此处检测账号是否存在
    Idin=Entry(frame1,textvariable=Id,validate='focusout',validatecommand=IdExistCheck)
    #检测密码是否正确
    Passin=Entry(frame2,validate='focusout',textvariable=Pass,validatecommand=PassCheck,show='*')
    
    #为开发方便插入已注册的账号密码，实际应用时删除
    Idin.insert(0,'44078419951107481X')
    Passin.insert(0,'12345678')

    Idin.pack(side=LEFT,pady=10)
    Passin.pack(side=LEFT,pady=10)

    b1=Button(frame3,text='确认登陆',command=Login)
    b2=Button(frame3,text='注册',command=Register)
    b1.pack(side=LEFT,padx=30,pady=10)
    b2.pack(side=RIGHT,padx=30,pady=10)

    frame1.pack()
    frame2.pack()
    frame3.pack()

    mainloop()

if __name__ == '__main__':
    LoginInterface()#登陆界面
