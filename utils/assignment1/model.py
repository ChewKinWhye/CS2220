from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense


def feed_forward_tis():
    model = Sequential()
    model.add(Dense(128, input_dim=201, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()
    return model
