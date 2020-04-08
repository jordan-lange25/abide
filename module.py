#Engine code
def splitter2(transdf,pldf): 
    accountslist=[]
    for i in pldf['Account']: 
        if i not in ("Revenue","COGS","GrossMargin","Profit"): 
            accountslist.append(i)
        else: 
            continue
    for account in accountslist:
        valuelist=[]
        totallist=[]
        totalrev=transdf['Revenue'].sum()
        for revval in transdf["Revenue"]:
            valuelist.append(pldf[pldf['Account']==str(account)]["Amount"].values[0]*(revval/totalrev))
            totallist.append(pldf[pldf['Account']==str(account)]["Amount"].values[0])
        transdf[str(account)+"AC"]=valuelist
    return transdf
    
