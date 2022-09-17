from tkinter import *
import tkinter.font as tkFont
from tkinter import filedialog, dialog
import tkinter.messagebox
import json
import os
import pandas as pd
from tkinter.simpledialog import askstring

#设置图片文件的路径变量
path1, path2 = None, None

class FCFS:
    '''
    FCFS对象
    属性列表：
        id：表示进程的进程id，数据类型为int
        name：表示进程的名称，数据类型为string
        good：表示进程的优先级，数据类型为int
        arrive：表示进程的到达时间，数据类型为time对象
        zx：表示进程执行所需要的的时间，数据类型为int
        start：表示进程开始运行的时间，数据类型为time对象
        finish：表示进程结束运行的时间，数据类型为time对象
        zz：表示进程的周转时间， 数据类型为int
        zzxs：表示进程的带权周转时间系数，数据类型为float
        flag：用于表示是否运行完成，数据类型为bool
        first：首次执行的时间，数据类型为time
        have_finished：已经执行的时间，数据类型为int
        arr：每轮时间片轮转的到达时间，数据类型为time
    
    方法列表：
        __init__：构造函数，需要一个参数ls。
                  ls为list对象，是一个存储FCFS各个参数内容的列表，是直接从csv读取并格式化后的数据表
        __getId：从ls中获取id
        __getName：从ls中获取name
        __getGood：从ls中获取good
        __getArrive：从ls中获取arrive
        __getZx：从ls中获取zx
    '''
    class time:
        '''
        时间time对象，用于存放一个时间。
        属性列表：
            hour：存放小时的变量，数据类型为int
            minute：存放分钟的变量，数据类型为int
            __total：表示这个时间对象总分钟数，用于运算比较等，数据类型为int
        方法列表：
            __init__：构造函数，有两个参数h和m。
                      h为小时数，m为分钟数，用于获取时间
            getkey：返回时间对象的总分钟数，用于运算比较
        '''
        hour, minute, __total = 0, 0, 0
        def __init__(self, h=0, m=0):
            self.hour, self.minute = h, m
            self.__total = self.hour*60 + self.minute
        def getkey(self):
            return self.__total
        def create_by_key(self, key):
            self.hour = key//60
            self.minute = key%60
    
    start = time(0, 0)
    first = time(0, 0)
    have_finished = 0
    arr = time(0, 0)
    finish = time(0, 0)
    zz = 0
    zzxs = 0.0
    flag = True

    def  __init__(self, ls):
        '''
        构造函数，需要一个参数ls。
        ls为list对象，是一个存储FCFS各个参数内容的列表，是直接从csv读取并格式化后的数据表
        '''
        self.id = self.__getId(ls[0])
        self.name = self.__getName(ls[1])
        self.good = self.__getGood(ls[2])
        self.arrive = self.__getArrive(ls[3])
        self.zx = self.__getZx(ls[4])
        self.is_first_time = True
    
    def __getId(self, value):
        '''
        从ls中获取id
        '''
        return int(value)
    
    def __getName(self, value):
        '''
        从ls中获取name
        '''
        return value
    
    def __getGood(self, value):
        '''
        从ls中获取good
        '''
        return value

    def __getArrive(self, value):
        '''
        从ls中获取arrive
        '''
        h, m = map(int, value.split(":"))
        return self.time(h, m)
    
    def __getZx(self, value):
        '''
        从ls中获取zx
        '''
        return int(value)

