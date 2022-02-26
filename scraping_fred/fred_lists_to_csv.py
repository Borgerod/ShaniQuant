import pandas as pd

PATH= r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_ticker_list\\'

fred_list_name = ['GDP_QUATERLY', 'Currency_in_Circulation_WEEKLY', 'Unemployment_Rate', 'Volatility_Index', '10Y_Breakeven_Inflation_Rate', 'Interest_Rates_Discount_Rate_US', 'Market_Yield_US_Treasury_Securities_10Y_Constant_Maturity', 'High_Yield_Index_Option_Adjusted_Spread_US', 'High_Yield_Index_Emerging_Markets_Option_Adjusted_Spread', 'High_Yield_Index_Effective_Yield_US', 'Moodys_Seasoned_Aaa_Corporate_Bond_YieldProducer_Price_Index_byIndustry_Total_Manufacturing', 'Producer_Price_Index_byIndustry_General_Freight_Trucking_longDistance', 'Producer_Price_Index_byIndustry_Truck_Transportation', 'Producer_Price_Index_byIndustry_Deep_Sea_Transportation', 'Producer_Price_Index_Finished_Consumer_Foods_Global', 'Consumer_Price_Index_Fuel_Electricity_US', 'Consumer_Price_Index_Fuel_Electricity_EU', 'Harmonized_Consumer_Price_Index_Electricity_EU', 'Producer_Price_byIndustry_Index_Rubber_Plastic', 'Producer_Price_byIndustry_Index_Rasins_Plastic', 'Producer_Price_byIndustry_Index_telecom_manufacturing', 'Producer_Price_Index_byIndustry_Audio_Video_Equipment_Manufactoring', 'Producer_Price_Index_byIndustry_Printed_Circuit_Assembly_Manufactoring', 'Producer_Price_Index_byIndustry_Semiconductor_Electronic_Component_Manufactoring', 'Producer_Price_Index_byIndustry_Semiconductors_Related_Device_Manufactoring', 'Import_Price_Index_byOrigin_Semiconductor_Electronic_Component_Manufactoring', 'Industrial_Production_electronic_components', 'Producer_Price_Index_byIndustry_Electrical_Equipment_Manufactoring', 'Producer_Price_Index_byIndustry_computer_Manufactoring', 'Producer_Price_Index_byIndustry_Cement_Product_Manufactoring', 'Producer_Price_Index_byIndustry_Building_Material_Manufactoring', 'Producer_Price_Index_byIndustry_Chemical_Manufactoring', 'Producer_Price_Index_byIndustry_glass_Manufactoring', 'Producer_Price_Index_byIndustry_Gypsum_Manufactoring', 'Producer_Price_Index_byIndustry_Aerospace_products_Manufactoring', 'Producer_Price_Index_byIndustry_Pharmaceutical_Manufactoring', 'Producer_Price_Index_byIndustry_Medical_Equipment_Manufactoring', 'Producer_Price_Index_byIndustry_industrial_machinery_Manufactoring', 'Producer_Price_Index_byIndustry_Metal_Pipe_Manufactoring', 'Producer_Price_Index_byIndustry_aluminium_sheet_Manufactoring', 'Producer_Price_Index_byIndustry_new_industrial_buildings_construction', 'Producer_Price_Index_byIndustry_TOTAL_mining_industies', 'Producer_Price_Index_byIndustry_Motor_Viechle_Metal_Stamping', 'Producer_Price_Index_byIndustry_Sheet_Metal_Work_Manufactoring', 'Producer_Price_Index_byIndustry_Primary_metal_Manufactoring', 'Producer_Price_Index_byIndustry_Iron_Steel_Products_Manufactoring', 'Producer_Price_Index_byIndustry_TOTAL_Manufactoring_industries', 'Producer_Price_Index_byIndustry_TOTAL_wholesale_industries', 'Producer_Price_Index_byIndustry_TOTAL_Retail_industries', 'Producer_Price_Index_byIndustry_TOTAL_Trade_industries', 'Producer_Price_Index_byIndustry_TOTAL_industrial_activities_EU', 'Producer_Price_Index_byIndustry_GROWTH_RATE_industrial_activities_EU']


# [
# 	"GDP_QUATERLY", "Currency_in_Circulation_WEEKLY", "Unemployment_Rate", "Volatility_Index", "10Y_Breakeven_Inflation_Rate", "Interest_Rates_Discount_Rate_US", "Interest_Rate_Excess_Reserves", 
# 	"Market_Yield_US_Treasury_Securities_10Y_Constant_Maturity" ,"High_Yield_Index_Option_Adjusted_Spread_US", "High_Yield_Index_Emerging_Markets_Option_Adjusted_Spread", "High_Yield_Index_Effective_Yield_US", 
# 	"Moodys_Seasoned_Aaa_Corporate_Bond_Yield"

# 	"Producer_Price_Index_byIndustry_Total_Manufacturing", "Producer_Price_Index_byIndustry_General_Freight_Trucking_longDistance", "Producer_Price_Index_byIndustry_Truck_Transportation", "Producer_Price_Index_byIndustry_Deep_Sea_Transportation",
# 	"Producer_Price_Index_Finished_Consumer_Foods_Global",  "Consumer_Price_Index_Fuel_Electricity_US", "Consumer_Price_Index_Fuel_Electricity_EU",
# 	"Harmonized_Consumer_Price_Index_Electricity_EU", "Producer_Price_byIndustry_Index_Rubber_Plastic", "Producer_Price_byIndustry_Index_Rasins_Plastic",
# 	"Producer_Price_byIndustry_Index_telecom_manufacturing", "Producer_Price_Index_byIndustry_Audio_Video_Equipment_Manufactoring", 


