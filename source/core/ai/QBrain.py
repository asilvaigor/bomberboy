import keras
import numpy as np
import os
import random

from source.core.ai.Memory import Memory
from source.core.utils import Constants


class QBrain:
    """
    Class which holds the neural network and performs the Q-Learning algorithm.
    """

    def __init__(self, id, training, load):
        """
        Default constructor. It generates the neural network.
        Based on <https://becominghuman.ai/lets-build-an-atari-ai-part-1-dqn-
        df57e8ff3b26>
        :param id: Character's id.
        :param training: Optional bool to indicate that the ai must train.
        :param load: Optional bool to load a neural network instead of
        creating a new one.
        """

        self.__memory = Memory(Constants.MEMORY_SIZE)
        self.__random_counter = 0
        self.__save_counter = 0
        self.__id = id
        self.__training = training

        if not load:
            # Input
            n_units = Constants.NUM_UNITS
            shape1 = (Constants.NUM_ROWS, Constants.NUM_COLUMNS)
            tilemap_input = keras.layers.Input(shape1, name='tilemap')
            tilemap_normalized = keras.layers.Lambda(
                lambda x: 1.0 * x / n_units)(tilemap_input)

            # Hidden layers
            conv = keras.layers.Conv1D(4, 4, activation='relu')(
                tilemap_normalized)
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
            self.__model.compile(optimizer, loss=self.__huber_loss)
        else:
            path = (os.path.dirname(os.path.realpath(__file__)) +
                    '/../../../assets/save/ai_model' + str(self.__id))
            self.__model = keras.models.load_model(path, custom_objects={
                '__huber_loss': self.__huber_loss})
        self.__target_model = self.__copy_model()

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

        if self.__training:
            # Decides if it should take a random step or a predicted one, to
            # avoid model fitting in local maximums
            self.__random_counter += 1
            self.__save_counter += 1
            if random.random() < max(Constants.RANDOM_ACTION_PROBABILITY,
                                     1 - self.__random_counter *
                                     Constants.RANDOM_SLOPE):
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
        else:
            action = np.argmax(
                self.__model.predict([tilemap,
                                      np.ones((1, Constants.NUM_ACTIONS))]))

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
        next_qs = self.__target_model.predict([states, np.ones(actions.shape)])
        next_qs[died] = 0
        qs = rewards + Constants.GAMMA * np.max(next_qs, axis=1)

        # Fitting model
        self.__model.fit(
            [previous_states, actions], actions * qs[:, None],
            nb_epoch=1, batch_size=len(previous_states), verbose=0)

        # Updating target model
        if self.__save_counter == Constants.MODEL_UPDATE_COUNTER:
            self.__target_model = self.__copy_model()
            self.__save_counter = 0

    def __copy_model(self):
        """
        Saves a copy of the current model and returns it. This should be used
        for saving the model and for updating the Q function being fitted.
        :return: Copied model.
        """

        path = (os.path.dirname(os.path.realpath(__file__)) +
                '/../../../assets/save/ai_model' + str(self.__id))
        self.__model.save(path)
        print('Just saved model', self.__id, '!')
        return keras.models.load_model(path, custom_objects={
            '__huber_loss': self.__huber_loss})

    @staticmethod
    def __huber_loss(a, b, in_keras=True):
        """
        Defines a huber loss function, which is proved to be better than mse.
        :param a: First element array.
        :param b: Second element array.
        :param in_keras: Bool if in keras.
        :return: Error.
        """

        error = a - b
        quadratic_term = error * error / 2
        linear_term = abs(error) - 1 / 2
        use_linear_term = (abs(error) > 1.0)
        if in_keras:
            use_linear_term = keras.backend.cast(use_linear_term, 'float32')
        return use_linear_term * linear_term + (
                1 - use_linear_term) * quadratic_term
