from PyQt5.QtCore import Qt, QPoint, QSize, QRect
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QLabel, QApplication, QSizePolicy

# 参考：https://blog.csdn.net/share_account/article/details/130029938

'''
TODO 放大缩小实现跟随
'''
 
class MyLabel(QLabel):
    """图片标签，实现缩放拖拽
    限制条件：
        1. 每次size变化时，图片会重置以自适应缩放显示
        2. 缩小不能小于自适应缩放的尺寸


    Args:
        QLabel (_type_): _description_
    """
    SCALE_RATE = 0.5  # 每次缩放的增量
    SCALE_COUNT = 10  # 可以缩放次数

    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)
        self.setMouseTracking(True)
        # self.setStyleSheet("QLabel { background-color: red; }")
        self.pressed = False
        self.label_drawPoint = QPoint(0, 0)  # label绘图起始位置
        self.curr_scale = 0  # 当前缩放次数

    def setPixmap(self, a0: QPixmap) -> None:
        self.pix = a0
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)  # 防止缩放图片时，size自动变化
        self.img_adaption()
    
    def img_adaption(self):
        """图片自适应缩放
        """
        self.parent_size = None
        view_size = self.size()
        img_size = self.pix.size()

        scale_w = view_size.width() / img_size.width()
        scale_h = view_size.height() / img_size.height()  
        scale = min(scale_w, scale_h, 1)

        new_size = img_size * scale
        offset_x = int((view_size.width() - new_size.width()) / 2)
        offset_y = int((view_size.height() - new_size.height()) / 2)
        self.label_drawPoint = QPoint(offset_x, offset_y) # 居中
        pixmap = self.pix.scaled(new_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        super().setPixmap(pixmap)

        self.scale_value = new_size * self.SCALE_RATE  # 缩放具体数值
        self.curr_scale = 0  # 重置缩放次数
        
    
    def paintEvent(self, event):
        if self.pixmap():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            # 参数：显示起始位置，图片源
            painter.drawPixmap(self.label_drawPoint, self.pixmap())
        
    
    def resizeEvent(self, event):
        super(MyLabel, self).resizeEvent(event)
        if self.pixmap():
            self.img_adaption()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressed = True
            self.m_lastPos = event.pos()
 
    def mouseMoveEvent(self, event):
        if self.pressed:
            delta = event.pos() - self.m_lastPos
            self.m_lastPos = event.pos()
            self.label_drawPoint += delta
            self.update()
 
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressed = False

    def wheelEvent(self, event):
        """鼠标滚轮事件

        滚轮可以放大缩小图片，通过改变改控件的Geometry来实现放大缩小
        缩大缩小过程中会自动调整

        Args:
            event (_type_): _description_
        """
        img_size = self.pixmap().size()
        new_size = None
        
        # 注意：self.pixmap().rect()的位置和实际绘图的不一样
        rect = QRect(self.label_drawPoint, img_size)
        if rect.contains(event.pos()):
            if event.angleDelta().y() > 0:
                if self.curr_scale < self.SCALE_COUNT:
                    new_size = QSize(img_size + self.scale_value)
                    self.curr_scale += 1
            else:
                if self.curr_scale > 0:
                    new_size = QSize(img_size - self.scale_value)
                    self.curr_scale -= 1
                    if self.curr_scale == 0:  # 图片还原，居中显示
                        point = QPoint(int((self.size().width() - new_size.width()) /2), int((self.size().height() - new_size.height()) /2))
                        self.label_drawPoint = point

            if new_size != None:
                pixmap = self.pix.scaled(new_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                super().setPixmap(pixmap)
                # self.update()




if __name__ == "__main__":
    from PyQt5.QtGui import QFocusEvent, QKeyEvent, QFont, QFontMetrics,QPixmap
    from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox, QLabel, QSizePolicy, QGraphicsDropShadowEffect
    from PyQt5.QtCore import Qt, QPoint, QTimerEvent, QRect

    import sys

    from mylabel import MyLabel
    app = QApplication(sys.argv)
    ml = MyLabel()
    pix = QPixmap(r'..\00001.jpg')
    ml.setPixmap(pix)
    ml.show()

    # ml2 = MyLabel()
    # pix = QPixmap(r'..\00002.jpg')
    # ml2.setPixmap(pix)
    # ml2.show()

    sys.exit(app.exec_())
