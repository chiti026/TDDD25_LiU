#!/usr/bin/env python3

# -----------------------------------------------------------------------------
# Distributed Systems (TDDD25)
# -----------------------------------------------------------------------------
# Author: Sergiu Rafiliu (sergiu.rafiliu@liu.se)
# Modified: 16 March 2017
#
# Copyright 2012-2017 Linkoping University
# -----------------------------------------------------------------------------

"""Client reader/writer for a fortune database."""

import sys
import socket
import json
import argparse

# -----------------------------------------------------------------------------
# Initialize and read the command line arguments
# -----------------------------------------------------------------------------


def address(path):
    addr = path.split(":")
    if len(addr) == 2 and addr[1].isdigit():
        return((addr[0], int(addr[1])))
    else:
        msg = "{} is not a correct server address.".format(path)
        raise argparse.ArgumentTypeError(msg)

description = """\
Client for a fortune database. It reads a random fortune from the database.\
"""
parser = argparse.ArgumentParser(description=description)
parser.add_argument(
    "-w", "--write", metavar="FORTUNE", dest="fortune",
    help="Write a new fortune to the database."
)
parser.add_argument(
    "-i", "--interactive", action="store_true", dest="interactive",
    default=False, help="Interactive session with the fortune database."
)
parser.add_argument(
    "address", type=address, nargs=1, metavar="addr:port",
    help="Server address."
)
opts = parser.parse_args()
server_address = opts.address[0]

# -----------------------------------------------------------------------------
# Auxiliary classes
# -----------------------------------------------------------------------------


class CommunicationError(Exception):
    pass


class DatabaseProxy(object):

    """Class that simulates the behavior of the database class."""

    def __init__(self, server_address):
        self.address = server_address

    # Public methods

    def read(self):
        #
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.address[0], self.address[1]))
                fp = s.makefile(mode='rw')
                fp.write(str(json.dumps({'method': 'read', 'args': ''}) + '\n'))
                # really important: it seems the cotent won't be written to the file until the fp is closed, 
                # and flush forces the change to take place in the file.
                fp.flush()
                #s.send(bytes(str(json.dumps({'method': 'read', 'args': ''}) + '\n'), 'utf-8'))
                #response = json.loads(s.recv(1024).decode('utf-8'))
                response = json.loads(fp.readline())
                if('result' in response):
                    return response['result']
                else:
                    error = response['error']
                    raise type(error['name'], (Exception, ), {error['args']})
        except:
            raise ConnectionError()
        #

    def write(self, fortune):
        #
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.address[0], self.address[1]))
                fp = s.makefile(mode='rw')
                fp.write(str(json.dumps({'method': 'write', 'args': [fortune]})) + '\n')
                fp.flush()
                response = json.loads(fp.readline())
                if('result' in response):
                    return
                else:
                    error = response['error']
                    raise type(error['name'], (Exception, ), {error['args']})
        except:
            raise ConnectionError()
        #

# -----------------------------------------------------------------------------
# The main program
# -----------------------------------------------------------------------------

# Create the database object.
db = DatabaseProxy(server_address)

if not opts.interactive:
    # Run in the normal mode.
    if opts.fortune is not None:
        db.write(opts.fortune)
    else:
        print(db.read())

else:
    # Run in the interactive mode.
    def menu():
        print("""\
Choose one of the following commands:
    r            ::  read a random fortune from the database,
    w <FORTUNE>  ::  write a new fortune into the database,
    h            ::  print this menu,
    q            ::  exit.\
""")

    command = ""
    menu()
    while command != "q":
        sys.stdout.write("Command> ")
        command = input()
        if command == "r":
            print(db.read())
        elif (len(command) > 1 and command[0] == "w" and
                command[1] in [" ", "\t"]):
            db.write(command[2:].strip())
        elif command == "h":
            menu()
