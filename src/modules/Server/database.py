# -----------------------------------------------------------------------------
# Distributed Systems (TDDD25)
# -----------------------------------------------------------------------------
# Author: Sergiu Rafiliu (sergiu.rafiliu@liu.se)
# Modified: 24 July 2013
#
# Copyright 2012 Linkoping University
# -----------------------------------------------------------------------------

"""Implementation of a simple database class."""

import random


class Database(object):

    """Class containing a database implementation."""

    def __init__(self, db_file):
        self.db_file = db_file
        self.rand = random.Random()
        self.rand.seed()
        #
        # Your code here.
        #
        with open(self.db_file, 'r') as f:
            contents = f.read()

        f.close()

        self.lines = contents.strip().split('\n%\n')
        self.lines = self.lines[:-1]
        pass

    def read(self):
        """Read a random location in the database."""
        #
        # Your code here.
        #
        if (len(self.lines) == 0):
            return ""
        else:
            return self.rand.choice(self.lines)

    def write(self, fortune):
        """Write a new fortune to the database."""
        #
        # Your code here.
        #
        with open(self.db_file, 'a') as f:
            f.write(fortune + '\n%')
        f.close()
        self.lines.append(fortune)
        pass
