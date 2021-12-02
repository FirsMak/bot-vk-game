import access as access

token = access.token
group_id = access.token

chat_id = 1

all_attempts = 1 # количество попыток

award = 100

admin_disable_game = False # если админ запретил, то игры не будет

patterns_start = ["/start"]
pattern_help = "/help"

pattern_admin_disable_game = "/disable-game"  # Никто не может играть в игру
pattern_admin_change_attempts = "/set-attempts" # Устанавливает количество попыток у игрока
pattern_admin_change_time_mute = "/set-time-mute" # Устанавливает время мьюта в минутах
pattern_admin_change_init_number = "/set-init-number" # Устанавливает число от которого выбираеться рандомное число
pattern_admin_change_last_number = "/set-last-number" # Устанавливает число до которого выбираеться рандомное число
pattern_admin_change_award = "/set-award" # Устанавливает размер приза в рублях


time_mute = 15 # насколько минут мьютить игрока

init_number = 1
last_number = 20

admins_list = access.admins_list

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

def get_start_text(name):
    return "☑ Игрок " + name + " начал игру. У вас "+get_ch(all_attempts)+"\n💡 Ваша задача заключается в том, чтобы угадать правильное число от " + str(init_number) + " до " + str(last_number) + ". "+"\n✅ Если вы угадаете, то получите деньги.\n✏ Чтобы дать свой ответ, нужно написать число."

def get_lose_text(name, number_true):
    stop_text = "❌ Ответ неверный. Игрок " + name + " будет заблокирован на " + str(time_mute) +" мин. Правильный ответ: " + str(number_true)
    return stop_text

def get_continue_text(atempts):
    stop_text = "❌ Ответ неверный. У вас осталось " + str(atempts)
    return stop_text

text_win = " угадал число."
def get_win_text(name):
    win_text = "✅ Игрок " + name + text_win
    return win_text

def get_is_game_text():
    return "⚠ В беседе уже проводится игра."

def get_help_text():
    return "⚠Чтобы запустить игру отправьте команду " + str(patterns_start[0]) + "\n\nЗатем число, чтобы дать ответ.\n\nУсловие: бот загадывает случайное число от " + str(init_number)+" до "+str(last_number)+". Вам нужно угадать это число.\n\nСтавки: в случае успеха вы получаете приз " + str(award) +"₽. В случае провала — мьют на " + str(time_mute) + " мин."

def admin_manager(msg_text):
    global admin_disable_game
    global number_players
    global all_attempts
    global time_mute
    global init_number
    global last_number
    global award
    boolean = ["true", "false"]
    text_c = "Команда не распознана."
    text_n = "Изменения применены."

    if pattern_admin_disable_game in msg_text:
        new_data = msg_text.replace(pattern_admin_disable_game, "")
        new_data = new_data.replace(" ", "")
        if new_data == boolean[0]:
            admin_disable_game = True
            return "Игра выключена."
        elif new_data == boolean[1]:
            admin_disable_game = False
            return "Игра включена."
        else:
            return text_c
    elif pattern_admin_change_attempts in msg_text:
        new_data = msg_text.replace(pattern_admin_change_attempts, "")
        new_data = new_data.replace(" ", "")
        try:
            new_data = int (new_data)
            all_attempts = new_data
            return "Кол-во попыток у игрока " + str(new_data)
        except ValueError:
            return text_c
    elif pattern_admin_change_time_mute in msg_text:
        new_data = msg_text.replace(pattern_admin_change_time_mute, "")
        new_data = new_data.replace(" ", "")
        try:
            new_data = int (new_data)
            time_mute = new_data
            return "Время мьюта " + str(new_data) + " мин."
        except ValueError:
            return text_c
    elif pattern_admin_change_init_number in msg_text:
        new_data = msg_text.replace(pattern_admin_change_init_number, "")
        new_data = new_data.replace(" ", "")
        try:
            new_data = int (new_data)
            init_number = new_data
            return "Начальное число " + str(new_data)
        except ValueError:
            return text_c
    elif pattern_admin_change_last_number in msg_text:
        new_data = msg_text.replace(pattern_admin_change_last_number, "")
        new_data = new_data.replace(" ", "")
        try:
            new_data = int (new_data)
            last_number = new_data
            return "Конечное число " + str(new_data)
        except ValueError:
            return text_c
    elif pattern_admin_change_award in msg_text:
        new_data = msg_text.replace(pattern_admin_change_award, "")
        new_data = new_data.replace(" ", "")
        try:
            new_data = int (new_data)
            award = new_data
            return "Приз " + str(new_data)
        except ValueError:
            return text_c
    else:
        return text_c
