try:                                #import     ok
    from sys import argv
    from PyQt5.QtWidgets import (
        QApplication, QWidget, QPushButton, 
        QVBoxLayout, QHBoxLayout,
        QLabel, QListWidget, QDialog, QMessageBox, 
        QInputDialog, QTextEdit,QPlainTextEdit,)
    from PyQt5.QtCore import Qt,QEvent,QTimer,QPoint,QEasingCurve,QPropertyAnimation
    from PyQt5.QtGui import QKeyEvent,QPixmap
    from json import load,dump,JSONDecodeError
    from collections import Counter
    from time import gmtime
    from random import randint
    import pygame.mixer
    from pygame import error as mp3_error
    from openai import OpenAI,OpenAIError
    from datetime import date
    from pathlib import Path
    from math import sin, pi
    from array import array
    from webbrowser import open_new_tab
except ImportError:                 #import     error
    print("Your environment may not be compatible <<Error>>")
    input("Enter any key to exit (｡•́︿•̀｡): ")
    exit()

class Cal:                          #Operation  manager
    @staticmethod
    def buy(money, day, price):
        if money>=price:
            money=money-price
            day=day+0.5
            return money,day,True
        return money,day,False
    @staticmethod
    def work(money,day,work_money):
        money=money+work_money
        day=day+0.5
        return money,day
    @staticmethod
    def dict_text(dict_: dict = None):
        if dict_ is None:
            dict_ = {}
        text = ""
        try:
            for key, value in dict_.items():
                if value and key:
                    text += f"{key}*{value}."
        except (ValueError, AttributeError):
            pass
        if not text:
            text = "empty"
        return text
    @staticmethod
    def _is_empty(backpack: dict) -> bool:
        return not any(v > 0 for v in backpack.values())
    @staticmethod
    def list_text(list_use:list,slow=False):
        if not slow:
            if not list_use:
                return "empty", None

            counter = Counter(list_use)
            text = "".join(f"{item}*{count} . " for item, count in counter.items())
            return text, dict(counter)
        if slow: 
            copy_list=list_use.copy()
            if not copy_list:
                return "empty",None
            text=""
            copy_list_set=list(set(copy_list))
            list_set_dict={}
            number_help_dict=0
            for thing in copy_list_set:
                number_help_dict=0
                for thing_two in copy_list:
                    if thing==thing_two:
                        number_help_dict=number_help_dict+1
                list_set_dict[thing]=number_help_dict
                text += f"{thing}*{list_set_dict[thing]} . "
            return text,list_set_dict
class Translate:                    #Translate  manager
    _COMMON = {
        "Rock": "石头", "Paper": "布", "Scissors": "剪刀",
        "Exit": "退出", "Play Card": "出牌", "Pass": "过",
        "Backpack": "背包", "Money": "金钱","empty":"空","is":"是",
        "CHINESE": "中文",
        "ENGLISH": "英文",
        "AI Say:": "AI说:",
        "Time zone":"时区",
        "Time Zone":"时区",
        "Auto":"自动",
        "Light":"浅色",
        "Dark":"深色",
        "Theme":"主题",
    }

    _FOOD = {
        "apple": "苹果", "banana": "香蕉", "chicken": "鸡肉",
        "beef": "牛肉", "pork": "猪肉", "shrimp": "虾",
        "tofu": "豆腐", "noodle": "面条", "pasta": "意大利面",
        "cheese": "奶酪", "yogurt": "酸奶", "butter": "黄油",
        "jam": "果酱", "honey": "蜂蜜", "oat": "燕麦",
        "barley": "大麦", "quinoa": "藜麦", "lentil": "扁豆",
        "pea": "豌豆", "carrot": "胡萝卜", "potato": "土豆",
        "tomato": "番茄", "onion": "洋葱", "garlic": "大蒜",
        "ginger": "姜",
    }
    _HUNT = {
        "broken_light": "破灯", "broken_car": "破车",
        "broken_phone": "破手机", "broken_computer": "破电脑",
        "broken_tv": "破电视", "broken_furniture": "破家具",
    }
    DICT_GUI = {
        **_COMMON,
        **_FOOD,
        **_HUNT,
        "Go": "走", "Back": "返回", "Yes": "是", "No": "否", "Next": "下一个",
        "Reset": "重置", "View Log": "日志查看", "AI Settings": "AI设置",
        "AI Memory Management": "AI记忆管理", "Show/Hide Pet": "显示/隐藏宠物",
        "Music Settings": "音乐设置", "Announcement": "公告",
        "Terminal": "终端", "Visit Github": "访问仓库",
        "Eat": "吃", "Sell All": "一键卖光", "Sell": "卖", "Buy": "买",
        "Turn left": "向左", "Forward": "向前", "Turn right": "向右",
        "Street": "街道", "Backpack": "背包", "Number Bomb": "数字炸弹",
        "Settings": "设置", "Single Card": "单张卡牌",
        "Rock-Paper-Scissors": "猜拳", "Exit": "退出", "AI Chat": "AI聊天",
        "Treasure Hunt": "寻宝", "Hunt Shop": "冒险家商店",
        "MP3": "外部MP3", "Random Music": "随机音频", "None": "不用",
        "SeeMore": "查看更多", "Languages": "语言"
    }
    DICT_TEXT = {
        **_COMMON,
        **_FOOD,
        **_HUNT,
        "Non-critical error" : "不影响使用的错误",
        "Audio error" : "音频错误,未找到音频",
        "Passing by a shop,menu:": "路过一家店,菜单:",
        "Stay?": "留下？",
        "Buy": "购买",
        "SeeMore": "查看更多",
        "Buy quantity:": "购买个数:",
        "Eat quantity": "食用个数",
        "Eat:": "食用:",
        "Money not enough": "金钱不足",
        "Backpack is empty": "背包空空如也",
        "Name?": "名字?",
        "PetName?": "宠物名?",
        "Hello": "你好",
        "Anything fun today?": "今天有什么好玩的吗?",
        "Reset!": "确定重置?",
        "Reset complete": "已重置",
        "Welcome": "欢迎",
        "Enjoy": "使用愉快",
        "Set:": "设置:",
        "Use?": "使用?",
        "Visit Github?": "访问Github?",
        "Chat": "聊天",
        "AI is not configured yet": "AI尚未配置成功",
        "Network request failed": "网络请求失败",
        "You Play:": "你出:",
        "AI Rock-Paper-Scissors": "AI猜拳",
        "You win": "你赢了",
        "AI win": "AI赢了",
        "It is a draw": "平局",
        "Got ": "得到 ",
        "Lost ": "失去 ",
        "Bomb": "炸弹",
        "Bomb is ": "炸弹是 ",
        "Card Game": "卡牌对战",
        "Over": "结束",
        "Win": "胜利",
        "Money": "金钱",
        "Hunt-Shop": "冒险家商店",
        "Street": "街道",
        "Backpack": "背包",
        "Exit": "退出",
        "Play Card": "出牌",
        "Pass": "过",
        "Setting": "设置",
        "Announcement": "公告",
        "Log": "日志",
        "Error": "错误",
        "AI Pet": "AI宠物",
        "Game": "游戏",
        "Go:": "方向:",
        "SET": "设置",
        "Set": "设置",
        "Del": "删除",
        "Day": "天数",
        "Name": "名字",
        "Pet": "宠物",
        "Emoji": "表情",
        "Hungry": "饥饿",
        "Money": "金钱",
        "money": "金钱",
        "Favor": "感情",
        "Backpack": "背包",
        "Hunt": "寻宝",
        "Shop": "商店",
    }
    DICT_TEXT_CONVERT_SYMBOLS={
        "{":" ",
        "}":" ",
        "\"":" ",
        "\'":" ",
        "[":" ",
        "]":" ",
        }
    @staticmethod
    def translate_GUI(text, english=True):
        if not english:
            return Translate.DICT_GUI.get(text, text)
        return text
    @staticmethod
    def reverse(display, choices):
        for key in choices:
            if Translate.translate_GUI(str(key), english=False) == display:
                return key
        return display
    @staticmethod
    def text(s, english=True):
        if not isinstance(s, str):
            return s
        content = s

        for symbol, replacement in Translate.DICT_TEXT_CONVERT_SYMBOLS.items():
            content = content.replace(symbol, replacement)
        if english:
            return content
        replacements = sorted(
            Translate.DICT_TEXT.items(),
            key=lambda pair: len(pair[0]),
            reverse=True
        )
        for english_word, chinese_word in replacements:
            content = content.replace(english_word, chinese_word)

        return content
