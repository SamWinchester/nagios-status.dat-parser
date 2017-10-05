#!/usr/bin/python
import sys
import re

servicename = ''#mention the service name here

def parseConf(filename):
    conf = []
    with open(filename, 'r') as f:
        for i in f.readlines():
            if i[0] == '#': continue
            matchID = re.search(r"([\w]+) {", i)
            matchAttr = re.search(r"[ ]*([\w]+)=([\w\d].*)", i)
            matchEndID = re.search(r"[ ]*}", i)
            if matchID:
                identifier = matchID.group(1)
                cur = [identifier, {}]
            elif matchAttr:
                attribute = matchAttr.group(1)
                value = matchAttr.group(2)
                cur[1][attribute] = value
            elif matchEndID:
                conf.append(cur)
    return conf
 

def datparser(filename):
    conf = parseConf(filename)
    output_dict={}	
    for ID in conf:
	if ID[0]!='servicestatus' : continue
	if ID[1]['service_description']==servicename  and not(ID[1]['plugin_output'].startswith('OK')):
		if not ID[1]['plugin_output'] in output_dict :
			output_dict[ID[1]['plugin_output']]=[]
			output_dict[ID[1]['plugin_output']].append(ID[1]['host_name'])
		else :
			output_dict[ID[1]['plugin_output']].append(ID[1]['host_name'])
    return output_dict

def main () :
	output = datparser('/var/log/nagios/status.dat')
	if output :
		for key, value in output.iteritems() :
			print 'ERROR MESSAGE : '+key
			print 'HOST LIST : '
			for val in value :
				print val
			print " "
		sys.exit(2)
	else : 
		return 0

if __name__ == "__main__": 
	main()

