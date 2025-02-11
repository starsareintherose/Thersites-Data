import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_csv_grouped_by_name(csv_folder):
    plt.figure(figsize=(10, 6))

    # define the color
    group_colors = {
        'darlingtoni': '#75ff66',  
        'mitchellae': '#48b9ff',
        'novaehollandiae': '#ff888a',
        'richmondiana': '#ede100',
        'sp1': '#0057b7',
        'sp2': '#b3b3b3',
    }

    # get all the csv in the folder
    csv_files = [os.path.join(csv_folder, file) for file in os.listdir(csv_folder) if file.endswith('.csv')]

    plotted_groups = set()
    handles = []  # init
    labels = []   # init

    for file in csv_files:
        # get base name
        file_name = os.path.basename(file)
        
        # read every csv
        df = pd.read_csv(file)
        
        # read first and the second row
        x = df.iloc[:, 0].values
        y = df.iloc[:, 1].values
        
        # extract group name by `_`
        group_name = file_name.split('_')[0]

        # debug
        print(f"File: {file_name}, Group name extracted: {group_name}")

        # if group doesn't exsit, use the bnalck
        color = group_colors.get(group_name, 'black')

        # draw curve lines
        plt.plot(x, y, label=group_name, color=color)

        line, = plt.plot(x, y, color=color)
        # add label of groups
        if group_name not in plotted_groups:
            handles.append(line)
            labels.append(group_name)
            plotted_groups.add(group_name)

    # create label
    plt.xlabel('Flagellum position (1 cm)')
    plt.ylabel('Flagellum width (1 cm)')
    plt.title('Flagellum width variation')

    # create group legend
    plt.legend(handles=handles, labels=labels, title='Group')

    plt.savefig("flagellum_shape.svg")

    # show the image
    plt.show()

# main function
csv_folder = '.' 
plot_csv_grouped_by_name(csv_folder)

