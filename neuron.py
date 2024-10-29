import random

class Neuron(object):

    def __init__(
        self
    ):
        self.and_neuron = random.randint(0, 1)
        
        self.input_value = [0] * 2
        self.input_source_ID = [0] * 2
        self.input_error_flag = [0] * 2
        self.connect_to_network_input = [1] * 2
        
        self.output_value = 0
        self.output_target_ID = 0
        self.output_target_port_ID = 0
        self.output_error_flag = 0