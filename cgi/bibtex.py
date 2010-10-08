#!/usr/bin/env python
# coding: utf-8

## This is bibtex.py  utilities for conversion of a bibtex file to a list of python 
## dictionaries and related scripts.
#  Copyright (C) Jim Pitman, Dept. Statistics, U.C. Berkeley
#  http://www.stat.berkeley.edu/users/pitman
#  2004-2009
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import re, string, sys, os, shutil, glob
import simplejson, codecs
import urllib, urllib2
import urlparse
import cgi, cgitb 
cgitb.enable()

### STRING CONVERSION TOOLS
greek_lower = ['alpha','beta','gamma','delta','epsilon','zeta','eta','theta','iota','kappa','lambda','mu','nu','xi','omicron','pi','rho','sigma','tau','upsilon','phi','chi','psi','omega']
greek_upper = ['Alpha','Beta','Gamma','Delta','Epsilon','Zeta','Eta','Theta','Iota','Kappa','Lambda','Mu','Nu','Xi','Omicron','Pi','Rho','Sigma','Tau','Upsilon','Phi','Chi','Psi','Omega']


def tex2html (s):      ### convert tex accents and math expressions etc to html
	s = string.replace(s, '\\cflex{o}', '&ocirc;')
	s  = string.replace(s,'\\aleph','&#8501;')
	s  = string.replace(s,'\\v','')
	s  = string.replace(s,'\\aa','&aring;')
	s = string.replace(s,'\\cprime ','\'')
	s = string.replace(s,'\\cyr','')
	s = string.replace(s,'{\\cprime}','\'')
	s = string.replace(s, '``', '\'\'')
	s = string.replace(s, '\\sterling', '&#163;')
	for g in  greek_lower + greek_upper:
		s = string.replace(s, '\\' + g , '&' + g + ';')
	for x in string.lowercase + string.uppercase:
		s = string.replace(s,'{'+x+'}',x)
	s = string.replace(s, '\\sb ', '_')
	s = string.replace(s, '\\sb', '_')
	s = string.replace(s, '\\ver', '|')
	s = string.replace(s, '\\colon', ':')
	s = string.replace(s, '\\Bbb', '')
	s = string.replace(s, '\\rm', '')
	s = string.replace(s, '\\bf', '')
	s = string.replace(s, '\\textbf', '')
	s = string.replace(s, '\\it', '')
	s = string.replace(s, '\\em', '')
	s = string.replace(s, '\\ast', '*')
	s = string.replace(s, '\\sp ', '^')
	s = string.replace(s, '\\sp', '^')
	s = string.replace(s, '$', '')
	s = string.replace(s, '\&', '&amp;')
	s = string.replace(s, '\=', '')   ###unsatisfactory: should give a bar over the letter
	s = string.replace(s, '\\`a', '&agrave;')
	s = string.replace(s, '\\`A', '&Agrave;')
	s = string.replace(s, '\\^a', '&acirc;')
	s = string.replace(s, '\\^A', '&Acirc;')
	s = string.replace(s, '\\ocirc A', '&Aring;')
	s = string.replace(s, '\\\"a', '&auml;')
	s = string.replace(s, '\\\"A', '&Auml;')
	s = string.replace(s, '\\\'a', '&aacute;')
	s = string.replace(s, '\\\'A', '&Aacute;')
	s = string.replace(s, '\\\c c', '&ccedil;')
	s = string.replace(s, '\\c{c}', '&ccedil;')
	s = string.replace(s, '\\c{C}', '&Ccedil;')
	s = string.replace(s, '\\c C', '&Ccedil;')
	s = string.replace(s, '\\\'e', '&eacute;')
	s = string.replace(s, '\\\'E', '&Eacute;')
	s = string.replace(s, '\\`e', '&egrave;')
	s = string.replace(s, '\\`E', '&Egrave;')
	s = string.replace(s, '\\^e', '&ecirc;')
	s = string.replace(s, '\\^E', '&Ecirc;')
	s = string.replace(s, '\\\"e', '&euml;')
	s = string.replace(s, '\\\"E', '&Euml;')
	s = string.replace(s, '\\`i', '&igrave;')
	s = string.replace(s, '\\\`I', '&Igrave;')
	s = string.replace(s, '\\^i', '&icirc;')
	s = string.replace(s, '\\^I', '&Icirc;')
	s = string.replace(s, '\\\"{\\i}}', '&iuml;')
	s = string.replace(s, '\\\"i', '&iuml;')
	s = string.replace(s, '\\\"I', '&Iuml;')
	s = string.replace(s, '\\\'i', '&iacute;')
	s = string.replace(s, '\\\'{\\i}}', '&iacute;')
	s = string.replace(s, '\\\'I', '&Iacute;')
	s = string.replace(s, '\\~n', '&ntilde;')
	s = string.replace(s, '\\o', '&oslash;')
	s = string.replace(s, '\\^o', '&ocirc;')
	s = string.replace(s, '\\^O', '&Ocirc;')
	s = string.replace(s, '\\\"o', '&ouml;')
	s = string.replace(s, '\\\"O', '&Ouml;')
	s = string.replace(s, '\\H o', '&ouml;')
	s = string.replace(s, '\\H{o}', '&ouml;')
	s = string.replace(s, '\\\"{o}', '&ouml;')
	s = string.replace(s, '\\Ho', '&ouml;')
	s = string.replace(s, '\\\H o', '&ouml;')
	s = string.replace(s, '\\\H O', '&Ouml;')
	s = string.replace(s, '\\\'o', '&oacute;')
	s = string.replace(s, '\\\'O', '&Oacute;')
	s = string.replace(s, '\\`o', '&ograve;')
	s = string.replace(s, '\\`O', '&Ograve;')
	s = string.replace(s, '\\`u', '&ugrave;')
	s = string.replace(s, '\\`U', '&Ugrave;')
	s = string.replace(s, '\\^u', '&ucirc;')
	s = string.replace(s, '\\^U', '&Ucirc;')
	s = string.replace(s, '\\\"u', '&uuml;')
	s = string.replace(s, '\\\"U', '&Uuml;')
	s = string.replace(s, '\\\oe', '&oslash')
	s = string.replace(s, '\\c', '')  ### should be cedilla
	s = string.replace(s, '\\u', '')  ### should be a bar
	s = string.replace(s, '{', '')
	s = string.replace(s, '}', '')
	s = string.replace(s, '\\ ', ' ')
	s = string.replace(s, '$^\\circ$', 'o.')
	s = string.replace(s, '\\newblock', '<br>')
	s = string.replace(s, '\\', '')
	return s

