from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QResizeEvent, QKeyEvent
from PyQt5.QtCore import Qt

from ui.Ui_img_widget import Ui_img_widget

# TODO 放大时，如果label小于视口，应该放大控件，在控件大小等于视口时，才进行局部放大

class ImgWidget(QWidget, Ui_img_widget):
    def __init__(self, parent=None):
        super(ImgWidget, self).__init__(parent)
        self.setupUi(self)
        self.pix = None
    
    def set_image(self, img_path:str)->None:
        self.pix = QPixmap(img_path)
        self.img_label.setPixmap(self.pix)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        # TODO 改用字典
        try:
            if a0.key() == Qt.Key.Key_Right:
                if self.right_fun:
                    self.right_fun()
            elif a0.key() == Qt.Key.Key_Left:
                if self.left_fun:
                    self.left_fun()
            elif a0.key() == Qt.Key.Key_Up:
                if self.up_fun:
                    self.up_fun()
            elif a0.key() == Qt.Key.Key_Down:
                if self.down_fun:
                    self.down_fun()
            elif a0.key() == Qt.Key.Key_Escape:
                if self.quit:
                    self.quit()
            elif a0.key() == Qt.Key.Key_C:
                if self.key_c:
                    self.key_c()
            elif a0.key() == Qt.Key.Key_1:
                if self.key_1:
                    self.key_1()
            elif a0.key() == Qt.Key.Key_2:
                if self.key_2:
                    self.key_2()
            elif a0.key() == Qt.Key.Key_3:
                if self.key_3:
                    self.key_3()
            elif a0.key() == Qt.Key.Key_4:
                if self.key_4:
                    self.key_4()
            elif a0.key() == Qt.Key.Key_0:
                if self.key_0:
                    self.key_0()
            else:
                print(f'按下按键值: {a0.key()}')
        except Exception as e:
            print(e)
        # super().keyPressEvent(a0)

    def set_right_fun(self, fun)->None:
        self.right_fun = fun

    def set_left_fun(self, fun)->None:
        self.left_fun = fun

    def set_up_fun(self, fun)->None:
        self.up_fun = fun

    def set_down_fun(self, fun)->None:
        self.down_fun = fun
    
    def set_quit_fun(self, fun)->None:
        self.quit = fun

    def set_key_c_fun(self, fun)->None:
        self.key_c = fun

    def set_key_1_fun(self, fun)->None:
        self.key_1 = fun

    def set_key_2_fun(self, fun)->None:
        self.key_2 = fun

    def set_key_3_fun(self, fun)->None:
        self.key_3 = fun

    def set_key_4_fun(self, fun)->None:
        self.key_4 = fun

    def set_key_0_fun(self, fun)->None:
        self.key_0 = fun