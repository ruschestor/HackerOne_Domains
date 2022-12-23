### MAIN ###
# Name: 		HackerOne_Domains
# Description: 	Python module for getting a list of domains from HackerOne platform.
# Version: 		1.0 | Date: 23.12.2022
# GitHub: 		https://github.com/ruschestor/HackerOne_Domains

### TESTED ENVIRONMENT ###
# Windows 10 Enterprise 2016 LTSB 1607 | Python 3.10.4 | Pip 22.0.4 | wget 3.2 | 

### VARIABLES LEGEND ###
# g_ - GLOBAL variables
# t_ - TEMP variables
# s_ - STATISTIC variables
# f_ - FILES

### MODULES ###
import json
import os
import wget
from datetime import datetime

### VARIABLES ###
g_url = "https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/main/data/hackerone_data.json"
g_url_TLDS = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
g_blocked_domains = ["hackerone.com", "github.com","gitlab.com", "*.*"]
g_blocked_symbols = ["!","@","#","$","%","^","&","(",")",";",":",",","?","=","+","<",">"]
g_protocols = ["https://","http://","ftp://"]
g_target_domains = []
g_wildcard_domains = []
g_TLDS = []
s_number_scope = 0
s_number_scope_companies = 0

### FILES ###
f_temp_file_folder = "C:/temp/HackerOne_Domains/"
f_temp_file = f_temp_file_folder + "/HackerOne_Domains_" + str(datetime.now().strftime("%Y-%m-%d")) + ".json"			# Once per day
f_temp_file_top_level_domains = f_temp_file_folder + "/IANA_TLDS_" + str(datetime.now().strftime("%Y-%m")) + ".txt"		# Once per month
f_report = f_temp_file_folder + "results.txt"
os.makedirs(f_temp_file_folder, exist_ok=True)

