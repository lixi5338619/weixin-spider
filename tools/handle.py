# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @File   : handle.py
import win32clipboard
import win32gui
import win32api
import time
import win32con
from exceptions import HandleDoseNotExistError


class CheckHandle:

    @staticmethod
    def check_handle(self_func):
        def __wrapper(myself, *args, **kwargs):
            myself.handle = win32gui.FindWindow(myself.classname, myself.title)
            if myself.handle == 0:
                raise HandleDoseNotExistError(f"{myself.title}窗口不存在{myself.classname}")
            # win32gui.ShowWindow(myself.handle, win32con.SW_SHOWDEFAULT)
            win32gui.SetForegroundWindow(myself.handle)     # 获取窗口
            # win32gui.ShowWindow(myself.handle, win32con.SW_HIDE)
            myself.rect = win32gui.GetWindowRect(myself.handle)
            return self_func(myself, *args, **kwargs)

        return __wrapper

    @staticmethod
    def has_handle(classname, title):
        return win32gui.FindWindow(classname, title) != 0

    @staticmethod
    def handle(classname, title):
        return win32gui.FindWindow(classname, title)


class HandleModel:

    @staticmethod
    def text_to_clipboard(string: str, encoding='gbk'):
        """写入剪切板"""
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_TEXT, string.encode(encoding=encoding))
        win32clipboard.CloseClipboard()

    @staticmethod
    def mouse_right_click_position(handle, rect_position: tuple):
        """鼠标右点击"""
        # 将两个16位的值连接成一个32位的地址坐标
        long_position = win32api.MAKELONG(*rect_position)
        # 点击左键
        win32api.SendMessage(handle, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, long_position)
        win32api.SendMessage(handle, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, long_position)

    @staticmethod
    def mouse_left_click_position(handle, rect_position: tuple):
        """鼠标左点击"""
        # win32api.SetCursorPos(rect_position)
        # 将两个16位的值连接成一个32位的地址坐标
        long_position = win32api.MAKELONG(*rect_position)
        # print(long_position, "long_position", rect_position)
        # 点击左键
        win32api.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
        win32api.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)

    @staticmethod
    def handle_size(rect: tuple):
        return tuple(abs(x - y) for x, y in zip(rect[:2], rect[2:]))

    # def


