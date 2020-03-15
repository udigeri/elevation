import math

from xml.dom import minidom
import matplotlib.pyplot as plt


#READ GPX FILE
file = (input(str("Zadaj nazov suboru:\n")))
data=open(file, encoding="utf-8")

xmldoc = minidom.parse(data)
track = xmldoc.getElementsByTagName('trkpt')
elevation=xmldoc.getElementsByTagName('ele')
n_track=len(track)
wpt_name = xmldoc.getElementsByTagName('name')
wpt = xmldoc.getElementsByTagName('wpt')
n_wpt=len(wpt)

#PARSING WPT ELEMENT
lon_list_wpt=[]
lat_list_wpt=[]
elev_list_wpt=[]
time_list_wpt=[]
name_list_wpt=[]
for s in range(n_wpt):
    lon,lat=wpt[s].attributes['lon'].value,wpt[s].attributes['lat'].value
    elev=elevation[s].firstChild.nodeValue
    lon_list_wpt.append(float(lon))
    lat_list_wpt.append(float(lat))
    elev_list_wpt.append(float(elev))
    name=wpt_name[s].firstChild.nodeValue
    name_list_wpt.append(str(name))

#PARSING GPX ELEMENT
lon_list=[]
lat_list=[]
elev_list=[]
for s in range(n_track):
    lon,lat=track[s].attributes['lon'].value,track[s].attributes['lat'].value
    elev=elevation[s].firstChild.nodeValue
    lon_list.append(float(lon))
    lat_list.append(float(lat))
    elev_list.append(float(elev))
    # PARSING TIME ELEMENT
    #dt=datetime[s].firstChild.nodeValue
    #time_split=dt.split('T')
    #hms_split=time_split[1].split(':')
    #time_hour=int(hms_split[0])
    #time_minute=int(hms_split[1])
    #time_second=int(hms_split[2].split('.')[0])
    #total_second=time_hour*3600+time_minute*60+time_second
    #time_list.append(total_second)

#GEODETIC TO CARTERSIAN FUNCTION
def geo2cart(lon,lat,h):
    a=6378137 #WGS 84 Major axis
    b=6356752.3142 #WGS 84 Minor axis
    e2=1-(b**2/a**2)
    N=float(a/math.sqrt(1-e2*(math.sin(math.radians(abs(lat)))**2)))
    X=(N+h)*math.cos(math.radians(lat))*math.cos(math.radians(lon))
    Y=(N+h)*math.cos(math.radians(lat))*math.sin(math.radians(lon))
    return X,Y


#DISTANCE FUNCTION
def distance(x1,y1,x2,y2):
    d=math.sqrt((x1-x2)**2+(y1-y2)**2)
    return d


#HAVERSINE FUNCTION
def haversine(lat1,lon1,lat2,lon2,ele):
    lat1_rad=math.radians(lat1)
    lat2_rad=math.radians(lat2)
    lon1_rad=math.radians(lon1)
    lon2_rad=math.radians(lon2)
    delta_lat=lat2_rad-lat1_rad
    delta_lon=lon2_rad-lon1_rad
    a=math.sqrt((math.sin(delta_lat/2))**2+math.cos(lat1_rad)*math.cos(lat2_rad)*(math.sin(delta_lon/2))**2)
    d=2*(6359000+ele)*math.asin(a)
    return d


#POPULATE DISTANCE
step=200
d_list=[0.0]
d_list_red=[0.0]
elev_list_red=[]
l=0
for k in range(n_track-1):
    if k<(n_track-1):
        l=k+1
    else:
        l=k
    
    #DISTANCE
    #XY0=geo2cart(lon_list[k],lat_list[k],elev_list[k])
    #XY1=geo2cart(lon_list[l],lat_list[l],elev_list[l])
    #d=distance(XY0[0],XY0[1],XY1[0],XY1[1])

    #d=haversine(lat_list[k],lon_list[k],lat_list[l],lon_list[l],0)
    d=haversine(lat_list[k],lon_list[k],lat_list[l],lon_list[l],(elev_list[k]+elev_list[l])/2)
    sum_d=d+d_list[-1]
    d_list.append(sum_d)

    if k==0:
        elev_list_red.append(elev_list[0])
    else:    
        if (sum_d-d_list_red[-1])>step:
            d_list_red.append(sum_d)
            elev_list_red.append(elev_list[k])

d_list_red.append(sum_d)
elev_list_red.append(elev_list[k])

d_list_rev=d_list[::-1] #reverse list
d_list_rev_red=d_list_red[::-1] #reverse list
d_list_rev=d_list #normal list
d_list_rev_red=d_list_red #normal list

#BASIC STAT INFORMATION
mean_elev=round((sum(elev_list)/len(elev_list)),3)
min_elev=min(elev_list)
max_elev=max(elev_list)
distance=d_list_rev[-1]

#PLOT ELEVATION PROFILE
base_reg=min_elev-(mean_elev-min_elev)/2
plt.figure(figsize=(12,5))
plt.plot(d_list_rev,elev_list)
plt.plot(d_list_rev_red,elev_list_red)

plt.plot([0,distance],[min_elev,min_elev],'--g',label='min: '+str(min_elev)+' m')
plt.plot([0,distance],[max_elev,max_elev],'--r',label='max: '+str(max_elev)+' m')
plt.plot([0,distance],[mean_elev,mean_elev],'--y',label='avg: '+str(mean_elev)+' m')
plt.plot([distance,distance],[base_reg,max_elev],'--b',label='dist: '+str(round(distance, 2))+' m')
plt.fill_between(d_list_rev,elev_list,base_reg,alpha=0.2)
plt.fill_between(d_list_rev_red,elev_list_red,base_reg,alpha=0.2)

plt.text(d_list_rev[0],elev_list[0],name_list_wpt[0])
plt.text(d_list_rev[-1],elev_list[-1],name_list_wpt[-1])
plt.xlabel("Distance(m)")
plt.ylabel("Elevation(m)")
plt.grid()
plt.legend(fontsize='small')

plt.show()    

