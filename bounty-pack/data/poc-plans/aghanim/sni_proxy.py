import socket,ssl,threading,sys
LISTEN=("127.0.0.1",8443)
TARGET=("pay-api.aghanim.com",443)
ctx=ssl.create_default_context()
def pipe(a,b):
    try:
        while True:
            d=a.recv(65536)
            if not d: break
            b.sendall(d)
    except Exception: pass
    finally:
        try: b.shutdown(socket.SHUT_WR)
        except Exception: pass
def handle(c):
    try:
        up=ctx.wrap_socket(socket.create_connection((socket.gethostbyname(TARGET[0]),TARGET[1]),timeout=20),server_hostname=TARGET[0])
    except Exception as e:
        c.close(); return
    threading.Thread(target=pipe,args=(c,up),daemon=True).start()
    pipe(up,c)
    try: c.close(); up.close()
    except: pass
s=socket.socket(); s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(LISTEN); s.listen(50)
print("SNI proxy 127.0.0.1:8443 -> %s" % (TARGET,), flush=True)
while True:
    c,_=s.accept()
    threading.Thread(target=handle,args=(c,),daemon=True).start()
