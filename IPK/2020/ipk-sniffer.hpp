/* Author: Daniel Stepanek
 * Email: xstepa61@stud.fit.vutbr.cz
 * Date: 3.5.2020
 */


#include<iostream>
#include<getopt.h>
#include<string.h>
#include<cstring>
#include<cstdio>
#include<pcap/pcap.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<netinet/ip.h>
#include<netinet/ip6.h>
#include<netinet/tcp.h>
#include<netinet/udp.h>
#include<arpa/inet.h>
#include<netdb.h>
#include<netinet/if_ether.h> /* includes net/ethernet.h */
#include<time.h>

/* ethernet headers are always exactly 14 bytes */
#define SIZE_ETHERNET 14
