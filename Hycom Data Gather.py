import xarray as xr
import pandas as pd
import numpy as np

# Connexion stable
url = "https://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0/uv3z"
ds = xr.open_dataset(url, decode_times=False)

def get_stable_data(depth, lat_range, lon_range, res):
    # On prend une zone un peu plus large pour l'extrapolation
    sub = ds.sel(
        lat=slice(lat_range[0]-0.1, lat_range[1]+0.1), 
        lon=slice(lon_range[0]-0.1, lon_range[1]+0.1)
    ).isel(time=-1).sel(depth=depth, method="nearest")

    # ÉTAPE CRUCIALE : Remplir les blancs (extrapolate) avant d'interpoler
    sub = sub.interpolate_na(dim='lon', method='linear', fill_value="extrapolate")
    sub = sub.interpolate_na(dim='lat', method='linear', fill_value="extrapolate")

    # Interpolation à 1000 points (Taille de fichier parfaite pour IsoFinder)
    new_lat = np.linspace(lat_range[0], lat_range[1], res)
    new_lon = np.linspace(lon_range[0], lon_range[1], res)
    sub = sub.interp(lat=new_lat, lon=new_lon)

    df = sub[['water_u', 'water_v']].to_dataframe().reset_index()
    df = df.rename(columns={'water_u': 'u', 'water_v': 'v'})
    
    # Correction Longitude Standard pour Leaflet
    df['lon'] = np.where(df['lon'] > 180, df['lon'] - 360, df['lon'])
    
    # Nettoyage final des valeurs aberrantes
    return df.dropna(subset=['u', 'v'])

# Zone Suruga + Sagami Bay
lat_b, lon_b = [34.3, 35.3], [138.3, 139.7]

print("Génération du fichier de secours (1000 pts)...")
d600 = get_stable_data(600, lat_b, lon_b, 1000)
d700 = get_stable_data(700, lat_b, lon_b, 1000)

# On fusionne les profondeurs et on réduit le poids du CSV
df_final = pd.concat([d600, d700]).round(3)

# Sauvegarde sous un nom simple
df_final[['lat', 'lon', 'u', 'v']].to_csv("suruga_sagami_fixed.csv", index=False)
print("Fichier 'suruga_sagami_fixed.csv' prêt. Essaie celui-ci !")