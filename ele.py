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
                    wpt_lon_list.append(round(float(value),6))
                elif (name == "lat"):
                    wpt_lat_list.append(round(float(value),6))
                #print(name, value)
        if list(elem):
            for child in elem:
                if child.tag.endswith("ele"):
                    wpt_elevation_list.append(round(float(child.text),1))
                    #child.text = str(round(float(child.text),1)-50)
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
                    trk_lon_list.append(round(float(value),6))
                elif (name == "lat"):
                    trk_lat_list.append(round(float(value),6))
        if list(elem):
            for child in elem:
                if child.tag.endswith("ele"):
                    child.text = str(round(float(child.text)+5.52,1))
                    trk_elevation_list.append(round(float(child.text),1))

                elif child.tag.endswith("time"):
                    trk_time_list.append(child.text)



tree.write("test.xml", encoding="UTF-8", xml_declaration=True)


#COMPUTE TRACK DISTANCE AND MAKE REDUCED TRACK LIST
step=50
trk_distance_list=[0.0]
trk_distance_list_reduced=[0.0]
trk_elevation_list_reduced=[]
trk_point_next=0

trk_counter = len(trk_elevation_list)
for trk_point in range(trk_counter-1):
    if trk_point<(trk_counter-1):
        trk_point_next=trk_point + 1
    else:
        trk_point_next=trk_point

    distance_between_points=haversine(  trk_lat_list[trk_point],
                                        trk_lon_list[trk_point],
                                        trk_lat_list[trk_point_next],
                                        trk_lon_list[trk_point_next],
                                        (trk_elevation_list[trk_point] + trk_elevation_list[trk_point_next])/2)

    sum_distance_trk=trk_distance_list[-1] + distance_between_points
    trk_distance_list.append(sum_distance_trk)

    #COMPUTE REDUCED LIST
    if trk_point==0:
        trk_elevation_list_reduced.append(trk_elevation_list[0])
    else:
        if (sum_distance_trk-trk_distance_list_reduced[-1])>=step:
            trk_distance_list_reduced.append(trk_distance_list[-2])
            trk_elevation_list_reduced.append(trk_elevation_list[trk_point])

trk_distance_list_reduced.append(sum_distance_trk)
trk_elevation_list_reduced.append(trk_elevation_list[trk_point])

trk_distance_list_output=trk_distance_list[::-1]                        #reverse list
trk_distance_list_reduced_output=trk_distance_list_reduced[::-1]        #reverse list
trk_distance_list_output=trk_distance_list                              #normal list
trk_distance_list_reduced_output=trk_distance_list_reduced              #normal list


#FIND SHORTEST DISTANCE BETWEEN WPT AND TRK
shortest_distance=sum_distance_trk
wpt_index_list=[]

wpt_counter = len(wpt_elevation_list)
for wpt_point in range(wpt_counter):
    shortest_distance=sum_distance_trk
    wpt_index_list.append(0)
    for trk_point in range(trk_counter):

        distance_between_points=haversine(  trk_lat_list[trk_point],
                                            trk_lon_list[trk_point],
                                            wpt_lat_list[wpt_point],
                                            wpt_lon_list[wpt_point],
                                            (trk_elevation_list[trk_point]+trk_elevation_list[wpt_point])/2)

        if distance_between_points<shortest_distance:
            shortest_distance=distance_between_points
            wpt_index_list[wpt_point]=trk_point
        if distance_between_points==0:
            break



#DIAGRAM DATA COMPUTATION
#BASIC STATISTICS INFORMATION
whole_avg_elevation=round((sum(trk_elevation_list)/len(trk_elevation_list)),3)
whole_min_elevation=min(trk_elevation_list)
whole_max_elevation=max(trk_elevation_list)
whole_distance=round(float(sum_distance_trk), 1)





#PLOT ELEVATION PROFILE
#fig, axs =plt.subplots(1,2)

base_reg=whole_min_elevation-20#(whole_avg_elevation-whole_min_elevation)/2
plt.figure(figsize=(16,9))
plt.title(tzt_name, ha="center")

#PLOT WHOLE TRACKPOITS
plt.plot(trk_distance_list_output,trk_elevation_list, alpha=0.3, color="black")
#PLOT REDUCED TRACKPOITS DEPENDS ON step VALUE
#plt.plot(trk_distance_list_reduced_output,trk_elevation_list_reduced, alpha=0.6, color="blue")

#PLOT LINES FOR LEGEND
plt.plot([0,whole_distance],[whole_min_elevation,whole_min_elevation],'-.g',label='min: '+str(round(whole_min_elevation,1))+' m', alpha=0.5)
#plt.plot([0,whole_distance],[whole_avg_elevation,whole_avg_elevation],'-.y',label='avg: '+str(round(whole_avg_elevation,1))+' m',alpha=0.5)
plt.plot([0,whole_distance],[whole_max_elevation,whole_max_elevation],'-.r',label='max: '+str(round(whole_max_elevation,1))+' m',alpha=0.5)
plt.plot([whole_distance,whole_distance],[base_reg,trk_elevation_list[-1]],'-.c',label='dĺžka: '+str(round(whole_distance))+' m',alpha=0.5)

#FILL TZT COLOR FROM ELEVATION TO BASEREG
plt.fill_between(trk_distance_list_output,trk_elevation_list,base_reg, alpha=0.2, facecolor=tzt_color)
#FILL TZT COLOR FROM ELEVATION TO BASEREG REDUCED
# #plt.fill_between(trk_distance_list_reduced_output,trk_elevation_list_reduced,base_reg,alpha=0.2, facecolor=tzt_color)


shift=whole_avg_elevation/20
y=shift

wpt_distance_list=[]
for wpt_point in range(wpt_counter):

    if y>shift:
        y=shift
    elif 0 < y <=shift:
        y=0
    else:
        y=shift/2

    #PLOT VERTICAL LINE TO WPT
    plt.plot([trk_distance_list_output[wpt_index_list[wpt_point]],trk_distance_list_output[wpt_index_list[wpt_point]]],[wpt_elevation_list[wpt_point],whole_max_elevation+y],':k',alpha=0.5)
    #PLOT NAME OF WPT
    plt.text(trk_distance_list_output[wpt_index_list[wpt_point]], whole_max_elevation+y,wpt_name_list[wpt_point]+"\n"+str(round(trk_distance_list_output[wpt_index_list[wpt_point]]))+"\n"+str(round(wpt_elevation_list[wpt_point],1)),ha="center")
    #PLOT BALL FOR WPT
    plt.plot(trk_distance_list_output[wpt_index_list[wpt_point]], wpt_elevation_list[wpt_point],'ko',alpha=0.75)

    wpt_distance_list.append(trk_distance_list_output[wpt_index_list[wpt_point]])
#PLOT LINES BETWEEN WPT zlomy
plt.plot(wpt_distance_list, wpt_elevation_list, color="black")



zlomy=[]
zlom=()
for wpt_point in range(wpt_counter):
    zlom = (wpt_name_list[wpt_point], round(trk_distance_list_output[wpt_index_list[wpt_point]]), round(wpt_elevation_list[wpt_point],1))
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

