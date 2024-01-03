########## LIBRARIES ##########
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_searchbox import st_searchbox
from module.__selectpage__ import st_page_selectbox

########## DATASET ##########
df = pd.read_csv('./data/join_02.csv')
df['date'] = pd.to_datetime(df['date'])                 # Format preparation
df['release_date'] = pd.to_datetime(df['release_date'])
df['avg_peak_perc'] = df['avg_peak_perc'].str.rstrip('%').astype('float') 
df = df.dropna()


########## FUNCTION ##########
##### Adding single-player feature
def add_opp_features(genre):
    df[genre[0]] = (df[genre[1]]==0)*1

##### Adding feature depending on range of a base feature
"""Scenario of using this function
For example, if we want a feature of price
between $10 to $30
"""
def add_range_features(arg):
    lower = arg[0]; upper = arg[1]
    name = arg[2]; genre = arg[3]
    
    condition = (df[genre]>=lower) & (df[genre]<upper)
    df[name] = condition*1

# Returning title version of feature name
def name(target):
    return target.replace('_', ' ').title()

##### Searchbox Functions
# Appending favorite game selected by user to filtered list
    """use after search box
    """
def add_top_games(top_games, fav_games, ranges, df_ax):
    ranges_last = ranges[1]
    for fav in fav_games:
        if fav in top_games: 
            range_last+=1
            top_games = df_ax.gamename.unique()[ranges[0]-1:range_last]
        elif fav!=None: 
            top_games = np.append(top_games, fav)
    return top_games

def add_list(favorite_game, rec_games):
    fav_games = []
    if favorite_game[0]: fav_games = favorite_game
    if rec_games: 
        fav_games = list(set(fav_games + rec_games))
    return fav_games

# fav_games = []
# if favorite_game: fav_games = [favorite_game]
# if st.session_state.gamenames[-1]: 
#     rec_games = st.session_state.gamenames[-1]
#     fav_games = list(set(fav_games + rec_games))

# def add_top_games(top_games, favorite_game, ranges, df_ax):
#     if favorite_game in top_games: 
#         top_games = df_ax.gamename.unique()[ranges[0]-1:ranges[1]+1]
#     elif favorite_game!=None: 
#         top_games = np.append(top_games, favorite_game)
#     return top_games

# Linear search over all gamenames
def search(target):
    gamenames = df['gamename'].unique()                 # all unique gamenames
    result = []
    for gamename in gamenames:
        if target.lower() in gamename.lower():          # games that contains the searching keyword
            result.append(gamename)
    return result 

# Streamlit search box
def searchbox():
    selected_game = st_searchbox(
        search_function=search,
        key="gamename_searchbox",
        default_options=None, 
        placeholder="Compare with your Favorite Game...",
    )
    return selected_game

# Overloaded with target name 
def searchbox(target):
    col1, col2= st.columns([1,1])
    with col1:  
        selected_game = st_searchbox(
            search_function=search,
            key="gamename_searchbox",
            default_options=target, 
            placeholder="Compare with your Favorite Game...",
        )
    return selected_game

########## PAGE SECTION ##########
# Datafram Section
    """Dataframe
    together with Title
    """
def dfbox(ax_name, y_name, df_ax, ranges, order_name):
    title = f"1.2 :blue[{ax_name}] Games with the {order_name} :blue[{y_name}]:"
    with st.sidebar:
        gamenames = df_ax.gamename.unique()
        df_names = pd.DataFrame(gamenames, columns=['gamename'])
        st.write(title)
        st.dataframe(df_names[ranges[0]:ranges[1]+1])

def rec_dfbox():
    title = f"1.1 :blue[Recommended] by :green[GameInsightify]"
    if len(st.session_state.gamenames) > 0:
        with st.sidebar:
            rec_games = st.session_state.gamenames[-1]
            df_names = pd.DataFrame(rec_games, columns=['gamename'])
            st.write(title)
            st.dataframe(df_names[0:len(rec_games)])
# Overloaded with argument of names
def home_dfbox(rec_games):
    title = f":blue[Recommended] by :green[GameInsightify]"
    if len(rec_games) > 0:
        with st.sidebar:
            df_names = pd.DataFrame(rec_games, columns=['gamename'])
            st.write(title)
            st.dataframe(df_names[0:len(rec_games)])


# plot 1 Section
    """Plot contains the top ranked games
    based on the selected features, 
    within selected genre
    """
def plot1_box(ax, y, order_name, ranges, df_ax, top_games):
    ax_name = name(ax)          # formating strings
    y_name = name(y)            # formeting strings
    
    title = f"1.3 Rank {ranges[0]} to {ranges[1]} :blue[{ax_name}] Games with the :red[{order_name}] :blue[{y_name}]"
    st.subheader(title)

    # Plot 1 - select box
    rec_games = []
    if len(st.session_state.gamenames) > 0 : rec_games = st.session_state.gamenames[-1]
    favorite_game = searchbox(None)                                                     # search box to add a user favorite game on Plot 1
    fav_games = add_list([favorite_game], rec_games)
    fav_options = st.multiselect('Select Recommended Games', fav_games)
    
    options = top_games
    selected_tops = st.multiselect('Select Video Games', options)
    selected_options = add_top_games(selected_tops, fav_options, ranges, df_ax) 

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

def plot2_box(theme, y, genres, df_bx):
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

