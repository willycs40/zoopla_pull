class Parameters:

    DB_HOST = 'mysql'
    DB_USER = 'will'
    DB_PASSWORD = 'housepass'
    DB_SCHEMA = 'housing'

    API_BASE_URL = 'http://api.zoopla.co.uk/api/v1/'
    API_SLEEP_DELAY_PER_PAGE = 3
    API_PAGE_SIZE = 100

    BASE_OUTPUT_FILE_NAME ='output/output_{}.csv'

    BASE_API_PARAMETERS = {
        'postcode': 'b23',
        'order_by': 'age',
        'max_results': 2000,
        'include_sold': 1,
        'include_rented': 1,
        'summarised': 'true'
    }

    BIRMINGHAM_OUTCODES = ['CV7', 'B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','B11','B12','B13','B14','B15','B16','B17','B18','B19','B20','B21','B23','B24','B25','B26','B27','B28','B29','B30','B31','B32','B33','B34','B35','B36','B37','B38','B40','B42','B43','B44','B45','B46','B47','B48','B49','B50','B60','B61','B62','B63','B64','B65','B66','B67','B68','B69','B70','B71','B72','B73','B74','B75','B76','B77','B78','B79','B80','B90','B91','B92','B93','B94','B95','B96','B97','B98']
    LONDON_OUTCODES = ['E1','E2','E3','E4','E5','E6','E7','E8','E9','E10','E11','E12','E13','E14','E15','E16','E17','E18','E20','EC1','EC2','EC3','EC4','N1','N2','N3','N4','N5','N6','N7','N8','N9','N10','N11','N12','N13','N14','N15','N16','N17','N18','N19','N20','N21','N22','NW1','NW2','NW3','NW4','NW5','NW6','NW7','NW8','NW9','NW10','NW11','SE1','SE2','SE3','SE4','SE5','SE6','SE7','SE8','SE9','SE10','SE11','SE12','SE13','SE14','SE15','SE16','SE17','SE18','SE19','SE20','SE21','SE22','SE23','SE24','SE25','SE26','SE27','SE28','SW1','SW2','SW3','SW4','SW5','SW6','SW7','SW8','SW9','SW10','SW11','SW12','SW13','SW14','SW15','SW16','SW17','SW18','SW19','SW20','W1','W2','W3','W4','W5','W6','W7','W8','W9','W10','W11','W12','W13','W14','WC1','WC2','BR1','BR2','BR2','BR3','BR4','BR5','BR6','BR7','BR8','CR0','CR9','CR2','CR4','CR5','CR6','CR7','CR8','DA1','DA5','DA6','DA7','DA8','DA18','DA14','DA15','DA16','DA17','EN1','EN2','EN3','EN4','EN5','EN8','HA0','HA9','HA1','HA2','HA3','HA4','HA5','HA6','HA7','HA8','IG1','IG2','IG3','IG4','IG5','IG6','IG7','IG8','IG11','KT1','KT2','KT3','KT4','KT5','KT6','KT9','RM1','RM2','RM3','RM4','RM5','RM6','RM7','RM8','RM9','RM10','RM11','RM12','RM13','RM14','SM1','SM2','SM3','SM4','SM5','SM6','TN14','TN16','TW1','TW2','TW3','TW4','TW5','TW6','TW7','TW8','TW9','TW10','TW11','TW12','TW13','TW14','UB1','UB2','UB3','UB4','UB5','UB6','UB7','UB8','UB9','UB10']
    OUTCODES = BIRMINGHAM_OUTCODES + LONDON_OUTCODES

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
            , timestamp
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

    SQL_STAGE_LISTING_HEADER = '''
        insert into housing.listing_stage(
            batch_id
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
        values 
        '''
    
    SQL_STAGE_LISTING_VALUES = '''    
        (
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

    SQL_MERGE_STAGE = ['''
        insert into housing.property_type(property_type)
        select property_type
        from listing_stage
        where property_type <> ''
        and property_type not in (select property_type from property_type)
        group by property_type;
    ''','''
        insert into housing.price_modifier(price_modifier)
        select price_modifier
        from listing_stage
        where price_modifier <> ''
        and price_modifier not in (select price_modifier from price_modifier)
        group by price_modifier;
    ''','''
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
            , price_modifier_id
            , property_type_id 
            , new_home 
            , latitude 
            , longitude 
            , first_published_date 
            , last_published_date
        )
        select      l.batch_id
                    , l.listing_id
                    , l.outcode
                    , l.num_bathrooms
                    , l.num_bedrooms
                    , l.num_floors
                    , l.num_recepts
                    , ls.listing_status_id
                    , s.status_id 
                    , l.price 
                    , pm.price_modifier_id
                    , pt.property_type_id 
                    , case when l.new_home='true' then 1 else 0 end
                    , l.latitude 
                    , l.longitude 
                    , l.first_published_date 
                    , l.last_published_date
        from        listing_stage l
        left join   listing_status ls
        on          l.listing_status = ls.listing_status
        left join   status s
        on          l.status = s.status
        left join   property_type pt
        on          l.property_type = pt.property_type
        left join   price_modifier pm
        on          l.price_modifier = pm.price_modifier
        left join   listing ll 
        on          l.listing_id = ll.listing_id
        and         l.last_published_date = ll.last_published_date
        where       ll.listing_id is null;
    ''','''
        insert into housing.listing_address(
            listing_table_id
            , displayable_address 
            , street_name
            , image_url 
            , details_url
        )
        select l.listing_table_id
            , replace(ls.displayable_address,'^','\\'')
            , replace(ls.street_name,'^','\\'')
            , replace(ls.image_url,'^','\\'')
            , replace(ls.details_url,'^','\\'')
        from        listing l
        inner join  listing_stage ls
        on          l.listing_id = ls.listing_id
        and         l.batch_id = ls.batch_id;
    ''']

    SQL_INITIALISE = ['''
        create table if not exists housing.log (
            log_id int NOT NULL AUTO_INCREMENT
            , batch_id int
            , timestamp datetime
            , level varchar(1)
            , message varchar(500)
            , primary key (log_id)
        );
        
        ''','''

        create table if not exists housing.listing_stage (
            listing_stage_id int NOT NULL AUTO_INCREMENT
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
            , property_type varchar(50)
            , street_name varchar(250)
            , image_url varchar(250)
            , details_url varchar(250)
            , new_home varchar(5)
            , latitude float
            , longitude float
            , first_published_date datetime
            , last_published_date datetime
            , primary key (listing_stage_id)
        );

        ''','''

        create table if not exists housing.listing (
            listing_table_id int NOT NULL AUTO_INCREMENT
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
            , first_published_date datetime
            , last_published_date datetime
            , primary key (listing_table_id)
        );
        
        ''','''

        create table if not exists housing.listing_address (
            listing_address_id int NOT NULL AUTO_INCREMENT
            , listing_table_id int
            , displayable_address varchar(250)
            , street_name varchar(250)
            , image_url varchar(250)
            , details_url varchar(250)
            , primary key (listing_address_id)
        );
        
        ''','''

        create table if not exists housing.listing_status (
            listing_status_id int
            , listing_status varchar(5)
            , primary key (listing_status_id)
        );
        
        ''','''

        insert into housing.listing_status
        values (1, 'sale'),
            (2, 'rent');
        
        ''','''

        create table if not exists housing.status (
            status_id int
            , status varchar(20)
            , primary key (status_id)
        );
        
        ''','''

        insert into housing.status
        values (1, 'for_sale'),
            (2, 'sale_under_offer'),
            (3, 'sold'),
            (4, 'to_rent'),
            (5, 'rent_under_offer'),
            (6, 'rented');   

        ''','''
            
        create table if not exists housing.price_modifier (
            price_modifier_id int NOT NULL AUTO_INCREMENT
            , price_modifier varchar(20)
            , primary key (price_modifier_id)
        );

        ''','''
        
        create table if not exists housing.property_type (
            property_type_id int NOT NULL AUTO_INCREMENT
            , property_type varchar(50)
            , primary key (property_type_id)
        );                   

        ''','''

        insert into housing.log(batch_id, timestamp, level, message)
        values (1, now(), 'I', 'Database created');
    ''']
