from app.config import get_settings
from fastapi import APIRouter, status, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from app.common_parameters import CommonQueryParams, CommonsDep
import sqlite3
import geopandas as gpd
from shapely.geometry import Point
from app.model import PSGCObject

# Router for CityMunicipality search operations.
router = APIRouter(
    prefix="",
    tags=["PSGC"],
)

def extract_psgc_codes(psgc_code: str):
    # Ensure the PSGC code is exactly 10 characters long
    if len(psgc_code) != 10:
        raise ValueError("PSGC code must be exactly 10 characters long. Got " + psgc_code)
    
    region_code = psgc_code[:2].ljust(10, "0")  # First two characters for the Region Code
    if region_code == "0000000000":
        region_code = None

    province_code = psgc_code[:5].ljust(10, "0")  # Next three characters for the Province Code or HUC

    if province_code == "0000000000":
        province_code = None

    municipal_code = psgc_code[:7].ljust(10, "0")  # Next two characters for the Municipal/City Code

    if municipal_code == "0000000000":
        municipal_code = None

    barangay_code = psgc_code.ljust(10, "0")  # Final three characters for the Barangay Code

    if barangay_code == "0000000000":
        barangay_code = None
    
    return barangay_code, province_code, municipal_code, region_code


@router.get("/cities-municipalities/search", 
    status_code=status.HTTP_200_OK,
    response_model = List[PSGCObject]
)
async def search(
    commons: CommonQueryParams = CommonsDep,
    resolveProvinceCode: Optional[bool] = Query(False, description="Resolve province code to province name"),
):
    query_param = commons.q
    skip = commons.skip
    limit = commons.limit

    # Connect to the citymunicipality.db
    conn = sqlite3.connect(f"db/psgc_{version}.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # SQL query to search for city/municipality using the query_param, and geographic_level is either 'City' or 'Mun'
    query = """
        SELECT * FROM PSGC
        WHERE (name LIKE ? OR code LIKE ? OR old_names LIKE ?)
        AND geographic_level IN ('City', 'Mun')
        LIMIT ? OFFSET ?
    """

    # Fetch the paginated matching rows
    cursor.execute(query, (f'%{query_param}%', f'%{query_param}%', f'%{query_param}%', limit, skip))
    rows = cursor.fetchall()

    if not rows:
        conn.close()
        return JSONResponse(content=[])
        
    tmp = [dict(row) for row in rows]
    result: List[PSGCObject] = []
    for row in tmp:
        psgc_code = row.get('code') 
        
        # Extract codes from PSGC
        barangay_code, province_code, municipal_code, region_code = extract_psgc_codes(psgc_code)
        
        # Add the extracted codes to the row data for instantiating PSGCObject
        city_municipality = PSGCObject(
            **row,
            barangay_code=barangay_code,
            province_code=province_code,
            municipal_code=municipal_code,
            region_code=region_code
        )
        
        result.append(city_municipality)

    # Optionally resolve province names
    if resolveProvinceCode:
        # conn = sqlite3.connect('province.db')
        # conn.row_factory = sqlite3.Row
        # cursor = conn.cursor()

        for item in result:
            if province_code:
                cursor.execute("SELECT name FROM PSGC WHERE code = ?", (item.province_code,))
                province_row = cursor.fetchone()
                if province_row:
                    item.province_name = province_row['name']
                else:
                    item.province_name = None  # If no matching province is found

        conn.close()

    conn.close()
    return result



version = get_settings().psgc_version
shapefile_path = f"./shapefiles/PSGC_adm4_{version}.shp"

def get_psgc_from_lat_long(lat: float, long: float):
    """
    Given a latitude and longitude, return the PSGC code from the shapefile at ADM4 level.
    """
    # Read the shapefile using GeoPandas
    adm4_shapes = gpd.read_file(shapefile_path)
    # print(adm4_shapes)

    # Create a Point object for the given latitude and longitude
    point = Point(long, lat)

    # Find the polygon that contains the point
    matching_shape = adm4_shapes[adm4_shapes.contains(point)]

    if not matching_shape.empty:
        # Assuming the PSGC code is stored in a column named 'PSGC'
        result = matching_shape.iloc[0]['psgc_code']
        print(result)
        return result
    else:
        # If no matching shape is found, return None
        return None

@router.get("/locate", 
    status_code=status.HTTP_200_OK,
    response_model=PSGCObject
)
async def get_psgc_by_lat_long(
    lat: float = Query(..., description="Latitude of the location"),
    long: float = Query(..., description="Longitude of the location"),
    resolveProvinceCode: Optional[bool] = Query(False, description="Resolve province code to province name"),
):
    # Step 1: Get PSGC code from latitude and longitude using the shapefile
    psgc_code = str(get_psgc_from_lat_long(lat, long)).rjust(10, "0")
    
    if not psgc_code:
        raise HTTPException(status_code=404, detail="No PSGC code found for the given location")

    # Step 2: Extract the PSGC codes (barangay, province, municipal, region)
    barangay_code, province_code, municipal_code, region_code = extract_psgc_codes(psgc_code)

    # Step 3: Connect to the database and query the PSGC data
    conn = sqlite3.connect(f"db/psgc_{version}.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
        SELECT * FROM PSGC
        WHERE code LIKE ?
    """

    cursor.execute(query, (psgc_code,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="No city or municipality found for the PSGC code")

    # Convert row to dict for processing
    row_dict = dict(row)

    # Step 4: Instantiate PSGCObject with additional codes
    psgc_object = PSGCObject(
        **row_dict,
        barangay_code=barangay_code,
        province_code=province_code,
        city_municipality_code=municipal_code,
        region_code=region_code
    )

    # Step 5: Optionally resolve the province name
    if resolveProvinceCode and province_code:
        cursor.execute("SELECT name FROM PSGC WHERE code = ?", (province_code,))
        province_row = cursor.fetchone()
        if province_row:
            psgc_object.province_name = province_row['name']
        else:
            psgc_object.province_name = None

    conn.close()
    return psgc_object
