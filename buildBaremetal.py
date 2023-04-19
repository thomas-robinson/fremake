#!/usr/bin/python3
## \date 2023
## \author Tom Robinson
## \email thomas.robinson@noaa.gov
## \description 

import subprocess
import os
import yaml

class buildBaremetal():
## \brief Creates the build script to compile the model
## \param self The buildScript object
## \param exp The experiment name
## \param mkTemplate The template used by mkmf to compile the model
## \param srcDir The source directory
## \param bldDir The build directory
## \param modules The list of modules to load before compilation
## \param modulesInit A list of commands with new line characters to initialize modules
 def __init__(self,exp,mkTemplate,srcDir,bldDir,modules,modulesInit):
     self.e = exp
     self.src = srcDir
     self.bld = bldDir
     self.mkmf = True
     self.template = mkTemplate
     self.modules = ""
     for m in modules:
          self.modules = self.modules +" "+ m
## Set up the top portion of the compile script
     self.setup=[   "#!/bin/sh -fx \n",
                    "bld_dir="+self.bld+"/ \n",
                    "src_dir="+self.src+"/ \n",
                    "mkmf_template="+self.template+" \n"]
     if self.modules != "":
          self.setup.extend(modulesInit) #extend because this is a list
          self.setup.append("module load "+self.modules+" \n") # Append because this is a single string
## Create the build directory
     os.system("mkdir -p "+self.bld)
## Create the compile script
     self.f=open(self.bld+"/compile.sh","w")
     self.f.writelines(self.setup)
## \brief Adds components to the build script
## \param self The build script object
## \param c Component from the compile yaml
 def writeBuildComponents(self, c):
# Shorthand for component
     comp = c["component"]
# Make the component directory
     self.f.write(" mkdir -p $bld_dir/"+comp+"\n")
# Get the paths needed for compiling
     pstring = ""
     for paths in c["paths"]:
          pstring = pstring+"$src_dir/"+paths+" "
# Run list_paths
     self.f.write(" list_paths -l -o $bld_dir/"+comp+"/pathnames_"+comp+" "+pstring+"\n")
     self.f.write(" cd $bld_dir/"+comp+"\n")
# Create the mkmf line
     if c["requires"] == [] and c["doF90Cpp"]: # If this lib doesnt have any code dependencies and it requires the preprocessor (no -o and yes --use-cpp)
          self.f.write(" mkmf -m Makefile -a $src_dir -b $bld_dir -p lib"+comp+".a -t $mkmf_template --use-cpp -c \""+c["cppdefs"]+"\" -IFMS/fms2_io/include -IFMS/include -IFMS/mpp/include -Imom6/MOM6-examples/src/MOM6/pkg/CVMix-src/include $bld_dir/"+comp+"/pathnames_"+comp+" \n")
     elif c["requires"] == []: # If this lib doesnt have any code dependencies (no -o)
          self.f.write(" mkmf -m Makefile -a $src_dir -b $bld_dir -p lib"+comp+".a -t $mkmf_template -c \""+c["cppdefs"]+"\" -IFMS/fms2_io/include -IFMS/include -IFMS/mpp/include -Imom6/MOM6-examples/src/MOM6/pkg/CVMix-src/include $bld_dir/"+comp+"/pathnames_"+comp+" \n")
     else: #Has requirements
#Set up the requirements as a string to inclue after the -o
          reqstring = ""
          for r in c["requires"]:
               reqstring = reqstring+"-I$bld_dir/"+r+" "
#Figure out if we need the preprocessor
          if c["doF90Cpp"]:
               self.f.write(" mkmf -m Makefile -a $src_dir -b $bld_dir -p lib"+comp+".a -t $mkmf_template --use-cpp -c \""+c["cppdefs"]+"\" -o \""+reqstring+"\" -IFMS/fms2_io/include -IFMS/include -IFMS/mpp/include -Imom6/MOM6-examples/src/MOM6/pkg/CVMix-src/include $bld_dir/"+comp+"/pathnames_"+comp+" \n")
          else:
               self.f.write(" mkmf -m Makefile -a $src_dir -b $bld_dir -p lib"+comp+".a -t $mkmf_template -c \""+c["cppdefs"]+"\" -o \""+reqstring+"\" -IFMS/fms2_io/include -IFMS/include -IFMS/mpp/include -Imom6/MOM6-examples/src/MOM6/pkg/CVMix-src/include $bld_dir/"+comp+"/pathnames_"+comp+" \n")
## Finishes and writes the build script
## \param self The buildScript object
##TODO: add targets input
 def writeScript(self):
     self.f.write("cd "+self.bld+"\n")
     #TODO add targets (DEBUG,REPRO,PROD and OPENMP)
     self.f.write("make -j 4 DEBUG=on \n")
     self.f.close()
## Run the build script
## \param self The dockerfile object
## TODO run as a batch job on the login cluster
 def run(self):
###### TODO make the Makefile
     os.chmod(self.bld+"/compile.sh", 0o744)
     command = [self.bld+"/compile.sh","|","tee",self.bld+"/log.compile"]
     try:
          subprocess.run(args=command, check=True)
     except:
          print("There was an error running "+self.bld+"/compile.sh")
          raise
 
