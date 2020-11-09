#!/usr/bin/env python
# coding: utf-8

import requests
import csv
import numpy as np
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import requests       # use requests pacakage to download webpages
import pandas as pd   # use pandas to store table as dataframe
from lxml import html # use lxml to parse html format
from lxml import etree 
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
from collections import defaultdict
import gmplot
import json

def creat_education_df():
    pittsZips = "15122, 15201, 15202, 15203, 15204, 15205, 15206, 15207, 15208, 15209, 15210, 15211, 15212, 15213, 15214, 15215, 15216, 15217, 15218, 15219, 15220, 15221, 15222, 15223, 15224, 15225, 15226, 15227, 15228, 15229, 15232, 15233, 15234, 15235, 15236, 15237, 15238, 15239, 15241, 15243, 15260, 15272, 15275, 15276, 15290, 15295, 15230, 15231, 15240, 15242, 15244, 15253, 15264, 15274, 15250, 15251, 15252, 15254, 15255, 15257, 15258, 15259, 15261, 15262, 15265, 15267, 15268, 15270, 15277, 15278, 15279, 15281, 15282, 15283, 15286, 15289"
    apiKey = "f2d076b71467894668dddaf60b33842250fdd35b"
    baseAPI = "https://api.census.gov/data/2017/acs/acs5?key=%s&get=B15003_022E&for=zip%%20code%%20tabulation%%20area:%s" 
    calledAPI = baseAPI % (apiKey, pittsZips)
    response = requests.get(calledAPI)
    formattedResponse = json.loads(response.text)[1:]
    formattedResponse = [item[::-1] for item in formattedResponse]
    pittsZipPopulations = pd.DataFrame(columns=['Zip Code', 'bachelor'], data=formattedResponse)
    
    baseAPI = "https://api.census.gov/data/2017/acs/acs5?key=%s&get=B15003_002E&for=zip%%20code%%20tabulation%%20area:%s" 
    calledAPI = baseAPI % (apiKey, pittsZips)
    response = requests.get(calledAPI)
    formattedResponse = json.loads(response.text)[1:]
    formattedResponse = [item[::-1] for item in formattedResponse]
    pittsZipPopulations2 = pd.DataFrame(columns=['Zip Code', 'high school'], data=formattedResponse)
    pittsZipPopulations = pittsZipPopulations.merge(pittsZipPopulations2, on='Zip Code')
    
    baseAPI = "https://api.census.gov/data/2017/acs/acs5?key=%s&get=B15003_017E&for=zip%%20code%%20tabulation%%20area:%s" 
    calledAPI = baseAPI % (apiKey, pittsZips)
    response = requests.get(calledAPI)
    formattedResponse = json.loads(response.text)[1:]
    formattedResponse = [item[::-1] for item in formattedResponse]
    pittsZipPopulations2 = pd.DataFrame(columns=['Zip Code', 'No schooling completed'], data=formattedResponse)


    pittsZipPopulations = pittsZipPopulations.merge(pittsZipPopulations2, on='Zip Code')
    baseAPI = "https://api.census.gov/data/2017/acs/acs5?key=%s&get=B15003_023E&for=zip%%20code%%20tabulation%%20area:%s" 
    calledAPI = baseAPI % (apiKey, pittsZips)
    response = requests.get(calledAPI)
    formattedResponse = json.loads(response.text)[1:]
    formattedResponse = [item[::-1] for item in formattedResponse]
    pittsZipPopulations2 = pd.DataFrame(columns=['Zip Code', 'Master'], data=formattedResponse)
    pittsZipPopulations = pittsZipPopulations.merge(pittsZipPopulations2, on='Zip Code')
    
    return pittsZipPopulations

