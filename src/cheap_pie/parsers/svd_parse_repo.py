#!/usr/bin/env python3
""" Cheap Pie parser module for .svd files using SVDParser module """
# this file is part of cheap_pie, a python tool for chip validation
# author: Marco Merlin
# email: marcomerli@gmail.com

# parser build for CMSIS-SVD xml file format
# https://www.keil.com/pack/doc/CMSIS/SVD/html/index.html
#
# simplified manual initialization
#
# import untangle
# hal = untangle.parse('QN908XC.xml')
# from cbitfield import cp_bitfield
# from cp_register import cp_register
# ADC_ANA_CTRL = cp_register("ADC_ANA_CTRL","0x4000702C",
#                            "ADC core and reference setting regsiter" , hif )
# ADC_BM = cp_bitfield("ADC_BM","0x4000702C",
#                      "ADC_ANA_CTRL",3,0, "ADC bias current selection." ,hif)

import os
from ast import literal_eval
from cmsis_svd.parser import SVDParser

from cheap_pie.cheap_pie_core.cp_builder import CpHalBuilder  # pylint: disable=C0413,E0401
from cheap_pie.cheap_pie_core.cp_cli import cp_devices_fname  # pylint: disable=C0413,E0401

import os
import requests
import zipfile
from urllib.parse import urlparse

def download_github_repo(repo_url, output_dir="."):
    """
    Download a GitHub repository as a ZIP file and extract it
    
    Args:
        repo_url (str): GitHub repo URL (e.g., "https://github.com/user/repo")
        output_dir (str): Directory to save the repository
    """
    try:
        # Parse the repository URL
        parsed = urlparse(repo_url)
        if not parsed.netloc == "github.com":
            raise ValueError("URL must be from github.com")
        
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) < 2:
            raise ValueError("Invalid GitHub repository URL")
        
        owner, repo = path_parts[:2]
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Download the ZIP file
        zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/main.zip"
        print(f"Downloading {zip_url}...")
        
        response = requests.get(zip_url, stream=True)
        response.raise_for_status()
        
        zip_path = os.path.join(output_dir, f"{repo}.zip")
        
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Extract the ZIP file
        print(f"Extracting to {output_dir}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        
        # Remove the ZIP file
        os.remove(zip_path)
        
        print(f"Successfully downloaded {owner}/{repo} to {output_dir}")
        return os.path.join(output_dir, f"{repo}-main")
        
    except Exception as e:
        print(f"Error downloading repository: {e}")
        return None

def get_cmsis_svd_data_dir():
    outdir = "."
    datalib = os.path.join(outdir,'cmsis-svd-data-main','data')
    if not os.path.isdir(datalib):
        download_github_repo(repo_url='https://github.com/cmsis-svd/cmsis-svd-data', output_dir=outdir)
    assert os.path.isdir(datalib)
    return datalib

def svd_parse_repo(fname, vendor=None, hif=None, base_address_offset="0x00000000",
                   svd_root=get_cmsis_svd_data_dir()
                   ):
    """ Cheap Pie parser function for .svd files using SVDParser module """
    ## read input file ########################################################
    if vendor is None:
        svd = SVDParser.for_xml_file(fname)
    else:
        svd = SVDParser.for_packaged_svd(package_root=svd_root, vendor=vendor, filename=fname)

    ## loop over lines ########################################################
    cpb = CpHalBuilder(hif)

    for periph in svd.get_device().peripherals:  # pylint: disable=R1702
        # print(periph.name.cdata)

        if hasattr(periph, 'registers'):
            for reg in periph.registers:
                if hasattr(reg, 'name'):
                    # new register
                    regaddr = (
                        reg.address_offset +
                        periph.base_address +
                        literal_eval(base_address_offset)
                    )

                    if hasattr(reg, 'reset_value'):
                        reset=reg.reset_value
                    else:
                        reset=0

                    cpb.reg_open(
                        regname=f'{periph.name}_{reg.name}',
                        regaddr=regaddr,
                        comments=reg.description,
                        reset=reset
                    )

                    if hasattr(reg, 'fields'):
                        for field in reg.fields:
                            if not field is None:
                                # reset value, if available
                                if hasattr(field, 'reset_value'):
                                    reset=field.reset_value
                                else:
                                    reset=0

                                # Create new field class
                                cpb.newfield(
                                    regfield=field.name,
                                    width=field.bit_width,
                                    offset=field.bit_offset,
                                    comments=field.description,
                                    reset=reset
                                )

    # convert output dictionary into structure
    return cpb.out()

def svd_repo_list_vendors() -> list:
    """ List the available vendors for function svd_parse_repo """
    data_path = get_cmsis_svd_data_dir()
    assert os.path.isdir(data_path), f'ERROR: directory {data_path} does not exist!'
    return [ f.path.split('/')[-1] for f in os.scandir(data_path) if f.is_dir() ]

def svd_repo_print_vendors() -> list:
    """ Print the available vendors for function svd_parse_repo """
    vendors = svd_repo_list_vendors()
    print('Available vendors:')
    for v in vendors:
        print(v)
    return vendors

def svd_repo_list_vendor_devices(vendor='Freescale') -> list:
    """ List the available devices for function svd_parse_repo """
    data_path = os.path.join(get_cmsis_svd_data_dir(),vendor)
    assert os.path.isdir(data_path), f'ERROR: directory {data_path} does not exist!'
    return [ f.path.split('/')[-1] for f in os.scandir(data_path) if f.is_file() ]

def svd_repo_print_vendor_devices(vendor='Freescale') -> list:
    """ Print the available devices for function svd_parse_repo """
    devices = svd_repo_list_vendor_devices(vendor=vendor)
    print(f'Available devices for vendor {vendor}:')
    for d in devices:
        print(d)
    return devices

def test_svd_parse_repo():
    """ Test Function for .svd parser based of SVDParser module """
    print('Testing QN9080 with repo parser...')

    fname = cp_devices_fname("QN908XC.svd")
    hal = svd_parse_repo(fname=fname)
    assert len(hal) > 0

    print('Testing K20 with repo parser...')
    hal = svd_parse_repo(fname='MK20D7.svd', vendor='Freescale')
    assert len(hal) > 0

    print('Testing svd_repo_list_vendors...')
    vendors = svd_repo_list_vendors()
    print(vendors)
    assert len(vendors) > 0

    print('Testing svd_repo_print_vendors...')
    vendors = svd_repo_print_vendors()
    print(vendors)
    assert len(vendors) > 0

    print('Testing svd_repo_list_vendor_devices...')
    devices = svd_repo_list_vendor_devices()
    print(devices)
    assert len(devices) > 0

    print('Testing svd_repo_print_vendor_devices...')
    devices = svd_repo_print_vendor_devices()
    print(devices)
    assert len(devices) > 0

if __name__ == '__main__':
    test_svd_parse_repo()
