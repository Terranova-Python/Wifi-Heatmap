def scan_ip(ip_address):

    def scan(ip):
        arp_packet = scapy.ARP(pdst=ip)
        broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_broadcast_packet = broadcast_packet/arp_packet
        answered_list = scapy.srp(arp_broadcast_packet, timeout=1, verbose=False)[0]
        client_list = []

        for element in answered_list:
            client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
            client_list.append(client_dict)
        
        return client_list

    def print_result(scan_list):
        result_head = "IP\t\tMAC\n---------------------------------"
        T2.insert('end', result_head + '\n')

        if scan_list:
            unifi_mac_list = ['00:15:6D','00:1B:67','00:1B:67','00:27:22','00:15:6D','00:1B:67',    # Ignore this - this is for Unifi Mac ID's
                            '00:27:22','04:18:D6','24:A4:3C','68:72:51','6C:5E:7A','9C:B0:08',
                            'DC:9F:DB','04:4e:5a']

            for client in scan_list:
                scan_results = client["ip"] + "\t\t" + client["mac"]
                T2.insert('end', scan_results + '\n')

                for mac_id in unifi_mac_list:
                    if mac_id in client['mac']:                           # Check condition - If Mac contains x, highlight the line that that Mac is on...
                        c_l = scan_list.index(client) + 3                 # Maybe add in a descriptor? Ex: 10.0.0.1 -- MAC -- (unifi) etc.
                        start_cl, end_cl = str(c_l) + ".0" , str(c_l) + ".40"
                        T2.tag_add('start', start_cl, end_cl)
                        T2.tag_configure('start', foreground='#40c773')
                    else:
                        pass

        else:
          pass

    result_list = scan(ip_entry.get())
    print_result(result_list)
