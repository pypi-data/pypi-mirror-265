from __future__ import annotations

import logging
from random import uniform
from numpy import sign

from .activation_functions import ActivationFunction

latest_id: int = 0

log = logging.getLogger(__name__)


def get_unique_id():
    global latest_id
    latest_id += 1
    return latest_id


def random_weight(weight_range: float = 1.0) -> float:
    # Select a random weight, uniformly distributed over the
    # interval from minus to plus *weight-range*."
    rand_number = uniform(-weight_range, weight_range)
    return float(rand_number)


class Connection(object):
    def __init__(self, from_node: [InputNode, HiddenNode], to_node: [HiddenNode, OutputNode]):

        self.id = get_unique_id()
        # Holds the current input weight.
        # initialize to a random weight
        self._weight: float = random_weight(1.0)

        # Holds the input weight delta.
        self._delta: float = 0.0

        # Holds the input weight slope.
        self._slope: float = 0.0

        # Holds the previous value of the input weight slope.
        self._previous_slope: float = 0.0

        # The input that feeds into this connection
        self.from_node: [InputNode, HiddenNode] = from_node
        self.to_node: [HiddenNode, OutputNode] = to_node

    def __str__(self):
        return f"Connection {self.id} from {self.from_node.id} to {self.to_node.id}. " \
               f"Weight: {self.weight} Delta: {self.delta} Slope: {self.slope} PSlope: {self.previous_slope}"

    @property
    def weighted_input_value(self) -> float:
        return self.weight * self.from_node.value

    @property
    def saliency(self) -> float:
        return self.weighted_input_value * (1 - self.weighted_input_value) * (1 - 2 * self.weighted_input_value)

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value: float):
        log.debug(f"Updating weight for {str(self)} to {value} ")
        self._weight = value

    @property
    def delta(self):
        return self._delta

    @delta.setter
    def delta(self, value: float):
        log.debug(f"Updating delta for {str(self)} to {value} ")
        self._delta = value

    @property
    def slope(self):
        return self._slope

    @slope.setter
    def slope(self, value: float):
        log.debug(f"Updating slope for {str(self)} to {value} ")
        self._slope = value

    @property
    def previous_slope(self):
        return self._previous_slope

    @previous_slope.setter
    def previous_slope(self, value: float):
        log.debug(f"Updating previous slope for {str(self)} to {value} ")
        self._previous_slope = value


class InnerConnection(Connection):
    def __init__(self, from_node: [InputNode, HiddenNode], to_node: [CandidateNode, HiddenNode]):
        super(InnerConnection, self).__init__(from_node, to_node)

    def update_slope(self, overall_direction: float):
        self.slope += overall_direction * self.from_node.value


class OutputConnection(Connection):
    def __init__(self, from_node: [InputNode, HiddenNode, CandidateNode], to_node: OutputNode):
        super(OutputConnection, self).__init__(from_node, to_node)

        # holds the correlation between a node's value and the residual
        # error of the output, computed over a whole epoch.
        self._correlation: float = 0.0

        # Holds the output_correlation value computed in the previous training epoch.
        self._previous_correlation: float = 0.0

    def __str__(self):
        return f"Connection from {self.from_node} to {self.to_node}. " \
               f"Weight: {self.weight} Delta: {self.delta} Slope: {self.slope} PSlope: {self.previous_slope}" \
               f"Correlation: {self.correlation} PCorrelation: {self.previous_correlation}"

    def update_output_correlation(self, activation_value: float) -> None:
        self.correlation += activation_value * self.to_node.error

    def get_direction(self, activation_prime: float, sum_square_error: float):
        _sign = sign(self.previous_correlation)

        return _sign * (activation_prime * ((self.to_node.error - self.to_node.sum_error) / sum_square_error))

    def update_slope(self):
        self.slope += self.to_node.error * self.from_node.value

    @property
    def correlation(self):
        return self._correlation

    @correlation.setter
    def correlation(self, value: float):
        log.debug(f"Updating correlation for {str(self)} to {value} ")
        self._correlation = value

    @property
    def previous_correlation(self):
        return self._previous_correlation

    @previous_correlation.setter
    def previous_correlation(self, value: float):
        log.debug(f"Updating previous correlation for {str(self)} to {value} ")
        self._previous_correlation = value


class Node(object):

    def __init__(self):
        self.id = get_unique_id()

        self._value: float = 0.0

    @property
    def value(self) -> float:
        return self._value


