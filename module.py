#Engine code
import pandas as pd
import plotly.graph_objects as go

def splitter2(transfile,plfile):
    transactiondata=pd.read_csv(transfile,delimiter=',')
    transdf=pd.DataFrame(transactiondata)
    pldata=pd.read_csv(plfile,delimiter=',')
    pldf=pd.DataFrame(pldata)       
    accountslist=[]
    for i in pldf['Account']: 
        if i not in ("Revenue","COGS","GrossMargin","Profit"): 
            accountslist.append(i)
        else:
            continue
    transdf["GrossMargin"]=transdf['Revenue']-transdf['COGS']
    for account in accountslist:
        valuelist=[]
        totallist=[]
        totalrev=transdf['Revenue'].sum()
        for revval in transdf["Revenue"]:
            valuelist.append(round(pldf[pldf['Account']==str(account)]["Amount"].values[0]*(revval/totalrev),2))
            totallist.append(pldf[pldf['Account']==str(account)]["Amount"].values[0])
        transdf[str(account)+"AC"]=valuelist
    transdf["Profit"]=transdf['GrossMargin']-transdf.iloc[:,-len(accountslist):].sum(axis=1)
    return transdf

def filetotable(file): 
    fileupload=pd.read_csv(file,delimiter=",")
    fig = go.Figure(data=[go.Table(header=dict(values=list(fileupload.columns),
    line_color='black',
    fill_color='lightgreen',
    align='center'
        ),
    cells=dict(values=fileupload.transpose(),
    line_color='black',
    fill_color='white'
         )
        )
    ])
    return fig

#Group the data and display in a bar chart
def groupdata(file,group,sumfield): 
    upload=pd.read_csv(file,delimiter=',')
    df=pd.DataFrame(upload)
    productprofit=pd.DataFrame(df.groupby(str(group))[str(sumfield)].sum().reset_index().sort_values(str(sumfield),ascending=False))
    #ceate visualization
    fig = go.Figure(data=[
        go.Bar(name=str(group) + ' Profitability', x=productprofit[str(group)], y=productprofit[str(sumfield)]),
    ])
    # Change the bar mode
    fig.update_layout(
        title=str(group) + ' Profitability',
        xaxis=dict(
            title= str(group),
            tickfont_size=14
        ),
        yaxis=dict(
        title='USD Net Profit'
        ),
        barmode='group'

    )
    return fig

#Show the P&L in a waterfall
#functionalize
#Show the P&L in a waterfall
#functionalize
def plwaterfall(plfile):
    pl_df=pd.read_csv(plfile,delimiter=',')
    measurelist=[]
    amountlist=[]
    allaccountslist=list(pl_df['Account'])
    allaccountslist
    for i in allaccountslist: 
        if i in ("GrossMargin","Profit"):
            measurelist.append('total')
            amountlist.append(pl_df[pl_df['Account']==i]['Amount'].values[0])
        elif i in ("Revenue"):
            measurelist.append('relative')
            amountlist.append(pl_df[pl_df['Account']==i]['Amount'].values[0])
        else: 
            measurelist.append('relative')
            amountlist.append(-pl_df[pl_df['Account']==i]['Amount'].values[0])
    fig = go.Figure(go.Waterfall(
        name = "20", orientation = "v",
        measure = measurelist,
        x=allaccountslist,
        #textposition = "outside",
        #text = ["+60", "+80", "", "-40", "-20", "Total"],
        y = amountlist,
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))

    fig.update_layout(
            title = "Profit and loss statement 2019",
            showlegend = True
    )

    return fig