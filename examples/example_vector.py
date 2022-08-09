settings = {
    "wps": {
        # URL for Geoserver WPS service
        # it's enough to change host and port
        "url": "http://localhost:8080/geoserver/wps",
        # Local storage of GeoPackage files, must be writeable
        # The directory will be created if it does not exist.
        "file_storage": "/tmp/jrodoswps"
    },
    "rest": {
        # TOMCAT rest service URL
        "url": "http://localhost:8080/jrodos-rest-1.2-SNAPSHOT/jrodos"
    }
}

from dateutil.parser import parse
from datetime import datetime, timedelta

try:
    import mysettings
    settings = mysettings.settings
except ImportError:
    pass
  
try:
    from rodospy import *
except ImportError: 
    import sys, os.path
    sys.path.append(os.path.abspath('C:/Users/Sara/Source/Repos/samsarayg/rodospy'))
    sys.path.append(os.path.abspath('C:/Users/Sara/Source/Repos/samsarayg/rodospy/examples'))
    from rodospy import *

# set debug level logging
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.ERROR)

# create connection
rodos = RodosConnection( settings )
# list projects available
# filters can be used but they are not required
#projects = rodos.projects_old( )
projects = rodos.projects


# Choose the latest project where model chain is "LSMC+EMERSIM+DEPOM+FDMT"
#project = rodos.get_projects(filters={"modelchainname":
#                                      "Emergency"})[-1]
project = rodos.get_projects(filters={"uid":
                                      "6c13fbfa-ac15-415f-7daa-0fbde7e0185d"})[-1]
print(project)
# Get the only task and also for wind series 12 first timestemps and 10 vertical levels
task = project.get_tasks({},2,2)[0]

#print(task.mpp2adm_levelhght.times())
#print(task.mpp2adm_levelhght.levels())
#print(task.mpp2adm_levelhght.gridseries)
cell = None 
for key in task.mpp2adm_levelhght.gridseries:
    levelhght = task.mpp2adm_levelhght.gridseries[key]
    print ( key, levelhght.timeSeries(113.939,22.31) )
    if cell is None: 
        cell = levelhght.getCell(113.939,22.31)
    
# Print following wind field series is available
#print(project.startOfRelease, project.timestepOfPrognosis, project.durationOfPrognosis)
for wind_field in task.mpp2adm_wind.keys():
    value = task.mpp2adm_wind[wind_field].valueAtCell(cell)
    print(wind_field, value)
    #print ( project.startOfRelease + timedelta(seconds=project.timestepOfPrognosis * (value["time"] + 1)) , value )

if __name__=="__main__":
    print ( "Sample data loaded.")
