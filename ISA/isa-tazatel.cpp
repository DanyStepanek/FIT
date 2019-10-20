#include<iostream>
#include<unistd.h>
#include<string>
#include<cstring>
#include<netdb.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>


using namespace std;

int hostname_to_ip(char* hostname, char* ip){

  struct hostent *h;
  struct in_addr **addr_list;

  if((h = gethostbyname(hostname)) == NULL){
    cerr << "Get host IP failed." << endl;
    return 20;
  }

  addr_list = (struct in_addr **)h->h_addr_list;

  if(addr_list[0] != NULL){
    strcpy(ip, inet_ntoa(*addr_list[0]));
    return 0;
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
  const int TCP_PORT = 43;
  const int UDP_PORT = 53;
  bool q_flag = false;
  bool w_flag = false;
  bool d_flag = false;

  string ip_hostname;
  string whois_server;
  //implicitne 1.1.1.1
  string dns_server = "1.1.1.1";

  int clientSocket, portNum, nBytes;
  char buffer[8192];
  struct sockaddr_in serverAddr;
  socklen_t addr_size;

/***********************************************************/

  while((c = getopt(argc, argv, ":q:w:d:")) != -1){
    switch(c){
      case 'q':
        if(optarg){
          ip_hostname = optarg;
  //        cout << "q: " << ip_hostname << endl;
          q_flag = true;
        }
      break;

      case 'w':
        if(optarg){
           whois_server = optarg;
    //       cout << "w: " << whois_server << endl;
           w_flag = true;
         }
      break;

      case 'd':
        if(optarg){
          dns_server = optarg;
  //        cout << "d: " << dns_server << endl;
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

/***********************************************************/

  char ip[16];
  char hostname[ip_hostname.size() + 1];
  strcpy(hostname, ip_hostname.c_str());
  if(hostname_to_ip(hostname, ip) == 0){
    cout << "host ip: " << ip << endl;
  }
  else{
    cerr << "hostname_to_ip(ip) failed\n";
    exit(20);
  }

  char dns_ip[16];
  char dns_hostname[dns_server.size() + 1];
  strcpy(dns_hostname, dns_server.c_str());
  if(hostname_to_ip(dns_hostname, dns_ip) == 0){
    cout << "dns ip: " << dns_ip << endl;
  }
  else{
    cerr << "hostname_to_ip(dns_ip) failed\n";
    exit(20);
  }

  char whois_ip[16];
  char whois_hostname[whois_server.size() + 1];
  strcpy(whois_hostname, whois_server.c_str());
  if(hostname_to_ip(whois_hostname, whois_ip) == 0){
    cout << "whois ip: " << whois_ip << endl;
  }
  else{
    cerr << "hostname_to_ip(whois_ip) failed\n";
    exit(20);
  }


// https://gist.github.com/fffaraz/9d9170b57791c28ccda9255b48315168
// http://www.nsc.ru/cgi-bin/www/unix_help/unix-man?gethostbyname+3
// https://www.geeksforgeeks.org/convert-string-char-array-cpp/
// https://wis.fit.vutbr.cz/FIT/st/course-sl.php?id=705161&item=75303&cpa=1

  /***************** ==DNS== *******************************************************/

  /*Create UDP socket*/
  clientSocket = socket(AF_INET, SOCK_DGRAM, 0);

  /*Configure settings in address struct*/
  serverAddr.sin_family = AF_INET;
  serverAddr.sin_port = htons(UDP_PORT);  //dns listen on port 53
  serverAddr.sin_addr.s_addr = inet_addr(dns_ip);
  memset(serverAddr.sin_zero, '\0', sizeof(serverAddr.sin_zero));

  /*Initialize size variable to be used later on*/
  addr_size = sizeof(serverAddr);

  char dns_query[64];

  strcpy(dns_query, ip);
  strcat(dns_query, "\r\n");

  nBytes = strlen(dns_query) + 1;

  /*Send message to server*/
  if(sendto(clientSocket, dns_query, nBytes, MSG_CONFIRM, (struct sockaddr *)&serverAddr, addr_size) == -1){
    cerr << "DNS: sendto failed " << endl;
    exit(-1);
  }

  cout << "DNS: socket send" << endl;

  int n = 0;
  unsigned int len;

/*  while(n = recvfrom(clientSocket, (char *)buffer, strlen(buffer) -1, MSG_WAITALL,
      (struct sockaddr *)&serverAddr, &len) > 0){

      buffer[n] = '\0';
      cout << "DNS: Received from server: " << buffer << endl;


  }
*/

  close(clientSocket);
/************************* ==WHOIS== ********************************************/

  clientSocket = socket(AF_INET, SOCK_STREAM, 0);

  serverAddr.sin_family = AF_INET;
  serverAddr.sin_port = htons(TCP_PORT);  //whois listen on port 43
  serverAddr.sin_addr.s_addr = inet_addr(whois_ip);
  memset(serverAddr.sin_zero, '\0', sizeof(serverAddr.sin_zero));

  addr_size = sizeof(serverAddr);

  char whois_query[64];

  strcpy(whois_query, ip);
  strcat(whois_query, "\r\n");


  nBytes = strlen(whois_query) + 1;

  if (connect(clientSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) != 0){
    cerr << "WHOIS: connect failed " << endl;
    exit(-1);
  }

  cout << "WHOIS: connected" << endl;


  if(send(clientSocket, whois_query, nBytes, 0) == -1){
    cerr << "WHOIS: Socket sending failed. " << endl;
    exit(-1);
  }

  cout << "=== WHOIS ===" << endl;
  n = 0;
  while(n = read(clientSocket, buffer, sizeof(buffer) - 1) > 0){
    cout << "Received from server: " << buffer << endl;

  }

  close(clientSocket);

//  dns_output();
//  whois_output();

  return 0;
}
