import tkinter.filedialog
from os import listdir
from os.path import isfile, join
from tkinter import Tk

from bs4 import BeautifulSoup

Tk().withdraw()
directory = tkinter.filedialog.askdirectory()  # получаем путь до директории
if directory[-1] != '/':  # проверяем есть ви в конце пути '/' для будущего обращения к файлам
    directory = directory + '/'
files = [f for f in listdir(directory) if isfile(join(directory, f))]  # создаём список названий файлов

correspondence_of_the_month_to_the_number = {'Январь': '01', 'Февраль': '02', 'Март': '03', 'Апрель': '04', 'Май': '05',
                                             'Июнь': '06', 'Июль': '07', 'Август': '08', 'Сентябрь': '09',
                                             'Октябрь': '10', 'Ноябрь': '11',
                                             'Декабрь': '12'}  # для замены название месяца, его номером

text = ''  # текст начальный для парсинга
final_text = ''  # финальный текст для записи в текстовый файл

for file in files:  # проходимся по каждому файлу и парсим его
    file = directory + file
    try:  # если в директории есть неподходящие файлы, то пропустит их
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
    except:
        continue
    soup = BeautifulSoup(text, features="lxml")  # объект для парсинга
    content_konf = soup.find('div', {'id': 'content_konf'})  # в этом объекте хранятся все записи о сеансах на странице
    if content_konf == None:  # если такого объекта нет, то пропускает этот файл
        continue
    days_on_page = content_konf.find_all('div', {'class': 'row',
                                                 'style': 'width: 100%;margin-left: 0'})  # в этом объекте хранятся все записи о сеансах за упомянутую в этом объекте дату
    if days_on_page == None:  # если такого объекта нет, то пропускает этот файл
        continue
    days_on_page = list(days_on_page)
    for day in days_on_page:  # проходит по всем дням
        date = day.find('div', {
            'style': 'text-align: center; margin-left: 5%; -moz-transform:rotate(270deg); writing-mode:tb-rl; width: 105px; '})
        if date == None:
            continue
        date = date.text.strip().replace(',', '').split(' ')  # удаляем запятую и превращаем строку в список
        date.pop()  # удаляем день недели
        date[1] = correspondence_of_the_month_to_the_number[date[1]]  # заменяем название месяца на его номер
        date = ".".join(date)  # превращаем списов в обратно строку в формате "dd.MM.YYYY"

        sessions_on_this_day = day.find_all('div', {'class': 'clearfix',
                                                    'style': 'margin-top: 2px'})  # находим все сеансы в этот день
        tmp_final_text = final_text

        for one_session in sessions_on_this_day:  # проходим по всем сеансов в этот день

            session_id_tmp = one_session.get(
                'id')  # получаем id сеанса чтобы понять учавструют ли наши студии в сеансе, так как объект html завязан на id сеанса
            session_id = ''.join([i for i in session_id_tmp if i.isdigit()])  # нам нужны только цифры в id сеанса

            try:  # некоторые сеансы отменяются, в таких случаях данный параметр становится типом None и при попытке забрать атрибут text, выдаёт ошибку, чтобы не учитывать данный сеанс мы его пропускаем
                tech_session = one_session.find('p', {
                    'style': 'font-size: 30px; line-height: 28px;text-align: center; padding-top: 30px;'}).text.strip()  # Находим начало технического сеанса
            except AttributeError:
                continue

            try:  # в сеансах, когда они только запланированы, такого объекта нет, и они нас не интересуют, поэтому пропускаем такие сеансы
                working_session = one_session.find('p', {
                    'style': 'font-size: 30px;text-align: center; line-height: 28px; padding-top: 10px;'}).text.strip()  # Находим начало и конец рабочего сеанса
            except AttributeError:
                continue
            start_working_session = working_session[:5]  # Находим начало рабочего сеанса
            finish_working_session = working_session[8:13]  # Находим конец рабочего сеанса

            name_subscriber = one_session.find('h3').text.strip().replace(' ', '_')  # Находим название абонента

            type_session = one_session.find('p',
                                            {'style': 'font-size: 21px; font-weight: bold; margin-bottom: 5px;'}).find(
                'i').text.strip()  # Находим тип сеанса
            if type_session == 'ЗВС-КВС':
                type_session = 'ЗВС'
            elif type_session == 'ЗВС':
                type_session = 'ЗВС'
            else:
                type_session = 'КВС'

            id_subscriber = 'example4a' + session_id
            session_participants_all = one_session.find('a', {'id': id_subscriber}).get(
                'data-content')  # получив информацию из объекта мы устанавливаем есть ли наши студии в списке
            if 'г. Севастополь' in session_participants_all and 'Республика Крым' in session_participants_all:
                session_participants = 'Севастополь/Республика_Крым'
            elif 'г. Севастополь' in session_participants_all:
                session_participants = 'Севастополь'
            elif 'Республика Крым' in session_participants_all:
                session_participants = 'Республика_Крым'
            else:
                session_participants = None

            second_record_video_session = None  # в случае двух КВС сеансов в двух студиях, во втором модуле это не дописано, поэтому решил реализовать тут, чтобы не менять код в том модуле
            additional_parameters = ''  # Эти параметры используются для передачи типа сеаса и студий учасников в текстовый файл, откуда второй модуль программы запостит это всё в журнал
            if type_session == 'ЗВС' and session_participants == 'Севастополь':
                additional_parameters = ' 1 1 3'
            elif type_session == 'ЗВС' and session_participants == 'Республика_Крым':
                additional_parameters = ' 1 1 2'
            elif type_session == 'КВС' and session_participants == 'Республика_Крым':
                additional_parameters = ' 2 2 2'
            elif type_session == 'КВС' and session_participants == 'Севастополь':
                additional_parameters = ' 2 10 3'
            elif type_session == 'КВС' and session_participants == 'Севастополь/Республика_Крым':
                additional_parameters = ' 2 2 2'
                second_record_video_session = name_subscriber + ' ' + date + ' ' + tech_session + ' ' + start_working_session + ' ' + finish_working_session + ' 2 10 3' + '\n'
            elif type_session == 'ЗВС' and session_participants == 'Севастополь/Республика_Крым':
                additional_parameters = ''

            one_record_video_session = name_subscriber + ' ' + date + ' ' + tech_session + ' ' + start_working_session + ' ' + finish_working_session + additional_parameters + '\n'

            if one_record_video_session in final_text:  # проверка на дублирование записи, из-за того, что иногда на следующей странице первый сеанс повторяет последний сеанс на предыдущей странице
                continue

            if second_record_video_session == None:
                final_text = final_text + one_record_video_session
            else:
                final_text = final_text + one_record_video_session + second_record_video_session

with open('Zapis_uchet_k.txt', 'w+') as f:  # создаем файл с записями для второго модуля программы
    f.write(final_text)
