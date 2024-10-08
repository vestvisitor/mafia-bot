import random
import datetime

def get_current_time(seconds):
    current_time = datetime.datetime.now()
    if seconds is None:
        return current_time
    else:
        future_time = current_time + datetime.timedelta(seconds=seconds)
        return future_time

def get_scenario(number):
    scenarios = {4: ["Мафия", "Комиссар", "Доктор", "Суицидник"],
                    5: ["Мафия", "Проститутка", "Комиссар", "Доктор", "Суицидник"],
                     6: ["Мафия", "Проститутка", "Комиссар", "Сержант", "Доктор", "Суицидник"],
                     7: ["Дон", "Мафия", "Проститутка", "Комиссар", "Сержант", "Доктор", "Суицидник"],
                     8: ["Дон", "Мафия", "Проститутка", "Комиссар", "Сержант", "Доктор", "Мститель", "Суицидник"],
                     9: ["Дон", "Мафия", "Проститутка", "Комиссар", "Сержант", "Доктор", "Телохранитель", "Мститель", "Суицидник"],
                    10: ["Дон", "Мафия", "Проститутка", "Комиссар", "Сержант", "Доктор", "Телохранитель", "Мститель", "Суицидник", "Мирный"]
                 }

    return scenarios.get(number)


def get_active_roles(number):
    scenarios = {4: ["Мафия", "Комиссар", "Доктор"],
                    5: ["Мафия", "Проститутка", "Комиссар", "Доктор"],
                     6: ["Мафия", "Проститутка", "Комиссар", "Сержант", "Доктор"],
                     7: ["Дон", "Мафия", "Проститутка", "Комиссар", "Сержант", "Доктор"],
                     8: ["Дон", "Мафия", "Проститутка", "Комиссар", "Сержант", "Доктор"],
                     9: ["Дон", "Мафия", "Проститутка", "Комиссар", "Сержант", "Доктор", "Телохранитель"],
                    10: ["Дон", "Мафия", "Проститутка", "Комиссар", "Сержант", "Доктор", "Телохранитель"]
                 }

    return scenarios.get(number)


def role_word_form(role):

    roles = {'Мафия': "Мафию", "Комиссар": "Комиссара", "Сержант": "Сержанта", "Доктор": "Доктора", "Телохранитель": "Телохранителя", "Мститель": "Мстителя", "Суицидник": "Суицидника", "Мирный": "Мирного"}

    result = roles.get(role)

    return result
def icons(number):
    all_smiles = ['🐵', '🐶', '🐺', '🦝', '🦊', '🐱', '🦁', '🐯', '🐮', '🐷', '🐗', '🦒', '🐭', '🐹', '🐰', '🐻', '🐨', '🐼', '🐸']
    smiles = []
    for s in range(number):
        smile = random.choice(all_smiles)
        smiles.append(smile)
        all_smiles.remove(smile)
    return smiles


def get_role_state(role):

    states = {'Дон': 2,
        'Мафия': 3,
        'Проститутка': 4,
        'Комиссар': 5,
        'Сержант': 6,
        'Доктор': 7,
        'Телохранитель': 8,
        'Мститель': 9,
        "Суицидник": 10,
        "Мирный": 11}

    # states = {
    #     'Мафия': 2,
    #     # "Проститутка": 5,
    #     'Комиссар': 3,
    #     'Доктор': 4
    #     # "Суицидник": 5
    # }

    return next((lambda: (v for (k, v) in states.items() if k == role))())


