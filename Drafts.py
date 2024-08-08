#database
# if roles[0] == 'Дон':
#     print('nobody')
#
# elif roles[0] == 'Мафия':  # don kills mafia
#     if roles[1] != 'Мафия':  # hoe didn't chose mafia
#         if roles[2] != 'Мафия':  # doctor didn't choose mafia
#             if roles[3] != 'Мафия':  # bodyguard didn't choose mafia
#                 print('mafia dead')
#             else:
#                 print('mafia saved, but bodyguard dead')  # bodyguard saved but died himself
#         else:
#             print('mafia saved')  # doctor saved
#     else:
#         print('mafia saved')  # hoe saved
#
# elif roles[0] == 'Проститутка':  # don kills hoe
#     if roles[2] != 'Проститутка':  # doctor didn't chose hoe
#         if roles[3] != 'Проститутка':  # bodyguard didn't choose hoe
#             if roles[1] != roles[2]:  # if not doctor didn't choose the same guy as hoe
#                 if roles[1] != roles[3]:  # if not bodyguard didn't choose the same guy as hoe
#                     print('hoe dead')
#                     print('the guy that hoe chose dead')
#                 else:
#                     print('hoe dead and the guy hoe chose saved but bodyguard dead')
#             else:
#                 print('hoe dead and the guy hoe chose saved')
#         else:
#             print('hoe saved')  # bodyguard saved but died himself
#     else:
#         print('hoe and the guy she chose are saved')  # doctor saved
#
# elif roles[0] == 'Комиссар':  # don kills comissar
#     if roles[1] != 'Комиссар':  # hoe didn't chose comissar
#         if roles[2] != 'Комиссар':  # doctor didn't choose comissar
#             if roles[3] != 'Комиссар':  # bodyguard didn't choose comissar
#                 print('comissar dead')
#             else:
#                 print('comissar saved, but bodyguard dead')  # bodyguard saved but died himself
#         else:
#             print('comissar saved')  # doctor saved
#     else:
#         print('comissar saved')  # hoe saved
#
# elif roles[0] == 'Сержант':  # don kills sergiant
#     if roles[1] != 'Сержант':  # hoe didn't chose sergiant
#         if roles[2] != 'Сержант':  # doctor didn't choose sergiant
#             if roles[3] != 'Сержант':  # bodyguard didn't choose sergiant
#                 print('sergiant dead')
#             else:
#                 print('sergiant saved, but bodyguard dead')  # bodyguard saved but died himself
#         else:
#             print('sergiant saved')  # doctor saved
#     else:
#         print('sergiant saved')  # hoe saved
#
# elif roles[0] == 'Доктор':  # don kills doctor
#     if roles[1] != 'Доктор':  # hoe didn't choose doctor
#         if roles[2] != 'Доктор':  # doctor didn't choose doctor
#             if roles[3] != 'Доктор':  # bodyguard didn't choose doctor
#                 print('doctor dead')
#             else:
#                 print('doctor saved, but bodyguard dead')  # bodyguard saved but died himself
#         else:
#             print('doctor saved')  # doctor saved
#     else:
#         print('doctor saved')  # hoe saved
#
# elif roles[0] == 'Телохранитель':  # don kills bodyguard
#     if roles[1] != 'Телохранитель':  # hoe didn't choose bodyguard
#         if roles[2] != 'Телохранитель':  # doctor didn't choose bodyguard
#             print('bodyguard dead')
#         else:
#             print('bodyguard saved')  # doctor saved
#     else:
#         print('bodyguard saved')  # hoe saved
#
# elif roles[0] == 'Мститель':  # don kills revenger
#     if roles[1] != 'Мститель':  # hoe didn't choose revenger
#         if roles[2] != 'Мститель':  # doctor didn't choose revenger
#             if roles[3] != 'Мститель':  # bodyguard didn't choose revenger
#                 print('revenger dead')
#             else:
#                 print('revenger saved, but bodyguard dead')  # bodyguard saved but died himself
#         else:
#             print('revenger saved')  # doctor saved
#     else:
#         print('revenger saved')  # hoe saved
#
# elif roles[0] == 'Суицидник':  # don kills suicide
#     if roles[1] != 'Суицидник':  # hoe didn't choose suicide
#         if roles[2] != 'Суицидник':  # doctor didn't choose suicide
#             if roles[3] != 'Суицидник':  # bodyguard didn't choose suicide
#                 print('suicide dead')
#             else:
#                 print('suicide saved, but bodyguard dead')  # bodyguard saved but died himself
#         else:
#             print('suicide saved')  # doctor saved
#     else:
#         print('suicide saved')  # hoe saved
#
# elif roles[0] == 'Мирный':  # don kills citizen
#     if roles[1] != 'Мирный':  # hoe didn't choose citizen
#         if roles[2] != 'Мирный':  # doctor didn't choose citizen
#             if roles[3] != 'Мирный':  # bodyguard didn't choose citizen
#                 print('citizen dead')
#             else:
#                 print('citizen saved, but bodyguard dead')  # bodyguard saved but died himself
#         else:
#             print('citizen saved')  # doctor saved
#     else:
#         print('citizen saved')  # hoe saved