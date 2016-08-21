from api import api
import csv
import logging
from parameters import Parameters
from keys import Keys
from db import run_sql
import MySQLdb


def stage_listings(batch_id, api_instance, api_parameters):

    counter = 0


    for listing in api_instance.property_listings(**api_parameters):

        row_fields = []
        for field in Parameters.FIELD_LIST:
            if hasattr(listing, field):
                row_fields.append(getattr(listing, field))
            else:
                row_fields.append('NULL')

        insert_statements.append(Parameters.SQL_STAGE_LISTING.format(batch_id, *row_fields))

        if len(insert_statements)>PARAMETERS.SQL_INSERT_BUFFER:
            run_sql(';'.join(insert_statements))
            insert_statements = []

    run_sql(';'.join(insert_statements))


def perform_looped_db_run():

    logging.info('Getting API')
    api_instance = api(api_key=Keys.API_KEY)

    api_parameters= Parameters.BASE_API_PARAMETERS

    batch_id = run_sql(Parameters.SQL_GET_BATCH_ID)
    logging.info('Starting Batch {}'.format(batch_id))
    run_sql(Parameters.SQL_LOG_ENTRY.format(batch_id=batch_id, level='I', message='Starting Batch'))

    for outcode in Parameters.OUTCODES:
        api_parameters['postcode'] = outcode

        run_sql(Parameters.SQL_CLEAR_STAGE)

        run_sql(Parameters.SQL_LOG_ENTRY.format(batch_id=batch_id, level='I', message='Pulling data for outcode [{}]'.format(outcode)))
        stage_listings(api_instance, api_parameters, batch_id)

        run_sql(Parameters.SQL_LOG_ENTRY.format(batch_id=batch_id, level='I', message='Merging data for outcode [{}]'.format(outcode)))
        run_sql(Parameters.SQL_MERGE_STAGE)

    run_sql(Parameters.SQL_LOG_ENTRY.format(batch_id=batch_id, level='I', message='Finished Batch'))

def csv_runner():
    logging.info('Getting API')
    api_instance = api(version=1, api_key=Keys.API_KEY)

    #single_run(api_instance, Parameters.BASE_API_PARAMETERS, Parameters.BASE_OUTPUT_FILE_NAME.format('single'))
    looped_run(api_instance, Parameters.BASE_API_PARAMETERS, Parameters.BASE_OUTPUT_FILE_NAME, 5)

def single_run(api_instance, api_params, file_name):
    get_data(api_instance, api_params, file_name, True)

def looped_run(api_instance, api_params, file_name, delay_spacer):
    for outcode in Parameters.OUTCODES:
        api_params['postcode'] = outcode
        chunk_file_name = file_name.format(outcode)
        get_data(api_instance, api_params, chunk_file_name, False)

def get_data_csv(api_instance, parameters, file_name, write_header):

    outputfile=open(file_name,'w',encoding='utf8',newline='')
    wr = csv.writer(outputfile, quoting=csv.QUOTE_ALL)

    if write_header:
        wr.writerow(Parameters.CSV_FIELD_LIST)

    for listing in api_instance.property_listings(**parameters):
        
        row_fields = []
        for field in Parameters.FIELD_LIST:
            if hasattr(listing, field):
                row_fields.append(getattr(listing, field))
            else:
                row_fields.append('')

        wr.writerow(row_fields)

    outputfile.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    perform_looped_db_run()