
/*  IPK-OMEGA: Scanner sitovych sluzeb
 *  @author: Daniel Stepanek xstepa61@stud.fit.vutbr.cz
 *
 */


#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <list>
#include <ctime>
#include <getopt.h>
#include <pcap.h>
#include <netdb.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <unistd.h>
#include <signal.h>
#include <sys/socket.h>
#include "scan_headers.h"

using namespace std;

//global handler
pcap_t *handle;

//Checksum funkce ze zdroje:
//https://tools.ietf.org/html/rfc1071
unsigned short check_sum(unsigned short *addr, int count){

  /* Compute Internet Checksum for "count" bytes
       *         beginning at location "addr".
       */
  register long sum = 0;

   while(count > 1)  {
      /*  This is the inner loop */
          sum += *(unsigned short *) addr++;
          count -= 2;
  }

      /*  Add left-over byte, if any */
  if(count > 0){
          sum += *(unsigned char *) addr;
  }
      /*  Fold 32-bit sum to 16 bits */
  while (sum >> 16){
      sum = (sum & 0xffff) + (sum >> 16);
  }

  u_int16_t checksum = ~sum;

  return checksum;
}


list<int> get_ports(string ports){
  list<int> portsList;
  size_t found;

//  http://www.cplusplus.com/reference/string/string/find/
  found = ports.find(',');
  if(found != string::npos){
    string num;
    size_t pos = 0;

    while(found != string::npos){
      num = ports.substr(pos, found);
      portsList.push_back(atoi(ports.c_str()));
      pos = found + 1;
      found = ports.find(',', pos);
    }

    num = ports.substr(pos, ports.length());
    portsList.push_back(atoi(ports.c_str()));

  }

  found = ports.find('-');
  if(found != string::npos){
    string num;

    num = ports.substr(0, found);
    int first = atoi(num.c_str());

    num = ports.substr(found + 1, ports.length());
    int last = atoi(num.c_str());

    for(int i = first; i <= last; i++){
      portsList.push_back(i);
    }

  }

  if((ports.find(',') == string::npos) && (ports.find('-') == string::npos)){
    portsList.push_back(atoi(ports.c_str()));

  }

  return portsList;

}

int get_source_ip(pcap_if_t *device){

  pcap_addr_t *IP = device->addresses;
  while(IP){
    if(IP->addr->sa_family == AF_INET){
      break;
    }
    else{
      IP = IP->next;
    }

  }

  return ((struct sockaddr_in *)IP->addr)->sin_addr.s_addr;
}

void callback_function(u_char *param, const struct pcap_pkthdr *header, const u_char *user){

  pcap_breakloop(handle);

  return;
}

void tcp_send_packet(char *packet, int tcpSocket, int port, tcpHead *tcpHeader, ipHead *ipHeader, sockaddr_in local_sin, pcap_if_t *device){

  // Set TCP packet attributes
  tcpHeader->source_port = 0;

  int min_port = 32768;
  int max_port = 61000;
  while(tcpHeader->source_port < min_port)
  {
    tcpHeader->source_port = rand() % max_port;
  }

  tcpHeader->dest_port = htons(port) ;
	tcpHeader->seq = htonl(rand()) ;

	// Fill pseudo header for checksum
	pseudoHead *ps = (pseudoHead*) (packet + sizeof(ipHead) + sizeof(tcpHead));
	ps->source_address = ipHeader->source_ip.s_addr;
	ps->dest_address = ipHeader->dest_ip.s_addr;
	ps->placeholder = 0;
	ps->protocol = IPPROTO_TCP;
	ps->length = ntohs(sizeof(tcpHead));

	// Count TCP checksum
  int size = sizeof(pseudoHead) + sizeof(tcpHead);
	tcpHeader->sum = htons(check_sum((unsigned short *)tcpHeader, size));


	// Set pcap filter
  char *errbuf[PCAP_ERRBUF_SIZE];
  struct bpf_program filter;
  char filter_app[100];
  bpf_u_int32 mask;
  bpf_u_int32 net;
  pcap_lookupnet(device->name, &net, &mask, *errbuf);
  handle = pcap_open_live(device->name, 65536, false, 1000, *errbuf);
  if(handle == NULL){
    cout << errbuf;
    exit(3);
  }

  pcap_compile(handle, &filter, filter_app, 0, net);
  pcap_setfilter(handle, &filter);

  if(sendto(tcpSocket, packet, ipHeader->ip_len , 0, (struct sockaddr *) &local_sin, sizeof (local_sin)) < 0){
    cerr << "Packet sending failed." << endl ;
  }

  //Start capturing
  if(pcap_loop(handle, 0, callback_function, NULL) == 0){
    cout << port << "/tcp" << "    " << "open" << endl;
  }
  else{
    cout << port << "/tcp" << "    " << "close" << endl;
  }

  return;
}

