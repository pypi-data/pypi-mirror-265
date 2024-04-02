from finance_mauritius.mcb import MCB

MCB.process_csv('mcb.CSV')
print(MCB.csv_money_in())
print(MCB.csv_money_out())