import math
import xml.etree.ElementTree as et
#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


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


#READ GPX FILE
#file = (input(str("Zadaj nazov suboru:\n")))
data=open("8674.gpx", encoding="utf-8")

tree = et.parse(data)
root = tree.getroot()
tree.write("test.xml", encoding="UTF-8", xml_declaration=True)

tzt_figure_name=""
tzt_name=""
tzt_color=""
wpt_lon_list=[]
wpt_lat_list=[]
wpt_elevation_list=[]
wpt_time_list=[]
wpt_name_list=[]
trk_lon_list=[]
trk_lat_list=[]
trk_elevation_list=[]
trk_time_list=[]

#READ GPX FILE
for elem in tree.getiterator():
    #PARSING METADATA ELEMENT
    if elem.tag.endswith("metadata"):
        if list(elem):
            for child in elem:
                if child.tag.endswith("name"):
                    tzt_figure_name=child.text
                    #print("TrackName " + tzt_figure_name)

    #PARSING WPT ELEMENT
    elif elem.tag.endswith("wpt"):
        if elem.keys():
            for name, value in elem.items():
                if (name == "lon"):
                    wpt_lon_list.append(round(float(value),5))
                elif (name == "lat"):
                    wpt_lat_list.append(round(float(value),5))
                #print(name, value)
        if list(elem):
            for child in elem:
                if child.tag.endswith("ele"):
                    wpt_elevation_list.append(round(float(child.text),1))
                    #print("ele " + child.text)
                elif child.tag.endswith("time"):
                    wpt_time_list.append(child.text)
                    #print("time " + child.text)
                elif child.tag.endswith("name"):
                    wpt_name_list.append(child.text)
                    #print("name " + child.text)

    #PARSING TRK ELEMENT
    elif elem.tag.endswith("trk"):
        if list(elem):
            for child in elem:
                if child.tag.endswith("name"):
                    tzt_name+=child.text
                elif child.tag.endswith("desc"):
                    tzt_name+=" "+child.text
                elif child.tag.endswith("extensions"):
                    if list(child):
                        for child1 in child:
                            if child1.tag.endswith("TrackExtension"):
                                if list(child1):
                                    for child2 in child1:
                                        if child2.tag.endswith("DisplayColor"):
                                            tzt_color=child2.text

    #PARSING TRKPT ELEMENT
    elif elem.tag.endswith("trkpt"):
        if elem.keys():
            for name, value in elem.items():
                if (name == "lon"):
                    trk_lon_list.append(round(float(value),5))
                elif (name == "lat"):
                    trk_lat_list.append(round(float(value),5))
        if list(elem):
            for child in elem:
                if child.tag.endswith("ele"):
                    trk_elevation_list.append(round(float(child.text),1))
                elif child.tag.endswith("time"):
                    trk_time_list.append(child.text)





#POPULATE TRACK DISTANCE
step=500
dist_list=[0.0]
dist_list_red=[0.0]
elev_list_red=[]
l=0

n_trk = len(trk_elevation_list)
for k in range(n_trk-1):
    if k<(n_trk-1):
        l=k+1
    else:
        l=k
    d=haversine(trk_lat_list[k],trk_lon_list[k],trk_lat_list[l],trk_lon_list[l],(trk_elevation_list[k]+trk_elevation_list[l])/2)
    sum_dist_trk=d+dist_list[-1]
    dist_list.append(sum_dist_trk)

    if k==0:
        elev_list_red.append(trk_elevation_list[0])
    else:
        if (sum_dist_trk-dist_list_red[-1])>step:
            dist_list_red.append(sum_dist_trk)
            elev_list_red.append(trk_elevation_list[k])

dist_list_red.append(sum_dist_trk)
elev_list_red.append(trk_elevation_list[k])

#dist_list_rev=dist_list[::-1] #reverse list
#dist_list_rev_red=dist_list_red[::-1] #reverse list
dist_list_rev=dist_list #normal list
dist_list_rev_red=dist_list_red #normal list


