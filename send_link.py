# Put your code here
import Constants as keys
from telegram.ext import *
from telegram import Bot
from group_sqlite import GroupSQlite
import requests
from match_users import *
group_db = GroupSQlite()
bot = Bot(keys.API_KEY)

def send_message(chat_id, message):
        endpoint = f"https://api.telegram.org/bot{keys.API_KEY}/sendMessage"
        data = { "chat_id" : chat_id,
                    "text" : message}
        response = requests.post(endpoint, data=data)

def send_link(context: CallbackContext):
    match_user()
    grp_lst = group_db.get_all_grp()
    for grp_chat_id in grp_lst:
        user_id_lst = group_db.get_all_members(grp_chat_id[0])
        for userID in user_id_lst:
            invite_link = bot.getChat(grp_chat_id[0]).invite_link
            link_message = "Hi, this is today group link %s. Have fun!" % invite_link
            send_message(int(userID), link_message)