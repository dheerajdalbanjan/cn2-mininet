import sys
from mininet.node import Controller, OVSKernelSwitch
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference

def topology():
    "Create a network."
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', position='10,30,0')
    ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', position='50,30,0')
    sta1 = net.addStation('sta1', ip='10.0.0.1/24', position='15,30,0')
    sta2 = net.addStation('sta2', ip='10.0.0.2/24', position='20,30,0')
    sta3 = net.addStation('sta3', ip='10.0.0.3/24', position='25,30,0')
    c1 = net.addController('c1')

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating and creating links\n")
    net.addLink(ap1, ap2)
    net.addLink(sta1,ap1)
    net.addLink(sta2,ap2)
    net.addLink(sta3,ap1)
    

    net.plotGraph(max_x=100, max_y=100)

    net.startMobility(time=0)
    net.mobility(sta1, 'start', time=1, position='10,30,0')
    net.mobility(sta2, 'start', time=2, position='10,30,0')
    net.mobility(sta3, 'start', time=3, position='10,30,0')
    net.mobility(sta1, 'stop', time=10, position='50,30,0')
    net.mobility(sta2, 'stop', time=11, position='55,30,0')
    net.mobility(sta3, 'stop', time=12, position='60,30,0')
    net.stopMobility(time=13)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])

    # Start packet capture on wireless interfaces
    info("*** Starting packet capture\n")
    ap1.cmd('tcpdump -i ap1-wlan1 -w /tmp/ap1-wlan1.pcap &')
    ap2.cmd('tcpdump -i ap2-wlan1 -w /tmp/ap2-wlan1.pcap &')

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()

