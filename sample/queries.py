# Standard library imports
import datetime

# Third party imports
import requests

# Local application/library specific imports


class EmptyJsonError(Exception):
    def __init__(self, url, json=None,
                 message='Empty JSON file received from URL:'):
        self.url = url
        self.message = message
        self.json = json
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}\n{self.url}\n{self.json}'


# TODO: Create other error messages for the other types of error messages.
class ServerFailedError(Exception):
    def __init__(self, status_code,
                 message='Server failed to fulfill request.'):
        self.message = message
        self.status_code = status_code
        self.error_codes = 'https://en.wikipedia.org/wiki/'\
                           'List_of_HTTP_status_codes#5xx_server_errors'
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}\n'\
               f'Error code: {self.status_code}\n'\
               f'{self.error_codes}'


# Placeholder classes for data structures
'''
# Listing all the offered data structures in case it's necessary to make 
#   classes for them later.
class WdsDataStructure:
    def __init__(self, ):
        pass


class ChangedSeries:
    pass


class CoordinateDataRequest:
    pass


class TableMetadata:
    pass


class Dimensions:
    pass


class Members:
    pass


class ReponseStatus:
    pass


class Datapoint:
    pass


class SeriesInfo:
    pass
'''


def _get(url):
    """Sends and returns a requests.get request to the URL given

    This function triggers a EmptyJsonError if the JSON received is empty.

    :param url: The url target.
    :return: The JSON object retrieved from the url, if any.
    """
    result = requests.get(url)
    if result.status_code >= 500:
        raise ServerFailedError(str(result.status_code))
    if result.text == '':
        raise EmptyJsonError(url)
    return result.json()


def _post(url, json):
    """Sends and returns a requests.post with post body to the URL given

    This function triggers a EmptyJsonError if the JSON received is empty.

    :param url: The url target.
    :param json: The post body to the request in JSON format.
    :return: The JSON object retrieved from the url, if any.

    """
    result = requests.post(url, json=json)
    if result.status_code >= 500:
        raise ServerFailedError(str(result.status_code))
    if result.text == '':
        raise EmptyJsonError(url, json)
    return result.json()


def _convert_date(date):
    """Converts to StatCan date string if date is a datetime.date object

    :param date: A string or a datetime.date object.
    :return: A StatCan formatted date string, ex: 2017-01-01
    """

    # TODO: Add date does not exist error
    if isinstance(date, datetime.date):
        date = '-'.join((str(date.year), str(date.month), str(date.day)))

    return date


# TODO Add conversion to output objects and finish editing docstrings
#  from here to EOF
# Product Change Listings GET Functions
def get_changed_series_list():
    """Returns a list of which series have changed today

    This can be invoked at any time of day and will reflect the list of
    series that have been updated at 8:30am EST on a given release up until
    midnight that same day.

    :return: TODO A ChangedSeries object.

    return example:
    {
     "status": "SUCCESS",
     "object": [
      {
       "responseStatusCode": 0,
       "vector_id": 107028707,
       "product_id": 25100059,
       "coordinate": "5.2.1.0.0.0.0.0.0.0",
       "releaseTime": "2018-01-23T08:30"
      },
    ... repeating objects
    """

    url = 'https://www150.statcan.gc.ca/t1/wds/rest/getChangedSeriesList'

    return _get(url)


def get_changed_cube_list(date):
    """Returns a list of which cubes have changed on the specified date

    :param date: Date example: '2021-05-03' or datetime.date(2021, 5, 3)
    :return: TODO

    return example:
    {
     "status": "SUCCESS",
     "object": [
      [
       {
        "responseStatusCode": 0,
        "product_id": 34100009,
        "releaseTime": "2017-12-07T08:30"
       },
    ... repeating objects

    Can be used using properly string formatted dates:
    >>> get_changed_cube_list('2021-05-03')
    As well as datetime.date objects:
    >>> get_changed_cube_list(datetime.date(2021, 5, 3))
    """

    # TODO: Add date does not exist error
    url = 'https://www150.statcan.gc.ca/t1/wds/rest/getChangedCubeList/'

    if isinstance(date, str):
        url += date
    elif type(date) is datetime.date:
        url += _convert_date(date)

    return _get(url)


