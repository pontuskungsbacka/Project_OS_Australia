# Project_OS_Australia

## Innehåll
I project_OS_Australia så använder vi oss av ett OS dataset från kaggle och och presenterar intressant data via en dash funktion.

## Repository layout
```
Project_OS_Australia/
├─ data/
│  ├─ athlete_events.csv
│  ├─ athlete_events_fixed_age.csv
│  ├─ australia_missing_AGE_FIX.csv
│  └─ noc_regions.csv
├─ assets /
│  ├─ style.css                 
│  ├─ favicon.ico            
│  └─ img
│      ├─ equ.svg 
│      ├─ github-mark.svg                 
│      ├─ hoc.svg     
│      ├─ linkedin-logo.svg 
│      ├─ olympic-logo.svg                 
│      ├─ row.svg     
│      ├─ swm.svg             
│      └─ team-AUS-logo.svg
├─ notebooks /
│  ├─ 00_explore_data.ipynb
│  ├─ Adam.ipynb               
│  ├─ Julia.ipynb          
│  ├─ Laura.ipynb
│  ├─ Laura_clean.ipynb                 
│  ├─ Pontus.ipynb           
│  ├─ cleaner.py
│  └─ swimming.ipynb
├─ pages /
│  ├─ about.py                
│  ├─ age.py          
│  ├─ equestrian.py
│  ├─ gender.py
│  ├─ hockey.py              
│  ├─ medals.py        
│  ├─ participation.py
│  ├─ rowing.py
│  └─ swimming.py
├─  .gitignore      
├─  README.md   
├─  app.py    
├─  load_data.py     
└─  requirements.txt
```

## Undersökning av data
I mappen /notebooks finns jupyter filer från alla deltagande där vi undersökt datan och som legat till grund för intressant statistik som sedan presenteras i dash.


## Användandet av applikationen
Ta ner och klona projektet från github: https://github.com/pontuskungsbacka/Project_OS_Australia
Installera korrekt moduler för att kunna köra applikationen: pip install -r requirements.txt
Starta Dash-applikation genom att skriva python app.py i terminalen
Öppna sedan i webbläsaren på adress: http://127.0.0.1:8050/

## Hur applikation fungerar
I load_data.py så tar vi in csv filer, mergar ihop noc_regions med OS-dataset för att kunna specifiera mer exakt vilken region de olika deltagande har. Vi anonymiserar sedan alla deltagarnamn.
Det finns även en funktion som tar bort dubletter, detta används då vi t ex ej vill visa 16 individuella guld i landhockey utan 1 gemensamt guld.
I mappen /pages så ligger de olika sidorna i vår dash-applikation, där plockar vi alla in en dataframe från load_data.py för att plotta våra grafer. I filen app.py så hämtar vi och läser in sidorna från pages och kör applikation.

## Skapad av:
### Pontus Johansson
### Julia Sälde
### Laura-Mirella Lomakin
### Adam Hedlund


