# STDLIB
import csv
from collections import OrderedDict
import logging
import pathlib
from typing import List


logger = logging.getLogger()


class CWriterObject(object):
    """
    creates a file like object to write on
    """

    def __init__(self) -> None:
        self.Buffer = ''
        pass

    def write(self, text) -> None:
        self.Buffer = self.Buffer + text


def read_csv_file_with_header_to_hashed_odict_of_odicts(file_fullpath: pathlib.Path,
                                                        hash_by_fieldname: str,
                                                        encoding: str = "ISO-8859-1",
                                                        delimiter: str = ";",
                                                        quotechar: str = '"',
                                                        quoting: int = csv.QUOTE_MINIMAL) -> 'OrderedDict[str, OrderedDict[str, str]]':
    """
    reads the csv file into an ordered dict of ordered dicts
    returns: {'indexfield':{fieldname1:value, fieldname2:value}, 'indexfield2':{fieldname1:value, fieldname2:value}}

    >>> # setup
    >>> test_directory = pathlib.Path(__file__).absolute().parent.parent / 'tests'
    >>> testfile1 = test_directory / '2018-04-26_alle_Navision_Artikel.csv'
    >>> testfile2 = test_directory / '0001_aktive_preis_qty.csv'
    >>> testfile3 = test_directory / '2018-06-06_active_qty_broken.csv'
    >>> r_csv = read_csv_file_with_header_to_hashed_odict_of_odicts

    >>> # Test Fieldname for hashing not existent in the header
    >>> r_csv(file_fullpath=testfile1, hash_by_fieldname='not_existing') # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Field "not_existing" is not available, or the csv file does not have header information

    >>> # Test OK, Fieldname for hashing is unique
    >>> r_csv(file_fullpath=testfile1, hash_by_fieldname='Nr.') # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    OrderedDict([('HUB025', OrderedDict([('HTMLpublish', 'Nein'), ('Artikel Nicht Verfügbar', 'Nein'), ('Sperre Angebot', 'Nein'), ...

    >>> # Test Fieldname for hashing is not unique
    >>> r_csv(file_fullpath=testfile2, hash_by_fieldname='CustomLabel')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Index is not unique, field: "CustomLabel", value: "HUB179"

    >>> # Test Number of Fields does not match
    >>> r_csv(file_fullpath=testfile3, hash_by_fieldname='CustomLabel')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Row has length ... instead of ... : "[...]"



    """
    with open(str(file_fullpath), 'r', encoding=encoding) as csvfile:
        is_first_row = True
        fieldnames = []
        index_of_hash_field = 0
        number_of_rows = 0
        dict_result = OrderedDict()

        my_csv_reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar, quoting=quoting)
        for row in my_csv_reader:

            if is_first_row:
                is_first_row = False
                fieldnames = row
                if hash_by_fieldname not in fieldnames:
                    raise ValueError('Field "{}" is not available, or the csv file does not have header information'.format(hash_by_fieldname))
                index_of_hash_field = fieldnames.index(hash_by_fieldname)
                number_of_rows = len(fieldnames)
                continue

            if len(row) != number_of_rows:
                raise ValueError('Row has length {} instead of {} : "{}"'.format(len(row), number_of_rows, row))

            dict_row = OrderedDict()

            for index, value in enumerate(row):
                dict_row[fieldnames[index]] = value

            index_value = row[index_of_hash_field]
            if index_value not in dict_result:
                dict_result[index_value] = dict_row
            else:
                raise ValueError('Index is not unique, field: "{}", value: "{}"'.format(hash_by_fieldname, index_value))

        return dict_result


