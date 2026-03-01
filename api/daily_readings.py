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

def get_readings(day):
    response = asyncio.run(load_readings(day))
    return response.to_dict()

if __name__=="__main__":
    readings = get_readings(datetime.date.today())
    print(readings)
    reading_map = {r['header']: r['readings'][0]['text'] for r in readings['sections']}
    print(reading_map)
