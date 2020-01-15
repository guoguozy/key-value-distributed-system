# -*- coding: utf-8 -*
import argparse
import rpyc


class Client(object):
    """
    commands:
    SET key value - set value to key
    GET key - get value from key
    GETALL - get all key-value
    DEL key - delete a key
    DELALL - delete all key-value
    GETlog - get the log
    """

    def try_to_connect(self):
        self.conn = rpyc.connect('localhost', 18861)
        self.id = self.conn.root.get_id()
        return self.id

    def run(self):
        try:
            while True:
                command = input('Client %d > ' % self.id)
                if command == 'help':
                    print(self.__doc__)
                else:
                    msg = self.conn.root.run_command(self.id, command)
                    if msg != None:
                        print(msg)
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    users = {}
    with open('user.txt') as f:
        for i in f.readlines():
            i = i.split()
            users[i[0]] = i[1]

    username = input('Please input your username:')
    usercode = input('Please input your code:')
    if username in users.keys() and users[username] == usercode:
        client = Client()
        client_id = client.try_to_connect()
        if client_id == None:
            print('Connection Failed.')
        else:
            print('Welcome to GZY simple distributed key-value database.')
            print('Your client ID is %d.' % client_id)
            print('Enter help for more info if necessary.')
            client.run()
    else:
        print('Your username or code has something wrong.please retry.')
