#include<iostream>
#include<unistd.h>
#include<string>
#include<cstring>
#include<netdb.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<arpa/nameser.h>
#include<time.h>
#include<resolv.h>
#include<netdb.h>

using namespace std;

const int TCP_PORT = 43;
const int UDP_PORT = 53;

//https://docstore.mik.ua/orelly/networking_2ndEd/dns/ch15_02.htm?fbclid=IwAR0rcGQ2T1muWvRsFFbPtfMzq4rmeW2efUGbJEMyXO1KkoMXgjoGT5JJSZY

void get_dns(char *hostname, char *dns_ip, int ip_type, int ip_dns_type, bool d_flag){

  unsigned char buffer[4096];
  char dispbuf[4096];
  ns_msg msg;
  ns_rr rr;
  int msg_size;
  int query_len = 0;

  if((strstr(hostname, "www.")) != NULL){
    char cut_host[strlen(hostname - 3)];
    for(unsigned i = 0; i < strlen(hostname); i++){
      cut_host[i] = hostname[i+4];
    }
    strcpy(hostname, cut_host);

  }

  cout << "===DNS===" << endl;


  if(!d_flag){

    res_init();

    if(res_search(hostname, ns_c_in, ns_t_ns, buffer, sizeof(buffer)) == -1){
      cerr << "RES_SEARCH: ERROR" << endl;
      perror(hostname);
    }

    if((query_len = res_mkquery(ns_o_query, hostname, ns_c_in, ns_t_ns, NULL, 0, NULL, buffer, sizeof(buffer))) == -1){
      cerr << "RES_MKQUERY: ERROR" << endl;
      perror(hostname);
    }

    // A RECORD
    if((msg_size = res_query(hostname, ns_c_in, ns_t_ns, buffer, sizeof(buffer))) == -1){
      cerr << "RES_QUERY: ERROR" << endl;
      perror(hostname);
    }


    if(res_send(reinterpret_cast<unsigned char*>(hostname), query_len, reinterpret_cast<unsigned char*>(buffer), sizeof(buffer)) == -1){
      cerr << "RES_SEND: ERROR" << endl;
      perror(hostname);
    }

    if (ns_initparse(buffer, msg_size, &msg) < 0) {
       fprintf(stderr, "ns_initparse: %s\n", strerror(errno));

    }

    char* ns_list[msg_size];
    int ns_count = 0;
    ns_rr rr;
    cout << "msg_size " << msg_size << endl;
    for (int i = 0; i < msg_size; i++){
      ns_parserr(&msg, ns_s_an, i, &rr);
      ns_sprintrr(&msg, &rr, NULL, NULL, dispbuf, sizeof(dispbuf));

      if (ns_name_uncompress(
         ns_msg_base(msg),/* Start of the message */
         ns_msg_end(msg), /* End of the message */
         ns_rr_rdata(rr), /* Position in the message */
         ns_list[msg_size], /* Result */
         msg_size) /* Size of nsList buffer */
          < 0) { /* Negative: error */
            (void) fprintf(stderr, "ns_name_uncompress failed\n");
             exit(1);
            }
      if(ns_count == 0){
        ns_list[0] = dispbuf;
        ns_count++;
      }
      for(int j = 0; j < ns_count; j++){
        cout<< "druhy cyklus " << j << " " << ns_count << " " << ns_list[j] << endl;
        if(strcasecmp(ns_list[j], dispbuf) != 0){
          ns_count++;
          cout << ns_count << " ns_count" << endl;
          ns_list[ns_count] = dispbuf;
        }
      }


    }

    for(int i = 0; i < ns_count; i++){
      printf("\t%s \n", ns_list[i]);
    }


/*    for(i = 0, dup=0; (i < *nsNum) && !dup; i++)
     dup = !strcasecmp(nsList[i], nsList[*nsNum]);
      if(dup)
       free(nsList[*nsNum]);
     else
      (*nsNum)++;
*/




  }

/*



  if(ip_dns_type == 4){
    clientSocket = socket(AF_INET, SOCK_DGRAM, 0);
    serverAddr.sin_family = AF_INET;
    inet_pton(AF_INET, dns_ip, &serverAddr.sin_addr);
  }
  else{
    clientSocket = socket(AF_INET6, SOCK_DGRAM, 0);
    serverAddr.sin_family = AF_INET6;
    inet_pton(AF_INET6, dns_ip, &serverAddr.sin_addr);
  }

  tm.tv_sec = 2;
  tm.tv_usec = 0;
  setsockopt(clientSocket, SOL_SOCKET, SO_RCVTIMEO, (const char *)&tm, sizeof(tm));
  serverAddr.sin_port = htons(UDP_PORT);  //dns listen on port 53
  memset(serverAddr.sin_zero, '\0', sizeof(serverAddr.sin_zero));


  addr_size = sizeof(serverAddr);

  char dns_query[64];

  strcpy(dns_query, hostname);
  for(int i = 0; i < strlen(hostname); i++){
    dns_query[i] = hostname[i];
  }
  for(int i = strlen(dns_query); i < strlen(dns_query) + 32; i++){
    dns_query[i] = '\0';
  }

  strcat(dns_query, "\r\n");

  cout << dns_query << endl;

  nBytes = strlen(dns_query) + 1;


  if(sendto(clientSocket, dns_query, nBytes, MSG_DONTWAIT, (struct sockaddr *)&serverAddr, addr_size) == -1){
    cerr << "DNS: sendto failed " << endl;
    exit(-1);
  }

  cout << "=== DNS ===" << endl;


  while((n = recv(clientSocket, (char *)buffer, strlen(buffer) -1, MSG_WAITALL)) != 0){

    cout << "n: " << n << endl;
    cout << "DNS: Received from server: " << buffer[5] << endl;
  }

  close(clientSocket);
*/
  return;
}

