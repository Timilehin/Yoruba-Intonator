"""TODO - adapt this code to Yoruba corpus"""
import numpy as np
import theano
import theano.tensor as T
import lasagne
from lasagne.layers import *
from text_featurizer import create_data
from transformations import all_variants as poss
# from layers import BroadcastLayer, highway_dense

import time
import tqdm


BATCHSIZE = 32
WINDOW_SIZE = 5

# word_classifiers = {}
# for eword in ewords:
# 	possibilities = poss(eword)
# 	featurizer = TextFeaturizer(possibilities)
# 	layer = DenseLayer()
# 	word_classifiers[eword] = (featurizer, layer)

def iterate_minibatches(inputs, targets, batchsize, shuffle=False):
    assert len(inputs) == len(targets)
    if shuffle:
        indices = np.arange(len(inputs))
        np.random.shuffle(indices)
    for start_idx in range(0, len(inputs) - batchsize + 1, batchsize):
        if shuffle:
            excerpt = indices[start_idx:start_idx + batchsize]
        else:
            excerpt = slice(start_idx, start_idx + batchsize)
        yield inputs[excerpt], targets[excerpt]


def train_valid_test_gen(inputs, targets, batchsize):
	# Train-validation-test split
	n = len(inputs)
	inputs_train, targets_train = inputs[:int(0.8 * n)], targets[:int(0.8 * n)]
	inputs_val, targets_val = inputs[int(0.8 * n):int(0.9 * n)], targets[int(0.8 * n):int(0.9 * n)]
	inputs_test, targets_test = inputs[int(0.9 * n):], targets[int(0.9 * n):]

	return (
		iterate_minibatches(inputs_train, targets_train, batchsize),
		iterate_minibatches(inputs_val, targets_val, batchsize),
		iterate_minibatches(inputs_test, targets_test, batchsize)
	)


def create_network(input_var, batchsize, input_dim, output_dim):
	l_inp = InputLayer(shape=(batchsize, input_dim), input_var=input_var)
	l_dense_1 = DenseLayer(dropout(l_inp, 0.5), num_units=1024)
	l_dense_2 = DenseLayer(dropout(l_dense_1, 0.5), num_units=1024)
	l_dense_3_class = DenseLayer(dropout(l_dense_2, 0.5), num_units=output_dim, nonlinearity=lasagne.nonlinearities.softmax)

	return l_dense_3_class

if __name__ == "__main__":
	print("Loading data...")
	from utils import download_file_unicode
	slovenian_text = download_file_unicode('https://www.gutenberg.org/files/34126/34126-0.txt')
	slovenian_text = slovenian_text.split('*** START OF THIS PROJECT')[1]
	slovenian_text = slovenian_text.split('*** END OF THIS PROJECT')[0]

	inputs, targets = create_data(slovenian_text, WINDOW_SIZE)
	train_gen, val_gen, test_gen = train_valid_test_gen(inputs, targets, BATCHSIZE)

	input_var = T.matrix('inputs')
	target_var = T.matrix('targets')

	print("Compiling...")
	network = create_network(input_var, BATCHSIZE, inputs.shape[1], targets.shape[1])

	# Training functions
	train_prediction = lasagne.layers.get_output(network)
	train_loss = lasagne.objectives.categorical_crossentropy(train_prediction, target_var).mean()
	train_acc = T.mean(T.eq(T.round(train_prediction), target_var))

	params = lasagne.layers.get_all_params(network, trainable=True)
	updates = lasagne.updates.adam(train_loss, params, learning_rate=0.01)

	# Validation Metrics
	val_prediction = lasagne.layers.get_output(network, deterministic=True)
	val_loss = lasagne.objectives.categorical_crossentropy(val_prediction, target_var).mean()
	val_acc = T.mean(T.eq(T.round(val_prediction), target_var))

	# Test output fn:
	test_prediction = lasagne.layers.get_output(network, deterministic=True)

	train_fn = theano.function([input_var, target_var], [train_loss, train_acc], updates=updates)
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
			inputs, targets = batch
			err, acc = train_fn(inputs, targets)
			train_err += err
			train_acc += acc
			train_batches += 1

		print("Validating...")
		# And a full pass over the validation data:
		val_err = 0
		val_acc = 0
		val_batches = 0
		for batch in tqdm.tqdm(val_gen):
			inputs, targets = batch
			err, acc = val_fn(inputs, targets)
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



