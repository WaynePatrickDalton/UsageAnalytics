"""
Hello there :)
This user analytics code originated from the UK Dynamo User Group (@UKDynUG) meeting in London 19.02.19
- tips and tricks session from Oliver Green (@Oliver_E_Green) from AHMM.
The origional autors of using reflection to obtain the current Dynamo instance from the Revit instance is:
John Pierson (@60secondrevit) & Brendan Cassidy (@brencass86)
accessed from: https://github.com/Amoursol/dynamoPython/blob/master/dynamoAPI/dynamoAPICurrentGraphName.py
I have just stuck these aspects together and added some notes, ^^ these guys have done all the heavy lifting ^^
- enjoy!
Wayne (@waynepdalton)
"""

# Importing Reference Modules
# CLR ( Common Language Runtime Module )
import clr

# Adding System details & Iron Python 2.7 Library
import sys

sys.path.append("C:\Program Files (x86)\IronPython 2.7\Lib")

# Adding the Operating System Details
import os
from datetime import datetime

#This should capture if this script is run outside of a dynamo instance running from revit
try:

	# Adding the DynamoRevitDS.dll module to work with the Dynamo API
	clr.AddReference('DynamoRevitDS')
	import Dynamo


	# Import DocumentManager and TransactionManager
	clr.AddReference("RevitServices")
	import RevitServices
	from RevitServices.Persistence import DocumentManager
	
	uiapp = DocumentManager.Instance.CurrentUIApplication
	app = uiapp.Application
	
	#Get application information
	revitVersion = app.VersionName
	revitBuild = app.VersionBuild
	
	# Access to the current Dynamo instance and workspace
	dynamoRevit = Dynamo.Applications.DynamoRevit()
	currentWorkspace = dynamoRevit.RevitDynamoModel.CurrentWorkspace
	
	# Access current version of dynamo
	dynamoversion = dynamoRevit.RevitDynamoModel.Version
	
	# checks version of dynamo and adjusts output according to version
	if dynamoversion.StartsWith("1."):
	
	    # Gets file name which includes full path
	    filename = currentWorkspace.FileName
	
	    # Splits out file path to just file name
	    dynamo_file_name = filename.Split("\\")[-1].Replace(".dyn", "")
	
	elif dynamoversion.StartsWith("2."):
	    dynamo_file_name = currentWorkspace.Name
	
	else:
	    dynamo_file_name = "Not supported"
	    
	# Adds check to make sure it will only run if dynamo version starts with 1 or 2
	if dynamo_file_name != "Not supported":
	 
		# Access exact date & time the script was ran
		date_ran = datetime.now().strftime("%Y,%m,%d,%H,%M")
		
		# Access exact date the script was ran
		script_user = os.getenv('username')
		
		# Access exact date the script was ran
		computer_name = os.environ['COMPUTERNAME']
		
		output_path = r"C:\Temp\UsageAnalytics.csv"
		
		
		# Gathers data for csv file from checks above
		log = "{},{},{},{},{},{},{}\n".format(date_ran, script_user, computer_name, dynamoversion, revitVersion, revitBuild, dynamo_file_name)
		
		# Title for CSV File
		csv_title="Year, Month, Day, House, Minute, UserName, ComputerName, DynamoVersion, RevitVersion, RevitBuild, DynamoFile\n"
		
		#Checks is csv file already exists
		
		#If it does exists it just adds a new line
		if os.path.isfile(output_path):
			with open(output_path, 'a') as csv_file:
				csv_file.write(log)
		
		#If it does not exists it adds titles into files
		else:
			with open(output_path, 'a') as csv_file:
				csv_file.write(csv_title+log)
	   
		OUT = "Dynamo Usage Analytics Logged!"
	
	# Addes output that this tool is
	else:
		OUT = "Current version of dynamo(Ver " + version + " ) is not supported by this analytics tool"
except:
	OUT = "This Usage data script has been created to run in a version of dynamo associated with revit only"
