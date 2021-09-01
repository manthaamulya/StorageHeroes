def image_exif(image_directory):
    """From image directory get the EXIF(information) of the image"""
    from exif import Image
    import os
    # assign directory
    images_list = []
    # iterate over files in
    # that directory
    if os.path.isfile(image_directory):
        with open(image_directory, "rb") as test_file:
            new_file = Image(test_file)
            #print(image_directory)

            return new_file

def get_location(img_exif):
    """Get the geolocation of the picture from EXIF"""
    from geopy.geocoders import Nominatim

    #get latitude and longitude
    img_lat = img_exif.gps_latitude[0] + (img_exif.gps_latitude[1] / 60) + (img_exif.gps_latitude[2] / 3600)
    img_lon = img_exif.gps_longitude[0] + (img_exif.gps_longitude[1] / 60) + (img_exif.gps_longitude[2] / 3600)

    # get the reference of the latitude, if South hemisphere becomes negative
    if img_exif.gps_latitude_ref == "S":
        img_lat = -img_lat

    #  get the reference of the longitude, if West becomes negative
    if img_exif.gps_longitude_ref == "W":
        img_lon = -img_lon

    geolocator = Nominatim(user_agent="Photo")

    # get date in case we need to use for something
    img_date = img_exif.datetime_original
    img_time = img_exif.subsec_time_original

    # reverse the geolocation from latitude e longitude give the place
    location = geolocator.reverse("%s,%s" % (img_lat, img_lon), language='en')
    a_acc = "àáâãäåæ"
    #e_acc = "èéêë"
    #i_acc = "ìíîï"
    #o_acc = "ðòóôõö"
    #u_acc = "ùúûü"
    #print(location.raw["address"].values())
    for value in location.raw["address"].values():
        for i in a_acc:
            if i in value:
                value.replace(a_acc, "a")

    if "town" in location.raw["address"].keys():
        town = location.raw["address"]["town"]
    elif "village" in location.raw["address"].keys():
        town = location.raw["address"]["village"]
    elif "municipality" in location.raw["address"].keys():
        town = location.raw["address"]["municipality"]
    else:
        town = "No Town"

    return f'Town: {town}, State: {location.raw["address"]["state"]}, Country: {location.raw["address"]["country"]}'


####################### TAG #############################
def add_geo_image_description(image):
    """Add the new Geo Tag to the picture in a EXIF variable"""


    if get_location(image):
        place = get_location(image)
        try:
            image.image_description = place
        except:
            image.image_description = "no location"

    #print(image.image_description)

    return image


def save_updated_image(image_directory):
    """"
    call the image_exif function for the EXIF information
    call the add_geo_image_description for updating the EXIF of the picture
    and finally Save the image with updated Tag
    """

    #filename = os.path.split(image_directory)[1]
    image_info = image_exif(image_directory)
    img32 = add_geo_image_description(image_info)

    with open(image_directory, 'wb') as image_ex:
        image_ex.write(img32.get_file())
        #print(image_ex.write(img32.get_file()))
        #print("File information updated")


#save_updated_image('/home/amulyamantha/code/jaseppala/photosorganisation/raw_data/test_mantha/Mantha.jpg')
