import sys
import os
import json
import argparse
from keras.utils import np_utils
from keras.layers import BatchNormalization
import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from sklearn.metrics import classification_report
from keras import backend as K

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

def training_model(args):
    (x_train_image,y_train_label),(x_test_image,y_test_label) = mnist.load_data() #手寫數字的訓練資料

    #reshape 28*28 array to 28*28*1
    x_Train = x_train_image.reshape(60000,28,28,1).astype('float32') #把array轉成28*28*1
    x_Test = x_test_image.reshape(10000,28,28,1).astype('float32') #把array轉成28*28*1

    #data normalization
    x_Train_normalize = x_Train/255 
    x_Test_normalize = x_Test/255

    #Label to one hot style
    y_Train_OneHot = np_utils.to_categorical(y_train_label)
    y_Test_OneHot = np_utils.to_categorical(y_test_label)

    default_filter1=args.filter1
    default_filter2=args.filter2
    default_kernel_size1=args.kernel_size1 
    default_kernel_size2=args.kernel_size2
    default_epoch=args.epoch
    default_batch=args.batch 


    #create a Sequential model
    model = Sequential()
    model.add(Conv2D(filters=default_filter1, kernel_size=(default_kernel_size1,default_kernel_size1),padding='same', input_shape=(28,28,1),activation='relu'))#convolution layer
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Conv2D(filters=default_filter2, kernel_size=(default_kernel_size2,default_kernel_size2),padding='same',activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Flatten())
    #drop權值，加快訓練速度，避免overfitting
    #odel.add(Dropout(0.25)) 
    #fully conection layer
    model.add(Dense(128,activation='relu'))
    #BatchNormalization，不同的方式來提升準確率
    #model.add(BatchNormalization())
    #drop權值，加快訓練速度，避免overfitting
    #odel.add(Dropout(0.5))
    #fully conection layer
    model.add(Dense(10, activation='softmax')) #最後一層的輸出，10指的是輸出的神經元

    #印出模型
    #print(model.summary())
    #loss:指定loss function, optimizer:指定權值(weight/bias)優化的方式, metrics:增加單純顯示用的衡量指標
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy',f1_m,precision_m, recall_m])

    #training model
    model.fit(x=x_Train_normalize,y=y_Train_OneHot, validation_split=0, epochs=default_epoch, batch_size=default_batch, verbose=0)
    #x:訓練圖, y:label, validation_split:0.2 表20%的資料拿來驗證, epochs:要訓練多少回合, batch_size:一次放多少照片來訓練, verbose=2，表示要把結果顯示出來

    scores = model.evaluate(x_Test_normalize, y_Test_OneHot) #評估精準度，越高越好
    print('accuracy=',scores)

    model.save("out/test.h5".format(default_filter1,default_filter2,default_kernel_size1,default_kernel_size2,default_epoch,default_batch))

    loss, accuracy, f1_score, precision, recall = model.evaluate(x_Test_normalize, y_Test_OneHot, verbose=0)

    output = {
            'f1_score':f1_score,
            'precision':precision,
            'recall':recall
            }

    print("score:",output)
    f=open("out/result.txt","w")
    f.write(json.dumps(output))
    f.close()

def ParameterValidator(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-filter1', required=True, help="1st layer filter. (ex: 16)")
    parser.add_argument('-filter2', required=True, help="2nd layer filter. (ex: 16)")
    parser.add_argument('-kernel_size1', required=True, help="1st layer kernel size. (ex: 3)")
    parser.add_argument('-kernel_size2', required=True, help="2nd layer kernel size. (ex: 3)")
    parser.add_argument('-epoch', required=True, help="Epoch value. (ex: 1)")
    parser.add_argument('-batch', required=True, help="Batch value. (ex: 200)")
    args = parser.parse_args(arguments)
    print(args)
    return args

def main(arguments):
    ValidatedArgs=ParameterValidator(arguments)
    training_model(ValidatedArgs)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

