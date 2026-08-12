try:                                #import
    from sys import argv as argv_sys    #import依赖
    from PyQt5.QtWidgets import (
        QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
        QLabel, QListWidget, QDialog, QMessageBox, QInputDialog, QTextEdit,QPlainTextEdit)
    from PyQt5.QtCore import Qt,QEvent
    from PyQt5.QtGui import QKeyEvent
    from json import load,dump,JSONDecodeError
    from time import gmtime
    from random import randint
    import pygame.mixer
    from pygame import error as mp3_error
    from openai import OpenAI,OpenAIError
    from datetime import date
    from pathlib import Path
    import numpy
except ImportError:                 #处理
    print("你的环境可能不适配<<Error>>")
    input("输入任意字符退出(｡•́︿•̀｡):")
    exit()
class Cal:                          #加减封装
    @staticmethod
    def buy(money, day, price):
        if money>price:
            money=money-price
            day=day+0.5
            return money,day,True
        return money,day,False
    @staticmethod
    def work(money,day,work_money):
        money=money+work_money
        day=day+0.5
        return money,day
class GUI:                          #GUI And 辅助
    DO=["逛街","小游戏","退出","背包","信息","设置","单张卡牌","猜拳"]
    STREET=["go","back"]
    STREET_IN=["yes", "no", "next"]
    SET_UP=["重置","日志查看","Root","返回", "AI设置", "Music设置", "公告"]
    SET_UP_AI=["API-KEY","URL","MODEL","NAME"]
    BAG=["eat", "返回"]
    MODEL_WHITE=("""
                    /* 1. 全局默认:白底深灰字 */
                    QWidget {
                        background-color: #ffffff;
                        color: #2c3e50;
                        font-family: "Microsoft YaHei";
                    }

                    /* 2. 标签:深色字,加粗 */
                    QLabel {
                        color: #2c3e50;
                        font-weight: bold;
                    }

                    /* 3. 输入框:纯白底,浅灰边框,聚焦变蓝 */
                    QLineEdit {
                        background-color: #ffffff;
                        color: #2c3e50;
                        border: 1.5px solid #dcdfe6;
                        border-radius: 6px;
                        padding: 5px 8px;
                    }
                    QLineEdit:focus {
                        border: 1.5px solid #409eff;
                    }

                    /* 4. 按钮:白底灰边框,悬浮变蓝 */
                    QPushButton {
                        background-color: #ffffff;
                        color: #2c3e50;
                        border: 1.5px solid #dcdfe6;
                        border-radius: 6px;
                        padding: 8px 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #ecf5ff;
                        border: 1.5px solid #409eff;
                        color: #409eff;
                    }
                    QPushButton:pressed {
                        background-color: #d9e8ff;
                        border: 1.5px solid #337ecc;
                    }

                    /* 5. 弹窗也变白 */
                    QDialog {
                        background-color: #ffffff;
                    }
                    QMessageBox {
                        background-color: #ffffff;
                    }
                """)
    MODEL_BLACK = """
    /* 1. 全局默认:黑底白字 */
    QWidget {
        background-color: #1e1e1e;
        color: #ffffff;
        font-family: "Microsoft YaHei";
    }

    /* 2. 标签:亮白字,加粗 */
    QLabel {
        color: #f0f0f0;
        font-weight: bold;
    }

    /* 3. 输入框:深灰底,亮白字,细边框 */
    QLineEdit {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #3a3a3a;
        border-radius: 5px;
        padding: 5px;
    }
    QLineEdit:focus {
        border: 1px solid #00bfff;
    }

    /* 4. 按钮:深空灰底,白字,圆角 */
    QPushButton {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #3a3a3a;
        border-radius: 8px;
        padding: 8px 15px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #3a3a3a;
        border: 1px solid #00bfff;
    }
    QPushButton:pressed {
        background-color: #1a1a1a;
    }

    /* 5. 弹窗（对话框）黑化 */
    QDialog {
        background-color: #1e1e1e;
    }
    QMessageBox {
        background-color: #1e1e1e;
    }

    /* ====== 新增:修复“边缘白色”问题 ====== */
    /* 列表控件（如选项列表） */
    QListWidget {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #3a3a3a;
        outline: none;          /* 去除焦点虚线框 */
    }
    QListWidget::item {
        background-color: #1e1e1e;
        color: #ffffff;
        padding: 4px;
    }
    QListWidget::item:selected {
        background-color: #3a3a3a;   /* 选中项高亮 */
    }

    /* 文本编辑控件（公告编辑） */
    QTextEdit {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #3a3a3a;
    }
    QScrollArea {
        background-color: #1e1e1e;   /* 滚动区域背景 */
        border: none;
    }
    QScrollBar:vertical {
        background: #2d2d2d;
        width: 12px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #5a5a5a;
        border-radius: 6px;
        min-height: 20px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    QScrollBar:horizontal {
        background: #2d2d2d;
        height: 12px;
        margin: 0px;
    }
    QScrollBar::handle:horizontal {
        background: #5a5a5a;
        border-radius: 6px;
        min-width: 20px;
    }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        width: 0px;
    }"""

    @staticmethod
    def _button_click(choice,  #button弹窗辅助关闭
                    window_button,
                    result):
        result[0] = choice
        window_button.accept()

    @staticmethod
    def _text_close(window_text#大型text弹窗辅助关闭
                    ):
        window_text.accept()

    @staticmethod
    def input(word="",    #GUI弹窗
                add_word_or_choice=None,
                model="msg",
                title="----",
                integer_lower=0,#最小是特殊弹窗调用
                integer_upper=100):#最大同上
        input_return=False
        if model=="msg":
            input_return=QMessageBox.information(None, title, f"{word}{add_word_or_choice}")
        elif model == "button":
            if not add_word_or_choice:
                return None
            if len(add_word_or_choice) > 8:
                dlg = QDialog()
                dlg.setWindowTitle(title)
                layout = QVBoxLayout()
                
                layout.addWidget(QLabel(word))
                
            # 带滚动条的列表
                list_widget = QListWidget()
                for item in add_word_or_choice:
                    list_widget.addItem(str(item))
                layout.addWidget(list_widget)
                
                # “选择”按钮
                result = [None]
                btn_ok = QPushButton("选择")
                def on_select():
                    current = list_widget.currentItem()
                    if current:
                        result[0] = current.text() # type: ignore
                        dlg.accept()
                btn_ok.clicked.connect(on_select)
                layout.addWidget(btn_ok)
                
                dlg.setLayout(layout)
                dlg.resize(250, 300)  # 固定大小,带滚动条
                dlg.exec_()
                return result[0]
            else:
                window = QDialog()
                window.setWindowTitle(title)
                layout = QVBoxLayout()
                layout.addWidget(QLabel(word))
                result = [None]
                for choice in add_word_or_choice:
                    btn = QPushButton(choice)
                    btn.clicked.connect(lambda checked, ch=choice: GUI._button_click(ch, window, result))
                    layout.addWidget(btn)
                window.setLayout(layout)
                window.exec_()
                return result[0]
        elif model=="enter":
            parent_father = QApplication.activeWindow()
            input_return, ok = QInputDialog.getText(parent_father, title, f"{word}{add_word_or_choice}")
            if not ok:
                input_return=ok
        elif model=="yn":
            input_return = QMessageBox.question(None, title, f"{word}{add_word_or_choice}", QMessageBox.Yes | QMessageBox.No)
            if input_return==QMessageBox.Yes:
                return True
            else:
                return False
        elif model=="integer":
            parent_father = QApplication.activeWindow()
            input_return, ok = QInputDialog.getInt(parent_father, title, f"{word}{add_word_or_choice}", value=integer_lower, min=integer_lower, max=integer_upper)
            if not ok:
                input_return=ok
        elif model=="text":
            dlg = QDialog()
            dlg.setWindowTitle(title)

            layout = QVBoxLayout()
            text_edit = QTextEdit()
            text_edit.setPlainText(f"{word}{add_word_or_choice}")
            layout.addWidget(text_edit)

            btn_close = QPushButton("关闭")
            btn_close.clicked.connect(lambda: GUI._text_close(dlg))
            layout.addWidget(btn_close)
            dlg.setLayout(layout)
            dlg.resize(600, 300)
            dlg.exec_()
            input_return=text_edit.toPlainText()
        return input_return
