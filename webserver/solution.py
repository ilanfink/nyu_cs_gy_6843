#ilan finkelstein
#cs gy 6843


from socket import *

import sys

def webServer(host="127.0.0.1", port=13331):
  
  # establish the server port
  serverSocket = socket(AF_INET, SOCK_STREAM)
  serverSocket.bind((host, port))
  serverSocket.listen()

  while True: # event loop

    # connect server port to client port
    print(f"Ready to serve on {port}...")
    connectionSocket, addr = serverSocket.accept()
    print(f"Connected on {addr}...")

    with connectionSocket:
      try:
        try:

          # parse client request
          message = connectionSocket.recv(1024)
          if not message:
            break

          # open requested file
          filename = message.split()[1]
          with open(filename[1:]) as file: # fails if file not found

            # send header & content-type
            connectionSocket.send('HTTP/1.0 200 OK\n'.encode())
            connectionSocket.send('Content-Type: text/html\n\n'.encode())
            
            # send HTML requested
            connectionSocket.sendall(file.read().encode())

        except IOError:
          connectionSocket.send('HTTP/1.0 404 Not Found\n'.encode())
          connectionSocket.send('Content-Type: text/html\n\n'.encode())

          # send HTML for 404
          connectionSocket.sendall("""<html>
                                        <head><title>FILE NOT FOUND</title></head>
                                        <body><h1>FILE NOT FOUND</h1></body>
                                      </html>""".encode())

      except (ConnectionResetError, BrokenPipeError):
        pass # forgives these errors silently

  serverSocket.close()
  sys.exit()

if __name__ == "__main__":
  webServer()
