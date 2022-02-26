
#____________________________EKSEMPEL DATAFRAME_______________________________#
	import pandas as pd
	df = pd.DataFrame({	'month': [1, 4, 7, 10],
						'year': [2012, 2014, 2013, 2014],
						'sale': [55, 40, 84, 31]}, index=[0,1,2,3])
#_____________________________________________________________________________#



# ___________________________MAKING DATAFRAMES________________________________#
	# Make an empty dataframe: 
		df=pd.DataFrame()
		'''
		OUTPUT:
							Empty DataFrame
							Columns: []
							Index: []
		'''

	# Make a dataframe from values: 
		df=pd.DataFrame({'month': ['january', 'april', 'july', 'october']})
		df=pd.DataFrame(['january', 'april', 'july', 'october'], columns=['month'])
		'''	
		#OUTPUT:
									     month
									0  january
									1    april
									2     july
									3  october
		'''

	# Make an dataframe from range: 
		df = pd.DataFrame({ 'month' : range(4)})

		'''	
		OUTPUT:
									   month
									0      0
									1      1
									2      2
									3      3
		'''

	# make dataframe with only index:
		index_df = pd.DataFrame(index=['january', 'april', 'july', 'october'])
		index_df = pd.DataFrame(index=[0,1,2,3,4])
		index_df = pd.DataFrame(index=range(4))
		'''	
		OUTPUT:
							Empty DataFrame
							Columns: []
							Index: [0, 1, 2, 3]
		'''



# ________________________________INDEX_______________________________________#
	# GIVE INDEX A NAME:
							df.index.name='month'
							'''
							OUTPUT:
											       month  year  sale
											month                   
											0          1  2012    55
											1          4  2014    40
											2          7  2013    84
											3         10  2014    31
							'''

	# SET COLUMN AS INDEX:
							df.set_index(['month'], inplace=True)
							'''	
							OUTPUT:		
												       year  sale
												month            
												1      2012    55
												4      2014    40
												7      2013    84
												10     2014    31
							'''

	# SET MULTIPLE COLUMNS AS INDEX
							df.set_index(['year', 'month'], inplace=True)
							'''
							OUTPUT:		
												            sale
												year month      
												2012 1        55
												2014 4        40
												2013 7        84
												2014 10       31
							'''

	# RESET INDEX (OLD INDEX BECOMES A COLUMN):
							df = df.reset_index()
							'''	
							OUTPUT:	
												month  year  sale        
											0	1      2012    55
											1	4      2014    40
											2	7      2013    84
											3	10     2014    31
							'''

	# RESET INDEX (OLD INDEX GETS DROPPED):
							df=df.reset_index(drop=True)
							'''	
							OUTPUT:		
											   year  sale        
											0  2012    55
											1  2014    40
											2  2013    84
											3  2014    31
							'''

	# SET INDEX FROM A LIST:
							# Alt 1)
							lst=['january', 'april', 'july', 'october']
							df = pd.DataFrame({'month': [1, 4, 7, 10],'year': [2012, 2014, 2013, 2014],'sale': [55, 40, 84, 31]}, index=lst)

							# Alt 2)
							df = pd.DataFrame({'month': [1, 4, 7, 10],'year': [2012, 2014, 2013, 2014],'sale': [55, 40, 84, 31]}, index=['january', 'april', 'july', 'october'])
							'''	
							OUTPUT:
												     month  year  sale
											january      1  2012    55
											april        4  2014    40
											july         7  2013    84
											october     10  2014    31
							'''

	# SET INDEX FROM A ANOTHER DATAFRAME'S COLUMN:
							index_df=pd.DataFrame(['january', 'april', 'july', 'october'], columns=['month'])
							df = pd.DataFrame({'month': [1, 4, 7, 10],'year': [2012, 2014, 2013, 2014],'sale': [55, 40, 84, 31]}, index=index_df['month'])
							print(df)
							'''
							OUTPUT:
											         month  year  sale
											month                     
											january      1  2012    55
											april        4  2014    40
											july         7  2013    84
											october     10  2014    31
							'''

	# SET INDEX FROM ANOTHER DATAFRAME'S INDEX:
							index_df = pd.DataFrame(index=['january', 'april', 'july', 'october'])
							df = pd.DataFrame({'month': [1, 4, 7, 10],'year': [2012, 2014, 2013, 2014],'sale': [55, 40, 84, 31]}, index=index_df.index)
							'''
							OUTPUT:
											         month  year  sale
											month                     
											january      1  2012    55
											april        4  2014    40
											july         7  2013    84
											october     10  2014    31
							'''



# ___________________________DISPLAY OPTIONS__________________________________#
	# alt 1)
	pd.set_option('display.max_columns', None)
	pd.set_option('display.max_row', None)
	pd.set_option('display.width', 200)

	# alt 2)
	pd.options.display.max_columns=None
	pd.options.display.max_rows=None
	pd.options.display.width=200
