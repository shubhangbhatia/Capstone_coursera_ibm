"""Create a Folium map of SpaceX launch sites (coordinates are public launchpad locations)."""
import folium
sites = [
    ("Cape Canaveral SLC-40", 28.5618571, -80.577366),
    ("Kennedy Space Center LC-39A", 28.6080585, -80.6039558),
    ("Vandenberg SLC-4E", 34.632093, -120.610829)
]
m = folium.Map(location=[30.5,-95], zoom_start=4, tiles="CartoDB positron")
for name, lat, lon in sites:
    folium.Marker([lat,lon], tooltip=name, popup=f"<b>{name}</b><br>Public launch-site reference").add_to(m)
m.save("launch_sites_map.html")
print("Saved launch_sites_map.html")