class TimeManageAndStartNotice:     #时间管理

    @staticmethod
    def now_time():  # 东八time
        time_now_is = gmtime()
        y = time_now_is[0]
        mo = time_now_is[1]
        d = time_now_is[2]
        h = time_now_is[3]
        mi = time_now_is[4]
        s = time_now_is[5]
        h = h + 8
        if h > 24:
            h=h-24
        if h > 12:
            h = h - 12
            m = "pm"
        else:
            m = "am"
        time_now = f'{y}-{mo}-{d}-{h}{m}:{mi}:{s}'
        return time_now

    @staticmethod
    def now_time_1am_or_2pm():
        time_now_is = gmtime()
        h = time_now_is[3]
        h = h + 8
        if h > 24:
            h=h-24
        if h < 12:
            h_am_or_pm=1
        else :
            h_am_or_pm=2
        return h_am_or_pm

    @staticmethod
    def get_year_to_day():
        time_now_is = gmtime() 
        y = time_now_is[0]
        mo = time_now_is[1] 
        d = time_now_is[2]
        return {"year":y,"month":mo,"day":d}

    @staticmethod
    def time_to_now_gap(time):
        time_now=TimeManageAndStartNotice.get_year_to_day()
        date1 = date(time["year"], time["month"], time["day"])
        date2 = date(time_now["year"], time_now["month"], time_now["day"])
        gap = date2 - date1
        return abs(gap.days)
class Music:                        #音乐管理
    freqs = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]
    _sound = None          # 类变量保存当前播放的 Sound 对象
    _initialized = False   # 类变量标记 mixer 是否已初始化

    @classmethod
    def _init_mixer(cls):
        if not cls._initialized:
            pygame.mixer.init(frequency=44100, size=-16, channels=1)
            cls._initialized = True

    @staticmethod
    def make_tone(frequency):
        duration = 0.3
        sample_rate = 44100
        gap = 0.05
        t = numpy.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        wave = numpy.sin(2 * numpy.pi * frequency * t)
        wave = (wave * 32767).astype(numpy.int16)
        silence = numpy.zeros(int(sample_rate * gap), dtype=numpy.int16)
        return numpy.concatenate([wave, silence])

    @classmethod
    def play_random_music_loop(cls, num_notes=1000):
        cls._init_mixer()
        indices = [randint(0, 6) for _ in range(num_notes)]
        freqs = [cls.freqs[i] for i in indices]
        waves = [cls.make_tone(f) for f in freqs]
        full_wave = numpy.concatenate(waves)
        if cls._sound:
            cls._sound.stop()
        cls._sound = pygame.mixer.Sound(buffer=full_wave.tobytes())
        cls._sound.play(loops=-1)

    @classmethod
    def stop_random_music(cls):
        if cls._sound:
            cls._sound.stop()
            cls._sound = None
            Music._initialized = False
            pygame.quit()

    @staticmethod
    def play_mp3_loop(filepath):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(filepath) 
            pygame.mixer.music.play(-1)
        except mp3_error:
            GUI.input("不影响使用的Error\n音频错误\n请检查mp3是否存在","","msg","Error")
            return CustomTxt.MUSIC_ERROR

    @staticmethod
    def stop_mp3():
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except mp3_error:
            pass
