import serial
import time
import sys
sys.path.append(r'D:\python安装\自写模块')
import pytosql
import os
from tkinter import *
Choiceroot=Tk()

#弹出一个新的窗口
def NewWindow(title,message):
    root=Toplevel()#此处使用Toplevel，使用Tk会产生错误
    root.title(str(title))

    frame1=Frame(root)
    
    sb=Scrollbar(root)
    sb.pack(side=RIGHT,fill=Y)
    sb1=Scrollbar(root,orient=HORIZONTAL)
    sb1.pack(side=BOTTOM,fill=X)

    #根据传入的标题判断需要显示的内容，在此进行数据处理
    lb=Listbox(frame1,yscrollcommand=sb.set,xscrollcommand=sb1.set,
               width=100,font=10,selectmode=SINGLE,height=45)

    if title!='用户基本信息':
        num=5
        num1=len(message)*2
        while num<=num1:
            message.insert(num,'\n')
            num+=6
    else:
        num=1
        num1=len(message)*2-1
        while num<=num1:
            message.insert(num,'\n')
            num+=2

    a=''        
    #把处理后的数据放进消息框中显示，并加入拖动条
    for each in message:
        a+=(each+'\n')
        lb.insert(END,each)
    
    lb.pack(side=TOP,fill=BOTH)

    sb.config(command=lb.yview)
    sb1.config(command=lb.xview)

    frame1.pack(pady=30)

