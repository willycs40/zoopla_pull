class Parameters:

    DB_HOST = 'mysql'
    DB_USER = 'will'
    DB_PASS = 'housepass'
    DB_SCHEMA = 'housing'

    API_BASE_URL = 'http://api.zoopla.co.uk/api/v1/'
    API_PAGE_SIZE = 100

    BASE_OUTPUT_FILE_NAME ='output/output_{}.csv'

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
    
    FIELD_LIST = [
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
        'price_modifier',
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

    SQL_INSERT_BUFFER = 100

    SQL_CLEAR_STAGE = '''
        TRUNCATE TABLE housing.listing_stage; 
    '''

    SQL_GET_BATCH_ID = '''
        select max(batch_id)+1 as batch_id
        from housing.log;
    '''

    SQL_LOG_ENTRY = '''
        insert into housing.log (
            batch_id
            timestamp
            , level
            , message
        )
        values (
            {batch_id}
            , now()
            , '{level}'
            , '{message}'
        )
    '''

    SQL_STAGE_LISTING = '''
        insert into housing.listing_stage(
            , batch_id
            , listing_id
            , outcode 
            , displayable_address 
            , num_bathrooms
            , num_bedrooms
            , num_floors
            , num_recepts
            , listing_status 
            , status 
            , price 
            , price_modifier 
            , property_type
            , street_name
            , image_url
            , details_url
            , new_home 
            , latitude 
            , longitude 
            , first_published_date 
            , last_published_date 
        )
        values (
            {}
            , {}
            , '{}'
            , '{}'
            , {}
            , {}
            , {}
            , {}
            , '{}'
            , '{}'
            , {}
            , '{}'
            , '{}'
            , '{}'
            , '{}'
            , '{}'
            , '{}'
            , {}
            , {}
            , '{}'
            , '{}'
        )
    '''

    SQL_MERGE_STAGE = '''
        insert into housing.listing(
            batch_id
            , listing_id
            , outcode 
            , num_bathrooms
            , num_bedrooms
            , num_floors
            , num_recepts
            , listing_status_id
            , status_id 
            , price 
            , property_type_id 
            , new_home 
            , latitude 
            , longitude 
            , first_published_date 
            , last_published_date
        )
        select      batch_id
                    , listing_id
                    , outcode
                    , num_bathrooms
                    , num_bedrooms
                    , num_floors
                    , num_recepts
                    , ls.listing_status_id
                    , s.status_id 
                    , price 
                    , pm.price_modifier_id
                    , pt.property_type_id 
                    , case when new_home='true' then 1 else 0 end
                    , latitude 
                    , longitude 
                    , first_published_date 
                    , last_published_date
        from        housing.listing_stage l
        left join   listing_status ls
        on          l.listing_status = ls.listing_status
        left join   status s
        on          l.status = s.status
        left join   property_type pt
        on          l.property_type = pt.property_type
        left join   price_modifier pm
        on          l.price_modifier = pm.price_modifier

        insert into housing.listing_address(
            listing_table_id
            , displayable_address 
            , street_name
            , image_url 
            , details_url
        )
        select l.listing_table_id
            , ls.displayable_address 
            , ls.street_name
            , ls.image_url 
            , ls.details_url
        from        listing l
        inner join  listing_stage ls
        on          l.listing_id = ls.listing_id
        and         l.batch_id = ls.batch_id

    '''

    SQL_INITIALISE = '''
        create table housing.log (
            log_id int NOT NULL AUTO_INCREMENT,
            , batch_id int
            , timestamp datetime
            , level varchar(1)
            , message varchar(500)
        primary key (log_id)
        );

        create table housing.listing_stage (
            listing_stage_id int NOT NULL AUTO_INCREMENT,
            , batch_id int
            , listing_id int
            , outcode varchar(5)
            , displayable_address varchar(250)
            , num_bathrooms int
            , num_bedrooms int
            , num_floors int
            , num_recepts int
            , listing_status varchar(5)
            , status varchar(20)
            , price int
            , price_modifier varchar(20)
            , property_type varchar(20)
            , street_name varchar(250)
            , image_url varchar(100)
            , details_url varchar(100)
            , new_home varchar(5)
            , latitude float
            , longitude float
            , first_published_date date
            , last_published_date date
        primary key (listing_stage_id)
        );


        create table housing.listing (
            listing_table_id int NOT NULL AUTO_INCREMENT,
            , batch_id int
            , listing_id int
            , outcode varchar(5)
            , num_bathrooms int
            , num_bedrooms int
            , num_floors int
            , num_recepts int
            , listing_status_id int
            , status_id int
            , price int
            , price_modifier_id int
            , property_type_id int
            , new_home tinyint
            , latitude float
            , longitude float
            , first_published_date date
            , last_published_date date
        primary key (listing_table_id)
        );

        create table housing.listing_address (
            listing_address_id int NOT NULL AUTO_INCREMENT,
            listing_table_id int
            displayable_address varchar(250)
            street_name varchar(250)
            image_url varchar(100)
            details_url varchar(100)
            )

        create table housing.listing_status (
            listing_status_id int
            , listing_status varchar(5)
        primary key (listing_status_id)
        );

        insert into housing.listing_status
        values (1, 'sale');
        insert into housing.listing_status
        values (2, 'rent');

        create table housing.status (
            status_id int
            , status varchar(20)
        primary key (status_id)
        );

        insert into housing.status
        values (1, 'for_sale');
        insert into housing.status
        values (2, 'sale_under_offer');
        insert into housing.status
        values (3, 'sold');
        insert into housing.status
        values (4, 'to_rent');
        insert into housing.status
        values (5, 'rent_under_offer');
        insert into housing.status
        values (6, 'rented');   

        create table housing.price_modifier (
            price_modifier_id int
            , price_modifier varchar(20)
        primary key (price_modifier_id)
        );

        insert into housing.price_modifier
        values (1, 'offers_over');
        insert into housing.price_modifier
        values (2, 'poa');
        insert into housing.price_modifier
        values (3, 'fixed_price');
        insert into housing.price_modifier
        values (4, 'from');
        insert into housing.price_modifier
        values (5, 'offers_in_region_of');
        insert into housing.price_modifier
        values (6, 'part_buy_part_rent');
        insert into housing.price_modifier
        values (7, 'price_on_request');
        insert into housing.price_modifier
        values (8, 'shared_equity');
        insert into housing.price_modifier
        values (9, 'shared_ownership');
        insert into housing.price_modifier
        values (10, 'guide_price');
        insert into housing.price_modifier
        values (11, 'sale_by_tender');

        create table housing.property_type (
            property_type_id int
            , property_type varchar(20)
        primary key (property_type_id)
        );                   

        insert into housing.property_type
        values (1, 'Terraced');
        insert into housing.property_type
        values (2, 'End of terrace');
        insert into housing.property_type
        values (3, 'Semi-detached');
        insert into housing.property_type
        values (4, 'Detached');
        insert into housing.property_type
        values (5, 'Mews house');
        insert into housing.property_type
        values (6, 'Flat');
        insert into housing.property_type
        values (7, 'Maisonette');
        insert into housing.property_type
        values (8, 'Bungalow');
        insert into housing.property_type
        values (9, 'Town house');
        insert into housing.property_type
        values (10, 'Cottage');        
        insert into housing.property_type
        values (11, 'Farm/Barn');
        insert into housing.property_type
        values (12, 'Mobile/static');
        insert into housing.property_type
        values (13, 'Land');
        insert into housing.property_type
        values (14, 'Studio');
        insert into housing.property_type
        values (15, 'Block of flats');
        insert into housing.property_type
        values (16, 'Office');
    '''