# Plot 3 - Pie chart
import plotly.express as px
def plot3_box(theme, labels):
    title = f"2.1 Ratio of Games Among :blue[{theme}]"
    st.subheader(title)
    
    if (type(labels)==str):
        values = []
        index = df[labels].unique().tolist()
        for idx, value in enumerate(index):
            count = len(df[df[labels] == value])
            values.append(count)
            if(count/len(df) < 0.02): index[idx] = 'Other'
        
        df_p = pd.DataFrame(data = values,  
                index = index,  
                columns = ['counts']) 
        df_p = df_p.reset_index().rename(columns={'index':labels})
        fig_ratio = px.pie(df_p, values='counts', names=labels)
        st.plotly_chart(fig_ratio)
        
    else:
        values = []
        for label in labels:
            value = len(df[df[label]==1])
            values.append(value)
        
        fig_ratio = go.Figure(data=[go.Pie(labels=labels, values=values)])
        st.plotly_chart(fig_ratio)

# Could not overload function, so renamed it
def plot3_box_limit(theme, labels, limit_perc):
    title = f"2.1 Ratio of Games Among :blue[{theme}] over :blue[{limit_perc*100}%]"
    st.subheader(title)
    
    values = []
    index = df[labels].unique().tolist()
    for idx, value in enumerate(index):
        count = len(df[df[labels] == value])
        values.append(count)
        if(count/len(df) < limit_perc): index[idx] = 'Other'
    
    df_p = pd.DataFrame(data = values,  
            index = index,  
            columns = ['counts']) 
    df_p = df_p.reset_index().rename(columns={'index':labels})
    fig_ratio = px.pie(df_p, values='counts', names=labels)
    st.plotly_chart(fig_ratio)

def plot_chat_box(y, query_num, top_games):
    y_name = name(y)            # formeting strings
    
    title = f"1.2 Comparison on The {query_num} Best Recommended Games on :blue[{y_name}]"
    st.subheader(title)

    # Plot 1 - select box                                                    # search box to add a user favorite game on Plot 1
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


##### Execute Page #####
def exec_page(emoji, theme, page_genres):
    # Select Page
    st_page_selectbox(theme)
    
    # Header
    st.header(emoji)
    st.header(f"Customized Plot on :blue[{theme}]")

    ##### FILTER #####
    # Featuer for both axis
    features = ['avg', 'gain', 'peak', 'avg_peak_perc']
    features += ['metacritic_score', 'positive', 'negative']
    genres = page_genres
    ##################


    # User Menu
    order = st.toggle(label='Rank the Worst Games', value=False)                    # descending order toggle switch
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
        value = (1, 3), 
        min_value=1, max_value=30, 
        # min_value=1, max_value=max, 
    )
    top_games = df_ax.gamename.unique()[ranges[0]-1:ranges[1]]
    

    # Dataframe preview
    rec_dfbox()
    dfbox(ax_name, y_name, df_ax, ranges, order_name)  

    ##### PLOT 1 #####
    # Plot 1 - markdown
    st.markdown("""***""")
    plot1_box(ax, y, order_name, ranges, df_ax, top_games)

    ##### PLOT 2 #####
    # Plot 2 - markdown
    st.markdown("""***""")
    plot2_box(theme, y, genres, df_bx)

##### HOME PAGE #####
def exec_page_home(theme):
    st_page_selectbox(theme)
    
    # Header
    st.header("👋")
    st.header("Customized Plot on :blue[General Features]")

    ##### FILTER #####
    # Featuer for both axis
    features = ['avg', 'gain', 'peak', 'avg_peak_perc']
    genres = features


    left_col, right_col = st.columns(2)
    order = st.toggle(label='Rank the Worst Games', value=False)        # descending order toggle switch
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
        value = (1, 3),
        min_value=1, max_value=30, 
        # min_value=1, max_value=max, 
    )
    top_games = df_ax.gamename.unique()[ranges[0]-1:ranges[1]]

    # Dataframe preview
    rec_dfbox()
    dfbox("", y_name, df_ax, ranges, order_name)


    ##### PLOT 1 #####
    # Plot 1 - markdown
    st.markdown("""***""")
    title = f"1.3 Rank {ranges[0]} to {ranges[1]} Games with the Overall :red[{order_name}] :blue[{y_name}]"
    st.subheader(title)


    # Plot 1 - select box
    rec_games = []
    if len(st.session_state.gamenames)>0: rec_games = st.session_state.gamenames[-1]
    favorite_game = searchbox(None)                                                     # search box to add a user favorite game on Plot 1
    fav_games = add_list([favorite_game], rec_games)
    fav_options = st.multiselect('Select Recommended Games', fav_games)
    
    options = top_games
    selected_tops = st.multiselect('Select Video Games', options)
    selected_options = add_top_games(selected_tops, fav_options, ranges, df_ax) 

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
    st.header(f"Customized Plot on :blue[{theme}]")

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
    rec_dfbox()
    dfbox(ax_name, y_name, df_ax, ranges, order_name)

    title = f"1.2 5 :blue[{theme}s] with the :red[{order_name}] Monthly :blue[{y_name}]:"
    st.subheader(title)
    st.dataframe(genres[0:5])



    ##### PLOT 1 #####
    # Plot 1 - markdown
    st.markdown("""***""")
    plot1_box(ax, y, order_name, ranges, df_ax, top_games)


    ##### PLOT 2 #####
    # Plot 2 - markdown
    st.markdown("""***""")
    plot2_box(theme, y, genres, df_bx)
