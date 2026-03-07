import numpy as np

def classify_seabed(lat, lon):
    # Base de données des 8 catégories (ID pur)
    if lat < 28.5: return 6
    if (139.0 <= lon <= 141.0 and lat < 34.2) or (130.0 <= lon <= 132.5 and 30.0 <= lat <= 33.5): return 5
    if (138.8 <= lon <= 139.5 and 34.2 <= lat <= 34.7) or (134.0 <= lon <= 136.0 and 33.0 <= lat <= 34.0): return 7
    if (138.5 <= lon <= 138.8 and 34.6 <= lat <= 35.0) or (139.3 <= lon <= 139.6 and 34.8 <= lat <= 35.2): return 4
    if lon > 146.0: return 3
    if (138.5 <= lon <= 138.7 and 34.4 <= lat <= 34.9) or (139.4 <= lon <= 139.8 and 34.9 <= lat <= 35.3) or (lon > 143.0): return 2
    if lat < 35.5 and (130.0 <= lon <= 142.0): return 1
    return 0

def generate_strict_grid(name, lat_range, lon_range, res_points):
    print(f"Génération de {name} au format Grille (marinedata2.html)...")
    
    # Création d'un espacement mathématique parfait
    lats = np.linspace(lat_range[0], lat_range[1], res_points)
    lons = np.linspace(lon_range[0], lon_range[1], res_points)
    
    filename = f"seabed_{name.lower().replace(' ', '_')}.csv"
    
    # On écrit ligne par ligne pour garantir l'ordre : Latitudes puis Longitudes.
    # C'est CRUCIAL pour que r2 * nc + c2 fonctionne dans votre JavaScript !
    with open(filename, "w", encoding="utf-8") as f:
        f.write("lat,lon,id\n") # En-tête propre sans colonnes inutiles
        for lat in lats:
            for lon in lons:
                soil_id = classify_seabed(lat, lon)
                f.write(f"{lat:.4f},{lon:.4f},{soil_id}\n")
                
    print(f"✔ Fichier généré : {filename} ({res_points * res_points} lignes)")

# --- EXÉCUTION ---

# On utilise une résolution de 200 (ce qui donne 200x200 = 40 000 points)
# 40 000 points est un fichier léger (~800 Ko) qui se chargera en 0.1 seconde.
generate_strict_grid("Suruga Sagami", [34.3, 35.5], [138.2, 139.8], 200)

# Pour le Japon Global, on garde la même approche avec une grille de 250x250 (62 500 points)
generate_strict_grid("Japon Global", [20.0, 50.0], [120.0, 160.0], 250)