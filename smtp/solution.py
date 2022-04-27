from socket import *
import time


def send(msg, sock):
    sock.send(msg.encode())
    recv = sock.recv(2048).decode()
    #print("C:", msg)
    #print("S:", recv)
    #print("----------")


def smtp_client(port=1025, mailserver='127.0.0.1'):
    clientsock = socket(AF_INET, SOCK_STREAM)
    clientsock.connect((mailserver, port))
    #print("C: Connecting...")
    #print("S:", clientsock.recv(1024).decode())
    #print("----------")

    send('HELO Ilan\r\n', clientsock)
    send('MAIL FROM:<from@test.com>\r\n', clientsock)
    send('RCPT TO:<to@test.com>\r\n', clientsock)
    send('DATA\r\n.\r\n', clientsock)
         
    subj = 'Subject: Test'
    date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
    cont = 'Email content here!'

    send(subj + '\r\n\r\n' + date + '\r\n\r\n' + cont + '\r\n.\r\n', clientsock)
    send('QUIT\r\n\r\n', clientsock)
    clientsock.close()


if __name__ == '__main__':
    smtp_client(port=1025, mailserver='127.0.0.1')
