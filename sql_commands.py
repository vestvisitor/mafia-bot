def commands_handler(type):
    if type == "INSERT_ALL_USERS":
        return ["SELECT userid FROM all_users WHERE userid = %s",
                "INSERT INTO all_users (username, userid) VALUES (%s,%s)"]

    elif type == 'ALL_USERS_TABLE':
        return ["""CREATE TABLE {} ( 
                    id serial PRIMARY KEY,
                    username varchar(120) NOT NULL,
                    userid integer NOT NULL,
                    room integer DEFAULT NULL
                )"""]

    elif type == "CREATE_ROOM":
        return ["SELECT room FROM all_users WHERE userid = %s", # 0
                "SELECT * FROM information_schema.tables where table_name = %s", # 1
                """CREATE TABLE {} ( 
                    id serial PRIMARY KEY,
                    username varchar(120) NOT NULL,
                    userid integer NOT NULL,
                    user_role varchar(50),
                    is_good smallint DEFAULT 1,
                    is_alive smallint DEFAULT 1,
                    mafia_choice smallint DEFAULT 0,
                    hoe_choice smallint DEFAULT 0,
                    doctor_choice smallint DEFAULT 0,
                    bodyguard_choice smallint DEFAULT 0,
                    user_state smallint,
                    poll_vote integer
                )""", # 2
                "INSERT INTO {} (username, userid, user_state) VALUES (%s, %s, 1)", # 3
                "UPDATE all_users SET room = %s WHERE userid = %s", # 4
                "INSERT INTO rooms (room, game_expires, actions_history) VALUES (%s, %s, %s)" # 5
                ]

    elif type == "CHECK_TIME":
        return ["SELECT {} FROM {}", # 0
                "SELECT room FROM rooms WHERE {} = %s", # 1
                "SELECT COUNT(id) FROM {}", # 2
                "SELECT userid FROM {}", # 3
                "UPDATE all_users SET room = NULL WHERE userid = %s",  # 4
                "DROP TABLE {}", # 5
                "DELETE FROM rooms WHERE room = %s", # 6
                "SELECT last_role FROM rooms WHERE room = %s", # 7
                "SELECT username, userid FROM {} WHERE user_role = %s", # 8
                "UPDATE {} SET {} = %s WHERE {} = %s", # 9
                "UPDATE {} SET {} = %s", # 10
                "SELECT {} FROM {} WHERE {} = %s", # 11
                ]

    elif type == 'JOIN_ROOM':
        return ["SELECT * FROM information_schema.tables where table_name = %s", # 0
                "SELECT room FROM all_users WHERE userid = %s", # 1
                "SELECT userid FROM {} WHERE userid = %s", # 2
                "INSERT INTO {} (username, userid, user_state) VALUES (%s, %s, 0)", # 3
                "UPDATE all_users SET room = %s WHERE userid = %s", # 4
                "SELECT count(id) FROM {}", # 5
                "SELECT user_role FROM {}" # 6
                ]

    elif type == 'USER_STATE_BY_CHATID':
        return ["SELECT user_state FROM {} WHERE userid = %s"]

    elif type == 'ENOUGH_PLAYERS':
        return ["SELECT count(id) FROM {}"]

    elif type == 'ROLES_GIVE':
        return ["SELECT userid FROM {}",
                "SELECT username FROM {}",
                "UPDATE {} SET username = %s WHERE userid = %s",
                "UPDATE {} SET user_role = %s WHERE userid = %s",
                "UPDATE {} SET is_good = %s WHERE userid = %s",
                "UPDATE {} SET user_state = 0 WHERE user_state = 1",
                "UPDATE {} SET user_state = %s WHERE user_role = %s", # 6
                "SELECT userid FROM {} WHERE user_role = %s", # 7
                "UPDATE rooms SET game_expires = NULL WHERE room = %s", # 8
                "UPDATE rooms SET {} = %s WHERE room = %s", # 9
                ]

    elif type == 'USER_ROOM' or type == 'USER_STATE_BY_USERID':
        return ["SELECT room FROM all_users WHERE userid = %s",
                "SELECT user_state FROM {} WHERE userid = %s"]

    elif type == 'WHO_IS_ALIVE':
        return ["SELECT room FROM all_users WHERE userid = %s", # 0
                "SELECT COUNT(id) FROM {}", # 1
                "UPDATE {} SET user_state = %s WHERE user_role = %s", # 2
                "SELECT userid FROM {} WHERE user_role = %s", # 3
                "SELECT is_alive FROM {} WHERE user_role = %s", # 4 
                "SELECT username FROM {} WHERE is_alive = 1", # 5
                "SELECT is_good FROM {} WHERE username = %s", # 6
                #except part
                "SELECT {} FROM {} WHERE {} = 1",  # 7
                "SELECT is_alive FROM {} WHERE {} = %s",  # 8
                "UPDATE {} SET is_alive = %s WHERE {} = %s", # 9
                "SELECT username, userid, user_role FROM {} WHERE is_alive = 0",  # 10
                "UPDATE all_users SET room = NULL WHERE userid = %s", # 11
                "UPDATE {} SET user_state = 88 WHERE is_alive = 1", # 12
                "SELECT user_role FROM {} WHERE is_alive = 1", # 13
                "SELECT userid FROM {} WHERE is_alive IS NOT NULL",  # 14
                "DROP TABLE {}", # 15
                "UPDATE {} SET (is_alive, user_state) = (NULL, NULL) WHERE userid = %s", # 16
                "UPDATE {} SET {} = %s WHERE {} = %s",  # 17
                "SELECT {} FROM {} WHERE {} = %s", # 18
                "UPDATE {} SET {} = %s WHERE {} = %s", # 19
                "DELETE FROM rooms WHERE room = %s" # 20
                ]

    elif type == 'ROLE_CHOICE':
        return ["SELECT username, userid, user_role FROM {} WHERE is_alive = 1", # 0
                "UPDATE {} SET {} = %s WHERE {} = %s", # 1 
                "UPDATE {} SET user_state = %s WHERE user_role = %s", # 2
                "SELECT {} FROM {} WHERE user_role = %s", # 3
                "SELECT user_role FROM {} WHERE {} = 1", # 4
                "UPDATE {} SET {} = 0", # 5
                "UPDATE {} SET is_good = 0 WHERE user_role = %s", # 6
                "SELECT {} FROM {} WHERE is_alive = 1", # 7
                "UPDATE {} SET (is_alive, user_state) = (NULL, NULL) WHERE {} = %s",  # 8
                "UPDATE all_users SET room = NULL WHERE userid = %s", # 9
                "SELECT userid FROM {} WHERE is_alive = 1", # 10
                "DROP TABLE {}", # 11
                "UPDATE {} SET user_state = 88 WHERE is_alive = 1", # 12
                "SELECT COUNT(userid) FROM {}",  # 13
                "SELECT game_day FROM rooms WHERE room = %s",  # 14
                "UPDATE rooms SET game_day = %s WHERE room = %s"  # 15
                ]

    elif type == 'PLAYERS_VOTE':
        return ["SELECT username, userid FROM {} WHERE is_alive = 1", # 0
                "UPDATE {} SET poll_vote = %s WHERE userid = %s", # 1
                "UPDATE {} SET user_state = 0 WHERE userid = %s", # 2
                "SELECT poll_vote FROM {} WHERE is_alive = 1", # 3
                "UPDATE {} SET {} = %s WHERE {} = %s" # 4
                ]

    elif type == 'POLL_RESULTS':
        return ["UPDATE {} SET poll_vote = NULL WHERE is_alive = 1", # 0
                "SELECT username, user_role FROM {} WHERE userid = %s", # 1
                "UPDATE {} SET is_alive = NULL WHERE userid = %s", # 2
                "UPDATE all_users SET room = NULL WHERE userid = %s", # 3
                "SELECT userid FROM {} WHERE is_alive = 1", # 4
                "UPDATE all_users SET room = NULL WHERE userid = %s", # 5
                "DROP TABLE {}", # 6
                "SELECT user_role FROM {} WHERE is_alive = 1", # 7
                "UPDATE {} SET user_state = %s WHERE user_role = %s", # 8
                "SELECT username FROM {} WHERE is_alive = 1", # 9
                "SELECT {} FROM {} WHERE user_role = %s", # 10
                "UPDATE {} SET {} = %s", # 11
                "SELECT {} FROM {} WHERE {} = %s", # 12
                "UPDATE {} SET {} = %s WHERE user_role = %s", # 13
                "SELECT game_day FROM rooms WHERE room = %s",  # 14
                "UPDATE rooms SET game_day = %s WHERE room = %s",  # 15
                "UPDATE {} SET {} = %s WHERE {} = %s",  # 16
                "DELETE FROM rooms WHERE room = %s", # 17
                "SELECT {} FROM {} WHERE user_role = %s AND is_alive = 1" # 18
                ]

    elif type == 'ROOM-2':
        return ["UPDATE all_users SET room = %s WHERE userid = %s"
                ]

    elif type == 'AVAILABLE_ROOM':
        return ["SELECT room_id FROM community_rooms WHERE available = 1",
                "UPDATE community_rooms SET available = 0 WHERE room_id = %s"
                ]


    elif type == 'BOOK_ROOM':
        return [""
                ]