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


def convertData(input_dir, output_dir):
	import os
	for root, dirs, files in os.walk(input_dir):
		for file in files:
			if file.endswith('.xml'):
				fileName = input_dir+'/'+file
				input_file = open(fileName, 'r')
				input_read = input_file.read()
				input_file.close()
				#input_read = html_escape(input_read)
				fileName = input_dir+'/__tmp__/'+file
				output_file = open(fileName, 'w')
				input_conv = input_read.replace('<?xml version="1.0" encoding="UTF-8" standalone="no"?>', '<?xml version="1.0" encoding="UTF-8"?>')
				input_conv = input_conv.replace('<data>', '<add> <doc>')
				input_conv = input_conv.replace('</data>', '</doc> </add>')
				input_conv = input_conv.replace('<number>', '<field name="id">')
				input_conv = input_conv.replace('</number>', '</field>')
				input_conv = input_conv.replace('<question>', '<field name="text_hangul">')
				input_conv = input_conv.replace('</question>', '</field>')
				input_conv = input_conv.replace('<answer>', '<field name="text_hangul">')
				input_conv = input_conv.replace('</answer>', '</field>')
				output_file.write(input_conv)
				output_file.close()
				# 결과 화면 출력
				#print input_conv


def insertData(output_dir):
	import subprocess
	subprocess.call(['./.post.sh', output_dir+'/*'])


def removeData(output_dir):
	import os
	for root, dirs, files in os.walk(output_dir):
		for name in files:
			os.remove(os.path.join(root, name))
		for name in dirs:
			os.rmdir(os.path.join(root, name))
		os.rmdir(output_dir)

def main():
	import sys
	import os
	if len(sys.argv) < 2:
		print "Usage: 2.insertData.py <inputDirectory>"
	else:
		input_dir = sys.argv[1]
		output_dir = input_dir+'/__tmp__'
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)
		
		convertData(input_dir, output_dir)
		insertData(output_dir)
		removeData(output_dir)


if __name__ == "__main__":
	import sys
	sys.exit(main())
	pass
