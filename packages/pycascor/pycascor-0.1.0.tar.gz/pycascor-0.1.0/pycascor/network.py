from __future__ import annotations

import logging

from numpy import sign

from .activation_functions import ActivationFunction
from .nodes import InputNode, OutputNode, HiddenNode, OutputConnection, CandidateNode, random_weight, InnerConnection


class CCNetwork(object):
    def __init__(self, num_inputs: int, num_outputs: int, output_function: ActivationFunction):
        self.input_nodes: list[InputNode] = [InputNode() for _ in range(num_inputs + 1)]  # 1 for the bias node
        self.output_nodes: list[OutputNode] = [OutputNode(output_function) for _ in range(num_outputs)]
        self.hidden_nodes: list[HiddenNode] = []

        self.output_connections: list[OutputConnection] = []
        self.inner_connections: list[InnerConnection] = []

        # connect all the inputs to all the outputs
        for input_node in self.input_nodes:
            for output_node in self.output_nodes:
                connection = OutputConnection(input_node, output_node)
                self.output_connections.append(connection)
                output_node.add_connection(connection)

    def __str__(self):
        return f"Network: Inputs: {len(self.input_nodes) - 1} Outputs: {len(self.output_nodes)} " \
               f"Hidden: {len(self.hidden_nodes)} " \
               f"OutputConnections: {len(self.output_connections)}"

    def set_inputs(self, training_case: list[float]):
        self.input_nodes[0].value = 1.0  # set the bias node to 1

        for i, input_value in enumerate(training_case):
            self.input_nodes[i+1].value = input_value

    @property
    def number_of_nodes(self) -> int:
        return len(self.input_nodes) + len(self.hidden_nodes) - 1  # remove one for the bias node

    @property
    def number_of_hidden_nodes(self) -> int:
        return len(self.hidden_nodes)

    @property
    def number_of_outputs(self) -> int:
        return len(self.output_nodes)

    @property
    def number_of_inputs(self) -> int:
        return len(self.input_nodes) - 1

    @property
    def number_inner_connections(self) -> int:
        return len(self.inner_connections)

    @property
    def number_of_output_connections(self) -> int:
        return len(self.output_connections)

    def install_hidden_node(self, node: CandidateNode):
        # node.freeze()
        _hidden_node = HiddenNode(node.value, node.activation_function)
        self.hidden_nodes.append(_hidden_node)

        # link connections to the outputs
        for c_conn in node.output_connections:
            _connection = OutputConnection(_hidden_node, c_conn.to_node)
            _connection.weight = -1.0 * (sign(c_conn.previous_correlation)) * random_weight()
            self.output_connections.append(_connection)
            _hidden_node.output_connections.append(_connection)
            c_conn.to_node.add_connection(_connection)

        for c_conn in node.input_connections:
            _connection = InnerConnection(c_conn.from_node, _hidden_node)
            _connection.weight = c_conn.weight
            _hidden_node.input_connections.append(_connection)
            self.inner_connections.append(_connection)

        _hidden_node.compute_value()

        for node in self.output_nodes:
            node.compute_value()

    def full_forward_pass(self, input_: list[float]):
        """ Set up the inputs from the input_ vector, then propagate activation values
            forward through all hidden nodes and output nodes. """

        self.set_inputs(input_)

        # ;; For each hidden unit, compute the activation value.
        for hidden in self.hidden_nodes:
            hidden.compute_value()

        # Now compute outputs.
        for output in self.output_nodes:
            output.compute_value()

    # For comparison with original implementation
    @property
    def values(self):
        values = []
        for node in self.input_nodes:
            values.append(node.value)
        for node in self.hidden_nodes:
            values.append(node.value)
        return values

    @property
    def weights(self):
        values = []
        for node in self.hidden_nodes:
            for connection in node.input_connections:
                values.append(connection.weight)
        return values

    @property
    def outputs(self):
        values = []
        for node in self.output_nodes:
            values.append(node.value)
        return values

    @property
    def output_weights(self):
        values = []
        for connection in self.output_connections:
            values.append(connection.weight)
        return values

    @property
    def errors(self):
        values = []
        for node in self.output_nodes:
            values.append(node.error)
        return values

    @property
    def output_slopes(self):
        values = []
        for connection in self.output_connections:
            values.append(connection.slope)
        return values

    @property
    def sum_errors(self):
        values = []
        for node in self.output_nodes:
            values.append(node.sum_error)
        return values


class PrunableCCNetwork(CCNetwork):
    def install_hidden_nodes(self, nodes: list[CandidateNode]):
        for node in nodes:
            self.install_hidden_node(node)

    def remove_output_connection(self, connection: OutputConnection):
        node = connection.to_node
        from_node = connection.from_node

        node.connections.remove(connection)
        self.output_connections.remove(connection)

        # if there are no output connections left,
        # we can get rid of the node when
        # we remove the connection.
        if type(from_node) is HiddenNode:
            from_node.output_connections.remove(connection)

            if len(from_node.output_connections) == 0:
                self.hidden_nodes.remove(from_node)
                # Remove the output connections from this node
                for inner_connection in from_node.input_connections:
                    self.inner_connections.remove(inner_connection)

        for node in self.output_nodes:
            node.compute_value()

    def remove_inner_connection(self, connection: InnerConnection):
        end_node: [HiddenNode] = connection.to_node

        end_node.input_connections.remove(connection)
        self.inner_connections.remove(connection)

        # if there are no more input_connections, remove the hidden_node
        # otherwise recalculate its value
        if len(end_node.input_connections) == 0:
            self.hidden_nodes.remove(end_node)
            logging.info(connection)
            logging.info(end_node.output_connections)
            # Remove the output connections from this node
            for output_connection in end_node.output_connections:
                logging.info(output_connection)
                logging.info(output_connection.to_node)
                logging.info(output_connection.to_node.connections)
                output_connection.to_node.connections.remove(output_connection)
                self.output_connections.remove(output_connection)

        else:
            end_node.compute_value()

        for node in self.output_nodes:
            node.compute_value()
