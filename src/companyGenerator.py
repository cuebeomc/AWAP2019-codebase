import random

class Company(object):
	def __init__(self, size):
		if size = 'S':
			self.size = 0
		else if size = 'M':
			self.size = 1;
		else if size = 'L':
			self.size = 2

		self.largeCompanies = [Amazon, 
						  	   AmazonRobotics,
						  	   Boeing,
						  	   Facebook,
						  	   Google,
						  	   Microsoft,
						  	   Oracle,
						  	   IBM,
						  	   INTEL,
						  	   Apple,
						  	   CiscoSystems,
						  	   Samsung,
						  	   GeneralMotors,
						  	   SAP	
		]

		self.mediumCompanies = [Linkedin,
						   	    Salesforce,
						   	    GoDaddy,
						   		Bloomberg,
						   		Battelle,
						   		Activision,
						   		Yelp,
						   		Uber,
						   		eBay,
						   		Adobe,
						   		NASA,
						   		Ctrip,
						   		Entergy,
						   		Nvidia,
						   		HudsonsBay,
						   		Playstation
		]

		self.smallCompanies = [Asana,
						  	   Citadel,
						  	   Slack,
						  	   Dropbox,
						  	   Mongo DB,
						  	   Duolingo,
						  	   Argo AI,
						  	   Pinterest,
						  	   Blend,
						  	   Niantic,
						  	   Datadog,
						  	   ContrastSecurity
		]

	def getCompany(self):
		if self.size == 0:
			return self.largeCompanies[random.randint(0, len(self.largeCompanies))]
		else if self.size == 1:
			return self.mediumCompanies[random.randint(0, len(self.mediumCompanies))]
		else:
			return self.smallCompanies[random.randint(0, len(self.smallCompanies))]





