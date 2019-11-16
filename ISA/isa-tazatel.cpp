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
#include<resolv.h>
#include<netdb.h>
#include<stdbool.h>

using namespace std;

const int TCP_PORT = 43;
const int UDP_PORT = 53;

// ./isa-tazatel -q www.fit.vutbr.cz -w whois.ripe.net



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

  //Source: https://docstore.mik.ua/orelly/networking_2ndEd/dns/ch15_02.htm?fbclid=IwAR0rcGQ2T1muWvRsFFbPtfMzq4rmeW2efUGbJEMyXO1KkoMXgjoGT5JJSZY

  bool ns_failed = false;

  // NS RECORD

  res_init();

  if(res_search(hostname, ns_c_in, ns_t_ns, buffer, sizeof(buffer)) == -1){
    ns_failed = true;
  }

  if((query_len = res_mkquery(ns_o_query, hostname, ns_c_in, ns_t_ns, NULL, 0, NULL, buffer, sizeof(buffer))) == -1){
    ns_failed = true;
  }

  if((msg_size = res_query(hostname, ns_c_in, ns_t_ns, buffer, sizeof(buffer))) == -1){
    ns_failed = true;
  }

  if(!ns_failed){
    if (ns_initparse(buffer, msg_size, &msg) < 0) {
       fprintf(stderr, "ns_initparse: %s\n", strerror(errno));
    }

    char* ns_list[msg_size];
    char* ns_index;
    char* after_ns;
    int ns_count = 0;
    bool ns_found = false;

    for (int i = 0; i < msg_size; i++){
      ns_parserr(&msg, ns_s_an, i, &rr);
      ns_sprintrr(&msg, &rr, NULL, NULL, dispbuf, sizeof(dispbuf));

      ns_index = strstr(dispbuf, "NS");
      after_ns = strndup(ns_index+3, strlen(ns_index) - 3);

      if(ns_count == 0){
        ns_list[0] = after_ns;
        ns_count++;
      }

      for(int j = 0; j < ns_count; j++){
        if(strcasecmp(ns_list[j], after_ns) == 0){
          ns_found = true;

        }
      }

      if(!ns_found){
        ns_list[ns_count] = after_ns;
        ns_count++;
      }

      ns_found = false;

    }

    cout << "NS:" << endl;
    for(int i = 0; i < ns_count; i++){
      cout << "\t" << ns_list[i] << endl;
    }

  }

/*************************************************************************/

  // SOA RECORD

  bool soa_failed = false;

  res_init();

  if(res_search(hostname, ns_c_in, ns_t_soa, buffer, sizeof(buffer)) == -1){
    soa_failed = true;
  }

  if((query_len = res_mkquery(ns_o_query, hostname, ns_c_in, ns_t_soa, NULL, 0, NULL, buffer, sizeof(buffer))) == -1){
    soa_failed = true;
  }

  if((msg_size = res_query(hostname, ns_c_in, ns_t_soa, buffer, sizeof(buffer))) == -1){
    soa_failed = true;
  }

  if(!soa_failed){
    if (ns_initparse(buffer, msg_size, &msg) < 0) {
       fprintf(stderr, "ns_initparse: %s\n", strerror(errno));
    }

    char* soa_list[msg_size];
    char* soa_index;
    char* after_soa;

    int soa_count = 0;

    bool soa_found = false;

    for (int i = 0; i < msg_size; i++){
      ns_parserr(&msg, ns_s_an, i, &rr);
      ns_sprintrr(&msg, &rr, NULL, NULL, dispbuf, sizeof(dispbuf));

      soa_index = strstr(dispbuf, "SOA");
      after_soa = strndup(soa_index + 4, strlen(soa_index));
      char soa[128];

      for(int i = 0; after_soa[i] != ' '; i++){
        soa[i] = after_soa[i];
        soa[i+1] = '\0';

      }

      if(soa_count == 0){
        soa_list[0] = soa;
        soa_count++;
      }

      for(int j = 0; j < soa_count; j++){
        if(strcasecmp(soa_list[j], soa) == 0){
          soa_found = true;

        }
      }

      if(!soa_found){
        soa_list[soa_count] = soa;
        soa_count++;
      }

      soa_found = false;

    }

    cout << "SOA:" << endl;
    for(int i = 0; i < soa_count; i++){
      cout << "\t" << soa_list[i] << endl;
    }
  }

