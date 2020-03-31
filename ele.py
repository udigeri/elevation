import math
import xml.etree.ElementTree as et
from statistics import mean
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

file = (input(str("Zadaj nazov suboru:\n")))
data=open(file, encoding="utf-8")
trk_shift0=0.0
trk_shift1=0.0
step=100
reverse=0

tree = et.parse(data)
root = tree.getroot()

tzt_figure_name=""
tzt_name=""
tzt_color=""

onetime=0
desc=0
elevation=1
latitude=2
longitude=3
time=4
distanceAB=5
distanceBA=6
minAB=7
minBA=8

wpt = ["", 0.0, 0.0, 0.0, "", 0.0, 0.0, 0.0, 0.0]
wptlist = []
wpt_elevation_list=[]


trk = ["", 0.0, 0.0, 0.0, "", 0.0, 0.0]
trklist = []
trklist_reduced = []
trklistAB_reduced = []
trklistBA_reduced = []


#READ GPX FILE
for elem in root.iter():
    #PARSING GPX ELEMENT
    if elem.tag.endswith("gpx"):
        pass

    #PARSING METADATA ELEMENT
    elif elem.tag.endswith("metadata"):
        if list(elem):
            for child in elem:
                if child.tag.endswith("name"):
                    tzt_figure_name=child.text
                    #print("TrackName " + tzt_figure_name)

    #PARSING WPT ELEMENT
    elif elem.tag.endswith("wpt"):
        if elem.keys():
            wptlist.append(wpt)
            wpt = ["", 0.0, 0.0, 0.0, "", 0.0, 0.0, 0.0, 0.0]
            for name, value in elem.items():
                if (name == "lon"):
                    value = round(float(value),6)
                    wpt[longitude]=value
                elif (name == "lat"):
                    value = round(float(value),6)
                    wpt[latitude]=value
                #print(name, value)
        if list(elem):
            for child in elem:
                if child.tag.endswith("ele"):
                    child.text = str(round(float(child.text),1))
                    wpt_elevation_list.append(float(child.text))
                    wpt[elevation] = float(child.text)
                elif child.tag.endswith("time"):
                    wpt[time] = child.text
                elif child.tag.endswith("name"):
                    wpt[desc] = child.text

    #PARSING TRK ELEMENT
    elif elem.tag.endswith("trk"):
        if onetime==0:
            wptlist.pop(0)
            wptlist.append(wpt)
            onetime = 1
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
            trklist.append(trk)
            trk = ["", 0.0, 0.0, 0.0, "", 0.0, 0.0]
            for name, value in elem.items():
                if (name == "lon"):
                    value = round(float(value),6)
                    trk[longitude]=value
                elif (name == "lat"):
                    value = round(float(value),6)
                    trk[latitude]=value
        if list(elem):
            for child in elem:
                if child.tag.endswith("ele"):
                    child.text = str(round(float(child.text),1))
                    trk[elevation] = float(child.text)
                elif child.tag.endswith("time"):
                    trk[time] = child.text
                elif child.tag.endswith("name"):
                    trk[desc] = child.text

trklist.pop(0)
trklist.append(trk)


tree.write(data.name+"_rounded.gpx", encoding="UTF-8", xml_declaration=True)

# i=0
# #READ GPX FILE
# for elem in root.iter():
#     #PARSING WPT ELEMENT
#     if elem.tag.endswith("wpt"):
#         if i>=len(wptlist):
#             elem.clear()
#         else:
#             if elem.keys():
#                 for name, value in elem.items():
#                     if (name == "lon"):
#                         value = wptlist[i][longitude]
#                     elif (name == "lat"):
#                         value = wptlist[i][latitude]
#             if list(elem):
#                 for child in elem:
#                     if child.tag.endswith("ele"):
#                         child.text = str(wptlist[i][elevation])
#                     elif child.tag.endswith("time"):
#                         child.text = wptlist[i][time]
#                     elif child.tag.endswith("name"):
#                         child.text = wptlist[i][name]
#             i = i+1


# tree.write(data.name+"_wpt.gpx", encoding="UTF-8", xml_declaration=True)


