import asyncio
import datetime

from catholic_mass_readings.models import MassType
from catholic_mass_readings import USCCB
from curl_cffi.requests.exceptions import HTTPError

# Return full text of mass readings for given day. Works back to about 2013 and forward to next year
async def load_readings(day):
    async with USCCB() as usccb:
        try:
            mass_types = await usccb.get_mass_types(day)
            mass_type = MassType.DAY if MassType.DAY in mass_types else MassType.DEFAULT
            mass_data = await usccb.get_mass(day, mass_type)
            return mass_data
        except HTTPError as e:
            if e.response.status_code == 404:
                return f"No readings found for {day}"

def transform_header(header):
    return 'First reading' if header == 'Reading 1' else 'Second reading' if header == 'Reading 2' else header

def get_readings(day):
    response = asyncio.run(load_readings(day)).to_dict()
    reading_dict = {transform_header(r['header']): r['readings'][0]['text'] for r in response['sections']}
    return {'url': response['url'], 'readings': reading_dict}

if __name__=="__main__":
    #readings = get_readings(datetime.date(2026, 3, 19))
    readings = get_readings(datetime.date.today())
    print(readings)
