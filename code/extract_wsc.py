from get_cc_data import get_cost_data
import sys



def extractWsc ():
    """
    Using lists of data from get_cost_data function, parses through names to determine
    ONLY water science centers and respective data. A bit wonky due to the lack of naming convention
    in the data source file...
    """
    ##importing data
    alloc_org, cc_name, dir_cc, reimburse_cc, reimburse_fac, reimburse_bur, reimburse_comp = get_cost_data('../data/data.txt')
    #alloc_org, cc_name, dir_cc, reimburse_cc, reimburse_fac, reimburse_bur, reimburse_comp = get_cost_data(sys.argv[1])


    ##https://stackoverflow.com/questions/4843158/check-if-a-python-list-item-contains-a-string-inside-another-string
    ## This is slick. Set strings to match and find them in any string.
    matchers = ['Water Sci', 'WATER SCI']
    matching = [s for s in cc_name if any (xs in s for xs in matchers)]

    fld_ofc = ['OFFICE', 'OFC', 'OFFIC', '"', ' FO', '- CT']

    wsc = [ctr for ctr in matching if not any(ofc in ctr for ofc in fld_ofc)]

    indices = []

    for i in range(len(alloc_org)):
        if cc_name[i] in wsc:
            indices.append(i)

    #print(indices)

    allocOrg = []
    ccName = []
    dirCC = []
    reimburseCC = []
    reimburseFac = []
    reimburseBur = []
    reimburseComp = []

    #raw_lists = [ alloc
    #plot_lists= [ allocOrg, ccName, dirCC, reimburseCC, reimburseFac, reimburseBur, reimburseComp ]

    for index in indices:
        allocOrg.append(alloc_org[index])
        ccName.append(cc_name[index])
        dirCC.append(dir_cc[index])
        reimburseCC.append(reimburse_cc[index])
        reimburseFac.append(reimburse_fac[index])
        reimburseBur.append(reimburse_bur[index])
        reimburseComp.append(reimburse_comp[index])

    return allocOrg, ccName, dirCC, reimburseCC, reimburseFac, reimburseBur, reimburseComp


    
if __name__ == "__main__":

    extractWsc() 