#COMPUTE TRACK DISTANCE AND MAKE REDUCED TRACK LIST
trk_distance_list=[0.0]
trk_distance_list_reduced=[0.0]
trk_elevation_list_reduced=[]
trk_point_prev=0
trk_point_next=0

trk_counter = len(trklist)
for trk_point in range(trk_counter-1):
    if trk_point<(trk_counter-1):
        trk_point_next=trk_point + 1
    else:
        trk_point_next=trk_point

    distance_between_points=haversine(  trklist[trk_point][latitude],
                                        trklist[trk_point][longitude],
                                        trklist[trk_point_next][latitude],
                                        trklist[trk_point_next][longitude],
                                        (trklist[trk_point][elevation] + trklist[trk_point_next][elevation])/2  )
    sum_distance = round(trklist[trk_point][distanceAB] + distance_between_points, 1)
    trklist[trk_point_next][distanceAB] = sum_distance
    trklist[trk_point][distanceBA] = sum_distance
    trk_distance_list.append(sum_distance)

    #COMPUTE REDUCED LIST BASE ON step VALUE
    if trk_point==0:
        trklistAB_reduced.append(trklist[trk_point])
        trk_elevation_list_reduced.append(trklist[trk_point][elevation])
    else:
        if (sum_distance - trklistAB_reduced[-1][distanceAB]) >= step:
            trklistAB_reduced.append(trklist[trk_point_next])
            trk_distance_list_reduced.append(trk_distance_list[-2])


trklistAB_reduced.append(trklist[-1])
trk_distance_list_reduced.append(sum_distance)





#COMPUTE TRACK DISTANCE AND MAKE REDUCED TRACK LIST REVERSED
for trk_point in range(trk_counter-1, 0, -1):
    if trk_point == 0:
        trk_point_prev=trk_point
    else:
        trk_point_prev=trk_point - 1


    distance_between_points=haversine(  trklist[trk_point][latitude],
                                        trklist[trk_point][longitude],
                                        trklist[trk_point_prev][latitude],
                                        trklist[trk_point_prev][longitude],
                                        (trklist[trk_point][elevation] + trklist[trk_point_prev][elevation])/2  )
    sum_distance = round(trklist[trk_point][distanceBA] + distance_between_points, 1)
    trklist[trk_point_prev][distanceBA] = sum_distance


    #COMPUTE REDUCED LIST REVERSED BASE ON step VALUE
    if trk_point==trk_counter-1:
        trklistBA_reduced.append(trklist[trk_point])
    else:
        if (sum_distance - trklistBA_reduced[-1][distanceBA]) >= step:
            trklistBA_reduced.append(trklist[trk_point_prev])

trklistBA_reduced.append(trklist[0])









#FIND SHORTEST DISTANCE BETWEEN WPT AND TRK
shortest_distance=sum_distance
wpt_index_list=[]

wpt_counter = len(wptlist)
for wpt_point in range(wpt_counter):
    shortest_distance=sum_distance
    wpt_index_list.append(0)
    for trk_point in range(trk_counter):

        distance_between_points=haversine(  trklist[trk_point][latitude],
                                            trklist[trk_point][longitude],
                                            wptlist[wpt_point][latitude],
                                            wptlist[wpt_point][longitude],
                                            (trklist[trk_point][elevation] + trklist[wpt_point][elevation])/2)

        if distance_between_points < shortest_distance:
            shortest_distance = distance_between_points
            wpt_index_list[wpt_point] = trk_point
            wptlist[wpt_point][distanceAB] = trklist[trk_point][distanceAB]
            wptlist[wpt_point][distanceBA] = trklist[trk_point][distanceBA]
        if distance_between_points == 0:
            break

#CALCULATE TIME FROM A TO B
wpt_counter = len(wptlist)
for wpt_point in range(1, wpt_counter):
    dst = wptlist[wpt_point][distanceAB]-wptlist[wpt_point-1][distanceAB]
    dst /= 1000
    ele = wptlist[wpt_point][elevation]-wptlist[wpt_point-1][elevation]
    if dst == 0:
        wptlist[wpt_point][minAB] = wptlist[wpt_point-1][minAB]
    else:
        wptlist[wpt_point][minAB] = round(14*dst + 0.028*ele + 0.00036*pow(ele, 2)/dst, 2)

