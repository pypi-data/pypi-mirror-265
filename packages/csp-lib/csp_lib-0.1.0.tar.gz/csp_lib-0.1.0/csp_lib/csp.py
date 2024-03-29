import winreg
from winreg import HKEY_USERS, HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER, HKEY_CURRENT_CONFIG, HKEY_CLASSES_ROOT
import re

# подключение к ветке реестра
def get_hkey_branch(comp_name, glob_branch, key_name):
    return winreg.OpenKey(winreg.ConnectRegistry(r'\\' + comp_name, glob_branch), key_name, access=winreg.KEY_ALL_ACCESS)


# получаем список ключей в ветке реестра
def get_list(hkey_branch):
    return [winreg.EnumKey(hkey_branch, y) for y in range(winreg.QueryInfoKey(hkey_branch)[0])]


# фильтрация списка ключей в ветке реестра
def filter_list(hkey_branch_key_list, pattern):
    return [i for i in hkey_branch_key_list if re.search(pattern, i)]



# создание новой ветки реестра
def create_new_branch(hkey_branch, new_key_list):
    for i in new_key_list:
        try:
            winreg.OpenKey(hkey_branch, i)
        except FileNotFoundError:
            winreg.CreateKey(hkey_branch, i)
        winreg.CloseKey(hkey_branch)


# получение списка параметров реестра
def get_values_in_branch(hkey_branch):
    return list(winreg.EnumValue(hkey_branch, j) for j in range(winreg.QueryInfoKey(hkey_branch)[1]))


# установка параметров из списка в ветку реестра. Список представляет собой список кортежей формата [(value_name, value_data), (value_name, value_data)]
def copy_values_to_branch(hkey_branch, values_list):
    for i in values_list:
        winreg.SetValueEx(hkey_branch, i[0], 0, winreg.REG_BINARY, i[1])
    winreg.CloseKey(hkey_branch)