from tag import *
from individual_sqlite import *
from interest import *

"""
Command to print out list of user registered interest on Telegram.

Usage
-----
/myinterest

Parameters 
----------
update: JSON file which calls the telegram command containing information about the user 
context: An object that is mainly used for error handling (Read more here: https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.callbackcontext.html)

Returns
-------
None
"""

individualdb = IndividualSQite()

def my_interest_command(update, context):
    user_char_id = update.effective_user.id
    resp = "Your registered interests:\n\n"
    # retrieving user_interest
    for usr_int in individualdb.get_tags(user_char_id):
        resp += usr_int + '\n'
    update.message.reply_text(resp)
    return