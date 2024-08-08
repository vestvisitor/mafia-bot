from rules import *
from methods import *
import datetime

def get_current_time(seconds):
    current_time = datetime.datetime.now()
    if seconds is None:
        return current_time
    else:
        future_time = current_time + datetime.timedelta(seconds=seconds)
        return future_time

def fn_rolechoice(connection_data, command, values):
    def get_players():
        cursor.execute(command[7].format('username', f'room{values[0]}'))
        players = [str(u[0]) for u in cursor.fetchall()]
        players_buttons = [p.split()[-1] for p in players]
        random.shuffle(players_buttons)

        players_list = ""
        random.shuffle(players)

        for i, p in enumerate(players):
            players_list += f"{i + 1}) {p}\n"

        return [players_list, players_buttons]

    def don_mafia_hoe(players, role):

        if players.get(values[1])[1] == role:
            cursor.execute(command[3].format(values[2], f"room{values[0]}"), [values[3]])
            if cursor.fetchone()[0] != 1:  # check if mafia had chosen itsefl perviously
                cursor.execute(command[5].format(f"room{values[0]}", values[2]))  # reset mafia choice
                cursor.execute(command[1].format(f"room{values[0]}", values[2], 'userid'),
                               [1, players.get(values[1])[0]])
                cursor.execute(command[1].format(f"room{values[0]}", f'is_good', 'userid'),
                               [1, players.get(values[1])[0]])  # make bad guy good
                cursor.execute(command[2].format(f"room{values[0]}"), [0, values[3]])  # set sate to 0
                return True
            else:
                players = get_players()
                return [False, players[1]]
        else:
            cursor.execute(command[6].format(f"room{values[0]}"), [values[3]])  # reset bad guy is_good
            cursor.execute(command[5].format(f"room{values[0]}", values[2]))  # reset bad guy choice
            cursor.execute(command[1].format(f"room{values[0]}", values[2], 'userid'),
                           [1, players.get(values[1])[0]])  # set bad guy choice

            # change is_good
            if values[3] == 'Проститутка':  # don can choose is_good
                cursor.execute(command[3].format(f'is_good', f"room{values[0]}"), [players.get(values[1])[1]])
                is_good = cursor.fetchone()[0]
                if is_good == 1:
                    cursor.execute(command[1].format(f"room{values[0]}", 'is_good', 'userid'),
                                   [0, players.get(values[1])[0]])
                else:
                    cursor.execute(command[1].format(f"room{values[0]}", 'is_good', 'userid'),
                                   [1, players.get(values[1])[0]])

            cursor.execute(command[2].format(f"room{values[0]}"), [0, values[3]])  # set state to 0
            return True

    def doctor_bodyguard(players, role):

        if players.get(values[1])[1] == role:
            try:
                cursor.execute(command[4].format(f"room{values[0]}", values[2]))
                check = cursor.fetchone()[0]
            except:
                check = None

            if check == role:
                players = get_players()
                return [False, players[1]]
            else:
                cursor.execute(command[5].format(f"room{values[0]}", values[2]))
                cursor.execute(command[1].format(f"room{values[0]}", values[2], 'userid'),
                               [1, players.get(values[1])[0]])
                cursor.execute(command[2].format(f"room{values[0]}"), [0, values[3]])
                return [True]
        else:
            cursor.execute(command[5].format(f"room{values[0]}", values[2]))
            cursor.execute(command[1].format(f"room{values[0]}", values[2], 'userid'), [1, players.get(values[1])[0]])
            cursor.execute(command[2].format(f"room{values[0]}"), [0, values[3]])
            return [True]

    get_number_of_roles = lambda: (cursor.execute(command[13].format(f"room{values[0]}")), cursor.fetchone()[0])[
        1]  # get number of roles in the room

    is_alive = lambda next_role: \
    (cursor.execute(command[3].format('is_alive', f'room{values[0]}'), [next_role]), cursor.fetchone()[0])[
        1]  # function that checks is_alive by user_role

    fn_set_last_role_deadline = lambda role, room, timestamp: (
        cursor.execute(command[1].format("rooms", f"last_role", 'room'), [role, room]),
        cursor.execute(command[1].format("rooms", f"action_deadline", 'room'),
                       [timestamp, room]))  # set role's deadline

    def set_role_deadline_answer(role):

        active_roles = get_active_roles(get_number_of_roles())  # get a list of active roles

        try:
            for i, r in enumerate(active_roles):
                if r == role:
                    next_role = active_roles[i + 1]
                    if len(active_roles) > 6 and role == 'Дон' and is_alive(role) == 1:
                        role = active_roles[i + 1]
                    elif len(active_roles) > 5 and role == 'Комиссар' and is_alive(role) == 1:
                        role = active_roles[i + 1]
                    elif is_alive(next_role) == 1:
                        fn_set_last_role_deadline(next_role, values[0],
                                                  get_current_time(15).strftime("%d-%m-%Y %H:%M:%S"))
                        break
                    else:
                        role = next_role
        except:
            fn_set_last_role_deadline(None, values[0], None)  # set last role and action_deadline to NULL

    with connection_data.cursor() as cursor:
        cursor.execute(command[0].format(f"room{values[0]}"))
        players = {i[0][-1]: [i[1], i[2]] for i in cursor.fetchall()}

        if values[1] in players.keys():
            if values[3] == 'Дон':
                don = don_mafia_hoe(players, 'Дон')
                set_role_deadline_answer('Дон')
                connection_data.close()
                return don

            elif values[3] == 'Мафия':
                mafia = don_mafia_hoe(players, 'Мафия')
                set_role_deadline_answer('Мафия')
                connection_data.close()
                return mafia

            elif values[3] == 'Проститутка':
                hoe = don_mafia_hoe(players, 'Проститутка')
                set_role_deadline_answer('Проститутка')
                connection_data.close()
                return hoe

            elif values[3] in ['Комиссар', 'Сержант']:
                cursor.execute(command[2].format(f"room{values[0]}"), [0, values[3]])
                set_role_deadline_answer(values[3])
                connection_data.close()
                return True

            elif values[3] == 'Доктор':
                doctor = doctor_bodyguard(players, 'Доктор')
                set_role_deadline_answer('Доктор')
                connection_data.close()
                return doctor

            elif values[3] == 'Телохранитель':
                bodyguard = doctor_bodyguard(players, 'Телохранитель')
                set_role_deadline_answer('Доктор')
                connection_data.close()
                return bodyguard

            elif values[3] == 'Мститель' or values[
                3] == 'мститель':  # answer from revenger when he was kicked out / answer from revenger when he was killed

                fn_1 = lambda column, value, userid: (
                cursor.execute(command[8].format(f"room{values[0]}", column), [value]),
                cursor.execute(command[9], [userid]))

                if players.get(values[1])[1] == 'Мститель':
                    fn_1('user_role', 'Мститель',
                         values[2])  # set revenger is_alive, user_state to NULL, and room in all_users to NULL
                    send_message_to_user(values[2], "✅ Выбор принят!")
                    send_message_to_chat(values[0], f'🦸‍♂ Мститель решил никого с собой не забирать! 🦸‍♀')

                else:
                    get_username = lambda role: \
                    (cursor.execute(command[3].format('username', f"room{values[0]}"), [role]), cursor.fetchone()[0])[1]

                    choice = players.get(values[1])
                    name = get_username(choice[1])

                    fn_1('user_role', 'Мститель',
                         values[2])  # set revenger is_alive, user_state to NULL, and room in all_users to NULL
                    fn_1('user_role', choice[1],
                         choice[0])  # set chosen guy is_alive, user_state to NULL, and room in all_users to NULL

                    send_message_to_user(values[2], "✅ Выбор принят!")
                    send_message_to_chat(values[0], f"🦹‍♂ Мститель забирает с собой {name} ({choice[1]}) 🦹‍♀")

                cursor.execute(command[7].format('user_role', f"room{values[0]}"))  # get all alive roles
                roles = [r[0] for r in cursor.fetchall()]  # get all alive roles

                if 'Дон' not in roles and 'Мафия' not in roles:  # mafia lost
                    send_message_to_chat(values[0], '🙏 Поздраляю! Мирные жители выигрывают эту игру!')

                elif len(roles) > 2 and 'Дон' in roles or 'Мафия' in roles:  # continue the game

                    if values[3] == 'Мститель':  # revenger was kicked out

                        get_day_number = lambda: (cursor.execute(command[14], [values[0]]), cursor.fetchone()[0])[
                            1]  # get current day
                        next_day = int(get_day_number() + 1)  # increase day
                        cursor.execute(command[15], [next_day, values[0]])  # update new day

                        send_message_to_chat(values[0],
                                             f"🌠 Наступает ночь {next_day}-ого дня, города засыпает...")  # send message to chat that game goes on

                        fn = lambda role: (
                            cursor.execute(command[3].format('userid', f'room{values[0]}'), [role]),
                            # "SELECT {} FROM {} WHERE user_role = %s"
                            cursor.fetchone()[0],
                            cursor.execute(command[2].format(f'room{values[0]}'), [get_role_state(role),
                                                                                   role]))  # "UPDATE {} SET user_state = %s WHERE user_role = %s"

                        try:  # get user_id
                            badguy_id = fn('Дон')[1]
                            role = 'Дон'
                        except:
                            badguy_id = fn('Мафия')[1]
                            role = 'Мафия'

                        send_message_to_chat(values[0],
                                             messages_to_group_while_actions(role))  # #send message of mafia action

                        players = get_players()  # 0 players_list, 1 players_buttons

                        send_message_to_user_keyboard(badguy_id, f"{get_message_for_role(role)}\n{players[0]}",
                                                      users_keyboard(players[1], 1))  # send message to the bad guy

                    elif values[3] == 'мститель':  # revenger was killed

                        players = get_players()  # 0 players_list, 1 players_buttons

                        send_message_with_keyboard_to_chat(values[0],
                                                           f'👀 У кого есть какие предположения? Напоминаю кто еще в игре:\n'
                                                           f'{players[0]}'
                                                           f'❗ Каждый игрок может проголосовать лишь один раз, поэтому сначала обсудите это в чате!\n'
                                                           f'🤡 Если хотите по приколу случайно проголосовать - выберите свой смайлик (Уснуть случайно не получится).\n'
                                                           f'⌛ У вас есть одна минута для принятия решения!',
                                                           users_keyboard(players[1], 0))

                        cursor.execute(command[12].format(
                            f'room{values[0]}'))  # set all alive users to 88 state for recieving votes

                        # set poll's deadline
                        fn_set_last_poll_deadline = lambda timestamp, room: (
                            cursor.execute(command[1].format("rooms", f"poll_deadline", 'room'), [timestamp, room]))

                        fn_set_last_poll_deadline(get_current_time(60).strftime("%d-%m-%Y %H:%M:%S"), values[0])

                    connection_data.close()
                    return [True, None]

                elif len(roles) == 2 and 'Дон' in roles or 'Мафия' in roles:  # mafia won
                    send_message_to_chat(values[0], '😈 Мафия выигрывает эту игру!')

                print("REMOVE GAME FROM ROOMS TABLE")
                fn = lambda: (cursor.execute(command[10].format(f"room{values[0]}")), cursor.fetchall())[
                    1]  # select all alive users
                (lambda: [cursor.execute(command[9], [i[0]]) for i in
                          fn()])()  # set all alive users room to NULL in all_users
                cursor.execute(command[11].format(f"room{values[0]}"))  # drop table

                connection_data.close()
                return [True, None]

        else:
            players = get_players()[1]
            connection_data.close()
            return [None, players]