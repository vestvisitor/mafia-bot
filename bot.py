import vk_api
import threading
import time
from vk_api.longpoll import VkLongPoll, VkEventType

from database import *
from methods import *

token = 'secret'

session = vk_api.VkApi(
    token=token)
vk = session.get_api()


def start_game(chat_id):

    number_of_players = execute_sql_command("ENOUGH_PLAYERS", chat_id)
    if number_of_players >= 4:
        scenario = get_scenario(number_of_players)  # choose scenario
        random.shuffle(scenario)  # shuffle roles
        messages = execute_sql_command("ROLES_GIVE", (chat_id, scenario))
        print(messages)
        send_message_with_empty_keyboard(chat_id, messages[0])  # send message to chat
        (lambda: [send_message_to_user(k, v) for k, v in messages[1].items()])()  # send messages to players

        if number_of_players >= 7:
            send_message_to_chat(chat_id, messages_to_group_while_actions('Дон'))
            send_message_to_user_keyboard(messages[2], f"{get_message_for_role('Дон')}\n{messages[4]}", users_keyboard(messages[3], 1))
        else:
            send_message_to_chat(chat_id, messages_to_group_while_actions('Мафия'))
            send_message_to_user_keyboard(messages[2], f"{get_message_for_role('Мафия')}\n{messages[4]}", users_keyboard(messages[3], 1))
    else:
        send_message_to_chat(chat_id, f"😒 Не хватает игроков!")


def check():
    while True:
        try:
            execute_sql_command("CHECK_TIME", ())
        except Exception as ex:
            print(ex)
        finally:
            time.sleep(.9)


