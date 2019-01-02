#Matthew Erickson
#Professor Quesada
#1200-102
#12/6/17
#ATOC Final Project

import numpy as np
import matplotlib.colors as colors
import matplotlib.pyplot as pl
from datetime import datetime

#Task 1a 
"""
This function counts number of rows in each file.  
Since number of rows is given to us this is not neccesary but I wanted to show 
how it would be done if we diddn't know

Arguments: 
    none
Returns:
    none
"""
def num_rows():
    file_obj=open("air_temp.1900") 
    rows=0
    for line in file_obj.readlines():
        rows+=1
    return rows

"""
This function reads in the files for both temp and precipitation and
calculates the 6 values we need from each row: min, max, mean,and sum.
It also stores the latitude and longitude from each row as well.
We then take these values and store them in two numpy arrays(one for temp and precip)

Arguments: 
    none
Returns:
    none
"""
#Task 1b +1c

def read_files():
   
    stack=[]
    for i in range(1900,2015):
        filename="air_temp_2014/air_temp."+str(i)
        fr=open(filename)
        layer=[]
        for line in fr.readlines():
            monthly_temp=[]
            row_data=[]
            line=line.strip()
            postsplit=line.split()
            row_data.append(postsplit[0])
            row_data.append(postsplit[1])
            monthly_temp=postsplit[2:]
            temp=monthly_temp
            monthly_temp=[float(i) for i in temp]
            row_data.append(min(monthly_temp))
            row_data.append(max(monthly_temp))
            row_data.append(float(sum(monthly_temp)/len(monthly_temp)))
            row_data.append(sum(monthly_temp))
            layer.append(row_data)
        stack.append(layer)
    nptemp=np.array(stack)

    np.save("smaller_temp.npy", nptemp)
    
   
    stack=[]    
    for i in range(1900,2015):
        filename="precip_2014/precip."+str(i)
        fr=open(filename)
        layer=[]
        print("Working on year ",i)
        for line in fr.readlines():
            monthly_precip=[]
            row_data=[]
            line=line.strip()
            postsplit=line.split()
            row_data.append(postsplit[0])
            row_data.append(postsplit[1])
            monthly_precip=postsplit[2:]
            precip=monthly_precip
            monthly_precip=[float(i) for i in precip]
            row_data.append(min(monthly_precip))
            row_data.append(max(monthly_precip))
            row_data.append(float(sum(monthly_precip)/len(monthly_precip)))
            row_data.append(sum(monthly_precip))
            layer.append(row_data)
    
        stack.append(layer)
    npprecip=np.array(stack)
  
    np.save("smaller_precip.npy", npprecip)
    return


#Task 3
"""
Here we load the numpy array with temp values and graph
the mean temp from each station in each year and graph 
those data points.  Uses nested for loops to go file by file
and row by row, accesing the 4th index which is the mean.
We us matplotlib to make a plot over the years 1900-2014.

Arguments: 
    none
Returns:
    none
"""
def graph_mean_temp():
    array=np.load("smaller_temp.npy")
    temps=[]
    for i in range(115):
        print("computing layer: ",i)
        sum_avg=0
        for j in range(85794):
            mean=array[i][j][4]
            sum_avg+=float(mean)
        global_avg=sum_avg/(85794)
        temps.append(global_avg)
    
    x=[i for i in range(1900,2015)]
    y=temps
    
    #graph_mean_temp=pl.figure(1)
    pl.figure(figsize=(15,7))
    pl.title("Time series global annual mean surface temperature from 1900 to 2014")
    pl.xlabel("Year")
    pl.ylabel("Temperature in deg Celsius")
    pl.plot(x, y)
    pl.show()
    #graph_mean_temp.savefig("graph_mean_temp.pdf") 
    #pl.close()    
    
#Task 4
"""
Here we do essentially same thing in task 3 but for precipitation.
We load the precip numpy array and use nested for loops to get data we need.
We plot mean preciptation fromm each year over the years 1900-2014.

Arguments: 
    none
Returns:
    none
"""    
def graph_total_precip():
    array=np.load("smaller_precip.npy")
    precip=[]
    for i in range(115):
        print("computing layer: ",i)
        total=0
        for j in range(85794):
            total+=float(array[i][j][5])
        precip.append(total)
    
    x=[i for i in range(1900,2015)]
    y=[i/1000 for i in precip] #list comprehension dividing by 1000 to conver ml to L
    
    graph_mean_precip=pl.figure(2)
    #pl.figure(figsize=(15,7))
    pl.plot(x, y)
    pl.title('Time series of global annual total precipitation from 1900 to 2014')
    pl.xlabel('Year')
    pl.ylabel('Precipitation in L')
    pl.show()
    graph_mean_precip.savefig("graph_mean_precip.pdf") 
    pl.close() 
    
