import sys
from tqdm import tqdm
import pandas as pd

print('''
Hi ...
      
Read Me : 
      This tool assumes that your data file contains Unique ID as Unique Identifier. 
      The Data file is in CSV (UTF - 8 Encoded) format.
      for the CEO the manager ID cell is blank.

''')


def build_data():
    path = input('Kindly enter the path to the CSV file (without any quotation) : ')
    param = input('Enter the name of the metadata where Manager Id is contained : ')
    df = pd.read_csv(path, dtype=str)
    df = df[['Unique Identifier', param]]
    return df

try:
    df = build_data()
except:
    try :
        print('Somewhere you messed up, Try again !')
        df = build_data()
    except:
        try :
            print('''
                    Somewhere you messed up Again , Try Once More !
                    Do not Enter the Path with quotation, Remove quotation and enter the path.
                    ''')
            df = build_data()
        except:
            print('Error again ! Failed to create the Dataframe')
            input('Type anything to Quit !')
            sys.exit()

# df = pd.read_csv('/Users/omkar/Downloads/nok.csv', dtype=str)

length = len(df['Unique Identifier'])

def get_manager(x):
    try: 
        index = df.loc[df['Unique Identifier'] == x].index[0]
        return df.iloc[index,1]
    except:
        return 'UM'
    
def chk_org(data, lenth):
    from tqdm import tqdm
    black_list = []
    checked_list = []
    unknown = []
    dummy = []
    df = data
    i = 0
    total_iter = lenth -1
    bar_format = "{l_bar}%s{bar}%s{r_bar}" % ("\033[38;5;11m", "\033[0m")  # Change font color to yellow
    progress_bar = tqdm(total=total_iter, desc="Processing", unit="steps",
                        dynamic_ncols= True, bar_format = bar_format, ncols = 100)
    while i<total_iter:
            if df.iloc[i,0] not in checked_list:
                x = str(df.iloc[i,0])
                # print(x)
                temp_list = []
                temp_list.append(x)
                while True:
                    manager = get_manager(x)
                    # print(manager)
                    if manager == 'UM':
                        # print('Unknown manager found for :', x, " !")
                        if x not in unknown:
                            unknown.append(x)
                        break
                    if manager in checked_list:
                        # print('Manager already checked')
                        for element in temp_list:
                            checked_list.append(element)
                        break
                    if str(manager) == 'nan':
                        # print('Reached CEO !')
                        for element in temp_list:
                            checked_list.append(element)
                        break
                    if manager in temp_list:
                        # print('manager in templist')
                        if x not in black_list:
                            black_list.append(x)

                        for element in temp_list:
                            checked_list.append(element)
                        break
                    else:
                        temp_list.append(manager)
                        # print(temp_list)
                        x = manager


            i+=1
            progress_bar.update(1)
            # track.append(len(set(checked_list)))
            # print(len(set(checked_list)),' ', i)
            # if i%500 ==0 or i == length-1:
            #     print(f'Progressed : {int((i/(length-1))*100)} %')
            # if i%100 == 0:
            # #     m = int((i/(lenth-1))*100)
            # if int((i/(lenth-1))*100) % 10 == 0:
            #         dummy.append(int((i / (lenth - 1)) * 100))
            #         if int((i / (lenth - 1)) * 100) not in dummy :
            #             print(f'Progressed : {int((i / (lenth - 1)) * 100)} %')

    return black_list, unknown


black_list, unknown = chk_org(data=df, lenth=len(df['Unique Identifier']))
# print('Completed  100% ')

print(f'Manager ID in Circular in Circular Reporting is {black_list}')
print(f'Number of Unknown Manager found is {len(unknown)}')

if len(unknown) !=0 or len(black_list) != 0:
    print('''
    
    Completed !
    
    The List of Unknown Manager and List of managers in circular mapping is prepared, give your path to save in CSV file
    
    ''')
    path = input('Enter the path without any quotation : ')
    e_data = {'Unknown Managers' : unknown}
    f_data = {'Manager in Circular reporting' : black_list}
    e_data =pd.DataFrame(e_data)
    f_data = pd.DataFrame(f_data)
    e_data.to_csv(str(path) + 'UnknownManager.csv', index=False)
    f_data.to_csv(str(path) + 'CircularRelationship.csv', index=False)
else:
    input('No Error Found! Type any word to Quit ! ')
