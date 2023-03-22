import yaml

srcDir="/apps"
## Class to create the checkout script
class checkout():
## \brief Opens the checkout script with the specified name
## \param self The checkout script object
## \param fname The file name of the checkout script
 def __init__(self,fname):
     self.fname = fname
     self.checkoutScript = open(fname, 'w')
     self.checkoutScript.write("#!/bin/sh -fx \n")
## \brief Wirtes the contents of the checkout script by looping through the input yaml
## \param self The checkout script object
## \param y The fremake compile yaml
 def writeCheckout(self,y):
   self.checkoutScript.write("cd  /apps/"+y["experiment"]+"/src \n")
   for c in y['src']:
     self.checkoutScript.write("echo cloning "+c['repo']+" -b "+c['branch']+" into "+srcDir+"/"+c['component']+"\n")
     if c['branch']=="":
          self.checkoutScript.write("git clone --recursive "+c['repo']+" "+c['component']+"\n")
     else:
          self.checkoutScript.write("git clone --recursive "+c['repo']+" -b "+c['branch']+" "+c['component']+"\n")
     if c['additionalInstructions']!="":
          self.checkoutScript.write(c['additionalInstructions'])
## \brief Closes the checkout script when writing is done
## \param self The checkout script object
 def finish (self):
     self.checkoutScript.close()
## \brief Changes the permission on the checkout script and runs it
## \param self The checkout script object
 def checkoutRun (self):
     os.chmod(srcDir+"/"+self.fname, 0o744)
     try:
          subprocess.run(args=["./"+srcDir+"/"+self.fname], check=True)
     except:
          print("There was an error with the checkout script "+checkoutScriptName)
          raise