html_accents = re.compile(r"\&(\w)\w+;")

def html2ascii(text):
        return html_accents.sub(lambda m: m.group(1), text)

def tex2ascii (s):      ### convert tex accents etc to ascii, designed mainly for author names
	return html2ascii(tex2html(s))


def clean_accents(instring):
	instring = string.replace(instring,'\\cprime ','')
	instring = string.replace(instring,'\v ','')
	instring = string.replace(instring,'{','')
	instring = string.replace(instring,'}','')
	instring = string.replace(instring,'\\','')
	instring = string.replace(instring,'^','')
	#instring = string.replace(instring,'\'','')
	instring = string.replace(instring,'\`','')
	instring = string.replace(instring,'\"','')
	instring = string.replace(instring,'\350','e')
	instring = string.replace(instring,'\351','e')
	instring = string.replace(instring,'\347','c')
	instring = string.replace(instring,'\374','u')
	instring = string.replace(instring,'\260','o.')
	instring = string.replace(instring,'\340','a')
	instring = string.replace(instring,'\352','e')
	instring = string.replace(instring,'\364','o')
	instring = string.replace(instring,'\356','i')
	instring = string.replace(instring,'\373','u')
	instring = string.replace(instring,'\311','E')
	instring = string.replace(instring,'\366','o')
	instring = string.replace(instring,'\371','u')
	return instring



