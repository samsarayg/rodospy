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
import pandas as pd

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


print("==== Start %s ===="% datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

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
                                      "808241fd-ac15-415f-7daa-0fbdfa70c60e"})[-1]
print(project)
# Get the only task and also for wind series 12 first timestemps and 10 vertical levels
task = project.get_tasks({},72,20)[0]
print(project.startOfRelease, project.timestepOfPrognosis, project.durationOfPrognosis)

df_levelhght = pd.DataFrame([], columns=["level", "height"])
df_windfield = pd.DataFrame([], columns=["time", "level", "direction", "speed"])

#print(task.mpp2adm_levelhght.times())
#print(task.mpp2adm_levelhght.levels())
#print(task.mpp2adm_levelhght.gridseries)
cell = None 
for key in task.mpp2adm_levelhght.gridseries:
    levelhght = task.mpp2adm_levelhght.gridseries[key]
    data = levelhght.timeSeries(113.937,22.31)
    #print ( key, levelhght.timeSeries(113.939,22.31) )
    df_levelhght = pd.concat([df_levelhght, pd.DataFrame([
      {
        "level": key, 
        "height": None if "values" not in data or len(data["values"]) == 0 else data["values"][0]
      }
    ])])
    if cell is None: 
        cell = levelhght.getCell(113.937,22.31)
        print(cell)

df_levelhght = df_levelhght.set_index("level")
print(df_levelhght)


# Print following wind field series is available
for wind_field in task.mpp2adm_wind.keys():
  print(wind_field)
  data = task.mpp2adm_wind[wind_field].valueAtCell(cell)
  time = project.startOfRelease + timedelta(seconds=project.timestepOfPrognosis * (data["time"] + 1))
  df_windfield = pd.concat([df_windfield, pd.DataFrame([
    {
      "time": time, 
      "level": None if "level" not in data else data["level"], 
      "direction": None if "Direction" not in data else data["Direction"], 
      "speed": None if "Speed" not in data else data["Speed"]
    }
  ])])

df_windfield = df_windfield.merge(df_levelhght, on="level", how="left")
df_windfield["time"] = pd.to_datetime(df_windfield["time"])
df_windfield = df_windfield.set_index(["time", "level"])
df_windfield.to_csv("C:\\Users\\Sara\\Documents\\JRODOS\\wind_field.csv")

if __name__=="__main__":
    print ( "Sample data loaded.")
    print("==== End %s ===="% datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
