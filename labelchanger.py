list_file=['LicensePlate1/','LicensePlate2/','MaskedAdults/','MaskedChildren/','Masks/','PuckupTrucks/','Vehicles1/','Vehicles2/','Vehicles3/','Vehicles4/','Vehicles5/']
import xml.etree.ElementTree, os

for dir in list_file:
    os.mkdir('processed_dataset/'+dir)
    folder_list=os.listdir(dir)
    unique_list=set()
    for file in folder_list:
        # Open original file
        tree = xml.etree.ElementTree.parse(dir+file)
        root = tree.getroot()
        objs = root.findall('object')
        objNum = 0
        for obj in objs:
            objNum += 1
            currentObj = obj.find('name').text
            if currentObj=='Car':
                obj.find('name').text='car'
            elif currentObj=='Pickup_truck':
                obj.find('name').text='truck'
            elif currentObj=='Bus':
                obj.find('name').text='bus'
            elif currentObj=='Van':
                obj.find('name').text='car'
            elif currentObj=='License_plate':
                obj.find('name').text='license_plate'
            elif currentObj=='SUV':
                obj.find('name').text='car'
            elif currentObj=='Bicycle':
                obj.find('name').text='license_plate'
        tree.write('processed_dataset/'+dir+'/'+file)




print(unique_list)