# -*- coding: utf-8 -*-
# @Time    : 2020/11/4 17:03
# @Author  : lx
# @IDE ：PyCharm

import win32gui
import win32api
import win32con
import time
import win32clipboard as w

class send_meg():
    def FindWindow(self,chatroom):
        win = win32gui.FindWindow(None, chatroom)
        if win != 0:
            win32gui.ShowWindow(win, win32con.SW_SHOWMINIMIZED)
            win32gui.ShowWindow(win, win32con.SW_SHOWNORMAL)
            win32gui.ShowWindow(win, win32con.SW_SHOW)
            win32gui.SetForegroundWindow(win)  # 获取控制
            time.sleep(0.5)
        else:
            raise ('找不到窗口: %s'%chatroom)
    def setText(self,aString):
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
        w.CloseClipboard()
    def zhanTie(self):
        win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
        win32api.keybd_event(86, 0, 0, 0)  # v键位码是86
        win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    def huiche(self):
        win32api.keybd_event(18, 0, 0, 0)  # Alt键位码
        win32api.keybd_event(83, 0, 0, 0)  # s键位码
        win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
        win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)
    def click(self):
        win32api.SetCursorPos([325, 474])   # 点击的坐标
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    def sendText(self,text):
        self.FindWindow('文件传输助手')
        self.setText(text)
        self.zhanTie()
        self.huiche()
        self.click()

#s=send_meg()
#s.sendText('https://mp.weixin.qq.com/s/l_EPaZghBPysjiAMoc3ttQ')