def creat_hospital_df():
    final=''
    for i in range(1,4):
        html='https://www.healthgrades.com/hospital-directory/pa-pennsylvania/pittsburgh'+('' if i==1 else '_'+str(i))+'?category=facility'
        page = requests.get(html)
        text=str(page.content)
        start=text.find('"results":[{"id":')
        end=text.find('],"activeSort":')
        final+=text[start+11:end]+','

    finalfinal='['+final+']'

    finaldata=eval(finalfinal)

    allphones = []
    allnames = []
    allfiveStarRatingsCount = []
    allurls = []
    allstreets= []
    allcity= []
    allstate= []
    allzip= []
    allpatientSat=[]

    for data in finaldata:
        allphones.append(data['phone'])
        allnames.append(data['name'])
        allfiveStarRatingsCount.append(data['fiveStarRatingsCount'])
        allurls.append(data['url'])
        allstreets.append(data['address']['street'])
        allcity.append(data['address']['city'])
        allstate.append(data['address']['state'])
        allzip.append(data['address']['zip'])

    import pandas as pd # use pandas to store table as dataframe
    #df = pd.DataFrame(allnames,allphones,allurls,allfiveStarRatingsCount,allstreets,allcity,allstate,allzip)
    df = pd.DataFrame()
    df['Name']=allnames
    df['Phone']=allphones
    df['URLs']=allurls
    df['Street']=allstreets
    df['City']=allcity
    df['State']=allstate
    df['Zip Code']=allzip
    df['Five Star Ratings Count']=allfiveStarRatingsCount
    df['Phone']=allphones
    df['URLs']=allurls
    df.index = df.index + 1
    return df

def creat_restaurant_df():
    df_table = pd.DataFrame(columns=['Name', 'description', 'Links', 'Score', 'Address','Zip Code','Votes','Cost', 'Hours' ])
    index = 0
    for i in range(1,296):

        url = "https://www.zomato.com/pittsburgh/restaurants?page={}".format(i)
        headers = {'User-Agent':'Mozilla/5.0(Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14'} 
        page = requests.get(url, headers = headers) 
        soup = BeautifulSoup(page.text, "html.parser")

        tc_table_list = soup.findAll('div',
                              { "class" : "content" } )
        tc = soup.find_all('div', class_=('card', 'search-snippet-card', 'search-card'))


        for c in tc_table_list:
            lineList = []
            for r in c.findAll('a',{ "data-result-type" : "ResCard_Name" } ):
                lineList.append(r.text.replace('\n','').strip())
                lineList.append(r.get('title'))
                lineList.append(r.get('href'))

            for r in c.findAll('div',{ "data-content" : ["Excellent", "Very Good", "Average"] } ):
                lineList.append(float(r.text.replace('\n','')))

            for r in c.findAll('div',{ "style" : [" max-width:370px; "]}):
                lineList.append(r.text.replace('\n',''))
                lineList.append(r.text.replace('\n','')[-5:])


            for r in c.findAll('span',{ "class" : re.compile('rating-votes-div-')}):
                lineList.append(r.text.replace('\n',''))


            for r in c.find_all('span',{ "itemprop" : ["priceRange"]}):
                s = '';
                for t in r.children:
                    s= s+t.text.replace('\n','')
                lineList.append(s)

            for r in c.findAll('div',{ "class" : ["res-timing clearfix"]} ):
                lineList.append(r.get('title'))


            if(len(lineList) == 9):
                df_table.loc[index] = lineList
                index = index + 1

                # classify info by Zip Code and calculate descriptive statistics      
    df_group_by_zipCode = df_table.groupby('Zip Code')
    zip_table = pd.DataFrame(columns=['Zip Code','meanScore', 'restaurantName', 'score','location'])
    zip_index = 0
    d = defaultdict(list)

    for name, group in df_group_by_zipCode:
        meanScore = round(group['Score'].mean(),1)
        restaurantName = group['Name'].tolist()
        restaurantScore = group['Score'].tolist()
        restaurantAddress = group['Address'].tolist()
        if(len(restaurantName) >= 5 and len(restaurantScore)>= 5 and len(restaurantAddress) >= 5):
            for i in range(5):
                if(name.isdigit()):
                    zip_table.loc[zip_index] = [name, meanScore,restaurantName[i],restaurantScore[i],restaurantAddress[i]]
                    d[name].append(restaurantAddress[i])
                    zip_index = zip_index + 1
    return zip_table

PittsHospitalData = creat_hospital_df()
PittsEducationData = creat_education_df()
PittsRestaurantData = creat_restaurant_df()

# enter a Zip Code and draw first top five restaurant's location in that area on Google map

