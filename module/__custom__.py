# Libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_searchbox import st_searchbox
from module.__selectpage__ import st_page_selectbox

# Load the dataset
df = pd.read_csv('./data/join_02.csv')

# Format preparation
df['date'] = pd.to_datetime(df['date'])
df['release_date'] = pd.to_datetime(df['release_date'])
df['avg_peak_perc'] = df['avg_peak_perc'].str.rstrip('%').astype('float') 
df = df.dropna()

# ### adding single-player feature ###
def add_opp_features(genre):
    df[genre[0]] = (df[genre[1]]==0)*1


def add_range_features(arg):
    lower = arg[0]; upper = arg[1]
    name = arg[2]; genre = arg[3]
    
    condition = (df[genre]>=lower) & (df[genre]<upper)
    df[name] = condition*1

def name(target):
    return target.replace('_', ' ').title()

def add_top_games(top_games, favorite_game, ranges, df_ax):
    if favorite_game in top_games: 
        top_games = df_ax.gamename.unique()[ranges[0]-1:ranges[1]+1]
    elif favorite_game!=None: 
        top_games = np.append(top_games, favorite_game)
    return top_games

def search(target):
    gamenames = df['gamename'].unique()
    result = []
    for gamename in gamenames:
        if target.lower() in gamename.lower():
            result.append(gamename)
    return result 

def searchbox():
    selected_game = st_searchbox(
        search_function=search,
        key="gamename_searchbox",
        default_options=None, 
        placeholder="Compare with your Favorite Game...",
    )
    return selected_game

def dfbox(ax_name, y_name, df_ax):
    title = f"1.1 Dataset of :blue[{ax_name}] Games Sorted by :blue[{y_name}]:"
    st.subheader(title)
    st.dataframe(df_ax)


def plot1_box(ax, y, order_name, ranges, df_ax, top_games):
    ax_name = name(ax)
    y_name = name(y)
    
    title = f"1.3 Rank {ranges[0]} to {ranges[1]} :blue[{ax_name}] Games with the :red[{order_name}] :blue[{y_name}]"
    st.subheader(title)

    # Plot 1 - select box
    favorite_game = searchbox()                                                     # search box to add a user favorite game on Plot 1
    top_games = add_top_games(top_games, favorite_game, ranges, df_ax)        
    options = top_games
    selected_options = st.multiselect('Select Video Games', options)

    # Plot 1
    title_names = ','.join(selected_options)
    plot_title = f"Monthly {y_name} of {title_names} Over Time"
    gb = df.sort_values(by='date')
    gb_list = {game: gb[gb["gamename"] == game] for game in selected_options}

    fig_1 = go.Figure()
    fig_1.update_layout(
        title = plot_title, 
        xaxis_title = 'Date',
        yaxis_title = y_name,
    )
    for game, gb in gb_list.items():
        fig_1 = fig_1.add_trace(go.Scatter(x=gb["date"], y=gb[y], name=game, mode='lines'))
    st.plotly_chart(fig_1)

def plo2_box(theme, y, genres, df_bx):
    y_name = name(y)
    
    title = f"2.0 Comparison Among :blue[{theme}] on Monthly :blue[{y_name}]:"
    st.subheader(title)

    # Plot 2 - Multiselect box
    options = genres
    selected_options = st.multiselect('Select Comparing Categories', options)
    selected_names = ','.join(selected_options)                         # formating titles
    plot_title = f"Monthly {y_name} of {selected_names} Over Time"


    # Plot 2

    # Tab 1 - Mean Line Plot
    gb = df_bx.sort_values(by='date')      # New copy of df
    mean_list = {genre: gb[gb[genre] == 1].groupby('date').mean(y).reset_index() for genre in selected_options}

    fig_mean = go.Figure()
    for genre, gb in mean_list.items():
        fig_mean = fig_mean.add_trace(go.Scatter(x=gb['date'], y=gb[y], name=genre, mode='lines'))
    fig_mean.update_layout(
        title = 'Mean of ' + plot_title,
        xaxis_title = 'Date',
        yaxis_title = 'Mean of '+y_name,
    )


    # Tab 2 - Sum Line Plot
    gb = df_bx.sort_values(by='date')
    sum_list = {genre: gb[gb[genre] == 1].groupby('date').sum(y).reset_index() for genre in selected_options}

    fig_sum = go.Figure()
    for genre, gb in sum_list.items():
        fig_sum = fig_sum.add_trace(go.Scatter(x=gb['date'], y=gb[y], name=genre))
    fig_sum.update_layout(
        title = 'Sum of ' + plot_title,
        xaxis_title='Date',
        yaxis_title='Sum of '+y_name,
    )

    # Tab 3 - Scatter / Marker Plot
    gb = df_bx.sort_values(by='date')
    gb_list = {genre: gb[gb[genre] == 1] for genre in selected_options}

    fig_sc = go.Figure()
    for genre, gb in gb_list.items():
        fig_sc = fig_sc.add_trace(go.Scatter(x=gb["date"], y=gb[y], name=genre, mode='markers'))
    fig_sc.update_traces(
        marker=dict(size=4, opacity=0.5)
    )
    fig_sc.update_layout(
        title = plot_title,
        xaxis_title='Date',
        yaxis_title=y_name,
    )


    # Showing Plot
    tab1, tab2, tab3 = st.tabs(['Line Plot', 'Sum Plot', 'Scatter Plot'])
    with tab1:
        st.plotly_chart(fig_mean)
    with tab2:
        st.plotly_chart(fig_sum)
    with tab3:
        st.plotly_chart(fig_sc)


