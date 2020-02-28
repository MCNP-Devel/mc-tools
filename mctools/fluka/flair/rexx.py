#
# Copyright European Organization for Nuclear Research (CERN)
# All rights reserved
#
# Author: Vasilis.Vlachoudis@cern.ch
# Date:   14-May-2004

__author__ = "Vasilis Vlachoudis"
__email__  = "Vasilis.Vlachoudis@cern.ch"

import string

_letters_digits = string.ascii_letters + string.digits
_letters_digits_symbol = _letters_digits + "_."

#-------------------------------------------------------------------------------
# abbrev
#-------------------------------------------------------------------------------
def abbrev(information, info, l=0):
	"""
	return true if the info is an abbreviation of information
	with minimum length l
	"""
	if l>0:
		length = l
	else:
		length = len(info)

	cond1 = (len(information) >= len(info))
	cond2 = (len(info) >= length)
	cond3 = (information[:len(info)] == info)
	return cond1 and cond2 and cond3

#-------------------------------------------------------------------------------
# center
#-------------------------------------------------------------------------------
def center(s, l, pad=' '):
	if l<=0: return ""
	i = l - len(s)
	if i==0:
		return s
	elif i < 0:
		i = -i
		a = i // 2
		return s[a:a+l]
	else:
		a = i // 2
		return "%s%s%s"%(pad*a, s, pad*(i-a))

#-------------------------------------------------------------------------------
# datatype
#-------------------------------------------------------------------------------
def datatype(s, check="N"):
	"""rexx datatype function"""

	try:
		if not s: return check=="X" or check=="B"
	except:
		return check=="X" or check=="B"

	if check=="N":
		return _isnum(s)

	if check=="A":
		return verify(s, _letters_digits)==-1
	elif check=="L":
		return verify(s, string.ascii_lowercase)==-1
	elif check=="M":
		return verify(s, string.ascii_letters)==-1
	elif check=="U":
		return verify(s, string.ascii_uppercase)==-1
	elif check=="O":
		return verify(s, string.octdigits)==-1
	elif check=="X":
		return verify(s, string.hexdigits)==-1
	elif check=="S":
		return (s[0] in string.ascii_letters) and \
			(verify(s[1:], _letters_digits_symbol)==-1)
	else:
		return _isnum(s)

#-------------------------------------------------------------------------------
# insert
#-------------------------------------------------------------------------------
def insert(new, target, n, pad=" "):
	"""
	insert new string to target as position n padded with pad characters
	"""
	if n==0:
		return new+target
	elif n>len(target):
		return target + pad*(n-len(target)) + new

	return target[0:n] + new + target[n:]

#-------------------------------------------------------------------------------
# string hash function to return always the same
# not depending on the python version
#-------------------------------------------------------------------------------
def hash(s):
	h = 0
	for ch in s:
		h += ord(ch)
		h += h<<10
		h &= 0xFFFFFFFF
		h ^= h>>6
		h &= 0xFFFFFFFF
	h += h<<3
	h &= 0xFFFFFFFF
	h ^= h>>11
	h &= 0xFFFFFFFF
	h += h<<15
	h &= 0xFFFFFFFF
	return h

#-------------------------------------------------------------------------------
# left
#-------------------------------------------------------------------------------
def left(s, length, pad=" "):
	"""return left of string s of length padded with pad chars"""
	if length<len(s):
		return s[0:length]
	else:
		return s + (pad*(length-len(s)))

#-------------------------------------------------------------------------------
# translate
#-------------------------------------------------------------------------------
def translate(s, tableo=None, tablei=None, pad=" "):
	"""translate string"""
	# If neither input nor output tables, uppercase.
	if tableo is None and tablei is None:
		return s.upper()

	if tableo is None: tableo = xrange(0,255)
	if tablei is None: tablei = xrange(0,255)

	# The input table defaults to all characters.
	dl = len(tablei)-len(tableo)
	if dl>0:
		tableo += pad*dl
	else:
		tablei += pad*(-dl)

	tbl = str.maketrans(tablei,tableo)
	return s.translate(tbl)

#-------------------------------------------------------------------------------
# reverse
#-------------------------------------------------------------------------------
def reverse(s):
	"""reverse string"""
	return s[::-1]

#-------------------------------------------------------------------------------
def search(s, needle):
	"""Search all matching words of needle in the string s"""
	for w in needle:
		if s.find(w) < 0: return False
	return True

#-------------------------------------------------------------------------------
# verify
#-------------------------------------------------------------------------------
def verify(s,ref,match=0,start=0):
	"""
	return the index of the first character in string that
	is not also in reference. if "Match" is given, then return
	the result index of the first character in string that is in reference
	"""

	if start<0: start = 0
	if start>=len(s): return -1

	for i in range(start,len(s)):
		found = ref.find(s[i])==-1
		if found ^ match:
			return i
	return -1

#-------------------------------------------------------------------------------
# xrange
#-------------------------------------------------------------------------------
def xrange(start,stop):
	return "".join([chr(x) for x in range(start, stop+1)])

