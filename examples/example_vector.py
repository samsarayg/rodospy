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
project = rodos.get_projects(filters={"modelchainname":
                                      "Emergency"})[-1]

# Get the only task and also for wind series 12 first timestemps and 10 vertical levels
task = project.get_tasks({},12,1)[0]

# Print following wind field series is available
for wind_field in task.wind_field.keys():
    #print ( wind_field )
    print ( task.wind_field[wind_field] )
    gpkg_file = task.wind_field[wind_field].gpkg_file()
    gpkg_data = gpkg_driver.Open(gpkg_file)

    #print ("No of layers:", len(gpkg_data))
    layer = gpkg_data.GetLayer(0)

    # Pick up a cell
    layer.SetAttributeFilter( "cell={:d}".format(8006) )

    for feature in layer:
      for feat in feature.keys():
        print(feat, feature.GetField(feat))
        pass

    print("")

if __name__=="__main__":
    print ( "Sample data loaded.")
