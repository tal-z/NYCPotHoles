#import contextily as ctx
from sodapy import Socrata
import geopandas as gpd
from matplotlib import  pyplot as plt
from datetime import datetime
import os
from dotenv import load_dotenv
#import adjustText as aT
load_dotenv()

start_date = '2020-03-12' #input("Start Date:  ")
end_date = '2021-03-12'  #input("End Date:  ")

"""Get pothole data from NYC Open Data into a GeoDataFrame."""
# 1. Authenticate user account on NYC Open Data platform (Socrata).
print("Logging into NYC Open Data")
client = Socrata("data.cityofnewyork.us",
                 'odQdEcIxnATZPym3KySwgWw27',
                 username=os.getenv('username'),
                 password=os.getenv('password'))

# 2. Request records from the desired resource:
# https://data.cityofnewyork.us/Transportation/Street-Pothole-Work-Orders-Closed-Dataset-/x9wy-ing4

print(f"Getting pothole data from {start_date} to {end_date}. "
      f"There are more than 300,000 records to retrieve, please be patient!")
results = client.get("x9wy-ing4",
                     content_type='geojson',
                     limit=304000,
                     where=f"rptdate between '{start_date}' and '{end_date}'")

# 3. Convert to records into a GeoDataFrame, setting projection to match community district boundary features projection.
potholes_gdf = gpd.GeoDataFrame.from_features(results).set_crs(epsg=4326, inplace=True)

# 4. Calculate response time for each pothole in the dataset, in days
print("Calculating the response time for each pothole.")
potholes_gdf['response_time'] = potholes_gdf['rptclosed'].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT00:00:00.000")) \
                                - potholes_gdf['rptdate'].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT00:00:00.000"))
potholes_gdf['response_time'] = potholes_gdf['response_time']\
                                    .apply(lambda x: x.to_pytimedelta().total_seconds()) / 60 / 60 / 24



"""Get community district boundaries from BYTES of the Big Apple."""
# 5. Request records from BYTES of the Big Apple
print("Getting community district boundaries from BYTES of the Big Apple.")
community_districts_gdf = gpd.read_file("https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Community_Districts/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson")
# Get rid of non-residential/open space districts, which dramatically skew the data.
community_districts_gdf.drop(community_districts_gdf[community_districts_gdf['BoroCD']
                             .isin([164, 226, 227, 228, 355, 356, 480, 481, 482, 483, 484, 595])].index, inplace=True)

"""Compare and analyze the two datasets"""
# 6. Spatially join the two datasets together, with potholes as the left table and community districts at the right table.
# This will allow us to add community district as a feature of each pothole.
print("Spatially analyzing data.")
potholes_with_commdist = gpd.sjoin(potholes_gdf, community_districts_gdf, how="inner", op='intersects')

# 7. Pivot and summarize the data, so that we can get the average response time for each community district.
commdists_with_potholes = gpd.GeoDataFrame(potholes_with_commdist.pivot_table(index='BoroCD', values='response_time'))

# 8. Re-join the pivoted data with original records from BYTES of the Big Apple,
# so that we can add average response time as a feature of each community district.
community_districts_gdf = community_districts_gdf.merge(commdists_with_potholes, how='left', on='BoroCD')


"""Create a choropleth map using average response time as the summary value."""
print("Preparing map...")
# 9. Throw the data into a matplotlib plot, using GeoPandas' in-built plot method.
community_districts_gdf.plot(column='response_time',
                             legend=True,
                             cmap='RdYlGn_r',
                             legend_kwds={'label': "Time in Days"},
                             figsize=(10, 8))
plt.title("Pothole Repair in New York City\nAvg. Response Times by Community District")


"""Some optional extras to decorate the map."""
# Add an optional base map.
# Note that ax will first need to be set.
#ctx.add_basemap(ax, zoom=1)

# Add optional labels to community districts.
# Note that ctx will need to be imported.
# Note that aT will need to be imported.
#community_districts_gdf['rep'] = community_districts_gdf['geometry'].centroid
#cd_points = community_districts_gdf.copy()
#cd_points.set_geometry("rep", inplace = True)
#texts = []
#for x, y, label in zip(cd_points.geometry.x, cd_points.geometry.y, cd_points["BoroCD"]):
#    texts.append(plt.text(x, y, label, fontsize = 6))
#aT.adjust_text(texts, force_points=0.3, force_text=0.5, expand_points=(1,1), expand_text=(1,1),
#               arrowprops=dict(arrowstyle="-", color='grey', lw=0.5))



# 10. Display the map.
plt.show()