#-------------------------------------------------------------------------------
# isnum - return true if string is number
#-------------------------------------------------------------------------------
def _isnum(s):
	s = s.strip()
	# accept one sign
	i = 0
	l = len(s)
	if l==0: return False
	if s[i]=='-' or s[i]=='+': i += 1

	# skip spaces after sign
	while i<l and s[i].isspace(): i += 1

	# accept many digits
	if i<l and '0'<=s[i]<='9':
		i += 1
		F  = 1
		while i<l and '0'<=s[i]<='9': i += 1
	else:
		F = 0

	# accept one dot
	if i<l and s[i]=='.':
		i+=1
		# accept many digits
		if i<l and '0'<=s[i]<='9':
			while i<l and '0'<=s[i]<='9': i += 1
		else:
			if not F: return False
	else:
		if not F: return False

	# accept one e/E/d/D
	if i<l and (s[i]=='e' or s[i]=='E' or s[i]=='d' or s[i]=='D'):
		i+=1
		# accept one sign
		if i<l and (s[i]=='-' or s[i]=='+'): i += 1
		# accept many digits
		if i<l and '0'<=s[i]<='9':
			while i<l and '0'<=s[i]<='9': i += 1
		else:
			return False

	if i != l: return False
	return True

#-------------------------------------------------------------------------------
if __name__=="__main__":
	from log import say

	say("abbrev")
	assert     abbrev('information','info',4)
	assert     abbrev('information','',0)
	assert not abbrev('information','Info',4)
	assert not abbrev('information','info',5)
	assert not abbrev('information','info ')
	assert     abbrev('information','info',3)
	assert not abbrev('info','information',3)
	assert not abbrev('info','info',5)

	say("center")
	assert center('****',0,'-')      == ''
	assert center('****',8,'-')      == '--****--'
	assert center('****',7,'-')      == '-****--'
	assert center('*****',8,'-')     == '-*****--'
	assert center('*****',7,'-')     == '-*****-'
	assert center('12345678',4,'-')  == '3456'
	assert center('12345678',5,'-')  == '23456'
	assert center('1234567',4,'-')   == '2345'
	assert center('1234567',5,'-')   == '23456'

	say("datatype")
	assert not datatype("")
	assert not datatype("foobar")
	assert not datatype("foo bar")
	assert not datatype("123.456.789")
	assert     datatype("123.456")
	assert not datatype("DeadBeef")
	assert not datatype("Dead Beef")
	assert not datatype("1234ABCD")
	assert     datatype("01001101")
	assert not datatype("0110 1101")
	assert not datatype("0110 101")
	assert     datatype("1324.1234")
	assert     datatype("123")
	assert     datatype("12.3")
	assert     datatype('123.123')
	assert     datatype('123.123E3')
	assert     datatype('123.0000003')
	assert     datatype('123.0000004')
	assert     datatype('123.0000005')
	assert     datatype('123.0000006')
	assert     datatype(' 23')
	assert     datatype(' 23 ')
	assert     datatype('23 ')
	assert     datatype('123.00')
	assert     datatype('123000E-2')
	assert     datatype('123000E+2')
	assert not datatype("A B C")
	assert not datatype("123ABC")
	assert not datatype("123AHC")
	assert     datatype('0.000E-2')
	assert     datatype('0.000E-1')
	assert     datatype('0.000E0')
	assert     datatype('0.000E1')
	assert     datatype('0.000E2')
	assert     datatype('0.000E3')
	assert     datatype('0.000E4')
	assert     datatype('0.000E5')
	assert     datatype('0.000E6')
	assert     datatype('0E-1')
	assert     datatype('0E0')
	assert     datatype('0E1')
	assert     datatype('0E2')
	assert not datatype('+.')
	assert not datatype('++0')

	say("insert")
	assert insert("abc","def",2) == "deabcf"
	assert insert("abc","def",3) == "defabc"
	assert insert("abc","def",5) == "def  abc"
	assert insert("abc","def",5,'*') == "def**abc"

	say("translate")
#	assert translate("Foo Bar"), "FOO BAR"
	assert translate("Foo Bar","","") == "Foo Bar"
#	assert translate("Foo Bar","") == "       "
#	assert translate("Foo Bar",None,None,'*') == "*******"
	assert translate("Foo Bar",xrange(1,255)) == "Gpp!Cbs"
	assert translate("","klasjdf","woieruw") == ""
	assert translate("foobar","abcdef","fedcba") == "aooefr"

	say("verify")
	assert verify('foobar', 'barfo', 0, 0)==-1
	assert verify('foobar', 'barfo', 1, 0)==0
	assert verify('', 'barfo')==-1
	assert verify('foobar', '')==0
	assert verify('foobar', 'barf', 0, 2)==2
	assert verify('foobar', 'barf', 0, 3)==-1
	assert verify('', '')==-1

	say("All Test passed")