class JsonSaveAndRead:              #json save及read
    def __init__(self,file_path,init_date):
        self.init_date=init_date
        self.path=Path(file_path)
        self.file_check()
        

            #定义文件操作
    def file_check(self):#检查file正常/存在
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            with open(self.path,'w', encoding='utf-8') as f:
                dump(self.init_date, f, ensure_ascii=False)
            return False
        
        try:
            with self.path.open('r+', encoding='utf-8') as file:
                file_try = load(file)
                if not isinstance(file_try, dict):
                    self.init_to_film()
            return True
        except (JSONDecodeError, ValueError, EOFError):
            self.init_to_film()
            return False


    def init_to_film(self):     #格式化
        with open(self.path,'r+',encoding="UTF-8") as file:
            file.seek(0)
            file.truncate(0)
            dump(self.init_date,file,ensure_ascii=False)

    def save_to_file(self, key, value):         #将json的list的值替换并存储
        with open(self.path,'r+',encoding="UTF-8") as file:
            filelist=load(file)
            filelist[key]=value
            file.seek(0)
            file.truncate(0)
            dump(filelist, file, ensure_ascii=False)

    def read_from_file(self, key):       #读json的list并读取对应值
        with open(self.path,'r+',encoding="UTF-8") as file:
            file.seek(0)
            save_file_list=load(file)
            if not save_file_list:
                self.init_to_film()
            return save_file_list.get(key,"")
class TxtSaveAndRead:               #txt save and read
    def __init__(self,file_path):
        self.path=Path(file_path)
        self.file_check()
    
                #定义文件操作
    def file_check(self):#检查file正常/存在
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            with self.path.open('w', encoding='UTF-8') as f:
                dump("", f, ensure_ascii=False)
            return None

    def read(self):
        with open(self.path,"r+",encoding="UTF-8") as file:
            file.seek(0)
            return file.read()

    def add_save(self,add_word,error=False):
        with open(self.path,"a+",encoding="UTF-8") as file:
            word=f"<{TimeManageAndStartNotice.now_time()}>\t<{add_word}>\n"
            if error:
                word=f"Error:{word}"
            file.write(word)

    def init_file(self):
        with open(self.path,"r+",encoding="UTF-8") as file:
            file.seek(0)
            file.truncate(0)
    def write(self,word):
        self.init_file()
        with open(self.path,"w+",encoding="UTF-8") as file:
            file.write(word)
class CustomTxt:                    #自定义txt save提示词
    NUMBER="V1.9.0-Stable"
    AI_WIFI_ERROR="WifiError in AI-chat"
    AI_OPENAI_ERROR="OpenAIError in AI-chat"
    MUSIC_ERROR="Did not use mp3"
    GAME_NUMBER=f"Pet Game-{NUMBER}"
    SETTING_AI="Setting AI-chat"
    OVER_GAME="CLOSE Pet Game"
    OPEN_GAME="OPEN Pet game"
    SETTING_MUSIC="Setting Music"
    AI_AUTO_REMOVE="AI-chat-List Auto-Remove"
    BUY="Buy"
    EAT="Eat"
    PLAY="Play"
    ROOT=["NoRoot","noroot","NOROOT","no-root","NO-ROOT","No-Root"]
    NOTICE=f"""版本:{NUMBER}\n公告:
            \t1.1.0完成框架 
            \t1.2.0补充丰富内容
            \t1.2.5修复了背包及食物购买页面退不出来的问题
            \t1.3.0新增在逛街及进食时增加好感
            \t1.3.5对公告及重置进行了优化
            \t1.4.0新增(优化)了食物购买页面持续购买的功能
            \t1.4.5卡牌脚本正式迁移pet game1.45
            \t1.5.0主程序用类改写
            \t1.6.0用Qt(PyQt)作为UI,并改写,替代旧UI新增页面的白天黑夜(不同时间启动不同颜色)
            \t1.6.5添加AI对话,5日记忆,三十轮对话
            \t1.7.0同时贴合linux,windows系统
            \t1.7.5使用树型文件结构,并推出随机音频背景音乐
            \t1.8.0加入日志功能
            \t1.8.5丰富日志功能
            \t1.9.0加入虚拟终端"""
class GameState:                    #封装JsonSaveAndRead
    def __init__(self, save_read_handle):
        if not isinstance(save_read_handle, JsonSaveAndRead):
            raise TypeError("save_read_handle must be JsonSaveAndRead instance")
        self._storage = save_read_handle  
        self.last_state = None
        self.name = ""
        self.money = 0
        self.day = 0
        self.pet = ""
        self.favor = 0
        self.backpack = []
        self.open_mp3 = 1
    
    def save(self):
        #批量存储游戏状态
        self.backpack.sort()
        self._storage.save_to_file("day", self.day)
        self._storage.save_to_file("money", self.money)
        self._storage.save_to_file("name", self.name)
        self._storage.save_to_file("pet", self.pet)
        self._storage.save_to_file("favor", self.favor)
        self._storage.save_to_file("time", self.last_state)
        self._storage.save_to_file("backpack", self.backpack)
        self._storage.save_to_file("open_mp3", self.open_mp3)
    
    def load(self):
        #批量加载游戏状态
        try:
            self.name = self._storage.read_from_file("name") or ""
            self.day = self._storage.read_from_file("day") or 0
            self.money = self._storage.read_from_file("money") or 0
            self.pet = self._storage.read_from_file("pet") or ""
            self.last_state = self._storage.read_from_file("time") or ""
            self.favor = self._storage.read_from_file("favor") or 0
            self.backpack = self._storage.read_from_file("backpack") or []
            self.open_mp3 = self._storage.read_from_file("open_mp3") or 0
        except (FileNotFoundError,PermissionError,AttributeError,OSError):
            self._storage.init_to_film()


            #游戏类
class ShingSort:                    #购买list管理
    def __init__(self,model):
        self.shing_sort=model
        self.shing_now={}
        self.shing_name=[]
        self.shing_price=[]
    def get_price(self,shing):
        shing_price=self.shing_sort[shing]
        return shing_price
    
    def fresh_shing_sort(self):
        self.shing_now={}
        for shing_key,shing_value in self.shing_sort.items():
            probability=randint(0,10)
            if probability<5:
                self.shing_now[shing_key]=shing_value
        return None
    
    def fresh_shing_name(self,model=False):        #model决定name从shing_sort/shing_now中获取
        self.shing_name=[]
        if model:
            for shing_name in self.shing_now.keys():
                self.shing_name.append(shing_name)
        else:
            for shing_name in self.shing_sort.keys():
                self.shing_name.append(shing_name)
    def fresh_shing_price(self,model=False):        #model决定price从shing_sort/shing_now中获取
        self.shing_price=[]
        if model:
            for shing_price in self.shing_now.values():
                self.shing_price.append(shing_price)
        else:
            for shing_price in self.shing_sort.values():
                self.shing_price.append(shing_price)
