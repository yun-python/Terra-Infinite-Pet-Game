try:                                #import导入依赖
    from sys import argv
    from PyQt5.QtWidgets import (
        QApplication, QWidget, QPushButton, 
        QVBoxLayout, QHBoxLayout,
        QLabel, QListWidget, QDialog, QMessageBox, 
        QInputDialog, QTextEdit,QPlainTextEdit)
    from PyQt5.QtCore import Qt,QEvent,QTimer
    from PyQt5.QtGui import QKeyEvent
    from json import load,dump,JSONDecodeError
    from time import gmtime
    from random import randint
    import pygame.mixer
    from pygame import error as mp3_error
    from openai import OpenAI,OpenAIError
    from datetime import date
    from pathlib import Path
    from math import sin, pi
    from array import array
except ImportError:                 #import失败处理
    print("你的环境可能不适配<<Error>>")
    input("输入任意字符退出(｡•́︿•̀｡):")
    exit()

class Cal:                          #operation  管理
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
class GUI:                          #GUI        管理
    DO=["逛街","小游戏","退出","背包","信息","设置","单张卡牌","猜拳"]
    STREET=["go","back"]
    STREET_IN=["yes", "no", "next"]
    SET_UP=["重置","日志查看","Terminal","返回", "AI设置", "Music设置", "公告"]
    SET_UP_AI=["API-KEY","URL","MODEL","NAME"]
    BAG=["eat", "返回"]
    GO_OUT=["向左","向前","向右","back"]
    MONEY_SHOP=["一键卖光","sell","buy","back"]
    MODEL_WHITE="""
        QWidget {
            background-color: #ffffff;
            color: #2c3e50;
            font-family: "Microsoft YaHei";
        }
        QLabel {
            color: #2c3e50;
            font-weight: bold;
        }
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
        QDialog {
            background-color: #ffffff;
        }
        QMessageBox {
            background-color: #ffffff;
        }"""
    MODEL_BLACK="""
        QWidget {
            background-color: #1e1e1e;
            color: #ffffff;
            font-family: "Microsoft YaHei";
        }
        QLabel {
            color: #f0f0f0;
            font-weight: bold;
        }
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
        QDialog {
            background-color: #1e1e1e;
        }
        QMessageBox {
            background-color: #1e1e1e;
        }
        QListWidget {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #3a3a3a;
            outline: none;
        }
        QListWidget::item {
            background-color: #1e1e1e;
            color: #ffffff;
            padding: 4px;
        }
        QListWidget::item:selected {
            background-color: #3a3a3a;
        }
        QTextEdit {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #3a3a3a;
        }
        QScrollArea {
            background-color: #1e1e1e;
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
    def _button_click(choice,  #button关闭
                    window_button,
                    result):
        result[0] = choice
        window_button.accept()

    @staticmethod
    def _text_close(window_text#大型text关闭
                    ):
        window_text.accept()

    @staticmethod
    def input(word="",    #GUI弹窗
                add_word_or_choice=None,
                model="msg",
                title="-----",
                integer_lower=0,
                integer_upper=100):
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
                btn_choice = QPushButton("选择")
                def on_select():
                    current = list_widget.currentItem()
                    if current:
                        result[0] = current.text() # type: ignore
                        dlg.accept()
                btn_choice.clicked.connect(on_select)
                layout.addWidget(btn_choice)
                
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
            input_return, check = QInputDialog.getText(parent_father, title, f"{word}{add_word_or_choice}")
            if not check:
                input_return=check
        elif model=="yn":
            input_return = QMessageBox.question(None, title, f"{word}{add_word_or_choice}", QMessageBox.Yes | QMessageBox.No)
            if input_return==QMessageBox.Yes:
                return True
            else:
                return False
        elif model=="integer":
            parent_father = QApplication.activeWindow()
            input_return, check = QInputDialog.getInt(parent_father, title, f"{word}{add_word_or_choice}", value=integer_lower, min=integer_lower, max=integer_upper)
            if not check:
                input_return=check
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
class GamePaths:                    #Path       管理
    FATHER_DIR="file_date"
    USER_PASH=f"{FATHER_DIR}/.save.json"
    PET_PATH=f"{FATHER_DIR}/.pet_date.json"
    AI_PATH=f"{FATHER_DIR}/.AI_date.json"
    TERMINAL_PATH=f"{FATHER_DIR}/.terminal.json"
    MUSIC_PATH=f"{FATHER_DIR}/.music_file.mp3"
    TXT_PATH=f"{FATHER_DIR}/date.txt"
class GameDict:                     #Dict       管理
    USER={"name": "", "day": 1, "money": 0, "pet":"", "time":"",
            "backpack":[],"open_mp3":1,"money_shop_backpack":[]}
    TERMINAL={"localhost":"localhost","password":"","root_next":0}
    AI={"NAME":"AI宠物","APIKEY":"","URL":"","MODEL":"","LAST":{}}
    PET={"favor":0,"hungry": 40,"hungry_feel":1,"emoji":"^&^"}
class ShopDict:                     #SHOPdict   管理
    FOOD_SHOP={"apple": 40, "banana": 30, "chicken": 70,
        "beef": 90, "pork": 80, "shrimp": 100,
        "tofu": 30, "noodle": 40, "pasta": 50,
        "cheese": 60, "yogurt": 40, "butter": 50,
        "jam": 30, "honey": 60, "oat": 30,
        "barley": 40, "quinoa": 70, "lentil": 40,
        "pea": 30,"carrot": 20, "potato": 30,
        "tomato": 40, "onion": 20, "garlic": 30,
        "ginger": 40
        }
    MONEY_SHOP={"broken_light":[30,50],
        "broken_car":[4000,6000],
        "broken_phone":[1000,2000],
        "broken_computer":[3000,5000],
        "broken_tv":[2000,4000],
        "broken_furniture":[100,300],
        }

class TimeManageAndStartNotice:     #Time       管理

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
        time_now = f"{y}-{mo}-{d}-{h}{m}:{mi}:{s}"
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
class Music:                        #Music      管理
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
        samples = int(sample_rate * duration)
        gap_samples = int(sample_rate * gap)
        wave = array("h", (
            int(32767 * sin(2 * pi * frequency * i / sample_rate))
            for i in range(samples)
        ))
        silence = array("h", [0]) * gap_samples
        wave.extend(silence)
        return wave

    @classmethod
    def play_random_music_loop(cls):
        cls._init_mixer()
        full_wave = array("h")
        for f in Music.freqs:
            full_wave.extend(cls.make_tone(f))
        cls._sound = pygame.mixer.Sound(buffer=full_wave.tobytes())
        cls._sound.play(-1)
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
class JsonSaveAndRead:              #json       管理
    def __init__(self,file_path,init_date):
        self.init_date=init_date
        self.path=Path(file_path)
        self.file_check()

    def file_check(self):#检查file存在
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            with open(self.path,"w", encoding="utf-8") as f:
                dump(self.init_date, f, ensure_ascii=False)
            return False
        
        try:
            with self.path.open("r+", encoding="utf-8") as file:
                file_try = load(file)
                if not isinstance(file_try, dict):
                    self.init_to_film()
            return True
        except (JSONDecodeError, ValueError, EOFError):
            self.init_to_film()
            return False


    def init_to_film(self):     #格式化
        with open(self.path,"r+",encoding="UTF-8") as file:
            file.seek(0)
            file.truncate(0)
            dump(self.init_date,file,ensure_ascii=False)

    def save_to_file(self, key, value):         #json值替换并存储
        with open(self.path,"r+",encoding="UTF-8") as file:
            filelist=load(file)
            filelist[key]=value
            file.seek(0)
            file.truncate(0)
            dump(filelist, file, ensure_ascii=False)

    def read_from_file(self, key):       #json读取对应值
        with open(self.path,"r+",encoding="UTF-8") as file:
            file.seek(0)
            save_file_list=load(file)
            if not save_file_list:
                self.init_to_film()
            return save_file_list.get(key,"")
class TxtSaveAndRead:               #txt        管理
    def __init__(self,file_path):
        self.path=Path(file_path)
        self.file_check()

    def file_check(self):#检查file正常/存在
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            with self.path.open("w", encoding="UTF-8") as f:
                pass
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
class CustomTxt:                    #text       管理
    NUMBER="V2.1.5-Stable"
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
    SELL="Sell"
    NOTICE=f"""版本:{NUMBER}\n公告:
            \t1.1.0完成框架 
            \t1.2.0补充丰富内容
            \t1.2.5修复了背包及食物购买页面退不出来的问题
            \t1.3.0新增在逛街及进食时增加好感
            \t1.3.5对公告及重置进行了优化
            \t1.4.0新增(优化)了食物购买页面持续购买的功能
            \t1.4.5卡牌脚本正式迁移pet game1.45
            \t1.5.0主程序用类改写
            \t1.6.0用Qt(PyQt)作为UI,并改写,替代旧UI
            \t\t新增页面的白天黑夜(不同时间启动不同颜色)
            \t1.6.5添加AI对话,5日记忆,三十轮对话
            \t1.7.0同时贴合Linux,Windows系统
            \t1.7.5使用树型文件结构,并推出随机音频背景音乐
            \t1.8.0加入日志功能
            \t1.8.5丰富日志功能
            \t1.9.0加入虚拟终端
            \t1.9.5加入记录宠物的文件
            \t2.0.0稳定及优化
            \t2.0.5修复一个没重视的Error
            \t2.1.0添加寻宝等Game
            \t2.1.5优化终端,购物等功能"""
class GameState:                    #Game       管理
    def __init__(self, save_read_handle,pet_date,terminal_json):
        if not isinstance(save_read_handle, JsonSaveAndRead):
            raise TypeError("Error")
        if not isinstance(pet_date, JsonSaveAndRead):
            raise TypeError("Error")
        if not isinstance(terminal_json, JsonSaveAndRead):
            raise TypeError("Error")
        self._storage = save_read_handle
        self.pet_date=pet_date  
        self.terminal_json=terminal_json

        self.last_state = None
        self.name = ""
        self.money = 0
        self.day = 0
        self.pet = ""
        self.backpack = []
        self.open_mp3 = 1
        self.money_shop_backpack=[]

        self.favor = 0
        self.hungry = 40
        self.hungry_feel = 1
        self.emoji = "^&^"

        self.password = ""
        self.localhost = "localhost"
        self.root_next = 0
    def save(self):
        #批量存储游戏状态
        self.backpack.sort()
        self._storage.save_to_file("day", self.day)
        self._storage.save_to_file("money", self.money)
        self._storage.save_to_file("name", self.name)
        self._storage.save_to_file("pet", self.pet)
        self._storage.save_to_file("time", self.last_state)
        self._storage.save_to_file("backpack", self.backpack)
        self._storage.save_to_file("open_mp3", self.open_mp3)
        self._storage.save_to_file("money_shop_backpack", self.money_shop_backpack)

        self.pet_date.save_to_file("favor", self.favor)
        self.pet_date.save_to_file("hungry",self.hungry)
        self.pet_date.save_to_file("hungry_feel",self.hungry_feel)
        self.pet_date.save_to_file("emoji",self.emoji)

        self.terminal_json.save_to_file("localhost", self.localhost)
        self.terminal_json.save_to_file("password", self.password)
        self.terminal_json.save_to_file("root_next", self.root_next)
    def load(self):
        #批量加载游戏状态
        try:
            self.name = self._storage.read_from_file("name") or ""
            self.day = self._storage.read_from_file("day") or 0
            self.money = self._storage.read_from_file("money") or 0
            self.pet = self._storage.read_from_file("pet") or ""
            self.last_state = self._storage.read_from_file("time") or ""
            self.backpack = self._storage.read_from_file("backpack") or []
            self.open_mp3 = self._storage.read_from_file("open_mp3") or 0
            self.money_shop_backpack = self._storage.read_from_file("money_shop_backpack") or []
            
            self.favor = self.pet_date.read_from_file("favor") or 0
            self.hungry_feel = self.pet_date.read_from_file("hungry_feel")
            self.hungry = self.pet_date.read_from_file("hungry") or 40
            self.emoji = self.pet_date.read_from_file("emoji") or "^&^"

            self.localhost = self.terminal_json.read_from_file("localhost") or "localhost"
            self.password = self.terminal_json.read_from_file("password") or ""
            self.root_next = self.terminal_json.read_from_file("root_next") or 0
            if self.hungry_feel not in (0, 1):
                self.hungry_feel = 1
        except (FileNotFoundError,PermissionError,AttributeError,OSError):
            self._storage.init_to_film()
            self.pet_date.init_to_film()
            self.terminal_json.init_to_film()

class Shop:                         #Shop       管理
    def __init__(self,model):
        self.shop=model
        self.shop_now={}
        self.shop_name=[]
        self.shop_price=[]
    def get_price(self,shop):
        shop_price=self.shop[shop]
        return shop_price
    def fresh_shop(self):
        self.shop_now={}
        for shop_key,shop_value in self.shop.items():
            probability=randint(0,10)
            if probability<5:
                self.shop_now[shop_key]=shop_value
        return None
    
    def fresh_shop_name(self,model=False):        #model决定name从shop/shop_now中获取
        self.shop_name=[]
        if model:
            for shop_name in self.shop_now.keys():
                self.shop_name.append(shop_name)
        else:
            for shop_name in self.shop.keys():
                self.shop_name.append(shop_name)
class HighShop(Shop):               #HighShop   管理
    def __init__(self, model):
        super().__init__(model)
    def shop_list(self):
        self.money_shop_now={}
        text=""
        price=0
        for shop_key,shop_value in self.shop.items():
            try:    
                price=self.average_price(shop_value)    
                text +=f"\t{shop_key}:{price}\n"
                self.money_shop_now[shop_key]=price
            except TypeError:
                return "Error"
        return text
    def random_shop(self):
        key_text=""
        self.fresh_shop_name()
        randint_number=randint(0,len(self.shop_name)-1)
        key_text=self.shop_name[randint_number]
        return key_text
    def average_price(self,list_price):
        try:       
            list_price.sort()
            max_price=max(list_price)
            small_price=list_price[0]
            price=randint(small_price,max_price)-1
            return price
        except (TypeError, ValueError):
            return False
    def get_shop_now_price(self, shop):
        if shop in self.money_shop_now:
            return self.money_shop_now[shop]
        else:
            return None
class Emoji:                        #emoji      管理
    SAD=["(；′⌒`)","(｡•́︿•̀｡)","(╥﹏╥)","(つ﹏⊂)"]
    HAPPY=["(◕‿◕✿)","(＾▽＾)","(◠‿◠)","(✿\"▽\")/"]
    NEUTRAL=["(-_-)" ,"(￣▽￣)ゞ"]
    EXCITED=["✧٩(ˊωˋ)و✧","(ﾉ◕ヮ◕)ﾉ:･ﾟ✧","ヽ(°▽°)ノ✿"]
    @staticmethod
    def emoji_random(model):
        index=randint(1,len(model))-1
        return model[index]

class SmallCardGame:                #最小卡牌单元类
    def __init__(self):
        self.play=[]
    def out(self, card_number):
        card_number = int(card_number)
        self.play.remove(card_number)        
        return True
    def have(self, number):
        self.play.sort()
        if number=={}:
            return None
        card_list=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]#11J 12Q 13K 14XW 15DW
        for sort_k,sort_v in number.items():
            if sort_v==0:
                card_list.remove(sort_k)
        random_over=randint(0,len(card_list)-1)
        v=card_list[random_over]
        number[v]-=1
        self.play.append(v)
        return number
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
    def is_big(self, number):     #是否Bigger than last(上家出的牌)
        if self.last>number or self.last==number:
            return False
        elif self.last<number:
            return True
        return False
    def my_card_format(self):     #为Input的ButtonBox做准备
        card_choice = []
        for out_card in self.playMY.play:
            ch = str(out_card)
            card_choice.append(ch)
        return card_choice
        #卡牌游戏类over
class CardGame:                     #完整卡牌系统类

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
class RockPaperScissors:            #完整猜拳系统类

        @staticmethod
        def run(money,day):
            add_money=0
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
class AI:                           #最小聊天单元类
    def __init__(self):
        self.AI_time = None
        self.AI_chat = None
        self.date=JsonSaveAndRead(GamePaths.AI_PATH,GameDict.AI)
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
                {"role": "system", "content": f"你是用户的好朋友,你叫{self.name},在和他聊天,上文:{list(self.last.keys())}"},
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
class AIChat:                       #完整聊天系统类
    def __init__(self):
        self._run=True
        self.ask="Hello"
        self.answer="< Hello >"
        self.AI_chat=AI()
        self.check=self.AI_chat.init()
        self.txt=TxtSaveAndRead(GamePaths.TXT_PATH)
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
class Game:                         #游戏类封装类

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

class PetWindow(QWidget):           #用户窗口
    def __init__(self):
        super().__init__()
        #创建对象
        self.date_json = JsonSaveAndRead(GamePaths.USER_PASH,GameDict.USER)#实例化文件管理
        self.pet_json = JsonSaveAndRead(GamePaths.PET_PATH,GameDict.PET)
        self.terminal_json = JsonSaveAndRead(GamePaths.TERMINAL_PATH,GameDict.TERMINAL)
        self.AI_json = JsonSaveAndRead(GamePaths.AI_PATH,GameDict.AI)
        self.txt = TxtSaveAndRead(GamePaths.TXT_PATH)
        self.state = GameState(self.date_json,self.pet_json,self.terminal_json)
        self.shop = Shop(ShopDict.FOOD_SHOP)
        self.money_shop = HighShop(ShopDict.MONEY_SHOP)
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
        self.btn_money_backpack=QPushButton("寻宝背包")
        self.btn_go_out=QPushButton("寻宝")
        self.btn_money_shop=QPushButton("冒险家商店")
        #宠物窗口刷新定时器
        self.hungry_timer = QTimer(self)
        self.hungry_timer.timeout.connect(self.update_display)
        self.hungry_timer.start(2000)
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
        btn_layout.addWidget(self.btn_money_backpack)
        btn_layout.addWidget(self.btn_go_out)
        btn_layout.addWidget(self.btn_money_shop)
        btn_layout.addWidget(self.btn_exit)
        btn_layout.addWidget(self.btn_chat)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)
        #连接信号与槽
        self.btn_street.clicked.connect(self.on_street)
        self.btn_bag.clicked.connect(self.on_backpack)
        self.btn_game.clicked.connect(self.on_game)
        self.btn_info.clicked.connect(self.on_info)
        self.btn_settings.clicked.connect(self.on_settings)
        self.btn_card.clicked.connect(self.on_card)
        self.btn_rps.clicked.connect(self.on_rps)
        self.btn_exit.clicked.connect(self.on_exit)
        self.btn_go_out.clicked.connect(self.on_go_out)
        self.btn_chat.clicked.connect(self.on_chat)
        self.btn_money_shop.clicked.connect(self.on_money_shop)
        self.btn_money_backpack.clicked.connect(self.on_money_backpack)
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
        self.state.save()
        self.state.load()
        self.hungry_cal()
        text = ""
        text += f"姓名: {self.state.name}\n"
        text += f"天数: {self.state.day}\n"
        text += f"金钱: {self.state.money}\n"
        text += f"宠物: {self.state.pet}\n"
        text += f"好感: {self.state.favor}\n"
        text += f"饥饿: {self.state.hungry}%\n"
        text += f"emoji:{self.state.emoji}\n"
        text += f"背包: {", ".join(self.state.backpack) if self.state.backpack else "空"}\n"
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
        GUI.input("\thello\n\t今天有什么好玩的吗?", "", "msg", CustomTxt.NUMBER)
    def music_on(self):
        if self.OPEN_MP3:
            check=Music.play_mp3_loop(GamePaths.MUSIC_PATH)
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
        running=True
        while running:
            self.shop.fresh_shop()
            self.shop.fresh_shop_name(True)
            choice = GUI.input(f"路过1家店,菜单:{self.shop.shop_name}留下?", GUI.STREET_IN, "button", "街道")
            if choice == "no" or not choice:
                running=False
                continue
            elif choice == "next":
                continue
            elif choice == "yes":
                running_buy=True
                while running_buy:
                    buy_choice = GUI.input(f"购买:{self.shop.shop_now}:", self.shop.shop_name, "button", "街道")
                    if not buy_choice:
                        running_buy=False
                        continue
                    elif buy_choice not in self.shop.shop_now:
                        GUI.input("输入菜单中的食物", "", "msg", "警告!警告!警告!")
                        continue
                    buy_number=GUI.input(f"购买个数:","","integer","NUMBER",integer_lower=1,integer_upper=50)
                    if not buy_number:
                        running_buy=False
                        continue
                    price=self.shop.get_price(buy_choice)
                    self.state.money, self.state.day, check = Cal.buy(
                        self.state.money, self.state.day, 
                        price*buy_number
                    )
                    if check:
                        GUI.input(f"{buy_number} {buy_choice}已放至背包", "", "msg", "街道")
                        for _ in range(0,buy_number):
                            self.state.backpack.append(buy_choice)
                        self.txt.add_save(f"{CustomTxt.BUY} {buy_number} {buy_choice}")
                        self.state.backpack.sort()
                    else:
                        GUI.input("money不够", "", "msg", "街道")
                    
        self.update_display()
    def on_backpack(self):
        while True:
            if not self.state.backpack:
                GUI.input("背包空空如也", "", "msg", "背包")
                break
            backpack_string = f"当前背包: {", ".join(self.state.backpack) if self.state.backpack else "空"}"
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
                self.state.hungry=self.state.hungry-35
                self.txt.add_save(f"{CustomTxt.EAT} {eat_choice}")
        self.update_display()
    def on_game(self):
        
        self.state.money, self.state.day,add_money = Game.digital_bomb_run(
            self.state.money, self.state.day
        )
        self.txt.add_save(f"{CustomTxt.PLAY} digital_bomb {add_money}")
        self.update_display()
    def on_info(self):
        info_text = ""
        info_text += f"姓名: {self.state.name}\n"
        info_text += f"天数: {self.state.day}\n"
        info_text += f"金钱: {self.state.money}\n"
        info_text += f"宠物: {self.state.pet}\n"
        info_text += f"好感: {self.state.favor}\n"
        info_text += f"背包: {", ".join(self.state.backpack) if self.state.backpack else "空"}\n"
        info_text += f"last time\t:\t{self.state.last_state}"
        GUI.input(info_text, "", "msg", "信息")
    def on_settings(self):
        choice = GUI.input("\t\t\t使用愉快", GUI.SET_UP, "button", "设置")
        if choice == "公告":
            GUI.input("公告栏", CustomTxt.NOTICE, "text", "设置")
        elif choice == "Terminal":
            terminal = Terminal(self,self.txt,self.state)
            terminal.exec_()
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
                self.date_json.init_to_film()
                self.pet_json.init_to_film()
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
    def hungry_cal(self):
        hungry_minus=0
        emoji_model=Emoji.HAPPY
        if self.state.hungry_feel:
            if 100-self.state.hungry >= 100:
                hungry_minus=3
                emoji_model=Emoji.EXCITED
            elif 100-self.state.hungry<=10:
                hungry_minus=0
                emoji_model=Emoji.SAD
            elif 100-self.state.hungry<=60:
                hungry_minus=1
                emoji_model=Emoji.NEUTRAL
            elif 100-self.state.hungry<=100:
                hungry_minus=2
                emoji_model=Emoji.HAPPY
        self.state.hungry=self.state.hungry+hungry_minus
        self.state.emoji=Emoji.emoji_random(emoji_model)
        return None
    def on_chat(self):
        self.state.save()
        check=Game.ai_chat_run()
        if check==CustomTxt.AI_OPENAI_ERROR:
            self.txt.add_save(CustomTxt.AI_OPENAI_ERROR,error=True)
    def on_go_out(self):
        running=True
        while running:
            choice=GUI.input("\t向",GUI.GO_OUT,"button","out-side")
            if choice=="back" or not choice:
                running=False
                continue
            if randint(1,3) < 2:
                text=self.money_shop.random_shop()
                GUI.input(f"A {text}","","msg","-")
                self.state.money_shop_backpack.append(text)
    def on_money_shop(self):
        running=True
        text=self.money_shop.shop_list()
        self.money_shop.fresh_shop_name()
        while running:
            choice=GUI.input(f"money:{self.state.money}\nmoney_backpack:{self.state.money_shop_backpack}",GUI.MONEY_SHOP,"button","money-shop")
            if choice=="buy":
                running_buy=True
                while running_buy:
                    buy_choice=GUI.input(f"money:{self.state.money}\nshop:\n{text}",self.money_shop.shop_name, "button", "money-shop")
                    if not buy_choice:
                        running_buy=False
                        continue
                    if buy_choice not in self.money_shop.shop_name:
                        GUI.input("输入shop中的东西", "", "msg", "警告!警告!警告!")
                        continue
                    self.state.money, self.state.day, check = Cal.buy(
                        self.state.money, self.state.day, 
                        self.money_shop.get_shop_now_price(buy_choice)
                    )
                    if check:
                        GUI.input(f"{buy_choice}已放至背包", "", "msg", "money-shop")
                        self.state.money_shop_backpack.append(buy_choice)
                        self.txt.add_save(f"{CustomTxt.BUY} {buy_choice}")
                        self.state.money_shop_backpack.sort()
                    else:
                        GUI.input("money不够", "", "msg", "money-shop")
            elif choice=="back" or not choice:
                running=False
                continue
            elif choice=="sell":
                if not self.state.money_shop_backpack:
                    GUI.input("money_backpack空空如也", "", "msg", "money-shop")
                    continue
                sell_choice=GUI.input(f"money_backpack:{self.state.money_shop_backpack}\n售价:\n{text}",self.state.money_shop_backpack, "button", "money-shop")
                if not sell_choice:
                    continue
                if sell_choice not in self.state.money_shop_backpack:
                    GUI.input("输入money_backpack中的东西", "", "msg", "警告!警告!警告!")
                    continue
                self.state.money, self.state.day = Cal.work(
                    self.state.money, self.state.day, 
                    self.money_shop.get_shop_now_price(sell_choice)
                )
                GUI.input(f"{sell_choice}已卖出", "", "msg", "money-shop")
                self.state.money_shop_backpack.remove(sell_choice)
                self.txt.add_save(f"{CustomTxt.SELL} {sell_choice}")
            elif choice=="一键卖光":
                if not self.state.money_shop_backpack:
                    GUI.input("money_backpack空空如也", "", "msg", "money-shop")
                    continue
                total_money=0
                for item in self.state.money_shop_backpack:
                    total_money=total_money+self.money_shop.get_shop_now_price(item)
                self.state.money, self.state.day = Cal.work(
                    self.state.money, self.state.day, 
                    total_money
                )
                GUI.input(f"一键卖光成功,总计:{total_money}元", "", "msg", "money-shop")
                self.txt.add_save(f"{CustomTxt.SELL} {total_money}")
                self.state.money_shop_backpack.clear()
        self.state.save()
    def on_money_backpack(self):
        if not self.state.money_shop_backpack:
            GUI.input("money_backpack空空如也", "", "msg", "money-shop")
            return
        backpack_string = f"money_backpack: {", ".join(self.state.money_shop_backpack) if self.state.money_shop_backpack else "空"}"
        choice = GUI.input(backpack_string, "", "msg", "money-backpack")
        if choice == "返回":
            return  
    def on_exit(self):
        self.close()
    def closeEvent(self, event):
        self.state.last_state = TimeManageAndStartNotice.now_time()
        self.state.save()
        self.txt.add_save(CustomTxt.OVER_GAME)
        Music.stop_mp3()
        event.accept()
class Terminal(QDialog):            #终端模拟
    def __init__(self, parent=None, txt=None, state=None):
        super().__init__(parent)
        if txt is None or state is None:
            self.save_read = JsonSaveAndRead(GamePaths.USER_PASH,GameDict.USER)
            self.terminal = JsonSaveAndRead(GamePaths.TERMINAL_PATH,GameDict.TERMINAL)
            self.pet = JsonSaveAndRead(GamePaths.PET_PATH,GameDict.PET)
            self.txt = TxtSaveAndRead(GamePaths.TXT_PATH)
            self.state = GameState(self.save_read,self.pet,self.terminal)
        else:
            self.state = state
            self.txt = txt
        self.root=0
        if self.state.root_next==1:
            self.root=1
        self.P1 = f"[User@Terminal]$:"
        self.update_P1()
        self.history = []
        self.history_index = None
        self.current_input = ""
        self.setWindowTitle(self.P1)
        self.resize(600, 400)
        self.setStyleSheet("background-color: #000000; color: #00ff00; font-family: \"Courier New\"; font-size: 14px;")

        self.output_area = QPlainTextEdit()
        self.output_area.setStyleSheet("background-color: #0a0a0a; border: none;")
        self.output_area.installEventFilter(self)
        self.output_area.setUndoRedoEnabled(False)
        layout = QVBoxLayout()
        layout.addWidget(self.output_area)
        self.setLayout(layout)
        self.output_area.insertPlainText(f"输入 \"help\" 查看可用命令\n")
        self.output_area.insertPlainText(self.P1)
        self.prompt_pos = self.output_area.textCursor().position()
        self.output_area.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.output_area.moveCursor(self.output_area.textCursor().End)
        self.output_area.setFocus()
    def eventFilter(self, obj, event):
        if obj == self.output_area:
            if event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonRelease,
                                QEvent.MouseButtonDblClick, QEvent.MouseMove):
                return True
            if event.type() == QEvent.Wheel:
                return True

        if obj == self.output_area:
            if event.type() == QKeyEvent.KeyPress:
                key = event.key()
                modifiers = event.modifiers()
                if key in (Qt.Key_Return, Qt.Key_Enter):
                    self.execute_current_line()
                    return True
                if key == Qt.Key_Up and modifiers == Qt.NoModifier:
                    self.handle_up_key()
                    return True
                if key == Qt.Key_Down and modifiers == Qt.NoModifier:
                    self.handle_down_key()
                    return True
                if modifiers & (Qt.ControlModifier | Qt.AltModifier | Qt.MetaModifier):
                    return True
                if key in (Qt.Key_PageUp, Qt.Key_PageDown, Qt.Key_Home, Qt.Key_End,
                           Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
                    cursor = self.output_area.textCursor()
                    pos = cursor.position()
                    if key == Qt.Key_Left and pos > self.prompt_pos:
                        return False
                    elif key == Qt.Key_Right and pos >= self.prompt_pos:
                        return False
                    else:return True
                if key == Qt.Key_Backspace:
                    cursor = self.output_area.textCursor()
                    if cursor.position() <= self.prompt_pos:
                        return True
                if key == Qt.Key_Delete:
                    cursor = self.output_area.textCursor()
                    if cursor.position() < self.prompt_pos:
                        return True
                return False
            if event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonDblClick,
                                QEvent.MouseButtonRelease, QEvent.MouseMove):
                if event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonDblClick):
                    mouse_cursor = self.output_area.cursorForPosition(event.pos())
                    if mouse_cursor.position() < self.prompt_pos:
                        cursor = self.output_area.textCursor()
                        cursor.setPosition(self.prompt_pos)
                        self.output_area.setTextCursor(cursor)
                        return True
                if event.type() == QEvent.MouseMove and event.buttons() & Qt.LeftButton:
                    cursor = self.output_area.textCursor()
                    if cursor.anchor() < self.prompt_pos or cursor.position() < self.prompt_pos:
                        cursor.clearSelection()
                        cursor.setPosition(max(cursor.position(), self.prompt_pos))
                        self.output_area.setTextCursor(cursor)
                        return False
                return False
            if event.type() == QEvent.ContextMenu:
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
            self.history.append(cmd)

        self.history_index = None
        self.current_input = ""

        self.output_area.insertPlainText(self.P1)
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
        if not self.history:
            return
        if self.history_index is None:
            
            cursor = self.output_area.textCursor()
            cursor.setPosition(self.prompt_pos)
            cursor.movePosition(cursor.EndOfBlock, cursor.KeepAnchor)
            self.current_input = cursor.selectedText()
            
            self.history_index = len(self.history) - 1
        else:
            
            if self.history_index > 0:
                self.history_index -= 1
            else:pass
        self.show_history_command(self.history[self.history_index])
    def handle_down_key(self):
        if self.history_index is None:
            return
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.show_history_command(self.history[self.history_index])
        else:
            self.history_index = None
            self.show_history_command(self.current_input)
    def run_command(self,cmd): 
        if not cmd:
            self.output_area.appendPlainText(self.P1)
            return None
        
        parts = cmd.split()
        command = parts[0].lower()
        self.state.load()
        args = parts[1:]
        
        if command == "exit":
            self.close()
        elif command == "help":
            root_text = """可用命令:\t
            money <number>    - 查看及修改金钱\t
            favor <number>    - 查看及修改好感度\t
            pet-name <name>   - 查看及修改宠物名\t
            name <name>       - 查看及修改玩家名\t
            day <day>         - 查看及修改天数\t
            date              - 查看及修改日志\t
            hungry <number>   - 修改或关闭饥饿\t
            info              - 查看当前状态\t
            su                - 变更身份\t
            password <str>    - 设置密码\t
            hostname <str>    - 设置主机名\t
            root              - 短暂永久Root\t
            exit              - 退出终端\n"""
            user_text = """可用命令:\t
            money             - 查看金钱\t
            favor             - 查看好感度\t
            pet-name          - 查看宠物名\t
            name              - 查看玩家名\t
            day               - 查看天数\t
            date              - 查看日志\t
            hungry            - 查看饥饿\t
            info              - 查看当前状态\t
            su                - 变更身份\t
            hostname          - 设置主机名\t
            exit              - 退出终端\n"""
            if self.is_root():
                text=root_text
            else:
                text=user_text
            self.output_area.appendPlainText(text)

        elif command == "money":
            if args:
                if self.is_root():
                    try:
                        amount = int(args[0])
                        self.state.money = amount
                        self.state.save()
                        self.output_area.appendPlainText(f"金钱已修改为 {amount}.\n")
                    except ValueError:
                        self.output_area.appendPlainText("错误:请输入整数金额.\n")
            else:
                self.output_area.appendPlainText(f"当前金钱:{self.state.money}\n")
        elif command == "hungry":
            if args:
                if self.is_root():
                    try:
                        amount = int(args[0])
                        self.state.hungry = amount
                        self.state.save()
                        self.output_area.appendPlainText(f"hungry已修改为 {amount}.\n")
                    except ValueError:
                        self.output_area.appendPlainText("错误:请输入整数.\n")
            else:
                if self.is_root():
                    if self.state.hungry_feel:
                        self.state.hungry_feel=0
                    else:
                        self.state.hungry_feel=1
                    self.state.save()
                    self.output_area.appendPlainText(f"已将饥饿设置成{self.state.hungry_feel}(1为开启,0为关闭)\n")
                else:
                    self.output_area.appendPlainText(f"当前hungry:{self.state.hungry}\n")
        elif command == "favor":
            if args:
                if self.is_root():
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
                if self.is_root():
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
                if self.is_root():
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
                if self.is_root():
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
            if self.is_root():
                self.txt.write(date_)
        elif command == "info":
            info_text = ""
            info_text += f"姓名: {self.state.name}\n"
            info_text += f"天数: {self.state.day}\n"
            info_text += f"金钱: {self.state.money}\n"
            info_text += f"宠物: {self.state.pet}\n"
            info_text += f"好感: {self.state.favor}\n"
            self.output_area.appendPlainText(info_text)
        elif command == "su":
            if args:
                if not self.is_root():
                    password = args[0]
                    if password == self.state.password:
                        self.root=1
                        self.update_P1()
                    else:
                        self.output_area.appendPlainText("密码错误\n")
            else:
                if self.is_root():
                    self.root=0
                    self.update_P1()
                elif not self.is_root():
                    if not self.state.password:
                        self.root=1
                        self.update_P1()
        elif command == "password":
            if args:
                if self.is_root():
                    password = args[0]
                    self.state.password = password
                    self.state.save()
                    self.output_area.appendPlainText("密码已设置\n")
            else:
                if self.is_root():
                    self.state.password = ""
                    self.state.save()
                    self.output_area.appendPlainText("密码已取消\n")
        elif command == "hostname":
            if args:
                hostname = args[0]
                self.state.localhost = hostname
                self.state.save()
                self.update_P1()
                self.output_area.appendPlainText(f"主机名已设置为 {hostname}\n")
            else:
                self.output_area.appendPlainText("请提供主机名参数\n")
        elif command == "root":
            if self.is_root():
                if self.state.root_next==0:
                    self.state.root_next=1
                    self.state.save()
                    self.output_area.appendPlainText("RootNext -I\n")
                elif self.state.root_next==1:
                    self.state.root_next=0
                    self.state.save()
                    self.output_area.appendPlainText("RootNext -O\n")
            else:
                pass

    def update_P1(self):
        if self.is_root():
            self.P1=f"[root@{self.state.localhost}]$ "
        else:
            self.P1=f"[{self.state.name}@{self.state.localhost}]# "
        self.setWindowTitle(self.P1)
    def is_root(self):
        if self.root:
            return True
        else:
            return False
if __name__=="__main__":            #正式运行
    app = QApplication(argv)
    pet_window = PetWindow()
    pet_window.show()
    app.exec_()
#OVER--OVER--OVER#