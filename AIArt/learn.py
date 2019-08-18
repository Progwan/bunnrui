print("[log] start")
import time,sys
starttime = time.time()
import keras
from keras.models import Sequential as seq
from keras.layers.convolutional import Conv2D as CV2
from keras.layers.pooling import MaxPool2D as mp2
from keras.layers import  Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
print("[log] keras import. time=",time.time() - starttime)
import numpy as np
starttime=time.time()
root_dir = "./image/"
categories = sys.argv[1:]
nb_classes = len(categories)
image_size = 50

def main():
    print("[log] call main")
    X_train,X_test,y_train,y_test = np.load("./image/dogandcat.npy")
    X_train = X_train.astype('float') / 256
    X_test = X_test.astype('float') / 256
    y_train = np_utils.to_categorical(y_train,nb_classes)
    y_test = np_utils.to_categorical(y_test,nb_classes)
    log_filepath="./logs/"
    tb_cb = keras.callbacks.TensorBoard(log_dir=log_filepath, histogram_freq=1, write_graph=True, write_images=True)
    model = model_train(X_train,y_train)
    model_eval(model,X_test,y_test)

def build_model(in_shape):
    print("[log] call build_model")
    model = seq()
    model.add(CV2(32, 4, input_shape=in_shape))
    model.add(Activation('relu'))
    model.add(mp2(pool_size=(2,2)))
    model.add(Dropout(0.25))
    model.add(CV2(64,3))
    model.add(Activation('relu'))
    model.add(CV2(64,3))
    model.add(mp2(pool_size=(2,2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    # sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    print("[log] model compile")
    model.compile(loss="binary_crossentropy",
            optimizer='rmsprop',
            metrics=['accuracy'])
    return model

def model_train(X,y):
    print("[log] call moel_train time=",time.time() - starttime)
    model = build_model(X.shape[1:])
    print("[log] model fit")
    model.fit(X,y,batch_size=32,epochs=10)
    hdf5_file = "./image/dogandcatmodel.hdf5"
    print("[log] model save")
    model.save_weights(hdf5_file)
    return model

def model_eval(model,X,y):
    print("[log] call model_eval")
    score = model.evaluate(X,y)
    print("[result] loss = ",score[0])
    print("[result] accuracy = ",score[1])

if __name__ == "__main__":
    main()
