from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QMainWindow,
                               QFrame, QMessageBox, QLineEdit, QComboBox,
                               QPushButton, QStackedWidget, QFileDialog, QPlainTextEdit)
from PySide6.QtGui import QIcon, QFont, QPixmap, QDragEnterEvent, QDropEvent
from PySide6.QtCore import QSize, Qt, Slot, QThread
import sys
import pynput.mouse
import pynput.keyboard
import time
import random
import json
import ast


class StimulatedElf(QMainWindow):
    def __init__(self):
        super().__init__()

        # 全局变量
        self.scroll_thread = None
        self.mouseClick_thread = None
        self.input_thread = None
        self.msg_cover = None
        self.msg_input = None
        global config

        # 窗口设置
        self.setWindowTitle("Stimulated Elf")
        self.setFixedSize(800, 600)
        screen = QApplication.screens()[0]
        size = self.geometry()
        self.move((screen.geometry().width() - size.width()) // 2, (screen.geometry().height() - size.height()) // 2)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowIcon(QIcon("Resource/icon.png"))

        #  stacked_widget
        self.main_stacked_widget = QStackedWidget(self)
        self.main_stacked_widget.setObjectName("main_stacked_widget")
        self.main_stacked_widget.setGeometry(0, 0, 800, 600)
        self.main_stacked_widget.setCurrentIndex(0)
        self.main_stacked_widget.setStyleSheet("#main_stacked_widget{background-color:white;}")

        self.main_page = QWidget()
        self.main_page.setObjectName("main_page")

        self.setting_page = QWidget()
        self.setting_page.setObjectName("setting_page")

        self.main_stacked_widget.addWidget(self.main_page)
        self.main_stacked_widget.addWidget(self.setting_page)

        self.function_stacked_widget = QStackedWidget(self.main_page)
        self.function_stacked_widget.setObjectName("function_stacked_widget")
        self.function_stacked_widget.setGeometry(230, 70, 530, 400)
        self.function_stacked_widget.setCurrentIndex(0)
        self.function_stacked_widget.setStyleSheet("#function_stacked_widget{background-color:white;}")
        self.welcome_page = QWidget()
        self.welcome_page.setObjectName("welcome_page")

        self.input_page = QWidget()
        self.input_page.setObjectName("input_page")

        self.mouseClick_page = QWidget()
        self.mouseClick_page.setObjectName("mouseClick_page")

        self.scroll_page = QWidget()
        self.scroll_page.setObjectName("scroll_page")

        self.function_stacked_widget.addWidget(self.welcome_page)
        self.function_stacked_widget.addWidget(self.input_page)
        self.function_stacked_widget.addWidget(self.mouseClick_page)
        self.function_stacked_widget.addWidget(self.scroll_page)

        # line
        self.line_main = QFrame(self.main_page)
        self.line_main.setObjectName("line_main")
        self.line_main.setGeometry(209, 40, 2, 460)
        self.line_main.setFrameShape(QFrame.VLine)
        self.line_main.setFrameShadow(QFrame.Sunken)

        # pushbutton_icon
        self.pb_icon = QPushButton(self.main_page)
        self.pb_icon.setGeometry(20, 20, 40, 40)
        self.pb_icon.setIcon(QIcon("Resource/icon.png"))
        self.pb_icon.setObjectName("pb_icon")
        self.pb_icon.setIconSize(QSize(40, 40))
        self.pb_icon.clicked.connect(lambda: self.function_stacked_widget.setCurrentIndex(0))
        self.pb_icon.setStyleSheet("#pb_icon{border: none;}#pb_icon:hover{border: 2px solid black;border-radius:5px}")

        # pushbutton_settings
        pushbutton_settings_font = QFont()
        pushbutton_settings_font.setFamily("华文中宋")
        pushbutton_settings_font.setPointSize(12)

        self.pb_settings_main = QPushButton("[高级设置]", self.main_page)
        self.pb_settings_main.setGeometry(20, 500, 100, 40)
        self.pb_settings_main.setObjectName("pb_settings_main")
        self.pb_settings_main.setFont(pushbutton_settings_font)
        self.pb_settings_main.clicked.connect(lambda: self.main_stacked_widget.setCurrentIndex(1))
        self.pb_settings_main.setStyleSheet(
            "#pb_settings_main:hover{border:none;color:blue}"
            "#pb_settings_main{border: none;}")

        # pushbutton_tab
        tab_font = QFont()
        tab_font.setFamily("华文中宋")
        tab_font.setPointSize(13)

        self.pb_input_main = QPushButton("输入模拟", self.main_page)
        self.pb_input_main.setGeometry(20, 70, 170, 120)
        self.pb_input_main.setObjectName("pb_input_main")
        self.pb_input_main.setFont(tab_font)
        self.pb_input_main.clicked.connect(lambda: self.function_stacked_widget.setCurrentIndex(1))
        self.pb_input_main.setStyleSheet(
            "#pb_input_main:hover{border: none;padding: 5px;border-radius:10px;"
            "background: qlineargradient(x1:1, y1:1, x2:0, y2:1,stop:0 rgba(0, 0, 0, 0), stop:1 rgb(0, 0, 0));}"
            "#pb_input_main{border: none;}")

        self.pb_mouseClick_main = QPushButton("鼠标连点", self.main_page)
        self.pb_mouseClick_main.setGeometry(20, 210, 170, 120)
        self.pb_mouseClick_main.setObjectName("pb_mouseClick_main")
        self.pb_mouseClick_main.setFont(tab_font)
        self.pb_mouseClick_main.clicked.connect(lambda: self.function_stacked_widget.setCurrentIndex(2))
        self.pb_mouseClick_main.setStyleSheet(
            "#pb_mouseClick_main:hover{border: none;padding: 5px;border-radius:10px;"
            "background: qlineargradient(x1:1, y1:1, x2:0, y2:1,stop:0 rgba(0, 0, 0, 0), stop:1 rgb(0, 0, 0));}"
            "#pb_mouseClick_main{border: none;}")

        self.pb_scroll_main = QPushButton("滚轮模拟", self.main_page)
        self.pb_scroll_main.setGeometry(20, 350, 170, 120)
        self.pb_scroll_main.setObjectName("pb_scroll_main")
        self.pb_scroll_main.setFont(tab_font)
        self.pb_scroll_main.clicked.connect(lambda: self.function_stacked_widget.setCurrentIndex(3))
        self.pb_scroll_main.setStyleSheet(
            "#pb_scroll_main:hover{border: none;padding: 5px;border-radius:10px;"
            "background: qlineargradient(x1:1, y1:1, x2:0, y2:1,stop:0 rgba(0, 0, 0, 0), stop:1 rgb(0, 0, 0));}"
            "#pb_scroll_main{border: none;}")

        # label
        welcome_font = QFont()
        welcome_font.setFamilies(["Lucida Calligraphy"])
        welcome_font.setPointSize(25)
        welcome_font.setBold(True)

        self.lb_welcome = QLabel(self.welcome_page)
        self.lb_welcome.setObjectName("lb_welcome")
        self.lb_welcome.setGeometry(120, 170, 310, 60)
        self.lb_welcome.setFont(welcome_font)
        self.lb_welcome.setText("Stimulated Elf")
        self.lb_welcome.setAlignment(Qt.AlignCenter)

        self.lb_icon = QLabel(self.welcome_page)
        self.lb_icon.setObjectName("lb_icon")
        self.lb_icon.setGeometry(230, 60, 60, 60)
        self.lb_icon.setPixmap(QPixmap("Resource/icon.png").scaled(
            QSize(60, 60),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))

        # 模拟输入
        input_font = QFont()
        input_font.setFamilies(["华文中宋"])
        input_font.setPointSize(10)

        self.pt_input = QPlainTextEdit(self.input_page)
        self.pt_input.setGeometry(40, 20, 460, 300)
        self.pt_input.setFont(input_font)
        self.pt_input.setPlaceholderText("在此输入需模拟输入的内容，可以导入txt文件或把文件拖到此处。")
        self.pt_input.setAcceptDrops(True)
        self.pt_input.dragEnterEvent = self.dragEnterEvent
        self.pt_input.dropEvent = self.dropEvent

        self.pb_update_input = QPushButton("导入", self.input_page)
        self.pb_update_input.setGeometry(40, 350, 90, 40)
        self.pb_update_input.setFont(input_font)
        self.pb_update_input.setObjectName("pb_update_input")
        self.pb_update_input.clicked.connect(self.update_text)

        self.pb_confirm_input = QPushButton("确认", self.input_page)
        self.pb_confirm_input.setGeometry(410, 350, 90, 40)
        self.pb_confirm_input.setFont(input_font)
        self.pb_confirm_input.setObjectName("pb_confirm_input")
        self.pb_confirm_input.clicked.connect(self.input_confirm)

        # 鼠标连点
        mouseClick_font1 = QFont()
        mouseClick_font1.setFamilies(["华文中宋"])
        mouseClick_font1.setPointSize(12)

        mouseClick_font2 = QFont()
        mouseClick_font2.setFamilies(["华文中宋"])
        mouseClick_font2.setPointSize(14)

        self.cob_time = QComboBox(self.mouseClick_page)
        self.cob_time.setGeometry(120, 70, 150, 35)
        self.cob_time.setObjectName("cob_time")
        self.cob_time.addItems(["10秒", "30秒", "自定义", "持续"])
        self.cob_time.setPlaceholderText("持续时间")
        self.cob_time.setCurrentIndex(-1)
        self.cob_time.setFont(mouseClick_font1)
        self.cob_time.currentIndexChanged.connect(self.set_le_enabled)

        self.le_time = QLineEdit(self.mouseClick_page)
        self.le_time.setGeometry(280, 70, 150, 35)
        self.le_time.setObjectName("le_time")
        self.le_time.setPlaceholderText("请输入时间")
        self.le_time.setFont(mouseClick_font1)
        self.le_time.setStyleSheet("#le_time{padding:3px}")
        self.le_time.setEnabled(False)

        self.lb_warning_mouseclick1 = QLabel(self.mouseClick_page)
        self.lb_warning_mouseclick1.setGeometry(90, 160, 380, 30)
        self.lb_warning_mouseclick1.setObjectName("lb_warning_mouseclick1")
        self.lb_warning_mouseclick1.setFont(mouseClick_font2)
        self.lb_warning_mouseclick1.setText(f"按下确认后，程序将在{config["program_start_time"]}秒内开始")
        self.lb_warning_mouseclick1.setAlignment(Qt.AlignCenter)
        self.lb_warning_mouseclick1.setStyleSheet("#lb_warning_mouseclick1{color:red}")

        self.lb_warning_mouseclick2 = QLabel(self.mouseClick_page)
        self.lb_warning_mouseclick2.setGeometry(90, 220, 380, 30)
        self.lb_warning_mouseclick2.setObjectName("lb_warning_mouseclick2")
        self.lb_warning_mouseclick2.setFont(mouseClick_font2)
        self.lb_warning_mouseclick2.setText(f"请及时在不需要连点时按{config["exit_shortcut"]}退出程序")
        self.lb_warning_mouseclick2.setAlignment(Qt.AlignCenter)
        self.lb_warning_mouseclick2.setStyleSheet("#lb_warning_mouseclick2{color:red}")

        self.pb_confirm_mouseclick = QPushButton("确认", self.mouseClick_page)
        self.pb_confirm_mouseclick.setGeometry(220, 300, 100, 40)
        self.pb_confirm_mouseclick.setObjectName("pb_confirm_mouseclick")
        self.pb_confirm_mouseclick.setFont(mouseClick_font1)
        self.pb_confirm_mouseclick.clicked.connect(self.mouseClick_confirm)

        # 滚轮模拟
        scroll_font1 = QFont()
        scroll_font1.setFamilies(["华文中宋"])
        scroll_font1.setPointSize(12)

        scroll_font2 = QFont()
        scroll_font2.setFamilies(["华文中宋"])
        scroll_font2.setPointSize(14)

        self.cob_scroll = QComboBox(self.scroll_page)
        self.cob_scroll.setGeometry(190, 70, 150, 35)
        self.cob_scroll.addItems(["模拟现实", "持续上滑", "持续下滑"])
        self.cob_scroll.setPlaceholderText("滚轮模拟模式")
        self.cob_scroll.setCurrentIndex(-1)
        self.cob_scroll.setFont(scroll_font1)
        self.cob_scroll.setObjectName("cob_scroll")

        self.lb_warning_scroll1 = QLabel(self.scroll_page)
        self.lb_warning_scroll1.setGeometry(90, 160, 380, 30)
        self.lb_warning_scroll1.setObjectName("lb_warning_scroll1")
        self.lb_warning_scroll1.setFont(scroll_font2)
        self.lb_warning_scroll1.setText(f"按下确认后，程序将在{config["program_start_time"]}秒内开始")
        self.lb_warning_scroll1.setAlignment(Qt.AlignCenter)
        self.lb_warning_scroll1.setStyleSheet("#lb_warning_scroll1{color:red}")

        self.lb_warning_scroll2 = QLabel(self.scroll_page)
        self.lb_warning_scroll2.setGeometry(90, 220, 380, 30)
        self.lb_warning_scroll2.setObjectName("lb_warning_scroll2")
        self.lb_warning_scroll2.setFont(scroll_font2)
        self.lb_warning_scroll2.setText(f"请及时在不需要模拟时按{config["exit_shortcut"]}退出程序")
        self.lb_warning_scroll2.setAlignment(Qt.AlignCenter)
        self.lb_warning_scroll2.setStyleSheet("#lb_warning_scroll2{color:red}")

        self.pb_confirm_scroll = QPushButton("确认", self.scroll_page)
        self.pb_confirm_scroll.setGeometry(220, 300, 100, 40)
        self.pb_confirm_scroll.setObjectName("pb_confirm_scroll")
        self.pb_confirm_scroll.setFont(scroll_font1)
        self.pb_confirm_scroll.clicked.connect(self.scroll_confirm)

        # settings
        # labels
        settings_title_font1 = QFont()
        settings_title_font1.setFamilies(["Lucida Calligraphy"])
        settings_title_font1.setPointSize(18)

        settings_title_font2 = QFont()
        settings_title_font2.setFamilies(["华文中宋"])
        settings_title_font2.setPointSize(12)

        settings_common_font = QFont()
        settings_common_font.setFamilies(["华文中宋"])
        settings_common_font.setPointSize(10)

        self.lb_settings_title = QLabel(self.setting_page)
        self.lb_settings_title.setGeometry(20, 20, 160, 40)
        self.lb_settings_title.setObjectName("lb_settings_title")
        self.lb_settings_title.setFont(settings_title_font1)
        self.lb_settings_title.setText("Settings")

        self.lb_global_settings = QLabel(self.setting_page)
        self.lb_global_settings.setGeometry(20, 70, 120, 30)
        self.lb_global_settings.setObjectName("lb_global_settings")
        self.lb_global_settings.setFont(settings_title_font2)
        self.lb_global_settings.setText("全局设置")

        self.lb_interval_settings = QLabel(self.setting_page)
        self.lb_interval_settings.setGeometry(20, 170, 120, 30)
        self.lb_interval_settings.setObjectName("lb_interval_settings")
        self.lb_interval_settings.setFont(settings_title_font2)
        self.lb_interval_settings.setText("时间间隔")

        self.lb_scroll_settings = QLabel(self.setting_page)
        self.lb_scroll_settings.setGeometry(20, 270, 220, 30)
        self.lb_scroll_settings.setObjectName("lb_scroll_settings")
        self.lb_scroll_settings.setFont(settings_title_font2)
        self.lb_scroll_settings.setText("滚轮模拟设置：持续/模拟")

        self.lb_exit_shortcut = QLabel(self.setting_page)
        self.lb_exit_shortcut.setGeometry(20, 120, 90, 20)
        self.lb_exit_shortcut.setObjectName("lb_exit_shortcut")
        self.lb_exit_shortcut.setFont(settings_common_font)
        self.lb_exit_shortcut.setText("退出快捷键")
        self.lb_exit_shortcut.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.lb_program_start_time = QLabel(self.setting_page)
        self.lb_program_start_time.setGeometry(250, 120, 90, 20)
        self.lb_program_start_time.setObjectName("lb_program_start_time")
        self.lb_program_start_time.setFont(settings_common_font)
        self.lb_program_start_time.setText("程序启动时间")
        self.lb_program_start_time.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.lb_input_interval = QLabel(self.setting_page)
        self.lb_input_interval.setGeometry(20, 220, 90, 20)
        self.lb_input_interval.setObjectName("lb_input_interval")
        self.lb_input_interval.setFont(settings_common_font)
        self.lb_input_interval.setText("模拟输入")
        self.lb_input_interval.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.lb_mouse_click_interval = QLabel(self.setting_page)
        self.lb_mouse_click_interval.setGeometry(250, 220, 90, 20)
        self.lb_mouse_click_interval.setObjectName("lb_mouse_click_interval")
        self.lb_mouse_click_interval.setFont(settings_common_font)
        self.lb_mouse_click_interval.setText("鼠标连点")
        self.lb_mouse_click_interval.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.lb_scroll_constant_interval = QLabel(self.setting_page)
        self.lb_scroll_constant_interval.setGeometry(20, 320, 90, 20)
        self.lb_scroll_constant_interval.setObjectName("lb_scroll_constant_interval")
        self.lb_scroll_constant_interval.setFont(settings_common_font)
        self.lb_scroll_constant_interval.setText("持续/单滑间隔")
        self.lb_scroll_constant_interval.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.lb_scroll_constant_times = QLabel(self.setting_page)
        self.lb_scroll_constant_times.setGeometry(250, 320, 90, 20)
        self.lb_scroll_constant_times.setObjectName("lb_scroll_constant_times")
        self.lb_scroll_constant_times.setFont(settings_common_font)
        self.lb_scroll_constant_times.setText("持续/单滑次数")
        self.lb_scroll_constant_times.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.lb_scroll_random_down_probability = QLabel(self.setting_page)
        self.lb_scroll_random_down_probability.setGeometry(480, 320, 90, 20)
        self.lb_scroll_random_down_probability.setObjectName("lb_scroll_random_down_probability")
        self.lb_scroll_random_down_probability.setFont(settings_common_font)
        self.lb_scroll_random_down_probability.setText("模拟/下滑概率")
        self.lb_scroll_random_down_probability.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.lb_scroll_random_slide_times = QLabel(self.setting_page)
        self.lb_scroll_random_slide_times.setGeometry(20, 370, 90, 20)
        self.lb_scroll_random_slide_times.setObjectName("lb_scroll_random_slide_times")
        self.lb_scroll_random_slide_times.setFont(settings_common_font)
        self.lb_scroll_random_slide_times.setText("模拟/单滑次数")
        self.lb_scroll_random_slide_times.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.lb_scroll_random_slide_interval = QLabel(self.setting_page)
        self.lb_scroll_random_slide_interval.setGeometry(250, 370, 90, 20)
        self.lb_scroll_random_slide_interval.setObjectName("lb_scroll_random_slide_interval")
        self.lb_scroll_random_slide_interval.setFont(settings_common_font)
        self.lb_scroll_random_slide_interval.setText("模拟/单滑间隔")
        self.lb_scroll_random_slide_interval.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.lb_scroll_random_interval = QLabel(self.setting_page)
        self.lb_scroll_random_interval.setGeometry(480, 370, 90, 20)
        self.lb_scroll_random_interval.setObjectName("lb_scroll_random_interval")
        self.lb_scroll_random_interval.setFont(settings_common_font)
        self.lb_scroll_random_interval.setText("模拟/总间隔")
        self.lb_scroll_random_interval.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        # line
        self.line1_settings = QFrame(self.setting_page)
        self.line1_settings.setGeometry(20, 60, 710, 16)
        self.line1_settings.setFrameShape(QFrame.HLine)
        self.line1_settings.setFrameShadow(QFrame.Sunken)

        self.line2_settings = QFrame(self.setting_page)
        self.line2_settings.setGeometry(20, 160, 710, 16)
        self.line2_settings.setFrameShape(QFrame.HLine)
        self.line2_settings.setFrameShadow(QFrame.Sunken)

        self.line3_settings = QFrame(self.setting_page)
        self.line3_settings.setGeometry(20, 260, 710, 16)
        self.line3_settings.setFrameShape(QFrame.HLine)
        self.line3_settings.setFrameShadow(QFrame.Sunken)

        # combo box
        self.cb_exit_shortcut = QComboBox(self.setting_page)
        self.cb_exit_shortcut.setGeometry(120, 110, 110, 35)
        self.cb_exit_shortcut.setObjectName("cb_exit_shortcut")
        self.cb_exit_shortcut.setFont(settings_common_font)
        self.cb_exit_shortcut.addItems(["Esc", "Tab", "F1", "Insert"])
        self.cb_exit_shortcut.setCurrentIndex(self.cb_exit_shortcut.findText(config["exit_shortcut"]))

        self.cb_program_start_time = QComboBox(self.setting_page)
        self.cb_program_start_time.setGeometry(350, 110, 110, 35)
        self.cb_program_start_time.setObjectName("cb_program_start_time")
        self.cb_program_start_time.setFont(settings_common_font)
        self.cb_program_start_time.addItems(["5", "10", "15", "20"])
        self.cb_program_start_time.setCurrentIndex(
            self.cb_program_start_time.findText(str(config["program_start_time"])))

        self.cb_input_interval = QComboBox(self.setting_page)
        self.cb_input_interval.setGeometry(120, 210, 110, 35)
        self.cb_input_interval.setObjectName("cb_input_interval")
        self.cb_input_interval.setFont(settings_common_font)
        self.cb_input_interval.addItems(["0.05", "0.1", "0.2", "0.3"])
        self.cb_input_interval.setCurrentIndex(self.cb_input_interval.findText(str(config["input_interval"])))

        self.cb_mouse_click_interval = QComboBox(self.setting_page)
        self.cb_mouse_click_interval.setGeometry(350, 210, 110, 35)
        self.cb_mouse_click_interval.setObjectName("cb_mouse_click_interval")
        self.cb_mouse_click_interval.setFont(settings_common_font)
        self.cb_mouse_click_interval.addItems(["0.05", "0.1", "0.2", "0.3"])
        self.cb_mouse_click_interval.setCurrentIndex(
            self.cb_mouse_click_interval.findText(str(config["mouseClick_interval"])))

        self.cb_scroll_constant_interval = QComboBox(self.setting_page)
        self.cb_scroll_constant_interval.setGeometry(120, 310, 110, 35)
        self.cb_scroll_constant_interval.setObjectName("cb_scroll_constant_interval")
        self.cb_scroll_constant_interval.setFont(settings_common_font)
        self.cb_scroll_constant_interval.addItems(["0.1", "0.2", "0.3", "0.4"])
        self.cb_scroll_constant_interval.setCurrentIndex(
            self.cb_scroll_constant_interval.findText(str(config["scroll_constant_interval"])))

        self.cb_scroll_constant_times = QComboBox(self.setting_page)
        self.cb_scroll_constant_times.setGeometry(350, 310, 110, 35)
        self.cb_scroll_constant_times.setObjectName("cb_scroll_constant_times")
        self.cb_scroll_constant_times.setFont(settings_common_font)
        self.cb_scroll_constant_times.addItems(["1", "2", "3"])
        self.cb_scroll_constant_times.setCurrentIndex(
            self.cb_scroll_constant_times.findText(str(config["scroll_constant_times"])))

        self.cb_scroll_random_down_probability = QComboBox(self.setting_page)
        self.cb_scroll_random_down_probability.setGeometry(580, 310, 110, 35)
        self.cb_scroll_random_down_probability.setObjectName("cb_scroll_random_down_probability")
        self.cb_scroll_random_down_probability.setFont(settings_common_font)
        self.cb_scroll_random_down_probability.addItems(
            ["0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"])
        self.cb_scroll_random_down_probability.setCurrentIndex(
            self.cb_scroll_random_down_probability.findText(str(config["scroll_random_down_probability"])))

        self.cb_scroll_random_slide_times = QComboBox(self.setting_page)
        self.cb_scroll_random_slide_times.setGeometry(120, 360, 110, 35)
        self.cb_scroll_random_slide_times.setObjectName("cb_scroll_random_slide_times")
        self.cb_scroll_random_slide_times.setFont(settings_common_font)
        self.cb_scroll_random_slide_times.addItems(["[2, 5]", "[3, 6]", "[4, 8]"])
        self.cb_scroll_random_slide_times.setCurrentIndex(
            self.cb_scroll_random_slide_times.findText(str(config["scroll_random_slide_times"])))

        self.cb_scroll_random_slide_interval = QComboBox(self.setting_page)
        self.cb_scroll_random_slide_interval.setGeometry(350, 360, 110, 35)
        self.cb_scroll_random_slide_interval.setObjectName("cb_scroll_random_slide_interval")
        self.cb_scroll_random_slide_interval.setFont(settings_common_font)
        self.cb_scroll_random_slide_interval.addItems(["[0.05, 0.1]", "[0.05, 0.2]", "[0.1, 0.3]"])
        self.cb_scroll_random_slide_interval.setCurrentIndex(
            self.cb_scroll_random_slide_interval.findText(str(config["scroll_random_slide_interval"])))

        self.cb_scroll_random_interval = QComboBox(self.setting_page)
        self.cb_scroll_random_interval.setGeometry(580, 360, 110, 35)
        self.cb_scroll_random_interval.setObjectName("cb_scroll_random_interval")
        self.cb_scroll_random_interval.setFont(settings_common_font)
        self.cb_scroll_random_interval.addItems(["[3, 6]", "[4, 8]", "[5, 10]"])
        self.cb_scroll_random_interval.setCurrentIndex(
            self.cb_scroll_random_interval.findText(str(config["scroll_random_interval"])))

        # pushbutton
        self.pb_back = QPushButton("返回", self.setting_page)
        self.pb_back.setGeometry(20, 500, 100, 40)
        self.pb_back.setObjectName("pb_back")
        self.pb_back.setFont(settings_common_font)
        self.pb_back.clicked.connect(self.back)

        self.pb_default = QPushButton("恢复默认", self.setting_page)
        self.pb_default.setGeometry(140, 500, 100, 40)
        self.pb_default.setObjectName("pb_default")
        self.pb_default.setFont(settings_common_font)
        self.pb_default.clicked.connect(self.default_config)

        self.pb_save = QPushButton("保存设置", self.setting_page)
        self.pb_save.setGeometry(640, 500, 100, 40)
        self.pb_save.setObjectName("pb_save")
        self.pb_save.setFont(settings_common_font)
        self.pb_save.clicked.connect(self.save_config)

    # 关闭窗口
    def keyPressEvent(self, event):
        global config, exit_shortcut
        if event.key() == exit_shortcut[config["exit_shortcut"]]:
            self.close()
            super().keyPressEvent(event)

    # 模拟输入
    # 导入文件
    def update_text(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "导入文本文件", "", "文本文件(*.txt)")
        if file_path:
            if self.pt_input.toPlainText() == "":
                with open(file_path, "r", encoding="utf-8") as f:
                    self.pt_input.setPlainText(f.read())
            else:
                self.msg_cover = QMessageBox().question(self, "提示", "检测到已有文本，是否覆盖当前文本？",
                                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if self.msg_cover == QMessageBox.Yes:
                    with open(file_path, "r", encoding="utf-8") as f:
                        self.pt_input.setPlainText(f.read())
                else:
                    with open(file_path, "r", encoding="utf-8") as f:
                        self.pt_input.appendPlainText(f.read())

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if self.pt_input.toPlainText() != "":
            self.msg_cover = QMessageBox().question(self, "提示", "检测到已有文本，是否覆盖当前文本？",
                                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if self.msg_cover == QMessageBox.Yes:
                self.pt_input.setPlainText("")
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith(".txt"):
                pass
            else:
                self.msg_input = QMessageBox().question(self, "错误", "请导入文本文件", QMessageBox.Yes,
                                                        QMessageBox.Yes)
                return
            with open(file_path, "r", encoding="utf-8") as f:
                self.pt_input.appendPlainText(f.read())

    @Slot()
    def input_confirm(self):
        global config
        self.msg_input = QMessageBox().question(self, "提示",
                                                f"{config["program_start_time"]}秒后开始模拟输入，请点击输入框",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if self.msg_input == QMessageBox.Yes:
            global input_content
            input_content = self.pt_input.toPlainText()
            self.input_thread = InputThread()
            self.input_thread.start()

    # 鼠标连点
    # 设置输入框是否可输入
    def set_le_enabled(self):
        if self.cob_time.currentIndex() == 2:
            self.le_time.setEnabled(True)
        else:
            self.le_time.setEnabled(False)

    @Slot()
    def mouseClick_confirm(self):
        global mouseClick_time
        if self.cob_time.currentIndex() == -1:
            QMessageBox.warning(self, "错误", "请选择持续时间")
            return
        elif self.cob_time.currentIndex() == 0:
            mouseClick_time = 10
        elif self.cob_time.currentIndex() == 1:
            mouseClick_time = 30
        elif self.cob_time.currentIndex() == 2:
            if self.le_time.text() and self.le_time.text().isdigit():
                if int(self.le_time.text()) > 0:
                    mouseClick_time = int(self.le_time.text())
                else:
                    QMessageBox.warning(self, "错误", "请确保输入的持续时间为正整数")
                    return
            else:
                QMessageBox.warning(self, "错误", "请确保输入的持续时间为正整数")
                return
        elif self.cob_time.currentIndex() == 3:
            mouseClick_time = -1
        self.mouseClick_thread = MouseClickThread()
        self.mouseClick_thread.start()

    # 滚轮模拟
    def scroll_confirm(self):
        global scroll_mode
        if self.cob_scroll.currentIndex() == -1:
            QMessageBox.warning(self, "错误", "请选择滚轮模拟模式")
            return
        elif self.cob_scroll.currentIndex() == 0:
            scroll_mode = "real"
        elif self.cob_scroll.currentIndex() == 1:
            scroll_mode = "up"
        elif self.cob_scroll.currentIndex() == 2:
            scroll_mode = "down"
        self.scroll_thread = ScrollThread()
        self.scroll_thread.start()

    # 设置
    def back(self):
        self.cb_exit_shortcut.setCurrentIndex(self.cb_exit_shortcut.findText(str(config["exit_shortcut"])))
        self.cb_program_start_time.setCurrentIndex(
            self.cb_program_start_time.findText(str(config["program_start_time"])))
        self.cb_input_interval.setCurrentIndex(self.cb_input_interval.findText(str(config["input_interval"])))
        self.cb_mouse_click_interval.setCurrentIndex(
            self.cb_mouse_click_interval.findText(str(config["mouseClick_interval"])))
        self.cb_scroll_constant_interval.setCurrentIndex(
            self.cb_scroll_constant_interval.findText(str(config["scroll_constant_interval"])))
        self.cb_scroll_constant_times.setCurrentIndex(
            self.cb_scroll_constant_times.findText(str(config["scroll_constant_times"])))
        self.cb_scroll_random_down_probability.setCurrentIndex(
            self.cb_scroll_random_down_probability.findText(str(config["scroll_random_down_probability"])))
        self.cb_scroll_random_slide_interval.setCurrentIndex(
            self.cb_scroll_random_slide_interval.findText(str(config["scroll_random_slide_interval"])))
        self.cb_scroll_random_slide_times.setCurrentIndex(
            self.cb_scroll_random_slide_times.findText(str(config["scroll_random_slide_times"])))
        self.cb_scroll_random_interval.setCurrentIndex(
            self.cb_scroll_random_interval.findText(str(config["scroll_random_interval"])))
        self.main_stacked_widget.setCurrentIndex(0)
        self.function_stacked_widget.setCurrentIndex(0)

    def default_config(self):
        global config
        with open("config/Default config.json", "r", encoding="utf-8") as f:
            content = json.load(f)
        with open("config/config.json", "w", encoding="utf-8") as f:
            json.dump(content, f)
        with open("config/config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        self.cb_exit_shortcut.setCurrentIndex(self.cb_exit_shortcut.findText(str(config["exit_shortcut"])))
        self.cb_program_start_time.setCurrentIndex(
            self.cb_program_start_time.findText(str(config["program_start_time"])))
        self.cb_input_interval.setCurrentIndex(self.cb_input_interval.findText(str(config["input_interval"])))
        self.cb_mouse_click_interval.setCurrentIndex(
            self.cb_mouse_click_interval.findText(str(config["mouseClick_interval"])))
        self.cb_scroll_constant_interval.setCurrentIndex(
            self.cb_scroll_constant_interval.findText(str(config["scroll_constant_interval"])))
        self.cb_scroll_constant_times.setCurrentIndex(
            self.cb_scroll_constant_times.findText(str(config["scroll_constant_times"])))
        self.cb_scroll_random_down_probability.setCurrentIndex(
            self.cb_scroll_random_down_probability.findText(str(config["scroll_random_down_probability"])))
        self.cb_scroll_random_slide_interval.setCurrentIndex(
            self.cb_scroll_random_slide_interval.findText(str(config["scroll_random_slide_interval"])))
        self.cb_scroll_random_slide_times.setCurrentIndex(
            self.cb_scroll_random_slide_times.findText(str(config["scroll_random_slide_times"])))
        self.cb_scroll_random_interval.setCurrentIndex(
            self.cb_scroll_random_interval.findText(str(config["scroll_random_interval"])))
        self.lb_warning_mouseclick1.setText(f"按下确认后，程序将在{config["program_start_time"]}秒内开始")
        self.lb_warning_mouseclick2.setText(f"请及时在不需要连点时按{config["exit_shortcut"]}退出程序")
        self.lb_warning_scroll1.setText(f"按下确认后，程序将在{config["program_start_time"]}秒内开始")
        self.lb_warning_scroll2.setText(f"请及时在不需要模拟时按{config["exit_shortcut"]}退出程序")

    def save_config(self):
        global config
        config["exit_shortcut"] = self.cb_exit_shortcut.currentText()
        config["program_start_time"] = int(self.cb_program_start_time.currentText())
        config["input_interval"] = float(self.cb_input_interval.currentText())
        config["mouseClick_interval"] = float(self.cb_mouse_click_interval.currentText())
        config["scroll_constant_interval"] = float(self.cb_scroll_constant_interval.currentText())
        config["scroll_constant_times"] = int(self.cb_scroll_constant_times.currentText())
        config["scroll_random_down_probability"] = float(self.cb_scroll_random_down_probability.currentText())
        config["scroll_random_slide_times"] = ast.literal_eval(self.cb_scroll_random_slide_times.currentText())
        config["scroll_random_slide_interval"] = ast.literal_eval(self.cb_scroll_random_slide_interval.currentText())
        config["scroll_random_interval"] = ast.literal_eval(self.cb_scroll_random_interval.currentText())
        with open("config/config.json", "w", encoding="utf-8") as f:
            json.dump(config, f)
        self.lb_warning_mouseclick1.setText(f"按下确认后，程序将在{config["program_start_time"]}秒内开始")
        self.lb_warning_mouseclick2.setText(f"请及时在不需要连点时按{config["exit_shortcut"]}退出程序")
        self.lb_warning_scroll1.setText(f"按下确认后，程序将在{config["program_start_time"]}秒内开始")
        self.lb_warning_scroll2.setText(f"请及时在不需要模拟时按{config["exit_shortcut"]}退出程序")
        self.main_stacked_widget.setCurrentIndex(0)
        self.function_stacked_widget.setCurrentIndex(0)


# 模拟输入线程
class InputThread(QThread):
    def run(self):
        global config
        time.sleep(config["program_start_time"])
        keyboard = pynput.keyboard.Controller()
        global input_content
        for char in input_content:
            if char == '\n':
                keyboard.type('\n')
            else:
                keyboard.press(char)
                keyboard.release(char)
            time.sleep(config["input_interval"])


# 鼠标连点线程
class MouseClickThread(QThread):
    def run(self):
        global mouseClick_time, config
        time.sleep(config["program_start_time"])
        mouse_click = pynput.mouse.Controller()
        current_time = time.time()
        if mouseClick_time == -1:
            while True:
                mouse_click.click(pynput.mouse.Button.left)
                time.sleep(config["mouseClick_interval"])
        else:
            while time.time() - current_time < mouseClick_time:
                mouse_click.click(pynput.mouse.Button.left)
                time.sleep(config["mouseClick_interval"])


# 滚轮模拟线程
class ScrollThread(QThread):
    def __init__(self):
        super().__init__()
        self.stimulated_scroll = None

    def scroll_up(self, times):
        self.stimulated_scroll = pynput.mouse.Controller()
        for _ in range(times):
            self.stimulated_scroll.scroll(0, -1)

    def scroll_down(self, times):
        self.stimulated_scroll = pynput.mouse.Controller()
        for _ in range(times):
            self.stimulated_scroll.scroll(0, 1)

    def run(self):
        global scroll_mode
        time.sleep(5)

        if scroll_mode == "real":
            while True:
                random.seed(time.time())
                if random.randint(1, 10) <= config["scroll_random_down_probability"] * 10:
                    for i in range(random.randint(config["scroll_random_slide_times"][0],
                                                  config["scroll_random_slide_times"][1])):
                        self.scroll_down(1)
                        time.sleep(random.uniform(config["scroll_random_slide_interval"][0],
                                                  config["scroll_random_slide_interval"][1]))
                else:
                    for i in range(random.randint(config["scroll_random_slide_times"][0],
                                                  config["scroll_random_slide_times"][1])):
                        self.scroll_up(1)
                        time.sleep(random.uniform(config["scroll_random_slide_interval"][0],
                                                  config["scroll_random_slide_interval"][1]))
                time.sleep(random.randrange(config["scroll_random_interval"][0],
                                            config["scroll_random_interval"][1]))
        elif scroll_mode == "up":
            while True:
                self.scroll_up(config["scroll_constant_times"])
                time.sleep(config["scroll_constant_interval"])
        elif scroll_mode == "down":
            while True:
                self.scroll_down(config["scroll_constant_times"])
                time.sleep(config["scroll_constant_interval"])


if __name__ == '__main__':
    # 全局变量
    input_content = ""
    mouseClick_time = 0
    scroll_mode = ""
    with open("config/config.json", "r", encoding="utf-8") as file:
        config = json.load(file)
    exit_shortcut = {
        "Esc": Qt.Key_Escape,
        "Tab": Qt.Key_Tab,
        "F1": Qt.Key_F1,
        "Insert": Qt.Key_Insert,
    }

    app = QApplication(sys.argv)
    window = StimulatedElf()
    window.show()
    sys.exit(app.exec())