class GUI:                          #GUI        manager
    USE_EN=True

    YES = "Yes"
    NO = "No"
    NEXT = "Next"
    BACK = "Back"
    GO = "Go"

    RESET = "Reset"
    VIEW_LOG = "View Log"
    AI_SETTINGS = "AI Settings"
    AI_MEMORY = "AI Memory Management"
    SHOW_HIDE_PET = "Show/Hide Pet"
    MUSIC_SETTINGS = "Music Settings"
    ANNOUNCEMENT = "Announcement"
    TERMINAL = "Terminal"
    VISIT_GITHUB = "Visit Github"
    TIMEZONE = "Time Zone"

    API_KEY = "API-KEY"
    URL = "URL"
    MODEL = "MODEL"
    NAME = "NAME"

    EAT = "Eat"

    TURN_LEFT = "Turn left"
    FORWARD = "Forward"
    TURN_RIGHT = "Turn right"

    SELL_ALL = "Sell All"
    SELL = "Sell"
    BUY = "Buy"

    EXIT="Exit"

    PLAY_CARD="Play Card"
    PASS="Pass"
    ROCK="Rock"
    PAPER="Paper"
    SCISSORS="Scissors"

    NONE="None"
    RANDOM_MUSIC="Random Music"
    MP3="MP3"
    MUSIC_SETTINGS="Music Settings"
    LANGUAGES="Languages"
    CHINESE="CHINESE"
    ENGLISH="ENGLISH"

    SEE_MORE="SeeMore"

    HELP="Help"
    MONEY="Money"
    HUNGRY="Hungry"
    FAVOR="Favor"
    PET_NAME="Pet-name"
    DAY="Day"
    DATE="Date"
    INFO="Info"
    SU="Su"
    PASSWORD="Password"
    HOSTNAME="Hostname"
    ROOT_NEXT="Root-next"
    THEME="Theme"
    DARK="Dark"
    LIGHT="Light"
    AUTO="Auto"


    STREET      = [GO, BACK]
    STREET_IN   = [YES, NO, NEXT]
    SET_UP      = [
        SHOW_HIDE_PET,ANNOUNCEMENT,TERMINAL,THEME,
        LANGUAGES,TIMEZONE,MUSIC_SETTINGS,SEE_MORE,BACK]
    SET_UP_AI   = [API_KEY, URL, MODEL, NAME]
    SET_UP_THEME= [LIGHT,DARK,AUTO]
    BAG         = [EAT, BACK]
    GO_OUT      = [TURN_LEFT, FORWARD, TURN_RIGHT, BACK]
    MONEY_SHOP  = [SELL_ALL, SELL, BUY, BACK]
    SET_UP_MUSIC= [MP3,RANDOM_MUSIC,NONE]
    SET_UP_LANGUAGES=[CHINESE,ENGLISH]
    SET_UP_MORE=[RESET,AI_SETTINGS,
                 VISIT_GITHUB,VIEW_LOG,AI_MEMORY,
                 BACK]

    MODEL_LIGHT_LABEL = """
        QLabel#infoLabel {
            font-size: 16px;
            background: #f0f0f0;
            color: #000;
            padding: 20px;
            border: 2px solid #ccc;}
        """

    MODEL_DARK_LABEL = """
        QLabel#infoLabel {
            font-size: 16px;
            background: #252525;
            color: #f0f0f0;
            padding: 20px;
            border: 2px solid #3a3a3a;}
        """

    MODEL_LIGHT="""
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

    MODEL_DARK="""
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
    def set_USE_EN(english: bool):
        GUI.USE_EN = english

    @staticmethod
    def _button_click(choice,  #Button close
                    window_button,
                    result):
        result[0] = choice
        window_button.accept()

    @staticmethod
    def _text_close(window_text#Big text close
                    ):
        window_text.accept()

    @staticmethod
    def input(word="", add_word_or_choice=None, model="msg", title="-----",
              integer_lower:int=0, integer_upper:int=100, integer_start=None,english=None):
        if english is None:
            english = GUI.USE_EN
        if not add_word_or_choice is list:
            add_word_or_choice = Translate.text(add_word_or_choice,english)
        word  = Translate.text(word, english)
        title = Translate.text(title, english)
        input_return = False

        if model == "msg":
            input_return = QMessageBox.information(None, title, f"{word}{add_word_or_choice}")

        elif model == "button":
            if not add_word_or_choice:
                return None

            if len(add_word_or_choice) > 13:
                dlg = QDialog()
                dlg.setWindowTitle(title)
                layout = QVBoxLayout()
                layout.addWidget(QLabel(word))

                list_widget = QListWidget()
                for item in add_word_or_choice:
                    list_widget.addItem(Translate.translate_GUI(str(item), english))

                layout.addWidget(list_widget)
                result = [None]

                def on_select():
                    current = list_widget.currentItem()
                    if current:
                        display = current.text()
                        key = Translate.reverse(display, add_word_or_choice) \
                              if not english else display
                        result[0] = key
                        dlg.accept()

                btn_choice = QPushButton(Translate.translate_GUI("O-K", english))
                btn_choice.clicked.connect(on_select)
                layout.addWidget(btn_choice)

                dlg.setLayout(layout)
                dlg.resize(250, 300)
                dlg.exec_()
                return result[0]

            else:
                window = QDialog()
                window.setWindowTitle(title)
                layout = QVBoxLayout()
                layout.addWidget(QLabel(word))
                result = [None]

                for choice in add_word_or_choice:
                    display = Translate.translate_GUI(choice, english)
                    btn = QPushButton(display)
                    btn.clicked.connect(
                        lambda checked, ch=choice: GUI._button_click(ch, window, result)
                    )
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
            if integer_start==None:
                integer_start=integer_lower
            input_return, check = QInputDialog.getInt(parent_father, title, f"{word}{add_word_or_choice}",
                                value=integer_start, min=integer_lower, max=integer_upper)
            if not check:
                input_return=check
            input_return=int(input_return)
        elif model=="text":
            dlg = QDialog()
            dlg.setWindowTitle(title)

            layout = QVBoxLayout()
            text_edit = QTextEdit()
            text_edit.setPlainText(f"{word}{add_word_or_choice}")
            layout.addWidget(text_edit)

            btn_close = QPushButton("Close")
            btn_close.clicked.connect(lambda: GUI._text_close(dlg))
            layout.addWidget(btn_close)
            dlg.setLayout(layout)
            dlg.resize(600, 300)
            dlg.exec_()
            input_return=text_edit.toPlainText()
        return input_return
class GamePaths:                    #Path       manager
    FATHER_DIR="file_date"
    USER_PASH=f"{FATHER_DIR}/.save.json"
    PET_PATH=f"{FATHER_DIR}/.pet_date.json"
    AI_PATH=f"{FATHER_DIR}/.AI_date.json"
    TERMINAL_PATH=f"{FATHER_DIR}/.terminal.json"
    SETTINGS_PATH=f"{FATHER_DIR}/.settings.json"
    MUSIC_PATH=f"{FATHER_DIR}/music.mp3"
    PET_PNG_PATH=f"{FATHER_DIR}/pet.png"
    TXT_PATH=f"{FATHER_DIR}/date.txt"
class GameDict:                     #Dict       manager
    BACKPACK_INIT={
        "apple": 0, "banana": 0, "chicken": 0,
        "beef": 0, "pork": 0, "shrimp": 0,
        "tofu": 0, "noodle": 0, "pasta": 0,
        "cheese": 0, "yogurt": 0, "butter": 0,
        "jam": 0, "honey": 0, "oat": 0,
        "barley": 0, "quinoa": 0, "lentil": 0,
        "pea": 0, "carrot": 0, "potato": 0,
        "tomato": 0, "onion": 0, "garlic": 0,
        "ginger": 0
        }
    HUNT_SHOP = {
        "broken_light": 0,
        "broken_car": 0,
        "broken_phone": 0,
        "broken_computer": 0,
        "broken_tv": 0,
        "broken_furniture": 0,
        }
    USER={"name": "", "day": 1, "money": 0, "pet":"",
            "backpack":BACKPACK_INIT.copy(),"hunt_shop_backpack":HUNT_SHOP.copy()}
    TERMINAL={"localhost":"localhost","password":"","root_next":0}
    AI={"NAME":"AI Pet","APIKEY":"","URL":"","MODEL":"","LAST":{}}
    PET={"favor":0,"hungry": 40,"hungry_feel":1,"emoji":"^&^"}
    SETTINGS={"open_mp3":1,"english":1,"time":"","add_time":0,"theme":"Auto"}
