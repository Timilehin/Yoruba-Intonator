import unicodedata
import char_to_unicode



u = unichr(233) + unichr(0x0bf2) + unichr(3972) + unichr(6000) + unichr(13231)
print u 

print chr(int(char_to_unicode.char_to_unicode["a_re"]) 

for i, c in enumerate(u):
    print i, '%04x' % ord(c), unicodedata.category(c),
    print unicodedata.name(c) + "is my name"
    print "~~~~~~~"

# Get numeric value of second character
print unicodedata.numeric(u[1])