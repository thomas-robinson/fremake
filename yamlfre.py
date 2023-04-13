import yaml
from platform import *

## Open the yaml file and parse as fremakeYaml
## \param fname the name of the yaml file to parse
def parseCompile(fname):
## Open the yaml file and parse as fremakeYaml
     with open(fname, 'r') as file:
          y = yaml.safe_load(file)
     file.close()
     return y 
## \brief Checks the yaml for variables.  Required variables will dump and error.  Non-required variables will 
## set a default value for the variable
## \param var A variable in the yaml
## \param val a default value for var
## \param req if true, the variable is required in the yaml and an exception will be raised
## \param err An error message to print if the variable is required and doesn't exist
def yamlVarCheck(var,val="",req=False,err="error"):
     try:
          var
     except:
          if req:
               print (err)
               raise
          else:
               var = val
## This will read the compile yaml for FRE and then fill in any of the missing non-required variables
class compileYaml():
## Read get the compile yaml and fill in the missing pieces
 def __init__(self,yamlFile):
     self.file = yamlFile
     self.yaml = parseCompile(self.file)
          ## Check the yaml for required things
     ## Check for required experiment name
     try:
          self.yaml["experiment"]
     except:
          print("You must set an experiment name to compile \n")
          raise
#     ## Set up the srcDir
#     self.src = modelRoot + "/" + self.yaml["experiment"] + "/src"
     ## Check for required src
     try:
          self.yaml["src"]
     except:
          print("You must set a src to specify the sources in "+self.yaml["experiment"]+"\n")
          raise
     ## Loop through the src array
     for c in self.yaml['src']:
     ## Check for required componenet name
          try:
               c['component']
          except:
               print("You must set the 'componet' name for each src component")
               raise
     ## Check for required repo url
          try:
               c['repo']
          except:
               print("'repo' is missing from the component "+c['component']+" in "+self.yaml["experiment"]+"\n")
               raise
     # Check for optional branch. Otherwise set it to blank
          try:
               c['branch']
          except:
               c['branch']=""
     # Check for optional cppdefs. Otherwise set it to blank
          try:
               c['cppdefs']
          except:
               c['cppdefs']=""
     # Check for optional doF90Cpp. Otherwise set it to False
          try:
               c['doF90Cpp']
          except:
               c['doF90Cpp']=False
     # Check for optional additional instructions. Otherwise set it to blank
          try:
               c['additionalInstructions']
          except:
               c['additionalInstructions']=""
     # Check for optional paths. Otherwise set it to blank
          try:
               c['paths']
          except:
               c['paths']=[c['component']]
     # Check for optional requires. Otherwise set it to blank
          try:
               c['requires']
          except:
               c['requires']=[]
## Returns the compile yaml
 def getCompileYaml(self):
     try:
          self.yaml
     except:
          print ("You must initialize the compile YAML object before you try to get the yaml \n")
          raise
     return self.yaml

#########################################################################################################################
## \description This will take the models yaml file which has a list of the sub yaml files and combine them into the 
## full freyaml that can be used and checked
# platformYaml: platforms.yaml
# layoutYaml:
# compileYaml: compile.yaml
# experiments:

class freyaml():
 def __init__(self,modelFileName):
     self.freyaml = {}
     self.modelfile = modelFileName
     with open(self.modelfile, 'r') as file:
          self.modelyaml = yaml.safe_load(file)
     file.close()
     self.compilefile = self.modelyaml["compileYaml"]
     self.compile = compileYaml(self.compilefile)
     self.compileyaml = self.compile.getCompileYaml()
     self.freyaml.update(self.compileyaml)
     self.platformsfile = self.modelyaml["platformYaml"]
     self.platforms = platforms(self.platformsfile)
     self.platformsyaml = self.platforms.getPlatformsYaml()
     self.freyaml.update(self.platformsyaml)
     print(self.freyaml["experiment"])
     print(self.freyaml["platforms"])
#     self.platformyaml = 

