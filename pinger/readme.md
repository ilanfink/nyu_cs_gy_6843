Lab 4: ICMP Pinger Lab
In this lab, you will gain a better understanding of Internet Control Message Protocol (ICMP). You will learn to implement a Ping application using ICMP request and reply messages. 

Ping is a computer network application used to test whether a particular host is reachable across an IP network. It is also used to self-test the network interface card of the computer or as a latency test. It works by sending ICMP “echo reply” packets to the target host and listening for ICMP “echo reply” replies. The "echo reply" is sometimes called a pong. Ping measures the round-trip time, records packet loss, and prints a statistical summary of the echo reply packets received (the minimum, maximum, and the mean of the round-trip times and in some versions the standard deviation of the mean).

Your task is to develop your own Ping application in Python. Your application will use ICMP but, in order to keep it simple, will not exactly follow the official specification in RFC 1739. Note that you will only need to write the client side of the program, as the functionality needed on the server side is built into almost all operating systems.

You should complete the Ping application so that it sends ping requests to a specified host separated by approximately one second. Each message contains a payload of data that includes a timestamp. After sending each packet, the application waits up to one second to receive a reply. If one second goes by without a reply from the server, then the client assumes that either the ping packet or the pong packet was lost in the network (or that the server is down).

Code
Below you will find the skeleton code for the client. You are to complete the skeleton code. The place where you need to fill in code is marked with #Fill in start and #Fill in end. In addition, you will need to add a few lines of code in order to calculate minimum time, average time, maximum time, and stdev time and print the results like in the operating system.




Additional Notes
1. In the “receiveOnePing” method, you need to receive the structure ICMP_ECHO_REPLY and fetch the information you need, such as checksum, sequence number, time to live (TTL), etc. Study the “sendOnePing” method before trying to complete the “receiveOnePing” method.
2. You do not need to be concerned about the checksum, as it is already given in the code.
3. This lab requires the use of raw sockets. In some operating systems, you may need administrator/root privileges to be able to run your Pinger program.
4. See the end of this programming exercise for more information on ICMP.

Testing the Pinger
First, test your client by sending packets to localhost, that is, 127.0.0.1.
Then, you should see how your Pinger application communicates across the network by pinging servers in different continents.

What to Hand in
Use your GitHub repository to upload the complete code for the assignment.


Example of a correct output:
“No.no.e” is a non-valid domain, therefore, the return value (vars) of ping is ['0', '0.0', '0', '0.0']. Please make sure you use this exact value.
“Google.co.il” is a valid domain, therefore, the return value is a list that can be created in the following way:
vars = [str(round(packet_min, 2)), str(round(packet_avg, 2)),str(round(packet_max, 2)), str(round(stdev(stdev_var),2))]
The method “ping” must return a Python list with the above values for a valid and a non-valid domain. [min,avg,max,stdev]. Return values must be in milliseconds. 