def getMap():
    restaurantAddressList =[]
    hospitalAddressList = []
    df_restaurant = PittsRestaurantData.groupby('Zip Code')
    PittsHospitalData['Address']= PittsHospitalData['Street']+','+PittsHospitalData['City']+','+PittsHospitalData['State']
    df_hospital = PittsHospitalData.groupby('Zip Code')
    for name, group in df_restaurant:
        restaurantAddress = group['location'].tolist()
        restaurantAddressList.append(restaurantAddress[0])
    
    for name, group in df_hospital:
        hospitalAddress = group['Address'].tolist()
        hospitalAddressList.append(hospitalAddress[0])
        
    
    re_latitude_list=[]
    re_longitude_list=[]
    hos_latitude_list=[]
    hos_longitude_list=[]

    # tranform address to latitude and longitude
    for i in restaurantAddressList:
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+i+'&key=AIzaSyADdiD2BWb-Woao41ATU13lmV-KFoxkVyo')
        resp_json_payload = response.json()
        latLng = resp_json_payload['results'][0]['geometry']['location']
        re_latitude_list.append(latLng['lat'])
        re_longitude_list.append(latLng['lng'])
        
    for i in hospitalAddressList:
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+i+'&key=AIzaSyADdiD2BWb-Woao41ATU13lmV-KFoxkVyo')
        resp_json_payload = response.json()
        latLng = resp_json_payload['results'][0]['geometry']['location']
        hos_latitude_list.append(latLng['lat'])
        hos_longitude_list.append(latLng['lng'])

    # mark location on Google map
    meanLat = np.mean(re_latitude_list)
    meanLng = np.mean(re_longitude_list)
    gmap = gmplot.GoogleMapPlotter(meanLat, meanLng, 15)

    gmap.scatter( re_latitude_list, re_longitude_list, 'k', 
                                  size = 30, marker = False )
    gmap.heatmap(hos_latitude_list, hos_longitude_list)
    gmap.apikey = "AIzaSyADdiD2BWb-Woao41ATU13lmV-KFoxkVyo"
    gmap.draw( "map.html" )
    
def createDF():
    #global df
    html = urlopen("https://data.wprdc.org/dataset/uniform-crime-reporting-data")
    bsObj = BeautifulSoup(html,features="lxml")

    #find the link for the data that we want on the site
    #specifically pull the one with "https" to get the correct link
    #look within the div class = btn-goup (found inspecting the webpage)
    for link in bsObj.find("div", {"class":"btn-group"}).findAll("a", href=re.compile("https")):
        if 'href' in link.attrs:
       #     print(link.attrs['href'])
            h=link.attrs['href']
    response = requests.get(h)


    #write the raw data to a file
    with open('crime_data_pitt.xlsx', 'wb') as output:
        output.write(response.content)

    df = pd.read_csv('crime_data_pitt.xlsx')

    """for date in range(l):
        year = df.iloc[date,4]
        y = year[0:4]
        if(int(y)<2018):
            df.drop(df.index[date], inplace=True)
     """
    #get only the dates we care about
    df=df.sort_values(by=['INCIDENTTIME'], ascending = False)
    #manually input the indices for times sake
    #iterating through the entire data set takes a long time
    desired_indices = [i for i in range(0,70372)]
    df= df.iloc[desired_indices]
    nondesired=[]
    for index in range(0,70372):
        temp = df.iloc[index,4]
        leng = len(str(temp))
        zip_code=temp[leng-5:leng]
        #match zipcode of format 15219
        zc = re.compile(r'\d\d\d\d\d')
        zip = zc.search(zip_code)
        #if there was not a zip code in the address add index to list
        if(zip==None):
            nondesired.append(index)
        else:
            df.iat[index,4]=zip_code
            
    #take the set difference of the entire dataset and the indices lacking a zipcode        
    desired = set(range(df.shape[0])) - set(nondesired)
    df= df.take(list(desired))
    #drop unwanted columns
    df=df.drop(columns='CCR')
    df=df.drop('CLEAREDFLAG',axis=1)
    df=df.drop('OFFENSES', axis=1)
    df=df.drop('INCIDENTTRACT', axis=1)
    df=df.drop('PK', axis=1)
    df=df.drop('COUNCIL_DISTRICT', axis=1)
    df=df.drop('X', axis=1)
    df=df.drop('Y', axis=1)
    df=df.drop('PUBLIC_WORKS_DIVISION',axis=1)
    #sort remaining values
    df=df.sort_values(by=['HIERARCHY', 'INCIDENTHIERARCHYDESC', 'INCIDENTLOCATION'])
    df=df.sort_values(by=['INCIDENTNEIGHBORHOOD'])
    #if you want to write the data to an excel sheet
    
    #write data to excel file
    """
    writer = pd.ExcelWriter("crime_data_pitt.xlsx", engine = 'xlsxwriter')
    df.to_excel(writer, sheet_name = 'Sheet2')

    workbook=writer.book
    worksheet=writer.sheets['Sheet2']
    worksheet.set_column(1,7,20)

    writer.save()"""
    return df

