"""Keep the printer in the SSDP multicast group so Anycubic Slicer Next can discover it in LAN mode.

The stock firmware never announces its membership of the SSDP group, so networks with IGMP snooping do not
deliver the slicer's discovery message to the printer. A single report is forgotten by the network after a
few minutes, so this keeps a socket joined to the group (the kernel then answers the router's IGMP queries)
and repeats the report periodically for networks without an IGMP querier.
"""
import socket
import struct
import time

MULTICAST_GROUP = '239.255.255.250'
REPORT_INTERVAL = 60  # seconds; IGMP snooping usually forgets a group after ~260 s without reports


def calculate_checksum(data):
    """Calculates 16-bit one's complement (Internet checksum)"""
    total = 0
    for i in range(0, len(data), 2):
        total += (data[i] << 8) + (data[i + 1] if i + 1 < len(data) else 0)
    while total >> 16:
        total = (total & 0xffff) + (total >> 16)
    return ~total & 0xffff


def send_report():
    """Send an IGMPv2 Membership Report for the SSDP group"""
    group_address = socket.inet_aton(MULTICAST_GROUP)
    checksum = calculate_checksum(struct.pack('!BBH4s', 0x16, 0, 0, group_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IGMP)
    try:
        sock.sendto(struct.pack('!BBH4s', 0x16, 0, checksum, group_address), (MULTICAST_GROUP, 0))
    finally:
        sock.close()


def join_group():
    """Open a socket that stays joined to the SSDP group; closing it would make the kernel leave the group"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mreq = struct.pack('4s4s', socket.inet_aton(MULTICAST_GROUP), socket.inet_aton('0.0.0.0'))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return sock


member = None
while True:
    try:
        if member is None:
            member = join_group()
            print(f"Joined multicast group {MULTICAST_GROUP}", flush=True)
        send_report()
    except OSError as e:  # network not up yet: try again on the next round
        print(f"Retrying after error: {e}", flush=True)
    time.sleep(REPORT_INTERVAL)
