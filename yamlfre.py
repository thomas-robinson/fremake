import yaml

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
     
