#ifndef _SCAN_HEADERS_H_
#define _SCAN_HEADERS_H_

typedef struct tcpHead{
  u_short source_port;
  u_short dest_port;
  u_int seq;
  u_int ack;
  u_char offx2;
  u_char flags;
  u_short window;
  u_short sum;
  u_short urp;
};

// UDP header structure
typedef struct udpHead{
	u_short source_port;
	u_short dest_port;
	u_short length;
	u_short sum;
};

typedef struct ipHead{
  u_char ip_hl:4; // member is 4bits
  u_char ip_v:4;
  u_char ip_tos;
  u_short ip_len;
  u_short ip_id;
  u_short ip_off;
  u_char ip_ttl;
  u_char ip_proto;
  u_int ip_sum;
  struct in_addr source_ip, dest_ip;
};

typedef struct pseudoHead{
  u_int source_address;
  u_int dest_address;
  u_char placeholder;
  u_char protocol;
  u_short length;
};

#endif