/*******************************************************************************/

  // MX

  bool mx_failed = false;

  res_init();

  if(res_search(hostname, ns_c_in, ns_t_mx, buffer, sizeof(buffer)) == -1){
    mx_failed = true;
  }
  if((query_len = res_mkquery(ns_o_query, hostname, ns_c_in, ns_t_mx, NULL, 0, NULL, buffer, sizeof(buffer))) == -1){
    mx_failed = true;
  }
  if((msg_size = res_query(hostname, ns_c_in, ns_t_mx, buffer, sizeof(buffer))) == -1){
    mx_failed = true;
  }

  if(!mx_failed){
    if (ns_initparse(buffer, msg_size, &msg) < 0) {
      fprintf(stderr, "ns_initparse: %s\n", strerror(errno));
    }

    char* mx_list[msg_size];
    char* mx_index;

    int mx_count = 0;

    bool mx_found = false;

    for (int i = 0; i < msg_size; i++){
      ns_parserr(&msg, ns_s_an, i, &rr);
      ns_sprintrr(&msg, &rr, NULL, NULL, dispbuf, sizeof(dispbuf));

      mx_index = strstr(dispbuf, "MX");

      char* mx = strndup(mx_index + 5, strlen(mx_index));

      if(mx_count == 0){
        mx_list[0] = mx;
        mx_count++;
      }

      for(int j = 0; j < mx_count; j++){
        if(strcasecmp(mx_list[j], mx) == 0){
          mx_found = true;

        }
      }

      if(!mx_found){
        mx_list[mx_count] = mx;
        mx_count++;
      }

      mx_found = false;

    }

    cout << "MX:" << endl;
    for(int i = 0; i < mx_count; i++){
      cout << "\t" << mx_list[i] << endl;
    }

  }

/*******************************************************************************/
    // A

  bool a_failed = false;

  res_init();

  if(res_search(hostname, ns_c_in, ns_t_a, buffer, sizeof(buffer)) == -1){
    a_failed = true;
  }
  if((query_len = res_mkquery(ns_o_query, hostname, ns_c_in, ns_t_a, NULL, 0, NULL, buffer, sizeof(buffer))) == -1){
    a_failed = true;
  }
  if((msg_size = res_query(hostname, ns_c_in, ns_t_a, buffer, sizeof(buffer))) == -1){
    a_failed = true;
  }

  if(!a_failed){
    if (ns_initparse(buffer, msg_size, &msg) < 0) {
       fprintf(stderr, "ns_initparse: %s\n", strerror(errno));
    }

    char* a_list[msg_size];
    char* a_index;

    int a_count = 0;
    bool a_found = false;

    for (int i = 0; i < msg_size; i++){
      ns_parserr(&msg, ns_s_an, i, &rr);
      ns_sprintrr(&msg, &rr, NULL, NULL, dispbuf, sizeof(dispbuf));

      a_index = strstr(dispbuf, "A");

      char* a = strndup(a_index + 2, strlen(a_index));

      if(a_count == 0){
        a_list[0] = a;
        a_count++;
      }

      for(int j = 0; j < a_count; j++){
        if(strcasecmp(a_list[j], a) == 0){
          a_found = true;
        }
      }

      if(!a_found){
        a_list[a_count] = a;
        a_count++;
      }

      a_found = false;

    }

    cout << "A:" << endl;
    for(int i = 0; i < a_count; i++){
      cout << "\t" << a_list[i] << endl;
    }

  }

