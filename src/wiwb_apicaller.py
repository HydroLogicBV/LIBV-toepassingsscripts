# -*- coding: utf-8 -*-

from typing import Dict
from pathlib import Path
import os, requests, sys

# WIWB api url
API_URL = "https://wiwb.hydronet.com/api/grids/get"


# =============================================================================
# HULP FUNCTIES
# =============================================================================

def build_payload(startdate: str, enddate: str, datasourcecode, variablecodes, extent=None) -> Dict:
    
    # Bouwt een payload voor het opvragen data via de WIWB-dataservice
    #
    # Parameters:
    # -----
    #   startdate : str 
    #       startdatum van de periode waarvoor data wordt opgevraagd
    #   enddate : str
    #       einddatum van de periode waarvoor data wordt opgevraagd
    #   entent : dict
    #       ruimtelijke extent (bounding box) van het onderzoeksgebied, inclusief EPSG-code
    #         Verwacht formaat:
    #            {
    #                "Xll": <float>,
    #                "Yll": <float>,
    #                "Xur": <float>,
    #                "Yur": <float>,
    #                "SpatialReference": {"Epsg": 28992}
    #            }
    #
    # Returns:
    # -----
    #     dict: Een dictionary die als payload kan worden gebruikt in een API-request voor het opvragen van satellietbodemvochtgegevens in GeoTIFF-formaat

    return {
        "Readers": [
            {
                "DataSourceCode": datasourcecode,
                "Settings": {
                    "StructureType": "Grid",
                    "VariableCodes": variablecodes,
                    "StartDate": startdate,
                    "EndDate": enddate,
                    "Extent": extent,
                }
            }
        ],
        "Exporter": {
            "DataFormatCode": "geotiff",
            "SpatialReference": {"Epsg": 28992}
        }
    }


def fetch_raster(headers: Dict, payload: Dict, out_path: Path):

    # voert een API-aanvraag uit om rasterdata op te halen en slaat het resultaat op als bestand
    #
    # Parameters:
    # -----
    #   headers : dict
    #       HTTP-headers met o.a. een geldig 'Authorization'-token
    #   payload : dict
    #       JSON-payload met de instellingen en parameters voor de data-aanvraag
    #   out_path : Path
    #       Bestandspad waar het opgehaalde rasterbestand wordt opgeslagen
    #
    # Raises:
    #   RuntimeError: Als de API-aanvraag geen succesvolle statuscode (200) retourneert

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        with open(out_path, "wb") as f:
            f.write(response.content)
        print(f"Opgeslagen: {out_path}")
    else:
        raise RuntimeError(f"Fout {response.status_code}: {response.text}")


def read_raster(file_path, geometry):
    
    # lees een raster in en knip het uit op de gegeven geometrie
    #
    # Parameters:
    # --------
    #   file_path : Path or str
    #       pad naar het rasterbestand (.tif)
    #   geometry : list
    #       lijst van shapely geometrieën van een waterschap om op te klippen
    # 
    # Returns:
    # --------
    #   np.ndarray : 2D array van het uitgesneden raster voor het waterschap

    with rasterio.open(file_path) as src:
        out_image, _ = mask(
            src, geometry, crop=True, filled=True, nodata=np.nan 
        )
        arr = out_image[0].astype(float)
        arr[arr == -999] = np.nan
        return arr

