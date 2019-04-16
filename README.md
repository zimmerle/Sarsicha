
## Sarsicha an educational and playful malware c&c platform

Disclaimer: This meant to be an educational platform where different pieces of a c&c will be highlighted. This is not meant to be put in production, on the contrary, this meant to be used
a case of study to help taking down botnets in general.


### About a c&c and botnet

In the beginning, a botnet where high hierarchical infrastructure where a *command control* is placed as a *masterpiece* delivering content to zombie nodes, sometimes even in plain sight - text/plain in IRC networks. No need to mention that those were not difficult to be taken apart, as for identifying the infected machine was about to identify the connection to the IRC network.
It was also easy to take over the nodes as the level of authentication of the owner was - intentionally or not - very basic.

Years passed and the botnets became even more valuable, for different purposes: from mining bitcoin all the way to perform DDoS attacks. Which, of course, led to an enhancement on the techniques on assorted areas: spread malware, hide the infected computers, exchange protocols, and on how to protect the network from being taken over by other attacks.

If you are willing to understand better about botnets, there is an excellent write up here:
[https://blog.mi.hdm-stuttgart.de/index.php/2016/09/05/botnets-structural-analysis-functional-principle-and-general-overview/](Botnets – Structural analysis, functional principle, and general overview) by Michael Kreuzer, which includes the Dridex, used as inspiration in this project.


## This project inspiration and concepts

As we are willing to mimic the behavior of a real c&c we choose the Dridex as the base model for this project with several twists in different areas, in order to innovate or the better illustrate some functionalities. Thanks to Marcos Alvares.

In this protect we split the c&c into different areas: control, network communication, and distribution.

### The command and control

As the command control, we opted to have a UI which concentrates all the functionalities: from the payload generation to sending commands to the proxy nodes. The proxy nodes will be better explained in the upcoming session.

The Image 1 is a screenshot for the command center. 

#### Master node

Master node concentrates information on all proxy nodes; The botnet owner can access only the master node to send commands to all proxy nodes.

#### Proxy node

The proxy node was written in python and it has an API which can be consumed from a UI to a command line utility. Among of the code, there is a command line interface script.

#### Slave node or node

The slave node is the one that runs on the infected machine it keeps pooling the proxy node to get further instructions. Currently, it can communicate with the proxy via HTTP and/DNS queries.

Further, it will be expanded to support:
Steganography, downloading images from public sites as such as: Redis.
Identify and communicate via other nodes on the same local area network.

The code base has a node simulator in python, that can be used to test the currently implemented features.


### What next?

The peers are not yet authenticating themselves. Web Of Trust should be added in order to authenticate which of the peers.


### Examples

#### Running the proxy node
#### The proxy node cli
#### Running the node simulator

