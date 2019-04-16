#include <pcap.h>
#include <iostream>
#include <stdlib.h>
#include <getopt.h>
#include <netdb.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <string.h>


using namespace std;

void callback_function(u_char *arg, const struct pcap_pkthdr* pkthdr, const u_char* packet){

  int i = 0;
  static int count = 0;

  cout << "Count: " << ++count << "\n";
  cout << "Size: " << pkthdr->len << "\n";
  cout << "Payload: \n";

  for(int i = 0; i < pkthdr->len; i++){
    if(isprint(packet[i])){
      cout << packet[i];
    }
    else{
      cout << " . ";
    }

    if((i % 16 == 0 && i != 0) || i == pkthdr->len - 1){
      cout << "\n";
    }
  }


}


int main(int argc,char **argv){

  string tcpPorts = "";
  string udpPorts = "";
  char *interface, errbuf[PCAP_ERRBUF_SIZE];
  struct hostent *domain;

  cout << "Interesting ports on " << "localhost " << "\n";

  cout << "PORT\t"  << "STATE\n";

  interface = pcap_lookupdev(errbuf);

  for(int i=1; i < argc; i += 2){

    if(strcmp(argv[i], "-i") == 0){
      interface = argv[i+1];
      cout << "argv: " << argv[i] << "\n";
    }
    else if(strcmp(argv[i],"-pt") == 0){
      tcpPorts = argv[i+1];
      cout << "argv: " << argv[i] << "\n";
    }
    else if(strcmp(argv[i],"-pu") == 0){
      udpPorts = argv[i+1];
      cout << "argv: " << argv[i] << "\n";
    }
    else{
      domain = gethostbyname(argv[i]);

      if (domain == NULL) {
         cout << "gethostbyname() failed\n";
      }
      else {
        cout << domain->h_name << ": ";
        unsigned int i=0;
        while ( domain->h_addr_list[i] != NULL) {
          cout << inet_ntoa( *( struct in_addr*)( domain->h_addr_list[i])) << " ";
          i++;
        }
        cout << "\n";
      }
    }


  }




  cout << "Device:" << interface << "\n";


  pcap_t *handle;                          /* Session handle */
  struct bpf_program filter;              /* The compiled filter expression */
  char filter_app[] = "80";          /* The filter expression */
  bpf_u_int32 mask;                       /* The netmask of our sniffing device */
  bpf_u_int32 net;                          /* The IP of our sniffing device */
  pcap_lookupnet(interface, &net, &mask, errbuf);
  handle = pcap_open_live(interface, BUFSIZ, 1, -1, errbuf);
  if(handle == NULL){
    cout << errbuf;
    return 1;
  }

  pcap_compile(handle, &filter, filter_app, 0, net);
  pcap_setfilter(handle, &filter);

  pcap_loop(handle, -1, callback_function, NULL);

  return 0;

/*
  if(argc == 8){
    for(int i = 0;i < 8;i++){
        cout << argv[i];
        cout << "\n";
    }
  }
  else if(argc == 6){
    for(int i = 0;i < 6;i++){
      cout << argv[i];
      cout << " ";
    }
    cout << "\n";
  }
  else{
    cerr << "Wrong count of parameters\n";
    exit(1);
  }

  return 0;

*/
}