class ShopDict:                     #ShopDict   manager
    FOOD_SHOP={"apple": 40, "banana": 50, "chicken": 70,
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

class TimeCal:                      #Time       manager
    @staticmethod
    def time_zone_cal_patch(hour:int,day:int,add_time:int):
        hour=hour+add_time
        if hour > 24:
            hour=hour-24
            day=day+1
        elif hour < 0:
            hour=hour+24
            day=day-1
        if hour > 12:
            am_or_pm="pm"
        else:
            am_or_pm="am"
        return hour,day,am_or_pm
    @staticmethod
    def now_time(add_time=0):  # time
        time_now_is = gmtime()
        year = time_now_is[0]
        month = time_now_is[1]
        day = time_now_is[2]
        hour = time_now_is[3]
        minute = time_now_is[4]
        second = time_now_is[5]
        hour,day,am_or_pm=TimeCal.time_zone_cal_patch(hour,day,add_time)
        time_now = f"{year}-{month}-{day}-{hour}{am_or_pm}:{minute}:{second}"
        return time_now

    @staticmethod
    def now_time_1am_or_2pm(add_time=0):
        time_now_is = gmtime()
        hour = time_now_is[3]
        hour,day,am_or_pm=TimeCal.time_zone_cal_patch(hour,0,add_time)
        if am_or_pm=="am":
            am_or_pm=1
        if am_or_pm=="pm":
            am_or_pm=2
        return am_or_pm

    @staticmethod
    def get_year_to_day():
        time_now_is = gmtime() 
        year = time_now_is[0]
        month = time_now_is[1] 
        day = time_now_is[2]
        return {"year":year,"month":month,"day":day}

    @staticmethod
    def time_to_now_gap(time):
        time_now=TimeCal.get_year_to_day()
        date1 = date(time["year"], time["month"], time["day"])
        date2 = date(time_now["year"], time_now["month"], time_now["day"])
        gap = date2 - date1
        return abs(gap.days)
class Music:                        #Music      manager
    freqs = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]
    _sound = None
    _initialized = False
    _mp3_music=False
    _random_music=False
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
        cls._random_music=True
    @classmethod
    def stop_random_music(cls):
        if cls._sound:
            cls._sound.stop()
            cls._sound = None
            Music._initialized = False
            pygame.quit()

    @classmethod
    def play_mp3_loop(cls,filepath):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(filepath) 
            pygame.mixer.music.play(-1)
            cls._mp3_music=True
        except mp3_error:
            GUI.input(CustomTxt.MP3_ERROR, "", "msg", "Error")
            return CustomTxt.MUSIC_ERROR

    @classmethod
    def stop_mp3(cls):
        try:
            cls._sound = None
            Music._initialized = False
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except mp3_error:
            pass
    @classmethod
    def easy_stop(cls):
        if cls._mp3_music:
            cls.stop_mp3()
        elif cls._random_music:
            cls.stop_random_music()
class JsonSaveAndRead:              #json       manager
    def __init__(self,file_path,init_date):
        self.init_date=init_date
        self.path=Path(file_path)
        self.file_check()

    def file_check(self):#Check file
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


    def init_to_film(self):     #Format file
        with open(self.path,"r+",encoding="UTF-8") as file:
            file.seek(0)
            file.truncate(0)
            dump(self.init_date,file,ensure_ascii=False)

    def save_to_file(self, key, value):  #Json value save
        with open(self.path,"r+",encoding="UTF-8") as file:
            filelist=load(file)
            filelist[key]=value
            file.seek(0)
            file.truncate(0)
            dump(filelist, file, ensure_ascii=False)

    def read_from_file(self, key):       #Json value load
        with open(self.path,"r+",encoding="UTF-8") as file:
            file.seek(0)
            save_file_list=load(file)
            if not save_file_list:
                self.init_to_film()
            return save_file_list.get(key,"")


    def update(self, **kwargs):         #Json value batch save
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = load(f)
        except (FileNotFoundError, JSONDecodeError):
            data = self.init_date.copy()
        data.update(kwargs)
        with open(self.path, "w", encoding="utf-8") as f:
            dump(data, f, ensure_ascii=False)

    def read_all(self):                 #Json value batch load
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = load(f)
            if not isinstance(data, dict):
                return self.init_date.copy()
            return data
        except (FileNotFoundError, JSONDecodeError, ValueError, EOFError):
            return self.init_date.copy()
class TxtSaveAndRead:               #txt        manager
    def __init__(self,file_path):
        self.path=Path(file_path)
        self.file_check()

    def file_check(self):#Check file
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            with self.path.open("w", encoding="UTF-8") as f:
                pass
            return None

    def read(self):
        with open(self.path,"r+",encoding="UTF-8") as file:
            file.seek(0)
            return file.read()

    def add_save(self,add_word,error=False,add_time:int=0):
        with open(self.path,"a+",encoding="UTF-8") as file:
            word=f"<{TimeCal.now_time(add_time)}>\t<{add_word}>\n"
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
class CustomTxt:                    #text       manager
    VERSION="V2.3.5-Stable"
    GAME_NAME_SUFFIX="Infinite"
    GAME_NAME_PREFIX="Terra"
    GAME_NAME_SIMPLE=f"{GAME_NAME_PREFIX}-{GAME_NAME_SUFFIX}"
    GAME_NAME_ALL=f"{GAME_NAME_PREFIX}-{GAME_NAME_SUFFIX}-{VERSION}"
    TITLE_SOL=f"{GAME_NAME_SIMPLE}-Sol"
    TITLE_LUNA=f"{GAME_NAME_SIMPLE}-Luna"
    COPYRIGHT_BOOK="GPL-V3"
    URL="https://github.com/yun-python/Terra-Infinite-Pet-Game"
    UPDATE = (
        "V<-1.1.0->Completed the basic framework\n"
        "V<-1.2.0->Added rich content\n"
        "V<-1.2.5->Fixed the issue where the backpack\n"
        "\tfood purchase page could not be exited\n"
        "V<-1.3.0->Added favor increase when shopping and eating\n"
        "V<-1.3.5->Optimized announcements and reset\n"
        "V<-1.4.0->Added continuous purchase function on the food purchase page\n"
        "V<-1.4.5->Card script officially migrated to pet game 1.45\n"
        "V<-1.5.0->Main program rewritten using classes\n"
        "V<-1.6.0->Rewrote UI using Qt (PyQt), replacing the old UI\n"
        "\tAdded day/night mode for pages (different colors at different startup times)\n"
        "V<-1.6.5->Added AI dialogue, 5-day memory, 30 rounds of dialogue\n"
        "V<-1.7.0->Compatible with both Linux and Windows systems\n"
        "V<-1.7.5->Used tree file structure\n"
        "\tAnd introduced random audio background music\n"
        "V<-1.8.0->Added logging feature\n"
        "V<-1.8.5->Enhanced logging feature\n"
        "V<-1.9.0->Added virtual terminal\n"
        "V<-1.9.5->Added file for recording pet data\n"
        "V<-2.0.0->Stability and optimization\n"
        "V<-2.0.5->Fixed an overlooked error\n"
        "V<-2.1.0->Added treasure hunting and other games\n"
        "V<-2.1.5->Optimized terminal, shopping and other features\n"
        "V<-2.2.0->Minor optimization of common features\n"
        "\tOfficially renamed to Terra-Infinite\n"
        "\tTerminal renamed to STL (Sol-Terra-Luna)\n"
        "V<-2.2.5->Added randomly wandering pet\n"
        "\tDouble-click to hide/show main window\n"
        "\tDraggable\n"
        "V<-2.3.0->English-localized game\n"
        "\tAnd Add 2 languages (Chinese and English)\n"
        "V<-2.3.5->Improved Chinese localization and custom time zones\n"
        "\tTheme can be adjusted manually/automatically\n"
        "\tOptimized list display format"
    )
    UPDATE_CHINESE = (
        "V<-1.1.0->完成基本框架\n"
        "V<-1.2.0->添加丰富内容\n"
        "V<-1.2.5->修复了背包及\n"
        "\t食物购买页面退不出来的问题\n"
        "V<-1.3.0->新增在逛街及进食时增加好感\n"
        "V<-1.3.5->对公告及重置进行了优化\n"
        "V<-1.4.0->新增(优化)了食物购买页面持续购买的功能\n"
        "V<-1.4.5->卡牌脚本正式迁移pet_game1.45\n"
        "V<-1.5.0->主程序用类改写\n"
        "V<-1.6.0->用Qt(PyQt)作为UI,并改写,替代旧UI\n"
        "\t新增页面的白天黑夜(不同时间启动不同颜色)\n"
        "V<-1.6.5->添加AI对话,5日记忆,三十轮对话\n"
        "V<-1.7.0->同时贴合Linux和Windows系统\n"
        "V<-1.7.5->使用树型文件结构\n"
        "\t并推出随机音频背景音乐\n"
        "V<-1.8.0->加入日志功能\n"
        "V<-1.8.5->丰富日志功能\n"
        "V<-1.9.0->加入虚拟终端\n"
        "V<-1.9.5->加入记录宠物的文件\n"
        "V<-2.0.0->稳定及优化\n"
        "V<-2.0.5->修复一个没重视的Error\n"
        "V<-2.1.0->添加寻宝等Game\n"
        "V<-2.1.5->优化终端,购物等功能\n"
        "V<-2.2.0->小幅度优化常用功能\n"
        "\t正式改名Terra-Infinite\n"
        "\t终端改名STL(Sol-Terra-Luna)\n"
        "V<-2.2.5->添加随机游走的宠物\n"
        "\t双击隐藏/显示主窗口\n"
        "\t可拖动\n"
        "V<-2.3.0->英文化游戏\n"
        "\t并添加2种语言(中文和英文)\n"
        "V<-2.3.5->优化中文化和自定义时区\n"
        "\t主题可以手动/自动调节\n"
        "\t优化列表显示格式"
        )
    
    LINE = "=" * 46

    ANNOUNCEMENT = (
        f"{LINE}\n"
        f"Version   : {GAME_NAME_ALL}\n"
        f"Copyright : {COPYRIGHT_BOOK}\n"
        f"{LINE}\n"
        f"{UPDATE}"
    )
    ANNOUNCEMENT_CHINESE = (
        f"{LINE}\n"
        f"版本 : {GAME_NAME_ALL}\n"
        f"版权 : {COPYRIGHT_BOOK}\n"
        f"{LINE}\n"
        f"{UPDATE_CHINESE}"
    )
    AI_WIFI_ERROR="WifiError in AI-chat"
    AI_OPENAI_ERROR="OpenAIError in AI-chat"
    MUSIC_ERROR="Did not use mp3"
    SETTING_AI="Setting AI-chat"
    OVER_GAME="CLOSE Pet Game"
    OPEN_GAME="OPEN Pet game"
    SETTING_MUSIC="Setting Music"
    AI_AUTO_REMOVE="AI-chat-List Auto-Remove"
    MONEY_NOT_ENOUGH="Money not enough"
    PLAY="Play"        
    BACKPACK_EMPTY="Backpack is empty"
    MP3_ERROR="Non-critical error\nAudio error"