/*******************************************************************************/
    // AAAA

  bool aaaa_failed = false;

  res_init();

  if(res_search(hostname, ns_c_in, ns_t_aaaa, buffer, sizeof(buffer)) == -1){
    aaaa_failed = true;
  }
  if((query_len = res_mkquery(ns_o_query, hostname, ns_c_in, ns_t_aaaa, NULL, 0, NULL, buffer, sizeof(buffer))) == -1){
    aaaa_failed = true;
  }
  if((msg_size = res_query(hostname, ns_c_in, ns_t_aaaa, buffer, sizeof(buffer))) == -1){
    aaaa_failed = true;
  }

  if(!aaaa_failed){
    if (ns_initparse(buffer, msg_size, &msg) < 0) {
       fprintf(stderr, "ns_initparse: %s\n", strerror(errno));
    }

    char* aaaa_list[msg_size];
    char* aaaa_index;

    int aaaa_count = 0;
    bool aaaa_found = false;

    for (int i = 0; i < msg_size; i++){
      ns_parserr(&msg, ns_s_an, i, &rr);
      ns_sprintrr(&msg, &rr, NULL, NULL, dispbuf, sizeof(dispbuf));

      aaaa_index = strstr(dispbuf, "AAAA");

      char* aaaa = strndup(aaaa_index + 5, strlen(aaaa_index));

      if(aaaa_count == 0){
        aaaa_list[0] = aaaa;
        aaaa_count++;
      }

      for(int j = 0; j < aaaa_count; j++){
        if(strcasecmp(aaaa_list[j], aaaa) == 0){
          aaaa_found = true;

        }
      }

      if(!aaaa_found){
        aaaa_list[aaaa_count] = aaaa;
        aaaa_count++;
      }

      aaaa_found = false;

    }

    cout << "AAAA:" << endl;
    for(int i = 0; i < aaaa_count; i++){
      cout << "\t" << aaaa_list[i] << endl;
    }

  }

/*******************************************************************************/

  // CNAME

  bool cname_failed = false;

  res_init();

  if(res_search(hostname, ns_c_in, ns_t_cname, buffer, sizeof(buffer)) == -1){
    cname_failed = true;
  }
  if((query_len = res_mkquery(ns_o_query, hostname, ns_c_in, ns_t_cname, NULL, 0, NULL, buffer, sizeof(buffer))) == -1){
    cname_failed = true;
  }
  if((msg_size = res_query(hostname, ns_c_in, ns_t_cname, buffer, sizeof(buffer))) == -1){
    cname_failed = true;
  }

  if(!cname_failed){
    if (ns_initparse(buffer, msg_size, &msg) < 0) {
       fprintf(stderr, "ns_initparse: %s\n", strerror(errno));
    }

    char* cname_list[msg_size];
    char* cname_index;

    int cname_count = 0;
    bool cname_found = false;

    for (int i = 0; i < msg_size; i++){
      ns_parserr(&msg, ns_s_an, i, &rr);
      ns_sprintrr(&msg, &rr, NULL, NULL, dispbuf, sizeof(dispbuf));

      cname_index = strstr(dispbuf, "CNAME");
      char* cname = strndup(cname_index + 5, strlen(cname_index));

      if(cname_count == 0){
       cname_list[0] = cname;
       cname_count++;
      }

      for(int j = 0; j < cname_count; j++){
        if(strcasecmp(cname_list[j], cname) == 0){
          cname_found = true;
        }
      }

      if(!cname_found){
       cname_list[cname_count] = cname;
       cname_count++;
      }

     cname_found = false;

    }

    cout << "CNAME:" << endl;
    for(int i = 0; i < cname_count; i++){
      cout << "\t" << cname_list[i] << endl;
    }

  }

