#!/bin/bash

iptables -A INPUT -p udp --dport 3478 -j ACCEPT
iptables -A INPUT -p tcp --dport 5349 -j ACCEPT
iptables -A INPUT -p udp --dport 45100:50000 -j ACCEPT
iptables -A OUTPUT -p udp --sport 3478 -j ACCEPT
iptables -A OUTPUT -p tcp --sport 5349 -j ACCEPT
iptables -A OUTPUT -p udp --sport 45100:50000 -j ACCEPT