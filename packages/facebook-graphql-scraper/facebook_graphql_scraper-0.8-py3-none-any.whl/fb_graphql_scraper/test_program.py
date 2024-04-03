# -*- coding: utf-8 -*-
#%%
import os
print(os.getcwd())
from facebook_graphql_scraper import FacebookGraphqlScraper as fb_graphql_scraper
from dotenv import load_dotenv
import os


# ## Load account info
# load_dotenv()
# username_or_userid = os.getenv("FB_USERNAME_OR_USERID") # Facebook帳號密碼
# pwd = os.getenv("FBPASSWORD")
# driver_path = "/Users/renren/Desktop/FB_graphql_scraper/fb_graphql_scraper/resources/chromedriver-mac-arm64/chromedriver"

# #%%
# ## Log in account version
# fb_user_id = "KaiCenatOfficial"
# url = "https://www.facebook.com/"
# res = fb_graphql_scraper.get_user_posts(
#     fb_username_or_userid=fb_user_id, 
#     loop_times=50,
#     username_or_userid=username_or_userid,
#     pwd=pwd
# )
# res
#%%
## Without logging in account version
fb_user_id = "KaiCenatOfficial"
driver_path = "/Users/renren/Desktop/FB_graphql_scraper/fb_graphql_scraper/resources/chromedriver-mac-arm64/chromedriver"
url = "https://www.facebook.com/"
res = fb_graphql_scraper.get_user_posts(
    fb_username_or_userid=fb_user_id, 
    loop_times=50
)
res
# %%