/*******************************************************************************/

  // PTR

  bool ptr_failed = false;

  res_init();

  if(res_search(hostname, ns_c_in, ns_t_ptr, buffer, sizeof(buffer)) == -1){
    ptr_failed = true;
  }
  if((query_len = res_mkquery(ns_o_query, hostname, ns_c_in, ns_t_ptr, NULL, 0, NULL, buffer, sizeof(buffer))) == -1){
    ptr_failed = true;
  }
  if((msg_size = res_query(hostname, ns_c_in, ns_t_ptr, buffer, sizeof(buffer))) == -1){
    ptr_failed = true;
  }

  if(!ptr_failed){
    if (ns_initparse(buffer, msg_size, &msg) < 0) {
       fprintf(stderr, "ns_initparse: %s\n", strerror(errno));
    }

    char* ptr_list[msg_size];
    char* ptr_index;

    int ptr_count = 0;

    bool ptr_found = false;

    for (int i = 0; i < msg_size; i++){
      ns_parserr(&msg, ns_s_an, i, &rr);
      ns_sprintrr(&msg, &rr, NULL, NULL, dispbuf, sizeof(dispbuf));
      ptr_index = strstr(dispbuf, "AAAA");

      char* ptr = strndup(ptr_index + 5, strlen(ptr_index));

      if(ptr_count == 0){
      ptr_list[0] = ptr;
        ptr_count++;
      }

      for(int j = 0; j < ptr_count; j++){
        if(strcasecmp(ptr_list[j], ptr) == 0){
          ptr_found = true;
        }
      }

      if(!ptr_found){
        ptr_list[ptr_count] = ptr;
        ptr_count++;
      }

      ptr_found = false;

    }

    cout << "PTR:" << endl;
    for(int i = 0; i < ptr_count; i++){
      cout << "\t" << ptr_list[i] << endl;
    }

  }


  return;
}

void get_whois(char* ip, char *whois_ip, int ip_type, int ip_whois_type){

  int n, nBytes;
  char buffer[4096];
  char whois_query[64];

  int clientSocket;
  struct sockaddr_in serverAddr;
  socklen_t addr_size;

  //Whois query
  strcpy(whois_query, ip);
  strcat(whois_query, "\r\n");

  //Socket for whois server
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

  //Read Whois response and print
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
    if((ip_dns_type = hostname_to_ip(dns_hostname, dns_ip)) == 20){
      cerr << "hostname_to_ip(dns_ip) failed\n";
      exit(20);
    }
  }

/***********************************************************/

  char ip[64];
  char hostname[ip_hostname.size() + 1];
  strcpy(hostname, ip_hostname.c_str());
  if((ip_type = hostname_to_ip(hostname, ip)) == 20){
    cerr << "hostname_to_ip(ip) failed\n";
    exit(20);
  }

// Get hostname from IP for DNS query
  if(isdigit(hostname[0]) || hostname[0] == ':'){

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(struct sockaddr_in));

    struct sockaddr_in6 addr6;
    memset(&addr6, 0, sizeof(struct sockaddr_in6));

    char hbuf[128];

    //IPv4
    if(ip_type == 4){
      addr.sin_family = AF_INET;
      inet_pton(AF_INET, hostname, &addr.sin_addr);

      if (getnameinfo((struct sockaddr*)&addr, sizeof(addr), hbuf, sizeof(hbuf), NULL, 0, 0 ) != 0){
        cerr << "getnameinfo() failed." << endl;
        exit(20);
      }
    }
    //IPv6
    else if(ip_type == 6){
      addr6.sin6_family = AF_INET6;
      inet_pton(AF_INET6, hostname, &addr6.sin6_addr);

      if (getnameinfo((struct sockaddr*)&addr6, sizeof(addr6), hbuf, sizeof(hbuf), NULL, 0, 0 ) != 0){
        cerr << "getnameinfo() failed." << endl;
        exit(20);
      }
    }

    strcpy(hostname, hbuf);

  }

  char whois_ip[64];
  char whois_hostname[whois_server.size() + 1];
  strcpy(whois_hostname, whois_server.c_str());
  if((ip_whois_type = hostname_to_ip(whois_hostname, whois_ip)) == 20){
    cerr << "hostname_to_ip(whois_ip) failed\n";
    exit(20);
  }


/***********************************************************/

  get_dns(hostname, dns_ip, ip_type, ip_dns_type, d_flag);
  get_whois(ip, whois_ip, ip_type, ip_whois_type);

  return 0;
}
