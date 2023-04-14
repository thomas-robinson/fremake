import os
import yaml
import subprocess

def writeRepo(file,repo,component,srcDir,branch,add,multi):
## Write message about cloning repo and branch in component
     file.write("echo cloning "+repo+" -b "+branch+" into "+srcDir+"/"+component+"\n")
## If this component has multiple repos, clone everything in the component folder
## If it's not multi, then use the component name (comp) as the folder name to clone into
     if multi:
          file.write("mkdir -p "+component+"\n")
          file.write("cd "+component+"\n")
          comp=""
     else:
          comp=component
## Check if there is a branch/version and then write the clone line
     if branch=="":
          file.write("git clone --recursive "+repo+" "+comp+"\n")
     else:
          file.write("git clone --recursive "+repo+" -b "+branch+" "+comp+"\n")
## Make sure to go back up in the folder structure
     if multi:
          file.write("cd .. \n")
     if add!="":
          file.write(add)


## Class to create the checkout script
class checkout():
## \brief Opens the checkout script with the specified name
## \param self The checkout script object
## \param fname The file name of the checkout script
## \param srcDir The source directory where fname will be run and source will exist
 def __init__(self,fname,srcDir):
     self.fname = fname
     self.src = srcDir
     os.system("mkdir -p "+self.src)
     os.system("rm -rf "+self.src+"/*")
     self.checkoutScript = open(self.src+"/"+fname, 'w')
     self.checkoutScript.write("#!/bin/sh -fx \n")
## \brief Wirtes the contents of the checkout script by looping through the input yaml
## \param self The checkout script object
## \param y The fremake compile yaml
 def writeCheckout(self,y):
   self.checkoutScript.write("cd  "+self.src +"\n")
   for c in y['src']:
     if type(c['repo']) is list and type(c['branch']) is list:
          for (repo,branch) in zip(c['repo'],c['branch']):
               writeRepo(self.checkoutScript,repo,c['component'],self.src,branch,c['additionalInstructions'],True)
     else:
          writeRepo(self.checkoutScript,c['repo'],c['component'],self.src,c['branch'],c['additionalInstructions'],False)
#          self.checkoutScript.write("echo cloning "+c['repo']+" -b "+c['branch']+" into "+srcDir+"/"+c['component']+"\n")
#          if c['branch']=="":
#               self.checkoutScript.write("git clone --recursive "+c['repo']+" "+c['component']+"\n")
#          else:
#               self.checkoutScript.write("git clone --recursive "+c['repo']+" -b "+c['branch']+" "+c['component']+"\n")
#     if c['additionalInstructions']!="":
          self.checkoutScript.write(c['additionalInstructions'])
## \brief Closes the checkout script when writing is done
## \param self The checkout script object
 def finish (self):
     self.checkoutScript.close()
## \brief Changes the permission on the checkout script and runs it
## \param self The checkout script object
 def run (self):
     os.chmod(self.src+"/"+self.fname, 0o744)
     try:
          subprocess.run(args=[self.src+"/"+self.fname], check=True)
     except:
          print("There was an error with the checkout script "+checkoutScriptName)
          raise

