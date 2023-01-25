import random
import def_for_sending_telegramm
import schedule
import time

time_min = str(random.randint(0, 59))  # Генерируем случайное время в минутах
if len(time_min) == 1:
    time_min = '0' + time_min
time_min = '18:' + time_min

list_user_for_good_night = ['+79XXXXXXX4', '+79XXXXXXX4', '+79XXXXXXX4']  # Аккаунты людей, которым желаю спокойной ночи

def job_that_executes_once(list_user_for_good_night):
    """
    Отправка сообщения сообщения в сгенерированное время
    """
    i = 0
    for item in list_user_for_good_night:
        def_for_sending_telegramm.sending_congratulation_message(list_user_for_good_night[i])
        i = i + 1
    return schedule.CancelJob

schedule.every().day.at(time_min).do(job_that_executes_once,
                                    list_user_for_good_night)  # Функция сработает в 20 часов по серверному времени

while True:
    schedule.run_pending()
    time.sleep(10)