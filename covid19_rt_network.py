import tweepy
import networkx as nx
import matplotlib as mpl
import selenium.webdriver as driver
import os


#NICK PERRA GOOD !!!! !!! !!! !!!! !!! !!! !!!! !!! !!! !!!!

def api_connection():

    api_key = os.getenv('TW_API_KEY')
    api_secret_key = os.getenv('TW_API_SECRET_KEY')

    user = os.getenv('TW_USER')
    pwd = os.getenv('TW_PWD')

    #defining the functions that will set up the authenticator, navigating to twitter, getting the verifier, verifying the authenicator, and getting some tweets. 
    def auth():
        global auth_obj
        auth_obj = tweepy.OAuthHandler(api_key, api_secret_key)

        
    def get_auth_url(auth):
        global redirect_url
        redirect_url = auth.get_authorization_url()


    def get_verified_api(url):   
        options = driver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--headless')

        #user the chrome browser to retrieve our verifier
        global chrome
        chrome_exe = os.path.join(os.getcwd(), 'chromedriver.exe')
        chrome = driver.Chrome(chrome_options = options, executable_path = chrome_exe)
        chrome.get(url)
        chrome.find_element_by_id('username_or_email').send_keys(user)
        chrome.find_element_by_id('password').send_keys(pwd)
        chrome.find_element_by_id('allow').click()
        verifier = chrome.find_element_by_tag_name('code').text
        
        #passing the verifier to our authentication object
        auth_obj.get_access_token(verifier)

        #establish our authorized api connection
        global tw_api
        tw_api = tweepy.API(auth_handler=auth_obj)
        tw_api.verify_credentials()

    def get_tweets(api):
        
        #arbitrarily lorge number
        max_tweets = 3200
        
        global collection
        collection = tweepy.Cursor(api.search, q='COVID-19', rpp=100, count=1000)
        print(len(list(collection.items(max_tweets))))
            

    
    #calling the functions above
    auth()
    get_auth_url(auth_obj)
    get_verified_api(redirect_url)
    get_tweets(tw_api)
    

api_connection()
