from rules import *
from methods import *

def fn_whoisalive(connection_data, command, values):
    with connection_data.cursor() as cursor:
        cursor.execute(command[0], [values[0]])  # get room number
        room_number = cursor.fetchone()[0]

        cursor.execute(
            command[1].format(f'room{room_number}'))  # get number of players in the room and select active_roles
        scenario = get_active_roles(cursor.fetchone()[0])

        role = values[1]
        is_alive = lambda next_role: \
        (cursor.execute(command[4].format(f'room{room_number}'), [next_role]), cursor.fetchone()[0])[
            1]  # function that checks is_alive by user_role

        def get_user_buttons_and_list():  # 0 players, 1 players_buttons, 2 players_list
            cursor.execute(command[5].format(f'room{room_number}'))
            players = [str(u[0]) for u in cursor.fetchall()]
            players_buttons = [p.split()[-1] for p in players]
            random.shuffle(players_buttons)

            players_list = ""

            random.shuffle(players)
            for i, p in enumerate(players):
                players_list += f"{i + 1}) {p}\n"

            return [players, players_buttons, players_list]

        try:
            for i, r in enumerate(scenario):
                if r == role:
                    next_role = scenario[i + 1]
                    if len(scenario) >= 6 and role == 'Дон' and is_alive(role) == 1:
                        role = scenario[i + 1]
                    elif len(scenario) >= 5 and role == 'Комиссар' and is_alive(role) == 1:
                        role = scenario[i + 1]
                    elif is_alive(next_role) == 1:
                        cursor.execute(command[2].format(f'room{room_number}'),
                                       [get_role_state(next_role), next_role])  # update next_role state

                        cursor.execute(command[3].format(f'room{room_number}'),
                                       [next_role])  # select userid by user_role
                        next_role_id = cursor.fetchone()[0]

                        break
                    else:
                        role = next_role

            players = get_user_buttons_and_list()  # 0 players, 1 players_buttons, 2 players_list

            message = f"{get_message_for_role(next_role)}\n{players[2]}"

            if values[1] in ['Комиссар', 'Сержант']:
                cursor.execute(command[6].format(f'room{room_number}'),
                               [next((n for n in players[0] if n[-1] == values[2]))])
                if cursor.fetchone()[0] == 1:
                    send_message_to_user(values[0], "👍 Это хороший персонаж!")
                else:
                    send_message_to_user(values[0], "👎 Это плохой персонаж!")

                # send message to chat about player's turns
                send_message_to_chat(room_number, messages_to_group_while_actions(next_role))

                connection_data.close()
                return {True: [next_role_id, message, players[1]]}
            else:

                # send message to chat about player's turns
                send_message_to_chat(room_number, messages_to_group_while_actions(next_role))

                connection_data.close()
                return {True: [next_role_id, message, players[1]]}

        except:

            fn_ids = lambda column: (
            (cursor.execute(command[7].format(f"userid", f'room{room_number}', column)), cursor.fetchone()[0])[1])
            fn_roles = lambda column: (
            (cursor.execute(command[7].format(f"user_role", f'room{room_number}', column)), cursor.fetchone()[0])[1])

            roles = []
            ids = []

            for column in ["mafia_choice", "hoe_choice", "doctor_choice", "bodyguard_choice"]:
                try:  # try to append chosen roles, ids
                    roles.append(fn_roles(column))
                    ids.append(fn_ids(column))
                except:  # if it's not possible add blank role and id
                    roles.append('Мертвец')
                    ids.append(-1)
                    pass

            cursor.execute(command[18].format("game_day", "rooms", "room"), [room_number])
            day_number = cursor.fetchone()[0]

            log = f"🖊 День {day_number}: "

            try:  # if don is alive
                cursor.execute(command[8].format(f'room{room_number}', f'user_role'), ['Дон'])
                if cursor.fetchone()[0] == 1:  # don is alive
                    if roles[0] == 'Дон':
                        log += 'Дон выбирает себя.\n'
                        death = False  # don had chosen himself

                    elif roles[0] == 'Проститутка':  # don kills hoe
                        log += 'Дон покушается на Проститутку: '
                        if roles[2] != 'Проститутка':  # doctor didn't chose hoe
                            if roles[3] != 'Проститутка':  # bodyguard didn't choose hoe
                                if roles[1] != roles[2]:  # if doctor didn't choose the same guy as hoe
                                    if roles[1] != roles[3]:  # if bodyguard didn't choose the same guy as hoe
                                        log += f"покушение проходит более чем успешно, Проститутка умирает, и, в свою очередь, забирает своего клиента ({role_word_form(roles[1])}).\n"
                                        cursor.execute(command[9].format(f'room{room_number}', f'user_role'),
                                                       [0, 'Проститутка'])  # is_alive = 0 hoe
                                        cursor.execute(command[9].format(f'room{room_number}', f'userid'),
                                                       [0, ids[1]])  # is_alive = 0 hoe's choice
                                        death = True
                                    else:
                                        log += f"покушение проходит более чем успешно, Проститутка умирает, однако Телохранитель спасает жизнь ее клиенту ({role_word_form(roles[1])}).\n"
                                        cursor.execute(command[9].format(f'room{room_number}', f'user_role'),
                                                       [0, 'Проститутка'])  # is_alive = 0 hoe
                                        cursor.execute(command[9].format(f'room{room_number}', f'user_role'),
                                                       [0, 'Телохранитель'])  # is_alive = 0 bodyguard
                                        death = True
                                else:
                                    log += f"покушчение проходит успешно, Проститутка умирает, однако Доктор спасает ее клиента ({role_word_form(roles[1])}).\n"
                                    cursor.execute(command[9].format(f'room{room_number}', f'user_role'),
                                                   [0, 'Проститутка'])  # is_alive = 0 hoe and her choice is alive
                                    death = True
                            else:
                                log += "покушение проходит не совсем по плану, Телохранитель спасает Проститутку, однако умирает сам.\n"
                                cursor.execute(command[9].format(f'room{room_number}', f'user_role'),
                                               [0, 'Телохранитель'])  # is_alive = 0 bodyguard but hoe is alive
                                death = True
                        else:
                            log += f"покушение срывается, Доктор спасает Проститутку и ее клиента ({role_word_form(roles[1])}).\n"
                            death = False  # doctor saved hoe and her choice

                    elif roles[0] in ['Мафия', 'Комиссар', 'Сержант', "Доктор", 'Телохранитель', "Мститель",
                                      "Суицидник", "Мирный"]:  # don one of these guys
                        log += f"Дон покушается на {role_word_form(roles[0])}: "
                        if roles[1] != roles[0]:  # hoe didn't save
                            if roles[2] != roles[0]:  # doctor didn't save
                                if roles[0] == 'Телохранитель':
                                    log += "покушение проходит по плану, Дон убивает свою жертву.\n"
                                    cursor.execute(command[9].format(f'room{room_number}', f'user_role'),
                                                   [0, 'Телохранитель'])  # is_alive = 0 bodyguard
                                    death = True
                                else:
                                    if roles[3] != roles[0]:  # bodyguard didn't save
                                        log += "покушение проходит по плану, Дон убивает свою жертву.\n"
                                        cursor.execute(command[9].format(f'room{room_number}', f'user_role'),
                                                       [0, roles[0]])  # set is_alive = 0 where user_role == 0
                                        death = True
                                    else:
                                        log += "покушение проходит не совсем по плану, Телохранитель спасает жертву покушения, однако умирает сам.\n"
                                        cursor.execute(command[9].format(f'room{room_number}', f'user_role'),
                                                       [0, 'Телохранитель'])  # bodyguard saved but died himself
                                        death = True
                            else:
                                log += "покушение срывается, Доктор спасает жертву покушения.\n"
                                death = False  # doctor saved
                        else:
                            log += "покушение срывается, Проститутка спасает жертву покушения.\n"
                            death = False  # hoe saved

            except:  # don is dead
                if roles[0] == 'Мафия':  # mafia chose itself
                    log += 'Мафия выбирает себя.\n'
                    death = False # nobody died

                elif roles[0] == 'Проститутка':  # don kills hoe
                    log += 'Мафия покушается на Проститутку: '
                    if roles[2] != 'Проститутка':  # doctor didn't chose hoe
                        if roles[3] != 'Проститутка':  # bodyguard didn't choose hoe #??????
                            if roles[1] != roles[2]:  # if not doctor didn't choose the same guy as hoe
                                if roles[1] != roles[3]:  # if not bodyguard didn't choose the same guy as hoe
                                    log += f"покушение проходит более чем успешно, Проститутка умирает, и, в свою очередь, забирает своего клиаента ({role_word_form(roles[1])}).\n"
                                    cursor.execute(command[9].format(f'room{room_number}', f'user_role'),
                                                   [0, 'Проститутка'])  # is_alive = 0 hoe
                                    cursor.execute(command[9].format(f'room{room_number}', f'userid'),
                                                   [0, ids[1]])  # is_alive = 0 hoe's choice
                                    death = True
                                else:
                                    log += f"покушение проходит более чем успешно, Проститутка умирает, однако Телохранитель спасает жизнь ее клиенту ({role_word_form(roles[1])}).\n"
                                    cursor.execute(command[9].format(f'room{room_number}', f'user_role'),
                                                   [0, 'Проститутка'])  # is_alive = 0 hoe
                                    cursor.execute(command[9].format(f'room{room_number}', f'user_role'),
                                                   [0, 'Телохранитель'])  # is_alive = 0 bodyguard
                                    death = True
                            else:
                                log += f"покушчение проходит успешно, Проститутка умирает, однако Доктор спасает ее клиента ({role_word_form(roles[1])}).\n"
                                cursor.execute(command[9].format(f'room{room_number}', f'user_role'),
                                               [0, 'Проститутка'])  # is_alive = 0 hoe and her choice is alive
                                death = True
                        else:
                            log += "покушение проходит не совсем по плану, Телохранитель спасает Проститутку, однако умирает сам.\n"
                            cursor.execute(command[9].format(f'room{room_number}', f'user_role'),
                                           [0, 'Телохранитель'])  # is_alive = 0 bodyguard but hoe is alive
                            death = True
                    else:
                        log += f"покушение срывается, Доктор спасает Проститутку и ее клиента ({role_word_form(roles[1])}).\n"
                        death = False  # doctor saved hoe and her choice

                elif roles[0] in ['Комиссар', 'Сержант', "Доктор", 'Телохранитель', "Мститель", "Суицидник",
                                  "Мирный"]:  # don one of these guys
                    log += f"Мафия покушается на {role_word_form(roles[0])}: "
                    if roles[1] != roles[0]:  # hoe didn't save
                        if roles[2] != roles[0]:  # doctor didn't save
                            if roles[0] == 'Телохранитель':
                                log += "покушение проходит по плану, Мафия убивает свою жертву.\n"
                                cursor.execute(command[9].format(f'room{room_number}', f'user_role'),
                                               [0, 'Телохранитель'])  # is_alive = 0 bodyguard
                                death = True
                            else:
                                log += "покушение проходит по плану, Мафия убивает свою жертву.\n"
                                if roles[3] != roles[0]:  # bodyguard didn't save
                                    cursor.execute(command[9].format(f'room{room_number}', f'user_role'), [0, roles[0]])
                                    death = True
                                else:
                                    log += "покушение проходит не совсем по плану, Телохранитель спасает жертву покушения, однако умирает сам.\n"
                                    cursor.execute(command[9].format(f'room{room_number}', f'user_role'),
                                                   [0, 'Телохранитель'])  # bodyguard saved but died himself
                                    death = True
                        else:
                            log += "покушение срывается, Доктор спасает жертву покушения.\n"
                            death = False  # doctor saved
                    else:
                        log += "покушение срывается, Проститутка спасает жертву покушения.\n"
                        death = False  # hoe saved

            cursor.execute(command[18].format("actions_history", "rooms", "room"), [room_number]) # select previous records of actions_history
            history = cursor.fetchone()[0]
            if history is None:
                history = ""
            history += log # add current log to the history

            cursor.execute(command[19].format("rooms", "actions_history", "room"), [history, room_number]) # update actions_history

            fn_set_last_poll_deadline = lambda timestamp, room: (
                cursor.execute(command[17].format("rooms", f"poll_deadline", 'room'),
                               [timestamp, room]))  # function that sets poll deadline

            if death is False:  # nobody died

                players = get_user_buttons_and_list()  # 0 players, 1 players_buttons, 2 players_list

                send_message_with_keyboard_to_chat(room_number, f'🔊 Сегодня ночью никто не умер!\n'
                                                                f'👀 У кого есть какие предположения? Напоминаю кто еще в игре:\n'
                                                                f'{players[2]}'
                                                                f'❗ Каждый игрок может проголосовать лишь один раз без права смены голоса, поэтому сначала обсудите это в чате!\n'
                                                                f'🤡 Если хотите по приколу случайно проголосовать - выберите свой смайлик (уснуть случайно не получится).\n'
                                                                f'⌛ У вас есть одна минута для принятия решения!',
                                                   users_keyboard(players[1], 0))

                cursor.execute(
                    command[12].format(f'room{room_number}'))  # set all alive users to 88 state for recieving votes

                # set poll's deadline
                fn_set_last_poll_deadline(get_current_time(60).strftime("%d-%m-%Y %H:%M:%S"), room_number)

            elif death is True:  # somebody dead

                cursor.execute(
                    command[10].format(f'room{room_number}'))  # select username, userid, user_role who are dead
                dead = [d for d in cursor.fetchall()]  # 0 - username, 1 - userid, 2 - user_role

                if len(dead) == 2:
                    message_dead = f'💀 Сегодня ночью произошло двойное убийство! \n😨 Были убиты: '
                    for i, d in enumerate(dead):
                        if i == 0:
                            d1 = d
                        else:
                            d2 = d
                    message_dead += f'{d1[0]} ({d1[2]}) и {d2[0]} ({d2[2]}).\n'
                else:
                    message_dead = f'💀 Сегодня ночью убили {dead[0][0]} ({dead[0][2]}).\n'

                fn_reset_room = lambda lst: [cursor.execute(command[11], [d[1]]) for d in
                                             lst]  # clear room for dead guys from all_users table
                fn_set_alive_state_null = lambda lst: [cursor.execute(command[16].format(f'room{room_number}'), [d[1]])
                                                       for d in lst]  # set dead guys 'is_alive', 'user_state' to NULL

                for i, d in enumerate(dead):
                    if d[2] == 'Мститель':
                        revenger_id = dead[i][1]

                        if len(dead) == 1:
                            send_message_to_chat(room_number,
                                                 f"{message_dead}👊 Мститель выбирает, кого сейчас он заберет с собой на тот свет!")
                        else:
                            send_message_to_chat(room_number,
                                                 f"{message_dead}👊 Среди убитых оказался Мститель, поэтому сейчас он выберет, кого заберет с собой на тот свет!")

                        cursor.execute(command[2].format(f"room{room_number}"),
                                       [10, 'Мститель'])  # set revenger to 10 state
                        cursor.execute(command[9].format(f"room{room_number}", "user_role"), [1,
                                                                                              'Мститель'])  # set revenger is_alive to 1 so he can choose himself later for not killing anyone with him

                        del dead[i]

                        fn_reset_room(dead)  # clear room for dead guys from all_users table
                        fn_set_alive_state_null(dead)  # set dead guys 'is_alive', 'user_state' to NULL

                        players = get_user_buttons_and_list()  # 0 players, 1 players_buttons, 2 players_list

                        send_message_to_user_keyboard(revenger_id,
                                                      f"👊 Выбирай кого сейчас ты заберешь с собой в могилу!\n{players[2]}😶 Выбери себя если не хочешь никого забирать.",
                                                      users_keyboard(players[1], 1))

                        # Give revenger 15 seconds to think
                        fn_set_last_role_deadline = lambda role, room, timestamp: (
                            cursor.execute(command[17].format("rooms", f"last_role", 'room'), [role, room]),
                            cursor.execute(command[17].format("rooms", f"action_deadline", 'room'),
                                           [timestamp, room]))  # set role's deadline
                        fn_set_last_role_deadline('Мститель', room_number,
                                                  get_current_time(15).strftime("%d-%m-%Y %H:%M:%S"))

                        return None

                fn_reset_room(dead)  # clear room for dead guys from all_users table
                fn_set_alive_state_null(dead)  # set dead guys 'is_alive', 'user_state' to NULL

                fn = lambda: \
                (cursor.execute(command[13].format(f'room{room_number}')), [r[0] for r in cursor.fetchall()])[
                    1]  # get alive roles
                roles = fn()

                if len(roles) > 2:  # does it make sense to continue the game?
                    if 'Дон' in roles or 'Мафия' in roles:  # continue the game
                        players = get_user_buttons_and_list()  # 0 players, 1 players_buttons, 2 players_list

                        send_message_with_keyboard_to_chat(room_number,
                                                           f'{message_dead}'  # need to replace that
                                                           f'👀 У кого есть какие предположения? Напоминаю кто еще в игре:\n'
                                                           f'{players[2]}'
                                                           f'❗ Каждый игрок может проголосовать лишь один раз, поэтому сначала обсудите это в чате!\n'
                                                           f'🤡 Если хотите по приколу случайно проголосовать - выберите свой смайлик (Уснуть случайно не получится).\n'
                                                           f'⌛ У вас есть одна минута для принятия решения!',
                                                           users_keyboard(players[1], 0))

                        cursor.execute(command[12].format(
                            f'room{room_number}'))  # set all alive users to 88 state for recieving votes

                        # set poll's deadline
                        fn_set_last_poll_deadline(get_current_time(60).strftime("%d-%m-%Y %H:%M:%S"), room_number)

                        connection_data.close()
                        return None

                    else:  # mafia lost the game
                        send_message_to_chat(room_number,
                                             f"{message_dead}\n🥳 Таким образом, мирные жители выигрывают эту игру!")
                else:
                    if 'Дон' in roles or 'Мафия' in roles:  # mafia won the game
                        send_message_to_chat(room_number, f"{message_dead}\n😈 Тем самым Мафия выигрывает эту игру!")
                    else:  # mafia lost the game
                        send_message_to_chat(room_number,
                                             f"{message_dead}\n🥳 Таким образом, мирные жители выигрывают эту игру!")

                send_message_to_chat(room_number, history) # send message to the chat about the game choices
                cursor.execute(command[20], [room_number]) # delete row about game in rooms table
                fn = lambda: (cursor.execute(command[14].format(f"room{room_number}")), cursor.fetchall())[1]  # select all alive players
                fn_reset_room(fn())  # clear room column in all_users for them
                cursor.execute(command[15].format(f"room{room_number}"))  # delete table