void tcp_scan(list<int> ports, char* packet, sockaddr_in local_sin, pcap_if_t *device){

  ipHead* ipHeader = (ipHead*) packet;
  tcpHead* tcpHeader = (tcpHead*) packet + sizeof(ipHead);

  ipHeader->ip_hl = 5;
  ipHeader->ip_v = 4;
  ipHeader->ip_tos = 0;
  ipHeader->ip_id = rand();
  ipHeader->ip_off = 0;
  ipHeader->ip_ttl = 255;
  ipHeader->ip_proto = IPPROTO_TCP;
  ipHeader->ip_sum = 0;
  ipHeader->ip_len = sizeof(ipHead) + sizeof(tcpHead);
  ipHeader->dest_ip.s_addr =   local_sin.sin_addr.s_addr;
  ipHeader->source_ip.s_addr = get_source_ip(device);

  int tcpSocket = socket(PF_INET, SOCK_RAW, IPPROTO_TCP);
  if(tcpSocket == -1){
    cerr << "Socket creating failed." << endl;
    exit(2);
  }


	// Fill TCP header

	// Offset after IP header
	tcpHeader->offx2 = 0x50;
	tcpHeader->ack = 0;
	tcpHeader->flags = 0x02;
	tcpHeader->sum = 0;
	tcpHeader->urp = 0;
	// Maximal window size
	tcpHeader->window = (65535);

	// Scan all specified ports
	for (auto port : ports){
    tcp_send_packet(packet, tcpSocket, port, tcpHeader, ipHeader, local_sin, device);
	}

  return;
}


int main(int argc,char **argv){

  string tcpPorts = "";
  string udpPorts = "";
  string domain = "";
  int isTCP = 0;
  int isUDP = 0;
  int isDomain = 0;

  char *interface, errbuf[PCAP_ERRBUF_SIZE];

  interface = pcap_lookupdev(errbuf);

//Parse arguments
  static struct option Options[] =
  {
    {"pt", 1, 0, 0},
    {"pu", 1, 0, 0},
    {"i", 1, 0, 0}
  };

  int c = 0;
  int opt = 0;
  while((c = getopt_long_only(argc, argv, "0", Options, &opt)) != -1){
    switch (c){
      // Parameters
      case 0:
        if(Options[opt].name == "i"){
          if(optarg){
            interface = optarg;
          }
        }
        else if(Options[opt].name == "pt"){
          if(optarg){
            isTCP = 1;
            tcpPorts = optarg;
          }
        }
        else if(Options[opt].name == "pu"){
          if(optarg){
            isUDP = 1;
            udpPorts = optarg;
          }
        }
        break;

      // Missing arguments
      case ':':
      case '?':
        cerr << "Missing Parameters" << endl;
        exit(1);

      // Error
      default:
        cerr << "Bad Parameters" << endl;
        exit(1);
    }
  }

  if(optind < argc){
    if ((optind+1) == argc){
      isDomain = 1;
  		domain = argv[optind];
  	}
    else{
  		cerr << "Bad Parameters" << endl ;
  		exit(1);
  	}
  }
  else{
    cerr << "Missing Parameters" << endl ;
  	exit(1);
  }

  if((isTCP == 0 && isUDP == 0) || isDomain == 0){
    cerr << "Bad Parameters" << endl;
    exit(1);
  }

  hostent* host = gethostbyname(domain.c_str());
  if(host == NULL){
    cerr << domain << ": is Unknown host" << endl;
    exit(2);
  }

  in_addr *host_addr = (struct in_addr*) *host->h_addr_list;
  string IP_addr = inet_ntoa(*host_addr);

  pcap_if_t *devices;
  pcap_if_t *dev;

  if(pcap_findalldevs(&devices, errbuf) == -1){
    cerr << "Device error: " << errbuf << endl;
    exit(2);
  }

  bool found = false;

  dev = devices;
  while(dev != NULL){
    if(strcmp(dev->name, interface) == 0){
      found = true;
      break;
    }
    dev = dev->next;

  }

  if(!found){
    cerr << "Invalid interface " << interface << "." << endl;
    pcap_freealldevs(devices);
    exit(2);
  }

// https://stackoverflow.com/questions/10918008/c-initializing-sockaddr-in
  sockaddr_in local_sin;

  local_sin.sin_family = AF_INET;
  local_sin.sin_port = 20;
  local_sin.sin_addr.s_addr = host_addr->s_addr;

  cout << "Interesting ports on " << domain << " " << IP_addr << endl;

  cout << "  PORT      STATE" << endl;

  //Ports Parsing
  list<int> tcpPortsList;
  if(tcpPorts != ""){
    tcpPortsList = get_ports(tcpPorts);
  }

  list<int> udpPortsList;
  if(udpPorts != ""){
    udpPortsList = get_ports(udpPorts);
  }

  if(tcpPortsList.size() != 0){
    char *packet = (char *) malloc(sizeof(ipHead) + sizeof(tcpHead) + sizeof(pseudoHead));
    memset(packet, 0,sizeof(ipHead)+sizeof(tcpHead)+sizeof(pseudoHead));


    tcp_scan(tcpPortsList, packet, local_sin, dev);


    free(packet);

  }



  if(udpPortsList.size() != 0){

  //  udp_scan();
  }

  // Free devs
  pcap_freealldevs(devices);

  return 0;
}