# Cube Metadata and Series Information POST Functions
def get_cube_metadata(product_id):
    """Gets metadata for the specified cube

    Users can also request series metadata either by CubePidCoord or Vector
    as seen earlier using getSeriesInfoFromVector

    :param product_id:
    :return: TODO

    return example:
    [
      {
        "status": "SUCCESS",
        "object": {
          "responseStatusCode": 0,
          "product_id": "35100003",
          "cansimId": "251-0008",
          "cubeTitleEn": "Average counts of young persons in
            provincial and territorial correctional services",
          "cubeTitleFr": "Comptes moyens des adolescents dans les services
            correctionnels provinciaux et territoriaux",
          "cubeStartDate": "1997-01-01",
          "cubeEndDate": "2015-01-01",
          "nbSeriesCube": 171,
          "nbDatapointsCube": 3129,
          "archiveStatusCode": "2",
          "archiveStatusEn": "CURRENT - a cube available to the public
            and that is current",
          "archiveStatusFr": "ACTIF - un cube qui est disponible au public
            et qui est toujours mise a jour",
          "releaseTime": "2015-05-09T08:30",
          "subjectCode": [
            "350102",
            "4211"
          ],
          "surveyCode": [
            "3313"
          ],
          "dimension": [
            {
              "dimensionPositionId": 1,
              "dimensionNameEn": "Geography",
              "dimensionNameFr": "Géographie",
              "hasUom": false,
              "member": [
                {
                  "memberId": 1,
                  "parentMemberId": 15,
                  "memberNameEn": "Newfoundland and Labrador",
                  "memberNameFr": "Terre-Neuve-et-Labrador",
                  "classificationCode": "10",
                  "classificationTypeCode": "1",
                  "geoLevel": 2,
                  "vintage": 2011,
                  "terminated": 0,
                  "memberUomCode": null
                },
    … repeating objects
    "footnote":[{"footnoteId":1,"footnotesEn":"Corrections Key Indicator Report
     for Youth, Canadian Centre for Justice and Community Safety Statistics
     (CCJCSS), Statistics Canada. Fiscal year (April 1 through March 31).
     Due to rounding,
    ... repeating objects
               "link":{"footnoteId":22,"dimensionPositionId":2,
               "memberId":12}}],"correctionFootnote":[],
               "geoAttribute":[],"correction":[]}}
    ]

    For example:
    >>> get_cube_metadata(33100036)

    Post body example:
    [{"productId":35100003}]
    """

    url = 'https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata'
    post_body = [{"productId": product_id}]

    return _post(url, post_body)


def get_series_info_from_cube_pid_coord(product_id, coordinate):
    """Gets the series info from a cube's product id and coordinate

    :param product_id:
    :param coordinate:
    :return: TODO

    Return example:
    [{
        "status": "SUCCESS",
        "object": {
          "responseStatusCode": 0,
          "product_id": 35100003,
          "coordinate": "1.12.0.0.0.0.0.0.0.0",
          "vector_id": 32164132,
          "frequencyCode": 12,
          "scalarFactorCode": 0,
          "decimals": 2,
          "terminated": 0,
          "SeriesTitleEn": "Newfoundland and Labrador;
                            Probation rate per 10,000 young persons",
          "SeriesTitleFr": "Terre-Neuve-et-Labrador;
                            Taux de probation pour 10 000 jeunes",
          "memberUomCode": 257
       }}]

    Post body example: [{"productId": 35100003,
                         "coordinate": "1.12.0.0.0.0.0.0.0.0"}]

    For example:
    >>> get_series_info_from_cube_pid_coord(33100036, '1.14.0.0.0.0.0.0.0.0')
    """

    url = ('https://www150.statcan.gc.ca/t1/wds/rest/'
           'getSeriesInfoFromCubePidCoord')

    post_body = [{'productId': product_id, 'coordinate': coordinate}]

    return _post(url, post_body)


def get_series_info_from_vector(vector_id):
    """Gets series metadata from a vector

    :param vector_id:
    :return: TODO

    return example:
    [{
        "status": "SUCCESS",
        "object": {
          "responseStatusCode": 0,
          "product_id": 35100003,
          "coordinate": "1.12.0.0.0.0.0.0.0.0",
          "vector_id": 32164132,
          "frequencyCode": 12,
          "scalarFactorCode": 0,
          "decimals": 2,
          "terminated": 0,
          "SeriesTitleEn": "Newfoundland and Labrador;
                            Probation rate per 10,000 young persons",
          "SeriesTitleFr": "Terre-Neuve-et-Labrador;
                            Taux de probation pour 10 000 jeunes",
          "memberUomCode": 257
       }}]

    Post body example: [{"vector_id":32164132}]

    For example:
    >>>get_series_info_from_vector(111666237)
    """

    url = 'https://www150.statcan.gc.ca/t1/wds/rest/getSeriesInfoFromVector'
    post_body = [{"vectorId": vector_id}]

    return _post(url, post_body)