class GameState:                    #Game       manager
    def __init__(self, user_date,pet_date,terminal_date,settings_date):
        if not isinstance(user_date, JsonSaveAndRead):
            raise TypeError("Error")
        if not isinstance(pet_date, JsonSaveAndRead):
            raise TypeError("Error")
        if not isinstance(terminal_date, JsonSaveAndRead):
            raise TypeError("Error")
        if not isinstance(settings_date, JsonSaveAndRead):
            raise TypeError("Error")
        self.user_date=user_date
        self.pet_date=pet_date  
        self.terminal_date=terminal_date
        self.settings_date=settings_date

        self.name = ""
        self.money = 0
        self.day = 0
        self.pet = ""
        self.backpack = GameDict.BACKPACK_INIT.copy()
        self.hunt_shop_backpack=GameDict.HUNT_SHOP.copy()

        self.favor = 0
        self.hungry = 40
        self.hungry_feel = 1
        self.emoji = "^&^"

        self.password = ""
        self.localhost = "localhost"
        self.root_next = 0

        self.last_state = None
        self.english = 1
        self.add_time = 0
        self.open_mp3 = 1
        self.theme = "Auto"
    def load(self):
        try:
            
            user_data = self.user_date.read_all()
            pet_data = self.pet_date.read_all()
            terminal_data = self.terminal_date.read_all()
            settings_date = self.settings_date.read_all()

            self.name = user_data.get("name", "")
            self.day = user_data.get("day", 0)
            self.money = user_data.get("money", 0)
            self.pet = user_data.get("pet", "")
            self.backpack = user_data.get("backpack") or GameDict.BACKPACK_INIT.copy()
            self.hunt_shop_backpack = user_data.get("hunt_shop_backpack") or GameDict.HUNT_SHOP.copy()

            self.favor = pet_data.get("favor", 0)
            self.hungry = pet_data.get("hungry", 40)
            self.hungry_feel = pet_data.get("hungry_feel", 1)
            self.emoji = pet_data.get("emoji", "^&^")
            
            self.localhost = terminal_data.get("localhost", "localhost")
            self.password = terminal_data.get("password", "")
            self.root_next = terminal_data.get("root_next", 0)

            self.last_state = settings_date.get("last_state", None)
            self.open_mp3 = settings_date.get("open_mp3", 1)
            self.english = settings_date.get("english", 1)
            self.add_time = settings_date.get("add_time", 0)
            self.theme = settings_date.get("theme","Auto")
            if self.hungry_feel not in (0, 1):
                self.hungry_feel = 1
            if self.english not in (0, 1):
                self.english = 1
        except (FileNotFoundError, PermissionError, AttributeError, OSError):
            self.user_date.init_to_film()
            self.pet_date.init_to_film()
            self.terminal_date.init_to_film()
    def save(self):
        self.user_date.update(
            day=self.day,
            money=self.money,
            name=self.name,
            pet=self.pet,
            backpack=self.backpack,
            hunt_shop_backpack=self.hunt_shop_backpack
        )
        self.pet_date.update(
            favor=self.favor,
            hungry=self.hungry,
            hungry_feel=self.hungry_feel,
            emoji=self.emoji
        )
        self.terminal_date.update(
            localhost=self.localhost,
            password=self.password,
            root_next=self.root_next
        )
        self.settings_date.update(
            last_state=self.last_state,
            open_mp3=self.open_mp3,
            english=self.english,
            add_time=self.add_time,
            theme=self.theme
        )
class Shop:                         #Shop       manager
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
    
    def fresh_shop_name(self,model=False):
        self.shop_name=[]
        if model:
            for shop_name in self.shop_now.keys():
                self.shop_name.append(shop_name)
        else:
            for shop_name in self.shop.keys():
                self.shop_name.append(shop_name)
class HighShop(Shop):               #HighShop   manager
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
class Emoji:                        #emoji      manager
    SAD=["(；′⌒`)","(｡•́︿•̀｡)","(╥﹏╥)","(つ﹏⊂)"]
    HAPPY=["(◕‿◕✿)","(＾▽＾)","(◠‿◠)","(✿\"▽\")/"]
    NEUTRAL=["(-_-)" ,"(￣▽￣)ゞ"]
    EXCITED=["✧٩(ˊωˋ)و✧","(ﾉ◕ヮ◕)ﾉ:･ﾟ✧","ヽ(°▽°)ノ✿"]
    @staticmethod
    def emoji_random(model):
        index=randint(1,len(model))-1
        return model[index]

class SmallCardGame:                #Minimal card unit class
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
class Card:                         #Complete card feature class

    def __init__(self):
        self.last=0
        self.choice = [GUI.EXIT,GUI.PLAY_CARD,GUI.PASS]
        self.sort={1:4,2:4,3:4,4:4,5:4,6:4,7:4,8:4,9:4,10:4,11:4,12:4,13:4,14:1,15:1}
        self.playMY=SmallCardGame()
        self.playAI=SmallCardGame()

    def ai_say(self):    #Find the smallest valid card in AI's hand
        ai_t_card=[]
        for out_card in self.playAI.play:
            if out_card>self.last:
                ai_t_card.append(out_card)
        if not ai_t_card:
            self.last = 0
            return GUI.PASS
        return_say=min(ai_t_card)
        self.last=return_say
        self.playAI.out(return_say)
        return return_say
    def is_big(self, number):     #Bigger than last
        if self.last>number or self.last==number:
            return False
        elif self.last<number:
            return True
        return False
class CardGame:                     #Full card system class

        @staticmethod
        def run(money,day):
            card = Card()
            add_money=0
            for _ in range(27):
                card.sort = card.playMY.have(card.sort)
                card.sort = card.playAI.have(card.sort)
            while True:  # run
                text,card_dict=Cal.list_text(card.playMY.play)
                game_to_do = GUI.input(f"You Play:{card.playMY.play}", card.choice, "button", "Card Game")
                if game_to_do == GUI.EXIT or not game_to_do:
                    break
                if game_to_do == GUI.PLAY_CARD:
                    me_out_card = GUI.input(f"{card.playMY.play}:", list(card_dict.keys()), "button", "Card Game",)
                    if not me_out_card:
                        continue
                    me_out_card = int(me_out_card)
                    if card.is_big(me_out_card):
                        card.playMY.out(me_out_card)
                        card.last = me_out_card
                    else:
                        continue
                if game_to_do == GUI.PASS:
                    card.last = 0
                if not game_to_do == GUI.EXIT:
                    ai_say = card.ai_say()
                    GUI.input(f"AI:{ai_say}", "", "msg", "AI Say")

                    #If over
                if len(card.playAI.play) <= 0:
                    GUI.input("AI win", "", "msg", "Over")
                    break
                if len(card.playMY.play) <= 0:
                    GUI.input("You win", "", "msg", "Win")
                    add_money=10 * len(card.playAI.play)
                    money, day = Cal.work(money, day, 10 * len(card.playAI.play))
                    GUI.input(f"Got {add_money} Money", "", "msg", "Money")
                    break
            return money, day, add_money
