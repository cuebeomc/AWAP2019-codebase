import sys
import random

# takes any #name #size #...data
# generates values where 
values = {
'S' : (20, 40),
'M' : (30, 50),
'L' : (40, 60),
'XL' : (50, 70)
}

sponsors = """
BAM
Dropbox
Nutanix
SandiaLabs
Google
DEShaw
GSK
Aptiv
Oracle
RiotGames
Bloomberg
Citadel
Siemens
GM
LiquidNet
"""

raw_companies = """
Amazon L
AmazonRobotics L
Boeing L
Facebook L
Google L
Microsoft L
Oracle L
IBM L
Intel L
Apple L
CiscoSystems L
Samsung L
GeneralMotors L
SAP L
Linkedin M
Salesforce M
GoDaddy M
Bloomberg M
Battelle M
Activision M
Yelp M
Uber M
eBay M
Adobe M
NASA M
Ctrip M
Entergy M
Nvidia M
HudsonsBay M
Playstation M
Asana S
Citadel S
Slack S
Dropbox S
MongoDB S
Duolingo S
ArgoAI S
Pinterest S
Blend S
Niantic S
Datadog S
ContrastSecurity S
BAM S 17
Dropbox M 12
Nutanix M 19
Sandia L 24
Google L 27
DEShaw M 16
GSK L 32
Aptiv L 14
Oracle L 28
RiotGames M 31
Bloomberg L 20
Citadel M 23
Siemens L 34
GM L 18
LiquidNet S
MongoDB M 10
HBO L 20
Neflix L 26
Tesla L 24
MemSQL S 15
Tinder S 15
JaneStreet S 22
Squarespace S 13
Affirm S 17
Palantir M 15 
TwoSigma M 22
"""

if len(sys.argv) < 2:
	print("Usage: Provide a file for you to write into")
	sys.exit(0)

sponsors_list = set(filter(lambda x: len(x) > 0, sponsors.split('\n')))

new_companies = {}
print("Num original companies", len(raw_companies.split('\n')))
for company in raw_companies.split('\n'):
	parts = company.split(' ')
	if len(parts) < 2:
		continue
	new_companies[parts[0]] = parts[1]

for sponsor in sponsors_list:
	new_companies[sponsor] = "XL"

new_companies_list = []
for company in new_companies.keys():
	new_companies_list.append((company, new_companies[company]))

new_companies_list = sorted(new_companies_list)

print("Num unique companies  ", len(new_companies_list))

def get_value(size):
	if not size in values:
		return 0
	(min_a, max_a) = values[size]
	return random.randint(min_a, max_a)

def adj_size(size):
	if size == "XL":
		return "L"
	return size

with open(sys.argv[1], "w+") as f:
	for company, size in new_companies_list:
		f.write("{} {} {}\n".format(company, adj_size(size), get_value(size)))