def printNeighborhoods(df):
    neig=df['INCIDENTNEIGHBORHOOD'].unique()
    neigh = dict(zip(range(1,len(neig)-1),neig))
    for key in neigh:
         print(key, ".", neigh[key])
    while True:
        try:
             val = int(input("Please pick a Neighborhood to view the data: "))
        except ValueError:
            print("Please enter a number")
            continue
        else:
            break

    print("The neighborhood chosen is: ", neigh[val])
    return neigh[val]

def getZips(neighdf):
    zips = neighdf['INCIDENTLOCATION'].unique()
    return zips
#create dictionary of crime hierarchy numbers and corresponding crime type
crimePairings = {1:'murders', 3:'robberies', 4:'aggregious assaults', 5:'burglaries', 6:'thefts', 7:'vehicle thefts'}

def summaryData(hood,df):
    print("Showing the data for: ", hood)
    print("--------------------------------------")
  
    #create a dataframe for the nieghborhood
    neigh_data = df[df['INCIDENTNEIGHBORHOOD']== hood]
    print("The zip codes included in this neighborhood are:")
    #get an array of zipcodes
    zipc = getZips(neigh_data)
    print(', '.join(zipc))
    
    printEducation(zipc)
    printRestaurant(zipc)
    printHospital(zipc)
    
    #find the earliest date of crime in the neighborhood for our data
    min_date = neigh_data['INCIDENTTIME'].min()
    print("-----------------------------------------------")
    print("The total number of crimes that have taken place since ",min_date[:10], "is", neigh_data['INCIDENTLOCATION'].count())
    print()
    print("Breakdown of serious crimes reported since",min_date[:10])
    for key in crimePairings:
        getCount(neigh_data,key)
    graphCrimes(neigh_data, df)
    

    print()

#get the count of rows for the specified
#Hierarchy number 
def getCount(df,crimeHierNum):
    seriesObj = df.apply(lambda x:True if x['HIERARCHY'] == crimeHierNum else False, axis=1)
    numOfRows=len(seriesObj[seriesObj == True].index)
    print('There were {0} {1}.'.format(numOfRows,crimePairings.get(crimeHierNum)))

#graphs the number of all crimes reported per month-year for specific neighborhood
def graphCrimes(neigh_df, df):
    #get pittsburgh date/year for each crime
    #removed from showing because lacking population data to normalize
    #frequency of crimes to be comparable between city and neighborhood
    """
    for index in range(0,len(df['INCIDENTTIME'])):
        temp = df.iloc[index,1]
        date=temp[0:7]
        df.iat[index,1]=date
    dateArray = np.array(df.iloc[:,1])
    unique, counts = np.unique(dateArray, return_counts=True)"""
    
    #get neighborhood date/year for crime
    for index in range(0,len(neigh_df['INCIDENTTIME'])):
        temp = neigh_df.iloc[index,1]
        date=temp[0:7]
        neigh_df.iat[index,1]=date
        
    #turn column in to np array
    neigh_dateArray = np.array(neigh_df.iloc[:,1])
    #find the number of crimes committed per day
    neigh_unique, neigh_counts = np.unique(neigh_dateArray, return_counts=True)
    #graph
    fig=plt.figure()
   # plt.plot(unique,counts, color = 'orange')
    plt.plot(neigh_unique, neigh_counts, color='g')
    plt.xticks(rotation=90)
    plt.title("Number Of Crimes Committed Over Time By Month-Year")
    plt.xlabel('Month-Year')
    plt.ylabel('Number of Crimes')
    plt.show()


#prints welcome menu
def welcomeMenu():
    val = int(input("Welcome to UrbAux!\n"          "-------------------\n"          "Please pick a city to explore:\n"          "1. Pittsburgh\n"          "2. Quit\n"))
    if(val<1 | val>2):
        print("Try Again")
        return welcomeMenu()
    return val


# In[22]:


#prints menu to ask if user would like to pick another neighborood
def pickAgainMenu():
    val = int(input("Would you like to explore another neighborhood?\n"                     "Please choose a number:\n"                     "1. Yes\n"                     "2. No\n"))
    if(val!=1):
        if(val!=2):
            print("Try Again")
            return pickAgainMenu()
    return val

