from ast import arg
from lzma import MODE_FAST
import re
from django.shortcuts import render , HttpResponse
from home.forms import Moviedata
import requests



import pandas as pd
import numpy as np

# Create your views here.
def index(request):
    return HttpResponse("this is home app no url path woooh")

def about(request):
    return HttpResponse("this is about page")

def services(request):
    return HttpResponse("this is services page")


def fetch_poster(movieid):
    response =requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b78a4c5a65cfebf5db59868a03e1a2db&language=en-US'.format(movieid))
    data =response.json()
    return  "https://image.tmdb.org/t/p/w200/" + data['poster_path']
def homepage(request):
    intial_data={
        'year':1916
    }
    if request.method=='POST':
        #data = Moviedata(request.POST)
        # if data.is_valid():
            # movie = data.cleaned_data['movie']
            # year = data.cleaned_data['year']
        movie=request.POST.get('movie')
        year=int(request.POST.get('year'))
        moviesdf =pd.read_csv('static\Final_MRS_DataSet.csv')
        moviesdf = moviesdf.drop('Unnamed: 0',axis=1)
        movie =movie.lower()
        moviesdf['title']=moviesdf['title'].str.lower()
        if(movie in moviesdf['title'].values):

            similarities = pd.read_csv('static\Similarites.csv')
            similarities =similarities.drop('Unnamed: 0',axis=1)

        
            
            # recommendation being done
            movie_index = moviesdf[moviesdf['title']==movie].index[0]
            dist = similarities.iloc[movie_index]
            recommendations =sorted(list(enumerate(dist)),reverse=True , key=lambda x:x[1])
            li =[]
            movie_posters=[]
        
            for j in range(1,len(moviesdf)):
                if(moviesdf.iloc[recommendations[j][0]]['release_data']>=year): # check the year if error
                    li.append(moviesdf.iloc[recommendations[j][0]])
                    
            
            li_rec=[]
            for i in li[0:5]:
                li_rec.append(i.title)
                #fetching poster from the movie
                movie_posters.append(fetch_poster(i.id))
            movies_dic = dict(zip(li_rec, movie_posters))


            args ={'Recommendations':movie_posters}
                
            
            return render(request ,'home1.html',args)    
        else:
            errorMessage="The movie you asked has not been found 😢😢 try another one!!"
            return render(request ,'base1.html',{'error':errorMessage})    






    else:
        # data = Moviedata(initial=intial_data)
    
        return render(request ,'base1.html')    