#### TOOLS FOR HANDLING NAME STRINGS  #####
def first_last(namestring):
	## (firstname, lastname) = first_last(namestring)
	namestring = string.strip(namestring)
	if string.find( namestring, ',') >= 0: 
		namesplit  =  string.split(namestring, ',',1)
		return (string.strip(namesplit[1]),  string.strip(namesplit[0]))
	else:
		try:
			if string.find(namestring,' Le ') >= 0:
				namestringsplit  =  string.split(namestring, 'Le ',1)
				lastname = 'Le ' + namestringsplit[1]
				firstnames = namestringsplit[0]
			elif string.find(namestring,' van ') >= 0:
				namestringsplit  =  string.split(namestring, 'van ',1)
				lastname = 'van ' + namestringsplit[1]
				firstnames = namestringsplit[0]
			else:
				namestringsplit  =  string.split(namestring)
				lastname = namestringsplit[ len(namestringsplit) - 1]
				firstnames = ''
				for frag in namestringsplit:
					if frag != lastname:	
						firstnames = firstnames + ' ' + frag
			return (string.strip(firstnames), string.strip(lastname))
		except IndexError:
			#return (namestring,namestring)
			return ('','')
			#return ('Unable_to_parse_name_string_for_first_name', 'Unable_to_parse_name_string_for_last_name')
def first_last_suffix(namestring):
	(first,last,suffix) = ('','','')
	comma_split = namestring.split(',')
	save_names = [string.strip(comma_split[0])]
	for n in comma_split[1:]:
		n = string.strip(n)
		if n in ['I','II','III','IV','V','Jr','Jr.']:
			suffix = n
		else:
			save_names += [string.strip(n)]
	## now proceed as before
	namestring = ','.join(save_names)
	(first,last) = first_last(namestring)
	return (first,last,suffix)

def last_name(namestring):
	(first, last,suffix) = first_last_suffix(namestring)
	return last 

def first_name(namestring):
	(first, last, suffix) = first_last_suffix(namestring)
	return first 

def first_initial (namestring):
	(first, last, suffix) = first_last_suffix(namestring)
	try:
		return first[0]
	except IndexError: return ''

def jptest(namestring):
	return namesting + 'XXX'

def initials(namestring):
	(first, last) = first_last(namestring)
	ss = string.split(first)
	inits = ''
	for s in ss:
		try:
			inits += ' ' + s[0]
		except: IndexError
	return inits

def last_name_first(namestring):
	(first, last) = first_last(namestring)
	if string.strip(last + first) != '': return last + ', ' + first
	else: return ''

def last_name_first(namestring):
	n = ''
	(first, last,suffix ) = first_last_suffix(namestring)
	if string.strip(last + first) != '': n = last + ', ' + first
	if suffix: 
		n  += ', '
		n  += suffix
	return n

def last_names_first(a):  ## format authors from usual bibtex author string
	aus = a.split(' and ')
	aus = [ last_name_first(au) for au in aus ]
	if len(aus) == 0:
		return ''
	elif len(aus) == 1:
		return aus[0]
	elif len(aus) == 2:
		return ' and '.join(aus)
	elif len(aus) >  2:
		return ', '.join(aus[0:-2]) + ', ' + ' and '.join(aus[-2:])


def first_name_first(namestring):
	(first, last) = first_last(namestring)
	return first + ' ' + last

def author_ls(author):
	author = string.replace(author,'\n',' ')
	ss = string.split(author,' and ')
	au_ls = []
	for  a in string.split(author,' and '):
		au_ls += [a]
	return au_ls
###########################################################################################

"""Functions to read a BibTeX string and convert it to a list of dictionaries."""


string_dict = {}
"""Dictionary for string definitions"""
## must be cleared before use if multiple bibs are processed
# to do:  could also handle preamble definitions. 

def up(instring):
	return string.upper(string.strip(instring))
	"""Capitalize and string.strip"""

def lo(instring):
	return string.lower(string.strip(instring))
	"""Uncapitalize and string.strip"""

def strip_quotes(instring):
	"""Strip double quotes enclosing string"""
	instring = string.strip(instring)
	if instring[0] == '"' and instring[-1] == '"':
		return instring[1:-1]
	else: return instring

