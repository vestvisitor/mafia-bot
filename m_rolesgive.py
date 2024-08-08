from rules import *
from methods import *
import datetime

def fn_rolesgive(connection_data, command, values):
    with connection_data.cursor() as cursor:
        cursor.execute(command[0].format(f'room{values[0]}'))
        ids_roles = {key[0]: value for (key, value) in zip(cursor.fetchall(), values[1])}

        cursor.execute(command[1].format(f'room{values[0]}'))
        usernames = [f"{u[0]} {s}" for u, s in zip(cursor.fetchall(), icons(len(values[1])))]

        (lambda: [cursor.execute(command[2].format(f'room{values[0]}'), [username, id]) for username, id in
                  zip(usernames, list(ids_roles.keys()))])()
        (lambda: [cursor.execute(command[3].format(f'room{values[0]}'), [v, k]) for k, v in ids_roles.items()])()
        (lambda: [cursor.execute(command[4].format(f'room{values[0]}'), [0, k]) for k, v in ids_roles.items() if
                  v in ["Дон", 'Мафия', 'Проститутка']])()

        roles = ", ".join(get_scenario(len(values[1])))  # need to shuffle the roles
        cursor.execute(command[1].format(f'room{values[0]}'))
        players = [str(u[0]) for u in cursor.fetchall()]

        players_buttons = [p.split()[-1] for p in players]
        random.shuffle(players_buttons)

        players_list = ""
        for i, p in enumerate(players):
            players_list += f"{i + 1}) {p}\n"

        message_to_group = "😎 Игра началась!\n" \
                           f"📽 Действующие роли: {roles}.\n" \
                           f"Список игроков:\n{players_list}" \
                           f"💤 Наступает ночь 1-ого дня! Город засыпает, просыпается..."

        messages_to_players = {k: get_role_description(v) for (k, v) in ids_roles.items()}

        cursor.execute(command[5].format(f'room{values[0]}'))  # set everyone to 0 state

        fn_set_last_role_deadline = lambda role, room, timestamp: (
        cursor.execute(command[9].format(f"last_role"), [role, room]),
        cursor.execute(command[9].format(f"action_deadline"), [timestamp, room]))

        if 'Дон' in values[1]:
            cursor.execute(command[6].format(f'room{values[0]}'), [get_role_state('Дон'), 'Дон'])
            cursor.execute(command[7].format(f'room{values[0]}'), ['Дон'])
            mafia_id = cursor.fetchone()[0]

            fn_set_last_role_deadline('Дон', values[0], get_current_time(15).strftime("%d-%m-%Y %H:%M:%S"))
        else:
            cursor.execute(command[6].format(f'room{values[0]}'), [get_role_state('Мафия'), 'Мафия'])
            cursor.execute(command[7].format(f'room{values[0]}'), ['Мафия'])
            mafia_id = cursor.fetchone()[0]

            fn_set_last_role_deadline('Мафия', values[0], get_current_time(15).strftime("%d-%m-%Y %H:%M:%S"))

        cursor.execute(command[8], [values[0]])  # set to NULL game_expires in rooms

        connection_data.close()
        return [message_to_group, messages_to_players, mafia_id, players_buttons, players_list]