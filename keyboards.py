import json


def get_button(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


def get_join_keybutton():
    join_keyboard = {
        "one_time": False,
        "buttons": [
            [get_button('Присоединиться', 'positive')]
        ]
    }

    join_keyboard = json.dumps(join_keyboard, ensure_ascii=False).encode('utf-8')
    join_keyboard = str(join_keyboard.decode('utf-8'))

    return join_keyboard


def get_empty_keyboard():
    empty_keyboard = {
        "one_time": False,
        "buttons": []
    }

    empty_keyboard = json.dumps(empty_keyboard, ensure_ascii=False).encode('utf-8')
    empty_keyboard = str(empty_keyboard.decode('utf-8'))

    return empty_keyboard


def users_keyboard(users, where_to): # 1 - to user, 0 - to chat

    if len(users) <= 5:

        row1 = [get_button(u, 'positive') for u in users]

        if where_to == 0:
            row2 = [get_button('Спать', 'negative')]
            buts = [row1, row2]

            users_buttons = {
                "one_time": False,
                "buttons": buts
            }

            users_buttons = json.dumps(users_buttons, ensure_ascii=False).encode('utf-8')
            users_buttons = str(users_buttons.decode('utf-8'))
            return users_buttons

        elif where_to == 1:

            users_buttons = {
                "one_time": True,
                "buttons": [row1]
            }

            users_buttons = json.dumps(users_buttons, ensure_ascii=False).encode('utf-8')
            users_buttons = str(users_buttons.decode('utf-8'))

            return users_buttons

    elif 5 < len(users) <= 10:

        row1 = [get_button(u, 'positive') for i, u in enumerate(users) if i+1 <= 5]
        row2 = [get_button(u, 'positive') for i, u in enumerate(users) if 5 < i+1 <= 10]
        buts = [row1, row2]

        if where_to == 0:
            buts.append([get_button('Спать', 'negative')])

            users_buttons = {
                "one_time": False,
                "buttons": buts
            }

            users_buttons = json.dumps(users_buttons, ensure_ascii=False).encode('utf-8')
            users_buttons = str(users_buttons.decode('utf-8'))
            return users_buttons

        elif where_to == 1:

            users_buttons = {
                "one_time": True,
                "buttons": buts
            }

            users_buttons = json.dumps(users_buttons, ensure_ascii=False).encode('utf-8')
            users_buttons = str(users_buttons.decode('utf-8'))
            return users_buttons


def get_join_or_look_button():
    keyboard = {
        "one_time": False,
        "buttons": [
            [get_button('Играть', 'positive')],
            [get_button('Присоединиться', 'positive')]
        ]
    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

    return keyboard

def get_join_inline(link):
    keyboard = {
          "inline": True,
          "buttons": [
            [
              {
                "action": {
                  "type": "open_link",
                  "link": link,
                  "label": "Присоединиться"
                }
              }
            ]
          ]
        }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

    return keyboard