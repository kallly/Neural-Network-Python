from Perceptron import Perceptron
from Network import Network

network = Network("network/tf_network_desc_template.txt","network/tf_network_struct_template.txt","RANDOM", 40)
network.inputDataCsv("data/tf.csv")
network.train(1000)
network.testNetworkCsv("data/tf.csv")