if __name__ == '__main__':

    # check for time
    x = threading.Thread(target=check, args=())
    x.start()

    for event in VkLongPoll(session).listen():

        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            user_id = event.user_id
            msg = event.text.lower()
            first_name = list(session.method("users.get", {"user_ids": user_id})[0].items())[1][1]
            second_name = list(session.method("users.get", {"user_ids": user_id})[0].items())[2][1]
            username = f'{first_name} {second_name}'
            execute_sql_command('INSERT_ALL_USERS', (username, user_id)) # you probably should to this on the start button not everytime

            if event.from_chat is True and msg == 'создать':
                chat_id = event.chat_id
                create_room = execute_sql_command('CREATE_ROOM', (chat_id, username, user_id))
                if create_room is False:
                    send_message_to_chat(chat_id, f"🗿 Игра уже создана!")
                elif create_room is None:
                    send_message_to_chat(chat_id, f"😒 {username}, ты не можешь создать новую игру пока не закончишь прежнюю!")
                else:
                    send_message_with_join_button(chat_id, f"🎭 {username} создал(-а) игру, скорее подключайся!")

            elif event.from_chat is True and msg == '[club217355254|@club217355254] присоединиться' or msg == '[club217355254|company chat-bot] присоединиться' or msg == 'присоединиться':
                chat_id = event.chat_id
                result = execute_sql_command("JOIN_ROOM", (chat_id, user_id, username))
                if result is True: # that means there are already 10 players
                    start_game(chat_id)

            elif event.from_chat is True and msg == 'начать':
                chat_id = event.chat_id
                if execute_sql_command("USER_STATE_BY_CHATID", (chat_id, user_id)) == 1:
                    number_of_players = execute_sql_command("ENOUGH_PLAYERS", chat_id)
                    start_game(chat_id)
                else:
                    send_message_to_chat(chat_id, "😠 Игра еще не создана, начинать нечего!")

            #create to accept answers from room
            elif event.from_chat is True and execute_sql_command('USER_STATE_BY_USERID', user_id) == 88:
                if msg.split()[0] in ['[club217355254|company', '[club217355254|@club217355254]', '[club217355254|company chat-bot]', '[club217355254|@club217355254]']:
                    choice = execute_sql_command('PLAYERS_VOTE', (event.chat_id, user_id, msg.split()[-1]))
                    if choice[0] is True:
                        send_message_to_chat(event.chat_id, f"✅ {username}, твой голос засчитан!")
                        if choice[1] is True:
                            send_message_to_chat(event.chat_id, '📫 Голосование окончено!')
                            execute_sql_command('POLL_RESULTS', (event.chat_id, choice[2]))
                    else:
                        send_message_to_chat(event.chat_id, f"🚫 {username}, неправильный выбор!")

            #answer from don
            elif event.from_user is True and execute_sql_command('USER_STATE_BY_USERID', user_id) == 2:
                choice = execute_sql_command("ROLE_CHOICE", (execute_sql_command("USER_ROOM", user_id), msg, 'mafia_choice', 'Дон'))
                if choice is True:
                    send_message_to_user(user_id, "✅ Выбор принят!")
                    results = execute_sql_command("WHO_IS_ALIVE", (user_id, "Дон"))
                    try:
                        check = list(results.keys())[0]
                        if check is True:
                            message = results.get(check)
                            send_message_to_user_keyboard(message[0], message[1], users_keyboard(message[2], 1))
                    except:
                        pass
                elif choice[0] is False:
                    send_message_to_user_keyboard(user_id, f'👺 Прошлую ночь ты уже выбирал(-а) себя!', users_keyboard(choice[1], 1))
                else:
                    send_message_to_user_keyboard(user_id, "🚫 Некорректный выбор!", users_keyboard(choice[1], 1))

            #answer from mafia
            elif event.from_user is True and execute_sql_command('USER_STATE_BY_USERID', user_id) == 3:
                choice = execute_sql_command("ROLE_CHOICE", (execute_sql_command("USER_ROOM", user_id), msg, 'mafia_choice', 'Мафия'))
                if choice is True:
                    send_message_to_user(user_id, "✅ Выбор принят!")
                    results = execute_sql_command("WHO_IS_ALIVE", (user_id, "Мафия"))
                    try:
                        check = list(results.keys())[0]
                        if check is True:
                            message = results.get(check)
                            send_message_to_user_keyboard(message[0], message[1], users_keyboard(message[2], 1))
                    except:
                        pass
                elif choice[0] is False:
                    send_message_to_user_keyboard(user_id, f'👺 Прошлую ночь ты уже выбирал(-а) себя!', users_keyboard(choice[1], 1))
                else:
                    send_message_to_user_keyboard(user_id, "🚫 Некорректный выбор!", users_keyboard(choice[1], 1))

            #answer from hoe
            elif event.from_user is True and execute_sql_command('USER_STATE_BY_USERID', user_id) == 4:
                choice = execute_sql_command("ROLE_CHOICE", (execute_sql_command("USER_ROOM", user_id), msg, 'hoe_choice', 'Проститутка'))
                if choice is True:
                    send_message_to_user(user_id, "✅ Выбор принят!")
                    results = execute_sql_command("WHO_IS_ALIVE", (user_id, "Проститутка"))
                    try:
                        check = list(results.keys())[0]
                        if check is True:
                            message = results.get(check)
                            send_message_to_user_keyboard(message[0], message[1], users_keyboard(message[2], 1))
                    except:
                        pass
                elif choice[0] is False:
                    send_message_to_user_keyboard(user_id, f'👺 Прошлую ночь ты уже выбирал(-а) себя!', users_keyboard(choice[1], 1))
                else:
                    send_message_to_user_keyboard(user_id, "🚫 Некорректный выбор!", users_keyboard(choice[1], 1))

            # answer from comissar
            elif event.from_user is True and execute_sql_command('USER_STATE_BY_USERID', user_id) == 5:
                if execute_sql_command("ROLE_CHOICE", (execute_sql_command("USER_ROOM", user_id), msg, 'sheriff_choice', 'Комиссар')) is True: #remove column
                    results = execute_sql_command("WHO_IS_ALIVE", (user_id, "Комиссар", msg))
                    try:
                        check = list(results.keys())[0]
                        if check is True:
                            message = results.get(check)
                            send_message_to_user_keyboard(message[0], message[1], users_keyboard(message[2], 1))
                    except:
                        pass
                else:
                    send_message_to_user(user_id, "🚫 Некорректный выбор!")

            # answer from sergiant
            elif event.from_user is True and execute_sql_command('USER_STATE_BY_USERID', user_id) == 6:
                if execute_sql_command("ROLE_CHOICE", (execute_sql_command("USER_ROOM", user_id), msg, 'sheriff_choice', 'Сержант')) is True: #remove column
                    results = execute_sql_command("WHO_IS_ALIVE", (user_id, "Сержант", msg))
                    try:
                        check = list(results.keys())[0]
                        if check is True:
                            message = results.get(check)
                            send_message_to_user_keyboard(message[0], message[1], users_keyboard(message[2], 1))
                    except:
                        pass
                else:
                    send_message_to_user(user_id, "🚫 Некорректный выбор!")

            # answer from doctor
            elif event.from_user is True and execute_sql_command('USER_STATE_BY_USERID', user_id) == 7:
                choice = execute_sql_command("ROLE_CHOICE", (execute_sql_command("USER_ROOM", user_id), msg, 'doctor_choice', 'Доктор'))
                if choice[0] is True:
                    send_message_to_user(user_id, "✅ Выбор принят!")
                    results = execute_sql_command("WHO_IS_ALIVE", (user_id, "Доктор"))
                    try:
                        check = list(results.keys())[0]
                        if check is True:
                            message = results.get(check)
                            send_message_to_user_keyboard(message[0], message[1], users_keyboard(message[2], 1))
                    except:
                        pass
                elif choice[0] is False:
                    send_message_to_user_keyboard(user_id, f'👺 Прошлую ночь ты уже выбирал(-а) себя!', users_keyboard(choice[1], 1))
                else:
                    send_message_to_user_keyboard(user_id, "🚫 Некорректный выбор!", users_keyboard(choice[1], 1))

            # answer from bodyguard
            elif event.from_user is True and execute_sql_command('USER_STATE_BY_USERID', user_id) == 8:
                choice = execute_sql_command("ROLE_CHOICE", (execute_sql_command("USER_ROOM", user_id), msg, 'bodyguard_choice', 'Телохранитель'))

                if choice[0] is True:
                    send_message_to_user(user_id, "✅ Выбор принят!")
                    results = execute_sql_command("WHO_IS_ALIVE", (user_id, "Телохранитель"))
                    try:
                        check = list(results.keys())[0]
                        if check is True:
                            message = results.get(check)
                            send_message_to_user_keyboard(message[0], message[1], users_keyboard(message[2], 1))
                    except:
                        pass
                elif choice[0] is False:
                    send_message_to_user_keyboard(user_id, f'👺 Прошлую ночь ты уже выбирал(-а) себя!', users_keyboard(choice[1], 1))
                else:
                    send_message_to_user_keyboard(user_id, "🚫 Некорректный выбор!", users_keyboard(choice[1], 1))

            # answer from revenger if he was kicked out during day's poll
            elif event.from_user is True and execute_sql_command('USER_STATE_BY_USERID', user_id) == 9:
                choice = execute_sql_command("ROLE_CHOICE", (execute_sql_command("USER_ROOM", user_id), msg, user_id, 'Мститель'))
                if choice[0] is None:
                    send_message_to_user_keyboard(user_id, "🚫 Некорректный выбор!", users_keyboard(choice[1], 1))

            # answer from revenger if he was killed during a night
            elif event.from_user is True and execute_sql_command('USER_STATE_BY_USERID', user_id) == 10:
                choice = execute_sql_command("ROLE_CHOICE", (execute_sql_command("USER_ROOM", user_id), msg, user_id, 'мститель'))
                if choice[0] is None:
                    send_message_to_user_keyboard(user_id, "🚫 Некорректный выбор!", users_keyboard(choice[1], 1))
