import sys
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class CustomTopo(Topo):
    def build(self):
        # Add switches
        s1 = self.addSwitch('s1', stp=True)
        s2 = self.addSwitch('s2', stp=True)
        s3 = self.addSwitch('s3', stp=True)

        # Add hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        h4 = self.addHost('h4', ip='10.0.0.4/24')
        h5 = self.addHost('h5', ip='10.0.0.5/24')
        h6 = self.addHost('h6', ip='10.0.0.6/24')

        # Add links between hosts and switches
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)
        self.addLink(h5, s3)
        self.addLink(h6, s3)

        # Add redundant links between switches
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s1)

def run():
    # Set up the topology and network
    topo = CustomTopo()
    net = Mininet(topo=topo, switch=OVSSwitch, controller=Controller)
    net.start()
    
    # Add a simple OpenFlow rule to each switch to forward packets
    for switch in net.switches:
        switch.cmd('ovs-ofctl add-flow {} "priority=1,actions=flood"'.format(switch.name))
    # Test connectivity
    info("Testing network connectivity\n")
    net.pingAll()

    # Start CLI
    CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
