import argparse
import logging
import pathlib
import sys
import time
import typing
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Tuple

import confuse
import tldextract
from loopia_update_ip.lib.LoopiaAPI import LoopiaAPI
from loopia_update_ip.lib.get_external_ip import get_external_ip


def get_config(command_line_args) -> dict:

    config = confuse.Configuration('loopia_update_ip', __name__)

    # Allow for picking up Docker configuration
    docker_config_path = pathlib.Path('/config/config.yaml')
    if docker_config_path.is_file():
        print(' Docker configuration file found!')
        config.set_file(docker_config_path.as_posix())
    else:
        print(' Docker configuration file NOT found!')

    # Set template for confuse
    template = {
        'credentials': confuse.OrderedDict({
            'loopia_username': str,
            'loopia_password': str,
        }),
        'domains': confuse.MappingValues({
            'sub_domains': list,
            'ttl': int
        })
    }

    # Get configuration from environmental variables
    config.set_env(prefix='LOOPIAAPI_')

    # Set configuration from command line
    config.set(command_line_args)

    # Verify that the configuration is correct according to template
    try:
        valid_config = config.get(template)
    except confuse.NotFoundError as e:
        sys.exit(f' ERROR: Required variable not set: {e}')

    if valid_config['domains'] == {}:
        sys.exit(" ERROR: No domains to update was provided. Exiting!")

    return valid_config


def get_command_line_arguments() -> Tuple[dict, str]:
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--username", type=str, help=" Your API-username for loopia, i.e 'myname'@loopiaapi.")
    parser.add_argument("--password", type=str, help=" Your API-password for loopia.")
    parser.add_argument("--ip",
                        default=get_external_ip(),
                        help="The IP address to point the domain zone record to, i.e. 127.0.0.1."
                             " Default resolves external ip.")
    parser.add_argument("--domain", type=tldextract.extract, help="FQDN for domain to update i.e. www.mydomain.com")
    parser.add_argument("--ttl", type=int, default=3600, help="Time To Live for zone record. Defaults to 3600 seconds")

    # Check arguments
    try:
        args = parser.parse_args()
    except SystemExit:
        # Print help before exiting
        parser.print_help()
        exit(2)

    # Get provided arguments
    cmd_line_arguments = dict()
    cmd_line_arguments['credentials'] = dict()

    if args.domain is not None:
        cmd_line_arguments['domains'] = dict()

        # Get domain and subdomain
        subdomain = args.domain.subdomain
        domain = '.'.join(args.domain[1:])

        cmd_line_arguments['domains'][domain] = dict()
        cmd_line_arguments['domains'][domain]['sub_domains'] = [subdomain, ]
        cmd_line_arguments['domains'][domain]['ttl'] = args.ttl

    if args.username is not None:
        cmd_line_arguments['credentials']['loopia_username'] = args.username

    if args.password is not None:
        cmd_line_arguments['credentials']['loopia_password'] = args.password

    return cmd_line_arguments, args.ip


def update():
    # Retrieve arguments from user input
    cmd_arguments, ip = get_command_line_arguments()

    # Get configuration from user space and environmental variables
    config = get_config(cmd_arguments)

    # Get credentials
    username = config['credentials']['loopia_username']
    password = config['credentials']['loopia_password']

    # Update IP for requested domains
    loop_objects = dict()

    for domain in config['domains']:
        current_domain = loop_objects[domain] = LoopiaAPI(username, password, domain)

        for subdomain in config['domains'][domain]['sub_domains']:
            current_zone_record_ip = current_domain.get_zone_record_subdomain_ip_address(subdomain)
            print(f' Domain: {subdomain}.{domain}: Zone record {current_zone_record_ip} - External IP {ip}')
            if current_zone_record_ip != ip:
                current_domain.update_subdomain_ip_address(ip, subdomain)
            else:
                print('\t No update required!')


