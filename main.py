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
def send_chat_msg(chat_id, some_text, forward_messages=None, reply_to = None):
    post = {
        "chat_id": chat_id,
        "message": some_text,
        "random_id": 0,
    }
    if forward_messages != None:
        post["forward_messages"] = forward_messages

    if reply_to != None:
        post["reply_to"] = reply_to
    vk_session.method("messages.send", post)


"""Отправить сообщение пользователю вк"""
def send_some_msg(user_id, some_text,  forward_messages=None, reply_to = None):
    post = {
        "user_id": user_id,
        "message": some_text,
        "random_id": 0,
    }
    if forward_messages != None:
        post["forward_messages"] = forward_messages

    if reply_to != None:
        post["reply_to"] = reply_to
    vk_session.method("messages.send", post)



"""Закрепить сообщение"""
def pin_chat_msg(message_id, peer_id):
    post = {
        "peer_id": peer_id,
        "message_id": message_id,
        #"conversation_message_id": conversation_message_id,
    }
    print("Сообщение закреплено")
    vk_session.method("messages.pin", post)


"""Получить имя отправителя"""
def get_name(user_id):
    user = vk_session.method("users.get", {"user_ids": user_id})
    fullname = user[0]['first_name'] + ' ' + user[0]['last_name']
    return fullname


"""Получаем случайное число"""
def get_random_number():
    number_true = random.randint(data.init_number, data.last_number)
    range_list = [i for i in range(data.init_number, data.last_number + 1)]
    print(range_list)
    return number_true


"""Вернуть True если дали ответ"""
def get_is_response(msg_text):
    range_list = [i for i in range(data.init_number, data.last_number+1)]
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


def add_player_mute_list(player):
    if not int(player.user_id) in data.admins_list:
        print("от не админа")
        mute_player_list.append(player)
    else:
        print("от админа")


def main():
        while True:
            try:
                print("Подключение установлено vk_side")
                global in_game
                global number_true
                global player
                for event in longpool.listen():
                    if event.from_chat:
                        if event.type == VkEventType.MESSAGE_NEW:
                            msg_text = event.text.lower()
                            chat_id = event.chat_id
                            message_id = event.message_id
                            peer_id = event.peer_id
                            if event.to_me:
                                    user_id = event.user_id
                                    name = get_name(user_id)
                                    is_member = sesstion_api.groups.isMember(group_id=data.group_id, user_id=user_id)
                                    if not is_member:
                                        send_chat_msg(chat_id,
                                                      get_name(user_id) +' , мы не можем обработать ваш запрос, пока вы не подпишитесь на нашу группу)', reply_to=message_id)
                                    else:
                                        if not user_id in mute_player_list:
                                                if not data.admin_disable_game:
                                                    print("Game: " + str(in_game))
                                                    if in_game:
                                                        if user_id == player.user_id:
                                                            if get_is_response(msg_text):
                                                                if int(msg_text) == number_true:
                                                                    """Если игрок выйграл"""
                                                                    player.win()
                                                                    send_chat_msg(chat_id, data.get_win_text(name), reply_to=message_id)
                                                                    in_game = False
                                                                    number_true = get_random_number()
                                                                else:
                                                                    player.change_attempts(number_true)
                                                                    if player.attempts == 0:
                                                                        """Если игрок проиграл"""
                                                                        player.lose(datetime.datetime.now())
                                                                        send_chat_msg(chat_id, data.get_lose_text(name, number_true), reply_to=message_id)
                                                                        add_player_mute_list(player)
                                                                        in_game = False
                                                                        number_true = get_random_number()
                                                                    else:
                                                                        send_chat_msg(chat_id, data.get_continue_text(get_ch(player.attempts)), reply_to=message_id)
                                                        else:
                                                            if msg_text in data.patterns_start:
                                                                send_chat_msg(chat_id, data.get_is_game_text(), reply_to=message_id)
                                                    else:
                                                        print("Обрабатываем игрока")
                                                        if msg_text in data.patterns_start:
                                                            in_game = True
                                                            send_chat_msg(chat_id, data.get_start_text(name))
                                                            player = Player(user_id, data.all_attempts)
                                                else:
                                                    delete_all_data()
                                    if user_id in data.admins_list:
                                        if "/" in msg_text:
                                            send_chat_msg(chat_id, data.admin_manager(msg_text))
                                            number_true = get_random_number()
                            else:
                                if data.text_win in msg_text:
                                    pin_chat_msg(message_id, peer_id)
                                    for admin_id in data.admins_list:
                                        send_some_msg(admin_id,"Победитель.", forward_messages=[message_id])
            except Exception:
                print("Переподключение vk_side")
                time.sleep(60)

"""Функция удаляет игроков которые в мьюте"""
def mute_listener(arg):
    while True:
        global mute_player_list
        if len (mute_player_list) != 0:
            print("игроки в мьюте" + mute_player_list)
            now = datetime.datetime.now()
            try:
                for player in mute_player_list:
                    delta = now - player.datetime
                    print(delta.seconds)
                    if delta.seconds > data.time_mute*60:
                        mute_player_list.remove(player)
            except RuntimeError:
                print("Runtime error")
                pass
        time.sleep(10)


Thread(target=mute_listener, args=(1,)).start()

print("spider-man")
main()
