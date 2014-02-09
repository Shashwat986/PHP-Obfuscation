''' This is my first attempt at building an obfuscator.
I shall be building a PHP obfuscator, and I hope it turns out well.
This shall definitely be hell on the file-size, but let's see what happens
'''

import os
import random
import re
import sys
import math

def obfuscateBeaut(line, header=""):
	oline = ""
	
	chars = list(set(line))
	random.shuffle(chars)
	
	mapping = dict(zip(chars,range(len(chars))))
	
	ctrB = 1
	ctrS = 0
	for key in mapping.keys():
		kval = key
		if kval in ["'","\\"]:
			# Escape the ' and \ symbols
			kval = "\\"+kval
		oline += "${}_{}='{}';".format(header, mapping[key], kval)
		ctrS += 1
		if ctrS == ctrB:
			oline += "\n"
			ctrB += 1
			ctrS = 0
	
	if ctrS != 0:
		usedVars = len(mapping)
		while ctrS < ctrB:
			oline += "${}_{}='{}';".format(header, usedVars, chr(random.randint(48,122)))
			usedVars += 1
			ctrS += 1
		
		oline += "\n"
	try:
		ll = len(oline.split('\n')[-2])
	except IndexError:
		ll = len(oline)
	
	ll += 8
	oline += 'eval("';
	ctrS = 9
	for char in line:
		oline += "${}_{}".format(header, mapping[char])
		ctrS +=len("${}_{}".format(header, mapping[char]))
		if ctrS >= ll:
			oline += '" .'
			oline += '\n  "'
			ctrS = 5
			ll += 8
	
	oline += '");'
	ctrS += 3
	
	if ctrS < ll:
		oline += '/*' + '*'*(ll-4-ctrS) + '*/'
	
	oline += "\n"
	
	return oline

def obfuscateNormal(line, header=""):
	oline = ""
	
	chars = list(set(line))
	random.shuffle(chars)
	
	mapping = dict(zip(chars,range(len(chars))))
	
	for key in mapping.keys():
		kval = key
		if kval in ["'","\\"]:
			# Escape the ' and \ symbols
			kval = "\\"+kval
		oline += "${}_{}='{}';".format(header, mapping[key], kval)
	
	oline += "\n"
	
	oline += 'eval("';
	for char in line:
		oline += "${}_{}".format(header, mapping[char])
	
	oline += '");\n'
	return oline

def obfuscate(fileName, outFileName = None, obfuscateLine = obfuscateNormal):
	fp = open(fileName,'r')
	lines = fp.readlines()
	
	headers = ['obf_','obfus_','bad_','sad_','sadist_','r_']
	
	if outFileName is None:
		if not any([os.path.exists(elem + fileName) for elem in headers]):
			for elem in headers:
				if not os.path.exists(elem+fileName):
					break
		else:
			elem = "%03d_"%(random.randint(1,1000))
			while os.path.exists(elem + fileName):
				elem = "%03d_"%(random.randint(1,1000))
		
		fo = open(elem+fileName,'w')
	else:
		fo = open(outFileName,'w')
	
	is_php = False
	for line in lines:
		#print line
		line = line.strip()
		elems = re.split('(<\?php)|(<\?)|(\?>)',line, flags = re.IGNORECASE)
		for elem in elems:
			if elem is None or len(elem)==0:
				continue
			if elem == '<?' or elem.lower() == '<?PHP'.lower():
				fo.write("<?PHP\n")
				is_php = True
				continue
			if elem == '?>':
				fo.write("?>\n")
				is_php = False
				continue
			if is_php:
				oline = obfuscateLine(elem)
				fo.write(oline)
				#print elem
			else:
				fo.write(elem+"\n"
				)
		
	fo.close()
	fp.close()

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print '''PHP Obfuscator v0.2
		Usage 1:
			>>> import obfuscate
			>>> obfuscate.obfuscate('input.php','output.php')
			>>> obfuscate.obfuscate('input.php')
			>>> obfuscate.obfuscateNormal('echo "hello world";')
		
		Usage 2:
			$ python obfuscate.py input.php
			$ python obfuscate.py input.php output.php
			$ python obfuscate.py input.php output.php AThirdParameterMeansBeautify
		'''
	elif len(sys.argv) < 3:
		ifile = sys.argv[1]
		obfuscate(ifile)
	elif len(sys.argv) < 4:
		ifile = sys.argv[1]
		ofile = sys.argv[2]
		obfuscate(ifile, ofile)
	else:
		ifile = sys.argv[1]
		ofile = sys.argv[2]
		obfuscate(ifile, ofile, obfuscateBeaut)
	