class MY_GUI():
    '''
    GUI对象，用于生成一个可交互的GUI
    参数列表：
        init_window_name：程序名称，由构造函数获得
        image_path1：按钮图片“选择文件.png”的绝对地址
        image_path2：按钮图片“开始模拟.png”的绝对地址
        init_data_label：程序界面的主标题文字显示部分
        result_data_label：程序界面的结果展示框的提示标题文字部分
        tip_information_label：程序界面的红色提示文字部分
        result_data_Text：结果显示文本框部分
        img1、img2：存储按钮图片的变量
        read_file_button：读取文件按钮
        start_button：开始模拟按钮
        fapth：文件的绝对路径存储变量，数据类型为string
        ls：存放数据内容的FCFS对象的列表
        simulate_mode：存放一个整数，代表模拟运行的模式（1为先到先运行，2为加入优先级，3为时间片轮转）
    
    方法列表：
        __init__(self, init_window_name)
        __read_config(self)
        set_init_window(self)
        timeAdd(self, t1, t2)
        average(self, value, n)
        getinput(self, fpath)
        data(self)
        message_showinfo(self)
        message_error01(self)
        message_error02(self)
        message_error03(self)
        message_error04(self)
        message_error05(self)
        choose_mode(self)
        start_simulate(self)
        print_result(self, ls)
    '''
    def __init__(self, init_window_name):
        '''
        构造函数，有一个参数init_window_name，参数内存放的是TK窗口对象，用于获取GUI窗口的变量名称
        '''
        self.init_window_name = init_window_name
    
    def __read_config(self):
        '''
        通过读取文件目录下的config/config.json进行设置，
        设置内容为两个按钮图片的相对路径。
        函数将相对路径转化为绝对路径并储存在MY_GUI对象的属性image_path1，和image_path2中
        '''
        global path1, path2
        path = os.path.abspath(os.path.dirname(__file__))      #通过abspath函数将config.json的相对路径转化为绝对路径
        with open(path + "//config//config.json", 'r', encoding='utf-8') as json_file:       #打开并读取config.json，并通过json内容配置全局变量path
            try:
                a = json.load(json_file)
            except:
                self.message_error06()
            globals().update(a)
            json_file.close()
        try:
            self.image_path1 = os.path.abspath(os.path.dirname(__file__)) + path1       #通过全局变量path转化为相对路径image_path
            self.image_path2 = os.path.abspath(os.path.dirname(__file__)) + path2
        except:
            self.message_error07()

    def set_init_window(self):
        '''
        窗口界面设置部分
        '''
        #程序名称、大小、出现位置、和变量配置设置
        self.init_window_name.title("模拟进程FCFS调度过程_v1.2")
        self.init_window_name.geometry('1024x768+100+100')
        self.__read_config()

        #文字内容部分
        self.init_data_label = Label(self.init_window_name, text="模拟进程FCFS调度", font=tkFont.Font(size=30, weight=tkFont.BOLD))
        self.init_data_label.place(x=512, y=30, anchor='center')
        self.result_data_label = Label(self.init_window_name, text="模拟结果：", font=tkFont.Font(size=20, weight=tkFont.BOLD))
        self.result_data_label.place(x=10, y=250, anchor='sw')
        self.tip_information_label = Label(self.init_window_name, text="样例文件是程序根目录下的/resources/date/FS.csv文件，如果要更改文件内容，请按照文件内的格式修改！", font=('Arial', 12), foreground="red")
        self.tip_information_label.place(x=512, y=140, anchor='center')

        #文本框部分
        self.result_data_Text = Text(self.init_window_name, width=142, height=30, font=tkFont.Font(size=12, weight=tkFont.BOLD))
        self.result_data_Text.place(x=10, y=285)

        #图片配置部分
        # image = Image.open(Image_Location)
        # image = image.resize((250, 250), Image.ANTIALIAS) #The (250, 250) is (height, width)
        # self.image_path1 = os.path.abspath("./resources/选择文件.png")
        # self.image_path2 = os.path.abspath("./resources/开始模拟.png")
        self.img1 = PhotoImage(file=self.image_path1)
        self.img2 = PhotoImage(file=self.image_path2)

        #按钮部分
        self.read_file_button = Button(self.init_window_name, image=self.img1, bd=0, command=self.data)
        self.read_file_button.place(x=512, y=100, anchor='center')
        self.start_button = Button(self.init_window_name,  image=self.img2, bd=0, command=self.start_simulate)
        self.start_button.place(x=900, y=230, anchor="center")
    
    def timeAdd(self, t1, t2):
        '''
        对于FCFS的时间time对象进行加法运算，
        并返回一个时间对象
        '''
        r = t1.getkey() + t2
        hour, minute = r//60, r%60
        result = FCFS.time(hour, minute)
        return result

    def average(self, value, n):
        '''
        求平均值函数
        参数列表：
            value：数量总和
            n：个数
        返回值：返回一个float，其值等于传入数据的平均值
        '''
        return value/n

    def getinput(self, fpath):
        '''
        读取csv文件函数
        参数列表：fpath：为csv文件的绝对路径
        返回值：返回处理后的文件数据f，数据类型为list
        '''
        f = pd.read_csv(fpath)
        f = f.reset_index(drop=True)
        f = f.values.tolist()
        return f

    def data(self):
        '''
        选择文件按钮绑定的文件选择函数，
        打开一个文件选择框并读取用户选择文件的绝对路径后，
        将绝对路径存储在MY_GUI的fpath属性内
        '''
        #打开一个文件选择框并读取选择的文件的绝对路径
        self.fpath = filedialog.askopenfilename(title=u'选择csv文件', initialdir=(os.path.expanduser(os.path.abspath(os.path.dirname(__file__)))))
        print('打开文件：', self.fpath)

        #未选择文件时的错误弹窗提示
        if self.fpath != '':
            self.message_showinfo()
        else:
            self.message_error01()

    def message_showinfo(self):
        '''
        弹窗消息提示
        '''
        top = tkinter.Tk()
        top.withdraw()  # ****实现主窗口隐藏
        top.update()  # *********需要update一下
        tkinter.messagebox.showinfo(title="提示", message="打开文件成功！")
        top.destroy()

    def message_error01(self):
        '''
        错误警告弹窗(下同)
        '''
        top = tkinter.Tk()
        top.withdraw()
        top.update()
        tkinter.messagebox.showerror(title="错误01", message="打开文件失败，请检查文件路径是否正确！错误代码：01")
        top.destroy()

    def message_error02(self):
        top = tkinter.Tk()
        top.withdraw()
        top.update()
        tkinter.messagebox.showerror(title="错误02", message="发生意外错误，请检查文件内容是否符合规范！错误代码：02")
        top.destroy()

    def message_error03(self):
        top = tkinter.Tk()
        top.withdraw()
        top.update()
        tkinter.messagebox.showerror(title="错误03", message="发生了一个预期之外的错误！错误代码：03")
        top.destroy

    def message_error04(self):
        top = tkinter.Tk()
        top.withdraw()
        top.update()
        tkinter.messagebox.showerror(title="错误04", message="发生了一个预期之外的错误！错误代码：04")
        top.destroy()

    def message_error05(self):
        top = tkinter.Tk()
        top.withdraw()
        top.update()
        tkinter.messagebox.showerror(title="错误05", message="读取数据失败！尚未选择任何文件！错误代码：05")
        top.destroy()
    
    def message_error06(self):
        top = tkinter.Tk()
        top.withdraw()
        top.update()
        tkinter.messagebox.showerror(title="错误06", message="读取config.json失败，缺少文件./config/config.json  ！")

    def message_error07(self):
        top = tkinter.Tk()
        top.withdraw()
        top.update()
        tkinter.messagebox.showerror(title="错误07", message="加载图片失败，缺少文件./resources  ！")
    
    def message_error08(self):
        top = tkinter.Tk()
        top.withdraw()
        top.update()
        tkinter.messagebox.showerror(title="错误08", message="发生了一个意料之外的错误：加载模式选择信息错误！错误代码：08")

    def choose_mode(self):
        '''
        因为模拟过程有三种算法，
        故需要一个模式选择函数。

        函数效果为创建一个弹窗并提供三个按钮进行模式选择
        '''
        pw = popup_display(self.init_window_name)       #弹窗对象的创建和储存
        self.init_window_name.wait_window(pw)       #等待弹窗对象结束
        return

    def start_simulate(self):
        '''
        模拟运行的数据计算部分
        分别有reset_list方法、count_next_item方法、do_average方法、sort_after方法。
        各方法的说明在方法内有

        start_simulate分为四部分：模式选择部分、数据导入部分、数据处理部分和数据展示部分
        '''
        def reset_list():
            '''
            根据ls的数据内容进行时间排序，并计算出第一个进行的进程的各项数据
            '''
            self.ls.sort(key=lambda x:x.arrive.getkey())        #根据时间排序

            self.ls[0].start = self.ls[0].arrive
            self.ls[0].finish = self.timeAdd(self.ls[0].start, self.ls[0].zx)
            self.ls[0].zz = self.ls[0].finish.getkey()-self.ls[0].arrive.getkey()
            self.ls[0].zzxs = self.ls[0].zz/self.ls[0].zx
            self.total_zz = self.ls[0].zz
            self.total_zzxs = self.ls[0].zzxs

        def count_next_item():
            '''
            除了第一个进程后，其他进程通过前面进程的信息递推计算出当前进程的信息内容
            '''
            if self.ls[i].arrive.getkey()<=self.ls[i-1].finish.getkey():
                self.ls[i].start = self.ls[i-1].finish
            else:
                self.ls[i].start = self.ls[i].arrive

            self.ls[i].finish = self.timeAdd(self.ls[i].start, self.ls[i].zx)
            self.ls[i].zz = self.ls[i].finish.getkey()-self.ls[i].arrive.getkey()
            self.ls[i].zzxs = self.ls[i].zz/self.ls[i].zx
            self.total_zz+=self.ls[i].zz
            self.total_zzxs+=self.ls[i].zzxs

        def do_average():
            '''
            平均值的计算部分
            '''
            self.average_zz = self.average(self.total_zz, self.n)
            self.average_zzxs = self.average(self.total_zzxs, self.n)

        def sort_after(ls, i, n):
            '''
            在先到先运行的基础上加入了优先级的概念后，
            需要在每次先到先运行的时候进行一次进程运行中等待队列的优先级排序，
            而sort_after函数的功能是通过读取列表和i、n参数，
            确定当列表第i-1项进程运行的时候，
            等待队列内的进程内容，并对其进行优先级排序

            参数列表：
                ls：存放进程信息FCFS对象的列表，数据类型为list
                i：未排序部分的开始指针，数据类型为int
                n：ls列表的数据长度，数据类型为int
            '''
            left, right = 0, 0
            left = i
            if n-i>1:
                for j in range(i, n):
                    #判断当前j指向的进程是否是在i-1进程运行时间内进入了等待队列，并获取等待队列的范围
                    if ls[j].arrive.getkey()<= ls[i-1].finish.getkey():     
                        right = j
                    else:
                        break
                #根据等待队列的范围对等待队列进行优先级排序
                ls[left:right+1] = sorted(ls[left:right+1], key=lambda x:x.good, reverse=True)
                return ls
            else:
                return ls

        #选择运行模式
        if self.fpath != '':
            self.choose_mode()
        else:
            self.message_error05()
            return 0
        print("选择完毕，模式为{}".format(self.simulate_mode))

        print("导入数据中……")
        #导入数据
        try:
            f = self.getinput(self.fpath)
            self.ls=[]
            self.n=0
            for information in f:
                self.ls.append(FCFS(information))
                self.n+=1
        except:
            self.message_error02()
            return 0
        print("导入完成！")

        print("数据处理中……")
        #数据处理部分
        #模式1：先到先运行模拟
        if self.simulate_mode==1:
            try:
                reset_list()
                for i in range(1, self.n):
                    count_next_item()
                do_average()
            except:
                self.message_error03()
                return 0

            try:
                self.print_result(self.ls)
                return 0
            except:
                self.message_error04()
                return 0
        
        #模式2：先到先运行的基础上根据优先级进行排序
        elif self.simulate_mode==2:
            #数据处理部分
            try:
                reset_list()
                for i in range(1,self.n):
                    self.ls = sort_after(self.ls, i, self.n)        #在先到先运行的基础上加入了优先级的排序
                    count_next_item()
                do_average()
            except:
                self.message_error03()
                return 0

            try:
                self.print_result(self.ls)
                return 0
            except:
                self.message_error04()
                return 0

        #模式3：时间片轮转模拟
        elif self.simulate_mode==3:
            #数据处理部分
            '''
            时间片轮转模拟思路为：
                完全模拟进程运行，以1分钟为单位时间循环递推，直到所有进程全部运行完毕。
                时间递推中，有2个事件会结束一次时间片：
                    1.时间片用完，正常结束
                    2.进程运行完成，需要进行运行完成后的状态数值的赋值
                有另外两个事件会需要暂停递推，完成特殊事件：
                    1.有新的进程在当前时间点进入就绪队列
                    2.进程运行完成，需要进行运行完成后的状态数值的赋值
                
                存在三个队列：
                    ls：获得数据时的进程存储队列
                    queue：进程的就绪队列
                    finish_list：进程的运行完成的存储队列
                存在一个进程变量：
                    process：用来保存当前正在cpu中运行的进程
                存在辅助变量：
                    time_cutting：通过弹窗后输入获取，是时间片的时间长度，数据类型为整数
                    now_time：是cpu运行模拟过程的当前时间，单位为分钟，数据类型为整数
                    times：是时间片轮转模拟的次数
                    start_time：开始时间，用于存放一个time对象，时间对应为当前时间，随后将这个对象赋值给进程的first属性，也用于在每一次轮转后输出本次轮转开始时间
                    temp：中转变量，用于暂时存放进程对象
                    arr_time：到达时间，用于存放一个time对象，时间对应为当前时间，随后将这个对象赋值给进程的arr属性
                    finish_time：完成时间，用于存放一个time对象，时间对应为当前时间，随后将这个对象赋值给进程的finish属性
                    echo：一个布尔变量，用于表达是否因为进程结束而中途退出了cpu，结束了时间片
            '''
            self.result_data_Text.delete(1.0, END)      #清空输出文本框内容

            self.ls.sort(key=lambda x:x.arrive.getkey())        #按照到达时间排序
            
            #数据初始化部分
            finish_list=[]
            queue=[self.ls.pop(0)]
            now_time = queue[0].arrive.getkey()
            time_cutting = askstring("获取时间片长度", "请输入一个整数作为时间片的长度（单位：分钟）", initialvalue=8)
            #第一个进程的部分属性的计算赋值
            queue[0].first = queue[0].arrive
            queue[0].arr = queue[0].arrive
            self.total_zz = queue[0].zz
            self.total_zzxs = queue[0].zzxs

            times=0     #轮转次数
                        
            while queue != [] or self.ls != []:     #主循环，除非进程全部运行结束才会退出循环
                times+=1        #轮转次数+1
                start_time = FCFS.time()        #获取本次轮转的开始时间
                start_time.create_by_key(now_time)
                process = queue.pop(0)      #从就绪队列中取出第一个进程
                if process.is_first_time:       #如果取出的进程是第一次被取出（被运行），则记录第一次运行时间，并将进程中表示是否第一次运行的布尔值改变
                    process.first = start_time
                    process.is_first_time = False
                echo = True     #设置标记
                for i in range(time_cutting):       #单个时间片循环，循环次数等于时间片长度
                    if len(self.ls)!=0 and now_time >= self.ls[0].arrive.getkey():      #事件：当前时刻有新进程进入就绪队列
                        temp = self.ls.pop(0)
                        arr_time = FCFS.time()
                        arr_time.create_by_key(now_time)
                        temp.arr = arr_time
                        queue.append(temp)
                        del arr_time, temp
                    if process.zx == process.have_finished:     #事件：当前时刻进程运行完毕，需要进行进程属性的运算赋值
                        finish_time = FCFS.time()       #获取当前时间作为进程的完成时间
                        finish_time.create_by_key(now_time)
                        process.finish = finish_time
                        process.zz = now_time-process.arrive.getkey()
                        del finish_time
                        process.zzxs = process.zz/process.zx
                        self.total_zz += process.zz
                        self.total_zzxs += process.zzxs
                        echo = False        #改变标记的内容
                        break
                    
                    #时间递推
                    process.have_finished += 1
                    process.last_time = process.zx - process.have_finished
                    now_time+=1

                #输出本次轮转结果
                self.result_data_Text.insert(END, "第{}轮执行和就绪队列结果：\n".format(times))
                self.result_data_Text.insert(END, "ID号   名字  到达时间  总执行时间（分钟） 当前开始时间  已完成时间（分钟）  剩余完成时间（分钟）：\n")
                self.result_data_Text.insert(END, "{:^4}   {:^4}   {:>2}:{:0>2}        {:^4}            {:>2}:{:0>2}           {:^4}              {:^4}\n".format(process.id, process.name, process.arrive.hour, process.arrive.minute, process.zx, start_time.hour, start_time.minute, process.have_finished, process.zx-process.have_finished))
                start_time = FCFS.time()
                for i in queue:
                    self.result_data_Text.insert(END, "{:^4}   {:^4}   {:>2}:{:0>2}        {:^4}            {:>2}:{:0>2}           {:^4}              {:^4}\n".format(i.id, i.name, i.arrive.hour, i.arrive.minute, i.zx, start_time.hour, start_time.minute, i.have_finished, i.zx-i.have_finished))
                self.result_data_Text.insert(END, "\n")

                #通过是否有进程完成导致时间片结束来判断将正在运行的进程放回就绪队列还是放入完成队列中
                if echo:
                    queue.append(process)
                else:
                    finish_list.append(process)
                
                del start_time, process

            do_average()

            #结果的输出部分
            self.ls.sort(key=lambda x:x.finish.getkey())
            self.result_data_Text.insert(END, "ID号    名字   到达时间    执行时间（分钟） 首次开始时间    完成时间    周转时间（分钟）   带权周转时间（系数）：\n")
            for i in finish_list:
                self.result_data_Text.insert(END, "{:^4}    {:^4}    {:>2}:{:0>2}          {:^4}        {:>2}:{:0>2}            {:>2}:{:0>2}        {:^4}                {:.2f}\n".format(i.id, i.name, i.arrive.hour, i.arrive.minute, i.zx, i.first.hour, i.first.minute, i.finish.hour, i.finish.minute, i.zz, i.zzxs, i.arr.hour, i.arr.minute))
            self.result_data_Text.insert(END, "平均周转时间                                                             {:.2f}\n".format(self.average_zz))
            self.result_data_Text.insert(END, "平均带权周转时间系数                                                                          {:.2f}\n".format(self.average_zzxs))

        else:
            self.message_error08()
        print("数据处理完成！")

    def print_result(self, ls):
        '''
        根据数据计算排序的结果进行格式化输出
        '''
        #模式1：先到先运行模拟
        if self.simulate_mode==1:
            #数据输出部分
            self.result_data_Text.delete(1.0, END)
            self.result_data_Text.insert(END, "模拟进程FCFS调度过程输出结果：\n")
            self.result_data_Text.insert(END, "ID号     名字    到达时间    执行时间（分钟） 开始时间    完成时间    周转时间（分钟）    带权周转时间（系数）：\n")
            for i in self.ls:
                self.result_data_Text.insert(END, "{:^4}    {:^4}      {:>2}:{:0>2}          {:^4}        {:>2}:{:0>2}       {:>2}:{:0>2}          {:^4}                 {:.2f}\n".format(i.id, i.name, i.arrive.hour, i.arrive.minute, i.zx, i.start.hour, i.start.minute, i.finish.hour, i.finish.minute, i.zz, i.zzxs))
            self.result_data_Text.insert(END, "平均周转时间                                                            {:.2f}\n".format(self.average_zz))
            self.result_data_Text.insert(END, "平均带权周转时间系数                                                                          {:.2f}\n".format(self.average_zzxs))
        
        #模式2：先到先运行的基础上根据优先级进行排序
        elif self.simulate_mode==2:
            self.result_data_Text.delete(1.0, END)
            self.result_data_Text.insert(END, "模拟进程FCFS调度过程输出结果：\n")
            self.result_data_Text.insert(END, "ID号    名字   优先级   到达时间    执行时间（分钟） 开始时间    完成时间    周转时间（分钟）   带权周转时间（系数）：\n")
            for i in self.ls:
                self.result_data_Text.insert(END, "{:^4}    {:^4}    {:^4}    {:>2}:{:0>2}          {:^4}        {:>2}:{:0>2}       {:>2}:{:0>2}          {:^4}                {:.2f}\n".format(i.id, i.name, i.good, i.arrive.hour, i.arrive.minute, i.zx, i.start.hour, i.start.minute, i.finish.hour, i.finish.minute, i.zz, i.zzxs))
            self.result_data_Text.insert(END, "平均周转时间                                                                  {:.2f}\n".format(self.average_zz))
            self.result_data_Text.insert(END, "平均带权周转时间系数                                                                               {:.2f}\n".format(self.average_zzxs))
        
        else:
            self.message_error08()

