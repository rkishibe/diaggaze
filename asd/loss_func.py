import tensorflow as tf
from tensorflow.keras import backend as K

def categorical_focal_loss(gamma=2, alpha=0.25):
    """
    Implementation of Focal Loss from the paper in multiclass classification.
    Formula:
        loss = -alpha*((1-p)^gamma)*log(p)
    Parameters:
        alpha -- Weighting factor for class imbalance.
        gamma -- Focusing parameter for modulating factor (1-p).
    """
    # @tf.function
    def focal_loss(y_true, y_pred, sample_weight=None):  # Add sample_weight as an argument

        y_true = tf.cast(y_true, tf.float32)

        # Define epsilon to avoid NaN in backpropagation
        epsilon = K.epsilon()
        y_pred = K.clip(y_pred, epsilon, 1.0 - epsilon)

        # Calculate the cross entropy (log loss)
        cross_entropy = -y_true * K.log(y_pred)

        # Calculate weight, which combines alpha and the focusing factor (1-p)^gamma
        weight = alpha * y_true * K.pow((1 - y_pred), gamma)

        # Compute focal loss
        loss = weight * cross_entropy

        # Sum the losses in the batch
        loss = K.sum(loss, axis=1)

        # If sample_weight is provided, multiply it by the loss
        if sample_weight is not None:
            loss = loss * sample_weight  # Apply sample weights

        return loss
    
    return focal_loss