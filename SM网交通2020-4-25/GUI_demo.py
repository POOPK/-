from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, QRegExp
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QIntValidator, QRegExpValidator
import sys
from Demo import Get_main
from Item_done import ItemDone
import threading as thr


class demo_UI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ZBPR')
        self.setWindowIcon(QIcon(r'.\bitbug_favicon.ico'))
        self.LUI()

    def LUI(self):
        self.button1 = QPushButton('开始')
        self.button2 = QPushButton('关闭')
        self.button3 = QPushButton('分析')

        self.button1.clicked.connect(self.on_clicked_button1)
        self.button2.clicked.connect(self.on_clicked_button2)
        self.button3.clicked.connect(self.on_clicked_button3)

        self.extdit1 = QLineEdit()
        self.extdit2 = QLineEdit()
        self.extdit3 = QLineEdit()
        self.extdit4 = QTextEdit()

        self.extdit1.setPlaceholderText('房间号数')
        self.extdit2.setPlaceholderText('储存位置及名字')
        self.extdit3.setPlaceholderText('打开文件的位置')

        regV1 = QRegExpValidator()
        rrr = QRegExp(r'[1-9]\d\d')
        regV1.setRegExp(rrr)

        self.extdit1.setValidator(regV1)

        layout1 = QGridLayout(self)
        layout1.addWidget(self.extdit1, 0, 0, 1, 1)
        layout1.addWidget(self.extdit2, 1, 0, 1, 6)
        layout1.addWidget(self.extdit3, 2, 0, 1, 6)
        layout1.addWidget(self.extdit3, 3, 0, 1, 6)
        layout1.addWidget(self.button1, 4, 0, 1, 1)
        layout1.addWidget(self.button2, 4, 2, 1, 1)
        layout1.addWidget(self.button3, 4, 1, 1, 1)
        layout1.addWidget(self.extdit4, 5, 0, 1, 6)

    def on_clicked_button1(self):
        # 多线程保证主程序正常运行
        if thr.active_count() <= 5:
            try:
                get_demo = Get_main()
                Thread1 = thr.Thread(target=get_demo.getData, args=(int(self.extdit1.text()), self.extdit2.text()),
                                    name='T1', daemon=True) #daemon为True时主线程结束则所有子线程也结束 守护线程
                Thread1.start()
                self.extdit4.setText('注意:多线程不要选中同一个直播间和同一个文件进行读写\n线程%s已经开始运行\n现存线程数量: %s' % (Thread1.name,thr.active_count()))
            except:
                self.extdit4.setText('错误的位置\n现存线程数量: %s' % (thr.active_count()))
        else:
            self.extdit4.setText('为了安全运行线程数量已到最大\n目前线程数量为%d(包括主线程1)' % thr.active_count())

    def on_clicked_button2(self):
        app = QApplication.instance()
        app.quit()

    def on_clicked_button3(self):
        open_path = r'' + self.extdit3.text()
        try:
            res = str(ItemDone().speaktimes_loc(open_path))
            self.extdit4.setText(res)
            ItemDone().speaktimes_re(open_path)
            ItemDone().speaktimes_time(open_path)
        except:
            self.extdit4.setText('不正确的文件位置或文件已损坏\n现存线程数量: %s' % (thr.active_count()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MW = demo_UI()
    MW.show()
    sys.exit(app.exec_())