#Task 5a
"""
In this task we use only for loops and no numpy operations.  We load temp array
and plot the temp anomalies over the period 1900-2014.  An anomaly is the difference
between the average temp of all the years (1900-2014) and an avg temp from a single
year.  If that paticular year was above the total avg, that is a positive anomaly.
If the paticular year was below that was a negative anomaly.  Also prints
time it takes to complete the task.

Arguments: 
    none
Returns:
    none
"""
def graph_temp_anomaly():
    array=np.load("smaller_temp.npy")
    temps=[]
    startTime = datetime.now()
    for i in range(115):
        print("computing layer: ",i)
        sum_avg=0
        for j in range(85794):
            mean=array[i][j][4]
            sum_avg+=float(mean)
        global_avg=sum_avg/(85794)
        temps.append(global_avg)
    total=0
    count=0      
    for item in temps:
        total+=item
        count+=1
    total_global_avg=total/count
    anomaly=[]
    for l in temps:
        anomaly.append(l-total_global_avg)
   
    y=anomaly
    x=[i for i in range(1900,2015)]
    graph_temp_anomaly=pl.figure(3)
    #pl.figure(figsize=(15,7))
    pl.plot(x, y)
    pl.title('Time series of global temperature anomalie with respect to 1900-2014')
    pl.xlabel('Year')
    pl.ylabel('Temperature in deg Celsius')
    pl.show() 
    graph_temp_anomaly.savefig("graph_temp_anomaly.pdf") 
    pl.close() 
    print(datetime.now() - startTime)
  
#Task 5b
"""
Here we do the sameting as in part 5a but for only for the years
1951-1980.  The only thing we needed to change here was the range
for the for loop and the x axis.

Arguments: 
    none
Returns:
    none
"""
def graph_temp_anomaly_specific():
    array=np.load("smaller_temp.npy")
    temps=[]
    startTime = datetime.now()
    for i in range(51,81):
        print("computing layer: ",i)
        sum_avg=0
        for j in range(85794):
            mean=array[i][j][4]
            sum_avg+=float(mean)
        global_avg=sum_avg/(85794)
        temps.append(global_avg)
    total=0
    count=0      
    for item in temps:
        total+=item
        count+=1
    total_global_avg=total/count
    anomaly=[]
    for l in temps:
        anomaly.append(l-total_global_avg)
   
    y=anomaly
    x=[i for i in range(1951,1981)]
    graph_temp_anomaly_specific=pl.figure(4)
    #pl.figure(figsize=(15,7))
    pl.plot(x, y)
    pl.ylabel('Temperature in deg Celsius')
    pl.xlabel('Year')
    pl.title('Time series of global temperature anomalie with respect to 1951-1980')
    pl.show()  
    graph_temp_anomaly_specific.savefig("graph_temp_anomaly_specific.pdf") 
    pl.close() 
    print(datetime.now() - startTime)
"""
This is simply a helper function that calculates mean temps for
all files.  I needed this helper fxn to do task 6. 

Arguments: 
    array(the numpy array containting temps)
Returns:
    temp
"""           
def helper(array):
    temp=array[:,:,2:].mean(axis=2)
    return temp

#Task 6a
"""
This function also plots temp anomalies but using numpy
aray operations and no for loops.  

Arguments: 
    array_temp (the numpy array with temp data)
Returns:
    none
"""
def numpy_graph_temp_anomaly(array_temp):
    #array=np.load("smaller_temp.npy")
    startTime = datetime.now()
    annual_avg=helper(array_temp).mean(axis=1)
    global_avg=annual_avg.mean(axis=0)
     
    anomaly=annual_avg-global_avg
    y=anomaly
    x=[i for i in range(1900,2015)]
    numpy_graph_temp_anomaly=pl.figure(5)
    #pl.figure(figsize=(15,7))
    pl.plot(x, y)
    pl.ylabel('Temperature in deg Celsius')
    pl.xlabel('Year')
    pl.title('Time series of global temperature anomalie with respect to 1900-2014')
    pl.show() 
    numpy_graph_temp_anomaly.savefig("numpy_graph_temp_anomaly.pdf") 
    pl.close() 
    print(datetime.now() - startTime)
    
 #Task 6b   
