
def open_data(data_file)
    file = open(data_file, 'rb')
    tb_dict = pickle.load(file)
    close(file)

    return tb_dict
