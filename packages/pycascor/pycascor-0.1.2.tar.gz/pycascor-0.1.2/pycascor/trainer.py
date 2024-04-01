import logging
from dataclasses import dataclass
from enum import Enum
from pprint import pformat
from typing import Optional
from random import randint

from .activation_functions import ActivationFunction
from .learning_algorithms import LearningAlgorithm, QuickProp
from .nodes import CandidateNode, Connection, InnerConnection, OutputConnection
from .network import CCNetwork, PrunableCCNetwork

log = logging.getLogger(__name__)


@dataclass
class ErrorStats:
    error_count: int
    true_error: float
    sum_square_error: float


class TrainingStatus(Enum):
    WIN = 1
    TIMEOUT = 2
    STAGNANT = 3
    STOP = 4


@dataclass
class TrainingResult:
    status: TrainingStatus
    stats: ErrorStats


class CandidatePool(object):
    def __init__(self, composition: list[tuple[int, ActivationFunction]]):
        self.best_candidate_score: float = 0.0
        self.best_candidate: Optional[CandidateNode] = None

        self.candidates: list[CandidateNode] = []
        self.composition: list[tuple[int, ActivationFunction]] = composition

    def refresh_pool(self, network: CCNetwork, max_connections_per_pair: int = 1):
        self.best_candidate_score = 0.0
        self.best_candidate = None
        self.candidates = []
        for qty, activation_type in self.composition:
            for _ in range(qty):
                candidate = CandidateNode(activation_type)
                for input_node in network.input_nodes:
                    for _ in range(randint(1, max_connections_per_pair)):
                        candidate.input_connections.append(InnerConnection(input_node, candidate))
                for hidden_node in network.hidden_nodes:
                    for _ in range(randint(1, max_connections_per_pair)):
                        candidate.input_connections.append(InnerConnection(hidden_node, candidate))
                for output_node in network.output_nodes:
                    for _ in range(randint(1, max_connections_per_pair)):
                        candidate.output_connections.append(OutputConnection(candidate, output_node))

                self.candidates.append(candidate)

    def compute_correlations(self):
        for candidate in self.candidates:
            candidate.compute_correlations()
            candidate.sum_of_training_activation_values += candidate.value

    def adjust_correlations(self, num_training_cases: int, sum_square_error: float):
        self.best_candidate = None
        self.best_candidate_score = 0.0

        for candidate in self.candidates:
            avg_value = candidate.sum_of_training_activation_values / num_training_cases
            score = 0.0

            for output_connection in candidate.output_connections:
                cor = (output_connection.correlation - (
                        avg_value * output_connection.to_node.sum_error)) / sum_square_error
                output_connection.previous_correlation = cor
                output_connection.correlation = 0.0
                score += abs(cor)

            # Keep track of the candidate with the best overall correlation.
            if score > self.best_candidate_score:
                self.best_candidate_score = score
                self.best_candidate = candidate