def get_role_description(role):

    description = {'Дон': "🤵 Твоя роль - Дон.\n👹 Ты чисто босс, глава мафии, все по сравнению с тобой шестерки! От твоего решения зависит чья-то жизнь! Выбрав себя, ты пытаешься снять с себя подозрения.",
        'Мафия': "😈 Твоя роль - Мафия.\n😎 Ты авторитетный чел, который в отсутствии Дона по каким-то причинам, вершит судьбу чьей-то жизни. Выбрав себя, ты пытаешься снять с себя подозрения.",
        'Проститутка': "👯‍♀ Твоя роль - Проститутка.\n🔞 Ты та самая девочка с района, работающая на мафию. Твоя задача качественно обслуживать клиентов! Выбрав себя, ты пытаешься снять с себя подозрения.",
        'Комиссар': "🕵‍♂ Твоя роль - Комиссар. 🕵‍♀\n👏 На тебя возлагаются все надежды мирного населения. Твое расследование играет ключевую роль в победе мирных жителей!",
        'Сержант': "👮‍♂ Твоя роль - Сержант. 👮‍♀\n🤠 Ты второй комиссар, при случае тебе придется заступить на должность и начать сообственное расследование. А пока что можешь наслаждаться беззаботной игрой.",
        'Доктор': "👨‍⚕ Твоя роль - Доктор. 👩‍⚕\n🤞 На тебя возлагаются все надежды мирного населения. Твои старания могут быть недооценены сразу, но поверь, твое чутье определяет многое!",
        "Телохранитель": "💂‍♀ Твоя роль - Телохранитель.\n🛡 Твоя задача благородно принять удар на себя при покушении на выбранного тобою человека. Ну а если тебе станет себя жалко, можешь просто выбрать себя.",
        'Мститель': "🦸‍♂ Твоя роль - Мститель. 🦸‍♀\n😼 Ты, как супергерой, можешь быть как плохим, так и хорошим персонажем, все зависит от твоего чутья - кого в случае своей смерти ты заберешь с собой.",
        "Суицидник": "🤯 Твоя роль - Суицидник.\n😏 Ты та самая черная лошадка, к которой все будут относится с осторожностью. Твоя задача - обмануть все населения на дневное убийство тебя!",
        "Мирный": "🙎‍♂ Твоя роль - Мирный. 🙎‍♀\n🤷‍♂ Ты просто мирный житель, ничего особенного. Может быть в следующий раз выпадет кто поинтереснее! 🤷‍♀"}

    return next((lambda: (v for (k, v) in description.items() if k == role))())


def get_message_for_role(role):

    messages = {
        'Дон': f"🚬 Выбирай с кем сегодня ночью расправится твоя мафия!",
        'Мафия': f"🔪 Выбирай кто сегодня ночью умрет!",
        "Проститутка": f"🖤 Выбирай, кто сегодня будет счастливчиком!",
        'Комиссар': f"🔎 Выбирай, кого сегодня ночью проверить!",
        'Сержант': f"🔦 Выбирай, к кому сегодня заглянуть с проверкой!",
        'Доктор': f"💊 Выбирай, кого сегодня ночью вылечить!",
        "Телохранитель": f"🛡 Выбирай, ради кого сегодня ночью ты пожертвуешь собой в случае его смерти!",
        "Мститель": f"☠ Выбирай, кого с собой ты утянешь в могилу!"
    }

    return messages.get(role)


def messages_to_group_while_actions(role):

    messages = {
        'Дон': f"🚬 Дон дает своей Мафии указания...",
        'Мафия': f"🔪 Мафия делает свои грязные делишки...",
        "Проститутка": f"🔞 Спутница любви обслуживает клиента...",
        'Комиссар': f"🔍 Комиссар допрашивает подозреваемых...",
        "Сержант": f"🔦 Сержант устраивает проверку...",
        'Доктор': f"💉 Доктор проводит сложную операцию...", #добавить возможность вакцинации 50% что даст игроку иммунитет от мафии на 5 ходов, 50% что убьъет игрока.
        "Телохранитель": f"🛡 Телохранитель внимательно выполняет свою работу..."
    }

    return messages.get(role)


if __name__ == '__main__':
    # icons(4)
    print(get_role_description('Мафия'))
    print(get_role_state('Мафия'))