def get_all_cubes_list():
    """Provides a complete inventory of data tables with dimension details

    Users can query the output database to provide a complete inventory
    of data tables available through this Statistics Canada API. This command
    accesses a comprehensive list of details about each table including
    information at the dimension level, as well as footnotes.

    :return: TODO

    return  example:
    [
      {
        "product_id":10100004,
        "cansimId":"176-0013",
        "cubeTitleEn":"Chartered banks, total claims and liabilities booked
            worldwide vis-à-vis non-residents, Bank of Canada",
        "cubeTitleFr":"Banques à charte, ensembles des créances et engagements
            comptabilisés dans le monde au nom de non-résidents,
            Banque du Canada",
        "cubeStartDate":"1978-04-01",
        "cubeEndDate":"2018-01-01",
        "archived":"2",
        "subjectCode":[
          "10"
        ],
        "surveyCode":[
          "7502"
        ],
        "frequencyCode":9,
        "dimensions":[
          {
            "dimensionNameEn":"Geography",
            "dimensionNameFr":"Géographie",
            "dimensionPositionId":1,
            "hasUOM":false
          },
          {
            "dimensionNameEn":"Claims and deposits",
            "dimensionNameFr":"Créances et dépôts",
            "dimensionPositionId":2,
            "hasUOM":false
          },
          {
            "dimensionNameEn":"Type of non-resident",
            "dimensionNameFr":"Genre du non-résident",
            "dimensionPositionId":3,
            "hasUOM":false
          },
          {
            "dimensionNameEn":"Country of non-resident",
            "dimensionNameFr":"Pays du non-résident",
            "dimensionPositionId":4,
            "hasUOM":true
          }
        ],
        "corrections":[
        ]
      },
      {
      ... repeating objects
    """

    url = 'https://www150.statcan.gc.ca/t1/wds/rest/getAllCubesList'

    return _get(url)


def get_all_cubes_list_lite():
    """Provides a complete inventory of data tables without dimension info

    Users can query the output database to provide a complete inventory of
    data tables available through this Statistics Canada API. This command
    accesses a list of details about each table.  Unlike getAllCubesList,
    this method does not return dimension or footnote information.

    :return: TODO

    return example:
    [
      {
        "product_id":10100004,
        "cansimId":"176-0013",
        "cubeTitleEn":"Chartered banks, total claims and liabilities booked
            worldwide vis-à-vis non-residents, Bank of Canada",
        "cubeTitleFr":"Banques à charte, ensembles des créances et engagements
            comptabilisés dans le monde au nom de non-résidents,
            Banque du Canada",
        "cubeStartDate":"1978-04-01",
        "cubeEndDate":"2018-01-01",
        "archived":"2",
        "subjectCode":[
          "10"
        ],
        "surveyCode":[
          "7502"
        ],
        "frequencyCode":9,
        "corrections":[
        ]
      },
      {
    ... repeating objects
    """

    url = 'https://www150.statcan.gc.ca/t1/wds/rest/getAllCubesListLite'

    return _get(url)


# Data Access; data changes for today, over time and full table
def get_changed_series_data_from_cube_pid_coord(product_id, coordinate):
    """Provides series metadata on changes given a table's id and coordinate

    :param product_id: Representative / default view product ID
        for a table or cube, 10-digit identifier (i.e. 1310008901).
    :param coordinate: Concatenation of the member ID values for each
        dimension. One value per dimension (i.e. 1.1.1.36.1.0.0.0.0.0)
    :return: TODO

    return example:
    [
      {
        "status": "SUCCESS",
        "object":{
        "responseStatusCode": 0,
        "product_id": 35100003,
        "coordinate": "1.12.0.0.0.0.0.0.0.0",
        "vector_id": 32164132,
        "refPer": "1994-01-01",
        "refPer2": "1995-01-01",
        "refPerRaw": "1994-01-01",
        "refPerRaw2": "1995-01-01",
        "value": 1052,
        "decimals": 0,
        "scalarFactorCode": 0,
        "symbolCode": 0,
        "statusCode": 7,
        "securityLevelCode": 0,
        "releaseTime": 2017-12-07T08:30,
        "frequencyCode": 13
      }
    ... repeating objects

    Post body example: [{"productId": 35100003,
                         "coordinate": "1.12.0.0.0.0.0.0.0.0"}]

    >>>get_changed_series_data_from_cube_pid_coord(36100402,
    ...                                            '1.2.3.0.0.0.0.0.0.0')
    """

    url = 'https://www150.statcan.gc.ca/t1/wds/rest/'\
          'getChangedSeriesDataFromCubePidCoord'
    post_body = [{"productId": product_id, "coordinate": coordinate}]

    return _post(url, post_body)