def strip_braces(instring):
	"""Strip braces enclosing string"""
	instring = string.strip(instring)
	if instring[0] == '{' and instring[-1] == '}':
		return instring[1:-1]
	else: return instring

def test(instring):  
	"""Test to check if instring is well-formed value of a bibtex field:
	returns 
	( number of double quotes mod 2, number of left braces - number right braces )
	"""
	instring = string.replace(instring,'\\"','')
	quote_count = string.count(instring,'"')
	lb_count = string.count(instring,'{')
	rb_count = string.count(instring,'}')
	return (divmod(quote_count , 2)[1] ,lb_count - rb_count)

def string_subst(instring,string_dict):
	""" Substitute string definitions """
	for k in string_dict.keys():
		instring = string.replace(instring,k,string_dict[k])
	return instring

keys_dict = {}
""" Dictionary of keys and their substitutions """
keys_dict['keyw'] = 'keywords'
keys_dict['authors'] = 'author'
keys_dict['bibtex'] = 'url_bib'

def add_key(key):
	""" Add upper-cased key to keys dictionary """
	key = lo(key)
	if key in keys_dict.keys():
		return keys_dict[key]
	else: return key
		
def add_val(instring,string_dict):
	""" Clean instring before adding to dictionary """
	if instring[-1] == ',': val = string.strip(instring)[:-1]  ###delete trailing ','
	else: val = instring
	val = strip_braces(val)
	val = strip_quotes(val)
	#val = strip_braces(val)
	val = string_subst(val,string_dict)
	return val

def read_bibitem(item,string_dict):     ### returns a python dict
		d = {} 
		type_rest = string.split(item, '{' ,1)
		d['bibtype'] = lo(type_rest[0])
		try:
			rest = type_rest[1]
		except IndexError:
			d['error'] = 'IndexError: nothing after first { in @' + item
			rest = ''
		if d['bibtype'] == 'string':
		###### Example:   @string{AnnAP = "Ann. Appl. Probab."}
			try:
				key_val = string.split(rest,'=')
				key = string.strip(key_val[0])
				val = string.strip(key_val[1])
				val = string.strip(val[:-1])   ## strip the trailing '}'
				val = val[1:-1]                ## strip the outer quotes 
				string_dict[key] = val
				#print 'string_dict[', key, '] = ', val
	
			except IndexError:
				d['error'] = 'IndexError: can\'t parse string definition in @' + item
				rest = ''
			
		else:
			comma_split = string.split(rest,',',1)
			d['citekey'] = string.strip(comma_split[0])
			d['bibtex'] = '@' + item
			try:
				rest = comma_split[1]
			except IndexError:
				d['error'] = 'IndexError: nothing after first comma in @' + item
				rest = ''
			
			count = 0
			current_field = ''
			while count <= 600:   ### just a safey net to avoid infinite looping if code breaks
				count = count + 1
				comma_split = string.split(rest,',',1)
				this_frag = comma_split[0]
				current_field = current_field + this_frag + ','
				(quote_count,br_count) = test(current_field)
				if quote_count == 0 and br_count == 0:
					key_val = string.split(current_field,'=',1)
					key = key_val[0]
					try:
						d[add_key(key)] = add_val( key_val[1],string_dict)
					except IndexError:
						d[add_key(key)] = ''
					current_field = ''
				elif quote_count == 0 and br_count < 0:    ###end of bibtex record
					key_val = string.split(current_field,'=',1)
					key = key_val[0]
					try:
						rest = comma_split[1]
					except IndexError:
						rest = ''
					try:
						val_comments  = string.split(key_val[1],'}')
						val = val_comments[0] 
						(quote_count,br_count) = test(val)
						if br_count == 1: val = val + '}'  
						else: val = val + ','  ## add comma to match format
						#### problem is record can end with  either e.g.
						#### year = 1997}
						#### year = {1997}}
						if string.find(key,'}') < 0:
							d[add_key(key)] = add_val( val,string_dict)
						#d['ERROR'] = str( br_count )
						## putting error messages into d['ERROR'] is a good
						## trick for debugging
						try:
							comments = val_comments[1][:-1]
							comments = string.strip(comments)
							if comments != '':
								d['between_entries'] = add_val(comments + ',',string_dict) + add_val(rest,string_dict)
						except: IndexError
					except: IndexError
					current_field = ''
					break
				try:
					rest = comma_split[1]
				except IndexError:
					key_val = string.split(current_field,'=',1)
					key = add_key( key_val[0] )
					if key != '':
						try:
							d[key] = add_val( key_val[1],string_dict)
						except IndexError:
							d[key] = ''
					break
		### impute year from Davis Fron to arxiv output:
		if d.has_key('eprint') and not d.has_key('year'): 
			yy = '????'
			ss = string.split(d['eprint'],'/')
			if len(ss) == 2: yy = ss[1][0:2]
			if yy[0] in ['0']: d['year'] = '20' + yy   ### year 2010 problem!!
			elif yy[0] in ['9']: d['year'] = '19' + yy
		return (d, string_dict)



