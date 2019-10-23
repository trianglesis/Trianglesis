# Load / unload data
# Make calculations and etc
import os, re, datetime
from pytz import timezone
from win_settings import MEDIA_ROOT
from banking.models import CardOperations

# Python logger
import logging

log = logging.getLogger("core.corelogger")


class InputRecords:

    def read_file(self, file_path):
        """
        Open CSV file of bank account history and read
        :param file_path:
        :return:
        """
        log.debug("Reading file: %s", file_path)

        file_data = ''
        file_dict_l = []  # List of dicts, where dict is parsed row from banking file
        sum_re = re.compile(r'\"(\d+),(\d+\.\d+)\"')

        i = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                i += 1
                # log.debug("Line No: %s", i)
                if "Номер рахунку" in line:
                    pass
                else:
                    line = re.sub(sum_re, r'\1\2', line)
                    parsed_line = self.parse_file(line=line)
                    if parsed_line:
                        file_dict_l.append(parsed_line)
                if i == 30:
                    log.warning("Stop after 30 lines!")
                    break

        return file_dict_l

    def parse_file(self, line):
        """
        Parse opened file and make dicts of values based on content rows
        :param line:
        :return:
        """
        # log.debug("Bank sheet row: %s", line)
        # Before split - ensure money sum is converted from  "11,000.00"

        tuple_line = tuple(line.split(','))  # Split CSV, remove line ending \n
        log.debug("tuple_line: %s", tuple_line)

        dict_line = dict(
            account_number=tuple_line[0],
            operation_type=tuple_line[1],
            # 25.10.2015 01:08:46
            operation_date=datetime.datetime.strptime(
                tuple_line[2], '%d.%m.%Y %H:%M:%S').replace(tzinfo=timezone('Europe/Kiev')),
            # 26.10.2015
            operation_bank_date=datetime.datetime.strptime(
                tuple_line[3], '%d.%m.%Y').replace(tzinfo=timezone('Europe/Kiev')),
            operation_description=tuple_line[4],
            operation_sum=float(tuple_line[5]) if tuple_line[5] else 0,
            operation_currency=tuple_line[6],
            operation_sum_by_account_currency=float(tuple_line[7]) if tuple_line[7] else 0,
            account_currency=tuple_line[8],
            company_code=tuple_line[9].replace('\n', ''),
        )
        log.debug("Dict line: %s", dict_line)

        return dict_line

    def insert_data(self, data):
        """
        Use parsed data dicts to insert into DB
        :param data:
        :return:
        """
        log.debug("Data to insert: %s", data)
        for item in data:
            insert = CardOperations.objects.update_or_create(**item)
        return True

    @staticmethod
    def get_files(user=None, user_id=None):
        """
        Go to user banking files and get list
        :return:
        """
        if user and not user_id:
            path = 'upload/user_media/files/user_{}/banking'.format(user.id)
        elif not user and user_id:
            path = 'upload/user_media/files/user_{}/banking'.format(user_id)
        else:
            pass

        hard_path = 'upload/user_media/files/user_6/banking'
        log.debug("Path to baking files: %s", hard_path)

        supported_files = ['csv', ]
        found_files = []
        if os.path.exists(hard_path):
            for file_ in os.listdir(hard_path):
                for ext in supported_files:
                    if file_.endswith(ext):
                        log.debug("Supported file type found: %s", file_)
                        if file_ not in found_files:
                            found_files.append(os.path.join(hard_path, file_))
        log.debug("Files to proceed: %s", found_files)
        return found_files

    def file_proceed(self, user=None, files_list=None):
        inserted = ''
        parsed_data = ''
        if not files_list and user:
            files_list = self.get_files(user)

        for file_path_ in files_list:
            log.debug("File file_path_: %s", file_path_)
            file_fill_path = os.path.normpath(MEDIA_ROOT) + os.path.normpath(file_path_)
            log.debug("File file_fill_path: %s", file_fill_path)
            parsed_data = self.read_file(file_path=file_fill_path)

            if parsed_data:
                # log.debug("Parsed data: %s", parsed_data)
                inserted = self.insert_data(data=parsed_data)
        # Fin
        return inserted