#CALCULATE TIME FROM B TO A
for wpt_point in range(wpt_counter-1, 0, -1):
    dst = wptlist[wpt_point][distanceAB]-wptlist[wpt_point-1][distanceAB]
    dst /= 1000
    ele = wptlist[wpt_point-1][elevation]-wptlist[wpt_point][elevation]
    if dst == 0:
        wptlist[wpt_point][minBA] = wptlist[wpt_point+1][minBA]
    else:
        wptlist[wpt_point-1][minBA] = round(14*dst + 0.028*ele + 0.00036*pow(ele, 2)/dst, 2)



print("{}\n".format(wptlist), end='\n')
# print(trklist)

#DIAGRAM DATA COMPUTATION
#BASIC STATISTICS INFORMATION
trk_elevation_list=[]
for trk_point in range(trk_counter):
    trk_elevation_list.append(trklist[trk_point][elevation])

whole_avg_elevation=round(mean(trk_elevation_list),1)#round(sum(trk_elevation_list)/len(trk_elevation_list))
whole_min_elevation=round(min(trk_elevation_list),1)
whole_max_elevation=round(max(trk_elevation_list),1)
whole_distance=round(float(sum_distance))






#ADJUST ELEVATION
#y=k*x+z
trk_elevation_list_shifted=[]

if trk_shift0>trk_shift1:
    for trk_point in range(trk_counter):
        trk_shift=(trk_counter-trk_point)/trk_counter*trk_shift0 + trk_shift1
        trk_elevation_list_shifted.append(round(trklist[trk_point][elevation] + trk_shift,1))
else:
    for trk_point in range(trk_counter):
        trk_shift=(trk_point)/trk_counter*trk_shift1 + trk_shift0
        trk_elevation_list_shifted.append(round(trklist[trk_point][elevation] + trk_shift,1))





#READ GPX FILE
data.close()
data=open(file, encoding="utf-8")
tree_new = et.parse(data)
i=0
for elem in tree_new.iter():
    #PARSING TRKPT ELEMENT
    if elem.tag.endswith("trkpt"):
        if list(elem):
            for child in elem:
                if child.tag.endswith("ele"):
                    child.text = str(trk_elevation_list_shifted[i])
                    i += 1

tree_new.write(data.name+"_shifted.gpx", encoding="UTF-8", xml_declaration=True)



trk_distance_list_output = []
trk_elevation_list_output = []
trk_elevation_list_shifted_output = []

trk_distance_list_reduced_output = []
trk_elevation_list_reduced_output = []

# wpt_elevation_list_output = []
wpt_index_list_output = []

if reverse:
    for trk_point in range(trk_counter,0,-1):
        trk_distance_list_output.append(trklist[trk_point-1][distanceBA])   #reverse list
        trk_elevation_list_output.append(trklist[trk_point-1][elevation])   #reverse list
        trk_elevation_list_shifted_output = trk_elevation_list_shifted[::-1] #reverse list

    for trk_point in range(len(trklistBA_reduced)):
        trk_distance_list_reduced_output.append(trklistBA_reduced[trk_point][distanceBA]) #reverse list
        trk_elevation_list_reduced_output.append(trklistBA_reduced[trk_point][elevation]) #reverse list
        
    wpt_elevation_list_output=wpt_elevation_list[::-1]                  #reverse list
    for wpt_point in range(wpt_counter,0,-1):
        wpt_index_list_output.append(trk_counter-1-wpt_index_list[wpt_point-1])#reverse list

else:
    for trk_point in range(trk_counter):
        trk_distance_list_output.append(trklist[trk_point][distanceAB]) #reverse list
        trk_elevation_list_output.append(trklist[trk_point][elevation]) #reverse list
        trk_elevation_list_shifted_output = trk_elevation_list_shifted  #reverse list

    for trk_point in range(len(trklistAB_reduced)):
        trk_distance_list_reduced_output.append(trklistAB_reduced[trk_point][distanceAB]) #reverse list
        trk_elevation_list_reduced_output.append(trklistAB_reduced[trk_point][elevation]) #reverse list
        
    wpt_elevation_list_output=wpt_elevation_list                        #reverse list
    wpt_index_list_output=wpt_index_list                                #reverse list



