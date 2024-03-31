import os

def pe_decomposition_template(output_path):
    calculation_function_template='''
import pandas as pd
from typing import List, Dict,Literal,Union

def filter_dataframe_on_time_period(input_dataframe:pd.DataFrame,year_col_name:str,month_col_name:str,time_period_start_month:int,time_period_end_month:int)->pd.DataFrame:
    """
    Filter a DataFrame based on a specified time period defined by months.

    Parameters:
        input_dataframe (pd.DataFrame): The DataFrame to filter.
        year_col_name (str): The name of the column containing year information.
        month_col_name (str): The name of the column containing month information.
        time_period_start_month (int): The start month index of the time period (inclusive).
        time_period_end_month (int): The end month index of the time period (exclusive).

    Returns:
        pd.DataFrame: The filtered DataFrame containing data within the specified time period.
    """
    input_dataframe[year_col_name] = input_dataframe[year_col_name].astype(str)
    input_dataframe[month_col_name] = input_dataframe[month_col_name].astype(str).str.zfill(2)
    year_month_col_name=year_col_name+'_'+month_col_name
    input_dataframe[year_month_col_name]=input_dataframe[year_col_name]+input_dataframe[month_col_name]
    year_month_unique_values = list(input_dataframe[year_month_col_name].unique())
    year_month_unique_values.sort()
    updated_list=year_month_unique_values[time_period_start_month:time_period_end_month]
    filtered_input_dataframe=input_dataframe[(input_dataframe[year_month_col_name].isin(updated_list))]
    return filtered_input_dataframe


def filter_dataframe_based_on_col_values(input_dataframe: pd.DataFrame, filters: Dict[str, List[str]]) -> pd.DataFrame:
    """
    Filter a DataFrame based on specified column values.

    Parameters:
        input_dataframe (pd.DataFrame): The DataFrame to filter.
        filters (Dict[str, List[str]]): A dictionary where keys are column names and values are lists of values
                                         to filter on.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    return input_dataframe[
        all(input_dataframe[column].isin(values) for column, values in filters.items())
    ]


def group_input_dataframe(input_dataframe: pd.DataFrame,groupby_columns: List[str],group_value_columns: Dict[str, Literal['sum', 'mean','min','max','count']]) -> pd.DataFrame:
    """
    Group a DataFrame based on specified columns and perform aggregation operations on selected value columns.

    Parameters:
        input_dataframe (pd.DataFrame): The DataFrame to be grouped and aggregated.
        groupby_columns (List[str]): A list of column names to group the DataFrame by.
        group_value_columns (Dict[str, Literal['sum', 'mean', 'min', 'max', 'count']]): A dictionary where keys are column names to apply aggregation operations on, and values specify the type of aggregation ('sum', 'mean', 'min', 'max', 'count').

    Returns:
        pd.DataFrame: The grouped DataFrame with aggregation applied to specified columns.
    """
    grouped_input_dataframe=input_dataframe.groupby(groupby_columns,as_index=False).agg(group_value_columns).reset_index()
    return grouped_input_dataframe


def calculate_volume_mix(input_dataframe:pd.DataFrame,sales_column_name:str,volume_mix_sales_column_name:str)->pd.DataFrame:
    """
    Calculate volume mix for each row in a DataFrame based on specified sales column.

    Parameters:
        input_dataframe (pd.DataFrame): The DataFrame containing sales data.
        sales_column_name (str): The name of the column containing sales values.
        volume_mix_sales_column_name (str): The name of the new column to store volume mix values.

    Returns:
        pd.DataFrame: The DataFrame with volume mix values calculated and added as a new column.
    """
    input_dataframe[sales_column_name]=input_dataframe[sales_column_name].astype(float)
    column_sum = input_dataframe[sales_column_name].sum()
    input_dataframe[volume_mix_sales_column_name] = input_dataframe[sales_column_name] / column_sum
    return input_dataframe


def contains_only_numerical_values(lst: List) -> bool:
    """
    Check if the elements in a list are numerical values.

    Parameters:
        lst (List): The list to be checked.

    Returns:
        bool: True if all elements in the list are numerical values (int, float, or string representation of a number), False otherwise.
    """
    return all(isinstance(item, (int, float)) or (isinstance(item, str) and item.replace('.', '', 1).isdigit()) for item in lst)



def get_vol_mix_multiplication_factor(sm_col: pd.Series, sku_col_name: str, manufacturer_col_name: str, vol_mix_col_name: str, manufacturer_sku_vol_mix_data: pd.DataFrame) -> Union[int, float]:
    """
    Get the volume mix multiplication factor for a specific SKU and manufacturer.

    Parameters:
        sm_col (pd.Series): The Series representing the SKU and manufacturer.
        sku_col_name (str): The name of the column containing SKU information.
        manufacturer_col_name (str): The name of the column containing manufacturer information.
        vol_mix_col_name (str): The name of the column containing volume mix data.
        manufacturer_sku_vol_mix_data (pd.DataFrame): The DataFrame containing volume mix data for SKUs and manufacturers.

    Returns:
        Union[int, float]: The volume mix multiplication factor if found, otherwise 1.
    """
    if len(manufacturer_sku_vol_mix_data[vol_mix_col_name][(manufacturer_sku_vol_mix_data[manufacturer_col_name]==sm_col.name.split('.')[0]) & (manufacturer_sku_vol_mix_data[sku_col_name]==sm_col.values[0])].values) >0:
       return manufacturer_sku_vol_mix_data[vol_mix_col_name][(manufacturer_sku_vol_mix_data[manufacturer_col_name]==sm_col.name.split('.')[0]) & (manufacturer_sku_vol_mix_data[sku_col_name]==sm_col.values[0])].values
    return [1]



def multiply_sm_col_with_vol_mix_value(col: pd.Series, 
                                       manufacturer_sku_vol_mix_data: pd.DataFrame, 
                                       sku_col_name: str, 
                                       manufacturer_col_name: str, 
                                       vol_mix_col_name: str) -> pd.Series:
    """
    Multiply the values in a column with volume mix factors based on SKU and manufacturer.

    Parameters:
        col (pd.Series): The Series representing the column to be multiplied.
        manufacturer_sku_vol_mix_data (pd.DataFrame): The DataFrame containing volume mix data for SKUs and manufacturers.
        sku_col_name (str): The name of the column containing SKU information in the volume mix data.
        manufacturer_col_name (str): The name of the column containing manufacturer information in the volume mix data.
        vol_mix_col_name (str): The name of the column containing volume mix data in the volume mix data.

    Returns:
        pd.Series: The modified column with values multiplied by volume mix factors.
    """
    print(manufacturer_sku_vol_mix_data)
    if contains_only_numerical_values(col.values[1:]):
        col.values[1:] = [float(x) for x in col.values[1:]]
        col.values[1:]*=get_vol_mix_multiplication_factor(col,sku_col_name,manufacturer_col_name,vol_mix_col_name,manufacturer_sku_vol_mix_data)
    return col



def calculate_sm_grid_X_vol_mix(sm_grid: pd.DataFrame, 
                                 manufacturer_sku_vol_mix_data: pd.DataFrame, 
                                 sku_col_name: str, 
                                 manufacturer_col_name: str, 
                                 vol_mix_col_name: str) -> pd.DataFrame:
    """
    Calculate the product of a Sales Mix (SM) grid with volume mix factors.

    Parameters:
        sm_grid (pd.DataFrame): The Sales Mix (SM) grid DataFrame.
        manufacturer_sku_vol_mix_data (pd.DataFrame): The DataFrame containing volume mix data for SKUs and manufacturers.
        sku_col_name (str): The name of the column containing SKU information in the volume mix data.
        manufacturer_col_name (str): The name of the column containing manufacturer information in the volume mix data.
        vol_mix_col_name (str): The name of the column containing volume mix data in the volume mix data.

    Returns:
        pd.DataFrame: The modified SM grid DataFrame with values multiplied by volume mix factors.
    """
    sm_grid_X_vol_mix_df=sm_grid.apply(lambda col: multiply_sm_col_with_vol_mix_value(col, manufacturer_sku_vol_mix_data,sku_col_name,manufacturer_col_name,vol_mix_col_name), axis=0)
    return sm_grid_X_vol_mix_df



def normalize_sm_grid_X_vol_mix(sm_grid_X_vol_mix_df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize the Sales Mix (SM) grid multiplied by volume mix factors.

    Parameters:
        sm_grid_X_vol_mix_df (pd.DataFrame): The SM grid DataFrame multiplied by volume mix factors.

    Returns:
        pd.DataFrame: The normalized SM grid DataFrame.
    """
    sm_grid_X_vol_mix_df.iloc[1:, 2:] = sm_grid_X_vol_mix_df.iloc[1:, 2:].div(sm_grid_X_vol_mix_df.iloc[1:, 2:].sum(axis=1), axis=0)
    return sm_grid_X_vol_mix_df



def calculate_walkrate_of_skus_for_given_manufacturer(normalized_sm_X_vol_mix_df: pd.DataFrame, 
                                                      sku_col_name: str, 
                                                      manufacturer_name_to_calculate_walkrate: str, 
                                                      walkrate_col_name: str) -> pd.DataFrame:
    """
    Calculate the walk rate of SKUs for a given manufacturer.

    Parameters:
        normalized_sm_X_vol_mix_df (pd.DataFrame): The normalized Sales Mix (SM) DataFrame multiplied by volume mix factors.
        sku_col_name (str): The name of the column containing SKU information.
        manufacturer_name (str): The name of the manufacturer.
        walkrate_col_name (str): The name of the column to store the calculated walk rates.

    Returns:
        pd.DataFrame: DataFrame containing SKUs and their calculated walk rates for the given manufacturer.
    """
    normalized_sm_X_vol_mix_df=normalized_sm_X_vol_mix_df.rename(columns={'Unnamed: 1':sku_col_name})
    given_manufacturer_cols = [col for col in normalized_sm_X_vol_mix_df.columns if col.startswith(manufacturer_name_to_calculate_walkrate)]
    given_manufacturer_cols.insert(0,sku_col_name)
    filtered_dataframe_for_skus=normalized_sm_X_vol_mix_df[given_manufacturer_cols]
    filtered_dataframe_for_skus=filtered_dataframe_for_skus.iloc[1:]
    filtered_dataframe_for_skus[walkrate_col_name] = filtered_dataframe_for_skus.iloc[:, 1:].sum(axis=1)
    filtered_dataframe_for_skus[walkrate_col_name]=1-filtered_dataframe_for_skus[walkrate_col_name]
    walkrate_calculated_dataframe_for_skus=filtered_dataframe_for_skus[[sku_col_name,walkrate_col_name]]
    return walkrate_calculated_dataframe_for_skus




def calculate_net_elasticity_and_gross_internal(input_dataframe: pd.DataFrame, 
                                                walkrate_calculated_dataframe_for_skus: pd.DataFrame, 
                                                columns_to_group_pe_decom: list, 
                                                pd_decom_value_col_dict: Dict[str, Literal['mean', 'sum']], 
                                                merging_col_list: list, 
                                                gross_internal_col_name: str, 
                                                pe_col_name: str, 
                                                net_elasticity_col_name: str, 
                                                walkrate_col_name: str) -> pd.DataFrame:
    """
    Calculate net elasticity and gross internal based on provided data.

    Parameters:
        input_dataframe (pd.DataFrame): The input DataFrame.
        walkrate_calculated_dataframe_for_skus (pd.DataFrame): DataFrame containing SKUs and their calculated walk rates.
        columns_to_group_pe_decom (list): List of columns to group for Price Decomposition (PE Decom).
        pd_decom_value_col_dict (Dict[str, Literal['mean', 'sum']]): Dictionary specifying the columns for PE Decom and the aggregation type ('mean' or 'sum').
        merging_col_list (list): List of columns to merge on.
        gross_internal_col_name (str): Name of the column to store gross internal.
        pe_col_name (str): Name of the column containing Price Decomposition (PE Decom) values.
        net_elasticity_col_name (str): Name of the column to store net elasticity.
        walkrate_col_name (str): Name of the column containing walk rates.

    Returns:
        pd.DataFrame: DataFrame containing net elasticity and gross internal calculations.
    """
    grouped_data = input_dataframe.groupby(columns_to_group_pe_decom,as_index=False).agg(pd_decom_value_col_dict).reset_index()
    merged_input_and_walkrate_df=pd.merge(grouped_data,walkrate_calculated_dataframe_for_skus,on=merging_col_list,how='left')
    merged_input_and_walkrate_df[net_elasticity_col_name]=merged_input_and_walkrate_df[walkrate_col_name]*merged_input_and_walkrate_df[pe_col_name]
    merged_input_and_walkrate_df[gross_internal_col_name]=merged_input_and_walkrate_df[pe_col_name]-merged_input_and_walkrate_df[net_elasticity_col_name]
    return merged_input_and_walkrate_df
'''

    api_method_template='''
from pe_decom_calculation import filter_dataframe_based_on_col_values, filter_dataframe_on_time_period,group_input_dataframe,calculate_volume_mix,calculate_sm_grid_X_vol_mix,normalize_sm_grid_X_vol_mix,calculate_walkrate_of_skus_for_given_manufacturer,calculate_net_elasticity_and_gross_internal
import pandas as pd
def run_pe_decom_calculation():
    sm_grid=pd.read_csv('sm_grid.csv')
    input_file=pd.read_csv('input_data1.csv')
    input_data=input_file
    #input_file=filter_dataframe_based_on_col_values(input_file,{})
    filtered_file_on_time_pd=filter_dataframe_on_time_period(input_file,'year','month',0,4)
    filtered_file_on_time_pd = input_file.applymap(lambda x: x.replace(',', '') if isinstance(x, str) else x)
    grouped_df_on_sku=group_input_dataframe(filtered_file_on_time_pd,['description_material','manufacturer'],{'sales_value':'sum'})
    df_containing_vol_mix=calculate_volume_mix(grouped_df_on_sku,'sales_value','volume_mix')
    df_sm_and_vol_mix=calculate_sm_grid_X_vol_mix(sm_grid,df_containing_vol_mix,'description_material','manufacturer','volume_mix')
    normmalize_sm_df=normalize_sm_grid_X_vol_mix(df_sm_and_vol_mix)
    walkrate_calculated_df=calculate_walkrate_of_skus_for_given_manufacturer(normmalize_sm_df,'description_material','Softys','walkrate')
    net_easticity_df=calculate_net_elasticity_and_gross_internal(input_data,walkrate_calculated_df,['chain_final','description_material','marca','tipo','size','tier','category'],{'pe':'mean','ppp':'mean'},['description_material'],'gross_internal','pe','net_elasticity','walkrate')
    return net_easticity_df

print(run_pe_decom_calculation())
'''
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Write template to the specified path
    calculation_function_template_file = os.path.join(output_path, "pe_decom_calculation.py")
    with open(calculation_function_template_file, "w") as file:
        file.write(calculation_function_template)
    print(f"PVP PE DECOM Calculation template generated at: pe_decom_calculation")

    api_method_template_file = os.path.join(output_path, "view.py")
    if os.path.exists(api_method_template_file):
        with open(api_method_template_file, "a") as file:
            file.write(api_method_template)
    else:
        with open(api_method_template_file, "w") as file:
            file.write(api_method_template)
    print(f"PVP PE DECOM api template generated at: view")
