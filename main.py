import gzip
import os
import pickle

from networks import Networks

if __name__ == "__main__":
    
    networks_number = 100
    train_data_length = 100
    
    data_file = gzip.open(os.path.join(os.curdir, "data", "mnist.pkl.gz"), "rb")
    train_data, val_data, test_data = pickle.load(data_file, encoding="latin1")
    data_file.close()
    
    networks = Networks(networks_number)
    networks.train_and_test(train_data, val_data, test_data, train_data_length)