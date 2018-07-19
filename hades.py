___author___ = 'xyph'

from time import sleep
from datetime import datetime

import requests
from urllib3.util.retry import Retry

from os import system
import shutil
from colorama import init, Fore, Back
init( autoreset = True, convert = True )


system( 'cls' ) # cls for windows, clear for linux
columns = shutil.get_terminal_size( ).columns
print( Fore.LIGHTWHITE_EX + Back.LIGHTRED_EX + 'hades'.center( columns )
                          + Back.RED + 'https://github.com/hate'.center( columns ) )

try:
    words = open( 'words.txt' )
    print( Fore.LIGHTRED_EX + '\n[' + datetime.now( ).strftime( '%I:%M:%S' ) + '] ' + Fore.LIGHTCYAN_EX + 'found words.txt!\n' )
except FileNotFoundError:
    print( Fore.LIGHTRED_EX + '[' + datetime.now( ).strftime( '%I:%M:%S' ) + '] ' + Fore.LIGHTYELLOW_EX + 'could not locate words.txt, make sure it exists!' )
    sleep( 5 )
    exit( )

session = requests.Session( )
retries = Retry( total = 10,
                 backoff_factor = 1,
                 status_forcelist = [ 500, 502, 503, 504 ],
                 raise_on_status = False
)
session.mount( 'https://', requests.adapters.HTTPAdapter( max_retries = retries ) )

for username in words.read( ).split( ):
    try:
        client = session.get( 'https://www.instagram.com/accounts/web_create_ajax/attempt/' )

        if client.status_code == 429: # too many requests
            print( Fore.LIGHTRED_EX + '[' + datetime.now( ).strftime( '%I:%M:%S' ) + '] ' + Fore.RED + 'limit reached, waiting 3 minutes...' )
            sleep( 180 ) # blah blah bootleg fix blah

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
            print( Fore.LIGHTRED_EX + '[' + datetime.now( ).strftime( '%I:%M:%S' ) + '] ' + Fore.LIGHTWHITE_EX + 'availability: ' + Fore.LIGHTGREEN_EX + username )

            with open( 'output.txt', 'a' ) as output:
                output.write( username + '\n' )

        elif 'form_validation_error' in response.text and 'account_created' in response.text:
            print( Fore.LIGHTRED_EX + '[' + datetime.now( ).strftime( '%I:%M:%S' ) + '] ' + Fore.LIGHTWHITE_EX + 'availability: ' + Fore.LIGHTRED_EX + username )

    except Exception as error:
        print( Fore.LIGHTRED_EX + '[' + datetime.now( ).strftime( '%I:%M:%S' ) + '] ' + Fore.GREEN + str( error ) )

words.close( )

print( Fore.LIGHTRED_EX + '\n[' + datetime.now( ).strftime( '%I:%M:%S' ) + '] ' + Fore.LIGHTCYAN_EX + 'finished checking! check output.txt' )
sleep( 3 )
exit( )
