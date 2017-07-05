import re

str = '/places/default/view/Andorra-6'
reg = '*/(view|index)'

if re.match(reg, str):
    print "cool"
else:
    print "fuck"