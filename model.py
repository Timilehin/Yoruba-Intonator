"""TODO - adapt this code to Yoruba corpus"""
import numpy as np
import theano
import theano.tensor as T
import lasagne
from collections import defaultdict
# import logging
from layers import PossibilitiesFilterLayer
from lasagne.layers import *
from text_featurizer import create_data, framify_features
from transformations import all_variants as poss
# from layers import BroadcastLayer, highway_dense
import os
import pdb
import sys
import time
import tqdm


BATCHSIZE = 32
WINDOW_SIZE = 5

should_train = False

MODELS_PATH = './models'
if not os.path.exists(MODELS_PATH):
	os.mkdir(MODELS_PATH)

# logger = logging.getLogger('accuracy_log')
# word_classifiers = {}
# for eword in ewords:
# 	possibilities = poss(eword)
# 	featurizer = TextFeaturizer(possibilities)
# 	layer = DenseLayer()
# 	word_classifiers[eword] = (featurizer, layer)

def iterate_minibatches(inputs, targets, batchsize, shuffle=True):
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


def create_network(input_var, input_dim, output_dim):
	l_inp = InputLayer(shape=(None, input_dim), input_var=input_var)
	# Standardize input
	# offset = input_var.min(axis=0)
	# scale = input_var.max(axis=0) - input_var.min(axis=0)
	# l_inp_std = standardize(l_inp, offset, scale, shared_axes=0)

	l_dense_1 = DenseLayer(dropout(l_inp, 0.5), num_units=1024)
	l_dense_2 = DenseLayer(dropout(l_dense_1, 0.5), num_units=1024)
	l_dense_3_class = DenseLayer(dropout(l_dense_2, 0.5), num_units=output_dim, nonlinearity=lasagne.nonlinearities.softmax)

	# base_feature_dim = input_dim / WINDOW_SIZE
	# slice_start_ind = base_feature_dim * (WINDOW_SIZE / 2)
	# l_inp_nocontext = SliceLayer(l_inp, slice(slice_start_ind, slice_start_ind + base_feature_dim), axis=1)

	return l_dense_3_class

def filtering_network(probabilities, input_var_nocontext, possibilities, input_dim):
	l_inp_nocontext = InputLayer(shape=(None, input_dim / WINDOW_SIZE), input_var=input_var_nocontext)
	l_filter_poss = PossibilitiesFilterLayer(probabilities, l_inp_nocontext, possibilities)
	
	return l_filter_poss


