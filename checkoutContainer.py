import yaml
from yamlfre import *
from checkout import *
## This container class handles the checking, creation, and running of the code checkout script
## for fremake
class checkoutContainer():
 checkoutScriptName = "checkout.sh"
## Open and check the yaml for the compile
## \param self The compile object
## \param compileYaml The name of the compile yaml file
 def __init__(self,compileYaml):
     ## Open the yaml file and parse as self.yaml
     self.yaml = parseCompile(compileYaml)
     ## Check the yaml for required things
     ## Check for required experiment name
     try:
          self.yaml["experiment"]
     except:
          print("You must set an experiment name to compile \n")
          raise
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
## Writes and closes the checkout script
## \param self The compile object
 def writeCheckout(self):
     checkoutScript = checkout(self.checkoutScriptName)
     checkoutScript.writeCheckout(self.yaml)
     checkoutScript.finish()
## Runs the checkout script
## \param self The compile object
 def run(self):
     checkoutScript.checkoutRun()
