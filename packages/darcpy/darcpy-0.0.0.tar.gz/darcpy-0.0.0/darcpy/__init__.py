try:
    import arcpy
    print("Warning, you have arcpy")
except ImportError:
    print("No arcpy detected, you are free!")