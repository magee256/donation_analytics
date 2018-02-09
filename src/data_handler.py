import datetime


class StreamingDataframe:
    delim = '|'
    header_to_index = {
        'CMTE_ID': 0,
        'NAME': 7,
        'ZIP_CODE': 10,
        'TRANSACTION_DT': 13,
        'TRANSACTION_AMT': 14,
        'OTHER_ID': 15}
    
    def __init__(self, input_file):
        self.input_file = input_file
        
    def __enter__(self):
        self.data_stream = open(self.input_file, 'r')
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.data_stream.close()
        if exc_type:
            raise
        
    def __iter__(self):
        for line in self.data_stream:
            entries = line.split(self.delim)
            data_dict = {header: entries[self.header_to_index[header]]
                         for header in self.header_to_index.keys()}
            valid_entry = self._clean_and_validate_data(data_dict)
            if valid_entry:
                yield data_dict
    
    def _clean_and_validate_data(self, data_dict):
        for header, value in data_dict.items():
            handler = getattr(self, '_handle_' + header, 
                              lambda x: (True, x))
            valid, data_dict[header] = handler(value)
            if not valid:
                return False
        return True
    
    # FIELD  HANDLERS
    # All handlers return a (valid flag, cleaned value) tuple
    # Record skipped if valid flag False
    @staticmethod
    def _handle_CMTE_ID(field):
        # Must have something for CMTE_ID
        return bool(field.strip()), field
        
    @staticmethod
    def _handle_NAME(field):
        # Must have a single comma separating first and last name
        name = field.split(',')
        return len(name) == 2, field
        
    @staticmethod
    def _handle_ZIP_CODE(field):
        # Must be at least five characters
        zip_code = field[:5]
        if len(zip_code) != 5:
            return False, None
        
        # Those characters should be numbers
        try:
            assert int(zip_code) >= 0
        except (ValueError, AssertionError):
            return False, None
        return True, zip_code
        
    @staticmethod
    def _handle_TRANSACTION_DT(field):
        # Only interested in year. Data recording started 1975.
        # Can't have contributions after current year
        min_year = 1975
        max_date = (
            datetime.datetime.now() 
          + datetime.timedelta(days=1)  # Add a day in case of timezone differences
        )
        
        # Properly formatted valid date
        try:
            cur_date = datetime.datetime.strptime(field, '%m%d%Y')
        except ValueError:
            return False, None
        return ((cur_date.year >= min_year) and (cur_date <= max_date)), cur_date

    @staticmethod
    def _handle_TRANSACTION_AMT(field):
        # Must have a number for TRANSACTION_AMT
        try:
            amount = float(field)
            assert amount > 0
        except (ValueError, AssertionError):
            return False, None
        return True, amount
        
    @staticmethod
    def _handle_OTHER_ID(field):
        # The OTHER_ID field must be blank
        return (not field.strip()), field
