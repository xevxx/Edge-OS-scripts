import json
import socket
import os

s_cfg_path = '/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper'
s_rule_names = []
pihole = {'rules':[]}
adguard = {'rules':[]}
dictToCheck = {'pihole':'IP ADDRESS','adguard':'IP ADDRESS'}

def get_config_object(s_config):
	s_out = '{'
	i_current_indent = -1
	i_multiplyer = 4
	for s_line in s_config.splitlines():
		s_striped_line = s_line.strip(' ')
		i_spaces = len(s_line) - len(s_striped_line)
		i_loop_indent = i_spaces / i_multiplyer

		if i_loop_indent == i_current_indent and b_object_has_data:
			s_out += ','

		if s_striped_line[-1:] == '{': #is object start
			b_object_has_data = False
			s_out += '"'+s_striped_line[:-2].strip('"')+'":{'

		elif s_striped_line[-1:] == '}': #is object end
			b_object_has_data = True
			s_out += '}'

		else :# is property#
			b_object_has_data = True
			tmp = s_striped_line.split(' ', 1)
			if len(tmp) == 1:
				tmp.append('"true"')
			s_out += '"'+tmp[0]+'":'+json.dumps(tmp[1].strip('"'))

		i_current_indent = i_loop_indent
	s_out += '}'
	#print out
	return json.loads(s_out)

def runRule(rule,up):
    if rule['disabled'] and up:
        os.system(s_cfg_path+' begin')
        os.system(s_cfg_path+' delete service nat ' + rule['ruleName'] + ' disable')
        os.system(s_cfg_path+' commit')
        os.system(s_cfg_path+' end')
    elif not rule['disabled'] and not up:
        os.system(s_cfg_path+' begin')
        os.system(s_cfg_path+' set service nat ' + rule['ruleName'] + ' disable')
        os.system(s_cfg_path+' commit')
        os.system(s_cfg_path+' end')

def runApp():
    f_handle = os.popen(s_cfg_path+ ' show')
    s_config = f_handle.read()
    # get the config as an object
    o_config = get_config_object(s_config)
    # find the right nat rule
    for rule, value in o_config['service']['nat'].iteritems():
        if 'source' in value:
            if 'group' in value['source']:
                if 'address-group' in value['source']['group']:
                    if value['source']['group']['address-group'] == 'REPLACE WITH GROUP NAME':
                        dict = {'ruleName':rule,'disabled':False}
                        if 'disable' in value:
                            dict['disabled'] = True
                        adguard['rules'].append(dict)
                    elif value['source']['group']['address-group'] == 'REPLACE WITH GROUP NAME':
                        dict = {'ruleName':rule,'disabled':False}
                        if 'disable' in value:
                            dict['disabled'] = True
                        pihole['rules'].append(dict)

    piholeUp  = True if os.system("ping -c 1 " + dictToCheck['pihole']) is 0 else False
    adGuardUp  = True if os.system("ping -c 1 " + dictToCheck['adguard']) is 0 else False


    for rule in pihole['rules']:
        runRule(rule,piholeUp)

    for rule in adguard['rules']:
        runRule(rule,adGuardUp)

runApp()