class RockPaperScissors:            #Full rock-paper-scissors system class

        @staticmethod
        def run(money,day):
            add_money=0
            while True:
                if money < 30:
                    GUI.input(CustomTxt.MONEY_NOT_ENOUGH,"","msg","","")
                    break
                rock_paper_scissors = [GUI.ROCK,GUI.PAPER,GUI.SCISSORS]
                rock_paper_scissors_dict = {GUI.ROCK: 0, GUI.PAPER: 1, GUI.SCISSORS: 2}
                rock_paper_scissors_dict_reverse={0:GUI.ROCK, 1:GUI.PAPER, 2:GUI.SCISSORS}
                game_do_to = GUI.input("You Play:", rock_paper_scissors, "button", title="AI Rock-Paper-Scissors")
                if not game_do_to:
                    break
                game_do_to=rock_paper_scissors_dict.get(game_do_to)
                probability=randint(1,10)
                if probability>3:
                    ai_say=(game_do_to+1)%3 #AI WIN
                else:
                    ai_say=(game_do_to+2)%3 #USER WIN
                over=(game_do_to-ai_say)%3
                if over==1:#you win
                    GUI.input(f"AI Say: {rock_paper_scissors_dict_reverse[ai_say]} You win", "", "msg", "Win")
                    money,day=Cal.work(money,day,30)
                    add_money=30
                    GUI.input("Got 30 money","","msg","Money")
                if over==2:#AI win
                    GUI.input(f"AI Say: {rock_paper_scissors_dict_reverse[ai_say]} AI win", "", "msg", "Game")
                    money,day,check=Cal.buy(money,day,30)
                    add_money=-30
                    GUI.input("Lost 30 money","","msg","Money")
                if over==0:#==
                    add_money=0
                    GUI.input(f"AI Say: {rock_paper_scissors_dict_reverse[ai_say]} It is a draw", "", "msg", "Game")
            return money,day,add_money
class DigitalBomb:                  #Digital bomb system class

    @staticmethod
    def run(money, day):
        lower = 0
        upper = 100
        over=randint(lower,upper)
        money_last=money
        money_over=0
        while True:
            if lower + 1 >= upper - 1:
                GUI.input(f"Bomb is {over}", "", "msg", "Bomb")
                money, day = Cal.work(money, day, money_over)
                break
            number=GUI.input(f"{lower}-{upper}", "","integer",title="Bomb", integer_lower=lower+1, integer_upper=upper-1)
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
                GUI.input("!", "", "msg", "Error")
                continue
        add_money=money-money_last
        GUI.input(f"Got {add_money} money","","msg","Money")
        return money,day,add_money
class AI:                           #Minimal chat unit class
    def __init__(self):
        self.AI_chat = None
        self.date = JsonSaveAndRead(GamePaths.AI_PATH, GameDict.AI)
        config = self.date.read_all()
        self.model = config.get("MODEL", "")
        self.last = config.get("LAST", {})
        self.api_key = config.get("APIKEY", "")
        self.url = config.get("URL", "")
        self.name = config.get("NAME", "")

    def change_set(self,model="",apikey="",url="",name=""):
            self.date.update(
                APIKEY=apikey,
                URL=url,
                MODEL=model,
                NAME=name)
    def init(self):
        try:
            self.AI_chat = OpenAI(
                            api_key=self.api_key,
                            base_url=self.url       )
        except OpenAIError:
            return CustomTxt.AI_OPENAI_ERROR
        return None

    def chat(self,ask):
        try:
            answer_ = self.AI_chat.chat.completions.create(
                    model=self.model,
                    messages=[
                {"role": "system", "content": f"""You are the user's good friend. Your name is {self.name}. 
                You are chatting with them. Keep answers concise. Context: {list(self.last.keys())}"""},
                {"role": "user", "content": ask}])
        except OpenAIError:
            GUI.input("Network request failed","","msg","")
            return CustomTxt.AI_WIFI_ERROR
        answer=answer_.choices[0].message.content
        self.last[f"USER:{ask}"]=TimeCal.get_year_to_day()
        self.last[f"AI:{answer}"]=TimeCal.get_year_to_day()
        self.date.update(LAST=self.last)
        return answer

    def auto_remove(self, index=0):
        if not index:
            to_del=[]
            day_max=5
            number_max=30
            for key,value in self.last.items():
                gap=TimeCal.time_to_now_gap(value)
                if gap >= day_max :
                    to_del.append(key)
            number=number_max
            for key in reversed(self.last):
                number=number-1
                if number <= 0:
                    to_del.append(key)
            for key in set(to_del):
                del self.last[key]
            self.date.update(LAST=self.last)
        else:
            number = 1
            for text in list(self.last.keys()):
                if number == index:
                    del self.last[text]
                    self.date.update(LAST=self.last)
                    return None
                number += 1
            self.date.update(LAST=self.last)
class AIChat:                       #Complete chat system class
    def __init__(self):
        self._run=True
        self.ask="Hello"
        self.answer="< Hello >"
        self.AI_chat=AI()
        self.check=self.AI_chat.init()
        self.txt=TxtSaveAndRead(GamePaths.TXT_PATH)
    def run(self):
        if self.check==CustomTxt.AI_OPENAI_ERROR:
            GUI.input("AI is not configured yet","","msg","Error")
            return CustomTxt.AI_OPENAI_ERROR
        while self._run:
            self.ask=GUI.input("Chat","","enter","AI Pet")
            if not self.ask:
                self._run=False
                continue
            self.answer=self.AI_chat.chat(self.ask)
            GUI.input(f"{self.AI_chat.name}:\n{self.answer}","","msg","Chat")
        self.AI_chat.auto_remove()
        self.txt.add_save(CustomTxt.AI_AUTO_REMOVE)
        return None
class Game:                         #Game wrapper class

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