class SmallCardGame:                #最小卡牌单元类
    def __init__(self):
        self.play=[]
    def out(self, card_number):
        card_number = int(card_number)
        self.play.remove(card_number)        
        return True
    def have(self, number_sort):
        self.play.sort()
        if number_sort=={}:
            return None
        card_list=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]#11J 12Q 13K 14XW 15DW
        for sort_k,sort_v in number_sort.items():
            if sort_v==0:
                card_list.remove(sort_k)
        random_over=randint(0,len(card_list)-1)
        v=card_list[random_over]
        number_sort[v]-=1
        self.play.append(v)
        return number_sort
class Card:                         #完整卡牌功能类

    def __init__(self):
        self.last=0
        self.choice = ["退出", "出牌", "pass"]
        self.sort={1:4,2:4,3:4,4:4,5:4,6:4,7:4,8:4,9:4,10:4,11:4,12:4,13:4,14:1,15:1}
        self.playMY=SmallCardGame()
        self.playAI=SmallCardGame()

    def ai_say(self):    #历遍ai牌找符合要求最小值
        ai_t_card=[]
        for out_card in self.playAI.play:
            if out_card>self.last:
                ai_t_card.append(out_card)
        if not ai_t_card:
            self.last = 0
            return "pass"
        return_say=min(ai_t_card)
        self.last=return_say
        self.playAI.out(return_say)
        return return_say
    def is_big(self, number):     #是否bigger than last(上家出的牌)
        if self.last>number or self.last==number:
            return False
        elif self.last<number:
            return True
        return False
    def my_card_format(self):     #为GUI.input的buttonbox做准备
        card_choice = []
        for out_card in self.playMY.play:
            ch = str(out_card)
            card_choice.append(ch)
        return card_choice
        #卡牌游戏类over
class CardGame:                     #完整卡牌系统类
        def __init__(self):
            pass

        @staticmethod
        def run(money,day):
            card = Card()
            add_money=0
            GUI.input("ready!", "", "msg", "提示")
            for _ in range(27):  # 抽牌
                card.sort = card.playMY.have(card.sort)
                card.sort = card.playAI.have(card.sort)
            while True:  # run
                game_to_do = GUI.input(f"you:{card.playMY.play}", card.choice, "button", "卡牌对战")
                if game_to_do == "退出":
                    break
                if game_to_do == "出牌":
                    choice = card.my_card_format()
                    me_out_card = GUI.input(f"{card.playMY.play}c:", choice, "button", "出牌选择")
                    if not me_out_card:
                        continue
                    me_out_card = int(me_out_card)
                    if card.is_big(me_out_card):
                        card.playMY.out(me_out_card)
                        card.last = me_out_card
                    else:
                        continue
                if game_to_do == "pass":
                    card.last = 0
                if game_to_do == "出牌" or game_to_do == "pass":
                    ai_say = card.ai_say()
                    GUI.input(f"ai:{ai_say}", "", "msg", "AI回应")

                    # 胜利判定
                if len(card.playAI.play) <= 0:
                    GUI.input("ai win", "", "msg", "游戏结束")
                    break
                if len(card.playMY.play) <= 0:
                    GUI.input("you win", "", "msg", "游戏胜利")
                    add_money=10 * len(card.playAI.play)
                    money, day = Cal.work(money, day, 10 * len(card.playAI.play))
                    GUI.input(f"得到{add_money}元", "", "msg", "money")
                    break
            return money, day, add_money
class RockPaperScissors:            #猜拳系统类
        def __init__(self):
            pass

        @staticmethod
        def run(money,day):
            while True:
                rock_paper_scissors=["石头","布","剪刀"]
                rock_paper_scissors_dict={"石头":0,"布":1,"剪刀":2}
                game_do_to=GUI.input("你出:",rock_paper_scissors, "button",title="ai猜拳")
                if not game_do_to:
                    break
                game_do_to=rock_paper_scissors_dict.get(game_do_to)
                probability=randint(1,10)
                if probability>3:
                    ai_say=(game_do_to+1)%3
                else:
                    ai_say=(game_do_to+2)%3
                over=(game_do_to-ai_say)%3
                if over==1:#you win
                    GUI.input("you win", "", "msg", "游戏胜利")
                    money,day=Cal.work(money,day,30)
                    add_money=30
                    GUI.input("得到30元","","msg","money")
                if over==2:#AI win
                    GUI.input("ai win", "", "msg", "游戏")
                    money,day,check=Cal.buy(money,day,30)
                    add_money=-30
                    GUI.input("输了30元","","msg","money")
                if over==0:#==
                    add_money=0
                    GUI.input("everyone is not win", "", "msg", "游戏")
            return money,day,add_money
class DigitalBomb:                  #数字炸弹系统类
    def __init__(self):
        pass

    @staticmethod
    def run(money, day):
        lower = 0
        upper = 100
        over=randint(lower,upper)
        money_last=money
        money_over=0
        while True:
            number=GUI.input(f"输入:{lower}-{upper}", "","integer",title="数字炸弹", integer_lower=lower+1, integer_upper=upper-1)
            if not number:
                break
            try:
                if over==number:
                    money,day=Cal.work(money,day,money_over)
                    break
                elif over>number:
                    lower=number
                elif over<number:
                    upper=number
                money_over=money_over+10
            except (TypeError,ValueError):
                GUI.input("输入数字!", "", "msg", "警告!警告!警告!")
                continue
        add_money=money-money_last
        GUI.input(f"{add_money}元","","msg","money")

        return money,day,add_money
