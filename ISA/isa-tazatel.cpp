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

struct dns_header{
  unsigned short id; // identification number

  unsigned char rd :1; // recursion desired
  unsigned char tc :1; // truncated message
  unsigned char aa :1; // authoritive answer
  unsigned char opcode :4; // purpose of message
  unsigned char qr :1; // query/response flag

  unsigned char rcode :4; // response code
  unsigned char cd :1; // checking disabled
  unsigned char ad :1; // authenticated data
  unsigned char z :1; // its z! reserved
  unsigned char ra :1; // recursion available

  unsigned short q_count; // number of question entries
  unsigned short ans_count; // number of answer entries
  unsigned short auth_count; // number of authority entries
  unsigned short add_count; // number of resource entries
};

int hostname_to_ip(char* hostname, char* ip){

  struct hostent *h;
  struct in_addr **addr_list;

  if((h = gethostbyname(hostname)) == NULL){
    cerr << "Get host IP failed." << endl;
    exit(20);
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
  const int PORT = 43;

  bool q_flag = false;
  bool w_flag = false;
  bool d_flag = false;

  string ip_hostname;
  string whois_server;
  //implicitne 1.1.1.1
  string dns_server = "1.1.1.1";

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

/*
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("whois.arin.net", 43))

#convert string to bytes, socket need bytes
s.send((sys.argv[1] + "\r\n").encode())

#declares a bytes
response = b""
while True:
    data = s.recv(4096)
    response += data
    if not data:
        break
s.close()

#convert bytes to string
print(response.decode())

*/

//  char hostname[ip_hostname.size + 1];
//  strcpy(char_)

  char ip[16];
  char hostname[ip_hostname.size() + 1];
  strcpy(hostname, ip_hostname.c_str());
  if(hostname_to_ip(hostname, ip) == 0){
    cout << ip << endl;
  }
  else{
    exit(20);
  }

  char dns_ip[16];
  char dns_hostname[dns_server.size() + 1];
  strcpy(dns_hostname, dns_server.c_str());
  if(hostname_to_ip(dns_hostname, ip) == 0){
    cout << ip << endl;
  }
  else{
    exit(20);
  }

  char whois_ip[16];
  char whois_hostname[whois_server.size() + 1];
  strcpy(whois_hostname, whois_server.c_str());
  if(hostname_to_ip(whois_hostname, ip) == 0){
    cout << ip << endl;
  }
  else{
    exit(20);
  }

  unsigned char buf[65536];
  int s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP); //UDP packet for dns

  struct sockaddr_in a;
  struct sockaddr_in dest;

  dest.sin_family = AF_INET;
  dest.sin_port = htons(53);
  dest.sin_addr.s_addr = inet_addr(dns_ip);

  struct dns_header *dns = (struct dns_header *)&buf;

  dns->id = (unsigned short) htons(getpid());
  dns->qr = 0; //This is a query
  dns->opcode = 0; //This is a standard query
  dns->aa = 0; //Not Authoritative
  dns->tc = 0; //This message is not truncated
  dns->rd = 1; //Recursion Desired
  dns->ra = 0; //Recursion not available! hey we dont have it (lol)
  dns->z = 0;
  dns->ad = 0;
  dns->cd = 0;
  dns->rcode = 0;
  dns->q_count = htons(1); //we have only 1 question
  dns->ans_count = 0;
  dns->auth_count = 0;
  dns->add_count = 0;

/***********************************************************/

// https://gist.github.com/fffaraz/9d9170b57791c28ccda9255b48315168
// http://www.nsc.ru/cgi-bin/www/unix_help/unix-man?gethostbyname+3
// https://www.geeksforgeeks.org/convert-string-char-array-cpp/
// https://wis.fit.vutbr.cz/FIT/st/course-sl.php?id=705161&item=75303&cpa=1

  dns_output();
  whois_output();

  return 0;
}