def update_txt_records():
    # Retrieve arguments from user input
    cmd_arguments, ip = get_command_line_arguments()

    # Get configuration from user space and environmental variables
    config = get_config(cmd_arguments)

    # Get credentials
    username = config['credentials']['loopia_username']
    password = config['credentials']['loopia_password']

    # Update IP for requested domains
    loop_objects = dict()

    for domain in config['domains']:
        current_domain = loop_objects[domain] = LoopiaAPI(username, password, domain)

        for subdomain in config['domains'][domain]['sub_domains']:
            zone_records = current_domain.get_zone_record_subdomain_txt_records(subdomain)

            new_txt_record = f'loopia-bot=Checked UTC {datetime.now().isoformat()}'

            records = list()
            for zone_record in zone_records:
                if zone_record['rdata'].startswith("loopia-bot="):
                    records.append(zone_record)

            # Cleanup excess records
            if len(records) >= 1:

                # Remove excess records
                for record in records[1:]:
                    current_domain.remove_txt_zone_record_subdomain(record['rdata'], subdomain)

                # Reuse first record
                old_txt_record = records[0]['rdata']
                # Update record
                current_domain.replace_txt_zone_record_subdomain(new_txt_record, old_txt_record, subdomain)

            # If now TXT records were available, create one
            else:
                current_domain.add_zone_record_subdomain(new_txt_record, subdomain, record_type='TXT')


def log_handling(log_file: pathlib.Path) -> typing.Tuple[logging.Logger, logging.Handler]:
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

    app_log = logging.getLogger('root')
    app_log.setLevel(logging.INFO)

    # Add log handler to file
    logfile_handler = RotatingFileHandler(log_file,
                                          mode='a',
                                          maxBytes=5 * 1024 * 1024,
                                          backupCount=2,
                                          encoding=None,
                                          delay=False)
    logfile_handler.setFormatter(log_formatter)
    logfile_handler.setLevel(logging.INFO)
    app_log.addHandler(logfile_handler)

    # Add log handler to stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stdout_handler.setFormatter(formatter)
    app_log.addHandler(stdout_handler)

    return app_log, logfile_handler


# Keep on running until shut down
def service():

    # Time between checking of external IP changes
    delay = 300

    print(" Starting service", flush=True)
    try:
        if pathlib.Path('/logs').is_dir():
            log_path = pathlib.Path('/logs')
        else:
            log_path = pathlib.Path.cwd()
        log_path = log_path.joinpath('loopia_update_ip.log')
        print(f" Logging to: {log_path.as_posix()}")

        log_handler, log_file_handler = log_handling(log_path)
    except Exception as e:
        print(f' A problem was encountered: {e}')
        sys.exit(f'ERROR: Could not setup logging to file for service. '
                 f'Check write permissions at: {log_path.as_posix()}')

    # Get the external IP address
    ip_external = get_external_ip()
    if not ip_external:
        sys.exit('ERROR: External IP could not be retrieved! Exiting!')
    # Set initial state
    ip_new = ip_external

    # Perform update
    update()
    # Set updated bot message
    update_txt_records()

    print(f'Service has started, waiting {delay}s until next renewal', flush=True)

    try:
        for i in range(0, delay, 5):
            time.sleep(5)

        while True:
            try:
                if ip_new != ip_external:
                    log_handler.info(f'New External IP-address. Changed from {ip_external} to {ip_new}')

                    ip_external = ip_new
                    update()

                else:
                    log_handler.info(f'External IP-address is still {ip_external}')

                # Set updated bot message
                update_txt_records()

                # Wait until next check
                for i in range(0, delay, 5):
                    time.sleep(5)

                # Check external IP
                ip_new_test = get_external_ip()
                # If external IP could not be resolved, handle it
                if ip_new_test:
                    ip_new = ip_new_test
                else:
                    log_handler.warning('WARNING: External IP could not be resolved')

            except Exception as e:
                log_handler.error(f'A problem was encountered: {e}')
                continue
    except KeyboardInterrupt:
        log_handler.info('Program terminated by KeyboardInterrupt')

    finally:
        log_file_handler.close()
        pass


if __name__ == "__main__":
    update()
    service()
