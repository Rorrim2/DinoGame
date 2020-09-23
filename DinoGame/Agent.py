import random
from collections import defaultdict
import json

class Agent:
    def __init__(self, alpha, epsilon, discount, get_legal_actions):
        self.get_legal_actions = get_legal_actions
        self._qvalues = defaultdict(lambda: defaultdict(lambda: 0))
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount = discount

    def get_qvalues(self):
        return self._qvalues

    def get_qvalue(self, state, action):
        return self._qvalues[state][action]

    def set_qvalue(self, state, action, value):
        self._qvalues[state][action] = value

    def get_value(self, state):
        possible_actions = self.get_legal_actions
        # If there are no legal actions, return 0.0
        if len(possible_actions) == 0:
            return 0.0
        max_value = self.get_qvalue(state, self.get_best_action(state))
        return max_value

    def update(self, state, action, reward, next_state, running):
        # agent parameters
        gamma = self.discount
        learning_rate = self.alpha
        next_state_q_value = 0
        if running:
            next_state_q_value = self.get_value(next_state)

        self.set_qvalue(state, action,
                        self.get_qvalue(state, action) +
                        learning_rate * (reward + gamma * next_state_q_value - self.get_qvalue(state, action)))

    def get_best_action(self, state):
        possible_actions = self.get_legal_actions
        v = 0.0
        i = 0
        best_action = []
        for a in possible_actions:
            if i == 0:
                v = self.get_qvalue(state, a)
                i = 1
                best_action.append(a)
            else:
                if self.get_qvalue(state, a) > v:
                    v = self.get_qvalue(state, a)
                    best_action.clear()
                    best_action.append(a)
                elif self.get_qvalue(state, a) == v:
                    best_action.append(a)
        if len(best_action) > 1:
            random.shuffle(best_action)
        return best_action[0]

    def get_action(self, state):
        possible_actions = self.get_legal_actions
        # If there are no legal actions, return None
        if len(possible_actions) == 0:
            return None
        epsilon = self.epsilon
        chosen_action = 0
        rand = random.uniform(0.0, 1.0)
        if rand >= epsilon:
            chosen_action = self.get_best_action(state)
        else:
            chosen_action = random.choice(possible_actions)

        return chosen_action

    def turn_off_learning(self):
        self.epsilon = 0
        self.alpha = 0

    def load_qValues_from_json(self, filename):
        with open("Data" + "/" + filename + '.json') as json_file:
            data = json.load(json_file)
            self._qvalues = defaultdict(lambda: defaultdict(lambda: 0))

            for key, value in data.items():
                convertedInner = defaultdict(lambda: 0)
                for inKey, inVal in value.items():
                    convertedInner[eval(inKey)] = inVal

                self._qvalues[eval(key)] = convertedInner

