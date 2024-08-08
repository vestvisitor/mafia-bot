from rules import *
from methods import *
from m_pollresults import fn_pollresults
from sql_commands import commands_handler

def fn_timing(connection_data, command, values):
    with connection_data.cursor() as cursor:
        cursor.execute(command[0].format(f"action_deadline", 'rooms'))
        last_role_actions = [a[0] for a in cursor.fetchall()]

        cursor.execute(command[0].format(f"poll_deadline", 'rooms'))
        last_poll_actions = [a[0] for a in cursor.fetchall()]

        cursor.execute(command[0].format(f"game_expires", 'rooms'))
        game_expires = [a[0] for a in cursor.fetchall()]

        current_time = get_current_time(None)

        for r, p, g in zip(last_role_actions, last_poll_actions, game_expires):

            if current_time.strftime("%d-%m-%Y %H:%M:%S") == r:  # choice from role
                fn_get_room = lambda: \
                (cursor.execute(command[1].format(f"action_deadline"), [r]), cursor.fetchone()[0])[1]
                room_number = fn_get_room()

                fn_last_role = lambda: (cursor.execute(command[7], [room_number]), cursor.fetchone()[0])[1]
                last_role = fn_last_role()

                fn_get_afk = lambda: \
                (cursor.execute(command[8].format(f'room{room_number}'), [last_role]), cursor.fetchone())[1]
                afk = fn_get_afk()

                fn_select_joined_players = lambda: \
                (cursor.execute(command[3].format(f"room{room_number}")), cursor.fetchall())[
                    1]  # select all alive players
                (lambda: [cursor.execute(command[4], [i[0]]) for i in
                          fn_select_joined_players()])()  # clear room column in all_users for them
                cursor.execute(command[5].format(f"room{room_number}"))  # delete table
                cursor.execute(command[6], [room_number])  # delete row from rooms table

                send_message_to_user_keyboard(afk[1],
                                              f"🚫 Вы были дисквалифицированы из игры из-за того, что не успели сделать выбор!",
                                              get_empty_keyboard())  # send warning to the guy and this is where you need to ban him for a while
                send_message_to_chat(room_number,
                                     f"😠 К сожалению, игра была остановлена, поскольку игрок {afk[0]} не успел(-а) сделать свой выбор.")

            elif current_time.strftime("%d-%m-%Y %H:%M:%S") == p:  # vote from poll

                # get room number
                fn_get_room = lambda: (cursor.execute(command[1].format(f"poll_deadline"), [p]), cursor.fetchone()[0])[1]
                room_number = fn_get_room()

                send_message_with_empty_keyboard(room_number, "⏰ Время для голосования окончено!")

                cursor.execute(command[9].format("rooms", "poll_deadline", "room"), [None, room_number]) # Reset poll deadline

                # Get all votes from who is alive and voted or not
                cursor.execute(command[11].format("poll_vote", f"room{room_number}", "is_alive"), [1])
                results = [vote[0] for vote in cursor.fetchall()]

                cursor.execute(command[9].format(f"room{room_number}", "poll_vote", "is_alive"), [None, 1]) # Reset everyone's alive poll_vote to null
                cursor.execute(command[9].format(f"room{room_number}", "user_state", "is_alive"), [None, 1]) # Reset everyone's alive state to null

                for i, v in enumerate(results): # if somebody hadn't voted, program considers it as -1, meaning this guy wants to sleep
                    if v is None:
                        results[i] = -1

                votes = {}
                for i in results: # prepare the dataset for the pollresults function
                    if i not in votes.keys():
                        votes[i] = 1
                    else:
                        quantity = votes.get(i) + 1
                        votes[i] = quantity

                fn_pollresults(connection_data, commands_handler("POLL_RESULTS"), (room_number, votes)) # launch pollresult function

            elif current_time.strftime(
                    "%d-%m-%Y %H:%M:%S") == g:  # nobody joined or not enough players joined during one minute

                fn_get_room = lambda: (cursor.execute(command[1].format(f"game_expires"), [g]), cursor.fetchone()[0])[1]
                room_number = fn_get_room()

                fn_number_of_players = lambda: \
                (cursor.execute(command[2].format(f"room{room_number}")), cursor.fetchone()[0])[1]
                number_of_players = fn_number_of_players()

                fn_select_joined_players = lambda: \
                (cursor.execute(command[3].format(f"room{room_number}")), cursor.fetchall())[1]  # select all joined players
                players = fn_select_joined_players()

                if number_of_players < 4:
                    message = "😟 К сожалению, подключилось недостаточное колличество игроков. Как минимум для начала игры необходимо 4 игрока."
                    if room_number <= 2000000000:
                        send_message_with_empty_keyboard(room_number, message)
                    else:
                        (lambda: [delete_user(room_number, i[0]) for i in players])()
                        keyboard = get_empty_keyboard()
                        (lambda: [send_message_to_user_keyboard(i[0], message, keyboard) for i in players])()
                else:
                    message = "🙄 Создатель игры не запустил ее, поэтому игра не начнется... Создайте кто-нибудь более ответственный!"
                    if room_number <= 2000000000:
                        send_message_with_empty_keyboard(room_number, message)
                    else:
                        (lambda: [delete_user(room_number, i[0]) for i in players])()
                        keyboard = get_empty_keyboard()
                        (lambda: [send_message_to_user_keyboard(i[0], message, keyboard) for i in players])()

                (lambda: [cursor.execute(command[4], [i[0]]) for i in players])()  # clear room column in all_users for them

                cursor.execute(command[5].format(f"room{room_number}"))  # delete table
                cursor.execute(command[6], [room_number])  # delete row from rooms table

                print("NEEED TO FIGURE OUT HOW TO ALLOW USER COME BACK TO THE ROOM AFTER BEING EXCLUDED")

                cursor.execute(command[9].format(f"room{room_number}", "available", "room_id"), [1]) # make community room available