def getdomainlist(mode = 'default', bounties = 'yes', swag = 'no', number = 0, start = 0, c_limit = 0):
	# MODE:
	#  'default' 	- Get clear list of domains
	#  'wildcard' 	- Get list of wildcard domains
	#  'statistics'	- Get statistics
	#
	# NUMBER:		- How many domains return
	#  0 			- Unlimited
	#
	# START			- Offset
	#
	# c_limit		- Number of first in-scope companies

	global s_number_companies
	global s_number_scope_companies
	global s_number_scope
	global g_target_domains
	global g_wildcard_domains
	global g_TLDS

	# Download HACKERONE domain list from GitHub (https://github.com/arkadiyt/bounty-targets-data)
	# Download only one file per day
	if not os.path.exists(f_temp_file):
		wget.download(g_url, f_temp_file)

	# Download TLDS file only one file per month
	if not os.path.exists(f_temp_file_top_level_domains):
		wget.download(g_url_TLDS, f_temp_file_top_level_domains)

	# Reading TLDS file
	with open(f_temp_file_top_level_domains, 'r') as t_f2:
		t_TLDS = t_f2.read().splitlines(True)[:-1]
		t_TLDS = t_TLDS[1:]
		for i in t_TLDS:
			g_TLDS.append(i.strip())
	t_f2.close()

	# Reading JSON source file
	#print("Temp file = ", f_temp_file)
	with open(f_temp_file, "r", encoding='utf-8') as t_f:
		t_json_raw = json.load(t_f)
	t_f.close()

	s_number_companies = len(t_json_raw)

	for i in range(s_number_companies):

		# Filter by "submission_state" = "open"
		t_json_submission_state = t_json_raw[i]['submission_state']
		if t_json_submission_state != "open":
			continue

		# Filter company by "offers_bounties" option in account
		t_json_offers_bounties = t_json_raw[i]['offers_bounties']
		if (bounties == "yes") and (t_json_offers_bounties is False):
			continue

		# Filter company by "offers_swag" option in account
		t_json_offers_swag = t_json_raw[i]['offers_swag']
		if (swag == "yes") and (t_json_offers_swag is False):
			continue

		# Limit number of first companies
		if (s_number_scope_companies > c_limit-1) and (c_limit != 0):
			continue
		s_number_scope_companies += 1

		t_json_raw_company = t_json_raw[i]['targets']['in_scope']

		for j in range(len(t_json_raw_company)):
			s_number_scope += 1
			if t_json_raw_company[j]['asset_type'] != 'URL':
				continue

			t_json_raw_domain = t_json_raw_company[j]['asset_identifier']

			# Cut URL and protocol
			if "/" in t_json_raw_domain:

				# Cut protocol (HTTP, HTTPS)
				for k in g_protocols:
					if k in t_json_raw_domain:
						t_json_raw_domain = t_json_raw_domain[len(k):]

				# Cut URL
				t_pos = t_json_raw_domain.find("/")
				if t_pos != -1:
					t_json_raw_domain = t_json_raw_domain[:-(len(t_json_raw_domain)-t_pos)]

			# Check top-level domain
			t_i = (t_json_raw_domain.split("."))[-1].upper()
			if (t_i not in g_TLDS):
				continue

			# Exclude blocked (we shouldn't check them) domains
			if t_json_raw_domain in g_blocked_domains:
				continue

			# Check wildcard
			if "*" in t_json_raw_domain:
				g_wildcard_domains.append(t_json_raw_domain)

				# Cut first "*." | Examples: *.platfoo.com"
				if t_json_raw_domain[:2] == "*.":
					t_json_raw_domain = t_json_raw_domain[2:]

				# Skip "*." | Example: "paypal-*.com"
				if "*." in t_json_raw_domain:
					continue

				# Cut first "*" | Examples: "*deere.com", "*jdisonline.com"
				if t_json_raw_domain[0] == "*":
					t_json_raw_domain = t_json_raw_domain[1:]

				# Skip ".*" | Examples: "www.*mongodb.com", "sothebysrealty.*"
				if ".*" in t_json_raw_domain:
					continue

			# Cut the last dot (".") in the domain
			if t_json_raw_domain[-1] == ".":
				t_json_raw_domain = t_json_raw_domain[:-1]

			# Skip non-domain = without "."
			if "." not in t_json_raw_domain:
				continue

			# Exclude domains with blocked characters
			t_skip = 0
			for m in g_blocked_symbols:
				if m in t_json_raw_domain:
					t_skip = 1
			if t_skip == 1:
				continue

			# Exclude duplicates
			if t_json_raw_domain in g_target_domains:
				continue

			g_target_domains.append(t_json_raw_domain.strip().lower())

	match mode:
		case 'default':
			if number == 0:
				return g_target_domains
			else:
				t_slice = slice(start,start+number)
				t_slice_list = g_target_domains[t_slice]
				return t_slice_list

		case 'wildcard':
			return g_wildcard_domains

		case 'statistics':
			t_result = []
			s_number_targets = len(g_target_domains)
			s_number_wilcard = len(g_wildcard_domains)
			print("Number of companies:", s_number_companies)
			print("Number of in-scope companies:", s_number_scope_companies)
			print("Number of in-scope objects:", s_number_scope)
			print("Number of real in-scope domains:", s_number_targets)
			print("Number of wildcard domains:", s_number_wilcard)
			t_result.append("Number of companies: " + str(s_number_companies))
			t_result.append("Number of in-scope companies: " + str(s_number_scope_companies))
			t_result.append("Number of in-scope objects: " + str(s_number_scope))
			t_result.append("Number of real in-scope domains: " + str(s_number_targets))
			t_result.append("Number of wildcard domains: " + str(s_number_wilcard))
			return t_result

# START #
if __name__ == '__main__':
	result = getdomainlist()

	# Export result to the file. Just for tests.
	t_a = '\n'.join(result)
	with open(f_report,"w") as t_file:
		t_file.write(t_a)
	t_file.close()