def read_csv_file_with_header_to_list_of_odicts(file_fullpath: str,
                                                encoding: str = "ISO-8859-1",
                                                delimiter: str = ";",
                                                quotechar: str = '"',
                                                quoting: int = csv.QUOTE_MINIMAL,
                                                doublequote: bool = True,
                                                check_row_length: bool = True) -> List[OrderedDict]:
    """
    reads the csv file into a list of ordered dicts

    >>> # setup
    >>> logger.setLevel(logging.INFO)
    >>> test_directory = pathlib.Path(__file__).absolute().parent.parent / 'tests'
    >>> testfile1 = test_directory / '2018-06-06_active_qty.csv'
    >>> testfile2 = test_directory / '2018-06-06_active_qty_broken.csv'
    >>> # Test Ok
    >>> read_csv_file_with_header_to_list_of_odicts(file_fullpath=testfile1)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    [OrderedDict(...), OrderedDict(...), ...]
    >>> # Test Number of Fields not the same as in Header
    >>> read_csv_file_with_header_to_list_of_odicts(file_fullpath=testfile2)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    ValueError: Row "[...]" has not the correct length


    """

    with open(str(file_fullpath), 'r', encoding=encoding) as csvfile:
        is_first_row = True
        fieldnames = []
        number_of_rows = 0
        l_dict_result = list()

        my_csv_reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar, quoting=quoting, doublequote=doublequote)
        for row in my_csv_reader:

            if is_first_row:
                is_first_row = False
                fieldnames = row
                number_of_rows = len(fieldnames)
                continue

            if check_row_length and (len(row) != number_of_rows):
                raise ValueError('Row "{}" has not the correct length'.format(row))

            dict_data = OrderedDict()

            for index, value in enumerate(row):
                if index < number_of_rows:
                    dict_data[fieldnames[index]] = value

            l_dict_result.append(dict_data)

        return l_dict_result


def write_hashed_odict_of_odicts_to_csv_file(dict_data: OrderedDict,
                                             file_fullpath: str,
                                             encoding: str = "ISO-8859-1",
                                             delimiter: str = ";",
                                             quotechar: str = '"',
                                             quoting: int = csv.QUOTE_MINIMAL):

    with open(file_fullpath, 'w', encoding=encoding, newline='\n') as csvfile:
        my_csv_writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotechar, quoting=quoting)
        b_first_line = True
        n_number_of_fields = 0

        for value in dict_data.values():
            row = []
            # Feldnamen schreiben
            if b_first_line:
                b_first_line = False
                for fieldname in value.keys():
                    row.append(fieldname)
                n_number_of_fields = len(row)
                my_csv_writer.writerow(row)
                row = []

            for field_value in value.values():
                row.append(field_value)

            if len(row) == n_number_of_fields:
                my_csv_writer.writerow(row)
            else:
                raise ValueError('Row "{}" has not the correct length'.format(row))


def write_ll_data_to_csv_file(ll_data: List[List[str]], file_fullpath: str, encoding: str = "ISO-8859-1",
                              delimiter: str = ";", quotechar: str = '"', quoting: int = csv.QUOTE_MINIMAL, lineterminator: str = '\n',
                              escapechar: str = '"', doublequote: bool = True):
    """

    >>> # setup
    >>> logger.setLevel(logging.INFO)
    >>> test_directory = pathlib.Path(__file__).absolute().parent.parent / 'tests'
    >>> testfile = test_directory / 'export_test.csv'

    >>> # export ok
    >>> ll_data =[['a','b','c'],[1,2,True]]
    >>> write_ll_data_to_csv_file(ll_data=ll_data,file_fullpath=testfile)
    >>> read_csv_file_with_header_to_list_of_odicts(file_fullpath=testfile)
    [OrderedDict([('a', '1'), ('b', '2'), ('c', 'True')])]

    >>> # Number of Rows does not match Header
    >>> ll_data =[['a','b','c'],[1,2]]
    >>> write_ll_data_to_csv_file(ll_data=ll_data,file_fullpath=testfile)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    ValueError: row "[1, 2]" has a different length as the header line

    >>> # Nothing to export
    >>> ll_data =[]
    >>> write_ll_data_to_csv_file(ll_data=ll_data,file_fullpath=testfile)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    ValueError: Nothing to export

    >>> # EBAY needs '"' as escape character und double escape
    >>> ll_data =[['a','b','c'],[1,2,'das ist ein "TE;ST">'],[2,3,'das ist ein TE;ST']]
    >>> write_ll_data_to_csv_file(ll_data=ll_data,file_fullpath=testfile,escapechar='"')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    >>> read_csv_file_with_header_to_list_of_odicts(file_fullpath=testfile)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    [OrderedDict([('a', '1'), ('b', '2'), ('c', 'das ist ein "TE;ST">')]), OrderedDict([('a', '2'), ('b', '3'), ('c', 'das ist ein TE;ST')])]


    """
    csv.register_dialect('MyDialect', delimiter=delimiter, quotechar=quotechar, quoting=quoting,
                         doublequote=doublequote, lineterminator=lineterminator, escapechar=escapechar)

    with open(file_fullpath, 'w', encoding=encoding, newline='\n') as csvfile:
        my_csv_writer = csv.writer(csvfile, dialect='MyDialect', quoting=quoting)

        if not len(ll_data):
            raise ValueError('Nothing to export')

        number_of_fields = len(ll_data[0])

        for l_data in ll_data:
            my_csv_writer.writerow(l_data)
            if len(l_data) != number_of_fields:
                raise ValueError('row "{}" has a different length as the header line'.format(l_data))