class WeChatWnd:
    """微信聊天句柄"""
    check_handle = CheckHandle()
    handle_model = HandleModel()

    def __init__(self, title: str, classname: str = "ChatWnd"):
        self.title = title
        self.classname = classname
        self.handle = 0
        self.rect = (0, 0, 0, 0)

    @property
    def handle_size(self):
        return tuple(abs(x - y) for x, y in zip(self.rect[:2], self.rect[2:]))

    @check_handle.check_handle
    def send_msg(self, msg: str):
        self.handle_model.text_to_clipboard(msg)
        rect_position = (200, self.handle_size[1] - 50)
        win32api.SetCursorPos(rect_position)
        self.handle_model.mouse_right_click_position(self.handle, rect_position)
        time.sleep(0.001)
        CMenuWnd().click_menu_wnd()
        time.sleep(0.1)
        #self.handle_model.mouse_left_click_position(self.handle, (30, 15))
        time.sleep(0.001)
        self.handle_model.mouse_left_click_position(self.handle, (self.handle_size[0] - 60, self.handle_size[1] - 15))
        time.sleep(0.1)

        # 新增click操作
        win32api.SetCursorPos([325, 474])
        time.sleep(0.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.5)

    def hidden(self):
        win32gui.ShowWindow(self.handle, win32con.SW_HIDE)

    @check_handle.check_handle
    def click_last_msg(self):
        handle_size = self.handle_model.handle_size(self.rect)
        print(handle_size)
        # print(handle_size, handle_size[0] // 2)
        self.handle_model.mouse_left_click_position(self.handle, (handle_size[0] // 2, 450))
        # print(WeChatWebViewWnd().handle_id())

    @staticmethod
    def close_web():
        WeChatWebViewWnd().close_web()


class CMenuWnd:
    """微信对话框粘贴板"""
    check_handle = CheckHandle()
    handle_model = HandleModel()

    def __init__(self, title: str = "", classname: str = "CMenuWnd"):
        self.title = title
        self.classname = classname
        self.handle = 0
        self.rect = (0, 0, 0, 0)

    @check_handle.check_handle
    def click_menu_wnd(self, t_position: int = 15):
        # print(self.handle, "CMenuWnd", self.rect)
        # win32api.SetCursorPos(self.rect)
        win32api.SetCursorPos((self.rect[0] + 30, self.rect[1] + 15))
        time.sleep(0.1)
        self.handle_model.mouse_left_click_position(self.handle, (30, t_position))
        time.sleep(0.1)


class ToastWnd:
    """空白信息提示"""
    check_handle = CheckHandle()

    def __init__(self, title: str = "", classname: str = "ToastWnd"):
        self.title = title
        self.classname = classname
        self.handle = 0
        self.rect = (0, 0, 0, 0)

    def has_toast(self):
        return self.check_handle.has_handle(self.classname, self.title)


class WeChatWebViewWnd:
    """内置浏览器"""
    check_handle = CheckHandle()
    handle_model = HandleModel()

    def __init__(self, title: str = "微信", classname: str = "CefWebViewWnd"):
        self.title = title
        self.classname = classname
        self.handle = 0
        self.rect = (0, 0, 0, 0)

    @check_handle.check_handle
    def handle_id(self):
        return self.handle

    @check_handle.check_handle
    def close_web(self, offset: int = 1):
        handle_size = self.handle_model.handle_size(self.rect)
        self.handle_model.mouse_left_click_position(self.handle, (handle_size[0] - offset, offset))


class ChromeWidgetWin0:
    """内置浏览器渲染主体父窗"""
    check_handle = CheckHandle()
    handle_model = HandleModel()

    def __init__(self, title: str = "", classname: str = "Chrome_WidgetWin_0"):
        self.title = title
        self.classname = classname
        self.handle = 0
        self.rect = (0, 0, 0, 0)

    def has_chrome_render(self):
        return self.check_handle.has_handle(self.classname, self.title)


class ChromeRenderWidgetHostHWND:
    """内置浏览器渲染主体"""
    check_handle = CheckHandle()
    handle_model = HandleModel()

    def __init__(self, title: str = "Chrome Legacy Window", classname: str = "Chrome_RenderWidgetHostHWND"):
        self.title = title
        self.classname = classname
        self.handle = 0
        self.rect = (0, 0, 0, 0)

    def has_chrome_render(self):
        return self.check_handle.has_handle(self.classname, self.title)


class FiddlerStartHandler:
    check_handle = CheckHandle()
    handle_model = HandleModel()

    def __init__(self, title: str = "Starting Fiddler...",
                 classname: str = "WindowsForms10.Window.8.app.0.2bf8098_r6_ad1"):
        self.title = title
        self.classname = classname
        self.handle = 0
        self.rect = (0, 0, 0, 0)

    def has_fiddler(self):
        self.handle = self.check_handle.handle(self.classname, self.title)
        return self.check_handle.has_handle(self.classname, self.title)


class FiddlerHandle:
    check_handle = CheckHandle()
    handle_model = HandleModel()

    def __init__(self, title: str = "Progress Telerik Fiddler Web Debugger",
                 classname: str = "WindowsForms10.Window.8.app.0.2bf8098_r6_ad1"):
        self.title = title
        self.classname = classname
        self.handle = 0
        self.rect = (0, 0, 0, 0)

    def has_fiddler(self):
        self.handle = self.check_handle.handle(self.classname, self.title)
        return self.check_handle.has_handle(self.classname, self.title)


class Fiddler:
    fiddler_handle = FiddlerHandle()
    fiddler_start_handle = FiddlerStartHandler()

    def __init__(self, exe_name: str = "Fiddler.exe"):
        self.exe_name = exe_name

    def startup(self, timeout=5):
        if not self.fiddler_handle.has_fiddler():
            win32api.ShellExecute(0, 'open', self.exe_name, '', '', 1)
        s_time = time.time()
        while not self.fiddler_start_handle.has_fiddler() and not self.fiddler_handle.has_fiddler():
            if time.time() - s_time > timeout * 1.0:
                raise TimeoutError("启动超时")
            time.sleep(0.001)

    def shutdown(self, timeout=5):
        # if self.fiddler_start_handle.has_fiddler():
        #     win32api.SendMessage(self.fiddler_start_handle.handle, win32con.WM_CLOSE, 0, 0)
        #     s_time = time.time()
        #     while not self.fiddler_handle.has_fiddler():
        #         if time.time() - s_time > timeout * 1.0:
        #             break
        #         time.sleep(0.001)

        if self.fiddler_handle.has_fiddler():
            time.sleep(0.1)
            win32api.SendMessage(self.fiddler_handle.handle, win32con.WM_CLOSE, 0, 0)


if __name__ == '__main__':
    #wx_chat = WeChatWnd("文件传输助手")
    #wx_chat.send_msg("https://mp.weixin.qq.com/s/l_EPaZghBPysjiAMoc3ttQ")
    #wx_chat.click_last_msg()
    pass
