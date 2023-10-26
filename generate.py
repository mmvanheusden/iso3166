#!/usr/bin/env python3

import requests
from json import loads

DATA_URL = "https://www.datahub.io/core/country-codes/r/country-codes.json"

NUMERIC_IDX = 'ISO3166-1-numeric'
ALPHA3_IDX = 'ISO3166-1-Alpha-3'
ALPHA2_IDX = 'ISO3166-1-Alpha-2'
REGION_CODE_IDX = 'Region Code'
REGION_NAME_IDX = 'Region Name'
NAME_IDX = 'CLDR display name'

def is_invalid(country):
    # Antartica is not real country
    return country[ALPHA3_IDX] is None or country[ALPHA3_IDX] == "ATA"

def main():
    resp = requests.get(DATA_URL)
    countries = resp.json()

    with open('src/data.rs', 'w', encoding='utf-8') as out:
        out.write("use crate::{Region, Data};\n\n")
        for country in countries:
            if is_invalid(country):
                continue

            out.write('pub const {}_ID: u16 = {};\n'.format(country[ALPHA3_IDX], country[NUMERIC_IDX].lstrip('0')))
            out.write('pub const {}_ALPHA2: &str = "{}";\n'.format(country[ALPHA3_IDX], country[ALPHA2_IDX]))
            out.write('pub const {0}_ALPHA3: &str = "{0}";\n'.format(country[ALPHA3_IDX]))
            out.write("pub const {}: Data = Data {{\n".format(country[ALPHA3_IDX]))
            out.write('    id: {}_ID,\n'.format(country[ALPHA3_IDX]))
            out.write('    alpha2: {}_ALPHA2,\n'.format(country[ALPHA3_IDX]))
            out.write('    alpha3: {}_ALPHA3,\n'.format(country[ALPHA3_IDX]))
            out.write('    name: "{}",\n'.format(country[NAME_IDX]))
            if country[ALPHA3_IDX] ==  "TWN":
                out.write('    region: Region::Asia,\n')
            elif country[REGION_NAME_IDX] == "Americas":
                if country['Intermediate Region Name'] == "South America":
                    out.write('    region: Region::SouthAmerica,\n')
                else:
                    out.write('    region: Region::NorthAmerica,\n')
            else:
                out.write('    region: Region::{},\n'.format(country[REGION_NAME_IDX]))
            out.write("};\n")

    with open('src/countries.rs', 'w', encoding='utf-8') as out:
        num = 0
        out.write("//!List of countries\n\n")
        out.write("use crate::{Country, data};\n\n")
        for country in countries:
            if is_invalid(country):
                continue

            out.write("///{}\n".format(country[NAME_IDX]))
            out.write("pub const {0}: Country = Country(&data::{0});\n".format(country[ALPHA3_IDX]))
            num += 1

        out.write("///List of countries\n")
        out.write("pub const LIST: [&'static Country; {}] = [\n".format(num))
        for country in countries:
            if is_invalid(country):
                continue
            out.write("    &{},\n".format(country[ALPHA3_IDX]))
        out.write("];\n")

if __name__ == "__main__":
    main()