class Trainer(object):

    def __init__(self, candidate_pool_composition: list[tuple[int, ActivationFunction]]):

        # Controls the amount of linear gradient descent to use in updating
        # output weights.
        self.output_epsilon: float = float(0.35)  # *output-epsilon*

        # This factor times the current weight is added to the slope at the
        # start of each output-training epoch. This keeps weights from growing too big.
        self.output_decay: float = float(0.0001)  # *output-decay*

        # If we go for this many epochs with no significant change, it's time to
        # stop tuning.  If 0, go on forever.
        self.output_patience: int = 8  # *output-patience*

        # The error must change by at least this fraction of its old value in
        # order to count as a significant change.
        self.output_change_threshold: float = float(0.01)  # *output-change-threshold*

        # Mu parameter used for quickprop training of output weights.  The
        # step size is limited to mu times the previous step.
        self.output_mu: float = float(2.0)  # *output-mu*

        # Derived from *output-mu*.  Used in computing whether the proposed step is
        # too large.
        self.output_shrink_factor: float = self.output_mu / (1.0 + self.output_mu)

        # If we go for this many epochs with no significant change, it's time to
        # stop tuning.  If 0, go on forever.
        self.input_patience: int = 8

        # This factor times the current weight is added to the slope at the
        # start of each output-training epoch. This keeps weights from growing too big.
        self.input_decay: float = float(0.0)

        # Controls the amount of linear gradient descent to use in updating
        # unit input weights.
        self.input_epsilon: float = float(1.0)

        # The correlation score for the best unit must change by at least
        # this fraction of its old value in order to count as a significant
        # change.
        self.input_change_threshold: float = float(0.03)

        # Mu parameter used for quickprop training of input weights.  The
        # step size is limited to mu times the previous step.
        self.input_mu: float = float(2.0)  # *input-mu*

        # Derived from *input-mu*.  Used in computing whether the proposed step is
        # #   too large.
        self.input_shrink_factor: float = self.input_mu / (1.0 + self.input_mu)

        # An output is counted as correct for a given case if the difference
        #   between that output and the desired value is smaller in magnitude than
        #   this value.
        self.score_threshold: float = 0.4

        self.error_tolerance: float = 0

        self.learning_algorithm: LearningAlgorithm = QuickProp()

        self.candidate_pool: CandidatePool = CandidatePool(candidate_pool_composition)

        self.epoch: int = 0

    def list_network(self, network: CCNetwork, error_stats: ErrorStats = None):
        log.info(
            f"Network at Epoch {self.epoch}"
        )
        log.info(
            f"Values: {pformat(network.values)}"
        )
        log.info(
            f"Weights: {pformat(network.weights)}"
        )
        log.info(
            f"Output: {pformat(network.outputs)}"
        )
        log.info(
            f"Output Weight: {pformat(network.output_weights)}"
        )
        log.info(
            f"Output Slopes: {pformat(network.output_slopes)}"
        )
        log.info(
            f"Errors: {pformat(network.errors)}"
        )
        log.info(
            f"Sum Errors: {pformat(network.sum_errors)}"
        )
        if error_stats:
            log.info(
                f"Error Count: {error_stats.error_count} True Error: {error_stats.true_error} "
                f"Sum Square Error: {error_stats.sum_square_error}"
            )

    def increment_epoch(self, network: CCNetwork):
        self.epoch += 1

    def train_network(self, training_inputs: list[list[float]], training_outputs: list[list[float]],
                      network: CCNetwork,
                      out_limit: int = 100, in_limit: int = 100, rounds: int = 25
                      ) -> CCNetwork:
        """
        Train the output weights until stagnation or victory is reached.  Then
        train the input weights to stagnation or victory.  Then install the best
        candidate unit and repeat.

        Args:
            training_inputs: a list of the training cases' input values
            training_outputs: a list of the training cases' expected output values
            network: the network to train
            out_limit: upper limit on the number of cycles in each output phase.
            in_limit:  upper limit on the number of cycles in each input phase.
            rounds: upper limit on the number of unit-installation cycles.

        Returns: a trained network
        """
        log.info("Starting Training")
        self.list_network(network, ErrorStats(0, 0.0, 0.0))

        # prime the candidate pool
        self.candidate_pool.refresh_pool(network)

        # TODO: figure out where this was supposed to get set in the loop
        last_epoch = 10000

        for r in range(rounds):
            result = self.train_outputs(network, out_limit, last_epoch, training_inputs, training_outputs)

            log.debug(f"Finished Training Outputs. Epoch {self.epoch}. Round {rounds}")
            self.list_network(network, result.stats)

            log.info(
                f"Epoch: {self.epoch} Round: {r} Output Training Complete. "
                f"Training result: {result.status} Error stats: {result.stats}")
            if result.status == TrainingStatus.STOP:
                log.info(
                    f"Stop after last epoch {self.epoch - 1}. "
                    f"{network.number_of_nodes - 1} units, "
                    f"{network.number_of_hidden_nodes} hidden, "
                    f"Error {result.stats.true_error}.")
                return network
            elif result.status == TrainingStatus.WIN:
                log.info(f"Victory at {self.epoch} epochs, "
                         f"{network.number_of_nodes - 1} units, "
                         f"{network.number_of_hidden_nodes} hidden, "
                         f"Error {result.stats.true_error}.")
                return network
            elif result.status == TrainingStatus.TIMEOUT:
                log.info(f"Epoch {self.epoch}: "
                         f"Out Timeout  {result.stats.error_count} bits wrong, "
                         f"error {result.stats.true_error}.")
            elif result.status == TrainingStatus.STAGNANT:
                log.info(f"Epoch {self.epoch}: "
                         f"Out Stagnant {result.stats.error_count} bits wrong, "
                         f"error {result.stats.true_error}.")

            self.reset_output_sum_errors_to_average(network, len(training_inputs))
            result = self.train_inputs(network, in_limit, last_epoch, training_inputs, training_outputs, result.stats)

            log.debug(f"Finished Training Inputs. Epoch {self.epoch}. Round {rounds}")
            self.list_network(network, result.stats)

            log.info(
                f"Epoch: {self.epoch} Round: {r} Input Training Complete. "
                f"Training result: {result.status} Error stats: {result.stats}")

            if result.status == TrainingStatus.STOP:
                log.info("Stop after last epoch.")
            elif result.status == TrainingStatus.TIMEOUT:
                log.info(f"Epoch {self.epoch}: In Timeout.  "
                         f"Cor: {self.candidate_pool.best_candidate_score}")
            elif result.status == TrainingStatus.STAGNANT:
                log.info(f"Epoch {self.epoch}: In Stagnant.  "
                         f"Cor: {self.candidate_pool.best_candidate_score}")

            self.install_new_unit(network)
            log.debug(f"Finished Installing New Unit. Epoch {self.epoch}. Round {rounds}")
            self.list_network(network, result.stats)

        return network

    def update_weight(self, total_connections: int, connection: Connection, num_training_cases: int, output: bool):
        # ;;; Note: Scaling *INPUT-EPSILON* by the number of cases and number of
        # ;;; inputs to each unit seems to keep the quickprop update in a good range,
        # ;;; as the network goes from small to large, and across many
        # ;;; different-sized training sets.  Still, choosing a good epsilon value
        # ;;; requires some trial and error.

        if output:
            eps = self.output_epsilon / num_training_cases
            decay = self.output_decay
            mu = self.output_mu
            shrink_factor = self.output_shrink_factor
        else:
            eps = self.input_epsilon / (num_training_cases * total_connections + 1)
            decay = self.input_decay
            mu = self.input_mu
            shrink_factor = self.input_shrink_factor

        delta, weight, prev_slope, slope = self.learning_algorithm.update(
            connection.delta, connection.weight, connection.slope, connection.previous_slope,
            eps, decay, mu, shrink_factor)
        connection.delta = delta
        connection.weight = weight
        connection.slope = slope
        connection.previous_slope = prev_slope

    def train_outputs(self, network: CCNetwork, max_cycles: int, last_epoch: int,
                      training_inputs: list[list[float]], training_outputs: list[list[float]]) -> TrainingResult:
        # Train the output weights.  If we exhaust MAX-EPOCHS, stop with value
        # TIMEOUT.  If there are zero error bits, stop with value :WIN.  Else,
        # keep going until the true error has not changed by a significant amount
        # for *OUTPUT-PATIENCE* epochs.  Then return :STAGNANT.  If
        # *OUTPUT-PATIENCE* is zero, we do not stop until victory or until
        # MAX-EPOCHS is used up."

        last_error = float(0.0)
        quit_epoch = self.epoch + self.output_patience
        first_time = True
        error_stats = ErrorStats(0, 0.0, 0.0)

        for i in range(max_cycles):

            error_stats = self.train_outputs_epoch(network, training_inputs, training_outputs)

            if self.epoch > last_epoch:
                return TrainingResult(TrainingStatus.STOP, error_stats)
            elif error_stats.error_count == 0:
                return TrainingResult(TrainingStatus.WIN, error_stats)
            elif self.output_patience == 0:
                continue
            elif first_time:
                first_time = False
                last_error = error_stats.true_error
            elif abs(error_stats.true_error - last_error) > last_error * self.output_change_threshold:
                last_error = error_stats.true_error
                quit_epoch = self.epoch + self.output_patience
            elif self.epoch >= quit_epoch:
                return TrainingResult(TrainingStatus.STAGNANT, error_stats)
        else:
            # if we haven't left early, then we return timeout
            return TrainingResult(TrainingStatus.TIMEOUT, error_stats)

    def train_inputs(self, network: CCNetwork, max_cycles: int, last_epoch: int,
                     training_inputs: list[list[float]], training_outputs: list[list[float]],
                     error_stats: ErrorStats) -> TrainingResult:
        """ Train the input weights of all candidates.  If we exhaust MAX-EPOCHS,
                   stop with value :TIMEOUT.  Else, keep going until the best candidate
                   unit's score has changed by a significant amount, and then until it does
                   not change significantly for PATIENCE epochs.  Then return :STAGNANT.  If
                   PATIENCE is zero, we do not stop until victory or until MAX-EPOCHS is
                   used up.
               """

        self.correlations_epoch(network, training_inputs, training_outputs, error_stats)

        last_score = 0.0
        quit_epoch = self.epoch + max_cycles
        first_time = True

        for i in range(max_cycles):

            self.train_inputs_epoch(network, training_inputs, training_outputs, error_stats)

            if self.epoch > last_epoch:
                return TrainingResult(TrainingStatus.STOP, error_stats)

            if self.input_patience == 0:
                continue

            if first_time:
                first_time = False
                last_score = self.candidate_pool.best_candidate_score
            elif abs(self.candidate_pool.best_candidate_score - last_score) > last_score * self.input_change_threshold:
                last_score = self.candidate_pool.best_candidate_score
                quit_epoch = i + self.input_patience  # Update quit epoch
            elif i >= quit_epoch:
                return TrainingResult(TrainingStatus.STAGNANT, error_stats)
        else:
            return TrainingResult(TrainingStatus.TIMEOUT, error_stats)

    def install_new_unit(self, network: CCNetwork):
        """ Add the candidate-unit with the best correlation score to the active
                    network.  Then reinitialize the candidate pool. """
        if self.candidate_pool.best_candidate:
            network.install_hidden_node(self.candidate_pool.best_candidate)
        self.candidate_pool.refresh_pool(network)

    def train_outputs_epoch(self, network: CCNetwork, training_inputs: list[list[float]],
                            training_outputs: list[list[float]]) -> ErrorStats:
        """
        Perform forward propagation once for each set of weights in the
        training vectors, computing errors and slopes.  Then update the output
        weights.

        Returns:

        """
        error_stats = ErrorStats(0, 0.0, 0.0)

        for o in network.output_nodes:
            o.sum_error = 0.0

        log.debug(f"Epoch {self.epoch}. Start train outputs epoch")
        self.list_network(network, error_stats)

        training_data = zip(training_inputs, training_outputs)

        # Now run through the training examples.
        for case_input, case_output in training_data:
            network.full_forward_pass(case_input)

            error_stats = self.compute_errors(network, case_output, error_stats)

        error_proportion = error_stats.error_count / (network.number_of_outputs * len(training_outputs))
        if error_proportion < self.error_tolerance:
            error_stats.error_count = 0

        # Do not change weights or count epoch if this run was perfect.
        if error_stats.error_count != 0:
            # Update the active network output weights
            for connection in network.output_connections:
                self.update_weight(len(network.output_connections),
                                   connection, len(training_inputs), output=True)

            # Update the candidate update weights
            for candidate in self.candidate_pool.candidates:
                for connection in candidate.output_connections:
                    self.update_weight(len(candidate.output_connections),
                                       connection, len(training_inputs), output=True)

            self.increment_epoch(network)

            log.debug(f"Epoch {self.epoch}. Train outputs epoch just incremented")
            self.list_network(network, error_stats)

        return error_stats

    def compute_errors(self, network: CCNetwork, case_output: list[float],
                       error_stats: ErrorStats, compute_stats: bool = True,
                       compute_slopes: bool = True) -> ErrorStats:
        """ GOAL is a vector of desired outputs.  Compute and record the error
                    statistics, incrementing the ERR-BITS, TRUE-ERR, and SUM-SQ-ERR variables,
                    and the proper entry in *SUM-ERRORS*.  If SLOPES-P is true, also compute
                    and record the slopes for output weights.
                """
        for i, output in enumerate(network.output_nodes):

            difference = output.update_error(case_output[i], increment_sum_error=compute_stats)

            if compute_stats:
                if abs(difference) >= self.score_threshold:
                    error_stats.error_count += 1

                error_stats.true_error += (difference ** 2)

                error_stats.sum_square_error += (output.error ** 2)

            if compute_slopes:
                for connection in network.output_connections:
                    connection.update_slope()

        return error_stats

    @staticmethod
    def reset_output_sum_errors_to_average(network: CCNetwork, num_training_cases: int):
        # Turn sum-errors into average errors.
        for output_node in network.output_nodes:
            output_node.sum_error /= num_training_cases

    def correlations_epoch(self, network: CCNetwork, training_inputs: list[list[float]],
                           training_outputs: list[list[float]], error_stats: ErrorStats) -> ErrorStats:
        """ Do an epoch through all active training patterns just to compute the
                    initial correlations.  After this one pass, we will update the
                    correlations as we train."""

        training_data = zip(training_inputs, training_outputs)

        log.debug(f"Epoch {self.epoch}. Correlations epoch start")
        self.list_network(network, error_stats)

        # Now run through the training examples.
        for case_input, case_output in training_data:
            # network.full_forward_pass(case_input)

            # error_stats = self.compute_errors(network, case_output, error_stats, compute_stats=False, compute_slopes=False)

            self.candidate_pool.compute_correlations()

        self.candidate_pool.adjust_correlations(len(training_inputs), error_stats.sum_square_error)

        self.increment_epoch(network)

        log.debug(f"Epoch {self.epoch}. Correlation epoch just incremented")
        self.list_network(network, error_stats)

        return error_stats

    def train_inputs_epoch(self, network: CCNetwork, training_inputs: list[list[float]],
                           training_outputs: list[list[float]], error_stats: ErrorStats) -> ErrorStats:
        """ For each training pattern, perform a forward pass.  Tune the candidate units'
                    weights to maximize the correlation score of each. Set sibling weights to 0 for sdcc.
                """
        training_data = zip(training_inputs, training_outputs)

        log.debug(f"Epoch {self.epoch}. Start train inputs epoch")
        self.list_network(network, error_stats)

        # Now run through the training examples.
        for case_input, case_output in training_data:
            network.full_forward_pass(case_input)

            error_stats = self.compute_errors(network, case_output, error_stats, compute_stats=False,
                                              compute_slopes=False)

            [candidate.compute_slope(error_stats.sum_square_error) for candidate in self.candidate_pool.candidates]

        # Now adjust the candidate unit input weights using quickprop.
        for candidate in self.candidate_pool.candidates:
            for connection in candidate.input_connections:
                self.update_weight(len(candidate.input_connections),
                                   connection, len(training_inputs), output=False)

        # Fix up the correlation values for the next epoch.
        self.candidate_pool.adjust_correlations(len(training_inputs), error_stats.sum_square_error)

        self.increment_epoch(network)

        log.debug(f"Epoch {self.epoch}. Train inputs epoch just incremented")
        self.list_network(network, error_stats)

        return error_stats


