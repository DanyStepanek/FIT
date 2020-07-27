#include "ipk-sniffer.hpp"

using namespace std;

pcap_if_t* get_active_interfaces(){
  pcap_if_t* interfaces;
  char error[PCAP_ERRBUF_SIZE];

  if(pcap_findalldevs(&interfaces, error) == 0){
    return interfaces;
  }
  else{
    cerr << error << endl;
    exit(-2);
  }
}

void print_interfaces(){
  pcap_if_t* interfaces, *temp;
  int i = 0;

  interfaces = get_active_interfaces();
  cout << "Active interfaces:";
  for(temp = interfaces; temp; temp=temp->next){
    if(temp->flags & PCAP_IF_RUNNING){
      cout << endl << "| " << i++ << " | " <<  temp->name;
    }
  }
  cout << endl;

  return;
}

void print_packet(const u_char* packet, int length){

  for(int i = 0; i < length / 16; i++){
    //print position in packet
    printf("0x%04x\t", i * 16);
    int l = i * 16;
    //print content of packet in hexa
    for(int j = 0 + l; j < 15 + l; j++){
      printf("%x ", packet[j]);
    }
    printf("  ");
    //print content of packet in ascii
    for(int k = 0 + l; k < 16 + l; k++){
      if(isprint(packet[k])){
        printf("%c ", packet[k]);
      }
      else{
        printf(".");
      }
    }
    printf("\n");
  }

  printf("\n");
  return;
}

void print_time(){

  struct timespec ts;
  timespec_get(&ts, TIME_UTC);
  //plus 2 hours
  ts.tv_sec = ts.tv_sec + 7200;
  char buff[100];
  strftime(buff, sizeof buff, "%T", gmtime(&ts.tv_sec));

  printf("%s.%09ld ", buff, ts.tv_nsec / 10^6);

}

void print_all_informations(const struct pcap_pkthdr* pkthdr, const u_char* packet, char* src, char* dst, uint16_t s_port, uint16_t d_port){

  print_time();
  cout << src << " : " << s_port << " > " << dst << " : " << d_port << endl;
  printf("\n");
  int length = pkthdr->len + SIZE_ETHERNET;
  print_packet(packet, length);
  printf("\n");
}

int ip_to_name(char* address, char* name, int ip_type){

  struct sockaddr_in addr;
  memset(&addr, 0, sizeof(struct sockaddr_in));
  int BUFFER_LEN = 128;
  char hbuf[BUFFER_LEN];

  //IPv4
  if(ip_type == 4){
    addr.sin_family = AF_INET;
    inet_pton(AF_INET, address, &addr.sin_addr);

    if (getnameinfo((struct sockaddr*)&addr, sizeof(addr), hbuf, sizeof(hbuf), NULL, 0, 0 ) != 0){
      cerr << "getnameinfo() failed." << endl;
      return 1;
    }
  }

  strcpy(name, hbuf);
  return 0;
}

//https://www.tcpdump.org/pcap.html
// http://yuba.stanford.edu/~casado/pcap/section4.html
// http://yuba.stanford.edu/~casado/pcap/section2.html

int ipv4_processing(const struct pcap_pkthdr* pkthdr, const u_char* packet){

  //ip header
  struct ip *iph = (struct ip *) (packet + SIZE_ETHERNET);

  uint16_t s_port;
  uint16_t d_port;

  //TCP
  if(iph->ip_p == 6){
    struct tcphdr *tcph = (struct tcphdr *) (packet + sizeof (struct ip) + SIZE_ETHERNET);
    s_port = ntohs(tcph->th_sport);
    d_port = ntohs(tcph->th_dport);
  }
  //UDP
  else if(iph->ip_p == 17){
    struct udphdr *udph = (struct udphdr *) (packet + sizeof (struct ip) + SIZE_ETHERNET);
    s_port = ntohs(udph->uh_sport);
    d_port = ntohs(udph->uh_dport);
  }

  char src[INET_ADDRSTRLEN];
  if(inet_ntop(AF_INET, &iph->ip_src, src, INET_ADDRSTRLEN) == NULL){
   perror("inet_ntop\n");
  }
  char dst[INET_ADDRSTRLEN];
  if(inet_ntop(AF_INET, &iph->ip_dst, dst, INET_ADDRSTRLEN) == NULL){
   perror("inet_ntop\n");
  }

  char src_name[128];
  ip_to_name(src, src_name, 4);
  char dst_name[128];
  ip_to_name(dst, dst_name, 4);


  print_all_informations(pkthdr, packet, src_name==NULL ? src : src_name, dst_name==NULL ? dst : dst_name, s_port, d_port);

  return 0;
}


