import pandas as pd

#index_col to say the column labels are first (not data)
df = pd.read_csv('rvu_credit_dataset.csv', index_col=0)

#add admin values as the 3rd column
admin_values = 1 - df['edu'] - df['teach'] - df['res'] - df['strat']
df.insert(2, 'admin', admin_values)

#move position titles to the first column
cols = df.columns.tolist()
cols = [cols[-1]] + cols[:-1]
df = df[cols]

#start with a vertical line
col_format = "|"

#title and cred columns should be right-justified, all others centered
for i in df.columns:
    if i=="title" or i=="cred":
        col_format = col_format + "r|"        
    else:
        col_format = col_format + "c|"

#notes on what I need to use if everything goes to df.style.to_latex()
#df = df.reset_index(drop=True)

latex_output = df.to_latex(column_format = col_format,
                           index=False,
                           bold_rows=True, 
                           escape=True,
                           caption="wRVUs for responsibilities",
                           label="tab:sample_table")

index = 13
substring = '[H]'
latex_output = latex_output[:index] + substring + latex_output[index:]


print(latex_output)
with open('output.tex', 'w') as file:
    file.write(latex_output)