def get_changed_series_data_from_vector(vector_id):
    """Provides series metadata on changes given a vector

    :param vector_id:
    :return: TODO

    return example:
    [
      {
        "status": "SUCCESS",
        "object":{
        "responseStatusCode": 0,
        "product_id": 35100003,
        "coordinate": "1.12.0.0.0.0.0.0.0.0",
        "vector_id": 32164132,
        "refPer": "1994-01-01",
        "refPer2": "1995-01-01",
        "refPerRaw": "1994-01-01",
        "refPerRaw2": "1995-01-01",
        "value": 1052,
        "decimals": 0,
        "scalarFactorCode": 0,
        "symbolCode": 0,
        "statusCode": 7,
        "securityLevelCode": 0,
        "releaseTime": 2017-12-07T08:30,
        "frequencyCode": 13
      }
    ... repeating objects

    Post body example: [{"vectorId":32164132}]

    >>>get_changed_series_data_from_vector(62464521)
    """

    url = 'https://www150.statcan.gc.ca/t1/wds/rest/'\
          'getChangedSeriesDataFromVector'
    post_body = [{"vectorId": vector_id}]

    return _post(url, post_body)


def get_data_from_cube_pid_coord_and_latest_n_periods(product_id,
                                                      coordinate, latest_n):
    """Gets the latest n periods of data from product id and coordinate

    For those who are looking to display data going back N reporting periods
    from today using product id and coordinate.

    :param product_id:
    :param coordinate:
    :param latest_n:
    :return: TODO

    return example:
    [
      {
        "status": "SUCCESS",
        "object": {
          "responseStatusCode": 0,
          "product_id": 34100006,
          "coordinate": "1.2.7.0.0.0.0.0.0.0",
          "vector_id": 42076,
          "vectorDataPoint": [
            {
              "refPer": "2017-07-01",
              "refPer2": "",
              "refPerRaw": "2017-01-01",
              "refPerRaw2": "",
              "value": "18381",
              "decimals": 0,
              "scalarFactorCode": 0,
              "symbolCode": 0,
              "statusCode": 0,
              "securityLevelCode": 0,
              "releaseTime": "2017-12-07T08:30",
              "frequencyCode": 6
            },
    ... repeating N times

    Post body example: [{"productId": 35100003,
                         "coordinate": "1.12.0.0.0.0.0.0.0.0",
                         "latestN":3}]

    >>>get_data_from_cube_pid_coord_and_latest_n_periods(
    ...    36100402, '1.2.3.0.0.0.0.0.0.0', 2
    ...)
    """

    url = 'https://www150.statcan.gc.ca/t1/wds/rest/'\
          'getDataFromCubePidCoordAndLatestNPeriods'

    post_body = [{"productId": product_id, "coordinate": coordinate,
                  "latestN": latest_n}]

    return _post(url, post_body)


def get_data_from_vectors_and_latest_n_periods(vector_id, latest_n):
    """Gets the latest n periods of data using vector id

    For those who are looking to display data going back N reporting periods
    from today using vector identification.

    :param vector_id:
    :param latest_n:
    :return: TODO

    return example:
    [
      {
        "status": "SUCCESS",
        "object": {
          "responseStatusCode": 0,
          "product_id": 34100006,
          "coordinate": "1.2.7.0.0.0.0.0.0.0",
          "vector_id": 42076,
          "vectorDataPoint": [
            {
              "refPer": "2017-07-01",
              "refPer2": "",
              "refPerRaw": "2017-01-01",
              "refPerRaw2": "",
              "value": "18381",
              "decimals": 0,
              "scalarFactorCode": 0,
              "symbolCode": 0,
              "statusCode": 0,
              "securityLevelCode": 0,
              "releaseTime": "2017-12-07T08:30",
              "frequencyCode": 6
            },
    ... repeating n times

    Post body example: [{"vectorId":32164132, "latestN":3}]

    For example:
    >>>get_data_from_vectors_and_latest_n_periods(62464521, 2)
    """

    url = ('https://www150.statcan.gc.ca/t1/wds/rest/'
           'getDataFromVectorsAndLatestNPeriods')
    post_body = [{"vectorId": vector_id, "latestN": latest_n}]

    return _post(url, post_body)


