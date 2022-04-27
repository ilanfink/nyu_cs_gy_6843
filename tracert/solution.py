from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2


def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2

    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def build_packet():
    ID = os.getpid() & 0xffff
    myChecksum = 0
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    myChecksum = checksum(header + data)
    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data

    return packet


def get_route(hostname):
    tracelist1 = []  # This is your list to use when iterating through each trace
    tracelist2 = []  # This is your list to contain all traces
    print("Begin traceroute to " + hostname + "(" + gethostbyname(hostname) + ")......\n")

    destAddr = gethostbyname(hostname)
    for ttl in range(1, MAX_HOPS):
        for tries in range(TRIES):
            timeLeft = TIMEOUT

            # Fill in start
            # Make a raw socket named mySocket
            icmp = getprotobyname("icmp")
            try:
                mySocket = socket(AF_INET, SOCK_RAW, icmp)
            except error as msg:
                print("Error Creating Socket:", msg)
            # Fill in end
            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t = time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                if whatReady[0] == []:  # Timeout
                    tracelist2.append(["*","*","*","Request timed out"])
                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()

                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    tracelist2.append(["*","*","*","Request timed out"])
            except timeout:
                continue
            else:
                # Fill in start
                # Fetch the icmp type from the IP packet

                # get TTL
                ttl = recvPacket[8]
                # get ICMP info
                type, pongCode, pongChecksum, pongID, pongSequence = struct.unpack("bbHHh", recvPacket[20:28])
                # get RTT in ms
                RTT = (timeReceived - struct.unpack("d", recvPacket[28:36])[0]) * 1000

                # try to get hostname of each router in the path
                try:
                    routerHostname = gethostbyaddr(addr[0])[0]
                except herror as emsg:
                    routerHostname = "(Could not look up name:" + str(emsg) + ")"

                # Fill in end
                if type == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    x = [str(ttl), str((timeReceived - timeSent) * 1000), addr[0], routerHostname]
                    tracelist2.append(x)

                elif type == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    x = [str(ttl), str((timeReceived - timeSent) * 1000), addr[0], routerHostname]
                    tracelist2.append(x)

                elif type == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    x = [str(ttl), str((timeReceived - timeSent) * 1000), addr[0], routerHostname]
                    tracelist2.append(x)
                    #tracelist2.append(tracelist1)
                    tracelist1 = []

                    if destAddr == addr[0]:
                        return tracelist2

                else:
                    print("error")
                #print(tracelist2)
                break
            finally:
                mySocket.close()


if __name__ == '__main__':
    print(get_route("google.co.il"))