class UserWindow(QWidget):          #User Window
    def __init__(self):
        super().__init__()
        #Instantiate
        self.date_json = JsonSaveAndRead(GamePaths.USER_PASH,GameDict.USER)
        self.pet_json = JsonSaveAndRead(GamePaths.PET_PATH,GameDict.PET)
        self.terminal_json = JsonSaveAndRead(GamePaths.TERMINAL_PATH,GameDict.TERMINAL)
        self.AI_json = JsonSaveAndRead(GamePaths.AI_PATH,GameDict.AI)
        self.settings_json = JsonSaveAndRead(GamePaths.SETTINGS_PATH,GameDict.SETTINGS)
        self.txt = TxtSaveAndRead(GamePaths.TXT_PATH)
        self.state = GameState(self.date_json,self.pet_json,self.terminal_json,self.settings_json)
        self.shop = Shop(ShopDict.FOOD_SHOP)
        self.hunt_shop = HighShop(ShopDict.MONEY_SHOP)
        self.info_label = QLabel()
        self.info_label.setObjectName("infoLabel") 
        self.info_label.setAlignment(Qt.AlignCenter)
        #Game load
        self.state.load()
        GUI.set_USE_EN(self.state.english)
        self.USE_EN=self.state.english
        #Buttons
        self.update_button(True)
        #window title timer
        self.title_timer = QTimer(self)

        #Pet window refresh timer
        self.hungry_timer = QTimer(self)
        self.hungry_timer.timeout.connect(self.update_display)
        self.hungry_timer.start(2000)
        #main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.info_label)
        #Buttons on layout
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_street)
        btn_layout.addWidget(self.btn_digital_bomb)
        btn_layout.addWidget(self.btn_card)
        btn_layout.addWidget(self.btn_rps)
        btn_layout.addWidget(self.btn_go_out)
        btn_layout.addWidget(self.btn_hunt_shop)
        btn_layout.addWidget(self.btn_chat)
        btn_layout.addWidget(self.btn_bag)
        btn_layout.addWidget(self.btn_settings)
        btn_layout.addWidget(self.btn_exit)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)
        #Connect signals and slots
        self.btn_street.clicked.connect(self.on_street)
        self.btn_bag.clicked.connect(self.on_backpack)
        self.btn_digital_bomb.clicked.connect(self.on_digital_bomb)
        self.btn_settings.clicked.connect(self.on_settings)
        self.btn_card.clicked.connect(self.on_card)
        self.btn_rps.clicked.connect(self.on_rps)
        self.btn_exit.clicked.connect(self.on_exit)
        self.btn_go_out.clicked.connect(self.on_go_out)
        self.btn_chat.clicked.connect(self.on_chat)
        self.btn_hunt_shop.clicked.connect(self.on_hunt_shop)

        self.update_QSS()
        self.resize(700, 300)
        self.init_game()
        self.update_display()

        self.pet = SimplePet(self)
        QTimer.singleShot(200, self._adjust_pet_position)

    def update_button(self,model=False):
        if model:
            self.btn_street = QPushButton(Translate.translate_GUI("Street",self.USE_EN))
            self.btn_bag = QPushButton(Translate.translate_GUI("Backpack",self.USE_EN))
            self.btn_digital_bomb = QPushButton(Translate.translate_GUI("Number Bomb",self.USE_EN))
            self.btn_settings = QPushButton(Translate.translate_GUI("Settings",self.USE_EN))
            self.btn_card = QPushButton(Translate.translate_GUI("Single Card",self.USE_EN))
            self.btn_rps = QPushButton(Translate.translate_GUI("Rock-Paper-Scissors",self.USE_EN))
            self.btn_exit = QPushButton(Translate.translate_GUI("Exit",self.USE_EN))
            self.btn_chat = QPushButton(Translate.translate_GUI("AI Chat",self.USE_EN))
            self.btn_go_out = QPushButton(Translate.translate_GUI("Treasure Hunt",self.USE_EN))
            self.btn_hunt_shop = QPushButton(Translate.translate_GUI("Hunt Shop",self.USE_EN))
        else:
            self.btn_street.setText(Translate.translate_GUI("Street", self.USE_EN))
            self.btn_bag.setText(Translate.translate_GUI("Backpack", self.USE_EN))
            self.btn_digital_bomb.setText(Translate.translate_GUI("Number Bomb", self.USE_EN))
            self.btn_settings.setText(Translate.translate_GUI("Settings", self.USE_EN))
            self.btn_card.setText(Translate.translate_GUI("Single Card", self.USE_EN))
            self.btn_rps.setText(Translate.translate_GUI("Rock-Paper-Scissors", self.USE_EN))
            self.btn_exit.setText(Translate.translate_GUI("Exit", self.USE_EN))
            self.btn_chat.setText(Translate.translate_GUI("AI Chat", self.USE_EN))
            self.btn_go_out.setText(Translate.translate_GUI("Treasure Hunt", self.USE_EN))
            self.btn_hunt_shop.setText(Translate.translate_GUI("Hunt Shop", self.USE_EN))
    def update_QSS(self,model=True):
        if self.state.theme==GUI.DARK:
            time=2
        elif self.state.theme==GUI.LIGHT:
            time=1
        else :
            time=TimeCal.now_time_1am_or_2pm(self.state.add_time)

        if time == 1:
            title=CustomTxt.TITLE_SOL
            label_model=GUI.MODEL_LIGHT_LABEL
            model=GUI.MODEL_LIGHT
        elif time == 2:
            title=CustomTxt.TITLE_LUNA
            label_model=GUI.MODEL_DARK_LABEL
            model=GUI.MODEL_DARK
        self.setWindowTitle(title)
        self.setStyleSheet(label_model)
        QApplication.instance().setStyleSheet(model)
    def update_display(self):
        self.hungry_cal()
        text_backpack=Cal.dict_text(self.state.backpack)
        text_hunt_backpack=Cal.dict_text(self.state.hunt_shop_backpack)
        text = ""
        text += f"Name: {self.state.name}\n"
        text += f"Pet: {self.state.pet}\n"
        text += f"Emoji: {self.state.emoji}\n"
        text += f"Hungry: {self.state.hungry}%\n"
        text += f"Money: {self.state.money}\n"
        text += f"Day: {self.state.day}\n"
        text += f"Favor: {self.state.favor}\n"
        text += f"Backpack: {text_backpack}\n"
        text += f"HuntBackpack: {text_hunt_backpack}"
        text=Translate.text(text,self.USE_EN)
        self.info_label.setText(text)
    def init_game(self):
        self.state.load()
        self.OPEN_MP3=self.state.open_mp3   #Open_mp3
        if not self.state.name and not self.state.pet:
            choice_languages=GUI.input("Languages:",GUI.SET_UP_LANGUAGES,"button","LANGUAGES")
            if choice_languages==GUI.CHINESE:
                self.state.english=0
                self.USE_EN=0
                GUI.set_USE_EN(0)
            elif choice_languages==GUI.ENGLISH:
                self.state.english=1
                self.USE_EN=1
                GUI.set_USE_EN(1)
            self.state.add_time=GUI.input("Time Zone:","","integer","TIME ZONE"
                                          ,integer_lower=-12,integer_upper=12,integer_start=0)
            self.state.name = GUI.input("Name?", "", "enter", "Terra")
            self.state.pet = GUI.input("PetName?", "", "enter", "Terra")
            self.state.day = 1
            self.state.favor = 0
            self.state.money = 0
            self.txt.add_save(CustomTxt.GAME_NAME_ALL)
            self.state.save()
        self.txt.add_save(CustomTxt.OPEN_GAME)
        GUI.input("\tHello\n\tAnything fun today?", "", "msg", CustomTxt.GAME_NAME_ALL)
        self.music_on()
    def music_on(self):
        if self.OPEN_MP3==1:
            check=Music.play_mp3_loop(GamePaths.MUSIC_PATH)
            if check==CustomTxt.MUSIC_ERROR:
                self.txt.add_save(check,error=True)
        elif self.OPEN_MP3==2:
            Music.play_random_music_loop()
        else:
            pass
    def on_street(self):
        running=True
        while running:
            self.shop.fresh_shop()
            self.shop.fresh_shop_name(True)
            choice = GUI.input(f"Passing by a shop,menu: {self.shop.shop_name}. Stay?",
                                GUI.STREET_IN, "button", "Street")
            if choice == GUI.NO or not choice:
                running=False
                continue
            elif choice == GUI.NEXT:
                continue
            elif choice == GUI.YES:
                running_buy=True
                while running_buy:
                    buy_choice = GUI.input(f"Buy:{self.shop.shop_now}:", self.shop.shop_name, "button", "Street",self.USE_EN)
                    if not buy_choice:
                        running_buy=False
                        continue
                    elif buy_choice not in self.shop.shop_now:
                        GUI.input("!", "", "msg", "Error")
                        continue
                    buy_number=GUI.input(f"Buy quantity:","","integer","NUMBER",integer_lower=1,integer_upper=1000000)
                    if not buy_number:
                        running_buy=False
                        continue
                    price=self.shop.get_price(buy_choice)
                    self.state.money, self.state.day, check = Cal.buy(
                        self.state.money, self.state.day, 
                        price*buy_number
                    )
                    if check:
                        GUI.input(f"{buy_number} {buy_choice}", "", "msg", "Street")
                        for _ in range(0,buy_number):
                            self.state.backpack[buy_choice]+=1
                        self.txt.add_save(f"{GUI.BUY} {buy_number} {buy_choice}")
                    else:
                        GUI.input(CustomTxt.MONEY_NOT_ENOUGH, "", "msg", "Street")
        self.state.save()
        self.update_display()
    def on_backpack(self):
        while True:
            if Cal._is_empty(self.state.backpack):
                GUI.input(CustomTxt.BACKPACK_EMPTY, "", "msg", "Backpack")
                break
            text=Cal.dict_text(self.state.backpack)
            choice = GUI.input(text, GUI.BAG, "button", "Backpack")
            if choice == GUI.BACK:
                break
            if choice == GUI.EAT:
                eatable = [k for k, v in self.state.backpack.items() if v > 0]
                if not eatable:
                    GUI.input(CustomTxt.BACKPACK_EMPTY, "", "msg", "Backpack")
                    continue
                eat_choice = GUI.input(f"{text}Eat:\n", eatable, "button", "Backpack")
                if not eat_choice or eat_choice not in eatable:
                    continue
                max_n = self.state.backpack[eat_choice]
                number = GUI.input("Eat quantity", "", "integer", "Eat",
                                   integer_lower=1, integer_upper=max_n)
                if not number:
                    continue
                for _ in range(0,number):
                    self.state.hungry=self.state.hungry-35
                    self.state.backpack[eat_choice]-=1
                    self.state.favor += 1
                GUI.input(f"Eat {number} {eat_choice}", "", "msg", "Backpack")
                self.txt.add_save(f"{GUI.EAT} {eat_choice}*{number}")
        self.state.save()
        self.update_display()
    def on_digital_bomb(self):
        
        self.state.money, self.state.day,add_money = Game.digital_bomb_run(
            self.state.money, self.state.day
        )
        self.txt.add_save(f"{CustomTxt.PLAY} Digital_bomb {add_money}")
        self.state.save()
        self.update_display()
    def on_settings(self):
        while True:
            choice = GUI.input("Enjoy", GUI.SET_UP, "button", "Setting")
            if choice == GUI.ANNOUNCEMENT:
                if self.USE_EN:
                    GUI.input("", CustomTxt.ANNOUNCEMENT, "text", "Announcement",english=True)
                else:
                    GUI.input("", CustomTxt.ANNOUNCEMENT_CHINESE,"text","CH")
            elif choice == GUI.TERMINAL:
                terminal = Terminal(self,self.txt,self.state)
                terminal.exec_()
            elif choice == GUI.MUSIC_SETTINGS:
                choice_music=GUI.input("Use?",GUI.SET_UP_MUSIC,"button","Music")
                if choice_music==GUI.NONE:
                    self.state.open_mp3 = 0
                    self.OPEN_MP3=0
                    Music.easy_stop()
                elif choice_music==GUI.MP3:
                    self.state.open_mp3 = 1
                    self.OPEN_MP3=1
                    Music.easy_stop()
                    Music.play_mp3_loop(GamePaths.MUSIC_PATH)
                elif choice_music==GUI.RANDOM_MUSIC:
                    self.state.open_mp3 = 2
                    self.OPEN_MP3=2
                    Music.easy_stop()
                    Music.play_random_music_loop()
                self.txt.add_save(CustomTxt.SETTING_MUSIC)
            elif choice == GUI.SHOW_HIDE_PET:
                if self.pet.isVisible():
                    self.pet.hide()
                else:
                    self.pet.show()
            elif choice == GUI.BACK or not choice:
                break
            elif choice == GUI.LANGUAGES:
                choice_languages=GUI.input("SET:",GUI.SET_UP_LANGUAGES,"button","LANGUAGES")
                if choice_languages==GUI.CHINESE:
                    self.state.english=0
                    self.USE_EN=0
                    GUI.set_USE_EN(0)
                    self.update_button()
                elif choice_languages==GUI.ENGLISH:
                    self.state.english=1
                    self.USE_EN=1
                    GUI.set_USE_EN(1)
                    self.update_button()
            elif choice == GUI.SEE_MORE:
                while True:
                    more_choice = GUI.input("Enjoy", GUI.SET_UP_MORE, "button", "More")
                    if more_choice==GUI.BACK or not more_choice:
                        break
                    elif more_choice == GUI.RESET:
                        confirm = GUI.input("Reset!", "", "yn", "!!!!!!!!!!!!!!!!")
                        if confirm:
                            self.txt.init_file()
                            self.date_json.init_to_film()
                            self.pet_json.init_to_film()
                            self.state.load()
                            self.state.name = GUI.input("Name?", "", "enter", "Welcome")
                            self.state.pet = GUI.input("PetName?", "", "enter", "Welcome")
                            self.txt.add_save(CustomTxt.GAME_NAME_ALL)
                            self.txt.add_save(CustomTxt.OPEN_GAME)
                            GUI.input("\tReset complete", "", "msg", "Game")
                    elif more_choice == GUI.AI_MEMORY:
                        text=""
                        number=1
                        ai_chat_recall=AI()
                        last_json=self.AI_json.read_from_file("LAST")
                        for string in last_json.keys():
                            text += f"{number} {string}\n"
                            number=number+1
                        index = GUI.input(text, "Del", "integer", "AI", 
                            integer_lower=0, integer_upper=30)
                        if index:
                            ai_chat_recall.auto_remove(index)
                    elif more_choice == GUI.VIEW_LOG:
                        GUI.input(self.txt.read(),"","text","Log",english=True)
                    elif more_choice == GUI.AI_SETTINGS:
                        ai_chat_choice=GUI.input("\tSet:",GUI.SET_UP_AI,"button","AI Setting")
                        ai_setting=AI()
                        if ai_chat_choice==GUI.NAME:
                            name_new=GUI.input("\tAI Pet","","enter","new-AI-NAME")
                            ai_setting.change_set(ai_setting.model,ai_setting.api_key,ai_setting.url,name_new)

                        elif ai_chat_choice==GUI.API_KEY:
                            apikey_new=GUI.input("\tAI Pet","","enter","new-AI-APIKEY")
                            ai_setting.change_set(ai_setting.model,apikey_new,ai_setting.url,ai_setting.name)

                        elif ai_chat_choice==GUI.URL:
                            url_new=GUI.input("\tAI Pet","","enter","new-AI-URL")
                            ai_setting.change_set(ai_setting.model,ai_setting.api_key,url_new,ai_setting.name)

                        elif ai_chat_choice==GUI.MODEL:
                            model_new=GUI.input("\tAI Pet","","enter","new-AI-MODEL")
                            ai_setting.change_set(model_new,ai_setting.api_key,ai_setting.url,ai_setting.name)

                        if ai_chat_choice:
                            self.txt.add_save(f"{CustomTxt.SETTING_AI} {ai_chat_choice}")
                    elif more_choice == GUI.VISIT_GITHUB:
                        url_yn=GUI.input("Visit Github?","","yn",CustomTxt.GAME_NAME_SIMPLE)
                        if url_yn:
                            open_new_tab(CustomTxt.URL)
            elif choice == GUI.TIMEZONE:
                self.state.add_time=GUI.input("Time Zone:","","integer","TIME ZONE",
                                              integer_lower=-12,integer_upper=12,integer_start=0)
                self.update_QSS()
            elif choice == GUI.THEME:
                self.state.theme=GUI.input("Theme",GUI.SET_UP_THEME,"button","Theme")
                self.update_QSS()
        self.state.save()
        self.update_display()
    def on_card(self):
        self.state.money, self.state.day,add_money = Game.card_run(
            self.state.money, self.state.day
        )
        self.txt.add_save(f"{CustomTxt.PLAY} Card_game {add_money}")
        self.update_display()
    def on_rps(self):
        self.state.money, self.state.day ,add_money= Game.rock_paper_scissors_run(
            self.state.money, self.state.day
        )
        self.txt.add_save(f"{CustomTxt.PLAY} Rock_paper_scissors {0+add_money}")
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
            choice=GUI.input("\t Go:",GUI.GO_OUT,"button","out-side")
            if choice==GUI.BACK or not choice:
                running=False
                continue
            if randint(1,3) < 2:
                text = self.hunt_shop.random_shop()
                if text and text in self.state.hunt_shop_backpack:
                    GUI.input(f"{text}", "", "msg", "-")
                    self.state.hunt_shop_backpack[text] += 1
    def on_hunt_shop(self):
        running=True
        text=self.hunt_shop.shop_list()
        self.hunt_shop.fresh_shop_name()
        while running:
            text_backpack=Cal.dict_text(self.state.hunt_shop_backpack)
            choice=GUI.input(f"Money:{self.state.money}\nBackpack:{text_backpack}",GUI.MONEY_SHOP,"button",
                             "Hunt-Shop")
            if choice==GUI.BUY:
                running_buy=True
                while running_buy:
                    buy_choice=GUI.input(f"Money:{self.state.money}\nShop:\n{text}",self.hunt_shop.shop_name, "button"
                                         , "Hunt-Shop")
                    if not buy_choice:
                        running_buy=False
                        continue
                    if buy_choice not in self.hunt_shop.shop_name:
                        GUI.input("!", "", "msg","Error")
                        continue
                    self.state.money, self.state.day, check = Cal.buy(
                        self.state.money, self.state.day, 
                        self.hunt_shop.get_shop_now_price(buy_choice)
                    )
                    if check:
                        GUI.input(f"A {buy_choice}", "", "msg", "Hunt-Shop")
                        self.state.hunt_shop_backpack[buy_choice]+=1
                        self.txt.add_save(f"{GUI.BUY} {buy_choice}")
                    else:
                        GUI.input(CustomTxt.MONEY_NOT_ENOUGH, "", "msg", "Hunt-Shop")
            elif choice==GUI.BACK or not choice:
                running=False
                continue
            elif choice==GUI.SELL:
                if Cal._is_empty(self.state.backpack):
                    GUI.input(CustomTxt.BACKPACK_EMPTY, "", "msg", "Hunt-Shop")
                    continue
                sellable = [k for k, v in self.state.hunt_shop_backpack.items() if v > 0]
                if not sellable:
                    GUI.input(CustomTxt.BACKPACK_EMPTY, "", "msg", "Hunt-Shop")
                    continue
                sell_choice = GUI.input(f"Backpack:{text_backpack}\nPrice:\n{text}",
                                        sellable, "button", "Hunt-Shop")
                if not sell_choice or sell_choice not in sellable:
                    continue
                self.state.money, self.state.day = Cal.work(
                    self.state.money, self.state.day, 
                    self.hunt_shop.get_shop_now_price(sell_choice)
                )
                GUI.input(f"{sell_choice}", "", "msg", "Hunt-Shop")
                self.state.hunt_shop_backpack[sell_choice]-=1
                self.txt.add_save(f"{GUI.SELL} {sell_choice}")
            elif choice==GUI.SELL_ALL:
                if Cal._is_empty(self.state.backpack):
                    GUI.input(CustomTxt.BACKPACK_EMPTY, "", "msg", "Hunt-Shop")
                    continue
                total_money = 0
                for item, count in self.state.hunt_shop_backpack.items():
                    if count > 0:
                        total_money += self.hunt_shop.get_shop_now_price(item) * count
                self.state.money, self.state.day = Cal.work(
                    self.state.money, self.state.day, total_money
                )
                GUI.input(f"{total_money} Money", "", "msg", "Hunt-Shop")
                self.txt.add_save(f"{GUI.SELL} {total_money}")
                self.state.hunt_shop_backpack = GameDict.HUNT_SHOP.copy()
        self.state.save()
    def on_exit(self):
        self.close()
    def closeEvent(self, event):
        self.state.last_state = TimeCal.now_time()
        self.state.save()
        self.txt.add_save(CustomTxt.OVER_GAME)
        if hasattr(self, "pet"):
            self.pet.close()
        Music.easy_stop()
        event.accept()
    def _adjust_pet_position(self):
        if hasattr(self, 'pet'):
            self.pet.move(self.x() + 10, self.y() + 10)
            self.pet.show()