def get_bulk_vector_data_by_range(vector_ids, start_data_release_date,
                                  end_data_release_date):
    """Provides vector data for a given date range

    For users that require accessing data according to a certain date range,
    this method allows access by date range and vector.

    :param vector_ids:
    :param start_data_release_date:
    :param end_data_release_date:
    :return:

    return example:
    [
      {
        "status": "SUCCESS",
        "object": {
          "responseStatusCode": 0,
          "product_id": 17100009,
          "coordinate": "1.0.0.0.0.0.0.0.0.0",
          "vector_id": 1,
          "vectorDataPoint": [
            {
              "refPer": "2017-01-01",
              "refPer2": "",
              "refPerRaw": "2017-01-01",
              "refPerRaw2": "",
              "value": 36474968,
              "decimals": 0,
              "scalarFactorCode": 0,
              "symbolCode": 0,
              "statusCode": 0,
              "securityLevelCode": 0,
              "releaseTime": "2018-03-22T15:05",
              "frequencyCode": 9
            },
            ... repeating for every datapoint
          ]
        }
      },
      ... repeating for every vector requested
    ]

    >>> get_bulk_vector_data_by_range(
    ...    [62464521, 1], "2015-12-01T08:30", "2018-03-31T19:00"
    ...)

    Post body example: {
        "vectorIds": [62464521, 1],
        "startDataPointReleaseDate": "2015-12-01T08:30",
        "endDataPointReleaseDate": "2018-03-31T19:00"
        }
    """

    # TODO: allow datetime.date arguments to be passed in.

    url = 'https://www150.statcan.gc.ca/t1/wds/rest/'\
          'getBulkVectorDataByRange'

    start_data_release_date = _convert_date(start_data_release_date)
    end_data_release_date = _convert_date(end_data_release_date)

    post_body = {
        "vectorIds": vector_ids,
        "startDataPointReleaseDate": start_data_release_date,
        "endDataPointReleaseDate": end_data_release_date
    }

    return _post(url, post_body)


def get_data_from_vector_by_reference_period_range(vectors,
                                                   start_reference_period,
                                                   end_reference_period):
    """Provides data for the specified vector for a given range of time

    For users that require accessing data according to a certain reference
    period range, this method allows access by reference period range
    and vector.

    :param vectors:
    :param start_reference_period:
    :param end_reference_period:
    :return:

    return example:
    {
      "status": "SUCCESS",
      "object": {
       "responseStatusCode": 0,
       "product_id": 17100009,
       "coordinate": "1.0.0.0.0.0.0.0.0.0",
       "vector_id": 1,
       "vectorDataPoint": [
        {
         "refPer": "2016-01-01",
         "refPer2": "",
         "refPerRaw": "2016-01-01",
         "refPerRaw2": "",
         "value": 35871136,
         "decimals": 0,
         "scalarFactorCode": 0,
         "symbolCode": 0,
         "statusCode": 0,
         "securityLevelCode": 0,
         "releaseTime": "2020-09-29T08:30",
         "frequencyCode": 9
        },
        {
         "refPer": "2016-04-01",
         "refPer2": "",
         "refPerRaw": "2016-04-01",
         "refPerRaw2": "",
         "value": 35970303,
         "decimals": 0,
         "scalarFactorCode": 0,
         "symbolCode": 0,
         "statusCode": 0,
         "securityLevelCode": 0,
         "releaseTime": "2020-09-29T08:30",
         "frequencyCode": 9
        }, ... repeating for every datapoint
       ]
      }
     },
     {
      "status": "SUCCESS",
      "object": {
       "responseStatusCode": 0,
       "product_id": 17100009,
       "coordinate": "2.0.0.0.0.0.0.0.0.0",
       "vector_id": 2,
       "vectorDataPoint": [
        {
         "refPer": "2016-01-01",
         "refPer2": "",
         "refPerRaw": "2016-01-01",
         "refPerRaw2": "",
         "value": 528800.0,
         "decimals": 0,
         "scalarFactorCode": 0,
         "symbolCode": 0,
         "statusCode": 0,
         "securityLevelCode": 0,
         "releaseTime": "2020-09-29T08:30",
         "frequencyCode": 9
        }, ... repeating for every datapoint
       ]
      }
     },
     ... repeating for every vector requested
    ]

    For example:
    >>>get_data_from_vector_by_reference_period_range(
    ...    [1, 2], "2016-01-01", "2017-01-01"
    ...)

    URL suffix example:
    ?vector_ids="1","2"&startRefPeriod=2016-01-01&end_reference_period=2017-01-01
    which is made up from these arguments:
        vector_ids="1","2"&
        startRefPeriod=2016-01-01&
        endReferencePeriod=2017-01-01
    """

    if isinstance(start_reference_period, datetime.date):
        start_reference_period = '-'.join((str(start_reference_period.year),
                                           str(start_reference_period.month),
                                           str(start_reference_period.day)))

    if isinstance(end_reference_period, datetime.date):
        end_reference_period = '-'.join((str(end_reference_period.year),
                                         str(end_reference_period.month),
                                         str(end_reference_period.day)))

    url = ('https://www150.statcan.gc.ca/t1/wds/rest/'
           'getDataFromVectorByReferencePeriodRange')

    url += '?vectorIds="' + '","'.join(str(i) for i in vectors) + '"&' \
           + 'startRefPeriod=' + start_reference_period + '&' \
           + 'endReferencePeriod=' + end_reference_period

    return _get(url)


