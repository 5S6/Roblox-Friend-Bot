import time, ctypes, threading, random, traceback, sys, datetime, json, os, subprocess
from threading import Thread
try:
    import requests
except:
    print("Please run run_first.py before using this")
    time.sleep(20)
    sys.exit()


try:
    from colorama import Fore, init, Back, Style
    
except:
    print("Please run run_first.py before using this") #do this lmfao
    time.sleep(20)
    sys.exit()

lock = threading.Lock()
print(f"Basic Friend Request|Developed BY Alek#2022")



print("Make sure you have proxies placed in proxies.txt and cookies in cookies.txt. ")

proxies = open('proxies.txt','r').read().splitlines()
proxies = [{'https':'http://'+proxy} for proxy in proxies]


time.sleep(1)
req = requests.Session()


try:
    format = int(input("\nCookie format:\n\n[1] user:pass:cookie\n[2] cookie\n"))
except:
    print(Fore.RED + "You did not enter a valid option -- closing")
cookies = open('cookies.txt','r').read().splitlines()
if format == 1:
    try:
        cookies = [cookie.split(':',2)[2] for cookie in cookies]
    except:
        print("\n Your cookies are not formatted like this or there were no cookies found in cookies.txt.") #sad
        time.sleep(20)
        sys.exit()
elif format == 2:
    cookies = ['_|'+line.split('_|')[-1] for line in cookies]
else:
    print("Not a valid option, exiting")
    time.sleep(20)
    sys.exit()

if len(cookies) == 0:
    print(Fore.RED + "\nWARNING - You have no cookies loaded - bit will not work\n") #Get Cookies SMH


def friend_request(i):
    global lock, checked, sent, id, proxies
    checked += 1
    print(f'Sent requests: {sent} | Progress: {checked}/{len(cookies)}')
    req = requests.Session()
    req.cookies['.ROBLOSECURITY'] = i
    try:
        r = req.get('http://www.roblox.com/mobileapi/userinfo').json() 
        r = req.post('https://auth.roblox.com/v2/login',proxies=random.choice(proxies))
        req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
    except:
        with lock:
            print(Fore.RED + "Invalid cookie or a proxy error occurred") #Sad
        return True
    while True:
        try:
            r = req.post(f"https://friends.roblox.com/v1/users/{id}/request-friendship",proxies=random.choice(proxies))
        except:
            with lock:
                print(Fore.RED + "Proxy Error - Retrying - You may potentially be using bad proxies")
            continue
        if 'success' in r.json():
            if r.json()['success'] == True:
                with lock:
                    print(Fore.GREEN + f"Successfully sent friend request to {id}") #YAY
                sent += 1
                print(f'Sent requests: {sent} | Progress: {checked}/{len(cookies)}')
                break
        elif 'errors' in r.json():
            if r.json()['errors'][0]['message'] == "The target user is already a friend.": #Lovely
                with lock:
                    print(Fore.RED + "[Failed to send friend request -- friend request is already pending") #LMFAO
                break
    print(f'Sent requests: {sent} | Progress: {checked}/{len(cookies)}')
    return True


print(Fore.CYAN + "[1] -> Mass Friend Request Bot") #The Only Option LMFAO


try:
    option = int(input("\n Enter number of tool that you'd like to use: "))
except:
    print(Fore.RED + "You did not enter a valid option -- closing")
    time.sleep(30)
    sys.exit()



open('output.txt', 'w+').close()
if option == 1:
    print("Note that this option requires proxies")
    id = int(input("Enter the ID of the person you would like to bot friend requests to: ")) 
    sent = 0
    checked = 0
    ts = []
    for i in cookies:
        t = threading.Thread(target=friend_request,args=(i,))
        t.start()
        ts.append(t)
        time.sleep(0.01)
    for i in ts:
        i.join()
    if sent == 0:
        print(Fore.RED + "No friend requests were sent")
    elif sent > 0:
        print(Fore.GREEN + f"Successfully sent {sent} friend requests to {id}")
      
