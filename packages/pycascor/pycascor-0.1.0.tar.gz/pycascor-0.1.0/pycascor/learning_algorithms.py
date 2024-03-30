

class LearningAlgorithm(object):
    def update(self, delta: float, weight: float, slope: float, previous_slope: float, epsilon: float,
               decay: float, mu: float, shrink_factor: float):
        raise NotImplemented()


class QuickProp(LearningAlgorithm):

    def update(self, delta: float, weight: float, slope: float, previous_slope: float, epsilon: float,
               decay: float, mu: float, shrink_factor: float) -> (float, float, float, float):
        """
        Given weight, delta, slope, and previous slope,
        update weight and delta appropriately.  Move
        slope to previous slope and zero out slope.  Add weight decay term to
        each slope before doing the update.
        """

        decayed_slope: float = slope + (decay * weight)
        next_step: float = 0.0

        # The step must always be downhill.
        if delta < 0:
            # If last step was negative...
            if decayed_slope > 0:
                # First, add in linear term if current slope is still positive.
                next_step -= epsilon * decayed_slope

            if decayed_slope >= shrink_factor * previous_slope:
                # If current slope is close to or larger than prev slope...
                # Take maximum size negative step.
                next_step += mu * delta
            else:
                # Else, use quadratic estimate.
                next_step += delta * (decayed_slope / (previous_slope - decayed_slope))

        elif delta > 0:
            # If last step was positive...
            if decayed_slope < 0:
                # First, add in linear term if current slope is still negative.
                next_step -= epsilon * decayed_slope

            if decayed_slope <= shrink_factor * previous_slope:
                # If current slope is close to or more neg than prev slope...
                # Take maximum size positive step.
                next_step += mu * delta
            else:
                # Else, use quadratic estimate.
                next_step += delta * (decayed_slope / (previous_slope - decayed_slope))

        else:
            # Last step was zero, so use only linear term.
            next_step -= float(epsilon) * decayed_slope

        # Having computed the next step, update the data.
        delta = next_step
        weight += next_step
        previous_slope = decayed_slope
        slope = 0.0

        return delta, weight, previous_slope, slope
