import os

class makefile():
## \brief Opens Makefile and sets the experiment and other common variables
## \param self The Makefile object
## \param mkTemplate The location of the template .mk file for compiling
 def __init__(self,exp,srcDir,bldDir,mkTemplate):
     self.e = exp
     self.src = srcDir 
     self.bld =  bldDir
     self.template = mkTemplate
     self.c =[] #components
     self.r=[] #requires
     os.system("mkdir -p "+self.bld)
     self.m=open(self.bld+"/Makefile","w")
## \brief Adds a component and corresponding requires to the list
## \param self The Makefile object
## \param c The component
## \param r The requires for that componenet
 def addComponet (self,c,r):
     self.c.append(c)
     self.r.append(r)
##\brief Sorts the component by how many requires there are for that component
##\param self The Makefile object
##\param c The component
##\param r The requires for that component
 def createLibstring (self,c,r):
     d=zip(self.c,self.r)
     return(sorted(d,key=lambda values:len(values[1]),reverse=True))
## \brief Writes the Makefile.  Should be called after all components are added
## \param self The Makefile object
 def writeMakefile (self):
# Get the list of all of the libraries
     sd=self.createLibstring(self.c,self.r)
     libstring=" "
     for i in sd:      
       lib=i[0]        
       libstring = libstring+lib+"/lib"+lib+".a "   
# Write the header information for the Makefile
     self.m.write("# Makefile for "+self.e+"\n")
     self.m.write("SRCROOT = "+self.src+"/\n")
     self.m.write("BUILDROOT = "+self.bld+"/\n")
     self.m.write("MK_TEMPLATE = "+self.template+"\n") 
     self.m.write("include $(MK_TEMPLATE)"+"\n")
# Write the main experiment compile 
     self.m.write(self.e+".x: "+libstring+"\n")
     self.m.write("\t$(LD) $^ $(LDFLAGS) -o $@ $(STATIC_LIBS)"+"\n")
# Write the individual component library compiles
     for (c,r) in sd:
          libstring = " "
          for lib in r:
               libstring = libstring+lib+"/lib"+lib+".a "
          cstring = c+"/lib"+c+".a: "
          self.m.write(cstring+libstring+" FORCE"+"\n")
          self.m.write("\t$(MAKE) SRCROOT=$(SRCROOT) BUILDROOT=$(BUILDROOT) MK_TEMPLATE=$(MK_TEMPLATE) --directory="+c+" $(@F)\n")
     self.m.write("FORCE:\n")
     self.m.write("\n")
# Set up the clean
     self.m.write("clean:\n")
     for c in self.c:
          self.m.write("\t$(MAKE) --directory="+c+" clean\n")
# Set up localize
     self.m.write("localize:\n")
     for c in self.c:
          self.m.write("\t$(MAKE) -f $(BUILDROOT)"+c+" localize\n")
# Set up distclean
     self.m.write("distclean:\n")
     for c in self.c:
          self.m.write("\t$(RM) -r "+c+"\n")
     self.m.write("\t$(RM) -r "+self.e+"\n")
     self.m.write("\t$(RM) -r Makefile \n")
## \brief closes the Makefile
## \param self The makefile object
 def finish(self):
     self.m.close()

## The makefile class for a container.  It gets built into a temporary directory so it can be copied
## into the container.
class makefileContainer(makefile):
 def __init__(self,exp,srcDir,bldDir,mkTemplate,tmpDir):
     self.e = exp
     self.src = srcDir 
     self.bld =  bldDir
     self.template = mkTemplate
     self.tmpDir = tmpDir
     self.c =[] #components
     self.r=[] #requires
     os.system("mkdir -p "+self.bld)
     self.m=open(self.tmpDir+"/Makefile","w")
## \return the tmpDir
## \param self The makefile object
 def getTmpDir(self):
     return self.tmpDir
