import pickle

def open_data(data_file):
    file = open(data_file, 'rb')
    tb_dict = pickle.load(file)
    file.close()

    return tb_dict


