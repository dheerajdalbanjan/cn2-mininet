import os
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

def setup_network():
    "Create a network."
    net = Mininet(controller=Controller, link=TCLink)

    info("* Adding controller\n")
    net.addController('c0')

    info("* Adding hosts\n")
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')

    info("* Adding switch\n")
    s1 = net.addSwitch('s1')

    info("* Creating links\n")
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    info("* Starting network\n")
    net.start()

    info("* Configuring web server on h1\n")
    h1.cmd('mkdir -p /tmp/www')
    os.system('cp index.html /tmp/www')
    h1.cmd('cd /tmp/www && python3 -m http.server 80 &')

    info("* Running CLI\n")
    CLI(net)

    info("* Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    setup_network()