##### Execute Page #####
def exec_page(emoji, theme, page_genres):
    # Select Page
    st_page_selectbox(theme)
    
    # Header
    st.header(emoji)
    st.title(f"Customized Plot on :blue[{theme}]")

    ##### FILTER #####
    # Featuer for both axis
    features = ['avg', 'gain', 'peak', 'avg_peak_perc']
    features += ['metacritic_score', 'positive', 'negative']
    genres = page_genres
    ##################


    # User Menu
    order = st.toggle(label='Find the Worst Games', value=False)                    # descending order toggle switch
    left_col, right_col = st.columns(2)                                             # Columns dividing 
    with left_col: y = st.selectbox("Select a Feature (y-axis)", features)          # feature select box (y axis of Plots)
    with right_col: ax = st.selectbox("Select a Genre (legend)", genres)            # category select box (filtering game basse on genre)

    order_name='Worst' if order else 'Highest'                                      # string formating
    y_name = name(y)                                            # string of names that would be used on Plot title
    ax_name = name(ax)

    # Data - sorting and filtering
    df_ax = df[df[ax]==1]
    df_ax = df_ax[['gamename', 'date', y, ax]].sort_values(by=y, ascending=order).reset_index()     # Data for Plot 1
    df_bx = df[['gamename', 'date', y]+genres].sort_values(by=y, ascending=order).reset_index()     # Data for Plot 2


    # Slider
    max = df_ax.gamename.unique().tolist()                          # max number of games
    max = len(max)-1
    ranges = st.slider(
        label=f'Select range of the {order_name.lower()} games',
        value = (1, 5), 
        min_value=1, max_value=30, 
        # min_value=1, max_value=max, 
    )
    top_games = df_ax.gamename.unique()[ranges[0]-1:ranges[1]]
    

    # Dataframe preview
    dfbox(ax_name, y_name, df_ax)

    ##### PLOT 1 #####
    # Plot 1 - markdown
    st.markdown("""***""")
    plot1_box(ax, y, order_name, ranges, df_ax, top_games)

    ##### PLOT 2 #####
    # Plot 2 - markdown
    st.markdown("""***""")
    plo2_box(theme, y, genres, df_bx)

