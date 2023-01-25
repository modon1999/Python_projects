"""
Задача: в случайном порятке перетасовать последовательность файлов в папке.
Программа использует в виде входных данных путь до директории который пользователь выбирает через gui,
затем она создает список названий файлов(директории игнорируются) и по количеству элементов создается список имет от
1 до N(где N - количество файлов), затем она переименовывает все файлы в temp_<название_файла>, после чего
последовательно проходится по списку с рандомными именами и в случайном порядке переназывает файлы в директории,
сохраняя расширение.
"""
import random
import tkinter.filedialog
from os import listdir
from os import rename
from os.path import isfile, join
from tkinter import Tk

Tk().withdraw()
directory = tkinter.filedialog.askdirectory()  # получаем путь до директории
if directory[-1] != '/':  # проверяем есть ви в конце пути '/' для будущего обращения к файлам
    directory = directory + '/'
files = [f for f in listdir(directory) if isfile(join(directory, f))]  # создаём список названий файлов
count_files = int(len(files))  # количество файлов в директории
random_names = list(range(1, count_files + 1))  # создаём список названий от 1 до N(где N - количество файлов)

for item in files:  # переименовываем все файлы в формат temp_<название_файла>
    rename(directory + item, directory + 'temp_' + item)

for name in random_names:
    random_elemet = random.randint(0, len(files) - 1)  # выбираем случайное название файла
    file_extension = files[random_elemet]  # создаем расширение файла
    temp_file_extension = ''  # переменная для создания расширения файла
    for letter in file_extension[::-1]:
        if letter == '.':
            break
        else:
            temp_file_extension = letter + temp_file_extension
    if temp_file_extension != file_extension:
        file_extension = '.' + temp_file_extension
    else:  # если разрешения у файла нет, то присваевает ему пустую строку
        file_extension = ''
    rename(directory + 'temp_' + files[random_elemet],
           directory + str(name) + file_extension)  # переименовываем файлы в соответствии с расширением файла
    files.remove(
        files[random_elemet])  # удаляем из списка файл, чтобы больше к нему не обращаться и так пока список не кончится
