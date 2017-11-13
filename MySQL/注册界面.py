from tkinter import *
import time
import os

import sys
sys.path.append(r'D:\python安装\自写模块')
import pytosql

Regiroot=Tk()

def ToDatabase(IdToWrite,PassToWrite,NameToWrite,SexToWrite,BirthToWrite,PhNumberToWrite):
    a=pytosql.pytosql()
    a.use('账号密码')
    command="insert into 账号密码 (身份证号码,密码) values('" + str(IdToWrite) + "','"+ str(PassToWrite)+"')"
    a.execute(command)
    a.use('用户信息检索')
    command="insert into 用户基本信息(ID,姓名,性别,出生日期,手机号码) values('"+str(IdToWrite)+\
             "','"+str(NameToWrite)+"','"+str(SexToWrite)+"','"\
             +str(BirthToWrite)+"','"+str(PhNumberToWrite)+"')"
    a.execute(command)
    #messagebox.showinfo(Regiroot,'注册成功！')
    Regiroot.destroy()
    os.system(r'C:\Users\Administrator\Desktop\新建文件夹\登陆界面.py')

def DataCheck(a,b,c,d,e,f,g,h):
    if(a and b and c and d and e and f and g and h):
        return True
    else:
        return False

def Register():
    def IdReadListConfig():
        list1=[]
        a=pytosql.pytosql()
        a.use('账号密码')
        IdRead=a.read('select 身份证号码 from 账号密码')
        for each in IdRead:
            for each1 in each:
                list1.append(each1)
        return list1
    
    #检测数据是否全部填写完毕，并把数据写入数据库
    def DataUpdate():
        Birthin_month_Regi=Birthin_month.get()
        if len(Birthin_month_Regi)==1:
            Birthin_month_Regi='0'+Birthin_month_Regi
        else:
              pass
        
        Birthin_day_Regi=Birthin_day.get()
        if len(Birthin_day_Regi)==1:
            Birthin_day_Regi='0'+Birthin_day_Regi
        else:
              pass
        
        IdToWrite=Idin.get()
        PassToWrite=Passin.get()
        NameToWrite=Namein.get()
        SexToWrite=Sex.get()
        BirthToWrite=Birthin_year.get()+'-'+Birthin_month_Regi+'-'+Birthin_day_Regi
        PhNumberToWrite=PhNumberin.get()
        #检测是否全部填写完毕
        if DataCheck(IdToWrite,PassToWrite,NameToWrite,SexToWrite,
                     Birthin_year.get(),Birthin_month.get(),Birthin_month.get(),PhNumberToWrite):
            #再次监测数据是否合法               
            if(IdCheck() and PassCheck() and NameCheck() and Birthin_year_check()
               and Birthin_month_check() and Birthin_day_check() and PhNumber_check()):
                ToDatabase(IdToWrite,PassToWrite,NameToWrite,SexToWrite,BirthToWrite,PhNumberToWrite)
            else:
                Regiroot.title('请先把数据填写完毕！')
        else:
            Regiroot.title('请先把数据填写完毕！')

    #重置
    def Reset():
        Regiroot.title('请注册')
        Idin.delete(0,END)
        Passin.delete(0,END)
        Namein.delete(0,END)
        Sex.set('男')
        Birthin_year.delete(0,END)
        Birthin_month.delete(0,END)
        Birthin_day.delete(0,END)
        PhNumberin.delete(0,END)
        ID_srting.set('身份证号码:')
        PASS_string.set('设置密码')
        NAME_string.set('姓名:')
        SEX_string.set('性别:')
        BIRTH_string.set('出生日期:')
        PHNUMBER_string.set('手机号码:')
        
    #以下一段以Check结尾的函数均用于检测输入数据是否合法
    def IdCheck():#账号
        if Idin.get() not in IdReadList:
            content=Idin.get() 
            if len(content)==18:
                if content[17]=='x' or content[17]=='X':
                    if content[0:16].isdigit():
                        ID_srting.set('√')
                        return True
                    else:
                        Idin.delete(0,END)
                        ID_srting.set('请输入正确的身份证号码！')
                        return False
                else:
                    if content.isdigit():
                        ID_srting.set('√')
                        return True
                    else:
                        Idin.delete(0,END)
                        ID_srting.set('请输入正确的身份证号码！')
                        return False
            else:
                Idin.delete(0,END)
                ID_srting.set('请输入正确的身份证号码！')
                return False
        else:
            Idin.delete(0,END)
            ID_srting.set('身份证号码已存在！')
            return False

    def PassCheck():#密码
        if len(Passin.get())>=8 and len(Passin.get())<=20:
            if Passin.get().isalnum:
                PASS_string.set('√')
                return True
            else:
                Passin.delete(0,END)
                PASS_string.set('密码只可由8到20位数字或字母组成')
                return False
        else:
            Passin.delete(0,END)
            PASS_string.set('密码只可由8到20位数字或字母组成')
            return False

    def NameCheck():#姓名
        if len(Namein.get())>=2 and len(Namein.get())<=20:
            if Namein.get().isalpha():
                NAME_string.set('√')
                return True
            elif ' ' in Namein.get():
                try:
                    a,b=Namein.get().split(' ')
                    if a.isalpha() and b.isalpha():
                        NAME_string.set('√')
                        return True
                    else:
                        Namein.delete(0,END)
                        NAME_string.set('请输入正确的名字！')
                        return False
                except ValueError:
                    Namein.delete(0,END)
                    NAME_string.set('请输入正确的名字！')
                    return False
            else:
                Namein.delete(0,END)
                NAME_string.set('请输入正确的名字！')
                return False
        else:
            Namein.delete(0,END)
            NAME_string.set('请输入正确的名字！')
            return False

    def SexCheck():
        b=Sex.get()
    
    def Birthin_year_check():#出生年
        try:
            if int(Birthin_year.get())>=1900 and int(Birthin_year.get())<=int(time.localtime().tm_year):
                return True
            else:
                Birthin_year.delete(0,END)
                Birthin_year.insert(0,'')
                return False
        except ValueError:
            Birthin_year.delete(0,END)
            Birthin_year.insert(0,'')
            return False
        
    def Birthin_month_check():#月
        try:
            if int(Birthin_month.get())<=12 and int(Birthin_month.get())>=1:
                return True
            else:
                Birthin_month.delete(0,END)
                Birthin_month.insert(0,'')
                return False
        except ValueError:
            Birthin_month.delete(0,END)
            Birthin_month.insert(0,'')
            return False

    def Birthin_day_check():#日
        try:
            if int(Birthin_day.get())>=1 and int(Birthin_day.get())<=31:
                return True
            else:
                Birthin_day.delete(0,END)
                Birthin_day.insert(0,'')
                return False
        except ValueError:
            Birthin_day.delete(0,END)
            Birthin_day.insert(0,'')
            return False

    def PhNumber_check():#手机号码
        try:
            if len(PhNumberin.get())== 11 and PhNumberin.get().isdigit():
                if PhNumberin.get().isdigit():
                    PHNUMBER_string.set('√')
                    return True
                else:
                    PhNumberin.delete(0,END)
                    PHNUMBER_string.set('请输入正确的电话号码！')
                    return False
            else:
                PhNumberin.delete(0,END)
                PHNUMBER_string.set('请输入正确的电话号码！')
                return False
        except ValueError:
            PhNumberin.delete(0,END)
            PHNUMBER_string.set('请输入正确的电话号码！')
            return False

    #主体设置
    Regiroot.title('请注册')
    IdReadList=IdReadListConfig()
    
    #框架设置
    frame1=Frame(Regiroot)
    frame_pass=Frame(Regiroot)
    frame2=Frame(Regiroot)
    frame3=Frame(Regiroot)
    frame4=Frame(Regiroot)
    frame5=Frame(Regiroot)
    frame6=Frame(Regiroot)

    #标题设置
    ID_srting=StringVar()
    ID_srting.set('身份证号码:')
    PASS_string=StringVar()
    PASS_string.set('设置密码')
    NAME_string=StringVar()
    NAME_string.set('姓名:')
    SEX_string=StringVar()
    SEX_string.set('性别:')
    BIRTH_string=StringVar()
    BIRTH_string.set('出生日期:')
    PHNUMBER_string=StringVar()
    PHNUMBER_string.set('手机号码:')
    
    IdLabel=Label(frame1,textvariable=ID_srting)
    PassLabel=Label(frame_pass,textvariable=PASS_string)
    NameLabel=Label(frame2,textvariable=NAME_string)
    SexLabel=Label(frame3,textvariable=SEX_string)
    BirthLabel=Label(frame4,textvariable=BIRTH_string)
    PhNumber=Label(frame5,textvariable=PHNUMBER_string)

    IdLabel.pack(side=LEFT)
    PassLabel.pack(side=LEFT)
    NameLabel.pack(side=LEFT)
    SexLabel.pack(side=LEFT)
    BirthLabel.pack(side=LEFT)
    PhNumber.pack(side=LEFT)

    #输入框架设置
    Id=StringVar()
    Pass=StringVar()
    Name=StringVar()
    Sex=StringVar()
    Birth_Y=StringVar()
    Birth_M=StringVar()
    Birth_D=StringVar()
    PhNumber=StringVar()

    Sexin_list=[('男','男'),('女','女')]
    Sex.set('男')
    
    Idin=Entry(frame1,textvariable=Id,validate='focusout',
               validatecommand=IdCheck)
    Passin=Entry(frame_pass,textvariable=Pass,validate='focusout',
                 validatecommand=PassCheck,show='*')
    Namein=Entry(frame2,textvariable=Name,validate='focusout',
                 validatecommand=NameCheck)
    for each,each_num in Sexin_list:
        Sexin=Radiobutton(frame3,text=each,variable=Sex,value=each_num)
        Sexin.pack(side=LEFT)
        
    Birthin_year=Entry(frame4,textvariable=Birth_Y,validate='focusout',width=10,
                       validatecommand=Birthin_year_check)
    Y=Label(frame4,text='年')
    
    Birthin_month=Entry(frame4,textvariable=Birth_M,validate='focusout',width=10,
                        validatecommand=Birthin_month_check)
    M=Label(frame4,text='月')
    
    Birthin_day=Entry(frame4,textvariable=Birth_D,validate='focus',width=10,
                      validatecommand=Birthin_day_check)
    D=Label(frame4,text='日')
    
    PhNumberin=Entry(frame5,textvariable=PhNumber,validate='focusout',
                     validatecommand=PhNumber_check)

    #此处为开发方便，实际应用时删除
    
    Idin.insert(0,'44078419951107481X')
    Passin.insert(0,'12345678')
    Namein.insert(0,'Lee')
    Birthin_year.insert(0,'1995')
    Birthin_month.insert(0,'11')
    Birthin_day.insert(0,'7')
    PhNumberin.insert(0,'18826226234')
    
    
    Idin.pack(side=LEFT)
    Passin.pack(side=LEFT)
    Namein.pack(side=LEFT)
    Birthin_year.pack(side=LEFT)
    Y.pack(side=LEFT)
    Birthin_month.pack(side=LEFT)
    M.pack(side=LEFT)
    Birthin_day.pack(side=LEFT)
    D.pack(side=LEFT)
    PhNumberin.pack(side=LEFT)
    
    #按钮设置
    Regi_reset=Button(frame6,text='重置',command=Reset)
    Regi_reset.pack(side=RIGHT,padx=30,pady=10)
    Regi_confirm=Button(frame6,text='确认注册',command=DataUpdate)
    Regi_confirm.pack(side=LEFT,padx=30,pady=10)
                          
    frame1.pack(pady=10)
    frame_pass.pack(pady=10)
    frame2.pack(pady=10)
    frame3.pack(pady=10,side=TOP)
    frame4.pack(pady=10)
    frame5.pack(pady=10)
    frame6.pack()

    #窗口运行
    mainloop()
    
if __name__ == '__main__':
    Register()#注册界面
