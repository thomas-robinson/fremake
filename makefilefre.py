
class makefile():
## \brief Opens Makefile and sets the experiment and other common variables
 def __init__(self,exp):
     self.e = exp
     self.src = "/apps/"+self.e+"/src/"
     self.bld = "/apps/"+self.e+"/exec/"
     self.template = "/apps/mkmf/templates/hpcme-intel21.mk"
     self.c =[] #components
     self.r=[] #requires
     self.m=open("Makefile","w")
## \brief Adds a component and corresponding requires to the list
## \param self The Makefile object
## \param c The component
## \param r The requires for that componenet
 def addComponet (self,c,r):
     self.c.append(c)
     self.r.append(r)
## \brief Writes the Makefile.  Should be called after all components are added
## \param self The Makefile object
 def writeMakefile (self):
# Get the list of all of the libraries
     libstring=" "
     for lib in self.c:
          libstring = libstring+lib+"/lib"+lib+".a "
# Write the header information for the Makefile
     self.m.write("# Makefile for "+self.e+"\n")
     self.m.write("SRCROOT = "+self.src+"\n")
     self.m.write("BUILDROOT = "+self.bld+"\n")
     self.m.write("MK_TEMPLATE = "+self.template+"\n") 
     self.m.write("include $(MK_TEMPLATE)"+"\n")
# Write the main experiment compile 
     self.m.write(self.e+": "+libstring+"\n")
     self.m.write("\t$(LD) $^ $(LDFLAGS) -o $@ $(STATIC_LIBS)"+"\n")
# Write the individual component library compiles
     for (c,r) in zip(self.c,self.r):
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
