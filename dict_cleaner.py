import string 

filename = "yoruba_dictionary.txt"
file = open(filename, "r")
bad_chars = ["<", "?", ".", ",", "(", ")", ":", ";", "-", "\"", "'", "+"] + list(string.digits)

fh = open("cleaned_yoruba_dict.txt","w")

for line in file:
    if line[0] not in bad_chars: #change it to be that no bad char must bein the word. 
  		fh.write(line)

fh.close()