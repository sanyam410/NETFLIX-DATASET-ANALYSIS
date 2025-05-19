import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
df=pd.read_csv(r"C:\Users\saura\Downloads\netflix_titles.csv")
print(df.columns)
print(df.shape)
print(df.isnull().sum())
df["director"].replace(np.nan,"No data",inplace=True)
df["cast"].replace(np.nan,"No data",inplace=True)
df["country"].replace(np.nan,"No data",inplace=True)
df.dropna(inplace=True)
print(df.isnull().sum(),df.shape)
df["country"]=df["country"].str.split().str[0]
df['country'].replace('United','USA',inplace=True)
df['country'].replace('South','Korea',inplace=True)
df['country'].replace('No','Norway',inplace=True)
# after some data cleaning we see that no of column decrease from 8807 to 8790 total 17 rows has been dropped
df["date_added"]=pd.to_datetime(df['date_added'])
# detecting a director with most project
valid_dir=df[df['director']!='No data']
val=valid_dir['director'].value_counts()
name=val.idxmax()
count=val.max()

# calculating content with their genre
res=df['rating'].value_counts()
print(res)
tit=res.idxmax()
count1=res.max()

#creating a new genere table from the existing one
df['genere']=df['listed_in'].str.split(',').str[0]
x=df['genere'].value_counts()
y=x.idxmax()
z=x.max()

# displaying the insights 
fig,(ax1,ax2,ax3)=plt.subplots(3,1,figsize=(12,3))
box_prop=dict(boxstyle='round,pad=0.5',
              facecolor='#F1F8E9',
              edgecolor='#558B2F')
text_style=dict(fontsize=14,fontweight='bold',color='#33691E')
ax1.axis('off')
ax1.text(0.5,0.5,f"{name} is the director involved with most project {count}",ha='center',va='center',bbox=box_prop,**text_style)
ax2.axis('off')
ax2.text(0.5,0.5,f'{tit} is the rating with most content {count1} available on netflix',ha='center',va="center",bbox=box_prop,**text_style)
ax3.axis('off')
ax3.text(0.5,0.5,f'{y} is the genere with the most content {z} available on netflix',ha='center',va="center",bbox=box_prop,**text_style)
plt.tight_layout()
plt.show()
#comparing number of tv shows and movies 
plt.figure(figsize=(6,4))
sns.countplot(x='type',data=df,hue='type',palette='Set2',legend=False)
plt.title('TV Shows VS Movies')
plt.xlabel('Type')
plt.ylabel('Count')
plt.show()
#Displaying country with most available content
df["country"].value_counts().head(10).plot(kind='bar',color='purple')
plt.xlabel('Country')
plt.ylabel('Number of titles')
plt.title('Top 10 countries with most netflix content')
plt.xticks(rotation=45)
plt.show()
# number of releases on netlix over the years
df['year_added']=df['date_added'].dt.year
plt.figure(figsize=(12,6))
df['year_added'].value_counts().sort_index().plot(kind='line', marker='o', color='red')
plt.title("Number of Netflix Releases Per Year")
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.grid()
plt.show()
# content age-group contribution by country
age_rating={ 
    'TV-PG': 'Older Kids',
    'TV-MA': 'Adults',
    'TV-Y7-FV': 'Older Kids',
    'TV-Y7': 'Older Kids',
    'TV-14': 'Teens',
    'R': 'Adults',
    'TV-Y': 'Kids',
    'NR': 'Adults',
    'PG-13': 'Teens',
    'TV-G': 'Kids',
    'PG': 'Older Kids',
    'G': 'Kids',
    'UR': 'Adults',
    'NC-17': 'Adults'
}
df['age_group']=df['rating'].map(age_rating)
top_country=df['country'].value_counts().head(10).index
df_top10=df[df['country'].isin(top_country)]
pivot_count=df_top10.pivot_table(index='country',columns='age_group',aggfunc='size',fill_value=0)
pivot_percent=pivot_count.div(pivot_count.sum(axis=1),axis=0)*100
plt.figure(figsize=(10,6))
sns.heatmap(pivot_percent,annot=True,fmt='.1f',cmap=None)
plt.title('Top 10 Countries: content distribution by age group')
plt.xlabel('Age group')
plt.ylabel('Country')
plt.tight_layout()
plt.show()




