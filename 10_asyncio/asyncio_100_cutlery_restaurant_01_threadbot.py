import sys, attr
import threading
from queue import Queue


# ----------------------------------------------------------------------------
# class ThreadBot
# ----------------------------------------------------------------------------

# A ThreadBot is a subclass of a thread.
class ThreadBot(threading.Thread):
    def __init__(self):
        # ----------
        # The target function of the thread is the manage_table()
        super().__init__(target=self.manage_table)
        # ----------
        # This bot is going to be waiting tables and will need to be responsible for some cutlery.
        # Each bot keeps track of the cutlery that it took from the kitchen here.
        self.cutlery = Cutlery(knives=0, forks=0)
        # ----------
        # The bot will also be assigned tasks.
        # They will be added to this task queue, and the bot will perform them during its main processing loop, next.
        self.tasks = Queue()

    def manage_table(self):
        while True:
            task = self.tasks.get()
            if task == 'prepare table':
                # prepare a "table for four", which means obtaining four sets of knives and forks from the kitchen
                kitchen.give(to=self.cutlery, knives=4, forks=4)
            elif task == 'clear table':
                # clear a table, which means returning the set of four knives and forks from a table back to the kitchen.
                self.cutlery.give(to=kitchen, knives=4, forks=4)
            elif task == 'shutdown':
                return

# ----------------------------------------------------------------------------
# Cutlery object
# ----------------------------------------------------------------------------

@attr.s
class Cutlery:
    # ----------
    # The attrib() function provides an easy way to create attributes
    knives = attr.ib(default=0)
    forks = attr.ib(default=0)
    # lock = attrib(threading.Lock())

    # ----------
    # Transfer knives and forks from one Cutlery object to another.
    # It will be used by bots to obtain cutlery from the kitchen for new tables,
    # and to return the cutlery back to the kitchen after a table is cleared.
    def give(self, to: 'Cutlery', knives=0, forks=0):
        self.change(-knives, -forks)
        to.change(knives, forks)

    # ----------
    # Altering inventory data in the object instance.
    def change(self, knives, forks):
        # ----------
        # NOTE: HERE TYPICAL SIGN OF A RACE CONDITION BUG !!!
        # The problem with preemptive multitasking is that any thread busy with these steps
        # can be interrupted at any time, and a different thread can be given the opportunity to
        # work through the same steps.
        # ----------
        self.knives += knives
        self.forks += forks

        # ----------
        # --> fixed by placing a lock, 
        # but this requires you to know all the places where state will be shared between multiple threads.
        # This approach is viable when you control all the source code.
        # ----------
        # with self.lock:
        #     self.knives += knives
        #     self.forks += forks
        # ----------


##############################################################################
# ----------------------------------------------------------------------------
# setting before service
# ----------------------------------------------------------------------------

# kitchen:  the identifier for the kitchen inventory of cutlery.
# Typically, each of the bots will obtain cutlery from this location.
# It is also required that they return cutlery to this store when a table is cleared.
kitchen = Cutlery(knives=100, forks=100)

print(f'kitchen knives : {kitchen.knives}  forks : {kitchen.forks}')


# This script is executed when testing.
# For our test, we'll be using 10 ThreadBots.
bots = [ThreadBot() for i in range(10)]

print(f'bots : {bots}')


# ----------------------------------------------------------------------------
# give each bot number of tasks (number of tables) for preparing and clearing tables in the restaurant.
# ----------------------------------------------------------------------------

# If num_tables is increased, unfortunately in practice
# you find that you do not end up with all cutlery accounted for when the restaurant closes !!!
# Different amounts compared to the previous run !!!
# The longer test fails in different, non-reproducible ways.

# num_tables = 100
# num_tables = 10000
num_tables = 100000


# BEFORE SERVICE
for bot in bots:
    print(f'==== bot : {bot}')
    # for i in range(int(sys.argv[1])):
    for i in range(int(num_tables)):
        bot.tasks.put('prepare table')
        # print(f'table : {i+1}  prepare table :  knives : {kitchen.knives}  forks : {kitchen.forks}')
        bot.tasks.put('clear table')
        # print(f'table : {i+1}  clear table   :  knives : {kitchen.knives}  forks : {kitchen.forks}')
    # ----------
    # The shutdown task will make the bots stop (so that bot.join() a bit further down will return).
    bot.tasks.put('shutdown')

print('Kitchen inventory before service:', kitchen)


# ----------
# Start service --> check knives and forks AFTER SERVICE 

for bot in bots:
    bot.start()

for bot in bots:
    bot.join()

print('Kitchen inventory after service:', kitchen)



