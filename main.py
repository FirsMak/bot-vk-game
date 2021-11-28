import datetime
import time
from threading import Thread
import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import config

from Player import Player

data = config

mute_player_list = []


"""Отправить сообщение в чат"""
def send_chat_msg(chat_id, some_text, attachments=None, keyboard=None):
    post = {
        "chat_id": chat_id,
        "message": some_text,
        "random_id": 0,
    }
    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
    if attachments != None:
        post["attachment"] = attachments
    vk_session.method("messages.send", post)


"""Получить имя отправителя"""
def get_name(user_id):
    user = vk_session.method("users.get", {"user_ids": user_id})
    fullname = user[0]['first_name'] + ' ' + user[0]['last_name']
    print(user)
    return fullname


"""Получаем случайное число"""
def get_random_number():
    number_true = random.randint(data.init_number, data.last_number)
    return number_true


"""Вернуть True если дали ответ"""
def get_is_response(msg_text):
    range_list = [i for i in range(data.init_number, data.last_number+1)]
    print(range_list)
    try:
        if int(msg_text) in range_list:
            return True
        else:
            return False
    except ValueError:
        return False


"""Получить правильное склонение слова попыток"""
def get_ch(attempts):

    ch = " попыток."
    if attempts < 5:
        if attempts < 2:
            ch = str(attempts) + " попытка."
            return ch
        ch = str(attempts) + " попытки."
    else:
        ch = str(attempts) + " попыток."
    return ch

vk_session = vk_api.VkApi(token=data.token)
sesstion_api = vk_session.get_api()
longpool = VkLongPoll(vk_session)

in_game = False # игра началась или нет

number_true = get_random_number() # загаданное число

player = None

def delete_all_data():
    global number_true
    global mute_player_list
    global in_game
    global player
    mute_player_list = []
    player = None
    number_true = get_random_number()
    in_game = False

def main():
    print("spider-man")
    global in_game
    global number_true
    global player
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                if event.from_chat:
                    msg_text = event.text.lower()
                    chat_id = event.chat_id
                    user_id = event.user_id
                    name = get_name(user_id)
                    is_member = sesstion_api.groups.isMember(group_id=data.group_id, user_id=user_id)
                    if not is_member:
                        send_chat_msg(chat_id,
                                      get_name(user_id) +' , мы не можем обработать ваш запрос, пока вы не подпишитесь на нашу группу)')
                    else:
                        if not user_id in mute_player_list:
                                print(str(not user_id in mute_player_list)+"v mute")
                                if not data.admin_disable_game:
                                    print(not data.admin_disable_game)
                                    if in_game:
                                        if user_id == player.user_id:
                                            if get_is_response(msg_text):
                                                if int(msg_text) == number_true:
                                                    player.win()
                                                    send_chat_msg(chat_id, data.get_win_text(name))
                                                    in_game = False
                                                    number_true = get_random_number()
                                                    return
                                                else:
                                                    player.change_attempts(number_true)
                                                    if player.attempts == 0:
                                                        player.lose(datetime.datetime.now())
                                                        send_chat_msg(chat_id, data.get_lose_text(name, number_true))
                                                        mute_player_list.append(player)
                                                        in_game = False
                                                        number_true = get_random_number()
                                                    else:
                                                        send_chat_msg(chat_id, data.get_continue_text(get_ch(player.attempts)))
                                        else:
                                            send_chat_msg(chat_id, data.get_is_game_text())
                                    else:
                                        if msg_text in data.patterns_start:
                                            in_game = True
                                            send_chat_msg(chat_id, data.get_start_text(name))
                                            player = Player(user_id, data.all_attempts)
                                            print(player)
                                else:
                                    delete_all_data()
                    if user_id in data.admins_list:
                        if "/" in msg_text:
                            send_chat_msg(chat_id, data.admin_manager(msg_text))

"""Функция удаляет игроков которые в мьюте больше 10 минут"""
def mute_listener(arg):
    global mute_player_list
    while True:
        if len (mute_player_list) != 0:
            print(mute_player_list)
            now = datetime.datetime.now()
            try:
                for player in mute_player_list:
                    delta = now - player.datetime
                    print(delta.seconds)
                    if delta.seconds > data.time_mute*60:
                        mute_player_list.remove(player)
            except RuntimeError:
                pass
        time.sleep(10)


Thread(target=mute_listener, args=(1,)).start()

main()
