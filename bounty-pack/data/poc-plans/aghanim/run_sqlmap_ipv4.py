import socket,sys,os
_orig=socket.getaddrinfo
def gai(host,port,family=0,type=0,proto=0,flags=0):
    try: return _orig(host,port,socket.AF_INET,type,proto,flags)
    except Exception: return _orig(host,port,family,type,proto,flags)
socket.getaddrinfo=gai
SP=r"C:\Users\WINDOWS10\AppData\Local\Programs\Python\Python314\Lib\site-packages\sqlmap"
sys.path.insert(0,SP)
os.chdir(SP)
sys.argv=["sqlmap.py"]+sys.argv[1:]
import sqlmap
sqlmap.main()
