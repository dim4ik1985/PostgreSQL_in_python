from client_management import DbCreate


if __name__ == '__main__':

    # ---Подключение к базе данных
    database = input('Database name: ').lower()
    name = input('Username: ').lower()
    password = input('Enter password: ')
    user_db = DbCreate(database, name, password)
    # user_db.create_table()
    # user_db.insert_user('Karl', 'Gray', 'freibre-5992@yopmail.com', '1(3810)432-75-9773')
    # user_db.insert_user('Henry', 'Anderson', 'jasilannugreu-1024@yopmail.com')
    # user_db.insert_user('Irma', 'Williams', 'bragr-5604@yopmail.com')
    # user_db.insert_user('Matthew', 'Brady', 'crehopritrota-9428@yopmail.com', '3(326)515-87-6015')
    # user_db.add_phone('freibre-5992@yopmail.com', '337(280)729-74-5062')
    # user_db.del_phone('freibre-5992@yopmail.com', '1(3810)432-75-9773')
    # user_db.del_user('freibre-5992@yopmail.com')
    # user_db.search_user('email', 'freibre-5992@yopmail.com')
    # user_db.search_user('phone', '3(326)515-87-6015')
    # user_db.search_user('phone', '337(280)729-74-506')
    # user_db.search_user('name', 'Irma')
    # user_db.to_change_data('phone', '3(326)515-87-6015', '337(280)729-74-506')
    # user_db.del_table()
