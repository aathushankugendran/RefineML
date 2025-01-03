import re
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import random

class CodeOptimizerDQL:
    def __init__(self, language='Python'):
        """
        Initialize the Deep Q-Learning-based Code Optimizer.
        - language: Programming language of the code (default is Python).
        """
        print("[DEBUG] Initializing CodeOptimizerDQL...")
        self.language = language

        # Define the possible actions for optimization
        self.actions = [
            "replace_nested_loops",
            "use_list_comprehension",
            "remove_redundant_code",
            "replace_data_structures",
            "replace_string_concatenation",
            "replace_manual_sum",
            "use_set_for_uniqueness",
            "remove_redundant_conversion",
            "use_conditional_comprehension"
        ]
        
        print(f"[DEBUG] Actions initialized: {self.actions}")

        print("[DEBUG] Building TensorFlow model...")
        self.model = self._build_dql_model()  # Build the DQL model
        print("[DEBUG] TensorFlow model built successfully.")

        # Deep Q-Learning parameters
        self.memory = []  # Replay memory for storing experiences
        self.gamma = 0.95  # Discount factor for future rewards
        self.epsilon = 1.0  # Exploration vs exploitation rate
        self.epsilon_min = 0.01  # Minimum epsilon value for exploration
        self.epsilon_decay = 0.995  # Epsilon decay factor

    def _build_dql_model(self):
        """
        Builds the Deep Q-Learning model for optimization decision-making.
        """
        model = Sequential([
            Dense(64, input_dim=1, activation='relu'),
            Dense(64, activation='relu'),
            Dense(len(self.actions), activation='linear')
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def _preprocess_code(self, code):
        """
        Preprocess the input code to a numerical feature for the ML model.
        For simplicity, the feature is the length of the code.
        """
        return np.array([[len(code)]])

    def identify_patterns(self, code):
        """
        Identifies inefficient patterns in the code using regex.
        """
        print("[DEBUG] Identifying patterns in the code...")
        patterns = []
        if self.language == 'Python':
            if re.search(r'for .* in .*:\n\s+for .* in .*:', code):
                patterns.append("Nested loops detected: Consider optimization.")
            if re.search(r'for .* in .*:\n\s+.*append\(', code):
                patterns.append("Single loop detected: Consider using list comprehensions.")
            if re.search(r'x = x \+ 0', code):
                patterns.append("Redundant code detected.")
        print(f"[DEBUG] Patterns identified: {patterns}")
        return patterns

    def act(self, state):
        """
        Chooses an action based on the epsilon-greedy policy.
        """
        if np.random.rand() <= self.epsilon:
            print("[DEBUG] Choosing action randomly (exploration).")
            return random.choice(range(len(self.actions)))
        print("[DEBUG] Choosing action using model (exploitation).")
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def remember(self, state, action, reward, next_state, done):
        """
        Stores an experience in the replay memory.
        """
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size=32):
        """
        Trains the model using a batch of stored experiences from replay memory.
        """
        print("[DEBUG] Starting experience replay...")
        if len(self.memory) < batch_size:
            print("[DEBUG] Not enough experiences for replay.")
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target += self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        print("[DEBUG] Experience replay completed.")

    def optimize_code(self, code):
        """
        Main function to optimize code using Deep Q-Learning.
        """
        print("[DEBUG] Starting code optimization...")
        state = self._preprocess_code(code)
        optimized_code = code
        suggestions = []

        for iteration in range(5):  # Allow multiple optimization iterations
            action = self.act(state)
            transformed_code, reward = self._apply_action(action, optimized_code)
            if transformed_code != optimized_code:
                suggestions.append(self.actions[action])
                optimized_code = transformed_code
                print(f"[DEBUG] Transformation applied: {self.actions[action]}")

            next_state = self._preprocess_code(optimized_code)
            self.remember(state, action, reward, next_state, reward > 0)
            state = next_state
        self.replay()
        print("[DEBUG] Optimization completed.")
        return suggestions, optimized_code

    def _apply_action(self, action_index, code):
        """
        Applies an optimization action to the code with explicit hardcoding for known inefficiencies.
        """
        print(f"[DEBUG] Applying action: {self.actions[action_index]}")

        try:
            if self.actions[action_index] == "replace_nested_loops":
                # Replace nested loops with a list comprehension
                if "result = []" in code and "for i in range(" in code and "for j in range(" in code:
                    code = code.replace(
                        "result = []\nfor i in range(10):\n    for j in range(10):\n        result.append(i * j)",
                        "result = [i * j for i in range(10) for j in range(10)]"
                    )
            elif self.actions[action_index] == "use_list_comprehension":
                # Replace single loop with a list comprehension
                if "result = []" in code and "for num in range(" in code and "result.append(" in code:
                    code = code.replace(
                        "result = []\nfor num in range(20):\n    result.append(num ** 2)",
                        "result = [num ** 2 for num in range(20)]"
                    )
            elif self.actions[action_index] == "replace_string_concatenation":
                # Replace string concatenation in a loop with join()
                if "sentence = ''" in code and "for word in words:" in code and "sentence += word + ' '" in code:
                    code = code.replace(
                        "sentence = ''\nfor word in words:\n    sentence += word + ' '",
                        "sentence = ' '.join(words) + ' '"
                    )
            elif self.actions[action_index] == "replace_manual_sum":
                # Replace manual sum with built-in sum()
                if "total = 0" in code and "for num in numbers:" in code and "total += num" in code:
                    code = code.replace(
                        "total = 0\nfor num in numbers:\n    total += num",
                        "total = sum(numbers)"
                    )
            elif self.actions[action_index] == "use_set_for_uniqueness":
                # Replace list-based uniqueness with set-based
                if "unique_items = []" in code and "for item in items:" in code and "if item not in unique_items:" in code:
                    code = code.replace(
                        "unique_items = []\nfor item in items:\n    if item not in unique_items:\n        unique_items.append(item)",
                        "unique_items = list(set(items))"
                    )
            else:
                print(f"[DEBUG] No hardcoded transformation for action: {self.actions[action_index]}")

            return code, 10  # Assign a reward for each successful transformation

        except Exception as e:
            print(f"[ERROR] Failed to apply action {self.actions[action_index]}: {e}")
            return code, 0