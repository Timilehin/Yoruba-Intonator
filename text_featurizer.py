import numpy as np
import theano
import theano.tensor as T
from unidecode import unidecode
from nltk.tokenize import RegexpTokenizer

whitespace_tokenizer = RegexpTokenizer('\w+')

"""Utility for one hot encoding/decoding text"""
# TODO - refactor to use np's own string dtype and such
class TextFeaturizer(object):

	"""Initialize with representative corpus"""
	def __init__(self, corpus, save_corpus=True):
		if save_corpus:
			self.corpus = corpus

		self.uniques = set(corpus)
		self.n = len(self.uniques)
		indexed_uniques = list(enumerate(self.uniques))

		self.w_to_i = dict([(w, i) for i, w in indexed_uniques])
		self.i_to_w = dict([(i, w) for i, w in indexed_uniques])

		self.eyemat = np.eye(self.n)

	def featurize_word(self, word):
		return self.eyemat[self.w_to_i[word]]

	def unfeaturize_to_word(self, vec):
		return self.i_to_w[np.argmax(vec)]

	"""Featurizes a list of words"""
	def featurize_words(self, words):
		return self.eyemat[[self.w_to_i[word] for word in words]]

	"""Unfeaturize a matrix into a list of words"""
	def unfeaturize_to_words(self, matrix):
		return [self.i_to_w[ind] for ind in np.argmax(matrix, axis=1)]

	def get_corpus(self):
		if not self.corpus:
			raise ValueError("This featurizer was not initialized with a corpus.")

		return self.corpus


"""Takes in a corpus (raw string), tokenizes it, and one-hot encodes it according
to distinct tokens. Returns a matrix of dim (length of corpus, size of vocab)"""
def token_featurize_corpus(corpus, make_lowercase=True):
	corpus = corpus.lower() if make_lowercase else corpus
	words = whitespace_tokenizer.tokenize(corpus)

	return TextFeaturizer(words)


"""Takes in a corpus of accented text. Return TextFeaturizers for both the 
original text and its accent-mark stripped version."""
def create_intonation_sources(accented_text):
	corpus_stripped = unidecode(accented_text)
	acc_featurizer = token_featurize_corpus(accented_text)
	stripped_featurizer = token_featurize_corpus(corpus_stripped)
	return acc_featurizer, stripped_featurizer


"""Framify features according to a given window size.
Returns a matrix of size (matrix.shape[0] - window_size + 1, matrix.shape[1] * window_size)"""
# TODO - compile a theano function to do this
def framify_features(matrix, window_size):
	frame_bound = matrix.shape[0] - window_size + 1
	frame_shifts = tuple(matrix[i:i+frame_bound] for i in range(window_size))
	return np.hstack(frame_shifts)


"""Takes in a corpus of accented text. Creates input data from the accent-stripped
version and targets from the accented words. Returns np arrays with shapes: """
def create_data(accented_text, window_size, return_featurizers=False):
	accented_f, stripped_f = create_intonation_sources(accented_text)
	input_feats = stripped_f.featurize_words(stripped_f.corpus)
	input_frames = framify_features(input_feats, window_size)

	target_feats = accented_f.featurize_words(accented_f.corpus)
	slice_bound = window_size / 2
	target_feats = target_feats[slice_bound:-slice_bound]

	if return_featurizers:
		return input_frames, target_feats, stripped_f, accented_f
	return input_frames, target_feats


if __name__ == "__main__":
	from utils import download_file_unicode
	slovenian_text = download_file_unicode('https://www.gutenberg.org/files/34126/34126-0.txt')
	slovenian_text = slovenian_text.split('*** START OF THIS PROJECT')[1]
	slovenian_text = slovenian_text.split('*** END OF THIS PROJECT')[0]

	acc, stri = create_intonation_sources(slovenian_text)
	