def read_bibstring(instring, string_dict={}):  ###parses a bibtex string into a list of dictionaries
	""" Main function 
	Input is a string, interpreted as bibtex, output is a list of dictionaries.
	All text after '--BREAK--' is ignored. All keys are regularized to upper
	case. Keys could also be regularized according to substitutions in string_dict
	which could be supplied as an extra argument but which is empty at present.
	"""
	dlist = []
	lines = []

# ADDED PARAMETER FOR string_dict
#	string_dict = {}

#	print instring
	for line in string.split(instring,'\n'):
		if string.find(line,'--BREAK--') >= 0:    
			break
		else: lines = lines + [string.strip(line)]
	instring = string.join(lines,'\n')
	items = string.split('\n'+ instring,'\n@')
	        #### must add the leading '\n' in case string starts with an '@'
	for item in items[1:]:
			(d,string_dict) = read_bibitem(item,string_dict)
			dlist = dlist + [d]	
	return dlist
	
def dict2bibtex(d):
	""" Simple function to return a bibtex entry from a python dictionary """
	outstring =  '@' + d.get('bibtype','unknown') + '{' + d.get('citekey','') + ',\n'
	kill_keys = ['citekey','bibtex','bibitem']
	top_keys = ['latex_output','latex_input','author','title','year',]
	top_items = []
	rest_items = []
	for k in top_keys:
		if k in d.keys(): top_items += [ ( k , d[k] )]
	for k in d.keys():
		if not k in top_keys:
			if not k in kill_keys:
				rest_items += [ ( k , d[k] )]
	rest_items.sort()
	for k in top_items + rest_items:
		outstring = outstring + '\t' + k[0] + ' = {' + k[1] + '},\n'
	outstring = outstring +  '}\n\n'
	return outstring
def wget(address):  ###returns string from httpaddress, or 'IOError'
        try:
		infile = urllib.urlopen(address)
		instring = infile.read()
		if string.find (instring, '404 Not Found') >= 0:
			return 'IOError'
		elif string.find (instring, 'Error 404') >= 0:
			return 'IOError'
		else: 
			return instring
	except IOError:
		return 'IOError'




def intyear(year):
	try: return int(year)
	except: return 3000
def comparison(d,e):
	if intyear(d.get('YEAR','')) > intyear(e.get('YEAR','')): 
		c = 1
	elif intyear(d.get('YEAR','')) < intyear(e.get('YEAR','')): 
		c = -1
	elif d['TITLE'] > e['TITLE']:
		c = 1
	else:
		c = -1
	return   c
def selection(d):
	if d.get('YEAR','') in ['1964','1965','1966']: return 1
	else: return 0


