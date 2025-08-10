import streamlit as st
import pandas as pd
from datetime import date
import uuid

st.set_page_config(page_title="GL Game - Oracle EBS R12 (Demo)", layout="wide")

if "coa" not in st.session_state:
    # default Chart of Accounts (segments)
    st.session_state.coa = {
        "Company": ["01 - MainCo", "02 - Subsidiary"],
        "Department": {"01 - MainCo": ["01 - Finance", "02 - HR"], "02 - Subsidiary": ["01 - Sales"]},
        "Account": ["1000 - Cash", "2000 - Payables", "4000 - Revenue", "5000 - Expense"]
    }

if "users" not in st.session_state:
    # simple hierarchical security: user -> allowed companies
    st.session_state.users = {"admin": {"password":"admin","companies":["01 - MainCo","02 - Subsidiary"]},
                              "finance_user": {"password":"fin","companies":["01 - MainCo"]}}

if "ledger" not in st.session_state:
    st.session_state.ledger = []

st.title("🎮 GL Game — Oracle EBS R12 (Mini Demo)")

with st.expander("1) Setup - 4C (Chart of Accounts, Calendar, Currency, Convention)"):
    st.subheader("Chart of Accounts (COA)")
    coa = st.session_state.coa
    col1, col2 = st.columns(2)
    with col1:
        st.write("Companies (Independent segment)")
        for c in coa["Company"]:
            st.write("-", c)
        newc = st.text_input("Add Company (format: '03 - NewCo')", key="new_company")
        if st.button("Add Company"):
            if newc:
                coa["Company"].append(newc)
                coa["Department"][newc] = []
                st.success(f"Added {newc}")
    with col2:
        st.write("Departments (dependent on Company)")
        comp = st.selectbox("Choose Company to view/edit Departments", coa["Company"], key="select_company")
        deps = coa["Department"].get(comp, [])
        for d in deps:
            st.write("-", d)
        newd = st.text_input("Add Department (format: '03 - R&D')", key="new_dept")
        if st.button("Add Department"):
            if newd:
                coa["Department"].setdefault(comp, []).append(newd)
                st.success(f"Added {newd} under {comp}")
    st.write("Accounts:")
    st.write(coa["Account"])
    newacc = st.text_input("Add Account (format: '6000 - New Account')", key="new_acc")
    if st.button("Add Account"):
        if newacc:
            coa["Account"].append(newacc)
            st.success(f"Added account {newacc}")

with st.expander("2) Login / Hierarchical Security"):
    st.write("A simple login to simulate Hierarchical Security.")
    user = st.selectbox("User", list(st.session_state.users.keys()))
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if pwd == st.session_state.users[user]["password"]:
            st.session_state.current_user = user
            st.success(f"Logged in as {user}")
        else:
            st.error("Wrong password")

if "current_user" in st.session_state:
    st.markdown(f"**Current User:** `{st.session_state.current_user}` — allowed companies: {st.session_state.users[st.session_state.current_user]['companies']}")

    with st.expander("3) Post Journal Entry (Play Mode)"):
        st.subheader("Create Journal Entry")
        allowed = st.session_state.users[st.session_state.current_user]["companies"]
        company = st.selectbox("Company (Independent)", allowed)
        department = st.selectbox("Department (Dependent)", st.session_state.coa["Department"].get(company, []))
        account = st.selectbox("Account", st.session_state.coa["Account"])
        jdate = st.date_input("Date", value=date.today())
        desc = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        side = st.selectbox("Side", ["Debit", "Credit"])
        if st.button("Post Entry"):
            entry = {
                "id": str(uuid.uuid4())[:8],
                "user": st.session_state.current_user,
                "company": company,
                "department": department,
                "account": account,
                "date": jdate.isoformat(),
                "description": desc,
                "debit": amount if side == "Debit" else 0.0,
                "credit": amount if side == "Credit" else 0.0
            }
            st.session_state.ledger.append(entry)
            st.success("Posted ✔️")

    with st.expander("4) View Ledger & Reports"):
        df = pd.DataFrame(st.session_state.ledger)
        if df.empty:
            st.info("No entries yet. Post some entries in Play Mode.")
        else:
            df_display = df.copy()
            df_display["date"] = pd.to_datetime(df_display["date"]).dt.date
            st.dataframe(df_display)
            # Trial balance by account
            tb = df.groupby("account").agg({"debit":"sum","credit":"sum"}).reset_index()
            tb["balance"] = tb["debit"] - tb["credit"]
            st.subheader("Trial Balance (by Account)")
            st.table(tb)

    with st.expander("5) Admin - Manage Users (only admin)"):
        if st.session_state.current_user == "admin":
            st.write("Add a user with allowed companies (comma separated)")
            new_u = st.text_input("Username")
            new_p = st.text_input("Password")
            new_companies = st.text_input("Allowed companies (comma separated)")
            if st.button("Create User"):
                if new_u and new_p:
                    st.session_state.users[new_u] = {"password": new_p, "companies": [c.strip() for c in new_companies.split(",") if c.strip()]}
                    st.success(f"User {new_u} created")
        else:
            st.write("Only admin can manage users.")

st.write("---")
st.caption("This is a simplified demo for learning GL concepts: independent/dependent segments, hierarchical security and the 4C. Not for production.")