def write_ll_data_to_csv_file_ebay(ll_data: List[List[str]],
                                   file_fullpath: str,
                                   encoding: str = "ISO-8859-1",
                                   delimiter: str = ";",
                                   quotechar: str = '"',
                                   lineterminator: str = '\n',
                                   escapechar: str = '"') -> None:
    """
    :return:    number of lines exported, including header line

    >>> logger.setLevel(logging.INFO)
    >>> import lib_path
    >>> import minilib
    >>> file_fullpath = lib_path.path_join_posix(minilib.path_rotek_apps,'/test/ebay_test/export_test.csv')
    >>> ll_data =[['a','b','c'],[1,2,True]]
    >>> write_ll_data_to_csv_file_ebay(ll_data=ll_data,file_fullpath=file_fullpath)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    >>> read_csv_file_with_header_to_list_of_odicts(file_fullpath=file_fullpath)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    [OrderedDict([('a', '1'), ('b', '2'), ('c', 'True')])]
    >>> ll_data =[['a','b','c'],[1,2]]

    >>> # issue warning: row [1, 2] has a different length as the header line
    >>> write_ll_data_to_csv_file_ebay(ll_data=ll_data,file_fullpath=file_fullpath)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE

    >>> ll_data =[]
    >>> write_ll_data_to_csv_file_ebay(ll_data=ll_data,file_fullpath=file_fullpath)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    RuntimeError: Nothing to export

    >>> # EBAY benötigt " als Escape Character - aber escape character beim CVS LESEN ist broken in python !!!
    >>> ll_data =[['a','b','c'],[1,2,'das ist ein "TE;ST">']]
    >>> write_ll_data_to_csv_file_ebay(ll_data=ll_data,file_fullpath=file_fullpath,escapechar='"')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    >>> read_csv_file_with_header_to_list_of_odicts(file_fullpath=file_fullpath)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    [OrderedDict([('a', '1'), ('b', '2'), ('c', 'das ist ein "TE;ST">')])]

    >>> ll_data =[['a','b','c'],[None,2,'das ist ein "TE;ST">']]
    >>> write_ll_data_to_csv_file_ebay(ll_data=ll_data,file_fullpath=file_fullpath,escapechar='"')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    >>> read_csv_file_with_header_to_list_of_odicts(file_fullpath=file_fullpath)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    [OrderedDict([('a', ''), ('b', '2'), ('c', 'das ist ein "TE;ST">')])]

    """

    b_delimiter = delimiter.encode(encoding)
    b_quotechar = quotechar.encode(encoding)
    b_lineterminator = lineterminator.encode(encoding)
    b_escapechar = escapechar.encode(encoding)

    # with open(file_fullpath, 'w', encoding=encoding, newline='\n', errors='xmlcharrefreplace') as csvfile:
    with open(file_fullpath, 'wb') as csvfile:
        if not len(ll_data):
            raise RuntimeError('Nothing to export')

        number_of_fields = len(ll_data[0])

        for l_data in ll_data:
            csvfile.write(get_ebay_csv_row(l_data, delimiter=b_delimiter, quotechar=b_quotechar, escapechar=b_escapechar) + b_lineterminator)
            if len(l_data) != number_of_fields:
                logger.warning('row {} has a different length as the header line'.format(l_data))


def get_ebay_csv_row(l_data: List[str], delimiter: bytes, quotechar: bytes, escapechar: bytes) -> bytes:
    """
    >>> get_ebay_csv_row(['test','teφst','te"st','te;st'], delimiter=b';', quotechar=b'"', escapechar=b'"')
    b'test;"te&#966;st";"te""st";"te;st"'
    """
    l_str_data = []
    for str_data in l_data:
        if str_data is None:
            byte_data = b''
        else:
            byte_data = str(str_data).encode('ISO-8859-1', errors='xmlcharrefreplace')
        byte_data = escape_quote_character_in_field(field_data=byte_data, quotechar=quotechar, escapechar=escapechar)
        byte_data = quote_field_if_needed(field_data=byte_data, quotechar=quotechar, delimiter=delimiter)
        l_str_data.append(byte_data)
    str_row = delimiter.join(l_str_data)
    return str_row


