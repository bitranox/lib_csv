"""
Usage:  lib_csv (-h | -v | -i)

    -h, --help          show help
    -v, --version       show version
    -i, --info          show Info

this module exposes no other useful functions to the commandline

"""
# docopt syntax see : http://docopt.org/

# STDLIB
import csv
from collections import OrderedDict
from docopt import docopt           # type: ignore
import logging
import pathlib
from typing import Dict, List, Union

# PROJ
try:
    from . import __init__conf__
except ImportError:                 # pragma: no cover
    # imports for doctest
    import __init__conf__           # type: ignore  # pragma: no cover


logger = logging.getLogger()


class CWriterObject(object):
    """
    creates a file like object to write on
    """

    def __init__(self) -> None:
        self.Buffer = ''

    def write(self, text: str) -> None:
        self.Buffer = self.Buffer + text


def read_csv_file_with_header_to_hashed_odict_of_odicts(path_csv_file: pathlib.Path,
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
    >>> csv_file_broken_less_fields_than_header = test_directory / 'csv_file_broken_less_fields_than_header.csv'
    >>> r_csv = read_csv_file_with_header_to_hashed_odict_of_odicts

    >>> # Test Fieldname for hashing not existent in the header
    >>> r_csv(path_csv_file=testfile1, hash_by_fieldname='not_existing') # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Field "not_existing" is not available, or the csv file does not have header information

    >>> # Test OK, Fieldname for hashing is unique
    >>> r_csv(path_csv_file=testfile1, hash_by_fieldname='Nr.') # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    OrderedDict([('HUB025', OrderedDict([('HTMLpublish', 'Nein'), ('Artikel Nicht Verfügbar', 'Nein'), ('Sperre Angebot', 'Nein'), ...

    >>> # Test Fieldname for hashing is not unique
    >>> r_csv(path_csv_file=testfile2, hash_by_fieldname='CustomLabel')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Index is not unique, field: "CustomLabel", value: "HUB179"

    >>> # Test Number of Fields is smaller than the header
    >>> r_csv(path_csv_file=csv_file_broken_less_fields_than_header, hash_by_fieldname='a')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Row has length 3 instead of 4 : "['1', '2', '3']"



    """
    with open(str(path_csv_file), 'r', encoding=encoding) as f_csv_file:
        is_first_row = True
        fieldnames = []
        index_of_hash_field = 0
        number_of_rows = 0
        dict_result = OrderedDict()

        my_csv_reader = csv.reader(f_csv_file, delimiter=delimiter, quotechar=quotechar, quoting=quoting)
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


def read_csv_file_with_header_to_list_of_odicts(path_csv_file: pathlib.Path,
                                                encoding: str = "ISO-8859-1",
                                                delimiter: str = ";",
                                                quotechar: str = '"',
                                                quoting: int = csv.QUOTE_MINIMAL,
                                                doublequote: bool = True,
                                                check_row_length: bool = True) -> 'List[OrderedDict[str, str]]':
    """
    reads the csv file into a list of ordered dicts

    >>> # setup
    >>> logger.setLevel(logging.INFO)
    >>> test_directory = pathlib.Path(__file__).absolute().parent.parent / 'tests'
    >>> testfile1 = test_directory / '2018-06-06_active_qty.csv'
    >>> path_csv_file_broken_less_fields_than_header = test_directory / 'csv_file_broken_less_fields_than_header.csv'
    >>> path_csv_file_broken_more_fields_than_header = test_directory / 'csv_file_broken_more_fields_than_header.csv'
    >>> # Test Ok
    >>> read_csv_file_with_header_to_list_of_odicts(path_csv_file=testfile1)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    [OrderedDict(...), OrderedDict(...), ...]
    >>> # Test Number of Fields less as in Header - check length
    >>> read_csv_file_with_header_to_list_of_odicts(path_csv_file=path_csv_file_broken_less_fields_than_header)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    ValueError: Row "[...]" has not the correct length

    >>> # Test Number of Fields less as in Header - not check length
    >>> read_csv_file_with_header_to_list_of_odicts(path_csv_file=path_csv_file_broken_less_fields_than_header, check_row_length=False)
    [OrderedDict([('a', '1'), ('b', '2'), ('c', '3')])]

    >>> # Test Number of Fields more as in Header - check length
    >>> read_csv_file_with_header_to_list_of_odicts(path_csv_file=path_csv_file_broken_more_fields_than_header)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Row "['1', '2', '3', '4', '5']" has not the correct length

    >>> # Test Number of Fields more as in Header - not check length
    >>> read_csv_file_with_header_to_list_of_odicts(path_csv_file=path_csv_file_broken_more_fields_than_header,
    ...                                             check_row_length=False )  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    ...
    ValueError: Row "['1', '2', '3', '4', '5']" has more fields than the header


    """

    with open(str(path_csv_file), 'r', encoding=encoding) as f_csv_file:
        is_first_row = True
        fieldnames = []
        number_of_rows = 0
        l_dict_result = list()

        my_csv_reader = csv.reader(f_csv_file, delimiter=delimiter, quotechar=quotechar, quoting=quoting, doublequote=doublequote)
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
                else:
                    raise ValueError('Row "{}" has more fields than the header'.format(row))

            l_dict_result.append(dict_data)

        return l_dict_result


def write_hashed_odict_of_odicts_to_csv_file(dict_data: 'OrderedDict[str, OrderedDict[str, str]]',
                                             path_csv_file: pathlib.Path,
                                             encoding: str = "ISO-8859-1",
                                             delimiter: str = ";",
                                             quotechar: str = '"',
                                             quoting: int = csv.QUOTE_MINIMAL) -> None:

    with open(str(path_csv_file), 'w', encoding=encoding, newline='\n') as csvfile:
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


def write_ll_data_to_csv_file(ll_data: List[List[str]],
                              path_csv_file: pathlib.Path,
                              encoding: str = "ISO-8859-1",
                              delimiter: str = ";",
                              quotechar: str = '"',
                              quoting: int = csv.QUOTE_MINIMAL,
                              lineterminator: str = '\n',
                              escapechar: str = '"',
                              doublequote: bool = True) -> None:
    """

    >>> # setup
    >>> logger.setLevel(logging.INFO)
    >>> test_directory = pathlib.Path(__file__).absolute().parent.parent / 'tests'
    >>> testfile = test_directory / 'export_test.csv'

    >>> # export ok
    >>> ll_data =[['a','b','c'],[1,2,True]]
    >>> write_ll_data_to_csv_file(ll_data=ll_data,path_csv_file=testfile)
    >>> read_csv_file_with_header_to_list_of_odicts(path_csv_file=testfile)
    [OrderedDict([('a', '1'), ('b', '2'), ('c', 'True')])]

    >>> # Number of Rows does not match Header
    >>> ll_data =[['a','b','c'],[1,2]]
    >>> write_ll_data_to_csv_file(ll_data=ll_data,path_csv_file=testfile)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    ValueError: row "[1, 2]" has a different length as the header line

    >>> # Nothing to export
    >>> ll_data =[]
    >>> write_ll_data_to_csv_file(ll_data=ll_data,path_csv_file=testfile)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    ValueError: Nothing to export

    >>> # EBAY needs '"' as escape character und double escape
    >>> ll_data =[['a','b','c'],[1,2,'das ist ein "TE;ST">'],[2,3,'das ist ein TE;ST']]
    >>> write_ll_data_to_csv_file(ll_data=ll_data,path_csv_file=testfile,escapechar='"')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    >>> read_csv_file_with_header_to_list_of_odicts(path_csv_file=testfile)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    [OrderedDict([('a', '1'), ('b', '2'), ('c', 'das ist ein "TE;ST">')]), OrderedDict([('a', '2'), ('b', '3'), ('c', 'das ist ein TE;ST')])]


    """
    csv.register_dialect('MyDialect', delimiter=delimiter, quotechar=quotechar, quoting=quoting,
                         doublequote=doublequote, lineterminator=lineterminator, escapechar=escapechar)

    with open(str(path_csv_file), 'w', encoding=encoding, newline='\n') as csvfile:
        my_csv_writer = csv.writer(csvfile, dialect='MyDialect', quoting=quoting)

        if not len(ll_data):
            raise ValueError('Nothing to export')

        number_of_fields = len(ll_data[0])

        for l_data in ll_data:
            my_csv_writer.writerow(l_data)
            if len(l_data) != number_of_fields:
                raise ValueError('row "{}" has a different length as the header line'.format(l_data))


def write_ll_data_to_csv_file_ebay(ll_data: List[List[str]],
                                   path_csv_file: pathlib.Path,
                                   encoding: str = "ISO-8859-1",
                                   delimiter: str = ";",
                                   quotechar: str = '"',
                                   lineterminator: str = '\n',
                                   escapechar: str = '"') -> None:
    """
    :return:    number of lines exported, including header line

    >>> # setup
    >>> logger.setLevel(logging.INFO)
    >>> test_directory = pathlib.Path(__file__).absolute().parent.parent / 'tests'
    >>> test_file = test_directory / 'export_test.csv'
    >>> if test_file.is_file(): test_file.unlink()

    >>> # Test OK
    >>> ll_data =[['a','b','c'],[1,2,True]]
    >>> write_ll_data_to_csv_file_ebay(ll_data=ll_data,path_csv_file=test_file)
    >>> read_csv_file_with_header_to_list_of_odicts(path_csv_file=test_file)
    [OrderedDict([('a', '1'), ('b', '2'), ('c', 'True')])]


    >>> # Test issue warning: row [1, 2] has a different length as the header line
    >>> ll_data =[['a','b','c'],[1,2]]
    >>> write_ll_data_to_csv_file_ebay(ll_data=ll_data,path_csv_file=test_file)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE

    >>> ll_data =[]
    >>> write_ll_data_to_csv_file_ebay(ll_data=ll_data,path_csv_file=test_file)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    RuntimeError: Nothing to export

    >>> # EBAY benötigt " als Escape Character - aber escape character beim CVS LESEN ist broken in python !!!
    >>> ll_data =[['a','b','c'],[1,2,'das ist ein "TE;ST">']]
    >>> write_ll_data_to_csv_file_ebay(ll_data=ll_data,path_csv_file=test_file,escapechar='"')
    >>> read_csv_file_with_header_to_list_of_odicts(path_csv_file=test_file)
    [OrderedDict([('a', '1'), ('b', '2'), ('c', 'das ist ein "TE;ST">')])]

    >>> ll_data =[['a','b','c'],[None,2,'das ist ein "TE;ST">']]
    >>> write_ll_data_to_csv_file_ebay(ll_data=ll_data,path_csv_file=test_file,escapechar='"')
    >>> read_csv_file_with_header_to_list_of_odicts(path_csv_file=test_file)
    [OrderedDict([('a', ''), ('b', '2'), ('c', 'das ist ein "TE;ST">')])]

    >>> # Teardown
    >>> if test_file.is_file(): test_file.unlink()


    """

    b_delimiter = delimiter.encode(encoding)
    b_quotechar = quotechar.encode(encoding)
    b_lineterminator = lineterminator.encode(encoding)
    b_escapechar = escapechar.encode(encoding)

    # with open(file_fullpath, 'w', encoding=encoding, newline='\n', errors='xmlcharrefreplace') as csvfile:
    with open(str(path_csv_file), 'wb') as csvfile:
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


def cast_list_2_csv(ls_values: List[str],
                    delimiter: str = ';',
                    quotechar: str = '"',
                    escapechar: str = '"',
                    quoting: int = csv.QUOTE_MINIMAL,
                    doublequote: bool = True) -> str:
    """
    konvertiere eine Liste von Strings in einen csv String

    >>> l_test = ['a', 'b', 'c;d', 'e"f']
    >>> cast_list_2_csv(l_test)
    'a;b;"c;d";"e""f"'
    >>> cast_list_2_csv(l_test, doublequote=False)
    'a;b;"c;d";e""f'


    """
    my_buffer = CWriterObject()

    my_csv_writer = csv.writer(my_buffer, delimiter=str(delimiter), quotechar=str(quotechar), quoting=quoting,
                               doublequote=doublequote, escapechar=escapechar)
    my_csv_writer.writerow(ls_values)
    return my_buffer.Buffer[:-2]                                         # hier \r\n entfernen, weil csv_writer eine ganze line mit linefeed schreibt


def cast_csv_2_list(csv_str: str, delimiter: str = ',', quote_char: str = '"',
                    csv_quoting: int = csv.QUOTE_MINIMAL, skipinitialspace: bool = True) -> List[str]:
    """
    konvertiere einen csv String in eine Liste von Strings. Ist csv_str nicht vom typ string, so wird der Wert unverändert zurückgegeben

    >>> import unittest
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
    >>> # UNERWARTETES verhalten wenn blank vor dem quotechar wenn nicht skipinitialspace=True gesetzt wird
    >>> cast_csv_2_list('a, "b , c" , b', skipinitialspace=False)
    ['a', ' "b ', ' c" ', ' b']

    >>> cast_csv_2_list('a,"b,c",b')
    ['a', 'b,c', 'b']
    >>> cast_csv_2_list('a')
    ['a']

    >>> # raise Error if csv_string is None
    >>> unittest.TestCase().assertRaises(Exception, cast_csv_2_list, csv_str=None)

    >>> # raise Error if csv_string is wrong type
    >>> unittest.TestCase().assertRaises(Exception, cast_csv_2_list, csv_str=1)


    """

    myreader = csv.reader([csv_str], delimiter=str(delimiter), quotechar=str(quote_char), quoting=csv_quoting, skipinitialspace=skipinitialspace)
    #
    # verwende csvreader im
    # den string zu parsen, str() wegen python2
    ls_returnlist = []
    for ls_lines in myreader:       # es wird immer nur eine Zeile geben
        ls_returnlist = ls_lines    # diese erste Zeile sind unsere neuen Commands
    return ls_returnlist


# we might import this module and call main from another program and pass docopt args manually
def main(docopt_args: Dict[str, Union[bool, str]]) -> None:
    """
    >>> docopt_args = dict()
    >>> docopt_args['--version'] = True
    >>> docopt_args['--info'] = False
    >>> main(docopt_args)   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    version: ...


    >>> docopt_args['--version'] = False
    >>> docopt_args['--info'] = True
    >>> main(docopt_args)   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    information for ...

    >>> docopt_args['--version'] = False
    >>> docopt_args['--info'] = False
    >>> main(docopt_args)


    """
    if docopt_args['--version']:
        __init__conf__.print_version()
    elif docopt_args['--info']:
        __init__conf__.print_info()


# entry point via commandline
def main_commandline() -> None:
    """
    >>> main_commandline()  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    docopt.DocoptExit: ...

    """
    docopt_args = docopt(__doc__)
    main(docopt_args)       # pragma: no cover


# entry point if main
if __name__ == '__main__':
    main_commandline()
