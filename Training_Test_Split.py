import arcpy
import os
classname = [] # Create a list of classes by entering the class names here
arcpy.env.overwriteOutput = True
fclass_list = 'SirianniFieldData2019.shp'
data_path = r'Put_Your_Data Path Here'
out_path = r'Put Your Output Location Path Here'
arcpy.env.workspace = data_path

#Split the data into individual classes and split them into training and test by 80:20 ratio
for cls in classname:
    arcpy.env.workspace = data_path
    arcpy.MakeFeatureLayer_management(fclass_list, 'data_point', """"classname" = '{}'""".format(cls))
    feature_layer = 'data_point'
    count = int(arcpy.GetCount_management(feature_layer).getOutput(0))
    valid_data_num = int((0.2*count)) # Here 0.2 represent the 20 % of total sample. Range (0 to 1) representing 0 to 100 %
    train_data_num = count - valid_data_num
    print("Total valid data {}: ".format(cls),valid_data_num)
    print("Total train data {}: ".format(cls),train_data_num)
    arcpy.management.CreateRandomPoints(out_path,"temp_valid.shp", feature_layer," ", valid_data_num, '25',"", "" )
    valid_data = 'temp_valid.shp'
    arcpy.env.workspace = out_path
    arcpy.MakeFeatureLayer_management(valid_data, 'valid_name')
    valid_data_name = 'valid_name'
    arcpy.management.SelectLayerByLocation(feature_layer,'INTERSECT',valid_data_name,'','NEW_SELECTION')
    arcpy.CopyFeatures_management(feature_layer, "{}_Valid_{}".format(valid_data_num,cls))
    arcpy.SelectLayerByAttribute_management(feature_layer, "SWITCH_SELECTION")
    arcpy.CopyFeatures_management(feature_layer, "{}_Train_{}".format(train_data_num,cls))
    print(cls, " Done !!!")
    print(" ")
print("Deleting temporary files")
arcpy.management.Delete("temp_valid.shp")
print(" ")
print('All Done Happy !!! 😊')

# Combined all individually splitted data into 2 files one training and one test/validation file

gdb_path = r'Enter_GDB_Path_Here' #Enter the gdb path of individual classe files
gdb_name = "Enter GDB Name Here"
if arcpy.Exists(gdb_path):
    arcpy.env.workspace = gdb_path
    feature_classes = arcpy.ListFeatureClasses()
    for fc in feature_classes:
        arcpy.Delete_management(fc)
if not arcpy.Exists(gdb_path):
    arcpy.CreateFileGDB_management(gdb_path, gdb_name)
arcpy.env.workspace = out_path    
fe_class = arcpy.ListFeatureClasses()
for fc in fe_class:
    arcpy.conversion.FeatureClassToGeodatabase(fc,gdb_path)
arcpy.env.workspace = gdb_path
fe_class = arcpy.ListFeatureClasses()
for fc in fe_class:
    val_fc = [fc for fc in fe_class if 'valid' in fc.lower()]
    tra_fc = [fc for fc in fe_class if 'train' in fc.lower()]
val_count = 0
tra_count = 0
for fc in val_fc:
    count = int(arcpy.GetCount_management(fc).getOutput(0))
    val_count = count + val_count
for fc in tra_fc:
    count = int(arcpy.GetCount_management(fc).getOutput(0))
    tra_count = count + tra_count
print("Total Validation points: ", val_count)
print("Total Training Points: ", tra_count)
arcpy.management.Merge(val_fc,"{}\\Validation_data".format(gdb_path))
arcpy.management.Merge(tra_fc,"{}\\Training_data".format(gdb_path))
print(" ")
print('All Done Happy !!! 😊')
