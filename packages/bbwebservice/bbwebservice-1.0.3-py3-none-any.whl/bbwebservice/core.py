import socket
from threading import Thread, Event, current_thread
import ssl
import os
from .config_loader import *
from .http_parser import HTTP_Message_Factory, LOGGING_OPTIONS, LOGGING_CALLBACK ,log

SESSIONS:dict = {}
PAGES:dict = {}
GET_TEMPLATES:list= []
POST_HANDLER:dict = {}
POST_TEMPLATES:list = []

ERROR_HANDLER:dict = {}

SERVER_THREADS:list = []
CONFIG = Config()




def servlet(conn, addr, worker_state) -> None:

    '''The servlet function is invoked on every new client accepted by the server
    each servlet runs in its own thread and represents a session.'''

    while worker_state.is_set():
        try:

            log(f'[THREADING] thread {current_thread().ident} listens now.', log_lvl='debug')

            message_factory = HTTP_Message_Factory(conn,addr,PAGES,GET_TEMPLATES,POST_HANDLER,POST_TEMPLATES,ERROR_HANDLER)
            resp = message_factory.get_message()
            conn.sendall(resp)
            
            header,_,content = resp.partition(b'\r\n\r\n')
            log('\n\nRESPONSE:',str(header,'utf-8'),content,'\n\n', log_lvl='response',sep='\n')
            
            if message_factory.stay_alive:
                continue
        except TimeoutError:
            log(f'[THREADING] thread {current_thread().ident} closes due to an error that occured "{err}"', log_lvl='debug')        
        except Exception as err:
            log(f'[THREADING] thread {current_thread().ident} closes due to an error that occured "{err}"', log_lvl='debug')
            conn.settimeout(1.0)
            conn.close()
            break
        
        log(f'[THREADING] thread {current_thread().ident} closes because stay_alive is set to False', log_lvl='debug')
        conn.settimeout(1.0)
        conn.close()
        break

def main(server:socket.socket,state:Event) ->None:

    '''The main function acts as a dispatcher on accepting new clients approaching the server.
       Each client is handet to the servlet function which is started in its own thread and appended
       to the SERVER_THRADS list'''
    
    print('[SERVER] '+ CONFIG.SERVER_IP + ' running on port '+str(CONFIG.SERVER_PORT)+'...')
    while state.is_set():
        global SERVER_THREADS
        SERVER_THREADS = [t for t in SERVER_THREADS if t[0].is_alive()]
        try:
            conn,addr = server.accept()
            worker_state = Event()
            worker_state.set()
            if conn:
                worker_thread = Thread(target=servlet , args = [conn, addr, worker_state])
                SERVER_THREADS.append([worker_thread,worker_state,conn])
                worker_thread.start()
                conn.settimeout(15)
        except TimeoutError:
            pass
        except Exception as e:
            if state.is_set():
                log(f'[CONNECTION_ERROR] a connection failed due to the following Error: {e}.\n', log_lvl='debug')

def start():

    '''The start function starts the server. First it tries to initiate a socket Object and 
       then proceeds to call the server main function.'''
       
    if CONFIG.SERVER_IP == 'default':
        CONFIG.SERVER_IP = socket.gethostbyname(socket.gethostname())
    try:
        socket.setdefaulttimeout(2)
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((CONFIG.SERVER_IP,CONFIG.SERVER_PORT))
        server.listen(CONFIG.QUE_SIZE)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if CONFIG.SSL:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(CONFIG.CERT_PATH,CONFIG.KEY_PATH)
            server = context.wrap_socket(server, server_side=True)

    except Exception as e:
        log(f'[SERVER] error while attempting to start the server {e}\n', log_lvl='debug')
        system.exit(0)
        
    server_state = Event()
    server_state.set()
    server_thread = Thread(target=main , args = [server,server_state])
    server_thread.start()
    
    while True:
       state = input()
       if state in ['quit', 'q', 'exit', 'e', 'stop']:
           try:
               server_state.clear()
               for obj in SERVER_THREADS:
                   obj[1].clear()
                   try:
                       obj[2].shutdown(socket.SHUT_RDWR)
                       obj[2].close()
                   except Exception as e:
                       print(f"[SERVER] Error while closing client connection: {e}")
                   obj[0].join(timeout=1)   
           finally:
               try:
                   server.shutdown(socket.SHUT_RDWR)
                   server.close()
               except Exception as e:
                   print(f"[SERVER] Error while closing server: {e}")   
               server_thread.join(timeout=1)    
               print('[SERVER] closed...')
               os._exit(0)  




