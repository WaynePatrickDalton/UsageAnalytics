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

# Adding the DynamoRevitDS.dll module to work with the Dynamo API
clr.AddReference('DynamoRevitDS')
import Dynamo

# Adding System details & Iron Python 2.7 Library
import sys

sys.path.append("C:\Program Files (x86)\IronPython 2.7\Lib")

# Adding the Operating System Details
import os
from datetime import datetime

# Access to the current Dynamo instance and workspace
dynamoRevit = Dynamo.Applications.DynamoRevit()
currentWorkspace = dynamoRevit.RevitDynamoModel.CurrentWorkspace

# Access current version of dynamo
version = dynamoRevit.RevitDynamoModel.Version

# checks version of dynamo and adjusts output according to version
if version.StartsWith("1."):

    # Gets file name which includes full path
    filename = currentWorkspace.FileName

    # Splits out file path to just file name
    dynamo_file_name = filename.Split("\\")[-1].Replace(".dyn", "")

elif version.StartsWith("2."):
    dynamo_file_name = currentWorkspace.Name

else:
    dynamo_file_name = "Not supported"

# Access exact date & time the script was ran
date_ran = datetime.now().strftime("%Y,%m,%d,%H,%M")

# Access exact date the script was ran
script_user = os.getenv('username')

# Access exact date the script was ran
computer_name = os.environ['COMPUTERNAME']

output_path = r"C:\Temp\UsageAnalytics.csv"

log = "{},{},{},{}\n".format(date_ran, script_user, computer_name, dynamo_file_name)

with open(output_path, 'a') as csv_file:
    csv_file.write(log)

OUT = "Dynamo Usage Analytics Logged!"