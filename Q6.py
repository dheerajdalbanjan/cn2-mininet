#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mn_wifi.link import wmediumd, mesh

def topology():
    net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='ssid1', mode='g', channel='1', position='10,30,0', range=30)
    ap2 = net.addAccessPoint('ap2', ssid='ssid2', mode='g', channel='6', position='50,30,0', range=50)
    ap3 = net.addAccessPoint('ap3', ssid='ssid3', mode='g', channel='11', position='90,30,0', range=30)
    sta1 = net.addStation('sta1', position='10,20,0')
    sta2 = net.addStation('sta2', position='20,20,0')
    sta3 = net.addStation('sta3', position='30,20,0')
    sta4 = net.addStation('sta4', position='40,20,0')
    sta5 = net.addStation('sta5', position='50,20,0')
    sta6 = net.addStation('sta6', position='60,20,0')
    c0 = net.addController('c0')

    info("*** Configuring WiFi nodes\n")
    net.configureWifiNodes()

    info("*** Associating stations with access points\n")
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)
    net.addLink(sta3, ap2)
    net.addLink(sta4, ap2)
    net.addLink(sta5, ap3)
    net.addLink(sta6, ap3)
    
    net.plotGraph(max_x=100, max_y=100)

    info("*** Setting Mobility\n")
    net.startMobility(time=0)
    net.mobility(sta1, 'start', time=1, position='10,20,0')
    net.mobility(sta1, 'stop', time=20, position='50,30,0')
    net.mobility(sta2, 'start', time=1, position='20,20,0')
    net.mobility(sta2, 'stop', time=20, position='90,30,0')
    net.stopMobility(time=30)


    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])
    ap3.start([c0])
    
    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()

