# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @File   : proxy.py

from ctypes import windll
import winreg

SETTING_PATH = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"


def _system_proxy(func):
    """系统代理装饰器"""

    def __wrapper(proxy_ip=u"", ignore_ip=u""):
        """
        系统代理设置
        :param proxy_ip: 代理ip
        :param ignore_ip: 忽略的ip
        :return: 开启状态，True开启，False关闭
        """
        internet_setting = winreg.OpenKey(winreg.HKEY_CURRENT_USER, SETTING_PATH, 0, winreg.KEY_ALL_ACCESS)
        internet_set_option = windll.Wininet.InternetSetOptionW

        def _set_key(name, value):
            """
            修改键值
            :param name: 系统键
            :param value: 键值
            """
            _, reg_type = winreg.QueryValueEx(internet_setting, name)
            winreg.SetValueEx(internet_setting, name, 0, reg_type, value)

        return func(_set_key, internet_set_option, proxy_ip, ignore_ip)

    return __wrapper


def system_proxy_status():
    """获取当前代理状态"""
    h_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, SETTING_PATH, 0, winreg.KEY_READ)
    ret_val = winreg.QueryValueEx(h_key, "ProxyEnable")
    ret_ser = winreg.QueryValueEx(h_key, "ProxyServer")
    winreg.CloseKey(h_key)
    return ret_val[0], ret_ser[0]


@_system_proxy
def open_system_proxy(_set_key, internet_set_option, proxy_ip=u"", ignore_ip=u""):
    """开启系统代理"""
    # internet_set_option(0, 37, 0, 0)
    # internet_set_option(0, 39, 0, 0)
    _set_key('ProxyEnable', 1)  # 启用
    if ignore_ip:
        _set_key('ProxyOverride', ignore_ip)  # 忽略的地址
    if proxy_ip:
        _set_key('ProxyServer', proxy_ip)  # 代理IP及端口
    internet_set_option(0, 37, 0, 0)
    internet_set_option(0, 39, 0, 0)
    return False if system_proxy_status()[0] == 0 else system_proxy_status()[1] == proxy_ip


@_system_proxy
def close_system_proxy(_set_key, internet_set_option, proxy_ip="", ignore_ip=""):
    """关闭系统代理"""
    internet_set_option(0, 37, 0, 0)
    internet_set_option(0, 39, 0, 0)
    _set_key('ProxyEnable', 0)  # 停用
    return False if system_proxy_status()[0] == 0 else system_proxy_status()[1] == proxy_ip


if __name__ == '__main__':
    # print(open_system_proxy("127.0.0.1:8080"))
    # print(system_proxy_status())
    # print(close_system_proxy())
    print(system_proxy_status())