class popup_display(Toplevel):
    '''
    弹窗部分
    通过构造函数继承父类MY_GUI，并在按钮内显性的更新父类的simulate_mode属性
    更新完成后自动关闭弹窗
    '''
    def __init__(self, parent):
        super().__init__()
        self.init_window_name = self
        self.parents = MY_GUI
        self.set_init_window()
    
    def set_init_window(self):
        self.init_window_name.title("选择运行模式")
        self.init_window_name.geometry('600x400+200+200')

        self.message_title_label = Label(self.init_window_name, text="请选择一个模拟运行模式：", font=tkFont.Font(family='KaiTi', size=30, weight=tkFont.BOLD))
        self.message_title_label.pack()
        
        self.choose_first_mode_button = Button(self.init_window_name, text="先来先服务进程调度", font=tkFont.Font(size=20), bd=2, command=self.choose_first_mode)
        self.choose_first_mode_button.pack(expand='yes')
        self.choose_second_mode_button = Button(self.init_window_name, text="优先级进程调度", bd=2, font=tkFont.Font(size=20), command=self.choose_second_mode)
        self.choose_second_mode_button.pack(expand='yes')
        self.choose_second_mode_button = Button(self.init_window_name, text="时间片轮转进程调度", bd=2, font=tkFont.Font(size=20), command=self.choose_third_mode)
        self.choose_second_mode_button.pack(expand='yes')
    
    def choose_first_mode(self):
        self.parents.simulate_mode=1
        print("已选择模式1")
        self.init_window_name.destroy()
        return
    def choose_second_mode(self):
        self.parents.simulate_mode=2
        print("已选择模式2")
        self.init_window_name.destroy()
        return
    def choose_third_mode(self):
        self.parents.simulate_mode=3
        print("已选择模式3")
        self.init_window_name.destroy()
        return

def gui_start():
        init_window = Tk()
        ZMJ_PORTAL = MY_GUI(init_window)
        ZMJ_PORTAL.set_init_window()
        init_window.mainloop()

gui_start()
