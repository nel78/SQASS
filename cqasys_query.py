#!/usr/bin/python
# -*- coding:utf-8 -*-

from xml.sax.saxutils import escape, unescape
# escape() and unescape() takes care of &, < and >.
html_escape_table = {
    '"': "&quot;",
    "'": "&apos;"
}
html_unescape_table = {v:k for k, v in html_escape_table.items()}

def html_escape(text):
    return escape(text, html_escape_table)


def queryConvert(input_fileName):
	import os
	import re
	import urllib
	query_list = []
	query=[]
	input_file = open(input_fileName, 'r')
	input_read = input_file.read()
	input_file.close()
	#input_read = html_escape(input_read)
	if(re.search(r'<qnum>\s*(.+)\s*</qnum>', input_read)):
		number = re.findall(r'<qnum>(.+)</qnum>', input_read)
	if(re.search(r'<text>\s*(.+)\s*</text>', input_read)):
		pre_query = re.findall(r'<text>\s*(.+)\s*</text>', input_read)
		for line in pre_query:
			query.append(urllib.quote(line))
			
	if(len(number) == len(query)):
		for item in number:
			local_list = []
			local_list.append(item)
			query_list.append(local_list)
			#print item
		num = 0
		for item in query:
			query_list[num].append(item)
			num += 1
			#print urllib.unquote(item)
	else:
		sys.stderr.write('Query mismatch1..\n')
		exit()
	return query_list


def doQuery(query_list, maxNum):
	import urllib
	import re
	ids = 0
	scores = 0
	for item in query_list:
		query = item[1]
		#print 'http://localhost:8983/solr/collection1/select?q=text_hangul%3A'+query+'&rows='+maxNum+'&fl=id%2C+score%2C+text_hangul&wt=xml'
		input_file = urllib.urlopen('http://localhost:8983/solr/collection1/select?q=text_hangul%3A'+query+'&rows='+maxNum+'&fl=id%2C+score%2C+text_hangul&wt=xml')
		result = input_file.read()
		input_file.close()
		
		if(re.search(r'<str name="id">(\d+)</str>', result)):
			ids = re.findall(r'<str name="id">(\d+)</str>', result)
			item.append(ids)
		else:
			item.append([])
		if(re.search(r'<float name="score">(\S+)</float>', result)):
			scores = re.findall(r'<float name="score">(\S+)</float>', result)
			item.append(scores)
		else:
			item.append([])
	#print query_list 

def resultConvert(query_list):
	for query in query_list:
		queryNum = query[0]
		result_list = []
		if(len(query[2]) == len(query[3])):
			for item in query[2]:
				local_list = []
				local_list.append(item)
				result_list.append(local_list)
			num = 0
			for item in query[3]:
				result_list[num].append(item)
				num += 1
		else:
			sys.stderr.write('Query mismatch2..\n')
			exit()

		print '<query><qnum>'+queryNum+'</qnum>'
		print '<rank>'
		for item in result_list:
			print item[0]+'\t',
			print float(item[1])*100
		print '</rank>'
		print '</query>'
			

def main():
	import sys
	import os
        if len(sys.argv) < 3:
		print "Usage: 3.queryResult.py <query file> <result number>"
        else:
		input_fileName = sys.argv[1]
		maxNum = sys.argv[2]
		query_list = queryConvert(input_fileName)
		doQuery(query_list, maxNum)
		resultConvert(query_list)
		#print query_list


if __name__ == "__main__":
        import sys
        sys.exit(main())
        pass

