import xmlrpc.client
from typing import List


class LoopiaAPI:
    def __init__(self, username: str, password: str, domain: str):
        self.username: str = username
        self.password: str = password
        self.domain: str = domain

        global_domain_server_url = 'https://api.loopia.se/RPCSERV'
        self.client = xmlrpc.client.ServerProxy(global_domain_server_url)

    def get_domain(self) -> str:
        return self.domain

    def get_subdomains(self) -> list:
        try:
            response = self.client.getSubdomains(self.username, self.password, self.domain)
        except xmlrpc.client.Fault as error_msg:
            print(f' ERROR: API-endpoint replied: {error_msg.faultCode} - {error_msg.faultString}')
            return ['ERROR', ]
        return response

    def check_if_subdomain_is_defined(self, subdomain: str) -> bool:
        try:
            response = self.client.getSubdomains(self.username, self.password, self.domain)
        except xmlrpc.client.Fault as error_msg:
            print(f' ERROR: API-endpoint replied: {error_msg.faultCode} - {error_msg.faultString}')
            return False
        if subdomain in response:
            return True
        else:
            return False

    def add_subdomain(self, subdomain) -> str:
        """
        Add a new subdomain to the domain
        :param subdomain: Name of new subdomain
        :return:  Loopia API endpoint status report
        """
        print(f' Adding subdomain "{subdomain}.{self.domain}"')
        try:
            response = self.client.addSubdomain(self.username, self.password, self.domain, subdomain)
        except xmlrpc.client.Fault as error_msg:
            return error_msg.faultString

        return response

    def remove_subdomain(self, subdomain) -> str:
        """
        Remove a subdomain from the domain
        :param subdomain: Name of subdomain to remove
        :return:  Loopia API endpoint status report
        """
        print(f' Removing subdomain "{subdomain}.{self.domain}"')
        try:
            response = self.client.removeSubdomain(self.username, self.password, self.domain, subdomain)
        except xmlrpc.client.Fault as error_msg:
            return error_msg.faultString
        return response

    def add_zone_record_subdomain(self,
                                  data: str,
                                  subdomain: str,
                                  ttl: int = 3600,
                                  record_type: str = "A",
                                  priority: int = 0) -> str:
        """
        Add a new zone record for a subdomain
        :param data: IP address for zone record of A-type, Data for TXT type and for other record types
        :param subdomain: Where to add the zone record
        :param ttl: Time to live for the zone record. Defaults to 3600 for Loopia
        :param record_type: Type of record to add
        :param priority: Priority order of records
        :return:  Loopia API endpoint status report
        """
        record_object = LoopiaAPI.create_record_dict(record_type=record_type,
                                                     ttl=ttl,
                                                     priority=priority,
                                                     rdata=data,
                                                     record_id=0)

        try:
            record_list = self.client.getZoneRecords(self.username,
                                                     self.password,
                                                     self.domain,
                                                     subdomain)
        except xmlrpc.client.Fault as error_msg:
            return error_msg.faultString

        # Only allow multiple TXT records
        if len(record_list) >= 1 and record_type != 'TXT':
            for record in record_list:
                if record['type'] == record_type:
                    return f'ERROR: Subdomain {subdomain}.{self.domain} with record of type {record_type} exists.'

        try:
            response = self.client.addZoneRecord(self.username,
                                                 self.password,
                                                 self.domain,
                                                 subdomain,
                                                 record_object)
        except xmlrpc.client.Fault as error_msg:
            return error_msg.faultString

        return response

    def update_zone_record_subdomain(self, data: str, subdomain: str, record_type: str = "A", ttl=3600) -> str:
        """
        Update zone record for subdomain. I.e. only a single record is supported!
        :param data: IP address for zone record of A-type, Data for TXT type and for other record types
        :param subdomain: The subdomain for which to update the zone record
        :param record_type: Type of record to update
        :param ttl: Time to live for zone record - Defaults to 3600 for Loopia domains
        :return:  Loopia API endpoint status report
        """
        try:
            record_list = self.client.getZoneRecords(self.username,
                                                     self.password,
                                                     self.domain,
                                                     subdomain)
        except xmlrpc.client.Fault as error_msg:
            return str(error_msg)

        if len(record_list) >= 2:

            temp_list = list()
            for record in record_list:
                if record['type'] == record_type:
                    temp_list.append(record)

            if len(temp_list) > 1:
                return f'ERROR: Subdomain {subdomain}.{self.domain} has multiple records of type {record_type}.'

            zone_record = temp_list[0]
            zone_record['rdata'] = data
            zone_record['ttl'] = ttl

        elif len(record_list) == 1:
            zone_record = record_list[0]
            zone_record['rdata'] = data
            zone_record['ttl'] = ttl

        elif len(record_list) == 0:
            print(' ERROR: No zone record has been previously defined')
            return ' ERROR: No zone record has been previously defined'

        try:
            response = self.client.updateZoneRecord(self.username,
                                                    self.password,
                                                    self.domain,
                                                    subdomain,
                                                    zone_record)
        except xmlrpc.client.Fault as error_msg:
            return error_msg.faultString

        return response

    def replace_txt_zone_record_subdomain(self, new_data: str, replace_data: str, subdomain: str, ttl=3600) -> str:
        """
        Update zone record for subdomain. I.e. only a single record is supported!
        :param new_data: New data for TXT data
        :param replace_data: TXT data to replace if exact match
        :param subdomain: The subdomain for which to update the zone record
        :param ttl: Time to live for zone record - Defaults to 3600 for Loopia domains
        :return:  Loopia API endpoint status report
        """
        try:
            record_list = self.client.getZoneRecords(self.username,
                                                     self.password,
                                                     self.domain,
                                                     subdomain)
        except xmlrpc.client.Fault as error_msg:
            return str(error_msg)

        zone_record = None
        if len(record_list) >= 1:
            # Loop through records and check if a record matches
            for record in record_list:
                if record['type'] == 'TXT' and record['rdata'] == replace_data:
                    zone_record = record
                    zone_record['rdata'] = new_data

        if not zone_record:
            print('ERROR: No zone record matched the provided data')
            return ' ERROR: No zone record matched the provided data'

        elif len(record_list) == 0:
            print(' ERROR: No zone record has been previously defined')
            return ' ERROR: No zone record has been previously defined'

        try:
            response = self.client.updateZoneRecord(self.username,
                                                    self.password,
                                                    self.domain,
                                                    subdomain,
                                                    zone_record)
        except xmlrpc.client.Fault as error_msg:
            return error_msg.faultString

        return response

    def remove_txt_zone_record_subdomain(self, data: str, subdomain: str) -> str:
        """
        Update zone record for subdomain. I.e. only a single record is supported!
        :param data: TXT data of record to remove
        :param subdomain: The subdomain for which to update the zone record
        :return:  Loopia API endpoint status report
        """
        try:
            record_list = self.client.getZoneRecords(self.username,
                                                     self.password,
                                                     self.domain,
                                                     subdomain)
        except xmlrpc.client.Fault as error_msg:
            return str(error_msg)

        zone_record_id = None
        if len(record_list) >= 1:
            # Loop through records and check if a record matches
            for record in record_list:
                if record['type'] == 'TXT' and record['rdata'] == data:
                    zone_record_id = record['record_id']

        if not zone_record_id:
            print('ERROR: No zone record matched the provided data')
            return ' ERROR: No zone record matched the provided data'

        try:
            print(f"Removing zone record type TXT - data: {data} for domain {subdomain}.{self.domain}")
            response = self.client.removeZoneRecord(self.username,
                                                    self.password,
                                                    self.domain,
                                                    subdomain,
                                                    zone_record_id)
        except xmlrpc.client.Fault as error_msg:
            return error_msg.faultString

        return response

    def remove_zone_records_subdomain(self, subdomain: str) -> List[str]:
        """
        Remove all zone records for the selected subdomain even if there are multiple
        :param subdomain: Subdomain for which all zone records are to be removed
        :return:  Loopia API endpoint status report
        """
        try:
            record_list = self.client.getZoneRecords(self.username,
                                                     self.password,
                                                     self.domain,
                                                     subdomain)
        except xmlrpc.client.Fault as error_msg:
            print(f' ERROR: Zone records for subdomain could not be retrieved: {error_msg.faultString}')
            return [error_msg.faultString, ]

        responses = list()
        for record in record_list:
            try:
                # Get record id
                record_id = record['record_id']
                # Remove zone record by record id
                response = self.client.removeZoneRecord(self.username,
                                                        self.password,
                                                        self.domain,
                                                        subdomain,
                                                        record_id)
                responses.append(response)
            except xmlrpc.client.Fault as error_msg:
                responses.append(error_msg.faultString)

        return responses

    def get_zone_record_subdomain_ip_address(self, subdomain: str) -> str:
        """
        Get current IP address from zone record for subdomain. Note: Only a single A-record is supported!
        :param subdomain: The subdomain for which to update the zone record
        :return:  IP-address for subdomain zone record
        """
        try:
            record_list = self.client.getZoneRecords(self.username,
                                                     self.password,
                                                     self.domain,
                                                     subdomain)
        except xmlrpc.client.Fault as error_msg:
            print(f' ERROR: Could not retrieve zone records for {subdomain}.{self.domain}'
                  f'\t\t{error_msg}')
            return ""

        if len(record_list) >= 1:
            # Loop through records and check if a record matches type A
            for record in record_list:
                if record['type'] == 'A':
                    return record['rdata']

        elif len(record_list) == 0:
            print(' ERROR: No zone record has been previously defined')
            return ""

        # Catch if no A record were found
        return ""

    def get_zone_record_subdomain_txt_records(self, subdomain: str) -> list:
        """
        Get all TXT record for subdomain
        :param subdomain: The subdomain for which to request the zone records
        :return:  All TXT zone records
        """
        try:
            record_list = self.client.getZoneRecords(self.username,
                                                     self.password,
                                                     self.domain,
                                                     subdomain)
        except xmlrpc.client.Fault as error_msg:
            print(f' ERROR: Could not retrieve zone records for {subdomain}.{self.domain}'
                  f'\t\t{error_msg}')
            return list()

        zone_record_txt = list()
        if len(record_list) >= 1:
            # Loop through records and check if a record matches type A
            for record in record_list:
                if record['type'] == 'TXT':
                    zone_record_txt.append(record)
            return zone_record_txt

        elif len(record_list) == 0:
            print(' ERROR: No zone record has been previously defined')
            return list()

        # Catch if no TXT record were found
        return list()

    def update_subdomain_ip_address(self, ip: str, subdomain: str, ttl: int = 3600) -> str:
        """
        Update IP address associated with subdomain A-record
        :param ip: New IP address to assign
        :param subdomain: subdomain to update
        :param ttl: Time to live for zone record
        :return: Loopia API endpoint status report
        """

        print(f'\t*** Updating zone record to {ip} for {subdomain}.{self.domain}\n')

        # Check if subdomain exists, if not create it.
        if self.check_if_subdomain_is_defined(subdomain):
            try:
                subdomain_records = self.client.getZoneRecords(self.username,
                                                               self.password,
                                                               self.domain,
                                                               subdomain)
            except xmlrpc.client.Fault as error_msg:
                print(f' ERROR: API-endpoint replied: {error_msg.faultCode} - {error_msg.faultString}')
                return error_msg.faultString
        else:
            print(f' Subdomain {subdomain} was not found in domain {self.domain}, creating it')
            response = self.add_subdomain(subdomain)
            if not response == 'OK':
                print(f' ERROR: Subdomain {subdomain} could not be created for domain {self.domain}\n'
                      f' \t API-endpoint error: {response}')
                return "ERROR"
            # Since just defined, no zone record exist!
            subdomain_records = []

        if len(subdomain_records) >= 2:
            print(' ERROR: Multiple DNS records defined which is not supported')
            return ' ERROR: Multiple DNS records defined which is not supported'

        elif len(subdomain_records) == 1:
            # Replace IP address in zone record
            subdomain_record = subdomain_records[0]
            subdomain_record['rdata'] = ip

            # Update zone record with new IP address
            try:
                response = self.client.updateZoneRecord(self.username,
                                                        self.password,
                                                        self.domain,
                                                        subdomain,
                                                        subdomain_record)
            except xmlrpc.client.Fault as error_msg:
                return error_msg.faultString

        elif len(subdomain_records) == 0:
            subdomain_record = self.create_record_dict('A', ttl, 0, ip, 0)

            # Create zone record with IP address
            try:
                response = self.client.addZoneRecord(self.username,
                                                     self.password,
                                                     self.domain,
                                                     subdomain,
                                                     subdomain_record)
            except xmlrpc.client.Fault as error_msg:
                return error_msg.faultString
        else:
            print(' ERROR: Unknown state happened... ')
            response = 'Not OK'

        return response

    @staticmethod
    def create_record_dict(record_type: str, ttl: int, priority: int, rdata: str, record_id: int) -> dict:
        record_dict = dict()
        record_dict['type'] = record_type
        record_dict['ttl'] = ttl
        record_dict['priority'] = priority
        record_dict['rdata'] = rdata
        record_dict['record_id'] = record_id
        return record_dict
