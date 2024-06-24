import sys
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.node import Controller
def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1', position='10,30,0')
    ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mode='g', channel='6', position='50,30,0')
    ap3 = net.addAccessPoint('ap3', ssid='ssid-ap3', mode='g', channel='11', position='90,30,0')
    sta1 = net.addStation('sta1', ip='10.0.0.1', position='15,30,0')
    sta2 = net.addStation('sta2', ip='10.0.0.2', position='20,40,0')
    sta3 = net.addStation('sta3', ip='10.0.0.3', position='25,50,0')
    sta4 = net.addStation('sta4', ip='10.0.0.4', position='30,60,0')
    sta5 = net.addStation('sta5', ip='10.0.0.5', position='35,70,0')
    sta6 = net.addStation('sta6', ip='10.0.0.6', position='40,80,0')

    c0 = net.addController('c0')

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(ap1, ap2)
    net.addLink(ap2, ap3)

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