def get_full_table_download_csv(product_id, language):
    """Provides the download link of product Id in either English or French

    For users who require the full table/cube of extracted time series,
    a static file download is available in CSV format. This function allows
    the user to specify English (en) or French (fr).

    :param product_id:
    :param language:
    :return: a link to the Product Id (PID) supplied in the URL

    return example:
    {
      "status": "SUCCESS",
      "object": "https://www150.statcan.gc.ca/n1/tbl/csv/14100287-eng.zip"
    }
    """
    def _id_language(lang):
        """A function to return 'en' or 'fr' if passed a common abbreviation.

        :param lang: The desired language tag, some abbreviation of
            either English or French
        :return: Either 'en' or 'fr' or None. Returns None if abbreviation is
            unrecognized.
        """
        lan_dict = {
            'en': ['english', 'English', 'ENGLISH', 'EN', 'en',
                   'En', 'Eng', 'ENG', 'eng'],
            'fr': ['french', 'French', 'FRENCH', 'FR', 'fr', 'Fr',
                   'Fre', 'FRE', 'fre', 'FRN', 'frn', 'Frn']
        }
        for k, v in lan_dict.items():
            if lang in v:
                return k

        return None

    url = 'https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/'
    url += str(product_id) + '/{lan}'.format(lan=_id_language(language))

    return _get(url)


def get_full_table_download_sdmx(product_id):
    """Returns a download link for the given table in bilingual SDMX format

    :param product_id: example: 14100287
    :return: TODO

    return example:
    {
      "status": "SUCCESS",
      "object": "https://www150.statcan.gc.ca/n1/tbl/csv/14100287-SDMX.zip"
    }

    For example:
    >>>get_full_table_download_csv(17100009, 'en')
    """
    url = 'https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadSDMX/'
    url += str(product_id)

    return _get(url)


# Supplemental Information GET Functions
def get_code_sets():
    """Provides information to describe StatCan data

    Code Sets provide additional information to describe the information
    such as scales, frequencies and symbols. Use method getCodeSets to access
    the most recent version of the code sets with descriptions
    (English and French) for all possible codes.

    :return: TODO

    return example:
    {
      "status": "SUCCESS",
      "object": {
        "scalar": [
          {
            "scalarFactorCode": 0,
            "scalarFactorDescEn": "units ",
            "scalarFactorDescFr": "unités"
          },
    … repeating objects
        ],
        "frequency": [
          {
            "frequencyCode": 1,
            "frequencyDescEn": "Daily",
            "frequencyDescFr": "Quotidien"
          },
    ... repeating objects

    For example:
    >>>get_code_sets()
    """

    url = 'https://www150.statcan.gc.ca/t1/wds/rest/getCodeSets'

    return _get(url)
