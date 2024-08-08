import asyncio
from asyncio import sleep

lis = ['Мафия', 'Комиссар', 'Доктор', 'Суицидник']
#
#
# try:
#     nex_role = next((lis[i+1] for i, r in enumerate(lis) if r == 'Доктор'))
# except Exception as ex:
#     print(ex)
#
# print(nex_role)

# kek = lambda: (print(1), print(2))
# kek()
#
# gen = (l for l in lis)
# print()

import threading, time, datetime

# def check(n):
#     for i in range(n):
#         print(i)
#         time.sleep(1)
#
# x = threading.Thread(target=check, args=(100,))
# x.start()
#
# print(1)



# current_time = datetime.datetime.now()
# future_time = current_time + datetime.timedelta(seconds=60)
#
# while True:
#     current_time = datetime.datetime.now()
#     if current_time.strftime("%Y-%m-%d %H:%M:%S") == future_time.strftime("%Y-%m-%d %H:%M:%S"):
#         print('reached')
#         print(current_time)
#         break
#     else:
#         time.sleep(1)
#
# print('finished')

la = 'kek'

print(la)

la += 's'

print(la)
#add seconds or minute




