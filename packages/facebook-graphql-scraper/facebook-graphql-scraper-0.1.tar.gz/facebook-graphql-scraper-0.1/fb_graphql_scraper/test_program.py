# -*- coding: utf-8 -*-
#%%
from fb_user_spider import *
from dotenv import load_dotenv
import os

## Log in account version
# load_dotenv()
# username_or_userid = os.getenv("FB_USERNAME_OR_USERID")
# pwd = os.getenv("FBPASSWORD")
# fb_user_id = "KaiCenatOfficial"
# res = get_user_posts(
#     fb_username_or_userid=fb_user_id, 
#     loop_times=50,
#     username_or_userid=username_or_userid, 
#     pwd=pwd
# )
# res


## Without logging in account version
fb_user_id = "KaiCenatOfficial"
res = get_user_posts(
    fb_username_or_userid=fb_user_id, 
    loop_times=50
)
print(res)