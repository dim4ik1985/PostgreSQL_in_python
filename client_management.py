import psycopg2


class DbCreate:
    def __init__(self, db, user, password):
        self.db = psycopg2.connect(
            database=db,
            user=user,
            password=password
        )

    # ---Функция, создающая структуру БД(таблицы)
    def create_table(self):
        try:
            with self.db.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    name_user VARCHAR(20) NOT NULL,
                    lastname_user VARCHAR(30) NOT NULL,
                    email VARCHAR(50) NOT NULL
                );
                """)

                cur.execute("""
                CREATE TABLE IF NOT EXISTS users_phone(
                    id SERIAL PRIMARY KEY,
                    phone_user VARCHAR(50),
                    user_id INTEGER NOT NULL REFERENCES users(id)
                );
                """)
                print('[INFO] Table created successfully')
        except Exception as error:
            print(f'[INFO] {error}')
        finally:
            if self.db:
                self.db.commit()
                self.db.close()
                print("[INFO] PostgresSQL connection closed")

    # ---Функция, позволяющая добавить нового клиента
    def insert_user(self, n_user, l_user, email, phone=None):
        try:
            with self.db.cursor() as cur:
                cur.execute("""
                    SELECT email FROM users WHERE email=%s;
                """, (email,))
                if cur.fetchone() is None:
                    cur.execute("""
                        INSERT INTO users(name_user, lastname_user, email) VALUES (%s, %s, %s) RETURNING id;
                    """, (n_user, l_user, email))
                    request = cur.fetchone()[0]
                    if phone:
                        cur.execute("""
                            INSERT INTO users_phone(phone_user, user_id) VALUES (%s, %s);
                        """, (phone, request))
                    print(f'Пользователь {n_user} {l_user} успешно добавлен!')
                else:
                    print(f'Пользователь с email {email} уже существует!')
        except Exception as _er:
            print('[INFO] Error while working with PostgreSQL', _er)
        finally:
            if self.db:
                self.db.commit()
                self.db.close()
                print('[INFO] PostgresSQL connection closed')

    # ---Функция, позволяющая добавить телефон для существующего клиента
    def add_phone(self, email, phone):
        try:
            with self.db.cursor() as cur:
                cur.execute("""
                    SELECT id FROM users WHERE email=%s;
                """, (email,))
                request_id = cur.fetchone()[0]
                if request_id is None:
                    print('[INFO] User is not found!')
                else:
                    cur.execute("""
                        SELECT * FROM users_phone WHERE phone_user=%s;
                    """, (phone,))
                    if cur.fetchone():
                        print(f'[INFO] Number {phone} already exists')
                    else:
                        cur.execute("""
                            INSERT INTO users_phone(phone_user, user_id) VALUES (%s, %s);
                        """, (phone, request_id))
                        print(f'[INFO] Phone {phone} successfully added')
        except Exception as _er:
            print('[INFO] Error while working with PostgreSQL', _er)
        finally:
            if self.db:
                self.db.commit()
                self.db.close()
                print('[INFO] PostgreSQL connection closed')

    # ---Функция, позволяющая изменить данные о клиенте
    def to_change_data(self, item, old_item, new_item):
        try:
            with self.db.cursor() as cur:
                if item == 'phone':
                    cur.execute("""
                        SELECT phone_user FROM users_phone WHERE phone_user=%s;
                    """, (old_item,))
                    if cur.fetchone():
                        cur.execute("""
                            UPDATE users_phone SET phone_user = %s WHERE phone_user=%s;
                        """, (new_item, old_item))
                        print(f'{item.capitalize()} changed')
                    else:
                        print('Wrong data')
                else:
                    cur.execute("""
                        SELECT * FROM users WHERE name_user=%s OR lastname_user=%s OR email=%s;
                    """, (old_item, old_item, old_item))
                    if cur.fetchone():
                        if item == 'name':
                            cur.execute("""
                                UPDATE users SET name_user = %s WHERE name_user=%s;
                            """, (new_item, old_item))
                        elif item == 'lastname':
                            cur.execute("""
                                UPDATE users SET lastname_user = %s WHERE lastname_user=%s;
                            """, (new_item, old_item))
                        elif item == 'email':
                            cur.execute("""
                                UPDATE users SET email = %s WHERE email=%s;
                            """, (new_item, old_item))
                        print(f'{item.capitalize()} changed')
                    else:
                        print('Wrong data')
        except Exception as _er:
            print('[INFO] Error while working with PostgreSQL', _er)
        finally:
            if self.db:
                self.db.commit()
                self.db.close()
                print('[INFO] PostgreSQL connection closed')

    # ---Функция, позволяющая удалить телефон для существующего клиента
    def del_phone(self, email, phone):
        try:
            with self.db.cursor() as cur:
                cur.execute("""
                    SELECT * FROM users WHERE email=%s;
                """, (email,))
                request_id = cur.fetchone()[0]
                if request_id:
                    cur.execute("""
                        SELECT * FROM users_phone WHERE phone_user=%s AND user_id=%s;
                    """, (phone, request_id))
                    if cur.fetchone():
                        cur.execute("""
                            DELETE FROM users_phone WHERE phone_user=%s AND user_id=%s;
                        """, (phone, request_id))
                        print(f'[INFO] Phone delete')
                    else:
                        print('[INFO]Phone not found!')
                else:
                    print(f'[INFO] User does not exist')
        except Exception as _er:
            print('[INFO] Error while working with PostgreSQL', _er)
        finally:
            if self.db:
                self.db.commit()
                self.db.close()
                print('[INFO] PostgreSQL connection closed')

    # ---Функция, позволяющая удалить существующего клиента
    def del_user(self, email):
        try:
            with self.db.cursor() as cur:
                cur.execute("""
                    SELECT * FROM users WHERE email=%s;
                """, (email,))
                requests = cur.fetchone()
                if requests:
                    cur.execute("""
                        DELETE FROM users_phone WHERE user_id=%s;
                    """, (requests[0],))
                    cur.execute("""
                        DELETE FROM users WHERE email=%s;
                    """, (email,))
                    print(f'[INFO] User {requests[1]} {requests[2]} removed')
                else:
                    print('[INFO] User does not exist')
        except Exception as _er:
            print('[INFO] Error while working with PostgreSQL', _er)
        finally:
            if self.db:
                self.db.commit()
                self.db.close()
                print('[INFO] PostgreSQL connection closed')

    # ---Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
    def search_user(self, item, value):
        try:
            with self.db.cursor() as cur:
                if item == 'name':
                    cur.execute("""
                        SELECT * FROM users WHERE name_user=%s;
                    """, (value,))
                    requests = cur.fetchall()
                elif item == 'lastname':
                    cur.execute("""
                        SELECT * FROM users WHERE lastname_user=%s;
                    """, (value,))
                    requests = cur.fetchall()
                elif item == 'email':
                    cur.execute("""
                        SELECT * FROM users WHERE email=%s;
                    """, (value,))
                    requests = cur.fetchall()
                elif item == 'phone':
                    cur.execute("""
                        SELECT user_id FROM users_phone WHERE phone_user=%s;
                    """, (value,))
                    request_id = cur.fetchone()
                    if request_id:
                        cur.execute("""
                            SELECT * FROM users WHERE id=%s;
                        """, (request_id,))
                        requests = cur.fetchall()
                    else:
                        requests = request_id
                if requests:
                    phone_book = []
                    for num, data in enumerate(requests):
                        cur.execute("""
                            SELECT phone_user FROM users_phone WHERE user_id=%s;
                        """, (data[0],))
                        request_phone = cur.fetchall()
                        if request_phone:
                            for phone in request_phone:
                                phone_book.append(phone[0])
                            print(f'User {num + 1}\nName: {data[1]}\n'
                                  f'Lastname: {data[2]}\nEmail: {data[3]}\nPhone: {phone_book}')
                        else:
                            print(f'User {num + 1}\nName: {data[1]}\n'
                                  f'Lastname: {data[2]}\nEmail: {data[3]}')
                else:
                    print('User not found!')
        except Exception as _er:
            print('[INFO] Error while working with PostgreSQL', _er)
        finally:
            if self.db:
                self.db.commit()
                self.db.close()
                print('[INFO] PostgreSQL connection closed')

    # ---Функция, позволяющая полностью удалить таблицу(ВНИМАНИЕ!!!ДАННЫЕ БУДУТ УТЕРЯНЫ!!!)
    def del_table(self):
        try:
            with self.db.cursor() as cur:
                cur.execute("""
                    DROP TABLE users_phone;
                """)
                cur.execute("""
                    DROP TABLE users;
                """)
                print('[INFO] Table deleted')
            self.db.commit()
        except Exception as error:
            print('[INFO] Error while working with PostgreSQL', error)
        finally:
            if self.db:
                self.db.close()
                print("[INFO] PostgresSQL connection closed")
