# -*- coding: utf-8 -*-

import pandas as pd
import os
from ddf_utils.str import to_concept_id
from ddf_utils.index import create_index_file


# configure paths
source = '../source/pp59adS3CHWfKPVb7dEexFA.xls'
out_dir = '../../'


if __name__ == '__main__':
    data001 = pd.read_excel(source, sheetname='Data')

    data001 = data001.rename(columns={'GDP per capita':'area'})

    # entities
    area = data001['area'].copy()
    area_id = area.map(to_concept_id)

    area_df = pd.DataFrame([], columns=['area', 'name'])
    area_df['area'] = area_id
    area_df['name'] = area

    path = os.path.join(out_dir, 'ddf--entities--area.csv')
    area_df.to_csv(path, index=False)

    # datapoints
    dp = data001.set_index('area')
    dp = dp.T.unstack()
    dp = dp.reset_index()

    dp.columns = ['area', 'year', to_concept_id('GDP per capita')]
    dp['area'] = dp['area'].map(to_concept_id)

    path = os.path.join(out_dir, 'ddf--datapoints--gdp_per_capita--by--area--year.csv')
    dp.dropna().to_csv(path, index=False)

    # concepts
    conc = ['gdp_per_capita', 'area', 'year', 'name']
    cdf = pd.DataFrame([], columns=['concept', 'name', 'concept_type'])
    cdf['concept'] = conc
    cdf['name'] = ['GDP per capita', 'Area', 'Year', 'Name']
    cdf['concept_type'] = ['measure', 'entity_domain', 'time', 'string']

    path = os.path.join(out_dir, 'ddf--concepts.csv')
    cdf.to_csv(path, index=False)

    # index
    create_index_file(out_dir)

    print("Done.")

