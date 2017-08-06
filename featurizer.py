import numpy as np
from nltk.tokenize.regexp import RegexpTokenizer
import theano
import theano.tensor as T

word_tokenizer = RegexpTokenizer('\w+')

"""Utility for one hot encoding/decoding text"""
# TODO - refactor to use np's own string arrays and such
class TextFeaturizer(object):

	"""Initialize with representative corpus"""
	def __init__(self, corpus, save_corpus=True):
		if save_corpus:
			self.corpus = save_corpus

		self.uniques = set(words)
		self.n = len(self.uniques)
		indexed_uniques = enumerate(self.uniques)

		self.w_to_i = dict([(w, i) for i, w in indexed_uniques])
		self.i_to_w = dict([(i, w) for i, w in indexed_uniques])

		self.eyemat = np.eye(self.n)

	"""Featurizes a list of words"""
	def featurize(self, words):
		return self.eyemat[[self.w_to_i[word] for word in words]]

	"""Unfeaturize a matrix into a list of words"""
	def unfeaturize(self, matrix):
		return [self.i_to_w[ind] for ind in np.argmax(matrix, axis=1)]

	def get_corpus(self):
		if not self.corpus:
			raise ValueError("This featurizer was not initialized with a corpus.")

		return self.corpus

"""Takes in a corpus (raw string), tokenizes it, and one-hot encodes it according
to distinct tokens. Returns a matrix of dim (length of corpus, size of vocab)"""
def token_featurize_corpus(corpus, make_lowercase=True):
	corpus = corpus.lower() if make_lowercase else corpus
	words = word_tokenizer.tokenize(corpus)

	return TextFeaturizer(words)

"""Framify features according to a given window size.
Returns a matrix of size (matrix.shape[0] - window_size + 1, matrix.shape[1] * window_size)"""
def framify_features(matrix, window_size):
	frame_bound = matrix.shape[0] - window_size + 1
	frame_shifts = tuple(matrix[i:i+frame_bound] for i in range(window_size))
	return np.hstack(frame_shifts)


