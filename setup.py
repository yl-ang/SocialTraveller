from group_sqlite import *

group_DB = GroupSQlite()

def setup_command(update, context):
    grp_chat_id = update.message.chat_id 
    msg_chat_id = update.message.message_id
    chat_type = update.message.chat.type
    user_char_id = update.effective_user.id
    group_DB.add_group(grp_chat_id, "", "","FALSE")
    print("Group has been added into DB!")