class OptimalBrainDamageTrainer(Trainer):
    def __init__(self, candidate_pool_composition):
        super(OptimalBrainDamageTrainer, self).__init__(candidate_pool_composition)
        self.pruning_threshold = 0.01

    def increment_epoch(self, network: PrunableCCNetwork):
        super(OptimalBrainDamageTrainer, self).increment_epoch(network)
        self.prune(network)

    def prune(self, network: PrunableCCNetwork):

        to_be_pruned = []
        lowest_saliency = 10.0
        #
        if self.epoch % 10 == 0:
            # look through the output connections for low weights
            for connection in network.output_connections:
                if abs(connection.saliency) < self.pruning_threshold:
                    to_be_pruned.append(connection)
                else:
                    lowest_saliency = min(lowest_saliency, connection.saliency)

            # if lowest_weight > self.pruning_threshold and self.pruning_threshold < 0.1:
            #     self.pruning_threshold = lowest_weight

            logging.info(f"Pruning {len(to_be_pruned)} connections")
            self.list_network(network)
            for connection in to_be_pruned:
                network.remove_output_connection(connection)

            logging.info(f"After pruning")
            self.list_network(network)

        if self.epoch % 15 == 0:
            # look through the inner connections
            to_be_pruned = []
            for connection in network.inner_connections:
                if abs(connection.saliency) < self.pruning_threshold:
                    to_be_pruned.append(connection)
                else:
                    lowest_saliency = min(lowest_saliency, connection.saliency)

            # if lowest_weight > self.pruning_threshold:
            #     self.pruning_threshold = lowest_weight

            logging.info(f"Pruning {len(to_be_pruned)} connections")
            self.list_network(network)
            for connection in to_be_pruned:
                network.remove_inner_connection(connection)

            logging.info(f"After pruning")
            self.list_network(network)

        if self.pruning_threshold < lowest_saliency < 0.1:
            self.pruning_threshold = lowest_saliency


