#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mn_wifi.link import wmediumd

def topology():
    net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='ssid1', mode='g', channel='1', position='50,50,0', range=50)
    server = net.addHost('server', ip='10.0.0.1')
    sta1 = net.addStation('sta1', ip='10.0.0.2', position='10,20,0')
    sta2 = net.addStation('sta2', ip='10.0.0.3', position='20,20,0')
    sta3 = net.addStation('sta3', ip='10.0.0.4', position='30,20,0')
    sta4 = net.addStation('sta4', ip='10.0.0.5', position='40,20,0')
    sta5 = net.addStation('sta5', ip='10.0.0.6', position='50,20,0')
    sta6 = net.addStation('sta6', ip='10.0.0.7', position='60,20,0')
    c0 = net.addController('c0')

    info("*** Configuring WiFi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(ap1, server)
    net.addLink(ap1, sta1)
    net.addLink(ap1, sta2)
    net.addLink(ap1, sta3)
    net.addLink(ap1, sta4)
    net.addLink(ap1, sta5)
    net.addLink(ap1, sta6)
    
    net.plotGraph(max_x=100, max_y=100)
    
    info("*** Setting Mobility Model\n")
    net.startMobility(time=0)
    net.mobility(sta1, 'start', time=1, position='10,20,0')
    net.mobility(sta1, 'stop', time=20, position='70,20,0')
    net.mobility(sta2, 'start', time=1, position='20,20,0')
    net.mobility(sta2, 'stop', time=20, position='80,20,0')
    net.mobility(sta3, 'start', time=1, position='30,20,0')
    net.mobility(sta3, 'stop', time=20, position='90,20,0')
    net.mobility(sta4, 'start', time=1, position='40,20,0')
    net.mobility(sta4, 'stop', time=20, position='100,20,0')
    net.mobility(sta5, 'start', time=1, position='50,20,0')
    net.mobility(sta5, 'stop', time=20, position='110,20,0')
    net.mobility(sta6, 'start', time=1, position='60,20,0')
    net.mobility(sta6, 'stop', time=20, position='120,20,0')
    net.stopMobility(time=30)

    info("*** Setting up web server\n")
    server.cmd('python3 -m http.server 80 &')
    
    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])


    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    server.cmd('kill %python3')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()

