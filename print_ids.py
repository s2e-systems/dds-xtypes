#!/usr/bin/python
#################################################################
# Use and redistribution is source and binary forms is permitted
# subject to the OMG-DDS INTEROPERABILITY TESTING LICENSE found
# at the following URL:
#
# https://github.com/omg-dds/dds-xtypes/blob/master/LICENSE.md
#
#################################################################

import argparse
from collections import defaultdict
import importlib
import inspect
import re
import subprocess


########
#
class Arguments:
    def parser():
        parser = argparse.ArgumentParser(
            description='Examine test_suite.py and print the XTypes TypeIdentifier associated with all referenced types.',
            add_help=True)

        gen_opts = parser.add_argument_group(title='general options')
        gen_opts.add_argument('-e','--exe',
            default=None,
            required=True,
            type=str,
            metavar='executable_name',
            help='Path to the test application. '
                'It may be absolute or relative path. Example: if the executable '
                'is in the same folder as the script: '
                '"-e ./toc_coredx_dds-6.12.0-test_main_linux".')

        optional = parser.add_argument_group(title='optional parameters')
        optional.add_argument('-v','--verbose',
            default=False,
            required=False,
            action='store_true',
            help='Print debug information to stdout. (Default: False).')
        optional.add_argument('-o','--type-object-version',
            default="2",
            required=None,
            type=str,
            choices=["1","2"],
            help='Type Object version used if not provided when running the '
                'test application. If this application already sets the '
                'type object version, this parameter is not used.'
                'If this parameter is not set, it does not add anything to the '
                'application. The potential values are 1 for TypeObject V1 and '
                '2 for TypeObject V2.')
        optional.add_argument('-s', '--test-suite',
            default='test_suite',
            required=False,
            type=str,
            metavar='test_suite_dictionary_file',
            help='Test Suite that is going to be tested. '
                'Test Suite is a file with a Python dictionary defined. It must '
                'be located on the same directory as interoperability_report. '
                'This value should not contain the extension ".py", '
                'only the name of the file. '
                'It will run all the dictionaries defined in the file. '
                '(Default: test_suite).')

        return parser


########
#
def main():

    parser = Arguments.parser()
    args = parser.parse_args()
    
    if args.verbose:
        print(f'exec: {args.exe}' )
        print(f'test suite: {args.test_suite}')
        
    re_TypeFile_arg = re.compile(r"^.*--type-file (\S*).*$")
    re_TypeName_arg = re.compile(r"^.*-y (\S*).*$")
    re_DataFile_arg = re.compile(r"^.*--data-file (\S*).*$")

    test_types = defaultdict(list)
    
    t_suite_module = importlib.import_module(args.test_suite)
        
    # check that the test_cases selected or disabled are in the test_suite and
    # exit the application if they are not.
    for test_suite_name, t_suite_dict in inspect.getmembers(t_suite_module):
        if type(t_suite_dict) is dict and test_suite_name != '__builtins__':
            if args.verbose:
                print(f'Test Suite {test_suite_name}' )
            for test_case_name, test_case_parameters in t_suite_dict.items():
                
                pub_type_file=None
                pub_data_file=None
                pub_type=None
                
                sub_type_file=None
                sub_data_file=None
                sub_type=None
                
                apps = test_case_parameters['apps']
                pub = apps[0]
                sub = apps[1]

                # A: Look for --type-folder and --type-file
                #   1) check common args
                if 'common_args' in test_case_parameters:
                    common_args = test_case_parameters['common_args']
                    for a in common_args:
                        m = re_TypeFile_arg.match(a)
                        if m:
                            pub_type_file = m.group(1)
                            sub_type_file = m.group(1)
                
                #   2) check in pub command:
                if not pub_type_file:
                    m = re_TypeFile_arg.match(pub)
                    if m:
                        pub_type_file = m.group(1)
                
                #   3) check in sub command:
                if not sub_type_file:
                    m = re_TypeFile_arg.match(sub)
                    if m:
                        sub_type_file = m.group(1)

                # B: look for pub type name
                m = re_TypeName_arg.match(pub)
                if m:
                    pub_type = m.group(1)

                # C: look for sub type name
                m = re_TypeName_arg.match(sub)
                if m:
                    sub_type = m.group(1)

                # D: look for pub and sub data file
                m = re_DataFile_arg.match(pub)
                if m:
                    pub_data_file = m.group(1)
                m = re_DataFile_arg.match(sub)
                if m:
                    sub_data_file = m.group(1)
                    
                # summarize:
                if args.verbose:
                    print(f'   test case: {test_case_name}')
                    print(f'      pub xml type file: {pub_type_file}')
                    print(f'      pub type: {pub_type}')
                    print(f'      pub data: {pub_data_file}')
                    print(f'      sub xml type file: {sub_type_file}')
                    print(f'      sub type: {sub_type}')
                    print(f'      sub data: {sub_data_file}')

                # collect all the type_file + type + data_file tuples, so we can remove duplicates (based on type) and run once for each instance
                type_params = test_types[pub_type_file]
                if not any( pub_type in param for param in type_params ):
                    #if not pub_type in test_types[pub_type_file]:
                    test_types[pub_type_file].append([pub_type, pub_data_file])
                type_params = test_types[sub_type_file]
                if not any( sub_type in param for param in type_params ):
                    # if not sub_type in test_types[sub_type_file]:
                    test_types[sub_type_file].append([sub_type, sub_data_file])

    # test_types contains a list of all XType File[s] used by the test_suite.py
    #    and, for each Type File, a list of each specific Data Type used from that file
    # SO:
    #   for each Type File:
    #     print out each Type Name and its corresponding TypeIdentifier
    re_typeid       = re.compile(r"^.*Type ID: (\S*).*$", re.M )  # v1 typeid (uint64)
    
    re_completeHash = re.compile(r"^Complete.*:\s(\S*).*$", re.M) # v2 complete equivalence hash
    re_minimalHash  = re.compile(r"^Minimal.*:\s(\S*).*$", re.M)  # v2 minimal equivalence hash

    exetimeout = 0.1 # the typeid output is done fairly quickly, so no need to wait very long...
    
    for type_file, params in test_types.items():
        print(f'{type_file} : ')
        
        for typ, datafile in params:
            # --data-file bad_file_so_we_exit_fast
            command = f'{args.exe} -P --type-folder types --type-file {type_file} --data-folder data -y {typ} --type-object-version {args.type_object_version} --print-typeid'
            
            if args.verbose:
                print(f'{command} --data-file {datafile}') # we append the data file, so it is easy to run the full command later for analysis...
                
            try:
                process = subprocess.run( command, capture_output=True, text=True, shell=True, timeout=exetimeout )
                output_txt = process.stdout
            except subprocess.TimeoutExpired as e:
                output_txt = e.stdout.decode()
                
            #print(f'output:\n {output_txt}' )
            
            if args.type_object_version == "1":
                reout = re_typeid.search(output_txt)
                if reout:
                    typeid=reout.group(1)
                else:
                    typeid='<unkn>'
                print(f'   {typ:>45} : {typeid}')
                
            else:
                
                complete = re_completeHash.search(output_txt)
                if complete:
                    ctid = complete.group(1)
                else:
                    ctid = '<not found>'
                print(f'   {typ:>45} : [ complete ] {ctid}')
                    
                minimal  = re_minimalHash.search(output_txt) 
                if minimal:
                    mtid = minimal.group(1)
                else:
                    mtid = '<not found>'
                print(f'   {typ:>45} : [ minimal  ] {mtid}' )
                
                
########
# run main        
if __name__ == '__main__':
    main()
    
