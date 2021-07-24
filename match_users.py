from individual_sqlite import *
from group_sqlite import *
from tag import *
import random

individual_DB = IndividualSQite()
group_DB = GroupSQlite()

def match_user():
    tags_to_draw = tags
    complete_individuals = []
    member_counter = individual_DB.count_users()
    while len(complete_individuals) != (member_counter - member_counter % 5):
        random_interest = random.choice(tags_to_draw)
        # random_interest = "sports"
        lst_users = individual_DB.match_users(random_interest)
        lst_users = [x[0] for x in lst_users]
        lst_users = [x for x in lst_users if x not in complete_individuals] 
        random.shuffle(lst_users)
        counter = int(len(lst_users) / 5)
        if counter != 0:
            for i in range(counter):
                # get the an empty chat id 
                if group_DB.check_available_group():
                    avail_group_id = group_DB.get_empty_group()
                    # then call the update_member_list
                    group_DB.update_member_list(avail_group_id, lst_users[:5])
                    group_DB.update_grp_interest(avail_group_id, random_interest)
                else:
                    return
                # update the tags_to_draw list and complete_individuals list
                complete_individuals = complete_individuals + lst_users[:5]
                lst_users = lst_users[5:]
        
        tags_to_draw.remove(random_interest)
                
        