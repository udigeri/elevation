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

lon_list_wpt=[]
lat_list_wpt=[]
elev_list_wpt=[]
time_list_wpt=[]
name_list_wpt=[]
tzt_figure_name=""
tzt_name=""
tzt_color=""
lon_list_trk=[]
lat_list_trk=[]
elev_list_trk=[]
time_list_trk=[]

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
                    lon_list_wpt.append(round(float(value),5))
                elif (name == "lat"):
                    lat_list_wpt.append(round(float(value),5))
                #print(name, value)
        if list(elem):
            for child in elem:
                if child.tag.endswith("ele"):
                    elev_list_wpt.append(round(float(child.text),1))
                    #print("ele " + child.text)
                elif child.tag.endswith("time"):
                    time_list_wpt.append(child.text)
                    #print("time " + child.text)
                elif child.tag.endswith("name"):
                    name_list_wpt.append(child.text)
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
                    lon_list_trk.append(round(float(value),5))
                elif (name == "lat"):
                    lat_list_trk.append(round(float(value),5))
        if list(elem):
            for child in elem:
                if child.tag.endswith("ele"):
                    elev_list_trk.append(round(float(child.text),1))
                elif child.tag.endswith("time"):
                    time_list_trk.append(child.text)



#POPULATE TRACK DISTANCE
step=500
dist_list=[0.0]
dist_list_red=[0.0]
elev_list_red=[]
l=0

n_trk = len(elev_list_trk)
for k in range(n_trk-1):
    if k<(n_trk-1):
        l=k+1
    else:
        l=k
    d=haversine(lat_list_trk[k],lon_list_trk[k],lat_list_trk[l],lon_list_trk[l],(elev_list_trk[k]+elev_list_trk[l])/2)
    sum_dist_trk=d+dist_list[-1]
    dist_list.append(sum_dist_trk)

    if k==0:
        elev_list_red.append(elev_list_trk[0])
    else:
        if (sum_dist_trk-dist_list_red[-1])>step:
            dist_list_red.append(sum_dist_trk)
            elev_list_red.append(elev_list_trk[k])

dist_list_red.append(sum_dist_trk)
elev_list_red.append(elev_list_trk[k])

#dist_list_rev=dist_list[::-1] #reverse list
#dist_list_rev_red=dist_list_red[::-1] #reverse list
dist_list_rev=dist_list #normal list
dist_list_rev_red=dist_list_red #normal list


#POPULATE WPT DISTANCE
dist_list_wpt=sum_dist_trk
index_list_wpt=[]

n_wpt = len(elev_list_wpt)
for w in range(n_wpt):
    dist_list_wpt=sum_dist_trk
    index_list_wpt.append(0)
    for k in range(n_trk):
        dist_wpt_trkpt=haversine(lat_list_trk[k],lon_list_trk[k],lat_list_wpt[w],lon_list_wpt[w],(elev_list_trk[k]+elev_list_trk[w])/2)
        if dist_wpt_trkpt<dist_list_wpt:
            dist_list_wpt=dist_wpt_trkpt
            index_list_wpt[w]=k
        if dist_wpt_trkpt==0:
            break




#BASIC STAT INFORMATION
mean_elev=round((sum(elev_list_trk)/len(elev_list_trk)),3)
min_elev=min(elev_list_trk)
max_elev=max(elev_list_trk)
distance=round(float(sum_dist_trk), 1)


#PLOT ELEVATION PROFILE
#fig, axs =plt.subplots(1,2)




base_reg=min_elev-30#(mean_elev-min_elev)/2
plt.figure(figsize=(16,9))
plt.title(tzt_name,ha="center")

plt.plot(dist_list_rev,elev_list_trk, alpha=0.3, color="black")
#plt.plot(dist_list_rev_red,elev_list_red, alpha=0.6, color="blue")

plt.plot([0,distance],[min_elev,min_elev],'-.g',label='min: '+str(round(min_elev,1))+' m', alpha=0.5)
#plt.plot([0,distance],[mean_elev,mean_elev],'-.y',label='avg: '+str(round(mean_elev,1))+' m',alpha=0.5)
plt.plot([0,distance],[max_elev,max_elev],'-.r',label='max: '+str(round(max_elev,1))+' m',alpha=0.5)
plt.plot([distance,distance],[base_reg,elev_list_trk[-1]],'-.c',label='dĺžka: '+str(round(distance))+' m',alpha=0.5)
plt.fill_between(dist_list_rev,elev_list_trk,base_reg,alpha=0.1, facecolor=tzt_color)
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

    plt.plot([dist_list_rev[index_list_wpt[k]],dist_list_rev[index_list_wpt[k]]],[elev_list_wpt[k],max_elev+y],':k',alpha=0.5)
    plt.text(dist_list_rev[index_list_wpt[k]], max_elev+y,name_list_wpt[k]+"\nvzd:"+str(round(dist_list_rev[index_list_wpt[k]]))+"\nvys:"+str(round(elev_list_wpt[k],1)),ha="center")
    plt.plot(dist_list_rev[index_list_wpt[k]], elev_list_wpt[k],'ko',alpha=0.75)
    wpt_distance_list.append(dist_list_rev[index_list_wpt[k]])

plt.plot(wpt_distance_list, elev_list_wpt, color="black")



zlomy=[]
zlom=()
for k in range(n_wpt):
    zlom = (name_list_wpt[k], round(dist_list_rev[index_list_wpt[k]]), round(elev_list_wpt[k],1))
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