if __name__ == "__main__":
	
	print("Loading data...")
	from utils import download_file_unicode
	slovenian_text = download_file_unicode('https://www.gutenberg.org/files/34126/34126-0.txt')
	slovenian_text = slovenian_text.split('*** START OF THIS PROJECT')[1]
	slovenian_text = slovenian_text.split('*** END OF THIS PROJECT')[0]

	# pdb.set_trace()

	inputs, targets, stripped, accented = create_data(slovenian_text, WINDOW_SIZE, True)
	
	possibilities = defaultdict(set)
	word_possibilities = defaultdict(set)
	for s, a in zip(stripped.corpus, accented.corpus):
		word_possibilities[s].add(a)
		possibilities[stripped.w_to_i[s]].add(accented.w_to_i[a])

	trv_split, vte_split = int(0.8 * len(inputs)), int(0.9 * len(inputs))
	inputs_train, targets_train = inputs[:trv_split], targets[:trv_split]
	inputs_val, targets_val = inputs[trv_split:vte_split], targets[trv_split:vte_split]
	inputs_test, targets_test = inputs[vte_split:], targets[vte_split:]

	input_var = T.matrix('inputs')

	base_feature_dim = inputs.shape[1] / WINDOW_SIZE
	slice_start_ind = base_feature_dim * (WINDOW_SIZE / 2)
	input_var_nocontext = input_var[:,slice_start_ind:slice_start_ind + base_feature_dim]
	target_var = T.matrix('targets')

	sys.setrecursionlimit(50000)

	print("Compiling...")
	network = create_network(input_var, inputs.shape[1], targets.shape[1])

	# Training functions
	train_prediction = lasagne.layers.get_output(network)
	train_loss = lasagne.objectives.categorical_crossentropy(train_prediction, target_var).mean()
	train_acc = T.mean(T.eq(T.argmax(train_prediction, axis=1), T.argmax(target_var, axis=1)))

	params = lasagne.layers.get_all_params(network, trainable=True)
	updates = lasagne.updates.adam(train_loss, params, learning_rate=0.01)

	# Validation/Test Metrics
	val_prediction = lasagne.layers.get_output(network, deterministic=True)
	val_loss = lasagne.objectives.categorical_crossentropy(val_prediction, target_var).mean()
	val_acc = T.mean(T.eq(T.argmax(val_prediction, axis=1), T.argmax(target_var, axis=1)))

	# lexicon_filter_network = filtering_network(network, input_var_nocontext, possibilities, BATCHSIZE, inputs.shape[1])
	# lexicon_filter_prediction = lasagne.layers.get_output(lexicon_filter_network, deterministic=True)
	# lexicon_filter_acc = T.mean(T.eq(T.argmax(lexicon_filter_prediction, axis=1), T.argmax(target_var, axis=1)))

	train_fn = theano.function([input_var, target_var], [train_prediction, train_loss, train_acc], updates=updates)
	val_fn = theano.function([input_var, target_var], [val_prediction, val_loss, val_acc])
	print("...Done.")
	# pdb.set_trace()

	if should_train:
		num_epochs = 5
		for epoch in range(num_epochs):
			# train_gen, val_gen, test_gen = train_valid_test_gen(inputs, targets, BATCHSIZE)

			print("Epoch {0}. Training...".format(epoch + 1))
			# In each epoch, we do a full pass over the training data:
			train_err = 0
			train_acc = 0
			train_batches = 0
			start_time = time.time()
			for batch in tqdm.tqdm(iterate_minibatches(inputs_train, targets_train, BATCHSIZE)):
				inputs, targets = batch
				_, err, acc = train_fn(inputs, targets)
				train_err += err
				train_acc += acc
				# logger.info(acc)
				train_batches += 1
				if train_batches % 50 == 0:
					print(train_acc / float(train_batches))

			print("Validating...")
			# And a full pass over the validation data:
			val_err = 0
			val_acc = 0
			val_lex_acc = 0
			val_batches = 0
			for batch in tqdm.tqdm(iterate_minibatches(inputs_val, targets_val, BATCHSIZE)):
				inputs, targets = batch
				_, err, acc = val_fn(inputs, targets)
				val_err += err
				val_batches += 1
				if val_batches % 50 == 0:
					print("  validation accuracy:\t\t{:.2f} %".format(
						val_acc / val_batches * 100))
					print("  validation lexicon accuracy:\t\t{:.2f} %".format(
						val_lex_acc / val_batches * 100))

			# Then we print the results for this epoch:
			print("Epoch {} of {} took {:.3f}s".format(
				epoch + 1, num_epochs, time.time() - start_time))
			print("  training loss:\t\t{:.6f}".format(train_err / train_batches))
			print("  training accuracy:\t\t{:.2f} %".format(
				train_acc / train_batches * 100))
			print("  validation loss:\t\t{:.6f}".format(val_err / val_batches))
			print("  validation accuracy:\t\t{:.2f} %".format(
				val_acc / val_batches * 100))
			print("  validation lexicon accuracy:\t\t{:.2f} %".format(
				val_lex_acc / val_batches * 100))

			# Save the model weights
			np.savez(os.path.join(MODELS_PATH, 'model_{0}_val_acc_{1}.npz'.format(epoch, val_acc)), *lasagne.layers.get_all_param_values(network))

	else:
		with np.load(os.path.join(MODELS_PATH, 'model_2_val_acc_0.npz')) as f:
			param_values = [f['arr_%d' % i] for i in range(len(f.files))]
		lasagne.layers.set_all_param_values(network, param_values)

    # After training, we compute and print the test error:
	test_err = 0
	test_acc = 0
	# test_lex_acc = 0
	test_batches = 0
	for batch in iterate_minibatches(inputs_test, targets_test, BATCHSIZE, shuffle=False):
		inputs, targets = batch
		_, err, acc = val_fn(inputs, targets)
		test_err += err
		test_acc += acc
		test_batches += 1
	print("Final results:")
	print("  test loss:\t\t\t{:.6f}".format(test_err / test_batches))
	print("  test accuracy:\t\t{:.2f} %".format(
		test_acc / test_batches * 100))
	# print("  test accuracy with lexicon:\t\t{:.2f} %".format(
	# 	test_lex_acc / test_batches * 100))

	# We now incorporate the lexicon.
	stripped_r, accented_r, inputs_test_r, targets_test_r = stripped.corpus[WINDOW_SIZE/2:1000 + (WINDOW_SIZE/2)], accented.corpus[WINDOW_SIZE/2:1000 + (WINDOW_SIZE/2)], inputs_test[:1000], targets_test[:1000]
	preds_r, err_r, acc_r = val_fn(inputs_test_r, targets_test_r)
	word_lex_preds = []
	for ind, word in enumerate(stripped_r):
		posses = list(word_possibilities[word])
		if len(posses) > 1:
			# pdb.set_trace()
			indices = [accented.w_to_i[a] for a in posses]
			heighest_weighted_word = posses[np.argmax(preds_r[ind, indices])]
			word_lex_preds.append(heighest_weighted_word)
		else:
			word_lex_preds.append(posses[0])

	print('Test with lex accuracy: {0}'.format(sum([1.0 if p == a else 0.0 for p, a in zip(word_lex_preds, accented_r)]) / len(word_lex_preds)))



