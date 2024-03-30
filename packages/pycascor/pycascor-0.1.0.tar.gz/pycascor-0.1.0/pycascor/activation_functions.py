from __future__ import annotations

from math import exp


class ActivationFunction(object):

    @staticmethod
    def activation(inputs_sum: float) -> float:
        raise NotImplemented()

    @staticmethod
    def activation_prime(*value) -> float:
        raise NotImplemented

    @staticmethod
    def second_order_derivative(*value) -> float:
        raise NotImplemented

    @staticmethod
    def output(inputs_sum: float) -> float:
        raise NotImplemented()

    @staticmethod
    def output_prime(output: float) -> float:
        raise NotImplemented()


class AsymmetricSigmoid(ActivationFunction):

    @staticmethod
    def activation(inputs_sum) -> float:
        """ Given the sum of weighted inputs, compute the unit's activation value. """
        if inputs_sum < -15.0:
            return float(0.0)
        elif inputs_sum > 15.0:
            return float(1.0)
        else:
            return float(float(1.0) / (float(1.0) + float(exp(-inputs_sum))))

    @staticmethod
    def activation_prime(value: float, *args) -> float:
        """ Given the unit's activation value and sum of weighted inputs, compute
        the derivative of the activation with respect to the sum. """
        return float(value) * (float(1.0) - float(value))

    @staticmethod
    def second_order_derivative(self, value: float, *args) -> float:
        # TODO: check math
        return value * (1 - value) * (1 - 2 * value)

    @staticmethod
    def output(inputs_sum: float) -> float:
        """
        Compute the value of an output, given the weighted sum of incoming values.
        """
        if inputs_sum < -15.0:
            return float(0)
        elif inputs_sum > 15.0:
            return float(1)
        else:
            return float((float(1.0) / (float(1.0) + float(exp(-inputs_sum)))))

    @staticmethod
    def output_prime(output: float) -> float:
        """ Compute the derivative of an output with respect to the weighted sum of
        incoming values. """
        return float(output) * (float(1.0) - float(output))


class Sigmoid(ActivationFunction):
    # This is added to the derivative of the sigmoid function to prevent the
    # system from getting stuck at the points where sigmoid-prime goes to
    # zero.
    sigmoid_prime_offset: float = float(0.1)  # *sigmoid-prime-offset*

    @staticmethod
    def activation(inputs_sum: float) -> float:
        """ Given the sum of weighted inputs, compute the unit's activation value. """
        if inputs_sum < -15.0:
            return float(-0.5)
        elif inputs_sum > 15.0:
            return float(0.5)
        else:
            return float((float(1.0) / (float(1.0) + float(exp(-inputs_sum)))) - float(0.5))

    @staticmethod
    def activation_prime(value: float, *args) -> float:
        """ Given the unit's activation value and sum of weighted inputs, compute
        the derivative of the activation with respect to the sum. """
        return float(0.25) - (float(value) * float(value))

    @staticmethod
    def second_order_derivative(self, value: float, *args) -> float:
        # TODO: check math
        return value * (1 - value) * (1 - 2 * value)

    @staticmethod
    def output(inputs_sum: float) -> float:
        """
        Compute the value of an output, given the weighted sum of incoming values.
        """
        if inputs_sum < -15.0:
            return float(-0.5)
        elif inputs_sum > 15.0:
            return float(0.5)
        else:
            return float((float(1.0) / (float(1.0) + float(exp(-inputs_sum)))) - float(0.5))

    @staticmethod
    def output_prime(output: float) -> float:
        """ Compute the derivative of an output with respect to the weighted sum of
        incoming values. """
        return Sigmoid.sigmoid_prime_offset + (float(0.25) - (float(output) * float(output)))


class Linear(ActivationFunction):

    @staticmethod
    def output(inputs_sum: float) -> float:
        """
        Compute the value of an output, given the weighted sum of incoming values.
        """
        return inputs_sum

    @staticmethod
    def output_prime(output: float) -> float:
        return float(1.0)


class Gaussian(ActivationFunction):

    @staticmethod
    def activation(inputs_sum: float) -> float:
        """ Given the sum of weighted inputs, compute the unit's activation value. """
        # Gaussian activation function in range 0.0 to 1.0.
        x = float(-0.5) * float(inputs_sum) * float(inputs_sum)
        if x < -75.0:
            return float(0.0)
        else:
            return float(exp(x))

    @staticmethod
    def activation_prime(value: float, inputs_sum: float, *args) -> float:
        """ Given the unit's activation value and sum of weighted inputs, compute
        the derivative of the activation with respect to the sum. """
        return float(-value) * float(inputs_sum)
