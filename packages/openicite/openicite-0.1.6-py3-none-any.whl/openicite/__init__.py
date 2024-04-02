import requests
import time
from functools import wraps

def measure_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print_info = kwargs.pop('print_info', True)  # Extracts print_info from keyword arguments, defaults to True if not provided
        response = func(*args, **kwargs)
        if print_info:
            print(f"Request Time: {round(response.elapsed.total_seconds(),3)} s")
            print(f"File Size: {round(len(response.content)/1024,3)} kB")
        return response
    return wrapper

class Openicite():
    BASE_URL = "https://icite.od.nih.gov/api"

    def __init__(self):
        """Initialize the client."""        
        self.api_url = f'{self.BASE_URL}/pubs'
        self.per_requests = 1000
        self.sleep = 0.05
    
    
    def get_icite(self, pmid, timeout=500, print_info=True):  # Add print_info parameter
        """
        Send a request to the specified URL for a single PMID.
        Example URL: https://icite.od.nih.gov/api/pubs/23456789
        --------------------------------------------------------
        Parameters:
            pmid: PubMed ID for the publication,
            timeout: Timeout for the request, default is 500 seconds.
            print_info: Controls whether to print content from the decorator, defaults to True.
        Returns:
        A JSON object with publication data if successful, None otherwise.
        """
        single_url = f'{self.api_url}/{pmid}'
        
        response = self._get_icite(single_url, timeout=timeout, print_info=print_info)  # Pass print_info parameter
        if response:
            return response.json()

        
    @measure_request
    def _get_icite(self, single_url, timeout=500):
        """
        """
        try:
            response = requests.get(single_url, timeout=timeout)
            if response.status_code == 200:
                return response
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

        
    @measure_request
    def _get_icites(self, payload, timeout=500, print_info=True):  # Add print_info parameter
        """
        """
        try:
            response = requests.get(self.api_url, params=payload, timeout=timeout)
            if response.status_code == 200:
                # Add this batch's results to the list of response data
                return response
            
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
    

    def get_icites(self, pmid_list=[], field_list=[], timeout=500, print_info=True):  # Add print_info parameter
        """
        Fetches publication data in bulk. If pmid_list exceeds 1000, it splits the requests and merges the results.
        Parameters:
            pmid_list: List of PMIDs,
            field_list: List of fields to be fetched,
            timeout: Timeout for the request, default is 500 seconds.
            print_info: Controls whether to print content from the decorator, defaults to True.
        Returns:
        A JSON object containing merged results of the requests.
        """
        per_requests = self.per_requests  # Maximum number of PMIDs per request
        responses_data = []  # To store response data from all batches
        
        # Split pmid_list into sublists of up to 1000 PMIDs each
        for i in range(0, len(pmid_list), per_requests):
            time.sleep(self.sleep)
            sub_pmid_list = pmid_list[i:i + per_requests]
            
            payload = {'pmids': ','.join(map(str, sub_pmid_list))}
            if field_list:
                payload['fl'] = ','.join(field_list)

            response = self._get_icites(payload, timeout=timeout, print_info=print_info)  # Pass print_info parameter
            if response:
                responses_data.extend(response.json().get('data', []))


        # Merge results from all batches and return
        return {
            'meta': {
                'pmids': ','.join(map(str, pmid_list)),
                'fl': ','.join(field_list)
            },
            'data': responses_data
        }


if __name__ == "__main__":
    
    icite = Openicite()
    Openicite.per_requests = 300 # Maximum of 1000 per request
    
    # get_icite
    pmid = 233333
    data = icite.get_icite(pmid, print_info=False)
    print(data)
    
    # get_icites
    pmid_list = [str(pmid) for pmid in range(400)]  # Example: Generate a list with more than 1000 PMIDs
    field_list = ['pmid', 'year', 'title', 'apt', 'relative_citation_ratio', 'cited_by_clin']
    data = icite.get_icites(pmid_list=pmid_list, field_list=field_list, print_info=True)
    print(data)