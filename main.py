from api import api
import csv
import logging
from parameters import Parameters
from keys import Keys

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
    api_instance = api(version=1, api_key=Keys.API_KEY)

    #single_run(api_instance, Parameters.BASE_API_PARAMETERS, Parameters.BASE_OUTPUT_FILE_NAME.format('single'))
    looped_run(api_instance, Parameters.BASE_API_PARAMETERS, Parameters.BASE_OUTPUT_FILE_NAME, 5)

def single_run(api_instance, api_params, file_name):
    get_data(api_instance, api_params, file_name, True)

def looped_run(api_instance, api_params, file_name, delay_spacer):
    for outcode in Parameters.OUTCODES[0:0]:
        api_params['postcode'] = outcode
        chunk_file_name = file_name.format(outcode)
        get_data(api_instance, api_params, chunk_file_name, False)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()