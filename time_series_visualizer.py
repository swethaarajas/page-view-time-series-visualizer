import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import datetime 
import calendar
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',index_col="date", parse_dates=["date"])
df.dropna()
df.head()

# Clean data
df = df[
        (df["value"] >= df["value"].quantile(0.025)) & 
        (df["value"] <= df["value"].quantile(0.975))]


def draw_line_plot():
    fig = plt.figure(figsize=(15,5))
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.plot(df.index, df["value"], color = 'red', linestyle = 'solid')


  
    #fig, ax = plt.figure(figsize=(15,5))
    #ax.xlabel("Date")
    #ax.ylabel("Page Views")
    #ax.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    #fig= ax.plot(df.index, df["value"], color = 'red', linestyle = 'solid')
  
# Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    #df_bar = None
    #df.index = pd.to_datetime(df.index)
    #df[['year', 'month', 'day']] = [x.timetuple()[:3] for x in df.index.tolist()]
    df.index = pd.to_datetime(df.index)
    df["month"] = df.index.month
    df["year"]= df.index.year
     
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month
    df_bar = df.groupby(["year", "month"])["value"].mean()
    df_bar = df_bar.unstack()

  # Draw bar plot 
    fig = df_bar.plot.bar(legend = True, figsize=(15,13)).figure
    plt.xlabel("Years",fontsize = 20)
    plt.ylabel("Average Page Views", fontsize = 20)
    #plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    #plt.legend(title = "months", fonts)
    plt.legend(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], fontsize = 18)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    ## Prepare data for box plots (this part is done!)
  
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    df_box['month_number'] = df_box['month'].apply(lambda x : list(calendar.month_abbr).index(x))
    df_box = df_box.sort_values(by=['month_number'], ascending = True)

    # Draw box plots (using Seaborn)
    fig, axis = plt.subplots(nrows = 1, ncols = 2, figsize = (10,5))
    axis[0]=sns.boxplot(x=df_box['year'], y=df_box['value'], ax = axis[0])
    axis[1]=sns.boxplot(x=df_box['month'], y=df_box['value'], ax = axis[1])

    axis[0].set_title("Year-wise Box Plot (Trend)")
    axis[0].set_xlabel("Year")
    axis[0].set_ylabel("Page Views")

    axis[1].set_title("Month-wise Box Plot (Seasonality)")
    axis[1].set_xlabel("Month")
    axis[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
