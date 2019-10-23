if __name__ == "__main__":

    import django
    # Python logger
    import logging

    django.setup()
    from banking.data_operations import *


    log = logging.getLogger("core.corelogger")


    # Sep calls
    log.debug("RUNNING LOCAL TEST DEV BANKING")
    # _read_file = InputRecords().read_file(file_path='')

    # _parse_file = InputRecords().parse_file(line='')

    # _insert_data = InputRecords().insert_data(data='')

    # _get_files = InputRecords().get_files(user='')

    files_list_debug = [
        '/user_media/files/user_6/banking/example.csv'
    ]
    _file_proceed = InputRecords().file_proceed(user=None, files_list=files_list_debug)