def escape_quote_character_in_field(field_data: bytes, quotechar: bytes, escapechar: bytes) -> bytes:
    """
    >>> escape_quote_character_in_field('test'.encode('ISO-8859-1'), quotechar=b'"', escapechar=b'"')
    b'test'
    >>> escape_quote_character_in_field('te"st'.encode('ISO-8859-1'), quotechar=b'"', escapechar=b'"')
    b'te""st'

    """
    if quotechar in field_data:
        field_data = field_data.replace(quotechar, escapechar + quotechar)
    return field_data


def quote_field_if_needed(field_data: bytes, quotechar: bytes, delimiter: bytes) -> bytes:
    """
    quote the field if quote character or delimiter is within the field

    >>> quote_field_if_needed(b'test', quotechar=b'"', delimiter=b';')
    b'test'
    >>> quote_field_if_needed(b'te""st', quotechar=b'"', delimiter=b';')
    b'"te""st"'
    >>> quote_field_if_needed(b'te;st', quotechar=b'"', delimiter=b';')
    b'"te;st"'
    """

    if quotechar in field_data or delimiter in field_data:
        field_data = quotechar + field_data + quotechar
    return field_data


def cast_list_2_csv(ls_values: List[str], s_value_delimiter: str = ',', s_quotechar: str = '"', n_quoting: int = csv.QUOTE_MINIMAL) -> str:
    """
    konvertiere eine Liste von Strings in einen csv String

    Args:
    ls_values            : Liste von Strings
    s_value_delimiter    : der Delimiter, Default=','
    s_quotechar          : der Character für Quoting, default='"'
    n_quoting            : Quoting Type, default=csv.QUOTE_MINIMAL

    Returns:

    Exceptions           :    Exception bei Fehler
    """
    my_buffer = CWriterObject()
    my_csv_writer = csv.writer(my_buffer, delimiter=str(s_value_delimiter), quotechar=str(s_quotechar), quoting=n_quoting)       # str() für python2

    my_csv_writer.writerow(ls_values)
    return my_buffer.Buffer[:-2]                                         # hier \r\n entfernen, weil csv_writer eine ganze line mit linefeed schreibt


def cast_csv_2_list(s_csvstr: str, s_value_delimiter: str = ',', s_quotechar: str = '"', n_quoting: int = csv.QUOTE_MINIMAL) -> List[str]:
    """
    konvertiere einen csv String in eine Liste von Strings. Ist s_csvstr nicht vom typ string, so wird der Wert unverändert zurückgegeben

    Args:
        :param s_csvstr:                ein CSV String. Ist s_csvstr nicht vom typ string, so wird der Wert unverändert zurückgegeben
        :param s_value_delimiter:       der Delimiter, Default=','
        :param s_quotechar:             der Character für Quoting, default='"'
        :param n_quoting:               Quoting Type, default=csv.QUOTE_MINIMAL

    Returns:
        :return:    ls_returnlist
        :rtype:     [str]

    Exceptions           :    Exception bei Fehler

    >>> cast_csv_2_list('a,b,c')
    ['a', 'b', 'c']
    >>> cast_csv_2_list('a,"b,c",d')
    ['a', 'b,c', 'd']
    >>> cast_csv_2_list('a,"b , c",d')
    ['a', 'b , c', 'd']
    >>> # UNERWARTETES verhalten wenn blank vor dem quotechar wenn nicht skipinitialspace=True gesetzt wird
    >>> cast_csv_2_list('a, "x, y" , b')
    ['a', 'x, y ', 'b']
    >>> # UNERWARTETES verhalten wenn blank vor dem quotechar wenn nicht skipinitialspace=True gesetzt wird
    >>> cast_csv_2_list('a, "b , c" , b')
    ['a', 'b , c ', 'b']
    >>> cast_csv_2_list('a,"b,c",b')
    ['a', 'b,c', 'b']
    >>> cast_csv_2_list('a')
    ['a']
    >>> cast_csv_2_list(1)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    _csv.Error: ...

    >>> cast_csv_2_list(None)   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    _csv.Error: ...


    """

    myreader = csv.reader([s_csvstr], delimiter=str(s_value_delimiter), quotechar=str(s_quotechar), quoting=n_quoting, skipinitialspace=True)
    #
    # verwende csvreader im
    # den string zu parsen, str() wegen python2
    ls_returnlist = []
    for ls_lines in myreader:       # es wird immer nur eine Zeile geben
        ls_returnlist = ls_lines    # diese erste Zeile sind unsere neuen Commands
    return ls_returnlist