##### HOME PAGE #####
def exec_page_home(theme):
    st_page_selectbox(theme)
    
    # Header
    st.header(f"👋 ForcaSteam")
    st.title("Customized Plot on :blue[General Features]")

    ##### FILTER #####
    # Featuer for both axis
    features = ['avg', 'gain', 'peak', 'avg_peak_perc']
    genres = features


    left_col, right_col = st.columns(2)
    order = st.toggle(label='Find the Worst Games', value=False)        # descending order toggle switch
    y = st.selectbox("Select a Feature (y-axis)", features)                      # feature select box
    order_name='Worst' if order else 'Highest'                          # string formating
    y_name = name(y)

    # Data - sorting and filtering
    df_ax = df[['gamename', 'date', y]].sort_values(by=y, ascending=order).reset_index()    # Data - Plot 1
    # df_bx = df[['gamename', 'date']+features].sort_values(by=y, ascending=order).reset_index()      # Data - Plot 2

    # Slider
    max = df_ax.gamename.unique().tolist()
    max = len(max)-1
    ranges = st.slider(
        label=f'Select range of the {order_name.lower()} games',
        value = (1, 5),
        min_value=1, max_value=30, 
        # min_value=1, max_value=max, 
    )
    top_games = df_ax.gamename.unique()[ranges[0]-1:ranges[1]]

    # Dataframe preview
    dfbox("", y_name, df_ax)


    ##### PLOT 1 #####
    # Plot 1 - markdown
    st.markdown("""***""")
    title = f"1.3 Rank {ranges[0]} to {ranges[1]} Games with the Overall :red[{order_name}] :blue[{y_name}]"
    st.subheader(title)


    # Plot 1 - select box
    favorite_game = searchbox()                                                     # search box to add a user favorite game on Plot 1
    top_games = add_top_games(top_games, favorite_game, ranges, df_ax) 
    options = top_games
    selected_options = st.multiselect('Select Video Games', options)

    # Plot 1
    title_names = ','.join(selected_options)
    plot_title = f"Monthly {y_name} of {title_names} Over Time"
    gb = df_ax.sort_values(by='date')
    gb_list = {game: gb[gb["gamename"] == game] for game in selected_options}

    fig_1 = go.Figure()
    fig_1.update_layout(
        title = plot_title, 
        xaxis_title = 'Date',
        yaxis_title = y_name,
    )
    for game, gb in gb_list.items():
        fig_1 = fig_1.add_trace(go.Scatter(x=gb["date"], y=gb[y], name=game, mode='lines'))
    st.plotly_chart(fig_1)

##### PUBLISHERS PAGE #####
def exec_page_pub(emoji, theme, main_genre):
    st_page_selectbox(theme)
    
    # Header
    st.header(emoji)
    st.title(f"Customized Plot on :blue[{theme}]")

    ##### FILTER #####
    # Featuer for both axis
    features = ['avg', 'gain', 'peak', 'avg_peak_perc']
    features += ['metacritic_score', 'positive', 'negative']
    genres = []

    left_col, right_col = st.columns(2)
    order = st.toggle(label='Find the Worst Games', value=False)        # descending order toggle switch
    with left_col: 
        y = st.selectbox("Select a Feature", features)                  # feature select box
    with right_col: 
        if (main_genre=='publishers'):
            genres = df.sort_values(by=y, ascending=order).publishers.unique()[0:5].tolist()
        elif (main_genre=='developers'):
            genres = df.sort_values(by=y, ascending=order).developers.unique()[0:5].tolist()
        
        for genre in genres:
            df[genre] = (df[main_genre]==genre)*1
        ax = st.selectbox("Select a Category", genres)                  # category select box
    order_name='Worst' if order else 'Highest'                          # string formating
    y_name = y.replace('_', ' ').title()
    ax_name = ax.title().replace('_', ' ')

    # ### adding best publisher features feature ###

    # Data - sorting and filtering
    df_ax = df[df[ax]==1]
    df_ax = df_ax[['gamename', 'date', y, ax]].sort_values(by=y, ascending=order).reset_index()    # Data - Plot 1
    df_bx = df[['gamename', 'date', y]+genres].sort_values(by=y, ascending=order).reset_index()      # Data - Plot 2

    # Slider
    max = df_ax.gamename.unique().tolist()
    max = len(max)
    if(max < 2):value_r = 0
    elif(max > 4):value_r = 5
    else: value_r = max

    ranges = st.slider(
        label=f'Select range of the {order_name.lower()} games',
        value = (1, value_r),
        # min_value=0, max_value=30, 
        min_value=1, max_value=max, 
    )
    top_games = df_ax.gamename.unique()[ranges[0]-1:ranges[1]]

    # Dataframe preview
    dfbox(ax_name, y_name, df_ax)

    title = f"1.2 {ranges[1]} :blue[{ax_name}] Games with the :red[{order_name}] Monthly :blue[{y_name}]:"
    st.subheader(title)
    st.write(top_games)



    ##### PLOT 1 #####
    # Plot 1 - markdown
    st.markdown("""***""")
    plot1_box(ax, y, order_name, ranges, df_ax, top_games)


    ##### PLOT 2 #####
    # Plot 2 - markdown
    st.markdown("""***""")
    plo2_box(theme, y, genres, df_bx)
