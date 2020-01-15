# -*- coding: utf-8 -*
import argparse
import rpyc
from rpyc.utils.server import ThreadedServer


class Master(rpyc.Service):
    """Master"""

    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        for c in clients:
            c.close()

    def exposed_get_id(self):
        for i in range(len(client_ids)):
            if not client_ids[i]:
                client_ids[i] = True
                # print(i)
                return i
        # print('what')
        return None

    @staticmethod
    def judge_command(cmd):
        if cmd == 'set':
            return 0
        if cmd == 'get' or cmd == 'del':
            return 1
        if cmd == 'getall' or cmd == 'delall':
            return 2
        if cmd == 'getlog':
            return 3
        return 4

    def exposed_run_command(self, client_id, clause):
        clause = clause.strip().split()
        lens = len(clause)
        WRONG_MSG = 'Wrong command. Enter help if necessary.'
        if lens < 1:
            return WRONG_MSG

        command = clause[0].lower()
        cmd_type = self.judge_command(command)
        if cmd_type == 4:
            return WRONG_MSG

        elif cmd_type == 0:  # set
            if lens != 3:
                return WRONG_MSG

            k, v = clause[1], clause[2]
            clients[client_id].root.set(k, v)
            clients[client_id].root.writelog('set '+str(k)+' - '+str(v))

        elif cmd_type == 3:
            if lens != 1:
                return WRONG_MSG
            return clients[client_id].root.getlog()

        elif cmd_type == 1:  # get or del
            if lens != 2:
                return WRONG_MSG
            k = clause[1]
            if command == 'get':
                msg = clients[client_id].root.get(k)
                clients[client_id].root.writelog('get '+str(k))
                if msg == None:
                    return 'Key %s not found.' % k
                else:
                    return msg
            else:
                clients[client_id].root.rem(k)
                clients[client_id].root.writelog('del '+str(k))


        else:  # getall or delall
            if lens != 1:
                return WRONG_MSG
            if command == 'getall':
                clients[client_id].root.writelog('getall')
                return clients[client_id].root.getall()
            else:
                clients[client_id].root.writelog('delall')
                return clients[client_id].root.delall()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--p', type=int, default=1)
    args = parser.parse_args()

    client_ids = [False] * args.p
    clients = [rpyc.connect('localhost', 18862+i) for i in range(args.p)]
    master = ThreadedServer(Master, port=18861)
    print('Master is running.')
    master.start()
