#script that parses P&L to transactions
import pandas as pd

transactiondata=pd.read_csv('transaction.csv',delimiter=',')
trans_df=pd.DataFrame(transactiondata)
pldata=pd.read_csv('pl.csv',delimiter=',')
pl_df=pd.DataFrame(pldata)


#split all columns in the P&L down to the line by revenue

print(pl_df['Revenue'])
