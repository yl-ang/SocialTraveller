# Put your code here
from tag import tags
from group_sqlite import GroupSQlite

def guess_command(update, context):

    '''
    Informs the user whether they guessed correctly and interacts with the database 
    to tell whether someone has already guessed correctly or to update the database
    when someone has guessed correctly.

    Parameters 
    ----------
    update: JSON file which calls the telegram command containing information about the user 
    context: An object that is mainly used for error handling (Read more here: https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.callbackcontext.html)

    Returns
    -------
    None

    '''


    resp = str(update.message.text).lower().split()
    group = GroupSQlite()
    grp_chat_id = update.message.chat_id

    if group.check_answered(grp_chat_id) :
        update.message.reply_text('Someone has already guessed the answer.')
    elif len(resp) == 1 or len(resp) >= 3 :
        update.message.reply_text('/guess <interest>\nList of interests can be viewed via the /interest command.')
    elif resp[1] not in tags :
        update.message.reply_text('Please guess a valid interest.\nList of interests can be viewed via the /interest command.')
    else :
        interest = resp[1]

        if interest == group.check_grp_interest(grp_chat_id) :
            group.update_answered(grp_chat_id, 'TRUE')
            update.message.reply_text('You guessed correctly. Well Done!')
        else :
            update.message.reply_text('You guessed incorrectly.')