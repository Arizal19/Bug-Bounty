import socket,threading
LISTEN=("127.0.0.1",8081)
def io(a,b):
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
        buf=b""
        while b"\r\n\r\n" not in buf:
            d=c.recv(4096)
            if not d: return
            buf+=d
        line=buf.split(b"\r\n")[0].decode()
        host,port=line.split()[1].rsplit(":",1)
        ip=socket.gethostbyname(host)   # force IPv4
        up=socket.create_connection((ip,int(port)),timeout=20)
        c.sendall(b"HTTP/1.1 200 Connection established\r\n\r\n")
        threading.Thread(target=io,args=(c,up),daemon=True).start()
        io(up,c)
    except Exception as e:
        try: c.sendall(b"HTTP/1.1 502 Bad\r\n\r\n")
        except: pass
    finally:
        try: c.close()
        except: pass
s=socket.socket(); s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(LISTEN); s.listen(50)
print("CONNECT proxy on 127.0.0.1:8081 (IPv4 forced)",flush=True)
while True:
    c,_=s.accept(); threading.Thread(target=handle,args=(c,),daemon=True).start()
