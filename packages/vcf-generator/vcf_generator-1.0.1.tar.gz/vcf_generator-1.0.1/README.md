[![build status](https://github.com/talk2bryan/vcf-generator/actions/workflows/ci.yaml/badge.svg)](https://github.com/talk2bryan/vcf-generator/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/talk2bryan/vcf-generator/graph/badge.svg?token=IHS7IJ3RPN)](https://codecov.io/gh/talk2bryan/vcf-generator)
[![PyPI version](https://badge.fury.io/py/vcf-generator.svg)](https://badge.fury.io/py/vcf-generator)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vcf-generator)](https://pypi.org/project/vcf-generator/)
[![PyPI - License](https://img.shields.io/pypi/l/vcf-generator)](https://pypi.org/project/vcf-generator/)
[![PyPI - Format](https://img.shields.io/pypi/format/vcf-generator)](https://pypi.org/project/vcf-generator/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/vcf-generator)](https://pypi.org/project/vcf-generator/)

# vcf-generator

A simple VCF generator. Generate VCF files with random data.

## Installation
Using pip:
```bash
pip install vcf-generator
```
## Quick Start
```bash
$ vcf-generator vcards --output-file test.vcf --num_contacts 1000
$ vcf-generator contacts_str --output-file test.txt --num_contacts 1000
```

## Command Line Interface
```bash
$ vcf-generator --help
Usage: vcf-generator [OPTIONS] COMMAND [ARGS]...
Options:
  --help  Show this message and exit.
Commands:
    contacts_str  Generate contacts as string
    vcards        Generate contacts in VCF format (4.0)
```

See help for each command:

```bash
$ vcf-generator COMMAND --help
Usage: vcf-generator COMMAND [OPTIONS]
  Generate contacts in VCF format (4.0)
Options:
    -o, --output-file TEXT  Output file  [optional]
    -n, --num_contacts INTEGER  Number of contacts to generate  [optional]
    --help              Show this message and exit.
```


## Examples
### Generate VCF data with 1 contact
```bash
$ vcf-generator vcards
```

The above command will generate a VCF file with 1 contact and print the content to the console:

```bash
BEGIN:VCARD
VERSION:4.0
N:None;Caroline;None;;None
FN:Caroline
ORG:None Co.
TITLE:None
TEL;TYPE#HOME,voice;VALUE#uri:tel:+72-665-5131092
TEL;TYPE#HOME,voice;VALUE#uri:tel:+63-689-8521227
TEL;TYPE#WORK,voice;VALUE#uri:tel:+594-235-6973654
ADR;TYPE#OTHER;PREF#1;LABEL#922 Williams Grove Apt. 408
Debbieside, NE 58214
Trinidad and Tobago:;;922 Williams Grove Apt. 408;Debbieside;NE;58214;Trinidad and Tobago
ADR;TYPE#WORK;PREF#2;LABEL#987 Middleton Shoals
Lake Amyview, OK 67042
Hungary:;;987 Middleton Shoals;Lake Amyview;OK;67042;Hungary
BDAY:1965-02-22
EMAIL:rebeccabrady@example.com
EMAIL:michaeljordan@example.com
EMAIL:campbellrodney@example.com
END:VCARD
```

### Generate 1 contact as string
```bash
$ vcf-generator contacts_str
```

The above command will generate a contact as string and print the content to the console:

```bash
Name: Latoya (Jenna) - Mrs.
DOB: 1953-04-23
Phone Numbers: MOBILE: +111 (747) 3381349, OTHER: +220 (470) 7413364
Emails: PERSONAL: jameswillis@example.org, OTHER: haasbrenda@example.com
Addresses: OTHER: 86137 Julie Neck Apt. 623, 745 East Eugenefort, MD 06582 Marshall Islands, WORK: 751 Michael Crossroad, 7971 New Andreaton, NM 31536 Israel
```
