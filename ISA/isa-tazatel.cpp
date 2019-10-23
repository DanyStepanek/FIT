#include<iostream>
#include<unistd.h>
#include<string>
#include<cstring>
#include<netdb.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<time.h>

using namespace std;

const int TCP_PORT = 43;
const int UDP_PORT = 53;

void get_dns(char *ip, char *dns_ip, int ip_type, int ip_dns_type){

  int n, nBytes;
  char buffer[8192];
  int clientSocket;
  struct sockaddr_in serverAddr;
  socklen_t addr_size;
  struct timeval tm;

  /*Create UDP socket*/
  clientSocket = socket(AF_INET, SOCK_DGRAM, 0);

  /*Configure settings in address struct*/
  if(ip_dns_type == 4){
    serverAddr.sin_family = AF_INET;
    inet_pton(AF_INET, dns_ip, &serverAddr.sin_addr);
  }
  else{
    serverAddr.sin_family = AF_INET6;
    inet_pton(AF_INET6, dns_ip, &serverAddr.sin_addr);
  }

  tm.tv_sec = 2;
  tm.tv_usec = 0;
  setsockopt(clientSocket, SOL_SOCKET, SO_RCVTIMEO, (const char *)&tm, sizeof(tm));
  serverAddr.sin_port = htons(UDP_PORT);  //dns listen on port 53
  memset(serverAddr.sin_zero, '\0', sizeof(serverAddr.sin_zero));

  /*Initialize size variable to be used later on*/
  addr_size = sizeof(serverAddr);

  char dns_query[64];

  strcpy(dns_query, ip);
  strcat(dns_query, "\r\n");

  nBytes = strlen(dns_query) + 1;

  /*Send message to server*/
  if(sendto(clientSocket, dns_query, nBytes, MSG_DONTWAIT, (struct sockaddr *)&serverAddr, addr_size) == -1){
    cerr << "DNS: sendto failed " << endl;
    exit(-1);
  }

  cout << "=== DNS ===" << endl;

  while((n = recv(clientSocket, (char *)buffer, strlen(buffer) -1, MSG_WAITALL)) > 0){
    buffer[n] = '\0';
    cout << "DNS: Received from server: " << buffer << endl;
  }

  close(clientSocket);

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
    unsigned int i = 0;
    unsigned int j = 0;
    while(buffer[i] != '\0' && i < strlen(buffer) - j){
      if(buffer[i] == '%' || buffer[i] == '#'){
        j++;
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
  if(!d_flag){
    /*
      FILE *fp=fopen("/etc/resolv.conf","r");
        char tmp[256]={0x0};
        while(fp && fgets(tmp, sizeof(tmp), fp))
        {
            if (strstr(tmp, "nameserver"))
                printf("%s", tmp);

        }
        if(fp) fclose(fp);
    */
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

  char dns_ip[64];
  char dns_hostname[dns_server.size() + 1];
  strcpy(dns_hostname, dns_server.c_str());
  if((ip_dns_type = hostname_to_ip(dns_hostname, dns_ip)) != 20){
    cout << "dns ip: " << dns_ip << endl;
  }
  else{
    cerr << "hostname_to_ip(dns_ip) failed\n";
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

  get_dns(ip, dns_ip, ip_type, ip_dns_type);
  get_whois(ip, whois_ip, ip_type, ip_whois_type);

  return 0;
}
