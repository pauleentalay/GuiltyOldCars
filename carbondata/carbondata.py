import pandas as pd

# NOTE: use only fix_headers and group_by_brand_model if using file from website

# def fix_headers(filename):
#     filename_ed = filename+'_ed'
#     df1 = pd.read_csv(f'{filename}.csv')
#     df1.columns = [c.replace(' ', '_') for c in df1.columns]
#     df1.columns = [c.replace('_(g/km)', '') for c in df1.columns]
#     df1.to_csv(f'{filename}_ed.csv', index=False)
#     return filename_ed
#
#
# def group_by_brand_model(filename_ed):                                           #not used first
#     df2 = pd.read_csv(f'{filename_ed}.csv')
#     grouped = df2.groupby(['Mk', 'Cn']).Enedc.mean().reset_index()               #reset_index() converts series to df
#     grouped.to_csv(f'{filename_ed}_brand_model.csv', index=False)

# NOTE: this will only get the average emission of each brand
# manually fix the data ie: remove 'vw' from 'volkswagen vw'


def group_by_brand(filename_ed):
    """

    :param filename_ed: csv file contains brand name (Mk), model (Cn), and Emission in g/Km (Enedc)
    :return: groups brand name (Mk) with average Emission g/Km (Enedc)

    csv file de_car_data_ed_grouped.csv (2019 data) can be used here
    """
    df2 = pd.read_csv(filename_ed)
    grouped = df2.groupby('Mk').Enedc.mean().reset_index()
    grouped.to_csv(f'{filename_ed}_brand.csv', index=False)

