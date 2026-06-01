from CNN.utils import *

from tqdm import tqdm
import argparse
import matplotlib.pyplot as plt
import pickle

#parser = argparse.ArgumentParser(description='Predict the network accuracy.')
#parser.add_argument('parameters', metavar = 'parameters', help='name of file parameters were saved in. These parameters will be used to measure the accuracy.')

if __name__ == '__main__':
    #args = parser.parse_args()
    #save_path = args.parameters
    
    params, cost = pickle.load(open("params.pkl", 'rb'))
    [f1, f2, w3, w4, b1, b2, b3, b4] = params
    print("params")
    print([f1, f2, w3, w4, b1, b2, b3, b4])
    print("params over")
    print()
    # Get test data
    m = 500
    X = extract_data('t10k-images-idx3-ubyte.gz', m, 28)
    y_dash = extract_labels('t10k-labels-idx1-ubyte.gz', m).reshape(m,1)
    # Normalize the data
    X-= int(np.mean(X)) # subtract mean
    X/= int(np.std(X)) # divide by standard deviation
    test_data = np.hstack((X,y_dash))
    print("test_data")
    print(test_data)
    print("test data over")
    print()
    X = test_data[:,0:-1]
    print("X")
    print(X)
    print("X over")
    print()
    X = X.reshape(len(test_data), 1, 28, 28)
    print("X eshaped")
    print(X)
    print("X reshaped over")
    print()
    y = test_data[:,-1]
    print("y")
    print(y)
    print("y over")
    print()

    corr = 0
    digit_count = [0 for i in range(10)]
    digit_correct = [0 for i in range(10)]
   
    print()
    print("Computing accuracy over test set:")

    t = tqdm(range(len(X)), leave=True)

    for i in t:
        x = X[i]
        pred, prob = predict(x, f1, f2, w3, w4, b1, b2, b3, b4)
        digit_count[int(y[i])]+=1
        if pred==y[i]:
            corr+=1
            digit_correct[pred]+=1

        #t.set_description("Acc:%0.2f%%" % (float(corr/(i+1))*100))
            
    print("Overall Accuracy: %.2f" % (float(corr/500 *100)))   
    #print("Overall Accuracy: %.2f" % (float(corr/len(test_data)*100)))
    x = np.arange(10)
    digit_recall = [x/y for x,y in zip(digit_correct, digit_count)]
    plt.xlabel('Digits')
    plt.ylabel('Recall')
    plt.title("Recall on Test Set")
    plt.bar(x,digit_recall)
    plt.show()
