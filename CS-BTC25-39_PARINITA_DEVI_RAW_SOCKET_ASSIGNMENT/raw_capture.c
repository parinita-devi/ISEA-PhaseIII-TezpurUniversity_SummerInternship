
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>

#define ROLL_NO "CS-BTC25-39"
#define PACKET_LIMIT 20
#define BUFFER_SIZE 65536

void process_packet(unsigned char* buffer, int size, int packet_num) {
    struct iphdr *iph = (struct iphdr*)buffer;
    unsigned short iphlen = iph->ihl * 4;

    struct sockaddr_in src, dst;
    memset(&src, 0, sizeof(src));
    src.sin_addr.s_addr = iph->saddr;
    memset(&dst, 0, sizeof(dst));
    dst.sin_addr.s_addr = iph->daddr;

    printf("ROLL NO=%s\n", ROLL_NO);
    printf("ASSIGNED PROTOCOL=TCP\n");
    printf("PACKET NO=%d\n", packet_num);
    printf("SRC IP=%s\n", inet_ntoa(src.sin_addr));
    printf("DST IP=%s\n", inet_ntoa(dst.sin_addr));
    printf("PROTOCOL=TCP\n");
    printf("PROTOCOL NO=%d\n", iph->protocol);
    printf("TTL=%d\n", iph->ttl);
    printf("PACKET SIZE=%d\n", size);

    printf("IP VERSION=%d\n", iph->version);

    if (iph->protocol == IPPROTO_TCP) {
        struct tcphdr *tcph = (struct tcphdr *)(buffer + iphlen);
        printf("SRC PORT=%d\n", ntohs(tcph->source));
        printf("DST PORT=%d\n", ntohs(tcph->dest));
        printf("TCP FLAGS: SYN=%d ACK=%d FIN=%d RST=%d PSH=%d URG=%d\n",
               tcph->syn, tcph->ack, tcph->fin, tcph->rst, tcph->psh, tcph->urg);
    }
    printf("----------------------------------------\n");
}

int main(){
    int sock_raw;
    int data_size;
    unsigned char buffer[BUFFER_SIZE];

    sock_raw = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
    if (sock_raw < 0) {
        perror("Socket Error (Did you run with sudo?)");
        return 1;
    }

    printf("Starting raw socket capture for TCP packets...\n\n");

    int packet_count = 0;
    while (packet_count < PACKET_LIMIT) {
        data_size = recvfrom(sock_raw, buffer, BUFFER_SIZE, 0, NULL, NULL);
        if (data_size < 0) {
            perror("Recvfrom error");
            return 1;
        }

        struct iphdr *iph = (struct iphdr*)buffer;
        if (iph->protocol == IPPROTO_TCP) {
            packet_count++;
            process_packet(buffer, data_size, packet_count);
        }
    }
    close(sock_raw);
    printf("Captured 20 TCP packets successfully.\n");
    return 0;
}