"""
This function counts number of rows in each file.  
Since number of rows is given to us this is not neccesary but I wanted to show 
how it would be done if we diddn't know

Arguments: 
    array_temp  (the numpy array with temp data)
Returns:
    none
"""
def numpy_graph_precip_anomaly(array_temp):   
    startTime = datetime.now()
    annual_avg=helper(array_temp).mean(axis=1)
    global_avg=annual_avg.mean(axis=0)
   
    anomaly=annual_avg-global_avg
    y=anomaly[51:81]
    x=[i for i in range(1951,1981)]
    
    numpy_graph_temp_anomaly_specific=pl.figure(6)
    #pl.figure(figsize=(15,7))
    pl.plot(x, y)
    pl.ylabel('Temperature in deg Celsius')
    pl.xlabel('Year')
    pl.title('Time series of global temperature anomalie with respect to 1951-1980')
    pl.show() 
    numpy_graph_temp_anomaly_specific.savefig("numpy_graph_temp_anomaly_specific.pdf") 
    pl.close() 
    print(datetime.now() - startTime)
    
#Task 7
"""
This function loads precip array and creates bar graph of
change in precipitation from year to year.  This is showing the 
rate of change in preciptation over the period 1900-2014.

Arguments: 
    none
Returns:
    none
"""
def change_precip():
    array=np.load("smaller_precip.npy")
    precip=[]
    for i in range(115):
        print("computing layer: ",i)
        sum_avg=0
        for j in range(85794):
            mean=array[i][j][4]
            sum_avg+=float(mean)
        global_avg=sum_avg/(85794)
        precip.append(global_avg)
    x=np.arange(1900,2014)
    y=[precip[j+1]-precip[j] for j in range(114)]
    
    change_precip=pl.figure(7)
    pl.bar(x,y)
    #pl.figure(figsize=(15,7))
    pl.title('Rate of change in global annual mean precipitation between 1900 and 2014')
    pl.show()
    change_precip.savefig("change_precip.pdf") 
    pl.close() 
    
#Task 8
"""
This function graphs a historam of min temps over all stations for a paticular
year and number of bins.

Arguments: 
    year,bin_num (# of bins you want in the graph)
Returns:
    none
"""
def graph_min_temps(year,bin_num):
    array=np.load("smaller_temp.npy")
    layer=year-1900
    min_temp=[]
    for i in range(85794):
        val=str(array[layer][i][2])
        val=val.strip('b\'')
        numval=float(val)
        min_temp.append(numval)
        
    graph_min_temps=pl.figure(8)
    pl.hist(min_temp,bin_num,histtype='stepfilled')
    pl.title('Histogram of min temperatures as recorded at all locations during year '+ str(year))
    pl.show()
    graph_min_temps.savefig("graph_min_temps.pdf") 
    pl.close()             
    
#Task 9a
"""
Here we graph a heat map using a scatter plot.  We take the mean temp readings 
across the globe for a paticular year and graph those with a log bar gradient.

Arguments: 
    year
Returns:
    none
"""
def graph_temp_map(year):
    array=np.load("smaller_temp.npy")
    layer=year-1900
    lats=[]
    lons=[]
    temps=[]
    for j in range(85794):
        tempval=str(array[layer][j][4])
        tempval=tempval.strip('b\'')
        mean_temp=float(tempval)
        temps.append(mean_temp)
        
        val=str(array[layer][j][0])
        val=val.strip('b\'')
        numval=float(val)
        lats.append(numval)
        
        valt=str(array[layer][j][1])
        valt=valt.strip('b\'')
        numvalt=float(valt)
        lons.append(numvalt)
       
    #graph_temp_map=pl.figure(9)
    pl.scatter(lats,lons,s=0.3,c=temps,norm=colors.LogNorm())
    pl.title('Mean annual temperature in deg Celsius, '+ str(year))
    pl.xlabel('latitude')
    pl.ylabel('longitude')
    pl.colorbar()
    pl.show()
    #graph_temp_map.savefig("graph_temp_map.pdf") 
    #pl.close()
    
