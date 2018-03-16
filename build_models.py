#make a function that does everything you need and tells you where the files are and progress updates.
from semantic_bigram import generate_bigram, generate_contextual_bigram
from bigram_probabilities import generate_bigram_probabilities
filename = "tokenized_sentences.txt"
print("Generating bigrams from {}".format(filename))
generate_bigram(filename)
print("Generating contextual bigrams from {}".format(filename))
generate_contextual_bigram(filename)
print("Generating bigram probabilities")
generate_bigram_probabilities()