import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train, num_dimenstion = X.shape
  num_class = W.shape[1]
  prob_history = np.zeros((num_train, num_class))
  for i in xrange(num_train):
    scores = np.dot(X[i], W)
    scores -= np.max(scores)    # Numeric stability.
    exp_scores = np.exp(scores)
    prob_history[i] = exp_scores / np.sum(exp_scores)

  loss = np.mean(-np.log(prob_history[np.arange(num_train), y]))
  loss += reg * np.sum(W**2)

  # derivative(without regularization):
  # dLi/dWj = 1/Pyi * Pyi * (1-Pyi) * Xi when j=yi
  # else    = 1/Pyi * -Pyi * Pj * Xi
  for i in xrange(num_train):
    for j in xrange(num_class):
      if j == y[i]:
        # dW[:, j] += 1/prob_history[i] * prob_history[i] * (1-prob_history[i]) * X[i]
        dW[:, j] += -(1-prob_history[i, j]) * X[i, :]
      else:
        dW[:, j] += prob_history[i, j] * X[i, :]
  
  dW /= num_train
  dW += reg * 2 * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train = X.shape[0]
  prob_matrix = np.exp(np.dot(X, W))
  prob_matrix /= np.sum(prob_matrix, axis=1, keepdims=True)
  loss = np.sum(-np.log(prob_matrix[np.arange(num_train), y]))
  loss /= num_train
  loss += reg * np.sum(W**2)

  prob_matrix[np.arange(num_train), y] -= 1
  dW = np.dot(X.T, prob_matrix)
  dW /= num_train
  dW += reg * 2 * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

