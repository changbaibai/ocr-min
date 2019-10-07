# -*- coding: utf-8 -*-
import urllib.request, urllib.parse
import  io, sys, json, socket
import base64
from pynput.keyboard import Listener
from PIL import ImageGrab
socket.setdefaulttimeout(30)
import pyperclip
# 从PyQt库导入QtWidget通用窗口类,基本的窗口集在PyQt5.QtWidgets模块里.
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QAction, QMenu,  QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication

def on_press(key):
    try:
        print("正在按压:", format(key.char))
    except AttributeError:
        # print("正在按压:", format(key))
        if format(key)=='Key.space':
            # print(233)
            ocr_clipboard()
    # 识别逻辑
def get_auth():
        apikey = 'ITOQAuZHCipDKPlXpbM2KyW7'
        secret_key = 'ewuoybwn1YfQE6vtvH8UFkaFYf3Soppk'
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
            apikey, secret_key)
        req = urllib.request.Request(host)
        req.add_header('Content-Type', 'application/json; charset=UTF-8')
        res = urllib.request.urlopen(req)
        content = res.read()

        if (content):
            o = json.loads(content.decode())
            return o['access_token']
        return None
def ocr_clipboard():
        im = ImageGrab.grabclipboard()
        if im is None:
            return None
        #     # self.msg_box = QMessageBox(QMessageBox.Warning, "提示", "《没有复制图片，__v_v__》")
        #     # self.msg_box =" 提示", "《没有复制图片，__v_v__》"
        #     # self.msg_box.show()
        #     QMessageBox.information(self, "标题", "我很喜欢学习python",
        #                             QMessageBox.Yes)
        #     return
        else:
            # print('image size: %sx%s\n' % (im.size[0], im.size[1]))
            mf = io.BytesIO()
            im.save(mf, 'JPEG')
            mf.seek(0)
            buf = mf.read()
            b64 = base64.encodebytes(buf)
            access_token = get_auth()
            if access_token is not None:
                url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=%s' % access_token
                data = urllib.parse.urlencode({'image': b64}).encode()
                req = urllib.request.Request(url, method='POST')
                req.add_header('Content-Type', 'application/x-www-form-urlencoded')
                with urllib.request.urlopen(req, data) as p:
                    res = p.read().decode('utf-8')
                    o = json.loads(res)
                    file_write_obj = open(r'text1.txt', 'w')
                    if o['words_result'] is not None:
                        for w in o['words_result']:
                            file_write_obj.writelines(w['words'])
                            file_write_obj.write('\n')
                            # print(w['words'])
                        file_write_obj.close()

            f = open(r'text1.txt', 'r')
            content = f.read()
            if content is None:
                content = "没有复制图片！"
            pyperclip.copy(content)



# 开始监听
def start_listen():
    with Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == '__main__':
    # pyqt窗口必须在QApplication方法中使用
    # 每一个PyQt5应用都必须创建一个应用对象.sys.argv参数是来自命令行的参数列表.Python脚本可以从shell里运行.这是我们如何控制我们的脚本运行的一种方法.
    app = QApplication(sys.argv)
    # 关闭所有窗口,也不关闭应用程序
    QApplication.setQuitOnLastWindowClosed(False)

    # QWidget窗口是PyQt5中所有用户界口对象的基本类.我们使用了QWidget默认的构造器.默认的构造器没有父类.一个没有父类的窗口被称为一个window.
    w = QWidget()
    # resize()方法调整了窗口的大小.被调整为250像素宽和250像素高.
    w.resize(250, 250)
    # move()方法移动了窗口到屏幕坐标x=300, y=300的位置.
    w.move(300, 300)
    # 在这里我们设置了窗口的标题.标题会被显示在标题栏上.
    w.setWindowTitle('Simple')

    # 在系统托盘处显示图标
    tp = QSystemTrayIcon(w)
    tp.setIcon(QIcon('image/22.png'))
    # 设置系统托盘图标的菜单
    a1 = QAction('&显示(Show)', triggered=w.show)


    def quitApp():
        w.show()  # w.hide() #隐藏
        re = QMessageBox.question(w, "提示", "退出系统", QMessageBox.Yes |
                                  QMessageBox.No, QMessageBox.No)
        if re == QMessageBox.Yes:
            # 关闭窗体程序
            QCoreApplication.instance().quit()
            # 在应用程序全部关闭后，TrayIcon其实还不会自动消失，
            # 直到你的鼠标移动到上面去后，才会消失，
            # 这是个问题，（如同你terminate一些带TrayIcon的应用程序时出现的状况），
            # 这种问题的解决我是通过在程序退出前将其setVisible(False)来完成的。
            tp.setVisible(False)


    a2 = QAction('&退出(Exit)', triggered=quitApp)  # 直接退出可以用qApp.quit

    tpMenu = QMenu()
    tpMenu.addAction(a1)
    tpMenu.addAction(a2)
    tp.setContextMenu(tpMenu)
    # 不调用show不会显示系统托盘
    tp.show()

    # 信息提示
    # 参数1：标题
    # 参数2：内容
    # 参数3：图标（0没有图标 1信息图标 2警告图标 3错误图标），0还是有一个小图标
    tp.showMessage('使用说明', '用QQ完成截图或是复制图片，按空格键完成文字识别，并且完成将文字复制在剪切板', icon=0)
    start_listen()


    def message():

        print("弹出的信息被点击了")


    tp.messageClicked.connect(message)


    def act(reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or  reason == 1:




            print("系统托盘的图标被点击了")


    tp.activated.connect(act)

    # sys为了调用sys.exit(0)退出程序
    # 最后,我们进入应用的主循环.事件处理从这里开始.主循环从窗口系统接收事件,分派它们到应用窗口.如果我们调用了exit()方法或者主窗口被销毁,则主循环结束.sys.exit()方法确保一个完整的退出.环境变量会被通知应用是如何结束的.
    # exec_()方法是有一个下划线的.这是因为exec在Python中是关键字.因此,用exec_()代替.
    sys.exit(app.exec_())