class Terminal(QDialog):            #Terminal
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
        self.P1 = f"[User@STL]$:"
        self.update_P1()
        self.history = []
        self.history_index = None
        self.current_input = ""
        self.setWindowTitle("Sol-Terra-Luna-Shell")
        self.resize(600, 400)
        self.setStyleSheet("background-color: #000000; color: #00ff00; font-family: \"Courier New\"; font-size: 14px;")

        self.output_area = QPlainTextEdit()
        self.output_area.setStyleSheet("background-color: #0a0a0a; border: none;")
        self.output_area.installEventFilter(self)
        self.output_area.setUndoRedoEnabled(False)
        layout = QVBoxLayout()
        layout.addWidget(self.output_area)
        self.setLayout(layout)
        self.output_area.insertPlainText(f"You Can Enter \"help\"\n")
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
    def show_history_command(self, cmd):
        #string --> command
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
            self.easy_print(self.P1)
            return None
        parts = cmd.split()
        command = parts[0].capitalize()
        args = parts[1:]
        
        if command == GUI.EXIT:
            self.state.save()
            self.close()
        elif command == GUI.HELP:
            root_text = """Commands:\t
                money <number>    - View and modify money\t
                favor <number>    - View and modify favor\t
                pet-name <name>   - View and modify pet name\t
                name <name>       - View and modify player name\t
                day <day>         - View and modify day\t
                date              - View and modify log\t
                hungry <number>   - Modify or disable hunger\t
                info              - View current status\t
                su                - Switch identity\t
                password <str>    - Set password\t
                hostname <str>    - Set hostname\t
                root-next         - Toggle permanent root\t
                exit              - Exit terminal\n"""
            user_text = """Commands:\t
                money             - View money\t
                favor             - View favor\t
                pet-name          - View pet name\t
                name              - View player name\t
                day               - View day\t
                date              - View log\t
                hungry            - View hunger\t
                info              - View current status\t
                su                - Switch identity\t
                hostname          - Set hostname\t
                exit              - Exit terminal\n"""
            if self.is_root():
                text=root_text
            else:
                text=user_text
            self.easy_print(text,end="")

        elif command == GUI.MONEY:
            if args:
                if self.is_root():
                    try:
                        amount = int(args[0])
                        self.state.money = amount
                        self.state.save()
                        self.easy_print(f"Money is {amount} now.")
                    except ValueError:
                        self.easy_print("Error: Please enter an integer amount.")
            else:
                self.easy_print(f"Now:{self.state.money}")
        elif command == GUI.HUNGRY:
            if args:
                if self.is_root():
                    try:
                        amount = int(args[0])
                        self.state.hungry = amount
                        self.state.save()
                        self.easy_print(f"Hungry is  {amount}% now.")
                    except ValueError:
                        self.easy_print("Error: Please enter an integer amount.")
            else:
                if self.is_root():
                    if self.state.hungry_feel:
                        self.state.hungry_feel=0
                    else:
                        self.state.hungry_feel=1
                    self.state.save()
                    self.easy_print(f"Hungry Model is {self.state.hungry_feel}(1 is on,0 is close)")
                else:
                    self.easy_print(f"Now:{self.state.hungry}%")
        elif command == GUI.FAVOR:
            if args:
                if self.is_root():
                    try:
                        value = int(args[0])
                        self.state.favor = value
                        self.state.save()
                        self.easy_print(f"favor is {value} now.")
                    except ValueError:
                        self.easy_print("Error: Please enter an integer amount.")
            else:
                self.easy_print(f"Now:{self.state.favor}")
        elif command == GUI.PET_NAME:
            if args:
                if self.is_root():
                    try:
                        amount = args[0]
                        self.state.pet = amount
                        self.state.save()
                        self.easy_print(f"Pet-Name is {amount} now.")
                    except ValueError:
                        self.easy_print("Error")
            else:
                self.easy_print(f"Now:{self.state.pet}")
        elif command == GUI.NAME:
            if args:
                if self.is_root():
                    try:
                        amount = args[0]
                        self.state.name = amount
                        self.state.save()
                        self.easy_print(f"Name is {amount} now.")
                    except ValueError:
                        self.easy_print("Error")
            else:
                self.easy_print(f"Now:{self.state.name}")
        elif command == GUI.DAY:
            if args:
                if self.is_root():
                    try:
                        value = int(args[0])
                        self.state.day= value
                        self.state.save()
                        self.easy_print(f"Day is {value} now.")
                    except ValueError:
                        self.easy_print("Error: Please enter an integer amount.")
            else:
                self.easy_print(f"Now:{self.state.day}.") 
        elif command == GUI.DATE:
            date_=GUI.input(self.txt.read(),"","text","DATE")
            if self.is_root():
                self.txt.write(date_)
        elif command == GUI.INFO:
            info_text_backpack=Cal.dict_text(self.state.backpack)
            info_text_hunt_backpack=Cal.dict_text(self.state.hunt_shop_backpack)
            info_text = ""
            info_text += f"Name: {self.state.name}\n"
            info_text += f"Pet: {self.state.pet}\n"
            info_text += f"Emoji: {self.state.emoji}\n"
            info_text += f"Hungry: {self.state.hungry}%\n"
            info_text += f"Money: {self.state.money}\n"
            info_text += f"Day: {self.state.day}\n"
            info_text += f"Favor: {self.state.favor}\n"
            info_text += f"Backpack: {info_text_backpack}\n"
            info_text += f"HuntBackpack: {info_text_hunt_backpack}"
            self.easy_print(info_text,end="")
        elif command == GUI.SU:
            if args:
                if not self.is_root():
                    password = args[0]
                    if password == self.state.password:
                        self.root=1
                        self.update_P1()
                    else:
                        self.easy_print("Wrong password. Use: su <password>")
            else:
                if self.is_root():
                    self.root=0
                    self.update_P1()
                elif not self.is_root():
                    if not self.state.password:
                        self.root=1
                        self.update_P1()
        elif command == GUI.PASSWORD:
            if args:
                if self.is_root():
                    password = args[0]
                    self.state.password = password
                    self.state.save()
                    self.easy_print("Password set")
            else:
                if self.is_root():
                    self.state.password = ""
                    self.state.save()
                    self.easy_print("Password removed")
        elif command == GUI.HOSTNAME:
            if args:
                hostname = args[0]
                self.state.localhost = hostname
                self.state.save()
                self.update_P1()
                self.easy_print(f"Hostname is {hostname} now.")
            else:
                self.easy_print("Please provide a hostname")
        elif command == GUI.ROOT_NEXT:
            if self.is_root():
                if self.state.root_next==0:
                    self.state.root_next=1
                    self.state.save()
                    self.easy_print("RootNext -I")
                elif self.state.root_next==1:
                    self.state.root_next=0
                    self.state.save()
                    self.easy_print("RootNext -O")
            else:
                pass
        else :
            self.easy_print(f"{cmd}: STL: Command not found")
    def update_P1(self):
        if self.is_root():
            self.P1=f"[root@{self.state.localhost}]$ "
        else:
            self.P1=f"[{self.state.name}@{self.state.localhost}]# "
    def is_root(self):
        if self.root:
            return True
        else:
            return False
    def easy_print(self,text,end="\n"):
        self.output_area.appendPlainText(f"{text}{end}")
