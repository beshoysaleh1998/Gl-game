GL Game - Oracle EBS R12 (Mini Demo)
-----------------------------------

This is a simple Streamlit app that simulates key GL concepts you learned:
- 4C: Chart of Accounts, Calendar, Currency, Convention (we focus on COA here)
- Independent vs Dependent segments (Company -> Department)
- Hierarchical security: simple users limited to certain companies
- Post journal entries (Debit/Credit) and view a simple trial balance

Requirements:
- Python 3.10+
- streamlit
- pandas

Run locally:
1. pip install streamlit pandas
2. streamlit run gl_game_app.py

Files included:
- gl_game_app.py : the Streamlit app
- sample_ledger.csv : a small sample dataset
- README.txt : this file