from telegram.ext import *
from telegram import Bot

def help_command(update, context):
    """
    Command to get list of available commands to use

    Parameters 
    ----------
    update: JSON file which calls the telegram command containing information about the user 
    context: An object that is mainly used for error handling (Read more here: https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.callbackcontext.html)

    Returns
    -------
    None
    """

    help_text= '''/start <list of interests tags>: Setup an account and register with valid interest tags
/interest: View list of interest tags you can add
/add <interest tag>: Add interest tag
/remove <interest tag>: Add interest tag
/myinterest: View list of interest tags that you have added.
/guess <interest tag>: Guess what is the common interest that the group has'''
    update.message.reply_text(help_text)