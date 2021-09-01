def image_exif(image_directory):
  """From image directory get the EXIF(information) of the image"""
  from exif import Image
  import os
  # assign directory
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
    #print(location.raw["address"])

    if "city" in location.raw["address"].keys():
        town = location.raw["address"]["city"]
    elif "town" in location.raw["address"].keys():
        town = location.raw["address"]["town"]
    elif "village" in location.raw["address"].keys():
        town = location.raw["address"]["village"]
    elif "municipality" in location.raw["address"].keys():
        town = location.raw["address"]["municipality"]
    else:
        town = "No Town"

    return f'{town}, {location.raw["address"]["state"]}, {location.raw["address"]["country"]}'


####################### TAGS #############################
def char_fixer(string):
    """
    Find special characters in a string and replace them for normal letters
    """
    a_acc = "àáâãäåæ"
    e_acc = "èéêë"
    i_acc = "ìíîï"
    o_acc = "ðòóôõö"
    u_acc = "ùúûü"

    location = string
    location_list = []
    for char in location:
        if char.lower() in a_acc:
            char = 'a'
        elif char.lower() in e_acc:
            char = "e"
        elif char.lower() in i_acc:
            char = "i"
        elif char.lower() in o_acc:
            char = "o"
        elif char.lower() in u_acc:
            char = "u"
        elif char.lower() in "ç":
            char = "c"
        location_list.append(char)

    return "".join(location_list)


def add_tags(image, user_comment):
    """
    Add the new Geo Tag to the picture in a EXIF variable
    Add Comment to the picture in a EXIF variable
    """
    try:
        get_location(image)
        place = get_location(image)
        image.image_description = char_fixer(place)
    except:
        image.image_description = "no location"
    #print(image.image_description)
    if user_comment != "0":
        image["user_comment"] = char_fixer(user_comment)
        #print(image["user_comment"])

    return image


def save_tags(image_directory, user_comment="0"):
    """"
    Call the image_exif function for the EXIF information
    Call the add_geo_image_description for updating the EXIF of the picture
    Save the image with updated Tags
    """

    #filename = os.path.split(image_directory)[1]
    image_info = image_exif(image_directory)
    img32 = add_tags(image_info, user_comment)
    # if comment == True:
    #     img32 = add_comment_tag(image_info, comment)

    with open(image_directory, 'wb') as image_ex:
        image_ex.write(img32.get_file())
        #print(image_ex.write(img32.get_file()))
        #print("File information updated")