class AI:                           #最小AI-chat单元
    def __init__(self):
        self.AI_time = None
        self.AI_chat = None
        self.date=JsonSaveAndRead("file_date/.AI_date.json",{"NAME":"AI宠物","APIKEY":"","URL":"","MODEL":"","LAST":{}})
        self.model=self.date.read_from_file("MODEL")
        self.last=self.date.read_from_file("LAST")
        self.api_key=self.date.read_from_file("APIKEY")
        self.url=self.date.read_from_file("URL")
        self.name=self.date.read_from_file("NAME")

    def change_set(self,model="",apikey="",url="",name=""):
        self.date.save_to_file("APIKEY",apikey)
        self.date.save_to_file("URL",url)
        self.date.save_to_file("MODEL",model)
        self.date.save_to_file("NAME",name)

    def init(self):
        try:
            self.AI_chat = OpenAI(
                            api_key=self.api_key,
                            base_url=self.url       )
        except OpenAIError:
            return CustomTxt.AI_OPENAI_ERROR
        self.AI_time=TimeManageAndStartNotice()
        return None

    def chat(self,ask):
        try:
            answer_ = self.AI_chat.chat.completions.create(
                    model=self.model,
                    messages=[
                {"role": "system", "content": f"你是用户的好朋友,叫{self.name},在和他聊天,上文:{list(self.last.keys())}"},
                {"role": "user", "content": ask}]
                )
        except OpenAIError:
            GUI.input("网络请求失败","","msg","")
            return CustomTxt.AI_WIFI_ERROR
        answer=answer_.choices[0].message.content
        self.last[f"用户:{ask}"]=self.AI_time.get_year_to_day()
        self.last[f"你:{answer}"]=self.AI_time.get_year_to_day()
        self.date.save_to_file("LAST",self.last)
        return answer

    def auto_remove(self):
        to_del=[]
        day_max=5
        number_max=30
        for key,value in self.last.items():
            gap=self.AI_time.time_to_now_gap(value)
            if gap >= day_max :
                to_del.append(key)
        number=number_max
        for key in reversed(self.last):
            number=number-1
            if number <= 0:
                to_del.append(key)
        for key in set(to_del):
            del self.last[key]
        self.date.save_to_file("LAST",self.last)
class AIChat:                       #完整AI-chat系统
    def __init__(self):
        self._run=True
        self.ask="Hello"
        self.answer="< Hello >"
        self.AI_chat=AI()
        self.check=self.AI_chat.init()
        self.txt=TxtSaveAndRead("file/date.txt")
    def run(self):
        if self.check==CustomTxt.AI_OPENAI_ERROR:
            GUI.input("您未配置成功AI","","msg","Error")
            return CustomTxt.AI_OPENAI_ERROR
        while self._run:
            self.ask=GUI.input("聊天(N退出)","","enter","AI宠物")
            if self.ask == "n" or self.ask == "N" or not self.ask:
                self._run=False
                continue
            self.answer=self.AI_chat.chat(self.ask)
            GUI.input(f"\t{self.AI_chat.name}:\n{self.answer}","","msg","对话")
        self.AI_chat.auto_remove()
        self.txt.add_save(CustomTxt.AI_AUTO_REMOVE)
        return None
class Game:                         #对游戏类封装

    @staticmethod
    def digital_bomb_run(money,day):
        money,day,add_money=DigitalBomb.run(money,day)
        return money,day,add_money

    @staticmethod
    def card_run(money,day):
        money,day,add_money=CardGame.run(money,day)
        return money,day,add_money

    @staticmethod
    def rock_paper_scissors_run(money,day):
        money,day,add_money=RockPaperScissors.run(money,day)
        return money,day,add_money

    @staticmethod
    def ai_chat_run():
        ai_chat_go=AIChat()
        check=ai_chat_go.run()
        if check==CustomTxt.AI_OPENAI_ERROR:
            return check
        return None
          #主程序
