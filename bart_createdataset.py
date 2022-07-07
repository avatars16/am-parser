from unittest import case

def data_set_from_corpus():
    int = 0
    current_file = 0
    dev_set = True

    new_devset   = open("little_prince_dev.txt", "w") #0
    new_testset  = open("little_prince_test.txt", "w") #1
    new_trainset = open("little_prince_training.txt", "w") #2
    with open("little_prince_corpus.txt") as corpus:
        for line in corpus:
            if (line != '\n'):
                if (int % 5 == 0):
                    if (dev_set):
                        new_devset.write(line)
                        current_file = 0
                    else:
                        new_testset.write(line)
                        current_file = 1
                else:
                    new_trainset.write(line)
                    current_file = 2
            else:
                if (current_file == 0): 
                    new_devset.write("\n")
                    dev_set = False
                if (current_file == 1): 
                    new_testset.write("\n")
                    dev_set = True
                if (current_file == 2): 
                    new_trainset.write("\n")
                int += 1

data_set_from_corpus()