void my_callback(u_char *options, const struct pcap_pkthdr* pkthdr, const u_char* packet){
   /**** Source: http://yuba.stanford.edu/~casado/pcap/section2.html ***/

   struct ether_header *eptr;
   //ethernet header
   eptr = (struct ether_header *) packet;

   if(ntohs(eptr->ether_type) == ETHERTYPE_IP){
     ipv4_processing(pkthdr, packet);
   }
}


char* concat_char_char(char* str1, char* str2){

  char* ch = (char *)malloc(sizeof(char) * (strlen(str1) + strlen(str2) + 1));

  int i = 0;
  for(i; i < strlen(str1); i++){
    ch[i] = str1[i];
  }
  int j = 0;
  for(j; j < strlen(str2); j++){
    ch[i] = str2[j];
    i++;
  }

  return ch;

}

int sniffer(char* interface, char* port, int p_filter, int num_of_packets){
  char err_buf[PCAP_ERRBUF_SIZE];
  char* filter;

  /* 0 = both
   * 1 = tcp_only
   * 2 = udp_only
   */
  switch (p_filter) {
    case 0:
      if(port != NULL){
        filter = "ip and (tcp or udp) and port ";
        filter = concat_char_char(filter, port);
      }
      else{
        filter = "ip and (tcp or udp)";
      }
      break;
    case 1:
      if(port != NULL){
        filter = "ip and tcp and port ";
        filter = concat_char_char(filter, port);
      }
      else{
        filter = "ip and tcp";
      }
      break;
    case 2:
      if(port != NULL){
        filter = "ip and udp and port ";
        filter = concat_char_char(filter, port);
      }
      else{
        filter = "ip and udp";
      }
      break;
  }

  cout << "Actual filter: " << filter << endl;
  cout << "-----------------------------------------" << endl;
  pcap_t* device;
  struct pcap_pkthdr *handler;

  device = pcap_open_live(interface, 1000, 0, -1, err_buf);
  if(device == NULL){
    cerr << "pcap_open_live(): " << err_buf << endl;
    exit(1);
  }

  struct bpf_program fp;      /* hold compiled program     */
  bpf_u_int32 maskp;          /* subnet mask               */
  bpf_u_int32 netp;           /* ip                        */

  /**** Source: http://yuba.stanford.edu/~casado/pcap/section4.html ***/
  if(pcap_compile(device,&fp,filter,0,netp) == -1)
  { fprintf(stderr,"Error calling pcap_compile\n"); exit(1); }

  /* set the compiled program as the filter */
  if(pcap_setfilter(device,&fp) == -1)
  { fprintf(stderr,"Error setting filter\n"); exit(1); }


  pcap_loop(device, num_of_packets, my_callback, reinterpret_cast < u_char* > (filter));

  /*********************************************************/

  return 0;
}