class PetWindow(QWidget):           #主窗口
    def __init__(self):
        super().__init__()
        #创建对象
        self.save_read = JsonSaveAndRead('file_date/.save.json',{"name": "", "day": 1, "money": 0, "pet":"", "time":"", "favor":0,"backpack":[],"open_mp3":1})#实例化文件管理
        self.txt = TxtSaveAndRead("file_date/date.txt")
        self.state = GameState(self.save_read)   #实例化快捷文件管理
        self.shop = ShingSort(                #实例化商店管理
                {"apple": 40, "banana": 30, "chicken": 70,
                "beef": 90, "pork": 80, "shrimp": 100,
                "tofu": 30, "noodle": 40, "pasta": 50,
                "cheese": 60, "yogurt": 40, "butter": 50,
                "jam": 30, "honey": 60, "oat": 30,
                "barley": 40, "quinoa": 70, "lentil": 40, 
                "pea": 30,"carrot": 20, "potato": 30,
                "tomato": 40, "onion": 20, "garlic": 30,
                "ginger": 40})
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-size: 16px; background: #f0f0f0; padding: 20px; border: 2px solid #ccc;")
        # 功能按钮
        self.btn_street = QPushButton("逛街")
        self.btn_bag = QPushButton("背包")
        self.btn_game = QPushButton("小游戏")
        self.btn_info = QPushButton("信息")
        self.btn_settings = QPushButton("设置")
        self.btn_card = QPushButton("单张卡牌")
        self.btn_rps = QPushButton("猜拳")
        self.btn_exit = QPushButton("退出")
        self.btn_chat = QPushButton("AI-chat")
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.info_label)
        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_street)
        btn_layout.addWidget(self.btn_bag)
        btn_layout.addWidget(self.btn_game)
        btn_layout.addWidget(self.btn_info)
        btn_layout.addWidget(self.btn_settings)
        btn_layout.addWidget(self.btn_card)
        btn_layout.addWidget(self.btn_rps)
        btn_layout.addWidget(self.btn_exit)
        btn_layout.addWidget(self.btn_chat)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)
        #连接信号与槽
        self.btn_street.clicked.connect(self.on_street)
        self.btn_bag.clicked.connect(self.on_bag)
        self.btn_game.clicked.connect(self.on_game)
        self.btn_info.clicked.connect(self.on_info)
        self.btn_settings.clicked.connect(self.on_settings)
        self.btn_card.clicked.connect(self.on_card)
        self.btn_rps.clicked.connect(self.on_rps)
        self.btn_exit.clicked.connect(self.on_exit)
        self.btn_chat.clicked.connect(self.on_chat)
        time=TimeManageAndStartNotice.now_time_1am_or_2pm()
        model = GUI.MODEL_WHITE
        if time == 1:
            self.setWindowTitle("🐉 宠物养成(白天)")
            model=GUI.MODEL_WHITE
        elif time == 2:
            self.setWindowTitle("🐉 宠物养成(黑夜)")
            self.info_label.setStyleSheet("background-color: #1e1e1e; color: #f0f0f0; padding: 20px; border: 2px solid #3a3a3a; border-radius: 10px;")
            model=GUI.MODEL_BLACK
        app.setStyleSheet(model)
        self.resize(700, 300)
        self.init_game()
        self.update_display()
    def update_display(self):
        """刷新主窗口的信息标签"""
        state = self.state
        state.load()
        text = f"👤 姓名: {state.name}\n"
        text += f"📅 天数: {state.day}\n"
        text += f"💰 金钱: {state.money}\n"
        text += f"🐾 宠物: {state.pet}  ❤️ 好感: {state.favor}\n"
        text += f"🎒 背包: {', '.join(state.backpack) if state.backpack else '空'}\n"
        self.info_label.setText(text)
        self.state.save()
    def init_game(self):
        self.state.load()
        self.OPEN_MP3=self.state.open_mp3   #不变open_mp3变量
        if self.state.name == "" and self.state.money == 0:
            self.state.name = GUI.input("name?", "", "enter", "欢迎")
            self.state.pet = GUI.input("pet?", "", "enter", "欢迎")
            self.state.day = 1
            self.state.favor = 0
            self.state.money = 0
            self.txt.add_save(CustomTxt.GAME_NUMBER)
            self.state.save()
        self.txt.add_save(CustomTxt.OPEN_GAME)
        self.music_on()
        GUI.input("\thello\n\t今天有什么好玩的吗?", "", "msg", "----")
    def music_on(self):
        if self.OPEN_MP3:
            check=Music.play_mp3_loop("file_date/.music_file.mp3")
            if check==CustomTxt.MUSIC_ERROR:
                self.txt.add_save(check,error=True)
        else:
            Music.play_random_music_loop()
    def music_close(self):
        if self.OPEN_MP3:
            Music.stop_mp3()
        else:
            Music.stop_random_music()
    def on_street(self):
        while True:
            choice = GUI.input("在街上:", GUI.STREET, "button", "街道")
            if choice == "back":
                break
            while True:
                self.shop.fresh_shing_sort()
                self.shop.fresh_shing_name(True)
                choice = GUI.input(f"路过1家店,菜单:{self.shop.shing_name}留下?", GUI.STREET_IN, "button", "街道")
                if choice == "no":
                    break
                elif choice == "next":
                    continue
                
                while True:
                    buy_choice = GUI.input(f"购买:{self.shop.shing_now}:", self.shop.shing_name, "button", "街道")
                    if buy_choice is None or buy_choice == "":
                        break
                    if buy_choice not in self.shop.shing_now:
                        GUI.input("输入菜单中的食物", "", "msg", "警告!警告!警告!")
                        continue
                    self.state.money, self.state.day, ok = Cal.buy(
                        self.state.money, self.state.day, 
                        self.shop.get_price(buy_choice)
                    )
                    if ok:
                        GUI.input(f"{buy_choice}已放至背包", "", "msg", "街道")
                        self.state.backpack.append(buy_choice)
                        self.txt.add_save(f"{CustomTxt.BUY} {buy_choice}")
                        self.state.backpack.sort()
                    else:
                        GUI.input("money不够", "", "msg", "街道")
                        
        self.update_display()
    def on_bag(self):
        while True:
            if not self.state.backpack:
                GUI.input("背包空空如也", "", "msg", "背包")
                break
            backpack_string = f"当前背包: {', '.join(self.state.backpack) if self.state.backpack else '空'}"
            choice = GUI.input(backpack_string, GUI.BAG, "button", "背包")
            if choice == "返回":
                break
            if choice == "eat":
                backpack_name = self.state.backpack.copy()
                eat_choice = GUI.input(f"eat:\n", backpack_name, "button", "背包")
                if eat_choice not in self.state.backpack:
                    GUI.input("输入背包中的thing", "", "msg", "警告!警告!警告!")
                    continue
                self.state.backpack.remove(eat_choice)
                self.state.favor += 1
                GUI.input(f"eat了{eat_choice}", "", "msg", "背包")
                self.txt.add_save(f"{CustomTxt.EAT} {eat_choice}")
        self.update_display()
    def on_game(self):
        
        self.state.money, self.state.day,add_money = Game.digital_bomb_run(
            self.state.money, self.state.day
        )
        self.txt.add_save(f"{CustomTxt.PLAY} digital_bomb {add_money}")
        self.update_display()
    def on_info(self):
        info_text = f"""\n\t  name:{self.state.name}    
                        \n\t  day:{self.state.day} 
                        \n\t  money:{self.state.money}  
                        \n\t  pet:{self.state.pet}({self.state.favor}好感)  
                        \n\t  背包:{self.state.backpack}  
                        \n\t  last time:{self.state.last_state}"""
        GUI.input(info_text, "", "msg", "信息")
    def on_settings(self):
        choice = GUI.input("\t\t\t使用愉快", GUI.SET_UP, "button", "设置")
        if choice == "公告":
            GUI.input("公告栏", CustomTxt.NOTICE, "text", "设置")
        elif choice == "Root":
            choice_root=GUI.input("是你想Root\n还是我想",["你","我(作者)","返回"],"button","Test")
            if choice_root=="我(作者)":
                GUI.input("不,我不想","","msg","失败")
            elif choice_root=="你":
                GUI.input("不,我看你不想","","msg","失败")
            elif choice_root=="返回":
                pass
            elif not choice_root:
                GUI.input("PASS\nPASS\nPASS","","msg","Pass")
                text=GUI.input("暗号","","enter","PASSWD")  
                if text in CustomTxt.ROOT:
                    terminal = RootTerminal(self,self.txt,self.state)
                    terminal.exec()
        elif choice == "Music设置":
            choice_music=GUI.input("是否使用mp3?","","yn","Music")
            if choice_music:
                self.state.open_mp3 = 1
            else:
                self.state.open_mp3 = 0
            self.txt.add_save(CustomTxt.SETTING_MUSIC)
        elif choice == "重置":
            confirm = GUI.input("是否重置", "", "yn", "!!!!!!!!!!!!!!!!")
            if confirm:
                self.txt.init_file()
                self.save_read.init_to_film()
                self.state.load()
                self.state.name = GUI.input("name?", "", "enter", "欢迎")
                self.state.pet = GUI.input("pet?", "", "enter", "欢迎")
                self.state.save()
                self.txt.add_save(CustomTxt.GAME_NUMBER)
                self.txt.add_save(CustomTxt.OPEN_GAME)
                GUI.input("\t已重置", "", "msg", "提示")
        elif choice == "AI设置":
            ai_chat_choice=GUI.input("\t要设置:",GUI.SET_UP_AI,"button","AI设置")
            ai_setting=AI()
            if ai_chat_choice=="NAME":
                name_new=GUI.input("\tAI宠物","","enter","new-AI-NAME")
                ai_setting.change_set(ai_setting.model,ai_setting.api_key,ai_setting.url,name_new)

            elif ai_chat_choice=="API-KEY":
                apikey_new=GUI.input("\tAI宠物","","enter","new-AI-APIKEY")
                ai_setting.change_set(ai_setting.model,apikey_new,ai_setting.url,ai_setting.name)

            elif ai_chat_choice=="URL":
                url_new=GUI.input("\tAI宠物","","enter","new-AI-URL")
                ai_setting.change_set(ai_setting.model,ai_setting.api_key,url_new,ai_setting.name)

            elif ai_chat_choice=="MODEL":
                model_new=GUI.input("\tAI宠物","","enter","new-AI-MODEL")
                ai_setting.change_set(model_new,ai_setting.api_key,ai_setting.url,ai_setting.name)

            if ai_chat_choice:
                self.txt.add_save(f"{CustomTxt.SETTING_AI} {ai_chat_choice}")
        elif choice == "日志查看":
            GUI.input(self.txt.read(),"","text","日志")
        self.update_display()
    def on_card(self):
        self.state.money, self.state.day,add_money = Game.card_run(
            self.state.money, self.state.day
        )
        self.txt.add_save(f"{CustomTxt.PLAY} card_game {add_money}")
        self.update_display()
    def on_rps(self):
        self.state.money, self.state.day ,add_money= Game.rock_paper_scissors_run(
            self.state.money, self.state.day
        )
        self.txt.add_save(f"{CustomTxt.PLAY} rock_paper_scissors {0+add_money}")
        self.update_display()
    def on_chat(self):
        self.state.save()
        check=Game.ai_chat_run()
        if check==CustomTxt.AI_OPENAI_ERROR:
            self.txt.add_save(CustomTxt.AI_OPENAI_ERROR,error=True)
    def on_exit(self):
        self.close()
    def closeEvent(self, event):
        self.state.last_state = TimeManageAndStartNotice.now_time()
        self.state.save()
        self.txt.add_save(CustomTxt.OVER_GAME)
        Music.stop_mp3()
        event.accept()