#POPULATE WPT DISTANCE
dist_list_wpt=sum_dist_trk
index_list_wpt=[]

n_wpt = len(wpt_elevation_list)
for w in range(n_wpt):
    dist_list_wpt=sum_dist_trk
    index_list_wpt.append(0)
    for k in range(n_trk):
        dist_wpt_trkpt=haversine(trk_lat_list[k],trk_lon_list[k],wpt_lat_list[w],wpt_lon_list[w],(trk_elevation_list[k]+trk_elevation_list[w])/2)
        if dist_wpt_trkpt<dist_list_wpt:
            dist_list_wpt=dist_wpt_trkpt
            index_list_wpt[w]=k
        if dist_wpt_trkpt==0:
            break




#BASIC STAT INFORMATION
mean_elev=round((sum(trk_elevation_list)/len(trk_elevation_list)),3)
min_elev=min(trk_elevation_list)
max_elev=max(trk_elevation_list)
distance=round(float(sum_dist_trk), 1)


#PLOT ELEVATION PROFILE
#fig, axs =plt.subplots(1,2)




base_reg=min_elev-30#(mean_elev-min_elev)/2
plt.figure(figsize=(16,9))
plt.title(tzt_name,ha="center")

plt.plot(dist_list_rev,trk_elevation_list, alpha=0.3, color="black")
#plt.plot(dist_list_rev_red,elev_list_red, alpha=0.6, color="blue")

plt.plot([0,distance],[min_elev,min_elev],'-.g',label='min: '+str(round(min_elev,1))+' m', alpha=0.5)
#plt.plot([0,distance],[mean_elev,mean_elev],'-.y',label='avg: '+str(round(mean_elev,1))+' m',alpha=0.5)
plt.plot([0,distance],[max_elev,max_elev],'-.r',label='max: '+str(round(max_elev,1))+' m',alpha=0.5)
plt.plot([distance,distance],[base_reg,trk_elevation_list[-1]],'-.c',label='dĺžka: '+str(round(distance))+' m',alpha=0.5)
plt.fill_between(dist_list_rev,trk_elevation_list,base_reg,alpha=0.1, facecolor=tzt_color)
#plt.fill_between(dist_list_rev_red,elev_list_red,base_reg,alpha=0.2)

y=mean_elev/20

wpt_distance_list=[]

for k in range(n_wpt):

    if y>mean_elev/20:
        y=mean_elev/20
    elif 0 < y <=mean_elev/20:
        y=0
    else:
        y=mean_elev/10

    plt.plot([dist_list_rev[index_list_wpt[k]],dist_list_rev[index_list_wpt[k]]],[wpt_elevation_list[k],max_elev+y],':k',alpha=0.5)
    plt.text(dist_list_rev[index_list_wpt[k]], max_elev+y,wpt_name_list[k]+"\nvzd:"+str(round(dist_list_rev[index_list_wpt[k]]))+"\nvys:"+str(round(wpt_elevation_list[k],1)),ha="center")
    plt.plot(dist_list_rev[index_list_wpt[k]], wpt_elevation_list[k],'ko',alpha=0.75)
    wpt_distance_list.append(dist_list_rev[index_list_wpt[k]])

plt.plot(wpt_distance_list, wpt_elevation_list, color="black")



zlomy=[]
zlom=()
for k in range(n_wpt):
    zlom = (wpt_name_list[k], round(dist_list_rev[index_list_wpt[k]]), round(wpt_elevation_list[k],1))
    zlomy.append(zlom)

collabel=(tzt_figure_name, "Kilom. poloha (m)", "Nadm. výška (m)")
#axs[0].axis('tight')
#axs[0].axis('off')

#the_table = plt.table(cellText=zlomy,colLabels=collabel,loc='center')




plt.xlabel("Vzdialenosť(m)")
plt.ylabel("Nadm. výška(m)")
plt.grid()
plt.legend(fontsize='small')
plt.savefig(tzt_figure_name + ".png")



plt.show()