def printEducation(zipc):
    neigh_edu = pd.DataFrame(columns = PittsEducationData.columns)
    
    for zipcode in zipc:
        edu = PittsEducationData[PittsEducationData["Zip Code"] == str(zipcode)]
        neigh_edu = pd.concat([neigh_edu,edu], ignore_index=True)
        neigh_edu = neigh_edu.astype({'bachelor': 'int32','high school': 'int32','No schooling completed': 'int32','Master': 'int32'})
    print("-----------------------------------------------")
    print("Education Level: Number of people having ")
    m = neigh_edu['Master'].sum(axis = 0, skipna = True)
    b = neigh_edu['bachelor'].sum(axis = 0, skipna = True)
    h = neigh_edu['high school'].sum(axis = 0, skipna = True)
    n = neigh_edu['No schooling completed'].sum(axis = 0, skipna = True)
    
    print("    Master degree: " + str(m))
    print("    Bachelor degree: " + str(b))
    print("    High School Diploma: "+ str(h))
    print("    No schooling completed: " +str(n))
        
    nums = [m,b,h,n]

    
    fig=plt.figure()
    plt.bar(['Master','Bachelor','High School','No Schooling Completed'], nums, color='g')
    plt.xticks(rotation=90)
    plt.title("Education Attainment Of People Over 25 years old ")
    plt.xlabel('Education Level')
    plt.ylabel('Number of People')
    plt.show()

def printRestaurant(zipc):
    neigh_res = pd.DataFrame(columns = PittsRestaurantData.columns)
    
    for zipcode in zipc:
        res = PittsRestaurantData[PittsRestaurantData["Zip Code"] == str(zipcode)]
        neigh_res = pd.concat([neigh_res,res], ignore_index=True)
    
    top5_res = pd.DataFrame(columns = ["Zip Code","restaurantName","score"])
    for top5 in neigh_res["score"].sort_values(ascending = False).head(5).unique():
        
        top5_res = pd.concat([top5_res,neigh_res[neigh_res["score"] == top5][["Zip Code","restaurantName","score"]]], ignore_index=True)
    
    top5_res["Restaurant Name"] = top5_res["restaurantName"] 
    del top5_res["restaurantName"] 
    print("-----------------------------------------------")
    print("Top restaurants in the neighborhood: ")
    print(top5_res[["Zip Code","Restaurant Name","score"]].to_string(index=False))

def printHospital(zipc):
    neigh_hos = pd.DataFrame(columns = PittsHospitalData.columns)

    for zipcode in zipc:
        hos = PittsHospitalData[PittsHospitalData["Zip Code"] == str(zipcode)]
        neigh_hos = pd.concat([neigh_hos,hos], ignore_index=True)
        
    top5_hos = pd.DataFrame(columns = ["Zip Code","Phone","Five Star Ratings Count","Name"])
   
    for top5 in neigh_hos["Five Star Ratings Count"].sort_values(ascending = False).head(3).unique():
        top5_hos = pd.concat([top5_hos,neigh_hos[neigh_hos["Five Star Ratings Count"] == top5][["Zip Code","Phone","Five Star Ratings Count","Name"]]], ignore_index=True)
      
    top5_hos["Ratings"] = top5_hos["Five Star Ratings Count"] 
    del top5_hos["Five Star Ratings Count"] 
    print("-----------------------------------------------")
    print("Top Hospitals in the neighborhood: ")
    print(top5_hos[["Zip Code","Name","Phone","Ratings"]].to_string(index=False))

def main():
    #creating dataframes
    PittsCrimeData = createDF()
    #initializing variable to print the neighborhoods the first time
    cont =1
    #get user input from the welcome menu
    #reject if user does not input 1 or 2
    try:
        choice = welcomeMenu()
    except ValueError:
        print("Bad input")
        sys.exit()
    #if user chose Pittsburgh
    if(choice==1):
        #stay in loop as long as the user chooses to continue
        while(cont == 1):
                #get the user's choice of neighborhood to explore
                #create dataframe
                pick=printNeighborhoods(PittsCrimeData)
                print(pick)
                
                #return the crime summary data for the neighborhood
                summaryData(pick,PittsCrimeData)
                try:
                    cont = pickAgainMenu() #if the user wants to pick another neighborhood cont =1
                except ValueError:
                    print("Not a valid choice")
                    sys.exit()
        if(cont==2):
            print("Good bye")
            sys.exit()
    print("Bad input. Good bye")
    sys.exit()

if __name__=="__main__":
    main()

# write data to csv file
#zip_table.to_csv("zomato_five_top_restaurant.csv",mode='w')
#df_table.to_csv("zomato_data.csv", mode='w')
#zip_table.to_csv("zomato_data_zipCode.csv", mode='w')





