from geopy.distance import great_circle
import pandas

class TruckData:
    APPLICANT  = 'Applicant'
    ADDRESS    = 'Address'
    STATUS     = 'Status'
    FOOD_ITEMS = 'FoodItems'
    LATITUDE   = 'Latitude'
    LONGITUDE  = 'Longitude'
    DISTANCE   = 'DistanceFromLocation'

    STATUS_ISSUED = 'ISSUED'
    STATUS_ONLINE = 'ONLINE'
    STATUS_EXPIRED = 'EXPIRED'
    STATUS_REQUESTED = 'REQUESTED'
    STATUS_SUSPEND = 'SUSPEND'

    STATUS_ENUM = [
        STATUS_ISSUED, STATUS_ONLINE, STATUS_EXPIRED, STATUS_REQUESTED, STATUS_SUSPEND
    ]

    def __init__(self, latitude=0.0, longitude=0.0):
        self.latitude = latitude
        self.longitude = longitude
        self.data = self._refreshDataSet()

    def _refreshDataSet(self):
        dataFrame = pandas.read_csv('https://data.sfgov.org/api/views/rqzj-sfat/rows.csv')
        dataFrame = dataFrame.reindex(
            [
                self.APPLICANT,
                self.ADDRESS, 
                self.STATUS, 
                self.FOOD_ITEMS, 
                self.LATITUDE, 
                self.LONGITUDE
            ],
            axis=1
        )
        return self._appendDistanceFromLocation(dataFrame)

    def _appendDistanceFromLocation(self, dataFrame):
        dataFrame[self.DISTANCE] = dataFrame.apply(
            self._calculateDistance, axis=1
        )

        return dataFrame

    def _calculateDistance(self, df_row):
        return great_circle(
            (self.latitude, self.longitude),
            (df_row[self.LATITUDE], df_row[self.LONGITUDE])
        ).miles