#检索与检测主程序
def ChoiceInterface():
    def ComNum(num):
        return num.isdigit()and (num==4800 or num==9600)
    ComNumCMD=Choiceroot.register(ComNum)

    def BaudrateNum(num):
        return num.isdigit()
    BaudrateNumCMD=Choiceroot.register(BaudrateNum)
    
    #与虚拟串口通信，获取串口传入的数据并进行解码后返回
    def Dataget(Ser):
        try:
            A=[]
            while True:
                A.append(Ser.read().decode('utf-8'))
                if '\n' in A:
                    return A
        except UnicodeDecodeError:
            #A.append(b'\xe2\x84\x83'.decode('utf-8'))
            return list('暂不支持中文')

    #从数据库中获取数据
    def Search():
        #根据提示按钮的选择判断需要搜索的内容，把数据处理后传给新窗口显示
        b=SearchChoiceSring.get()
        if b=='用户基本信息':
            list1=[]
            list2=[]
            a=pytosql.pytosql()
            a.use('用户信息检索')
            command="select * from 用户基本信息 where ID='"+str(Id)+"'"
            IdMessage=a.read(command)
            for i in IdMessage:
                for j in i:
                    list1.append(j)
            ab=['ID：','姓名：','性别：','出生日期：','手机号码：']
            for i in range(len(list1)):
                list2.append(ab[i]+list1[i])
            NewWindow('用户基本信息',list2)
            
        elif b=='用户治疗信息':
            a=pytosql.pytosql()
            a.use('用户信息检索')
            command="select 串口数据输入,串口数据输入日期,诊断医生 from 用户治疗信息 where ID='"+str(Id)+"'"
            CureMessage=a.read(command)
            
            list1=[]
            for i in CureMessage:
                for j in i:
                    list1.append(j)
                    
            list2=[]
            x,y=0,3
            ab=['日期：','诊断医生：','体温：','心跳:','输液完成:']
            while y<=len(list1):
                list2.append(list1[x:y])
                x+=3
                y+=3
                
            list3=[]
            for i in list2:
                for j in i:
                    if '-' in j:
                        temp,rate,fin=j.split('-')
                        list3.append(temp)
                        list3.append(rate)
                        list3.append(fin)

            list4=[]            
            x,y=0,3
            for i in list2:
                i.remove(i[0])
                list4.append(i+list3[x:y])
                x+=3
                y+=3
            for i in list4:
                i[2]+='℃'
                i[3]+='bpm'
            
            list5=[]
            for i in list4:
                for j in range(len(i)):
                    list5.append(ab[j]+i[j])
            
            if list5!=[]:
                    NewWindow('用户治疗信息',list5)
            elif list5==[]:
                    list5=['无数据']
                    NewWindow('用户治疗信息',list5)
          
        #需要注意此处是使用模糊查询，而前两个是使用精确查询
        elif b=='白度一下':
            #根据输入框的内容获取搜索关键字，若输入框为空则不执行
            if SearchFrame.get():
                SearchMessage=SearchFrame.get()
                a=pytosql.pytosql()
                a.use('用户信息检索')
                command="select 串口数据输入,诊断医生,串口数据输入日期 from 用户治疗信息 where ID ='"\
                         +str(Id)+"'and 串口数据输入 like '%"+str(SearchMessage)+"%'"
                NormalMessage1=a.read(command)
                command="select 串口数据输入,诊断医生,串口数据输入日期 from 用户治疗信息 where ID ='"\
                         +str(Id)+"'and 诊断医生 like '%"+str(SearchMessage)+"%'"
                NormalMessage2=a.read(command)
                command="select 串口数据输入,诊断医生,串口数据输入日期 from 用户治疗信息 where ID ='"\
                         +str(Id)+"'and 串口数据输入日期 like '%"+str(SearchMessage)+"%'"
                NormalMessage3=a.read(command)
                NormalMessage=NormalMessage1+NormalMessage2+NormalMessage3

                list1=[]
                for i in NormalMessage:
                    for j in i:
                        list1.append(j)

                list2=[]
                x,y=0,3
                ab=['诊断医生：','日期：','体温：','心跳:','输液完成:']
                while y<=len(list1):
                    list2.append(list1[x:y])
                    x+=3
                    y+=3
                    
                list3=[]
                for i in list2:
                    for j in i:
                        if '-' in j:
                            temp,rate,fin=j.split('-')
                            list3.append(temp)
                            list3.append(rate)
                            list3.append(fin)
                            
                list4=[]
                x,y=0,3
                for i in list2:
                    i.remove(i[0])
                    list4.append(i+list3[x:y])
                    x+=3
                    y+=3

                list5=[]
                for i in list4:
                    for j in range(len(i)):
                        list5.append(ab[j]+i[j])
                if list5!=[]:
                        NewWindow('白度一下',list5)
                elif list5==[]:
                        list5=['无数据']
                        NewWindow('白度一下',list5)

    #Python连接虚拟串口的主要参数             
    #Serial<id=0x1fd9db0, open=False>(port=None, baudrate=9600, bytesize=8,
    #parity='N', stopbits=1, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False

    #Python连接虚拟串口的主要代码
    def DataContect():
        #检测医生是否已签名，若未签名则不能收集数据
        def NameCheck():
            if len(DoctorFrame.get())>=2 and len(DoctorFrame.get())<=20:
                if DoctorFrame.get().isalpha():
                    return True
                elif ' ' in DoctorFrame.get():
                    try:
                        a,b=DoctorFrame.get().split(' ')
                        if a.isalpha() and b.isalpha():
                            return True
                        else:
                            DoctorFrame.delete(0,END)
                            return False
                    except ValueError:
                        DoctorFrame.delete(0,END)
                        return False
                else:
                    DoctorFrame.delete(0,END)
                    return False
            else:
                DoctorFrame.delete(0,END)
                return False

        #把虚拟串口传入的处理后的数据放进数据库
        def ToDataBase():
            if NameCheck() and TransfutionFrame.get()=='completed':
                a=pytosql.pytosql()
                a.use('用户信息检索')
                command="insert into 用户治疗信息(ID,串口数据输入,串口数据输入日期,诊断医生) values ('"\
                         +str(Id)+"','"+str(Data)+"','"+str(Time)+"','"+ str(DoctorFrame.get())+"')"
                #messagebox.showinfo(Choiceroot,'收集成功！')
                a.execute(command)
                root.destroy()

        try:
            #连接串口
            Baudrate=BaudrateFrame.get()
            num=ReceiveFrame.get()
            com='com'+str(num)
            Ser=serial.Serial(port=com,baudrate=int(Baudrate))

            Unit=['年','月','日','时','分','秒']
            TempertureString=StringVar()
            RateString=StringVar()
            TransfutionString=StringVar()
            TimeString=StringVar()

            #获取虚拟串口数据后的显示框架
            root=Toplevel()
            root.title('数据收集')
                
            frame1=Frame(root)
            frame2=Frame(root)
            frame3=Frame(root)
            frame4=Frame(root)
            
            TempertureLabel=Label(frame1,text='体温：')
            RateLabel=Label(frame1,text='心跳：')
            TransfutionLabel=Label(frame1,text='输液：')
            TimeLabel=Label(frame2,text='时间：')
            DoctorLabel=Label(frame3,text='医生：')
            
            TimeLabel.pack(side=LEFT)
            DoctorLabel.pack(side=LEFT)

            #注意此处为确保数据的准确性，输入框都为只读模式
            TempertureFrame=Entry(frame1,state='readonly',width=12,textvariable=TempertureString)
            RateFrame=Entry(frame1,state='readonly',width=12,textvariable=RateString)
            TransfutionFrame=Entry(frame1,state='readonly',width=12,textvariable=TransfutionString)
            TimeFrame=Entry(frame2,state='readonly',width=50,textvariable=TimeString)
            DoctorFrame=Entry(frame3,width=50,validate='focusout',validatecommand=NameCheck)

            TempertureLabel.pack(side=LEFT)
            TempertureFrame.pack(side=LEFT)
            RateLabel.pack(side=LEFT)
            RateFrame.pack(side=LEFT)
            TransfutionLabel.pack(side=LEFT)
            TransfutionFrame.pack(side=LEFT)
            TimeFrame.pack(side=LEFT)
            DoctorFrame.pack(side=LEFT)

            Button(frame4,text='收集此数据',command=ToDataBase).pack()

            frame1.pack(pady=30)
            frame2.pack(pady=30)
            frame3.pack(pady=30)
            frame4.pack()
            try:
                while TransfutionFrame.get()!='completed': 
                    #调用串口通信代码，获取返回的数据并进行处理
                    Data=Dataget(Ser)
                    #获取当前时间
                    Time=time.localtime()
                    #串口数据处理
                    Data.pop()
                    String=''
                    for each in Data:
                        String+=each
                    Data=String
                    try:
                        Temperture,Rate,Transfution=Data.split('-')
                    except ValueError:
                        root.destroy()
                        BaudrateNum.set('9600')
                        break
                    
                    #时间数据处理
                    String=''
                    List=[]
                    for each in range(len(Unit)):
                        List.append(str(Time[each])+Unit[each])
                    for each in List:
                        String+=each
                    Time=String

                    #在新框架中显示获取的数据和当前时间
                    TempertureString.set(Temperture+'℃')
                    RateString.set(Rate+'bpm')
                    TransfutionString.set(Transfution)
                    TimeString.set(Time)
                
                    root.update()#更新窗口
            except TclError:
                pass
        except serial.serialutil.SerialException:
            pass

    #获取用户信息，并显示在界面的右上角
    def UserMessage():
        b=''
        list1=[]
        
        #判断用户性别和姓名，以列表方式返回
        a=pytosql.pytosql()
        a.use('用户信息检索')
        command="select 姓名,性别,ID from 用户基本信息 where ID='"+str(Id)+"'"
        NameRead=a.read(command)
        if NameRead[0][1]=='男':
            b='先生'
        if NameRead[0][1]=='女':
            b='小姐'
        list1.append(NameRead[0][0])
        list1.append(b)
        return list1

    #主程序开始读取登陆时写入的账号信息
    file=open(r'C:\Users\Administrator\Desktop\新建文件夹\登陆者.txt','r')
    Id=file.read()#全局关键字
    file.close()

    #主框架
    Choiceroot.title('检索与检测')
    UserMessageString=UserMessage()
    UserMessageString='欢迎使用本系统，'+UserMessageString[0]+' '+UserMessageString[1]
    SearchChioceColumn=0

    frame0=Frame(Choiceroot)
    frame1=Frame(Choiceroot)
    frame2=Frame(Choiceroot)
    frame3=Frame(Choiceroot)
    frameCom=Frame(Choiceroot)
    frame4=Frame(Choiceroot)

    SearchChioceList=[('用户基本信息','用户基本信息'),('用户治疗信息','用户治疗信息'),('白度一下','白度一下')]

    SearchChoiceSring=StringVar()
    SearchChoiceSring.set('用户基本信息')
    MessageShowString=StringVar()
    ButtonString=StringVar()
    ButtonString.set('数据收集')

    ReceiveComNum=StringVar()
    ReceiveComNum.set('6')
    BaudrateNum=StringVar()
    BaudrateNum.set('9600')

    User=Label(frame0,text=UserMessageString,font=10)

    Brand=Label(frame1,text='白度',font=('黑体',30))
    
    SearchFrame=Entry(frame2,width=100,validate='focusin')
    Searchbutton=Button(frame2,text='白度一下',command=Search)
    SearchFrame.insert(0,'输入关键字')
    
    for each,each_num in SearchChioceList:
        SearchChioce=Radiobutton(frame3,text=each,variable=SearchChoiceSring,value=each_num)
        SearchChioce.pack(side=LEFT,pady=10)

    ReceiveLabel=Label(frameCom,text='接收端口：com')
    ReceiveFrame=Entry(frameCom,width=10,validate='key',textvariable=ReceiveComNum,
                       validatecommand=(ComNumCMD,'%P'))
    BaudrateLabel=Label(frameCom,text='波特率')
    BaudrateFrame=Entry(frameCom,width=10,validate='key',textvariable=BaudrateNum,
                       validatecommand=(BaudrateNumCMD,'%P'))

    DataSelectButton=Button(frame4,textvariable=ButtonString,command=DataContect)

    #打包
    User.pack(pady=30)
    
    Brand.pack(pady=30)
    
    SearchFrame.pack(side=LEFT)
    Searchbutton.pack(side=LEFT)

    ReceiveLabel.pack(side=LEFT)
    ReceiveFrame.pack(side=LEFT)
    BaudrateLabel.pack(side=LEFT)
    BaudrateFrame.pack(side=LEFT)
    
    DataSelectButton.pack(pady=30)
    
    frame0.pack(anchor='ne')
    frame1.pack()
    frame2.pack()
    frame3.pack()
    frame4.pack(side=BOTTOM)
    frameCom.pack(side=BOTTOM)
    
    mainloop()

    

if __name__ == '__main__':
    ChoiceInterface()#检索与检测界面