def get_bbl(fname):
	''' convert a typical .bbl file into a dictionary '''
	infile = open(fname + '.bbl','r')
	instring = infile.read()
	instring = instring.split('\\end{thebibliography}')[0]
	items = instring.split('\\bibitem')
	#\bibitem[\protect\citename{Rog, }1965]{Rogers}
	#\bibitem{Rogers}
	bbl= {}
	bbl['__top_line__'] = items[0]
	bbl['__key_order__'] = []
	for item in items[1:]:
		item = item.strip()
		if item[0] == '[':
			item = item.split(']',1)[1]	
			## just discard what's in the "[...]" for now
		#now e.g. item = "{Rogers} .... "
		item = item.strip()[1:]   
		k,v = item.split('}',1)
		v = v.strip()
		bbl[k] = v
		bbl['__key_order__'] += [k]
	return bbl 



def xmake_tex(params):  
	''' make a small tex file  for processing biblio data with input from dictionary params'''
	tex = '''
\\documentclass{article}
*packages_line*
\\nonstopmode
\\begin{document}
\\nocite{*}
\\renewcommand{\\refname}{*refname*}
\\bibliographystyle{*bibliographystyle*}
\\bibliography{*bibfnames*}
\\end{document}
'''
	for k in params.keys():
		tex = tex.replace('*' + k + '*' , params[k] )
	outfile = open( params['tmpfname'] + '.tex','w')
	outfile.write(tex)
	outfile.close()
	p = 'Wrote file ' + params['tmpfname'] + '.tex\n'
	#p+= 'to process data from these BibTex files:\n'
	#p+= params['bibfnames']
	#p+= '\nwith BibTex style "' + params['bibliographystyle'] + '"\n\n'
	return p

def make_files(fname):
	''' usual pdflatex/bibtex processing of file fname.tex to create .aux, .bbl, .pdf etc'''
	p = ''
	os.popen('pdflatex ' + fname, "r").read()
	p += os.popen('bibtex ' + fname, "r").read()
	os.popen('pdflatex ' + fname, "r").read()
	p += os.popen('pdflatex ' + fname, "r").read()
	return p

def bib2tex(bibfname,outfname,params):
	## create a .tex file from a .bib and some parameters
	#outfile = open(outfname + '.bib','w')
	#outfile.write(bibtex)
	#outfile.close()
	params['bibfnames'] = bibfnames
	params['outfname'] =  outfname
	make_tex(params)
	print make_files(outfname)

def make_all_files(params):
	fname = params['tmpfname']
	outfile = open( fname + '.tex','w')
	outfile.write(params['latex'])
	outfile.close()
	p = 'Wrote file ' + params['tmpfname'] + '.tex\n'
	''' usual pdflatex/bibtex processing of file fname.tex to create .aux, .bbl, .pdf etc'''
	os.popen('pdflatex ' + fname, "r").read()
	p += os.popen('bibtex ' + fname, "r").read()
	os.popen('pdflatex ' + fname, "r").read()
	p += os.popen('pdflatex ' + fname, "r").read()
	return p

#def make_bbl(bibfname,outfname,comparison,selection,params):  

def make_bbl(comparison,selection,display,params):  
	tmpfname = params['tmpfname']
	outfname = params['outfname']
	### extract comma separated list of bibfile names from the latex input:
	bibfnames = params['latex'].split('\\bibliography{',1)[1].split('}')[0]
	### extract the relevant .bbl entries 
	bbl = get_bbl(tmpfname)
	dls = []
	for f in bibfnames.split(','):
		infile = open(f + '.bib','r')
		bibstring= infile.read()
		for d in read_bibstring(bibstring):
			d['bibfile'] = d.get('bibfile',f)    ### take a bibfile entry if present, else use the filename
			d['bibitem'] = bbl.get(d['citekey'],'')
			if selection(d) and d['bibitem']: dls += [d]
	dls.sort(comparison)
	#p = '\\begin{itemize}\n'
	p = ''
	count = 0
	for d in dls:
		count += 1
		d['count'] = str(count)
		p += display(d)
	#p += '\\end{itemize}\n'
	### rewrite the extracted/sorted .bbl entries 
	return p
