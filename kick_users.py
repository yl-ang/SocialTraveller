import Constants as keys
from telegram.ext import *
from telegram import Bot
from group_sqlite import GroupSQlite

group_db = GroupSQlite()
bot = Bot(keys.API_KEY)

def kick_users(context: CallbackContext):
    grp_lst = group_db.get_all_grp()
    for grp_chat_id in grp_lst:
        user_id_lst = group_db.get_all_members(grp_chat_id)
        for userID in user_id_lst:
            bot.kick_chat_member(grp_chat_id, int(userID))
        group_db.update_member_list(grp_chat_id, [])
