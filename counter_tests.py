from counter import Counter

c = Counter(2, [2,3,])
assert c.get_curr_value() == "00"
assert c.can_increment()
c.increment()
assert c.get_curr_value() == "01"
assert c.can_increment()
c.increment()
assert c.get_curr_value() == "02"
assert c.can_increment()
c.increment()
assert c.get_curr_value() == "10"
assert c.can_increment()
c.increment()
assert c.get_curr_value() == "11"
assert c.can_increment()
c.increment()
assert c.get_curr_value() == "12"
assert not c.can_increment()


d = Counter(3, [6,1,6])
assert d.get_curr_value() == "000"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "001"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "002"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "003"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "004"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "005"
assert d.can_increment()
d.increment()

assert d.get_curr_value() == "100"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "101"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "102"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "103"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "104"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "105"
assert d.can_increment()
d.increment()

assert d.get_curr_value() == "200"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "201"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "202"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "203"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "204"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "205"
assert d.can_increment()
d.increment()


assert d.get_curr_value() == "300"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "301"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "302"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "303"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "304"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "305"
assert d.can_increment()
d.increment()


assert d.get_curr_value() == "400"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "401"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "402"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "403"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "404"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "405"
assert d.can_increment()
d.increment()


assert d.get_curr_value() == "500"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "501"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "502"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "503"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "504"
assert d.can_increment()
d.increment()
assert d.get_curr_value() == "505"
assert not d.can_increment()

print "ALL COUNTER TESTS PASS"