def make_bbl_dls(comparison,selection,params):  
	tmpfname = params['tmpfname']
	outfname = params['outfname']
	### extract comma separated list of bibfile names from the latex input:
	bibfnames = params['latex'].split('\\bibliography{',1)[1].split('}')[0]
	### extract the relevant .bbl entries 
	bbl = get_bbl(tmpfname)
	dls = []
	for f in bibfnames.split(','):
		infile = open(f + '.bib','r')
		bibstring= infile.read()
		for d in read_bibstring(bibstring):
			d['bibfile'] = d.get('bibfile',f)    ### take a bibfile entry if present, else use the filename
			d['bibitem'] = bbl.get(d['citekey'],'')
			if selection(d) and d['bibitem']: dls += [d]
	dls.sort(comparison)
	dls1 = []
	count = 0
	for d in dls:
		count += 1
		d['count'] = str(count)
		dls1 += [d]
	return dls1
	
def comparison(d,e):
	return cmp(d,e)

def selection(d):
	#if d.get('YEAR','') in ['1965']: return 1
	if d.get('bibfile','').find('Zbl') >= 0: return 1
	else: return 0

def display(d): return '\\item[$\mbox{' + d['count'] + '}$] [' + d['bibfile'].split('/')[-1] + '/' + d['citekey'] + '] ' + d['bibitem'] + '\n\n'


def bibtex_to_json_service(cgi_fields):
	callback = ''
	response = {}
	bibstring = ''
	error = False
	if (not cgi_fields):
			print 'Content-type: text/plain \n\n',
			print 'Error: This service expects a bibtex string or url to a bibtex file (url=  or  document=)',	
	else:	   
		callback = cgi_fields.getfirst('callback')
		document = cgi_fields.getfirst('document')
		file = cgi_fields.getfirst('file')
		url = cgi_fields.getfirst('url')


		value_substitutions = {
			'{':'',
			'}':''
			}
		
		if (file):
			bibstring = open(file, "r").read()
		elif (url):
			bibstring = str(urllib2.urlopen(url).read())
		elif (document):
			bibstring = document	
			
		if (bibstring):
			bibstring = unicode(bibstring, errors='replace')
			response = read_bibstring(bibstring, value_substitutions)
			debug_info = {"params":''+'f: '+str(file) +'  u: '+str(url)+'  d: '+str(document)}	
	#		response.append(debug_info)
	#		if error:
	#			response['error'] = '' #urllib.quote_plus(cgi_fields.getfirst('params'))
		else:
			response = {
					"error":'no param values',
					"params":''+'f: '+str(file) +'  u: '+str(url)+'  d: '+str(document)}
	
		print 'Content-type: text/plain \n\n'
		if ('callback' in cgi_fields):	
			print callback+'('+simplejson.dumps(response)+')'
		else:
			print simplejson.dumps(response)

#if __name__ == "__main__":

#cgitb.enable()
cgi_fields = cgi.FieldStorage()    
if (cgi_fields):
    bibtex_to_json_service(cgi_fields)
#	print "Content-type: text/html"
#	print
#	print "Hello World"	
else:
	
#	params = {}
#	params['packages_line'] = '\\usepackage[utf8]{inputenc}'
#	params['refname'] = 'Publications related to J. F. C. Kingman'
#	params['bibliographystyle'] = 'plain'  
#	params['bibfnames'] = ','.join( [ f.replace('.bib','') for f in glob.glob('./bibfiles/*.bib')])
#	params['tmpfname'] = 'tmp_kingman'
#	params['outfname'] = 'kingman'
	#print make_all_files(params)
	#bbl = make_bbl(comparison,selection,display,params)
	#print bbl
	#os.popen('pdflatex ' + fname, "r").read()
	#print os.popen('pdflatex ' + fname, "r").read()
	#print last_names_first('')
	
	value_substitutions = {
		'{':'',
		'}':''
		}
	bibstring = open('temp.bib', "r").read()
	bibstring = unicode(bibstring, errors='replace')
	bibjson = read_bibstring(bibstring, value_substitutions)
	
	str(urllib2.urlopen('http://localhost/bkn/bibtex/temp.bib').read()).strip()
	print simplejson.dumps(bibjson, indent=2)