#Task 9b
"""
Now for a given year we do the same thing but for precipitation.  The darker
the region, the smaller the amount of precipitation.  Again we use a log bar
as the gradient. 

Arguments: 
    none
Returns:
    none
"""
def graph_precip_map(year):
    array=np.load("smaller_precip.npy")
    layer=year-1900
    lats=[]
    lons=[]
    precip=[]
    for j in range(85794):
        mean_precip=array[layer][j][4]
        precipval=str(array[layer][j][4])
        precipval=precipval.strip('b\'')
        mean_precip=float(precipval)
        precip.append(mean_precip)
        
        val=str(array[layer][j][0])
        val=val.strip('b\'')
        numval=float(val)
        lats.append(numval)
        
        valt=str(array[layer][j][1])
        valt=valt.strip('b\'')
        numvalt=float(valt)
        lons.append(numvalt)
    
    #graph_precip_map=pl.figure(10)
    pl.scatter(lats,lons,s=0.3,c=precip,norm=colors.LogNorm())
    pl.colorbar()
    pl.title('Total annual precipitation in millimiters, '+ str(year))
    pl.xlabel('latitude')
    pl.ylabel('longitude')
    pl.show()
    #graph_precip_map.savefig("graph_precip_map.pdf") 
    #pl.close()
    
#Task 10 
"""
This function is very similar to 9a but makes a heat map for a given 
time period.  Put in a starting and ending year and this will use a scatter
plot to graph the heat map over those years.

Arguments: 
    start,end (these are the years of the range)
Returns:
    none
"""       
def graph_temp_map_over_period(start,end):
    array=np.load("smaller_temp.npy")
    layer_start=start-1900
    layer_end=end-1899   
    lats=[]
    lons=[]
    temps=[]
    for i in range(layer_start,layer_end):
        for j in range(85794):
            tempval=str(array[i][j][4])
            tempval=tempval.strip('b\'')
            mean_temp=float(tempval)
            temps.append(mean_temp)
            
            val=str(array[i][j][0])
            val=val.strip('b\'')
            numval=float(val)
            lats.append(numval)
            
            valt=str(array[i][j][1])
            valt=valt.strip('b\'')
            numvalt=float(valt)
            lons.append(numvalt)
       
    #graph_temp_map_over_period=pl.figure(11)
    pl.scatter(lats,lons,s=0.3,c=temps,norm=colors.LogNorm())
    pl.title('Global distribution of the ensemble mean annual mean surface air temperature averaged over the period '+ str(start)+'-'+ str(end))
    pl.xlabel('latitude')
    pl.ylabel('longitude')
    pl.colorbar()
    pl.show()
    #graph_temp_map_over_period.savefig("graph_temp_map_over_period.pdf") 
    #pl.close()    

"""
This function takes the idea from task 10 but applies it to precipitation.
For any given start and end year (a period of time) this function graphs with a
scatter plot, the avg precipitation from each station across the globe over that
time period.

Arguments: 
    start,end (these are the years of the range)
Returns:
    none
"""  
def extra_credit(start,end):     
    array=np.load("smaller_precip.npy")
    layer_start=start-1900
    layer_end=end-1899   
    lats=[]
    lons=[]
    precip=[]
    for i in range(layer_start,layer_end):
        for j in range(85794):
            precipval=str(array[i][j][4])
            precipval=precipval.strip('b\'')
            mean_precip=float(precipval)
            precip.append(mean_precip)
            
            val=str(array[i][j][0])
            val=val.strip('b\'')
            numval=float(val)
            lats.append(numval)
            
            valt=str(array[i][j][1])
            valt=valt.strip('b\'')
            numvalt=float(valt)
            lons.append(numvalt)
       
    #extra_credit=pl.figure(12)
    pl.scatter(lats,lons,s=0.3,c=precip,norm=colors.LogNorm())
    pl.title('Global distribution of the ensemble mean annual mean precipitation averaged over the period '+ str(start)+'-'+ str(end))
    pl.xlabel('latitude')
    pl.ylabel('longitude')
    pl.colorbar()
    pl.show()
    #extra_credit.savefig("extra_credit.pdf") 
    #pl.close()
    
if __name__ == "__main__":
    
    #array_temp=np.load("smaller_temp.npy")

    #read_files()  #Task 1b+1c
    
    #graph_mean_temp() #Task 3
    
    #graph_total_precip() #Task 4
    
    #graph_temp_anomaly() #Task 5a
    
    #graph_temp_anomaly_specific() #Task 5b
    
    #numpy_graph_temp_anomaly(array_temp# #Task 6a
    
    #numpy_graph_precip_anomaly(array_temp) #Task 6b
                               
    #change_precip() #Task 7
    
    #graph_min_temps(2013,15) #Task 8
    
    graph_temp_map(2014) #Task 9a
    
    #graph_precip_map(1905) #Task 9b
    
    #graph_temp_map_over_period(1920,1939) #Task 10
    
    #extra_credit(1969,1998) #Extra Credit    