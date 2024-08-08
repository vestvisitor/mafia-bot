from bot import session
from keyboards import *


def send_message_to_chat(chat_id, message):
    session.method("messages.send", {
        "chat_id": chat_id,
        "message": message,
        "random_id": 0
    })


def send_message_to_user_keyboard(user_id, message, keyboard):
    session.method("messages.send", {
        "user_id": user_id,
        "message": message,
        "random_id": 0,
        "keyboard": keyboard
    })


def send_message_to_user(user_id, message):
    session.method("messages.send", {
        "user_id": user_id,
        "message": message,
        "random_id": 0
    })


def send_message_with_join_button(chat_id, message):
    session.method("messages.send", {
        "chat_id": chat_id,
        "message": message,
        "random_id": 0,
        "keyboard": get_join_keybutton()
    })


def send_message_with_empty_keyboard(chat_id, message):

    if chat_id > 2000000000:
        chat_id = chat_id - 2000000000

    session.method("messages.send", {
        "chat_id": chat_id,
        "message": message,
        "random_id": 0,
        "keyboard": get_empty_keyboard()
    })


def send_message_with_keyboard_to_chat(chat_id, message, keyboard):
    session.method("messages.send", {
        "chat_id": chat_id,
        "message": message,
        "random_id": 0,
        "keyboard": keyboard
    })


def create_chat_group(host_id):
    session.method("messages.createChat", {
        "user_ids": f"*{host_id}",
        "title": "Mafia123",
        "group_id": 217355254,
    })


def get_invitation(chat_id):
    if chat_id < 2000000000:
        chat_id = chat_id + 2000000000

    invitation = session.method("messages.getInviteLink", {
        "peer_id": chat_id,
        "reset": 1
    })['link']

    return invitation


def delete_user(chat_id, user_id):
    if chat_id > 2000000000:
        chat_id = chat_id - 2000000000

    session.method("messages.removeChatUser", {
        "chat_id": chat_id,
        "user_id": user_id
    })


def create_chat(user_id):

    cov = session.method("messages.createChat", {
        "user_ids": f"*{user_id}",
        "title": "Мафия"
    })

    return cov


def get_list_of_conversations():
    conversations = session.method("messages.getConversations", {
        "filter": "all"
    })['items']

    empty_rooms = []
    print(conversations)

    for c in conversations:
        print(c)
        # number_of_members = c.get('conversation').get('chat_settings').get('members_count')

        # if number_of_members == 1:
        #     chat_id = c.get('conversation').get('peer').get('id')
        #     empty_rooms.append(chat_id)

    print(empty_rooms)




# def delete_message(peer_id):
#     session.method("messages.getConversations",{
#         "delete_for_all": 1,
#         "peer_id": peer_id,
#         "cmids": 0
#     })