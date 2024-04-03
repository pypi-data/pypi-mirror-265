# -*- coding: utf-8 -*-
#%%
from facebook_graphql_scraper import FacebookGraphqlScraper as fb_graphql_scraper
from dotenv import load_dotenv
import os


## Load account info
load_dotenv()
username_or_userid = os.getenv("FB_USERNAME_OR_USERID")
pwd = os.getenv("FBPASSWORD")

#%%
## Log in account version
fb_user_id = "KaiCenatOfficial"
url = "https://www.facebook.com/"
res = fb_graphql_scraper.get_user_posts(
    fb_username_or_userid=fb_user_id, 
    loop_times=50,
    username_or_userid=username_or_userid,
    pwd=pwd
)
res
#%%
## Without logging in account version
fb_user_id = "KaiCenatOfficial"
url = "https://www.facebook.com/"
res = fb_graphql_scraper.get_user_posts(
    fb_username_or_userid=fb_user_id, 
    loop_times=50
)
res
# %%
