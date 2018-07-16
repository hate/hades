___author___ = 'xyph'

import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import shutil
from colorama import init, Fore, Back, Style
init( autoreset = True, convert = True )


print( '\033[H\033[J' ) # clears the screen lmao
columns = shutil.get_terminal_size( ).columns
print( Fore.LIGHTWHITE_EX + Back.LIGHTRED_EX + "hades".center( columns ) 
                          + Back.RED + "https://github.com/hate".center( columns ) )

try:
    words = open( 'words.txt' )
    print( Fore.LIGHTCYAN_EX + "found words.txt!\n" )
except FileNotFoundError:
    print( Fore.LIGHTYELLOW_EX + "could not locate words.txt, make sure it exists!" )
    time.sleep( 5 )
    exit( )

session = requests.Session( )
retries = Retry( total = 10, backoff_factor = 0.5, status_forcelist = [ 500, 502, 503, 504 ], raise_on_status = False )
session.mount( 'https://', HTTPAdapter( max_retries = retries ) )

for username in words.read( ).split( ):
    try:
        client = session.get( 'https://www.instagram.com/accounts/web_create_ajax/attempt/' )

        header_data = {
                'x-csrftoken': client.cookies[ 'csrftoken' ], 
                'referer': 'https://www.instagram.com/'
        }

        post_data = {        
                'email': 'very_cool_email@gmail.com',
                'password': 'very_strong_password',
                'username': username,
                'first_name': 'very cool name'
        }

        response = session.post( 'https://www.instagram.com/accounts/web_create_ajax/attempt/', 
                                    data = post_data, 
                                    headers = header_data
        )
            
        if 'form_validation_error' not in response.text and 'account_created' in response.text:
            print( Fore.LIGHTWHITE_EX + "availability: " + Fore.LIGHTGREEN_EX + username )

            with open( 'output.txt', 'a' ) as output:
                output.write( username + '\n' )

        elif 'form_validation_error' in response.text and 'account_created' in response.text:
            print( Fore.LIGHTWHITE_EX + "availability: " + Fore.LIGHTRED_EX + username )
    except:
       print( Fore.LIGHTYELLOW_EX + "failed to connect" )

words.close( )

print( Fore.LIGHTCYAN_EX + "\nfinished checking! check output.txt" )
time.sleep( 3 )
exit( )
