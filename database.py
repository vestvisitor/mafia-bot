import psycopg2
import random
import operator
import datetime
from config import host, user, password, db_name
from sql_commands import commands_handler

from rules import *
from methods import *
from m_rolesgive import fn_rolesgive
from m_rolechoice import fn_rolechoice
from m_whoisalive import fn_whoisalive
from m_pollresults import fn_pollresults
from m_timing import fn_timing

def db_connection(fn):

    def wrapper(type, values, *args, **kwargs):
        try:
            connection_data = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection_data.autocommit = True
        except Exception as _ex:
            print(_ex)

        command = commands_handler(type)

        if type == "INSERT_ALL_USERS":
            with connection_data.cursor() as cursor:
                cursor.execute(command[0], [values[1]])
                if cursor.fetchone() is None:
                    cursor.execute(command[1], values)

        elif type == "CREATE_ROOM":

            with connection_data.cursor() as cursor:
                room = lambda: (cursor.execute(command[0], [values[2]]), cursor.fetchone()[0])[1]
                room = room()
                if room is None or room == -2:
                    cursor.execute(command[1], [f'room{values[0]}'])
                    if cursor.fetchone() is None:
                        cursor.execute(command[2].format(f'room{values[0]}'))
                        cursor.execute(command[3].format(f'room{values[0]}'), [values[1], values[2]])
                        cursor.execute(command[4].format(f'room{values[0]}'), [values[0], values[2]])

                        future_time = get_current_time(60) # get future time
                        cursor.execute(command[5], [values[0], future_time.strftime("%d-%m-%Y %H:%M:%S"), "📖 Хроника игровых событий 📖 \n"]) # insert room and future time into rooms
                        connection_data.close()
                        return True
                    else:
                        connection_data.close()
                        return False
                else:
                    connection_data.close()
                    return None

        elif type == "CHECK_TIME":

            return fn_timing(connection_data, command, values)

        elif type == "JOIN_ROOM":

            with connection_data.cursor() as cursor:
                cursor.execute(command[0], [f'room{values[0]}'])
                is_room_created = cursor.fetchone()

                cursor.execute(command[6].format(f'room{values[0]}'))
                has_game_began = cursor.fetchone()[0]

                if is_room_created is None:
                    send_message_to_chat(values[0], f'✋ Игра еще не создана!')

                elif has_game_began is not None:
                    send_message_to_chat(values[0], f'☝ Игра уже началась!')

                else:
                    room = lambda: (cursor.execute(command[1], [values[1]]), cursor.fetchone()[0])[1]
                    if room() is None:
                        cursor.execute(command[2].format(f'room{values[0]}'), [values[1]])
                        if cursor.fetchone() is None:
                            cursor.execute(command[3].format(f'room{values[0]}'), [values[2], values[1]])
                            cursor.execute(command[4], [values[0], values[1]])

                            cursor.execute(command[5].format(f'room{values[0]}'))
                            count = cursor.fetchone()[0]

                            send_message_to_chat(values[0], f'✅ {values[2]} присоединился(-ась) к игре! (👥 {count} игроков)')

                            if count == 10:
                                send_message_with_empty_keyboard(values[0], f'❗ Достигнуто максимальное колличество игроков, поэтому игра начинается автоматически!')
                                connection_data.close()
                                return True

                        else:
                            send_message_to_chat(values[0], f'❗ {values[2]}, ты уже в игре!')
                    else:
                        send_message_to_chat(values[0], f'‼ {values[2]}, ты не можешь присоединиться к новой игре пока не закончишь прежнюю!')

        elif type == "USER_STATE_BY_CHATID":
            try:
                with connection_data.cursor() as cursor:
                    cursor.execute(command[0].format(f'room{values[0]}'), [values[1]])
                    state = cursor.fetchone()[0]
                    connection_data.close()
                    return state
            except:
                return False

        elif type == "ENOUGH_PLAYERS":
            with connection_data.cursor() as cursor:
                cursor.execute(command[0].format(f'room{values}'))
                count = cursor.fetchone()[0]
                connection_data.close()
                return count

        elif type == "ROLES_GIVE":
            return fn_rolesgive(connection_data, command, values)

        elif type == "USER_STATE_BY_USERID":
            with connection_data.cursor() as cursor:
                cursor.execute(command[0], [values])
                try:
                    room_number = cursor.fetchone()[0]
                    cursor.execute(command[1].format(f"room{room_number}"), [values])
                    user_state = cursor.fetchone()[0]
                    connection_data.close()
                    return user_state
                except:
                    pass

        elif type == "USER_ROOM":
            with connection_data.cursor() as cursor:
                cursor.execute(command[0], [values])
                try:
                    room_number = cursor.fetchone()[0]
                    connection_data.close()
                    return room_number
                except:
                    pass

        elif type == "ROLE_CHOICE":

            return fn_rolechoice(connection_data, command, values)

        elif type == 'WHO_IS_ALIVE':

            return fn_whoisalive(connection_data, command, values)

        elif type == 'PLAYERS_VOTE':
            
            with connection_data.cursor() as cursor:
                cursor.execute(command[0].format(f'room{values[0]}'))
                users = {k[-1]: v for k, v in cursor.fetchall()}
                choice = values[2]

                if values[1] == users.get(choice):
                    del users[choice]
                    choice = random.choice(list(users.keys()))

                if choice == 'спать':
                    users[choice] = -1

                if choice in users.keys():
                    cursor.execute(command[1].format(f'room{values[0]}'), [users.get(choice), values[1]])
                    cursor.execute(command[2].format(f'room{values[0]}'), [values[1]])

                    cursor.execute(command[3].format(f'room{values[0]}'))
                    results = [r[0] for r in cursor.fetchall()]
                    if None in results:
                        connection_data.close()
                        return [True, False, None]
                    else:
                        cursor.execute(command[4].format("rooms", "poll_deadline", "room"), [None, values[0]]) # reset poll_deadline in rooms
                        votes = {}
                        for i in results:
                            if i not in votes.keys():
                                votes[i] = 1
                            else:
                                quantity = votes.get(i) + 1
                                votes[i] = quantity

                        connection_data.close()
                        return [True, True, votes]
                else:
                    connection_data.close()
                    return [False, False, None]

        elif type == 'POLL_RESULTS':

            return fn_pollresults(connection_data, command, values)

        elif type == 'ROOM-2':
            with connection_data.cursor() as cursor:
                cursor.execute(command[0], [-2, values])
                connection_data.close()
            return

        elif type == 'AVAILABLE_ROOM':
            with connection_data.cursor() as cursor:
                try:
                    room = lambda: (cursor.execute(command[0]), cursor.fetchone()[0])[1]
                    room = room()
                except:
                    room = None

                if room is not None:
                    cursor.execute(command[1], [room])
                    return room
                else:
                    return room

        elif type == 'BOOK_ROOM':
            print(1)


        connection_data.close()
        return command
    return wrapper


@db_connection
def execute_sql_command(type, values):
    pass


if __name__ == '__main__':
    pass

