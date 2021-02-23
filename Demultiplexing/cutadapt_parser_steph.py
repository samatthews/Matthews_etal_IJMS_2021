import re
import pandas as pd
import argparse
import csv
import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups')




#### Parser program
def handle_program_options():
    """Parses the given options passed in at the command line."""
    parser = argparse.ArgumentParser(description='Takes cutadapt summary output and create a new files with indexes and passing reads information')
    parser.add_argument('-i', "--input", required=True,help='Takes cutadapt summary output, [REQUIRED]')
    parser.add_argument("-o", "--output", required=True,help="Output path for the new summary table. [REQUIRED]")
    return parser.parse_args()



def main():
	args = handle_program_options()

    # Importing file
	with open(args.input) as file:
		file_contents = file.read()
	file = file_contents.split('\n')
	file = file[3:]
#	df = pd.DataFrame(file)
	df = pd.DataFrame(file)

	# Patterns to capture
	Index_for = r'Command line parameters: -G (\w+)'
	Index_rev = r'-g (\w+)'
	Passing_filters_Nbr = r'Pairs written \(passing filters\):\s+ (\d+)'
	Passing_filters_pct = r'Pairs written \(passing filters\):.*\((\d+.\d+)'
	# Capturing patterns
	inFW = df[df[0].str.contains(Index_for)].values.tolist()
	inRV = df[df[0].str.contains(Index_rev)].values.tolist()
	PNbr = df[df[0].str.contains(Passing_filters_Nbr)].values.tolist()
	PPct = df[df[0].str.contains(Passing_filters_pct)].values.tolist()
#	print(inFW)
#	print(inRV)
#	print(PNbr)


#data = {'row_1': [3, 2, 1, 0], 'row_2': ['a', 'b', 'c', 'd']}
#pd.DataFrame.from_dict(data, orient='index')

	a = {'Index_forward': inFW, 'Index_revers': inRV, 'Passing_reads_Nbr': PNbr, 'Passing_reads_Pct': PPct}
	new_df = pd.DataFrame.from_dict(a, orient='index')
#	print(new_df)
	new_df = new_df.transpose()
#	print(new_df)
#	print(a)
#	new_df = df.transpose()
#	new_df.head()
#	print(new_df)

    # Changing series into strings
	new_df.Index_forward= new_df.Index_forward.astype(str)
	new_df.Index_revers= new_df.Index_revers.astype(str)
	new_df.Passing_reads_Nbr= new_df.Passing_reads_Nbr.astype(str)
	new_df.Passing_reads_Pct= new_df.Passing_reads_Pct.astype(str)

	# Removing undesired characters
	new_df.Index_forward.replace(regex=True,inplace=True,to_replace=r'Command line parameters: -g ',value=r'')
	new_df.Index_forward.replace(regex=True,inplace=True,to_replace=r"\[",value=r'')
	new_df.Index_forward.replace(regex=True,inplace=True,to_replace=r'\]',value=r'')
	new_df.Index_forward.replace(regex=True,inplace=True,to_replace=r"\'",value=r'')


	new_df.Index_revers.replace(regex=True,inplace=True,to_replace=r'-G ',value=r'')
	new_df['Filename'] = new_df['Index_revers'] # Creating new column with the filename
	new_df.Index_revers.replace(regex=True,inplace=True,to_replace=r'-o .*',value=r'')
	new_df.Index_revers.replace(regex=True,inplace=True,to_replace=r'\[',value=r'')
	new_df.Index_revers.replace(regex=True,inplace=True,to_replace=r"\'",value=r'')

	new_df.Passing_reads_Nbr.replace(regex=True,inplace=True,to_replace=r'Pairs written \(passing filters\):\s+ ',value=r'')
	new_df.Passing_reads_Nbr.replace(regex=True,inplace=True,to_replace=r'\[',value=r'')
	new_df.Passing_reads_Nbr.replace(regex=True,inplace=True,to_replace=r'\]',value=r'')
	new_df.Passing_reads_Nbr.replace(regex=True,inplace=True,to_replace=r' .*',value=r'')
	new_df.Passing_reads_Nbr.replace(regex=True,inplace=True,to_replace=r"\'",value=r'')

	new_df.Passing_reads_Pct.replace(regex=True,inplace=True,to_replace=r'Pairs written \(passing filters\):.*\ ',value=r'')
	new_df.Passing_reads_Pct.replace(regex=True,inplace=True,to_replace=r"\'",value=r'')
	new_df.Passing_reads_Pct.replace(regex=True,inplace=True,to_replace=r'\[',value=r'')
	new_df.Passing_reads_Pct.replace(regex=True,inplace=True,to_replace=r'\]',value=r'')
	new_df.Passing_reads_Pct.replace(regex=True,inplace=True,to_replace=r'\(',value=r'')
	new_df.Passing_reads_Pct.replace(regex=True,inplace=True,to_replace=r'\%\)',value=r'')

	new_df.Filename.replace(regex=True,inplace=True,to_replace=r'^.*Results_X\/',value=r'')
	new_df.Filename.replace(regex=True,inplace=True,to_replace=r'\/.*',value=r'')


	# Transforming string into float for the percentage column
	new_df.Passing_reads_Pct= new_df.Passing_reads_Pct.astype(float)

	# Sorting table according to the percentage value
	new_df = new_df.sort_values(by=['Passing_reads_Pct'],ascending=False)

	# Adding a column with the filename
	#new_df['File_name'] = args.input
	#print(args.input)

	# Writing the table to csv
	new_df.to_csv(args.output,sep=",",index=False)


if __name__ == '__main__':
    main()
