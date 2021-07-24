from tag import *
from individual_sqlite import *
from interest import *
from my_interest import *

"""
Command to remove interest tag(s) from user database.
Removes at least one interest specified.

Usage
-----
Remove only one interest:
e.g. /remove student

Remove multiple interests:
e.g. /remove gamer programmer ...

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

def my_interest(user_id):
    resp = "Your registered interests:\n\n"
    # retrieving user_interest
    for usr_int in individualdb.get_tags(user_id):
        resp += usr_int + '\n'
    return resp

def remove_interest_command(update,context):

    # retrieve 'text' data
    usr_input = str(update.message.text).lower().split()[1:]
    user_char_id = update.effective_user.id

    # defining containers to store interests
    valid_int = []
    int_not_found = []

    # interating over each input given
    for interest in usr_input:
        outcome = checker(interest, user_char_id)
        if outcome == 0:
            valid_int.append(interest)
        else:
            int_not_found.append(interest)
    
    # No inputs given
    if len(valid_int) == 0 and len(int_not_found) == 0:
        remove_empty = "Please include at least one interest to remove."
        update.message.reply_text(remove_empty)
        return
    else:
        remove_resp = ''
        if len(valid_int) != 0:
            individualdb.remove_tags(user_char_id, " ".join(valid_int))
            remove_resp +=  "%s has been successfully removed from your interests.\n" % ", ".join(valid_int)
        if len(int_not_found) != 0:
            remove_resp += "%s is/are not found.\n" % ", ".join(int_not_found)

    # Return response from bot
    update.message.reply_text(remove_resp + '\n' + my_interest(user_char_id))
    return