class SimplePet(QWidget):           #Pet Window
    def __init__(self, main_window):
        size_png=[80,80]
        super().__init__()
        self.main_window = main_window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.label.setFixedSize(size_png[0],size_png[1])
        pixmap = QPixmap(GamePaths.PET_PNG_PATH)
        if not pixmap.isNull():
            self.label.setPixmap(pixmap.scaled(size_png[0],size_png[1], Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.label.setText("Pet")
        self.label.setStyleSheet("font-size: 48px; background: transparent;")
        self.label.setAlignment(Qt.AlignCenter)
        self.resize(80, 80)

        self.target_pos = self.pos()
        self.step_timer = QTimer(self)
        self.step_timer.timeout.connect(self._move_step)
        self.step_timer.setInterval(30)  # 30ms Go

        self.random_timer = QTimer(self)
        self.random_timer.timeout.connect(self._set_random_target)
        self.random_timer.setInterval(3000)
        self.random_timer.start()

        self.drag_start_pos = None
        self.drag_threshold = 5

    def _set_random_target(self):
        screen = QApplication.primaryScreen().geometry()
        distance = 150
        new_x = self.x() + randint(-distance, distance)
        new_y = self.y() + randint(-distance, distance)
        max_x = screen.width() - self.width()
        max_y = screen.height() - self.height()
        new_x = max(0, min(new_x, max_x))
        new_y = max(0, min(new_y, max_y))
        self.target_pos = QPoint(new_x, new_y)
        self.step_timer.start()

    def _move_step(self):
        current = self.pos()
        delta_x = self.target_pos.x() - current.x()
        delta_y = self.target_pos.y() - current.y()
        step = 5
        if abs(delta_x) <= step:
            step_x = delta_x
        else:
            step_x = step if delta_x > 0 else -step
        if abs(delta_y) <= step:
            step_y = delta_y
        else:
            step_y = step if delta_y > 0 else -step
        self.move(current.x() + step_x, current.y() + step_y)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.globalPos()
            self.step_timer.stop()
            self.random_timer.stop()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_start_pos is not None:
            delta = event.globalPos() - self.drag_start_pos
            if delta.manhattanLength() > self.drag_threshold:
                self.move(self.pos() + delta)
                self.drag_start_pos = event.globalPos()
                event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = None
            self.random_timer.start()
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.main_window is not None:
            if self.main_window.isVisible():
                self.main_window.hide()
            else:
                self.main_window.show()
                self.main_window.raise_()
        event.accept()
class Terra:                        #Game Manager
    @staticmethod
    def run():
        if __name__=="__main__":
            app = QApplication(argv)
            user_window = UserWindow()
            user_window.show()
            app.exec_()

#main
Terra.run()