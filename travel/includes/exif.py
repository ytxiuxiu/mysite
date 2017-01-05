import datetime

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

class Exif():
    exif = {}

    def __init__(self, image):
        self.exif = self._get_image_exif(image)

    def get_exif(self):
        return self.exif;

    def device(self):
        if 'Model' in self.exif:
            return self.exif['Model']

    def coordinate(self):
        if 'GPSInfo' in self.exif:
            gps_info = self.exif['GPSInfo']
            if ('GPSLatitude' in gps_info and 'GPSLatitudeRef' in gps_info and 
                'GPSLongitude' in gps_info and 'GPSLongitudeRef' in gps_info):
                latitude = self._convert_to_degree(gps_info['GPSLatitude'])
                longitude = self._convert_to_degree(gps_info['GPSLongitude'])

                if gps_info['GPSLatitudeRef'] != 'N':
                    latitude = -latitude
                if gps_info['GPSLongitudeRef'] != 'E':
                    longitude = -longitude

                return latitude, longitude

    def lens(self):
        if 'LensModel' in self.exif:
            return self.exif['LensModel']

    def exposure(self):
        if 'ExposureTime' in self.exif:
            exposure_time = self.exif['ExposureTime']
            return int(
                round(float(exposure_time[1]) / exposure_time[0], 0)
            )

    def iso(self):
        if 'ISOSpeedRatings' in self.exif:
            return self.exif['ISOSpeedRatings']

    def focal_length(self):
        if 'FocalLength' in self.exif:
            focus_length = self.exif['FocalLength']
            return float(focus_length[0]) / focus_length[1]

    def aperture(self):
        if 'ApertureValue' in self.exif:
            aperture = self.exif['ApertureValue']
            return float(aperture[0]) / aperture[1]

    def time(self):
        if 'DateTimeOriginal' in self.exif:
            return datetime.datetime.strptime(self.exif['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')

    def _get_image_exif(self, image):
        """
        Helper function to get the EXIF from an image
        """
        exif = {}
        image = Image.open(image.path)
        if image._getexif():
            for tag, value in image._getexif().items():
                exif[TAGS.get(tag, tag)] = value
            if 'GPSInfo' in exif:
                gps_info = {}
                for tag, value in exif['GPSInfo'].items():
                    gps_info[GPSTAGS.get(tag, tag)] = value
                exif['GPSInfo'] = gps_info
        return exif

    def _convert_to_degree(self, value):
        """
        Helper function to convert the GPS coordinates stored in the EXIF to degree
        """
        d0 = value[0][0]
        d1 = value[0][1]
        d = float(d0) / float(d1)

        m0 = value[1][0]
        m1 = value[1][1]
        m = float(m0) / float(m1)

        s0 = value[2][0]
        s1 = value[2][1]
        s = float(s0) / float(s1)

        return d + (m / 60.0) + (s / 3600.0)
