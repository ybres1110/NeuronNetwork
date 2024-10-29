import random

from neuron import Neuron

class Networks(object):

    def __init__(
        self,
        networks_number
    ):
        if networks_number < 20:
            exit(0)
        self.networks_number = networks_number
        self.networks = [[[Neuron()]] for _ in range(self.networks_number)]

    def connect(self, network_index, level_index, neuron_index, input_index, specify_value_flag, specify_value):
        if self.networks[network_index][level_index][neuron_index].connect_to_network_input[input_index] == 0:
            exit(0)
        connect_fail_flag = True
        if input_index == 0:
            another_input_index = 1
        else:
            another_input_index = 0
        while connect_fail_flag:
            networks_input_ID = random.randint(0, self.networks_input_number - 1)
            if specify_value_flag:
                if self.networks_input_value[networks_input_ID] == specify_value:
                    if networks_input_ID != self.networks[network_index][level_index][neuron_index].input_source_ID[another_input_index]:
                        self.networks[network_index][level_index][neuron_index].input_source_ID[input_index] = networks_input_ID
                        connect_fail_flag = False

            else:
                if networks_input_ID != self.networks[network_index][level_index][neuron_index].input_source_ID[another_input_index]:
                    self.networks[network_index][level_index][neuron_index].input_source_ID[input_index] = networks_input_ID
                    connect_fail_flag = False
            
    def level_predict(self, network_index, level_index):
        for neuron_index in range(len(self.networks[network_index][level_index])):
            for port_index in range(2):
                if self.networks[network_index][level_index][neuron_index].connect_to_network_input[port_index] == 1:
                    self.networks[network_index][level_index][neuron_index].input_value[port_index] = self.networks_input_value[self.networks[network_index][level_index][neuron_index].input_source_ID[port_index]]
            
            neuron_type = self.networks[network_index][level_index][neuron_index].and_neuron
            if neuron_type == 1:
                if self.networks[network_index][level_index][neuron_index].input_value[0] == 1 and self.networks[network_index][level_index][neuron_index].input_value[1] == 1:
                    self.networks[network_index][level_index][neuron_index].output_value = 1
                else:
                    self.networks[network_index][level_index][neuron_index].output_value = 0
            else:
                if self.networks[network_index][level_index][neuron_index].input_value[0] == 0 and self.networks[network_index][level_index][neuron_index].input_value[1] == 0:
                    self.networks[network_index][level_index][neuron_index].output_value = 0
                else:
                    self.networks[network_index][level_index][neuron_index].output_value = 1
                
            if level_index > 0:
                next_level = level_index - 1
                next_level_neuron = self.networks[network_index][level_index][neuron_index].output_target_ID
                next_level_neuron_port = self.networks[network_index][level_index][neuron_index].output_target_port_ID
                self.networks[network_index][next_level][next_level_neuron].input_value[next_level_neuron_port] = self.networks[network_index][level_index][neuron_index].output_value
    
    def network_predict(self, network_index):
        for level_index in range(len(self.networks[network_index])):
            self.level_predict(network_index, len(self.networks[network_index]) - level_index - 1)
            
    def level_feedback(self, network_index, level_index):
        for neuron_index in range(len(self.networks[network_index][level_index])):
            for input_index in range(2):
                self.networks[network_index][level_index][neuron_index].input_error_flag[input_index] = 0
            
            neuron_type = self.networks[network_index][level_index][neuron_index].and_neuron
            
            if self.networks[network_index][level_index][neuron_index].output_error_flag == 1:
                if neuron_type == 1:
                    if self.networks[network_index][level_index][neuron_index].output_value == 0:
                        for input_index in range(2):
                            if self.networks[network_index][level_index][neuron_index].input_value[input_index] == 0:
                                self.networks[network_index][level_index][neuron_index].input_error_flag[input_index] = 1
                    else:
                        error_input_index = random.randint(0, 1)
                        if self.networks[network_index][level_index][neuron_index].input_value[error_input_index] == 1:
                            self.networks[network_index][level_index][neuron_index].input_error_flag[error_input_index] = 1
                        else:
                            exit(0)  
                else:
                    if self.networks[network_index][level_index][neuron_index].output_value == 0:
                        error_input_index = random.randint(0, 1)
                        if self.networks[network_index][level_index][neuron_index].input_value[error_input_index] == 0:
                            self.networks[network_index][level_index][neuron_index].input_error_flag[error_input_index] = 1
                        else:
                            exit(0) 
                    else:
                        for input_index in range(2):
                            if self.networks[network_index][level_index][neuron_index].input_value[input_index] == 1:
                                self.networks[network_index][level_index][neuron_index].input_error_flag[input_index] = 1

            for input_index in range(2):
                if self.networks[network_index][level_index][neuron_index].connect_to_network_input[input_index] == 0:
                    next_level = level_index + 1
                    next_level_neuron = self.networks[network_index][level_index][neuron_index].input_source_ID[input_index]
                    self.networks[network_index][next_level][next_level_neuron].output_error_flag = self.networks[network_index][level_index][neuron_index].input_error_flag[input_index]
            
    def network_feedback(self, network_index, network_correct_value):
        if self.networks[network_index][0][0].output_value != network_correct_value:
            self.networks[network_index][0][0].output_error_flag = 1
        else:
            self.networks[network_index][0][0].output_error_flag = 0
            
        for level_index in range(len(self.networks[network_index])):
            self.level_feedback(network_index, level_index)
        
    def network_copy(self, copy_form_index, copy_to_index):
        self.networks[copy_to_index].clear()
        for level_index in range(len(self.networks[copy_form_index])):
            self.networks[copy_to_index].append([])
        for level_index in range(len(self.networks[copy_form_index])):
            for neuron_index in range(len(self.networks[copy_form_index][level_index])):
                self.networks[copy_to_index][level_index].append(Neuron())
                
                self.networks[copy_to_index][level_index][neuron_index].and_neuron = self.networks[copy_form_index][level_index][neuron_index].and_neuron
                
                for input_index in range(2):
                    self.networks[copy_to_index][level_index][neuron_index].input_value[input_index] = self.networks[copy_form_index][level_index][neuron_index].input_value[input_index]
                    self.networks[copy_to_index][level_index][neuron_index].input_source_ID[input_index] = self.networks[copy_form_index][level_index][neuron_index].input_source_ID[input_index]
                    self.networks[copy_to_index][level_index][neuron_index].input_error_flag[input_index] = self.networks[copy_form_index][level_index][neuron_index].input_error_flag[input_index]
                    self.networks[copy_to_index][level_index][neuron_index].connect_to_network_input[input_index] = self.networks[copy_form_index][level_index][neuron_index].connect_to_network_input[input_index]
                    
                self.networks[copy_to_index][level_index][neuron_index].output_value = self.networks[copy_form_index][level_index][neuron_index].output_value
                self.networks[copy_to_index][level_index][neuron_index].output_target_ID = self.networks[copy_form_index][level_index][neuron_index].output_target_ID
                self.networks[copy_to_index][level_index][neuron_index].output_target_port_ID = self.networks[copy_form_index][level_index][neuron_index].output_target_port_ID
                self.networks[copy_to_index][level_index][neuron_index].output_error_flag = self.networks[copy_form_index][level_index][neuron_index].output_error_flag
        
    def networks_predict(self, training_data):
        self.train_success_flag = [[0] * len(training_data) for _ in range(self.networks_number - 10)]
        best_index = 0
        best_score = 0
        for training_data_index in range(len(training_data)):
            #update network input
            for networks_input_index in range(self.networks_input_number):
                self.networks_input_value[networks_input_index] = training_data[training_data_index][0][networks_input_index]
                
            for network_index in range(self.networks_number - 10):
                self.network_predict(network_index)
                if self.networks[network_index][0][0].output_value == training_data[training_data_index][1]:
                    self.train_success_flag[network_index][training_data_index] = 1
                else:
                    self.train_success_flag[network_index][training_data_index] = 0

        for network_index in range(self.networks_number - 10):  
            if sum(self.train_success_flag[network_index]) > best_score:
                best_score = sum(self.train_success_flag[network_index])
                best_index = network_index
                
        return best_index, best_score
    
    def get_error_info_from_a_random_error_sample(self, training_data, network_reference_index):
        error_sample_number = self.train_success_flag[network_reference_index].count(0)
        if error_sample_number == 0:
            exit(0)
        elif error_sample_number == 1:
            random_error_sample_index = self.train_success_flag[network_reference_index].index(0)
        else:
            cnt = random.randint(1, error_sample_number)
            cnt_temp = 0
            for index in range(len(self.train_success_flag[network_reference_index])):
                if self.train_success_flag[network_reference_index][index] == 0:
                    cnt_temp += 1
                if cnt == cnt_temp:
                    random_error_sample_index = index
                    break
        #update network input
        for networks_input_index in range(self.networks_input_number):
            self.networks_input_value[networks_input_index] = training_data[random_error_sample_index][0][networks_input_index]
            
        self.network_predict(network_reference_index)
        self.network_feedback(network_reference_index, training_data[random_error_sample_index][1])
        error_level = []
        error_neuron = []
        error_input = []
        
        for level_index in range(len(self.networks[network_reference_index])):
            for neuron_index in range(len(self.networks[network_reference_index][level_index])):
                for input_index in range(2):
                    if self.networks[network_reference_index][level_index][neuron_index].connect_to_network_input[input_index] == 1 and self.networks[network_reference_index][level_index][neuron_index].input_error_flag[input_index] > 0:
                        error_level.append(level_index)
                        error_neuron.append(neuron_index)
                        error_input.append(input_index) 
                        
        return error_level, error_neuron, error_input
    
    def change_connection(self, training_data, network_reference_index, network_available_start_index):
        error_level, error_neuron, error_input = self.get_error_info_from_a_random_error_sample(training_data, network_reference_index)

        network_index = network_available_start_index
        
        if len(error_level) > 0:
            for level_index in range(len(self.networks[network_reference_index])):
                print(len(self.networks[network_reference_index][level_index]))
            while network_index < self.networks_number - 10:
                self.network_copy(network_reference_index, network_index)
                for error_neuron_index in range(len(error_neuron)):
                    error_level_id = error_level[error_neuron_index]
                    error_neuron_id = error_neuron[error_neuron_index]
                    error_neuron_input_index = error_input[error_neuron_index]
                    input_value = self.networks[network_reference_index][error_level_id][error_neuron_id].input_value[error_neuron_input_index]
                    if input_value == 1:
                        self.connect(network_index, error_level_id, error_neuron_id, error_neuron_input_index, 1, 0)
                    else:
                        self.connect(network_index, error_level_id, error_neuron_id, error_neuron_input_index, 1, 1)
                network_index += 1         
        
    def neuron_split(self, network_index, level_index, neuron_index, input_index):
        if self.networks[network_index][level_index][neuron_index].connect_to_network_input[input_index] == 0:
            exit(0)
        next_level = level_index + 1
        
        if len(self.networks[network_index]) <= next_level:
            self.networks[network_index].append([])
            
        self.networks[network_index][next_level].append(Neuron())
        next_level_neuron = len(self.networks[network_index][next_level]) - 1
        
        self.networks[network_index][next_level][next_level_neuron].connect_to_network_input[0] = 1
        self.networks[network_index][next_level][next_level_neuron].connect_to_network_input[1] = 1
        self.networks[network_index][next_level][next_level_neuron].output_target_ID = neuron_index
        self.networks[network_index][next_level][next_level_neuron].output_target_port_ID = input_index
        
        next_level_neuron_type = self.networks[network_index][next_level][next_level_neuron].and_neuron
        error_input_value = self.networks[network_index][level_index][neuron_index].input_value[input_index]
        if error_input_value == 1:
            if next_level_neuron_type == 1:
                self.networks[network_index][next_level][next_level_neuron].input_source_ID[0] = self.networks[network_index][level_index][neuron_index].input_source_ID[input_index]
                self.connect(network_index, next_level, next_level_neuron, 1, 1, 0)
            else:
                self.connect(network_index, next_level, next_level_neuron, 0, 1, 0)
                self.connect(network_index, next_level, next_level_neuron, 1, 1, 0)
        else:
            if next_level_neuron_type == 0:
                self.networks[network_index][next_level][next_level_neuron].input_source_ID[0] = self.networks[network_index][level_index][neuron_index].input_source_ID[input_index]
                self.connect(network_index, next_level, next_level_neuron, 1, 1, 1)
            else:
                self.connect(network_index, next_level, next_level_neuron, 0, 1, 1)
                self.connect(network_index, next_level, next_level_neuron, 1, 1, 1)
        
        self.networks[network_index][level_index][neuron_index].connect_to_network_input[input_index] = 0
        self.networks[network_index][level_index][neuron_index].input_source_ID[input_index] = next_level_neuron
        
    def network_split(self, training_data, network_reference_index, network_available_start_index):
        error_level, error_neuron, error_input = self.get_error_info_from_a_random_error_sample(training_data, network_reference_index)

        network_index = network_available_start_index
        
        if len(error_level) > 0:
            while network_index < self.networks_number - 10:
                self.network_copy(network_reference_index, network_index)
                for error_neuron_index in range(len(error_neuron)):
                    error_level_id = error_level[error_neuron_index]
                    error_neuron_id = error_neuron[error_neuron_index]
                    error_neuron_input_index = error_input[error_neuron_index]
                    if self.networks[network_reference_index][error_level_id][error_neuron_id].connect_to_network_input[error_neuron_input_index] == 1:
                        self.neuron_split(network_index, error_level_id, error_neuron_id, error_neuron_input_index)
                    else:
                        exit(0)
                network_index += 1 
            self.network_copy(network_available_start_index, network_reference_index)
        
    def train(self, training_data):
        self.networks_input_number = len(training_data[0][0])
        self.networks_output_number = 1
        self.networks_input_value = [0] * self.networks_input_number
        
        #Neuron network connection initialization
        for network_index in range(self.networks_number - 10):
            for level_index in range(len(self.networks[network_index])):
                for neuron_index in range(len(self.networks[network_index][level_index])):
                    for input_index in range(2):
                        self.networks[network_index][level_index][neuron_index].input_source_ID[input_index] = self.networks_input_number + 1
                        if self.networks[network_index][level_index][neuron_index].connect_to_network_input[input_index] == 0:
                            print('bug')
                            exit(0)
                        self.networks[network_index][level_index][neuron_index].connect_to_network_input[input_index] = 1
                        
        for network_index in range(self.networks_number - 10):
            for level_index in range(len(self.networks[network_index])):
                for neuron_index in range(len(self.networks[network_index][level_index])):
                    for input_index in range(2):
                        self.connect(network_index, level_index, neuron_index, input_index, 0, 0)
                        
        best_score_backup = 0
        best_score_times = 0
        
        while True:
            best_index, best_score = self.networks_predict(training_data)
            print(best_index, best_score/len(training_data))
            
            if best_index != 0 and best_score > best_score_backup:
                self.network_copy(best_index, 0)
                best_score_backup = best_score
                best_score_times = 0
            else:
                best_score_times += 1
                
            if best_score < len(training_data):
                self.change_connection(training_data, 0, 1)
            else:
                return True
            
            if best_score_times > 50:
                self.network_split(training_data, 0, 1)
                best_score_times = 0
                best_score_backup = 0
                
    def input_binarization(self, x):
        y = [0] *(28*28*2)
        for index in range(len(x)):
            if x[index] < 0.5:
                y[2*index] = 1
                y[2*index+1] = 0
            else:
                y[2*index] = 0
                y[2*index+1] = 1
        return y
    
    def output_binarization(self, x, value):
        if x == value:
            return 1
        else:
            return 0
        
    def test(self, test_data):
        for network_index in range(10):
            self.network_copy(self.networks_number - 10 + network_index, network_index)
            
        test_number = 0
        test_success_number = 0
        for data_index in range(len(test_data)):
            #update network input
            for networks_input_index in range(self.networks_input_number):
                self.networks_input_value[networks_input_index] = test_data[data_index][0][networks_input_index]
            
            test_result = []
            for network_index in range(10):
                self.network_predict(network_index)
                test_result.append(self.networks[network_index][0][0].output_value)
                
            if test_result.count(1) == 1:
                if test_result.index(1) == test_data[data_index][1]:
                    test_success_number += 1
            elif test_result.count(1) > 1:
                cnt = random.randint(1, test_result.count(1))
                cnt_temp = 0
                for index in range(len(test_result)):
                    if test_result[index] == 1:
                        cnt_temp += 1
                    if cnt_temp == cnt:
                        if index == test_data[data_index][1]:
                            test_success_number += 1
                        break
                
            test_number += 1
        
        print('Accuracy:')
        print(test_success_number/test_number)
            
    def train_and_test(self, train_data, val_data, test_data, train_data_length):
        all_inputs = [self.input_binarization(x) for x in train_data[0]] + [self.input_binarization(x) for x in val_data[0]] + [self.input_binarization(x) for x in test_data[0]]
        
        for train_index in range(10):
            all_results = [self.output_binarization(x, train_index) for x in train_data[1]] + [self.output_binarization(x, train_index) for x in val_data[1]] + [self.output_binarization(x, train_index) for x in test_data[1]]
            all_data = list(zip(all_inputs, all_results))
            for network_index in range(self.networks_number - 10):
                self.networks[network_index].clear()
                self.networks[network_index].append([])
                self.networks[network_index][0].append(Neuron())
            self.train(all_data[:train_data_length])
            self.network_copy(0, self.networks_number - 10 + train_index)
            
        all_results = list(train_data[1]) + list(val_data[1]) + list(test_data[1])
        all_data = list(zip(all_inputs, all_results))
        self.test(all_data[train_data_length:])
        