void get_whois(char* ip, char *whois_ip, int ip_type, int ip_whois_type){

  int n, nBytes;
  char buffer[8192];
  char whois_query[64];

  int clientSocket;
  struct sockaddr_in serverAddr;
  socklen_t addr_size;

  strcpy(whois_query, ip);
  strcat(whois_query, "\r\n");

  clientSocket = socket(AF_INET, SOCK_STREAM, 0);
  if(ip_whois_type == 4){
    serverAddr.sin_family = AF_INET;
    inet_pton(AF_INET, whois_ip, &serverAddr.sin_addr);
  }
  else{
    serverAddr.sin_family = AF_INET6;
    inet_pton(AF_INET6, whois_ip, &serverAddr.sin_addr);
  }

  serverAddr.sin_port = htons(TCP_PORT);  //whois listen on port 43

  memset(serverAddr.sin_zero, '\0', sizeof(serverAddr.sin_zero));

  addr_size = sizeof(serverAddr);

  nBytes = strlen(whois_query) + 1;

  if (connect(clientSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) != 0){
    cerr << "WHOIS: connect failed " << endl;
    exit(-1);
  }

  if(send(clientSocket, whois_query, nBytes, 0) == -1){
    cerr << "WHOIS: Socket sending failed. " << endl;
    exit(-1);
  }

  cout << "=== WHOIS ===" << endl;

  while((n = read(clientSocket, buffer, sizeof(buffer) - 1)) > 0){
    int i = 0;
    while(buffer[i] != '\0' && i < n){
      if(buffer[i] == '%' || buffer[i] == '#'){
        while(buffer[i] != '\n'){
          i++;
        }
      }
      else{
        cout << buffer[i];
      }
      i++;
    }
  }
  cout << endl;
  close(clientSocket);

  return;
}

