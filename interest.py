from tag import *

"""
Command to print out list of valid interest on Telegram.

Usage
-----
/interest

Parameters 
----------
update: JSON file which calls the telegram command containing information about the user 
context: An object that is mainly used for error handling (Read more here: https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.callbackcontext.html)

Returns
-------
None
"""

def interest_command(update,context):
    # bot response
    resp = 'Interest tags:\n\n'    
    for interest in tags:
        resp += interest + '\n'
    update.message.reply_text(resp)
    return