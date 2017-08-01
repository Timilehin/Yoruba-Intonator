"""TODO - adapt this code to Yoruba corpus"""

import numpy as np
import theano
import theano.tensor as T
import lasagne
from lasagne.layers import *
from data import train_valid_test_gen #create this later!
# from layers import BroadcastLayer, highway_dense

import time
import tqdm

CONSTS = {
	'vocab_len': 10 #fill this in later!
}

BATCHSIZE = 32
CONTEXT_DIM = CONSTS['vocab_len'] * 5


def create_network(input_var):
	l_inp = InputLayer(shape=(BATCHSIZE, CONTEXT_DIM), input_var=input_var)
	l_dense_1 = DenseLayer(dropout(l_inp, 0.5), num_units=1024)
	l_dense_2 = DenseLayer(dropout(l_dense_1, 0.5), num_units=1024)
	l_dense_3 = DenseLayer(dropout(l_dense_2, 0.5), num_units=512, nonlinearity=lasagne.nonlinearities.softmax)


if __name__ == "__main__":
	train_gen, val_gen, test_gen = train_valid_test_gen(BATCHSIZE)

	input_var = T.matrix('inputs')
	target_var = T.tensor2('targets')

	print("Compiling...")
	network = encoder_network(input_var)

	# Training functions
	prediction = lasagne.layers.get_output(network)
	loss = lasagne.objectives.categorical_crossentropy(prediction, target_var).mean()

	params = lasagne.layers.get_all_params(network, trainable=True)
	updates = lasagne.updates.adam(loss, params, learning_rate=0.01)

	# Validation Metrics
	val_prediction = lasagne.layers.get_output(network, deterministic=True)
	val_loss = lasagne.objectives.categorical_crossentropy(val_prediction.reshape((-1, CONSTS['targ_char_dim'])), target_var.reshape((-1, CONSTS['targ_char_dim']))).mean()
	val_acc = T.mean(T.eq(T.round(val_prediction), target_var))

	# Test output fn:
	test_prediction = lasagne.layers.get_output(network, deterministic=True)

	train_fn = theano.function([input_var, target_var], [loss, train_acc], updates=updates)
	val_fn = theano.function([input_var, target_var], [val_loss, val_acc])
	test_fn = theano.function([input_var], test_prediction)
	print("...Done")


	num_epochs = 5
	for epoch in range(num_epochs):

		print("Epoch {0}. Training...".format(epoch + 1))
		# In each epoch, we do a full pass over the training data:
		train_err = 0
		train_acc = 0
		train_batches = 0
		start_time = time.time()
		for batch in tqdm.tqdm(train_gen):
			inputs, langs, targets = batch
			err, acc = train_fn(inputs, langs, targets)
			train_err += err
			train_acc += acc
			train_batches += 1

		print("Validating...")
		# And a full pass over the validation data:
		val_err = 0
		val_acc = 0
		val_batches = 0
		for batch in tqdm.tqdm(val_gen):
			inputs, langs, targets = batch
			err, acc = val_fn(inputs, langs, targets)
			val_err += err
			val_acc += acc
			val_batches += 1


		# Then we print the results for this epoch:
		print("Epoch {} of {} took {:.3f}s".format(
			epoch + 1, num_epochs, time.time() - start_time))
		print("  training loss:\t\t{:.6f}".format(train_err / train_batches))
		print("  training accuracy:\t\t{:.2f} %".format(
			train_acc / train_batches * 100))
		print("  validation loss:\t\t{:.6f}".format(val_err / val_batches))
		print("  validation accuracy:\t\t{:.2f} %".format(
			val_acc / val_batches * 100))