int hostname_to_ip(char* hostname, char* ip){

  struct addrinfo hints, *res;
  char addrstr[100];
  void *ptr;
  int err;

  memset (&hints, 0, sizeof (hints));
  hints.ai_family = PF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_flags |= AI_CANONNAME;

  if((err = getaddrinfo(hostname, NULL, &hints, &res)) != 0){
    cerr << "Get host IP failed." << endl;
    return 20;
  }

  printf("Host: %s\n", hostname);

  while(res){
    inet_ntop(res->ai_family, res->ai_addr->sa_data, addrstr, 100);

    switch(res->ai_family){
      case AF_INET:
        ptr = &((struct sockaddr_in *)res->ai_addr)->sin_addr;
        break;
      case AF_INET6:
        ptr = &((struct sockaddr_in6 *)res->ai_addr)->sin6_addr;
        break;
    }

    inet_ntop(res->ai_family, ptr, addrstr, 100);
    printf("IPv%d address: %s (%s)\n", res->ai_family == PF_INET6 ? 6 : 4,
        addrstr, res->ai_canonname);
    strcpy(ip, addrstr);
    if(res->ai_family == PF_INET){
      return 4;
    }
    else{
      return 6;
    }


    res = res->ai_next;
  }

  return 20;

}

void dns_output(){
  cout << "=== DNS ===" << endl;
  cout << "A: " << endl;
  cout << "AAAA: " << endl;
  cout << "SDA: " << endl;
  cout << "admin email: " << endl;

  return;
}

void whois_output(){
  cout << "=== WHOIS ===" << endl;
  cout << "inetnum: " << endl;
  cout << "netname: " << endl;
  cout << "descr: " << endl;
  cout << "country: " << endl;
  cout << "admin-c: " << endl;
  cout << "address: " << endl;
  cout << "address: " << endl;
  cout << "address: " << endl;
  cout << "address: " << endl;
  cout << "phone: " << endl;
  cout << "phone: " << endl;

  return;
}

int main(int argc, char** argv){

  int c = 0;
  int ip_type, ip_dns_type, ip_whois_type = 0;

  bool q_flag = false;
  bool w_flag = false;
  bool d_flag = false;

  char dns_ip[64] = {0x0};

  string ip_hostname;
  string whois_server;
  string dns_server;

/***********************************************************/

  while((c = getopt(argc, argv, ":q:w:d:")) != -1){
    switch(c){
      case 'q':
        if(optarg){
          ip_hostname = optarg;
          q_flag = true;
        }
      break;

      case 'w':
        if(optarg){
           whois_server = optarg;
           w_flag = true;
         }
      break;

      case 'd':
        if(optarg){
          dns_server = optarg;
          d_flag = true;
        }
      break;

      case ':':
        cerr << "Option needs a value." << endl;
        exit(10);
      break;

      case '?':
        cerr << "Unknown option." << endl;
        exit(10);
      break;
    }
  }

  for(; optind < argc; optind++){
    cerr << "Unknown argument(s)" << endl;
    exit(10);
  }

  if(!q_flag){
    cerr << "Missing -q argument." << endl;
    exit(10);
  }
  if(!w_flag){
    cerr << "Missing -w argument." << endl;
    exit(10);
  }
  if(d_flag){
    char dns_hostname[dns_server.size() + 1];
    strcpy(dns_hostname, dns_server.c_str());
    if((ip_dns_type = hostname_to_ip(dns_hostname, dns_ip)) != 20){
      cout << "dns ip: " << dns_ip << endl;
    }
    else{
      cerr << "hostname_to_ip(dns_ip) failed\n";
      exit(20);
    }
  }

/***********************************************************/

  char ip[64];
  char hostname[ip_hostname.size() + 1];
  strcpy(hostname, ip_hostname.c_str());
  if((ip_type = hostname_to_ip(hostname, ip)) != 20){
    cout << "host ip: " << ip << endl;
  }
  else{
    cerr << "hostname_to_ip(ip) failed\n";
    exit(20);
  }



  char whois_ip[64];
  char whois_hostname[whois_server.size() + 1];
  strcpy(whois_hostname, whois_server.c_str());
  if((ip_whois_type = hostname_to_ip(whois_hostname, whois_ip)) != 20){
    cout << "whois ip: " << whois_ip << endl;
  }
  else{
    cerr << "hostname_to_ip(whois_ip) failed\n";
    exit(20);
  }

/***********************************************************/

  get_dns(hostname, dns_ip, ip_type, ip_dns_type, d_flag);
  get_whois(ip, whois_ip, ip_type, ip_whois_type);

  return 0;
}
