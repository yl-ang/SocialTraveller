from tag import *
from individual_sqlite import *
from interest import *
from my_interest import *

"""
Command to add interest tag(s) to user database.
Adds at least one interest specified. 

Usage
-----
Add only one interest:
e.g. /add student

Add multiple interests:
e.g. /add gamer programmer ...

Parameters 
----------
update: JSON file which calls the telegram command containing information about the user 
context: An object that is mainly used for error handling (Read more here: https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.callbackcontext.html)

Returns
-------
None
"""

individualdb = IndividualSQite()

def checker(string, user_id):
    for valid in tags:
        # check for valid interest
        if string == valid:
            # check if interest exists in user database
            for usr_int in individualdb.get_tags(user_id):
                if string == usr_int:
                    return 0
            # interest does not exist in user database
            return 1
    # invalid interest
    return 2

def interest_list():
    resp = 'List of valid interest tags:\n\n'    
    for interest in tags:
        resp += interest + '\n'
    return resp

def my_interest(user_id):
    resp = "Your registered interests:\n\n"
    # retrieving user_interest
    for usr_int in individualdb.get_tags(user_id):
        resp += usr_int + '\n'
    return resp

def add_interest_command(update,context):
    # retrieve 'text' data
    usr_input = str(update.message.text).lower().split()[1:]
    user_char_id = update.effective_user.id

    # defining containers to store interests
    valid_int = []
    duplicates = []
    invalid_int = []

    # interating over each input given
    for interest in usr_input:
        outcome = checker(interest, user_char_id)
        if outcome == 1:
            valid_int.append(interest)
        elif outcome == 0:
            duplicates.append(interest)
        else:
            invalid_int.append(interest)
    
    # No inputs given
    if len(valid_int) == 0 and len(duplicates) == 0 and len(invalid_int) == 0:
        add_empty = "Please include at least one interest to add."
        update.message.reply_text(add_empty)
        return
    else:
        add_resp = ''
        if len(valid_int) != 0:
            individualdb.add_tags(user_char_id, ' '.join(valid_int))
            add_resp += "%s has been successfully added to your interest(s).\n" % ", ".join(valid_int)
        if len(duplicates) != 0:
            add_resp += "%s already exist(s).\n" % ", ".join(duplicates)
        if len(invalid_int) != 0:
            add_resp += "%s is/are not valid interest(s).\n" % ", ".join(invalid_int)

    # Return response from bot
    if len(duplicates) == 0 and len(invalid_int) == 0:
        update.message.reply_text(add_resp + '\n' + my_interest(user_char_id) +'\n')
    else:
        bot_resp = add_resp +'\n'
        if len(invalid_int) != 0:
            bot_resp += interest_list() +'\n'
        if len(duplicates) != 0:
            bot_resp += my_interest(user_char_id) 
        update.message.reply_text(bot_resp)
    return