class RootTerminal(QDialog):        #Root终端模拟
    def __init__(self, parent=None, txt=None, state=None):
        super().__init__(parent)
        if txt is None or state is None:
            # 如果没有传入，则创建新的
            self.save_read = JsonSaveAndRead('file_date/.save.json', {"name": "", "day": 1, "money": 0, "pet":"", "time":"", "favor":0,"backpack":[],"open_mp3":1})
            self.txt = TxtSaveAndRead("file_date/date.txt")
            self.state = GameState(self.save_read)
        else:
            self.state = state
            self.txt = txt
        self.history = []           # 历史命令列表
        self.history_index = None   # 当前浏览位置
        self.current_input = ""     # 临时保存正在输入的内容
        self.setWindowTitle("Root-Terminal")
        self.resize(600, 400)
        self.setStyleSheet("background-color: #000000; color: #00ff00; font-family: 'Courier New'; font-size: 14px;")

        self.output_area = QPlainTextEdit()
        self.output_area.setStyleSheet("background-color: #0a0a0a; border: none;")
        self.output_area.installEventFilter(self)
        self.output_area.setUndoRedoEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.output_area)
        self.setLayout(layout)

        self.prompt = "Root-$:"
        self.output_area.insertPlainText("Root-Terminal:输入 'help' 查看可用命令\n")
        self.output_area.insertPlainText(self.prompt)
        self.prompt_pos = self.output_area.textCursor().position()  # 提示符之后的位置
        self.output_area.moveCursor(self.output_area.textCursor().End)
        self.output_area.setFocus()

    def eventFilter(self, obj, event):
        if obj == self.output_area:
            if event.type() == QKeyEvent.KeyPress:
                key = event.key()
                cursor = self.output_area.textCursor()
                pos = cursor.position()

                # 回车执行命令
                if key in (Qt.Key_Return, Qt.Key_Enter):
                    self.execute_current_line()
                    return True

                # 上箭头：显示历史命令
                if key == Qt.Key_Up:
                    self.handle_up_key()
                    return True

                # 下箭头：显示更新的历史命令
                if key == Qt.Key_Down:
                    self.handle_down_key()
                    return True

                # 其他限制（左箭头、退格等）保持不变
                if key == Qt.Key_Backspace:
                    if pos <= self.prompt_pos:
                        return True
                if key == Qt.Key_Delete:
                    if pos < self.prompt_pos:
                        return True
                if key == Qt.Key_Left:
                    if pos <= self.prompt_pos:
                        return True
                # 禁止 PageUp/PageDown/Home/End 等导致光标乱跳的键
                if key in (Qt.Key_PageUp, Qt.Key_PageDown, Qt.Key_Home, Qt.Key_End):
                    return True
                if event.modifiers() & Qt.ControlModifier:
                    return True

            # 鼠标点击：如果点击位置在提示符之前，强制光标回到提示符后
            if event.type() == QEvent.MouseButtonPress:
                mouse_cursor = self.output_area.cursorForPosition(event.pos())
                if mouse_cursor.position() < self.prompt_pos:
                    cursor = self.output_area.textCursor()
                    cursor.setPosition(self.prompt_pos)
                    self.output_area.setTextCursor(cursor)
                    return True

            return super().eventFilter(obj, event)

    def make_cursor_at_prompt(self):
        cursor = self.output_area.textCursor()
        cursor.setPosition(self.prompt_pos)
        return cursor

    def execute_current_line(self):
        cursor = self.output_area.textCursor()
        cursor.setPosition(self.prompt_pos)
        cursor.movePosition(cursor.EndOfBlock, cursor.KeepAnchor)
        cmd = cursor.selectedText().strip()

        cursor.clearSelection()
        cursor.movePosition(cursor.EndOfBlock)
        self.output_area.setTextCursor(cursor)

        self.output_area.insertPlainText("\n")

        if cmd:
            self.run_command(cmd)
            self.history.append(cmd)  # 加入历史

        # 重置浏览状态
        self.history_index = None
        self.current_input = ""

        self.output_area.insertPlainText(self.prompt)
        self.prompt_pos = self.output_area.textCursor().position()
        self.output_area.moveCursor(self.output_area.textCursor().End)
        self.state.load()
    def show_history_command(self, cmd):
        """把当前输入行替换成指定命令"""
        cursor = self.output_area.textCursor()
        cursor.setPosition(self.prompt_pos)
        cursor.movePosition(cursor.EndOfBlock, cursor.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText(cmd)
        cursor.movePosition(cursor.EndOfBlock)
        self.output_area.setTextCursor(cursor)
    def handle_up_key(self):
        """上箭头：显示更早的历史命令"""
        if not self.history:
            return
        if self.history_index is None:
            # 第一次按上箭头，保存当前输入
            cursor = self.output_area.textCursor()
            cursor.setPosition(self.prompt_pos)
            cursor.movePosition(cursor.EndOfBlock, cursor.KeepAnchor)
            self.current_input = cursor.selectedText()
            # 开始显示最后一条历史
            self.history_index = len(self.history) - 1
        else:
            # 继续往前翻
            if self.history_index > 0:
                self.history_index -= 1
            else:
                # 已经到最早命令，不再变化
                pass
        self.show_history_command(self.history[self.history_index])

    def handle_down_key(self):
        """下箭头：显示更新的历史命令或恢复当前输入"""
        if self.history_index is None:
            return
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.show_history_command(self.history[self.history_index])
        else:
            # 已经翻过最新命令，恢复之前保存的输入
            self.history_index = None
            self.show_history_command(self.current_input)
    def run_command(self,cmd): 
        if not cmd:
            self.output_area.appendPlainText("Root-$:")
            return None
        
        parts = cmd.split()
        command = parts[0].lower()
        self.state.load()
        args = parts[1:]
        
        if command == "exit":
            self.close()
        elif command == "help":
            self.output_area.appendPlainText("""可用命令:\t
            money <金额>    - 修改金钱\t
            favor <数值>    - 修改好感度\t
            pet-name <name> - 改宠物名\t
            name <name>     - 改玩家名\t
            day <day>       - 改天数\t
            date            - 查看及修改日志\t
            exit            - 退出终端\n""")
        elif command == "money":
            if args:
                try:
                    amount = int(args[0])
                    self.state.money = amount
                    self.state.save()
                    self.output_area.appendPlainText(f"金钱已修改为 {amount}.\n")
                except ValueError:
                    self.output_area.appendPlainText("错误:请输入整数金额.\n")
            else:
                self.output_area.appendPlainText(f"当前金钱:{self.state.money}\n")
        elif command == "favor":
            if args:
                try:
                    value = int(args[0])
                    self.state.favor = value
                    self.state.save()
                    self.output_area.appendPlainText(f"好感度已修改为 {value}.\n")
                except ValueError:
                    self.output_area.appendPlainText("错误:请输入整数.\n")
            else:
                self.output_area.appendPlainText(f"当前好感度:{self.state.favor}\n")
        elif command == "pet-name":
            if args:
                try:
                    amount = args[0]
                    self.state.pet = amount
                    self.state.save()
                    self.output_area.appendPlainText(f"宠物名已修改为 {amount}.\n")
                except ValueError:
                    self.output_area.appendPlainText("错误\n")
            else:
                self.output_area.appendPlainText(f"当前Pet-Name:{self.state.pet}\n")
        elif command == "name":
            if args:
                try:
                    amount = args[0]
                    self.state.name = amount
                    self.state.save()
                    self.output_area.appendPlainText(f"玩家名已修改为 {amount}.\n")
                except ValueError:
                    self.output_area.appendPlainText("错误\n")
            else:
                self.output_area.appendPlainText(f"当前Name:{self.state.name}\n")
        elif command == "day":
            if args:
                try:
                    value = int(args[0])
                    self.state.day= value
                    self.state.save()
                    self.output_area.appendPlainText(f"Day已修改为 {value}.\n")
                except ValueError:
                    self.output_area.appendPlainText("错误:请输入整数.\n")
            else:
                self.output_area.appendPlainText(f"当前Day:{self.state.day}\n") 
        elif command == "date":
            date_=GUI.input(self.txt.read(),"","text","DATE")
            self.txt.write(date_)
#---------------------RUN---------------------#
if __name__=="__main__":#                    |
    app = QApplication(argv_sys)#            |
    pet_window = PetWindow()#                |
    pet_window.show()#                       |
    app.exec_()#                             |
#---------------------OVER--------------------#
