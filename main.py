from api import api
import csv
import logging

class Parameters:
    BASE_OUTPUT_FILE_NAME ='output2/output_{}.csv'
    API_KEY = '85g6qverxyyjqe37gxkgqp6n'

    BASE_API_PARAMETERS = {
        'postcode': 'b23',
        'order_by': 'age',
        'max_results': 2000,
    #    'listing_status': 'rent',   # rent / sale
        'include_sold': 1,
        'include_rented': 1,
        'summarised': 'true'
    }

    OUTCODES = [
        'CV7', 'B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','B11','B12','B13','B14','B15','B16','B17','B18','B19','B20','B21','B23','B24','B25','B26','B27','B28','B29','B30','B31','B32','B33','B34','B35','B36','B37','B38','B40','B42','B43','B44','B45','B46','B47','B48','B49','B50','B60','B61','B62','B63','B64','B65','B66','B67','B68','B69','B70','B71','B72','B73','B74','B75','B76','B77','B78','B79','B80','B90','B91','B92','B93','B94','B95','B96','B97','B98'
        ]
    

    CSV_FIELD_LIST = [
        'listing_id',
        'outcode',
        'displayable_address',
        'num_bathrooms',
        'num_bedrooms',
        'num_floors',
        'num_recepts',
        'listing_status',
        'status',
        'price',
        'property_type',
        'street_name',
        'image_url',
        'details_url',
        'new_home',
        'latitude',
        'longitude',
        'first_published_date',
        'last_published_date'
    ]

def get_data(api_instance, parameters, file_name, write_header):

    outputfile=open(file_name,'w',encoding='utf8',newline='')
    wr = csv.writer(outputfile, quoting=csv.QUOTE_ALL)

    if write_header:
        wr.writerow(Parameters.CSV_FIELD_LIST)

    for listing in api_instance.property_listings(**parameters):
        
        row_fields = []
        for field in Parameters.CSV_FIELD_LIST:
            if hasattr(listing, field):
                row_fields.append(getattr(listing, field))
            else:
                row_fields.append('')

        wr.writerow(row_fields)

    outputfile.close()

def main():

    logging.info('Getting API')
    api_instance = api(version=1, api_key=Parameters.API_KEY)

    #single_run(api_instance, Parameters.BASE_API_PARAMETERS, Parameters.BASE_OUTPUT_FILE_NAME.format('single'))
    looped_run(api_instance, Parameters.BASE_API_PARAMETERS, Parameters.BASE_OUTPUT_FILE_NAME, 5)

def single_run(api_instance, api_params, file_name):
    get_data(api_instance, api_params, file_name, True)

def looped_run(api_instance, api_params, file_name, delay_spacer):
    for outcode in Parameters.OUTCODES[28:29]:
        api_params['postcode'] = outcode
        chunk_file_name = file_name.format(outcode)
        get_data(api_instance, api_params, chunk_file_name, False)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()