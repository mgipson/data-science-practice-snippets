import pandas as pd 
import os
import matplotlib.pyplot as plt

def get_name_type():
    name_type = input("Would you like to see the performance of a marble or team?\n").lower()
    if name_type == 'marble' or name_type == 'team':
        return name_type+'_name'
    else:
        print('Marble or Team was not selected, please enter a valid selection.')
        return None

def get_name(name_type):
    name = input("Enter the name of the {}.\n".format(name_type.replace('_name', ''))).lower()
    # check if name is in name_type column
    if name in list(data[name_type].str.lower()):
        return name
    else:
        print("{} with name '{}' couldn't be found, please enter a valid selection.".format(name_type.replace('_name', '').title(), name))
        return None

if __name__ == "__main__":
    global data
    if not os.path.join(os.path.dirname( __file__ ), 'marbles.csv'):
        data = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-06-02/marbles.csv')
        data.to_csv('marbles.csv')
    else:
        print('Using marbles.csv in directory.')
        data = pd.read_csv('marbles.csv')

    # inputs
    name_type = None
    while(name_type is None):
        name_type = get_name_type()
    name = None
    while(name is None):
        name = get_name(name_type)

    # for each row, find those with the name_type matching name, and create a subset df from them
    data_subset = pd.DataFrame(columns = list(data.columns))
    data_subset = data_subset.append(pd.DataFrame(data=data.loc[data[name_type].str.lower() == name]))

    # calculate the m/s per race and add to dataframe
    m_per_s_list = []
    for index, row in data_subset.iterrows():
        total_race_length_m = row['number_laps'] * row['track_length_m']
        m_per_s = total_race_length_m / row['time_s']
        m_per_s_list.append(m_per_s)
    data_subset['m_per_s'] = m_per_s_list

    # Give a stats dashboard & graph
    name_label = data_subset.iloc[0][name_type]
    print('------------ Stats Dashboard for {} "{}"------------'.format(name_type.replace('_name', '').title(), name_label))
    avg_m_per_s = data_subset['m_per_s'].sum() / data_subset['m_per_s'].count()
    print('Average m/s for {}: {}'.format(name_label, avg_m_per_s))
    print('Best Race: {}'.format(data_subset['m_per_s'].max()))
    print('Worst Race: {}'.format(data_subset['m_per_s'].min()))

    plt.plot(data_subset['race'],data_subset['m_per_s'])
    plt.title('Performance of {} "{}"'.format(name_type.replace('_name', '').title(), name_label))
    plt.xlabel('Race')
    plt.ylabel('Time (m/s)')
    plt.show()