class InputNode(Node):

    def __str__(self):
        return f"Input {self.id}: {self._value}"

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        log.debug(f"Updating value for {str(self)} to {value} ")
        self._value = value


class OutputNode(Node):
    def __init__(self, activation_function: ActivationFunction):
        super().__init__()
        self.activation_function = activation_function

        self.connections: list[OutputConnection] = []

        self._error: float = 0.0
        self._sum_error: float = 0.0

    def __str__(self):
        return f"Output {self.id}: {self._value} Error: {self._error} Sum Error: {self._sum_error}"

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value: float):
        log.debug(f"Updating error for {str(self)} to {value} ")
        self._error = value

    @property
    def sum_error(self):
        return self._sum_error

    @sum_error.setter
    def sum_error(self, value: float):
        log.debug(f"Updating sum error for {str(self)} to {value} ")
        self._sum_error = value

    @property
    def value(self) -> float:
        return self._value

    def compute_value(self):
        sum_val = 0.0

        for connection in self.connections:
            sum_val += connection.weighted_input_value

        value = self.activation_function.output(sum_val)

        self._value = value

    def add_connection(self, connection: OutputConnection):
        self.connections.append(connection)

    def update_error(self, expected_value: float, increment_sum_error: bool = True) -> float:
        actual = self.value
        diff = actual - expected_value

        log.debug(f"Difference in expected vs actual value for {str(self)} is {diff} ")

        ep = diff * self.activation_function.output_prime(actual)
        self.error = ep

        if increment_sum_error:
            self.sum_error += ep

        return diff


class CandidateNode(Node):
    def __init__(self, activation_function: ActivationFunction):
        super().__init__()

        self.activation_function: ActivationFunction = activation_function

        self.input_connections: list[InnerConnection] = []
        self.output_connections: list[OutputConnection] = []

        # used by candidate
        # the sum of its values over an entire training set.
        self._sum_of_training_activation_values: float = 0.0

    def __str__(self):
        return f"Candidate {self.id}: {self._value} Sum: {self._sum_of_training_activation_values}" \
               f"Inputs: {len(self.input_connections)} Outputs: {len(self.output_connections)}"

    @property
    def sum_of_training_activation_values(self):
        return self._sum_of_training_activation_values

    @sum_of_training_activation_values.setter
    def sum_of_training_activation_values(self, value: float):
        log.debug(f"Updating sum of training activation values for {str(self)} to {value} ")
        self._sum_of_training_activation_values = value

    def add_output_connection(self, connection: OutputConnection):
        self.output_connections.append(connection)

    def add_input_connection(self, connection: InnerConnection):
        self.input_connections.append(connection)

    @property
    def value(self) -> float:
        activation, _ = self.activation()
        self._value = activation
        log.debug(f"Current value for {str(self)} is {activation} ")

        return activation

    def activation(self) -> tuple[float, float]:
        sum_of_weighted_input_values = 0.0
        # Forward pass through each candidate unit to compute activation-prime.
        for connection in self.input_connections:
            sum_of_weighted_input_values += connection.weighted_input_value

        activation = self.activation_function.activation(sum_of_weighted_input_values)
        activation_prime = self.activation_function.activation_prime(activation, sum_of_weighted_input_values)

        log.debug(f"Current activation for {str(self)} is {activation} ")
        log.debug(f"Current activation prime for {str(self)} is {activation_prime} ")

        return activation, activation_prime

    def compute_correlations(self):
        activation, _ = self.activation()

        # Accumulate value of each unit times error at each output.
        for connection in self.output_connections:
            connection.update_output_correlation(activation)

    def compute_slope(self, sum_square_error: float):
        activation, activation_prime = self.activation()

        overall_direction = 0.0

        for output_connection in self.output_connections:
            output_connection.update_output_correlation(activation)
            overall_direction -= output_connection.get_direction(activation_prime, sum_square_error)

        for connection in self.input_connections:
            connection.update_slope(overall_direction)


class HiddenNode(Node):
    def __init__(self, value: float, activation_function: ActivationFunction):
        super().__init__()

        self.activation_function = activation_function
        self._value = value
        self.input_connections: list[InnerConnection] = []
        self.output_connections: list[OutputConnection] = []

    def __str__(self):
        return f"Hidden {self.id}: {self._value}"

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        log.debug(f"Updating value for {str(self)} to {value} ")
        self._value = value

    def compute_value(self):
        sum_val = float(0.0)

        for connection in self.input_connections:
            sum_val += connection.weighted_input_value

        self.value = self.activation_function.activation(sum_val)


