from rules import *
from methods import *

def fn_pollresults(connection_data, command, values):
    max_votes = max(values[1].values())

    kicked_guy_id = max(values[1], key=values[1].get)

    votes = [k for k, v in values[1].items() if int(v) == int(max_votes)]

    with connection_data.cursor() as cursor:

        def get_players():

            cursor.execute(command[9].format(f'room{values[0]}'))
            players = [str(u[0]) for u in cursor.fetchall()]
            players_buttons = [p.split()[-1] for p in players]
            random.shuffle(players_buttons)

            players_list = ""
            random.shuffle(players)

            for i, p in enumerate(players):
                players_list += f"{i + 1}) {p}\n"

            return [players, players_buttons, players_list]

        def start_new_round():

            columns_roles = {'Проститутка': 'hoe_choice', 'Доктор': 'doctor_choice',
                             'Телохранитель': 'bodyguard_choice'}

            for role, column in columns_roles.items():
                try:
                    cursor.execute(command[10].format('is_alive', f'room{values[0]}'),
                                   [role])  # select is_alive of the role
                    is_alive = cursor.fetchone()[0]
                    if is_alive is None:  # if role is dead

                        if role == 'Проститутка':
                            cursor.execute(command[12].format('user_role', f'room{values[0]}', column),
                                           [1])  # select role which hoe had chosen
                            hoe_choice = cursor.fetchone()[0]

                            cursor.execute(command[10].format('is_alive', f'room{values[0]}'),
                                           [hoe_choice])  # select if the role is alive
                            choice_alive = cursor.fetchone()[0]

                            if choice_alive is None:  # role is dead - nothing to do
                                pass
                            else:  # role is alive - reset its is_good
                                if hoe_choice in ['Дон', 'Мафия']:
                                    number = 0
                                elif hoe_choice in ["Комиссар", "Сержант", "Доктор", "Телохранитель", "Мститель",
                                                    "Суицидник", "Мирный"]:
                                    number = 1

                                cursor.execute(command[13].format(f'room{values[0]}', 'is_good'),
                                               [number, hoe_choice])  # update is_good depending on the chosen role

                        cursor.execute(command[11].format(f'room{values[0]}', column),
                                       [0])  # set its column's rows to 0

                except:
                    pass

            fn = lambda role: (
                cursor.execute(command[18].format('userid', f'room{values[0]}'), [role]), cursor.fetchone()[0],
                cursor.execute(command[8].format(f'room{values[0]}'), [get_role_state(role), role]))

            try:  # get user_id
                badguy_id = fn('Дон')[1]
                role = 'Дон'
            except:
                badguy_id = fn('Мафия')[1]
                role = 'Мафия'

            send_message_to_chat(values[0],
                                 messages_to_group_while_actions(role))  # #send message of mafia action

            players = get_players()  # 0 players, 1 players_buttons, 2 players_list

            send_message_to_user_keyboard(badguy_id, f"{get_message_for_role(role)}\n{players[2]}",
                                          users_keyboard(players[1], 1))  # send message to the bad guy

            fn_set_last_role_deadline(role, values[0], get_current_time(15).strftime("%d-%m-%Y %H:%M:%S")) # give bad guy 15 seconds to thinks

        def change_day():
            get_day_number = lambda: (cursor.execute(command[14], [values[0]]), cursor.fetchone()[0])[
                1]  # get current day
            next_day = int(get_day_number() + 1)  # increase day
            cursor.execute(command[15], [next_day, values[0]])  # update new day
            return next_day

        # set role's deadline
        fn_set_last_role_deadline = lambda role, room, timestamp: (
            cursor.execute(command[16].format("rooms", f"last_role", 'room'), [role, room]),
            cursor.execute(command[16].format("rooms", f"action_deadline", 'room'),
                           [timestamp, room]))

        if votes[0] == -1 or len(votes) >= 2:  # players decided to sleep
            cursor.execute(command[0].format(f"room{values[0]}"))  # set all alive users poll_vote to NULL

            if votes[0] == -1:
                send_message_with_keyboard_to_chat(values[0],
                                                   f"💤 Больнишство жителей проголосовало за сон, поэтому город засыпает...\n🌙 Наступает ночь {change_day()}-ого дня...",
                                                   get_empty_keyboard())  # send message to chat
            else:
                send_message_with_keyboard_to_chat(values[0],
                                                   f"🤷‍♂🤷‍♀ По результатам дневного голосования, жители не пришли к общему мнению.\n"
                                                   f"😴 Поэтому ночь {change_day()}-ого дня наступает, а город засыпает...",
                                                   get_empty_keyboard())

            start_new_round()

            connection_data.close()
            return True

        else:  # somebody was voted off
            cursor.execute(command[0].format(f"room{values[0]}"))  # set all alive users poll_vote to NULL

            cursor.execute(command[1].format(f"room{values[0]}"),
                           [kicked_guy_id])  # select username, user role of kicked guy
            dead = cursor.fetchone()

            if dead[1] != 'Мститель':
                cursor.execute(command[2].format(f"room{values[0]}"),
                               [kicked_guy_id])  # set kicked guy's is_alive to NULL
                cursor.execute(command[16].format(f"room{values[0]}", "user_state", "userid"), [None, kicked_guy_id]) # set kicked guy state to NUll
                cursor.execute(command[3], [kicked_guy_id])  # set kicked guy's room to NULL in all_users

            fn_check = lambda column, role: (
            cursor.execute(command[10].format(column, f'room{values[0]}'), [role]), cursor.fetchone()[0])

            if dead[1] in ['Дон', 'Мафия']:  # mafia voted off

                if dead[1] == "Дон":
                    try:
                        alive = fn_check('is_alive', 'Мафия')[1]
                    except:
                        alive = False
                elif dead[1] == 'Мафия':
                    try:
                        alive = fn_check('is_alive', 'Дон')[1]
                    except:
                        alive = False

                if alive == 1:
                    send_message_with_keyboard_to_chat(values[0],
                                                       f'🕯 На дневном голосовании жители определили, что сегодня этот мир покидает {dead[0]} ({dead[1]}).\n'
                                                       f'🌃 И вновь наступает ночь {change_day()}-ого дня, город засыпает...',
                                                       get_empty_keyboard())

                    start_new_round()

                    connection_data.close()
                    return True

                else:
                    send_message_with_keyboard_to_chat(values[0],
                                                       f'🥳 На дневном голосовании жители определили, что сегодня этот мир покидает {dead[0]} ({dead[1]}).\n'
                                                       f'👊 Поздравляю, мирные выигрывают эту игру!',
                                                       get_empty_keyboard())

            elif dead[1] == 'Суицидник':  # suicide voted off
                send_message_with_keyboard_to_chat(values[0],
                                                   f'😩 На дневном голосовании жители определили, что сегодня этот мир покидает {dead[0]} ({dead[1]}).\n'
                                                   f'👽 Поздравляю, прекрасная работа!', get_empty_keyboard())

            elif dead[1] == 'Мститель':  # revenger voted off
                send_message_with_keyboard_to_chat(values[0],
                                                   f'😰 На дневном голосовании жители определили, что сегодня этот мир покидает {dead[0]} ({dead[1]}).\n👊 Мститель выбирает, кого сейчас он заберет с собой на тот свет!',
                                                   get_empty_keyboard())

                players = get_players()  # 0 players, 1 players_buttons, 2 players_list
                revenger_id = fn_check(f'userid', 'Мститель')[1]

                cursor.execute(command[8].format(f'room{values[0]}'), [get_role_state('Мститель'), 'Мститель'])
                send_message_to_user_keyboard(revenger_id,
                                              f"👊 Выбирай кого сейчас ты заберешь с собой в могилу!\n{players[2]}😶 Выбери себя если не хочешь никого забирать.",
                                              users_keyboard(players[1], 1))

                # Give revenger 15 seconds to think
                fn_set_last_role_deadline('Мститель', values[0], get_current_time(15).strftime("%d-%m-%Y %H:%M:%S"))

                connection_data.close()
                return True

            else:
                fn = lambda: (cursor.execute(command[7].format(f'room{values[0]}')), [r[0] for r in cursor.fetchall()])[
                    1]
                roles = fn()
                if len(roles) > 2:
                    send_message_with_empty_keyboard(values[0],
                                                     f'🕯 На дневном голосовании жители определили, что сегодня этот мир покидает {dead[0]} ({dead[1]}).\n🌃 Наступает ночь {change_day()}-ого дня, город засыпает...')

                    start_new_round()

                    connection_data.close()
                    return True

                elif len(roles) == 2 and 'Дон' in roles or 'Мафия' in roles:
                    send_message_with_keyboard_to_chat(values[0],
                                                       f'🕯 На дневном голосовании жители определили, что сегодня этот мир покидает {dead[0]} ({dead[1]}).\n'
                                                       f'😈 Тем самым мафия выигрывает эту игру!', get_empty_keyboard())

            # select game history
            cursor.execute(command[12].format("actions_history", "rooms", "room"), [values[0]])
            history = cursor.fetchone()[0]

            send_message_to_chat(values[0], history)  # send message to the chat about the game choices

            cursor.execute(command[17], [values[0]])  # delete row about game in rooms table
            fn = lambda: (cursor.execute(command[4].format(f"room{values[0]}")), cursor.fetchall())[1]
            (lambda: [cursor.execute(command[5], [i[0]]) for i in fn()])()
            cursor.execute(command[6].format(f"room{values[0]}"))