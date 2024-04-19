from PyQt5.QtGui import QFocusEvent, QKeyEvent, QFont, QFontMetrics
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox, QLabel, QSizePolicy, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QPoint, QTimerEvent, QRect
import pyperclip

import sys
import os

from ui.Ui_main import Ui_Dialog
from view.img_widget import ImgWidget
from logic import Comiclogic


class MainPage(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(MainPage, self).__init__(parent)
        self.setupUi(self)

        self.init_ui()
        self.init_event()

        # self.setFocusPolicy(Qt.StrongFocus) # 获取焦点，可以接受Esc，空格，回车等事件

    def init_ui(self):
        self.setWindowTitle('禁漫浏览器')
        self.comic_dir = r'D:\禁漫天堂\data\禁漫天堂\下载中'
        self.lineEdit_comic_dir.setText(self.comic_dir)

    def init_event(self):
        self.pushButton_comic_dir.clicked.connect(self.btn_event_clicked_comic)
        self.pushButton_start.clicked.connect(self.start)

    def btn_event_clicked_comic(self):
        """按钮事件，打开选择文件夹
        """
        dir = self.open_dir(self.comic_dir)
        if dir:
            self.comic_dir = dir
            self.lineEdit_comic_dir.setText(self.comic_dir)


    def open_dir(self, directory: str = ''):
        """弹窗选择目录

        Args:
            directory (str, optional): 显示的默认目录. Defaults to ''.

        Returns:
            _type_: 返回选择的目录路径，取消返回空字符串
        """
        return QFileDialog.getExistingDirectory(directory=directory)
    
    def get_comboBox_static(self):
        data = {
            "全选": None,
            "下载中": 0,
            "未整理": 1,
            "通过": 2,
            "黑名单": 3,
            "收藏": 4,
        }
        text = self.comboBox_static.currentText()
        if text in data:
            return data[text]
        return None
    
    def get_comboBox_sort(self):
        data = {
            "不排序": None,
            "升序": True,
            "降序": False,
        }
        text = self.comboBox_sort.currentText()
        if text in data:
            return data[text]
        return None

    def start(self):
        if (not self.comic_dir) or (not os.path.isdir(self.comic_dir)):
            self.error_dir()
            return
        try:
            filter = {'tag': self.lineEdit_tag.text(),
                      'static': self.get_comboBox_static(),
                      'isAsc': self.get_comboBox_sort(),
                      'search': self.lineEdit_search.text()}
            self.comic_logic = Comiclogic(self.comic_dir, filter)
        except Exception as e:
            print(f'func:start {e}')
            MessageLabel(self).info(str(e), 1000)
            return
        self.hide()
        self.img_widget = ImgWidget()
        self.img_widget.show()
        self.img_widget.set_right_fun(self.next_img)
        self.img_widget.set_left_fun(self.previous_img)
        self.img_widget.set_key_0_fun(self.set_comic_download)
        self.img_widget.set_key_1_fun(self.set_comic_ready)
        self.img_widget.set_key_2_fun(self.set_comic_pass)
        self.img_widget.set_key_3_fun(self.set_comic_backlist)
        self.img_widget.set_key_4_fun(self.set_comic_like)
        self.img_widget.set_quit_fun(self.close_img_widget)
        self.img_widget.set_key_c_fun(self.write_dir_perclip)
        self.img_widget.set_up_fun(self.previous_comic)
        self.img_widget.set_down_fun(self.next_comic)

        self.img_widget_set_img(self.comic_logic.curr_file())

    def img_widget_set_img(self, file: str):
        """自定义控件中设置图片

        Args:
            file (str): 图片路径
        """
        if self.comic_logic:
            self.img_widget.setWindowTitle(self.comic_logic.info())
        if file and os.path.exists(file):
            self.img_widget.set_image(file)
    
    def set_comic_status(self, status:int):
        txt = {0:'添加到 未下载',
               1:'添加到 未整理',
               2:'添加到 通过',
               3:'添加到 黑名单',
               4:'添加到 收藏',
               }
        self.comic_logic.set_status_pass(status)
        self.img_widget.setWindowTitle(self.comic_logic.info())
        MessageLabel(self.img_widget).info(txt[status], 1000)

    def close_img_widget(self):
        self.show()
        self.img_widget.close()
        del self.comic_logic

    def next_img(self):
        self.img_widget_set_img(self.comic_logic.next())

    def previous_img(self):
        self.img_widget_set_img(self.comic_logic.previous())

    def set_comic_download(self):
        self.set_comic_status(0)

    def set_comic_ready(self):
        self.set_comic_status(1)

    def set_comic_pass(self):
        self.set_comic_status(2)

    def set_comic_backlist(self):
        self.set_comic_status(3)

    def set_comic_like(self):
        self.set_comic_status(4)

    def write_dir_perclip(self):
        """标题赋值到剪切板
        """
        pyperclip.copy(self.comic_logic.get_comic_title())
    
    def previous_comic(self):
        self.img_widget_set_img(self.comic_logic.previous_comic())

    def next_comic(self):
        self.img_widget_set_img(self.comic_logic.next_comic())

    def error_dir(self):
        QMessageBox.warning(self, '错误', '目录不存在', QMessageBox.StandardButton.Ok)

    # def keyPressEvent(self, a0: QKeyEvent) -> None:
    #     qDebug(f"{a0.text()} , {a0.key()} , {a0.nativeVirtualKey()}")
    #     super().keyPressEvent(a0)

    # def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
    #     if a1.type() == QEvent.KeyPress:
    #         print(a1.key())
    #         return True
    #     return super().eventFilter(a0, a1)


class MessageLabel(QLabel):

    def timerEvent(self, a0: QTimerEvent) -> None:
        """定时器触发时间

        Args:
            a0 (QTimerEvent): _description_
        """
        # 清空定时器，关闭自身
        self.killTimer(self.timer_id)
        self.close()

    def info(self, text: str, ms: int):
        """显示消息提示，数秒后消失

        Args:
            text (str): 显示文本
            ms (int): 毫秒
        """
        self.setText(text)
        self.timer_id = super().startTimer(ms)
        self.setStyleSheet("""  
            QLabel {  
                border: 1px solid rgb(118,118,118);
                border-radius:5px; /*圆角*/
                background-color: rgb(255, 255, 255); 
                padding: 0px;
            }  
        """)
        font = QFont()
        font.setPointSize(14)
        self.setFont(font)
        self.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=25, xOffset=0, yOffset=0))  # 标签添加阴影
        self.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # 自适应字体大小
        padding = 10
        metrics = QFontMetrics(self.font())
        size = metrics.boundingRect(QRect(), Qt.AlignLeft, self.text()).size()
        self.setFixedSize(size.width() + padding, size.height() + padding)

        # TODO 处理消息比父控件大的问题
        # 调整在父控件的位置
        p_size = self.parent().size()
        self.move((p_size.width() - size.width() - padding) // 2,  # 水平居中
                  p_size.height() - size.height() - padding - 10)  # 底部往上10


def get_dir_content(dir: str, mode: str = 'all') -> list:
    '''获取目录下所有文件
    paramete: dir 指定的目录
    mode: mode 'file' 读取文件 ，'dir' 读取目录，其他读取文件和目录
    '''
    ret_list = []
    for i in os.listdir(dir):
        path = os.path.abspath(os.path.join(dir, i))
        if (mode == 'file' and os.path.isfile(path)) or (mode == 'dir' and os.path.isdir(path)):
            ret_list.append(path)
        elif mode != 'file' and mode != 'dir':
            ret_list.append(path)

    return ret_list


def get_dir_content_g(dir: str, mode: str = 'all'):
    '''获取目录下所有文件
    paramete: dir 指定的目录
    paramete: mode 'file' 读取文件 ，'dir' 读取目录，其他读取文件和目录
    Return: 生成器，可以配合for使用
    '''
    for i in os.listdir(dir):
        path = os.path.abspath(os.path.join(dir, i))
        if (mode == 'file' and os.path.isfile(path)) or (mode == 'dir' and os.path.isdir(path)):
            yield path
        elif mode != 'file' and mode != 'dir':
            yield path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mp = MainPage()
    mp.show()
    sys.exit(app.exec_())