# 	"Producer_Price_Index_byIndustry_Printed_Circuit_Assembly_Manufactoring", "Producer_Price_Index_byIndustry_Semiconductor_Electronic_Component_Manufactoring", "Producer_Price_Index_byIndustry_Semiconductors_Related_Device_Manufactoring", 
# 	"Import_Price_Index_byOrigin_Semiconductor_Electronic_Component_Manufactoring", "Industrial_Production_electronic_components", "Producer_Price_Index_byIndustry_Electrical_Equipment_Manufactoring", "Producer_Price_Index_byIndustry_computer_Manufactoring",
# 	"Producer_Price_Index_byIndustry_Cement_Product_Manufactoring", "Producer_Price_Index_byIndustry_Building_Material_Manufactoring", "Producer_Price_Index_byIndustry_Chemical_Manufactoring", "Producer_Price_Index_byIndustry_glass_Manufactoring", "Producer_Price_Index_byIndustry_Gypsum_Manufactoring", 
	
# 	"Producer_Price_Index_byIndustry_Aerospace_products_Manufactoring", "Producer_Price_Index_byIndustry_Pharmaceutical_Manufactoring", "Producer_Price_Index_byIndustry_Medical_Equipment_Manufactoring", "Producer_Price_Index_byIndustry_industrial_machinery_Manufactoring", 
# 	"Producer_Price_Index_byIndustry_Metal_Pipe_Manufactoring", "Producer_Price_Index_byIndustry_aluminium_sheet_Manufactoring", "Producer_Price_Index_byIndustry_new_industrial_buildings_construction", "Producer_Price_Index_byIndustry_TOTAL_mining_industies",
# 	"Producer_Price_Index_byIndustry_Motor_Viechle_Metal_Stamping", "Producer_Price_Index_byIndustry_Sheet_Metal_Work_Manufactoring", "Producer_Price_Index_byIndustry_Primary_metal_Manufactoring", "Producer_Price_Index_byIndustry_Iron_Steel_Products_Manufactoring", 
# 	"Producer_Price_Index_byIndustry_TOTAL_Manufactoring_industries", "Producer_Price_Index_byIndustry_TOTAL_wholesale_industries", "Producer_Price_Index_byIndustry_TOTAL_Retail_industries", "Producer_Price_Index_byIndustry_TOTAL_Trade_industries", 
# 	"Producer_Price_Index_byIndustry_TOTAL_industrial_activities_EU", "Producer_Price_Index_byIndustry_GROWTH_RATE_industrial_activities_EU",

# 	]

fred_list = ['GDP', 'WCURCIR', 'UNRATE', 'VIXCLS', 'T10YIE', 'INTDSRUSM193N', 'DGS10', 'BAMLH0A0HYM2', 'BAMLEMHBHYCRPIOAS', 'BAMLH0A0HYM2EY', 'AAA', 'PCUOMFGOMFG', 'PCU484121484121', 'PCU484484', 'PCU483111483111', 'WPSFD4111', 'CPGREN01USM657N', 'EA19CPGREN01GPM', 'CP0451EU28M086NEST', 'WPU072B01', 'PCU325211325211', 'PCU3342103342104', 'PCU3343103343105', 'PCU3344183344189', 'PCU33443344', 'PCU334413334413A', 'COINDUSZ3344', 'PCU3353133531', 'PCU334334', 'PCU32733273', 'PCU44414441', 'PCU325325', 'PCU3272132721', 'PCU3274203274201', 'PCU3364133641', 'PCU325412325412', 'PCU33913391', 'PCU33323332', 'PCU3312103312100', 'PCU3313153313150', 'PCU236211236211', 'PCUOMINOMIN', 'PCU336370336370', 'PCU332322332322', 'PCU331331', 'WPU101', 'PCUOMFGOMFG', 'PCUAWHLTRAWHLTR', 'PCUARETTRARETTR', 'PCUATRADEATRADE', 'PIEATI01EZM661N', 'EA19PIEATI01GYM']

# [
# 	"GDP", "WCURCIR", "UNRATE","VIX", "T10YIE", "INTDSRUSM193N", "IOER", 
# 	"DGS10", "BAMLH0A0HYM2", "BAMLEMHBHYCRPIOAS", "BAMLH0A0HYM2EY", 
# 	"AAA",

# 	"PCUOMFGOMFG", "PCU484121484121", "PCU484484", "PCU483111483111", 
# 	"WPSFD4111", "CPGREN01USM657N", "EA19CPGREN01GPM",
# 	"CP0451EU28M086NEST", "WPU072B01", "PCU325211325211",
# 	"PCU3342103342104", "PCU3343103343105",


# 	"PCU3344183344189", "PCU33443344", "PCU334413334413A", 
# 	"COINDUSZ3344", "IPB53122S","PCU3353133531", "PCU334334"
# 	"PCU32733273", "PCU44414441", "PCU325325", "PCU3272132721", "PCU3274203274201",

# 	"PCU3364133641", "PCU325412325412", "PCU33913391", "PCU33323332", 
# 	"PCU3312103312100", "PCU3313153313150", "PCU236211236211", "PCUOMINOMIN", 
# 	"PCU336370336370", "PCU332322332322", "PCU331331", "WPU101", 
# 	"PCUOMFGOMFG", "PCUAWHLTRAWHLTR", "PCUARETTRARETTR", "PCUATRADEATRADE", 
# 	"PIEATI01EZM661N", "EA19PIEATI01GYM",

# 	]

fred_list_name= pd.DataFrame(fred_list_name)
fred_list=pd.DataFrame(fred_list)
fred_list_name.columns=['fred_list_name']
fred_list.columns=['fred_list']
fred_list_name.to_csv(PATH+"fred_list_name.csv", index=False, header=True)
fred_list.to_csv(PATH+"fred_list.csv", index=False, header=True)