#PLOT ELEVATION PROFILE
#fig, axs =plt.subplots(1,2)

base_reg=whole_min_elevation-20#(whole_avg_elevation-whole_min_elevation)/2
plt.figure(figsize=(16,10))
plt.title(tzt_name, ha="center")

#PLOT WHOLE TRACKPOITS
plt.plot(trk_distance_list_output, 
        trk_elevation_list_output, 
        alpha=0.3, 
        color="black")
#PLOT WHOLE TRACKPOITS WITH ELEVATION SHIFTED
plt.plot(trk_distance_list_output, 
        trk_elevation_list_shifted_output, 
        alpha=0.6, 
        color="pink")

#PLOT REDUCED TRACKPOITS DEPENDS ON step VALUE
plt.plot(trk_distance_list_reduced_output, 
        trk_elevation_list_reduced_output, 
        alpha=0.6, 
        color="blue")





#PLOT LINES FOR LEGEND
plt.plot([0, whole_distance],
        [whole_min_elevation, whole_min_elevation], 
        '-.g', 
        label='min: '+str(round(whole_min_elevation,1))+' m', 
        alpha=0.5)
#plt.plot([0, whole_distance],[whole_avg_elevation, whole_avg_elevation],'-.y',label='avg: '+str(round(whole_avg_elevation,1))+' m',alpha=0.5)
plt.plot([0, whole_distance], 
        [whole_max_elevation, whole_max_elevation], 
        '-.r', 
        label='max: '+str(round(whole_max_elevation,1))+' m', 
        alpha=0.5)
plt.plot([whole_distance, whole_distance], 
        [base_reg, trk_elevation_list_output[-1]], 
        '-.c', 
        label='dĺžka: '+str(round(whole_distance))+' m', 
        alpha=0.5)

#FILL TZT COLOR FROM ELEVATION TO BASEREG
plt.fill_between(trk_distance_list_output, 
        trk_elevation_list_output, 
        base_reg, 
        alpha=0.4, 
        facecolor=tzt_color)
#FILL TZT COLOR FROM ELEVATION TO BASEREG REDUCED
plt.fill_between(trk_distance_list_reduced_output, 
        trk_elevation_list_reduced_output, 
        base_reg, 
        alpha=0.2, 
        facecolor=tzt_color)



print("normal_list:", len(trklist))
print("reduced_list (each {:.1f} m): {:d}".format(step, len(trklistAB_reduced)))
print("wpt_list:", len(wptlist))






shift=whole_avg_elevation/20
ele_shift=shift

wpt_distance_list_output = []
for wpt_point in range(wpt_counter):

    if ele_shift>=shift:
        ele_shift=0
    elif 0 < ele_shift <shift:
        ele_shift=shift
    else:
        ele_shift=shift/2


    x = trk_distance_list_output[wpt_index_list_output[wpt_point]]
    y = wpt_elevation_list_output[wpt_point]
    #PLOT VERTICAL LINE TO WPT
    plt.plot([x, x],
            [y, whole_max_elevation + ele_shift],
            ':k',
            alpha=0.5)
    #PLOT BALL FOR WPT
    plt.plot(x, 
            y,
            'ko',
            alpha=0.75)
    #PLOT NAME OF WPT
    plt.text(x, 
            whole_max_elevation + ele_shift,
            wptlist[wpt_point][desc] + "\n" + str(round(x)) + "\n" + str(round(y, 1)),
            ha="center")

    wpt_distance_list_output.append(x)
#PLOT LINES BETWEEN WPT
plt.plot(wpt_distance_list_output, wpt_elevation_list_output, alpha=0.75, color="black")



zlomy=[]
zlom=()
for wpt_point in range(wpt_counter):
    zlom = (wptlist[wpt_point][desc], round(trk_distance_list_output[wpt_index_list_output[wpt_point]]), round(wpt_elevation_list_output[wpt_point],1))
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

