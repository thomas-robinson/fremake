import subprocess
import os
import yaml
from yamlfre import *



class platforms ():
 def __init__(self,fname):
     self.yaml=parseCompile(fname)
## Check the yaml for errors/omissions
     try:
          self.yaml["platforms"]
     except:
          print(fname+" must have a platforms key\n")
          raise
## Loop through the platforms
     for p in self.yaml["platforms"]:
## Check the platform name
          try:
               p["name"]
          except:
               print("At least one of the platforms is missing a name in "+fname+"\n")
               raise
## Check the compiler
          try:
               p["compiler"]
          except:
               print ("You must specify a compiler in your "+p["name"]+" platform in the file "+fname+"\n")
               raise
## Check for the Fortran (fc) and C (cc) compilers
          try:
               p["fc"]
          except:
               print ("You must specify the name of the Fortran compiler as fc on the "+p["name"]+" platform in the file "+fname+"\n")
               raise
          try:
               p["cc"]
          except:
               print ("You must specify the name of the Fortran compiler as cc on the "+p["name"]+" platform in the file "+fname+"\n")
               raise
## Check for modules to load
          try:
               p["modules"]
          except:
               p["modules"]=[""]
## Check for modulesInit to set up the modules environment
          try:
               p["modulesInit"]
          except:
               p["modulesInit"]=[""]
## Get the root for the build
          try:
               p["modelRoot"]
          except:
               p["modelRoot"] = "/apps"
## Check if we are working with a container and get the info for that
          try:
               p["container"]
          except:
               p["container"] = ""
               p["containerBuild"] = ""
               p["containerRun"] = ""
          if p["container"] != "" :
## Check the container builder
               try:
                    p["containerBuild"]
               except:
                    print ("You must specify the program used to build the container (containerBuild) on the "+p["name"]+" platform in the file "+fname+"\n")
                    raise
               if p["containerBuild"] != "podman":
                    raise ValueError("Container builds only supported with docker or podman, but you listed "+p["containerBuild"]+"\n")
## Check the container runner
               try:
                    p["containerRun"]
               except:
                    print ("You must specify the program used to run the container (containerRun) on the "+p["name"]+" platform in the file "+fname+"\n")
                    raise
               if p["containerRun"] != "apptainer":
                    raise ValueError("Container builds only supported with apptainer, but you listed "+p["containerRun"]+"\n")
## set the location of the mkTemplate.  In a container, it uses the hpc-me template cloned from mkmf
               p["mkTemplate"] = "/apps/mkmf/templates/hpcme-intel21.mk"
          else:
               try:
                    p["mkTemplate"]
               except:
                    raise ValueError("The non-container platform "+p["name"]+" must specify a mkTemplate \n")
 def getPlatformFromName(self,name):
     for p in self.yaml["platforms"]:
          if p["name"] == name:
               return (p["compiler"], p["modules"], p["modulesInit"], p["fc"], p["cc"], p["modelRoot"],p["container"], p["mkTemplate"],p["containerBuild"], p["containerRun"])
