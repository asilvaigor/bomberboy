import keras
import numpy as np
import random

from source.core.ai.Memory import Memory
from source.core.utils import Constants


class Brain:
    """
    Class which holds the neural network and performs the Q-Learning algorithm.
    """

    def __init__(self):
        """
        Default constructor. It generates the neural network.
        Based on <https://becominghuman.ai/lets-build-an-atari-ai-part-1-dqn-
        df57e8ff3b26>
        """

        self.__memory = Memory(Constants.MEMORY_SIZE)
        self.__count = 0

        # Input
        shape1 = (Constants.NUM_ROWS, Constants.NUM_COLUMNS)
        tilemap_input = keras.layers.Input(shape1, name='tilemap')
        tilemap_normalized = keras.layers.Lambda(
            lambda x: 1.0 * x / Constants.NUM_UNITS)(tilemap_input)

        # Hidden layers
        conv = keras.layers.Conv1D(4, 4, activation='relu')(tilemap_normalized)
        conv_flattened = keras.layers.Flatten()(conv)
        hidden = keras.layers.Dense(64, activation='relu')(conv_flattened)

        # Output
        output = keras.layers.Dense(Constants.NUM_ACTIONS)(hidden)

        # Applying mask
        shape2 = (Constants.NUM_ACTIONS,)
        actions_input = keras.layers.Input(shape2, name='mask')
        filtered = keras.layers.Multiply()([output, actions_input])

        # Model
        self.__model = keras.Model(inputs=[tilemap_input, actions_input],
                                   outputs=filtered)
        optimizer = keras.optimizers.RMSprop(lr=Constants.LEARNING_RATE,
                                             rho=0.95, epsilon=0.01)
        self.__model.compile(optimizer, loss='mse')

    def think(self, tilemap, reward, died):
        """
        Based on the current tilemap and the rewards it received on the previous
        step, it returns an action to be executed in the form of a number. It
        also performs one step on the Q-Learning algorithm.
        :param tilemap: Numpy array with the map information.
        :param reward: Reward the cpu got on the last iteration.
        :param died: Bool to inform if the agent just died.
        :return: Number that will be converted to an action to be executed.
        """

        # Reshaping tilemap for Keras API
        tilemap = np.reshape(tilemap, (1, tilemap.shape[0], tilemap.shape[1]))

        # Decides if it should take a random step or a predicted one, to avoid
        # model fitting in local maximums
        self.__count += died
        if random.random() < max(Constants.RANDOM_ACTION_PROBABILITY,
                                 1 - 0.001 * self.__count):
            action = random.randint(0, Constants.NUM_ACTIONS - 1)
        else:
            action = np.argmax(
                self.__model.predict([tilemap,
                                      np.ones((1, Constants.NUM_ACTIONS))]))

        # Putting state in memory
        action_vec = np.zeros(Constants.NUM_ACTIONS, dtype=bool)
        action_vec[action] = True
        self.__memory.append(tilemap[0], action_vec, reward, died)

        # Performing one step of Q-Learning
        self.__learn()

        return action

    def __learn(self):
        """
        Performs one step of the Q-Learning algorithm, in which it gets a random
        batch from the memory, calculates the Q value and fits the neural
        network.
        """

        # Getting random batch
        element = self.__memory.get_batch(Constants.BATCH_SIZE)
        if element is None:
            return
        previous_states = element[0]
        states = element[1]
        actions = element[2]
        rewards = element[3]
        died = element[4]

        # Calculating Q
        next_qs = self.__model.predict([states, np.ones(actions.shape)])
        next_qs[died] = 0
        qs = rewards + Constants.GAMMA * np.max(next_qs, axis=1)

        # Fitting model
        self.__model.fit(
            [previous_states, actions], actions * qs[:, None],
            nb_epoch=1, batch_size=len(previous_states), verbose=0)