class PruneTrainer(Trainer):

    def __init__(self, candidate_pool_composition):
        super(PruneTrainer, self).__init__(candidate_pool_composition)
        self.pruning_threshold = 0.01

    # def install_new_unit(self, network: PrunableCCNetwork):
    #     """ Adds all candidates to the active
    #                 network.  Then reinitialize the candidate pool. """
    #     network.install_hidden_nodes(self.candidate_pool.candidates)
    #     # if self.candidate_pool.best_candidate:
    #     #     network.install_hidden_node(self.candidate_pool.best_candidate)
    #     self.candidate_pool.refresh_pool(network, 10)

    def increment_epoch(self, network: PrunableCCNetwork):
        super(PruneTrainer, self).increment_epoch(network)
        self.prune(network)

    def prune(self, network: PrunableCCNetwork):

        to_be_pruned = []
        lowest_weight = 10.0
        #
        if self.epoch % 10 == 0:
            # look through the output connections for low weights
            for connection in network.output_connections:
                if abs(connection.weight) < self.pruning_threshold:
                    to_be_pruned.append(connection)
                else:
                    lowest_weight = min(lowest_weight, connection.weight)

            # if lowest_weight > self.pruning_threshold and self.pruning_threshold < 0.1:
            #     self.pruning_threshold = lowest_weight

            logging.info(f"Pruning {len(to_be_pruned)} connections")
            self.list_network(network)
            for connection in to_be_pruned:
                network.remove_output_connection(connection)

            logging.info(f"After pruning")
            self.list_network(network)

        if self.epoch % 15 == 0:
            # look through the inner connections
            to_be_pruned = []
            for connection in network.inner_connections:
                if abs(connection.weight) < self.pruning_threshold:
                    to_be_pruned.append(connection)
                else:
                    lowest_weight = min(lowest_weight, connection.weight)

            # if lowest_weight > self.pruning_threshold:
            #     self.pruning_threshold = lowest_weight

            logging.info(f"Pruning {len(to_be_pruned)} connections")
            self.list_network(network)
            for connection in to_be_pruned:
                network.remove_inner_connection(connection)

            logging.info(f"After pruning")
            self.list_network(network)

        if self.pruning_threshold < lowest_weight < 0.1:
            self.pruning_threshold = lowest_weight