void print_help(){

cout << "ZETA: Sniffer paketů" << endl;
cout << endl;
cout << "Autor: Daniel Štěpánek" << endl;
cout << "Email: xstepa61@stud.fit.vutbr.cz" << endl;
cout << endl;
cout << "Popis: Síťový analyzátor v C/C++, který na určitém síťovém rozhraní zachytává a filtruje pakety." << endl;
cout << endl;
cout << "Soubory: ipk-sniffer.cpp, ipk-sniffer.hpp, Makefile, README, manual.pdf" << endl;
cout << endl;
cout << "Příklad spuštění:  ./ipk-sniffer -i rozhraní [-p ­­port] [--tcp|-t] [--udp|-u] [-n num]" << endl;
cout << "kde" << endl;
cout << "-i eth0 (rozhraní, na kterém se bude poslouchat. Nebude-li tento parametr uveden, vypíše se seznam aktivních rozhraní)" << endl;
cout << "-p 23 (bude filtrování paketů na daném rozhraní podle portu; nebude-li tento parametr uveden, uvažují se všechny porty)" << endl;
cout << "-t nebo --tcp (bude zobrazovat pouze tcp pakety)" << endl;
cout << "-u nebo --udp (bude zobrazovat pouze udp pakety)" << endl;
cout << "Pokud nebude -tcp ani -udp specifikováno, uvažují se TCP a UDP pakety zároveň" << endl;
cout << "-n 10 (určuje počet paketů, které se mají zobrazit; pokud není uvedeno, uvažujte zobrazení pouze 1 paket)" << endl;
cout << endl;
cout << "Implementace: Implementováno v C/C++11, s využitím knihovny libpcap a strukturami v knihovnách netinet." << endl;
cout << endl;
cout << "Omezení: Zachytávání pouze paketů IPv4." << endl;

}

int main(int argc,char **argv){
  int c;
  bool tcp_only = false;
  bool udp_only = false;
  bool interface_set = false;

  char* interface;
  char* port = NULL;
  int num_of_packets = 1;

  /* Argument parsing */
  while(1){
    static struct option long_options[] = {
      {"tcp", no_argument, 0, 't'},
      {"udp", no_argument, 0, 'u'},
      {"help", no_argument, 0, 'h'},
      {0, 0, 0, 0}
    };

    int option_index = 0;

    c = getopt_long(argc, argv, "i:p:n:tuh", long_options, &option_index);

    if(c == -1){
      break;
    }

    switch(c){
      case 0:
        if (long_options[option_index].flag != 0){
          break;
        }
        else if(strcmp(long_options[option_index].name, "tcp") == 0){
          if(udp_only){
            cerr << "udp_only flag is set!" << endl;
            exit(-1);
          }
          tcp_only = true;
          cout << "TCP only" << endl;
        }
        else if(strcmp(long_options[option_index].name, "udp") == 0){
          if(tcp_only){
            cerr << "tcp_only flag is set!" << endl;
            exit(-1);
          }
          udp_only = true;
          cout << "UDP only" << endl;
        }

        break;
      case 'i':
        interface_set = true;
        interface = optarg;
        cout << "Listening on interface: " << interface << endl;
        break;
      case 'p':
        port = optarg;
        cout << "Port number: " << port << endl;
        break;
      case 't':
        tcp_only = true;
        cout << "TCP" << endl;
        break;
      case 'u':
        udp_only = true;
        cout << "UDP" << endl;
        break;
      case 'n':
        for(int i = 0; i < strlen(optarg); i++){
          if((optarg[i] - '0') >= 0 && (optarg[i] - '0') <= 9){
            ;
          }
          else{
            cerr << "Invalid value of -n parameter!" << endl;
            exit(-1);
          }
        }
        num_of_packets = atoi(optarg);
        cout << "Count of packets: " << num_of_packets << endl;
        break;
      case 'h':
        print_help();
        exit(0);
        break;
      case '?':
        cerr << "Usage: ./ipk-sniffer -i rozhraní [-p ­­port] [--tcp|-t] [--udp|-u] [-n num]\n" << endl;
        exit(-1);

    }
  }

  /* Packet filtering */
  int p_filter = 0;
  if(tcp_only && !udp_only){
    p_filter = 1;
  }
  else if(udp_only && !tcp_only){
    p_filter = 2;
  }

  int result = 0;
  if(interface_set){
    result = sniffer(interface, port, p_filter, num_of_packets);
  }
  else{
    print_interfaces();
  }


  return result;
}
