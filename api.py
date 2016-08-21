#!/usr/bin/env python

import requests
from urllib.parse import urlencode
import logging
from time import sleep
from parameters import Parameters

log = logging.getLogger(__name__)

def api(version, **kwargs):
    if version == 1:
        return _ApiVersion1(**kwargs)
    else:
        raise ValueError("Unsupported API version: '{}'".format(version))

class PropertyListing(object):
    def __init__(self, member_variables):
        self.__dict__ = member_variables


class _ApiVersion1(object):
    def __init__(self, api_key, session_id=None, cache_seconds=(12 * 60 * 60)):
        self.api_key = api_key

    def _make_url(self, command, arguments):
        arguments['api_key'] = self.api_key
        url = "{}{}.js?{}".format(Parameters.API_BASE_URL, command,urlencode(sort_dict(arguments)))
        log.debug(url)
        return url

    def _call_api(self, command, arguments):
        url = self._make_url(command, arguments)
        content = download_url(url)
        if 'error_code' in content:
            raise RuntimeError("Error {}: {}".format(content['error_code'], content['error_string']))
        return content

    def _call_api_paged(self, command, args, max_results, result_processor):

        num_yielded = 0
        num_yielded_in_loop = 0
        args['page_size'] = Parameters.API_PAGE_SIZE
        args['page_number'] = 1
        result_count = None

        def reached_limit(number, limit):
            return number >= limit if limit is not None else False

        def finished():
            log.debug("yielded: {}, max_results: {}, result_count: {}".format(num_yielded, max_results, result_count))
            if reached_limit(num_yielded, max_results):
                log.debug("Stop paging, yielded={}, max_results={}".format(
                    num_yielded, max_results))
                return True
            elif reached_limit(num_yielded, result_count):                      
                log.debug("Stop paging, yielded={}, result_count={}".format(num_yielded, result_count))
                return True
            else:
                return False

        while not finished():
            sleep(40)
            response = self._call_api(command, args)
            result_count = response['result_count'] - 1         # note I added a -1 here because I was getting an off-by-one causing looping meaning I used up all my quota
            num_yielded_in_loop = 0

            for listing in result_processor(response):
                yield listing
                num_yielded += 1
                num_yielded_in_loop += 1
                if finished():
                    break

            if num_yielded_in_loop < 5:                        # an extra safety, this breaks the loop if we didn't get at least 5 results...
                break

            args['page_number'] += 1


    def property_listings(self, max_results=100, **kwargs):

        log.debug('property_listings(max_results={}, {})'.format(max_results, kwargs))
        
        result_processor = self._create_listings

        generator = self._call_api_paged('property_listings', kwargs, max_results, result_processor)

        for listing in generator:
            yield listing

    def _create_listings(self, api_response):

        response_meta = dict(api_response)
        del response_meta['listing']
        log.debug("response meta: {}".format(response_meta))

        listings = api_response['listing']
        log.debug("{} listings".format(len(listings)))

        for listing in listings:
            listing['meta'] = response_meta
            yield PropertyListing(listing)


def download_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def sort_dict(some_dict):
    return sorted(some_dict.items())