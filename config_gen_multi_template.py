#! /usr/bin/env python
# Chris Cole 06.23.2020

#
#
# This python script creates device configurations by matching the values in a CSV file to a jinja2 template
# Whats different is the jinja2 template are called out in the CSV file, this was created for multi cisco switch types
#
# How it works
# The python script will read the CSV file
# The first row in the CSV file will be the "key" in key:value dictionary
# Then loop/iterate in the rows and put them as values into the dictionary
# The "key" name in the first row of the CSV should match the jinja2 templete "{{ variable }}"
# Make sure that the first parameter is "hostname" in the CSV file the script will name the output file with the hostname
# Use the parameter/key name "template" in the CSV file for the name of the Jinja2 template to be used
# Templates should be in a sub-directory "./templates/"
#
# To run script with use of switches:
#    -C CSV parameter file
#    -O Create Directory for files
#
# $ python3 config_gen_csv.py -C csv-file-with-values.csv -O output-dir
#
# to make excutable
# $ chmod +x config_gen_csv.py
# $ ./config_gen_csv.py -J jinja2-template.j2 -C csv-file-with-values.csv -O output-dir
#
# To run script with prompts:
#
#    $ python3 config_gen_csv.py
#	CSV File: csv-file-with-values.csv
#	Output Dir: output-dir
#
#

from __future__ import absolute_import, division, print_function
# This module gives us compatibility when running this on Python 3 as well as Python 2

import jinja2 # Jinja2 is a modern and designer-friendly templating language for Python
import sys  # This library we are using to pass different arguments to the script
import os   # This library we are using to get the image files from the OS filesystem
import argparse #This library is a command line option and argument parsing
import re

# File check, does the paramter/values file exists
def file_check(csv_parameter_file):
    csv_parameter_file_check = bool(os.path.exists(csv_parameter_file))
    if csv_parameter_file_check == False:
        raise SystemExit('>>>>> File %s Not Found' % csv_parameter_file)
    print('>>>>> File %s found' % csv_parameter_file)

def file_extension(csv_parameter_file):
	csv_parameter_file_extension = bool(re.search(r'(?:.csv)',csv_parameter_file))
	if csv_parameter_file_extension == False:
		raise SystemExit('>>>>> File %s needs to have .csv extension' % csv_parameter_file)
	print('>>>>> File extension verifed')

def template_dir(template_directory):
    template_directory_check = bool(os.path.exists(template_directory))
    if template_directory_check == False:
        raise SystemExit('>>>>> No Template Directory %s ' % template_directory)
    print(">>>>> Template directory verifed...")

def output_dir(output_directory):
    output_directory_check = bool(os.path.exists(output_directory))
    if output_directory_check == False:
        os.mkdir(output_directory)
        print(">>>>> Created Output Directory %s..." % output_directory)
    print(">>>>> Output Directory %s Verifed..." % output_directory)

def read_file(csv_parameter_file):
    print(">>>>> Read %s parameter file..." % csv_parameter_file )
    f = open(csv_parameter_file)
    csv_content = f.read()
    f.close()
    return csv_content

def csv_to_dict(csv_content,config_parameters,output_directory):
    print(">>>>> Convert CSV file to dictionaries..." )
    csv_lines = csv_content.splitlines()
    headers = csv_lines[0].split(",")
    for i in range(1, len(csv_lines)):
        values = csv_lines[i].split(",")
        parameter_dict = dict()
        for h in range(0, len(headers)):
            parameter_dict[headers[h]] = values[h]
            #print(parameter_dict)
        config_parameters.append(parameter_dict)
        #print(config_parameters)
    for parameter in config_parameters:
        # 3. next we need to create the central Jinja2 environment and we will load
        # the Jinja2 template file
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="./templates/"))
        template = env.get_template(parameter['template'])
        print(">>>>> Read Jinja2 environment..." + parameter['template'])

        # 4. now create the templates
        print(">>>>> Create templates...")
        result = template.render(parameter)
        f = open(os.path.join(output_directory, parameter['hostname'] + "-AAA-CFG.txt"), "w")
        f.write(result)
        f.close()
        print(">>>>> Configuration '%s' created..." % (parameter['hostname'] + "-AAA-CFG.txt"))
    print("DONE")

def main():
    parser = argparse.ArgumentParser(description="description here")
    parser.add_argument('-C', '-csv', dest='csv_parameter_file_arg', type=str,
                    help='Input CSV Values file. Default filename is values.csv', default='values.csv')
    parser.add_argument('-O', '-out', dest='output_arg', type=str,
                    help='Output directory for configuration, Default output directory is output', default='output')
    results = parser.parse_args()
    if not results.csv_parameter_file_arg:
        results.csv_parameter_file_arg= input("CSV File: ")
    if not results.output_arg:
        results.output_arg= input("Output Dir: ")
    csv_parameter_file = results.csv_parameter_file_arg
    # Todo add a argument for ./templates directory
    template_directory = ('./templates')
    config_parameters = []
    output_directory = results.output_arg
    file_check(csv_parameter_file)
    file_extension(csv_parameter_file)
    template_dir(template_directory)
    output_dir(output_directory)
    csv_content = read_file(csv_parameter_file)
    csv_to_dict(csv_content,config_parameters,output_directory)


if __name__ == '__main__':
  main()
