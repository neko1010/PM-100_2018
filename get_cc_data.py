import sys

def get_cost_data(datafile):

	##Reading file
	#datafile = sys.argv[1]#"C:\\Users\\nkolarik\\Desktop\\Desktop\\d3\\visual\\sample.txt"


	## Empties for data
	alloc_org = []
	cc_name = []
	dir_cc = []
	reimburse_cc = []
	reimburse_fac = []
	reimburse_bur = []
	reimburse_comp = []


	with open(datafile) as f:
	    row_reader = f.readlines()
	    
	    
	    for row in row_reader[1:]:
	        row_vals= row.split("\t")    
	        
	       	## Checking for empty allocation organizations
	       	## came from a pivot table in excel, so empty values 
	       	## indicate same alloc_org as preceding value

	        if row_vals[0] == "":
	            alloc_org.append(alloc_org[-1])
	        else:
	            alloc_org.append(row_vals[0])
	        
			## populating lists with remaining data
	        cc_name.append(row_vals[1])
	        dir_cc.append(float(row_vals[2]))
	        reimburse_cc.append(float(row_vals[3]))
	        reimburse_fac.append(float(row_vals[4]))
	        reimburse_bur.append(row_vals[5])
	        reimburse_comp.append(float(row_vals[6]))

	#print(alloc_org, cc_name, dir_cc, reimburse_cc, reimburse_fac, reimburse_bur, reimburse_comp)
	return alloc_org, cc_name, dir_cc, reimburse_cc, reimburse_fac, reimburse_bur, reimburse_comp

if __name__ == "__main__":

	get_cost_data(sys.argv[1])
