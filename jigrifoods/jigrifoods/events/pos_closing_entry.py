import frappe
from frappe.utils import flt
from frappe.model.document import Document

def custom_on_submit(doc, method):
    if doc.custom_pos_expenses:
        abbr = get_company_abbr()
        je = frappe.new_doc("Journal Entry")
        je.voucher_type = "Journal Entry"
        je.posting_date = doc.posting_date
        je.custom_pos_closing_entry = doc.name
   
        # Example debit entries
        for item in doc.custom_pos_expenses:
            je.append("accounts", {
                "account": item.account_name,   # Replace with actual account
                "debit_in_account_currency": item.amount,
                "user_remark": item.description
            })

        je.append("accounts", {
            "account": f"Cash - {abbr}",    # Replace with actual account
            "credit_in_account_currency": doc.custom_total_amount,
        })


        # Save and submit the Journal Entry
        je.save()
        je.submit()
        frappe.msgprint(f"Journal Entry {je.name} created and submitted.")

    if doc.custom_balance_amount > 0:
        abbr = get_company_abbr()
        je2 = frappe.new_doc("Journal Entry")
        je2.voucher_type = "Journal Entry"
        je2.posting_date = doc.posting_date
        je2.custom_pos_closing_entry = doc.name
   
        # Example debit entries
        for item in doc.custom_cash_in_entries:
            je2.append("accounts", {
                "account": item.account,    # Replace with actual account
                "credit_in_account_currency": item.amount,
                "user_remark": item.description
            })
        je2.append("accounts", {
            "account": f"Cash - {abbr}",   # Replace with actual account
            "debit_in_account_currency": doc.custom_total_cash_in_amount
        })

        # Save and submit the Journal Entry
        je2.save()
        je2.submit()
        frappe.msgprint(f"Journal Entry {je2.name} created and submitted.")


def get_company_abbr():
    """Get current company abbreviation"""
    company = frappe.defaults.get_user_default("Company") or frappe.defaults.get_global_default("company")
    
    if not company:
        return None
    
    return frappe.db.get_value("Company", company, "abbr")


def custom_validate(doc, method):
    set_cash_amount(doc)
    sum_cash_in_entries_amount(doc)
    sum_amount(doc)

def set_cash_amount(doc):
    """Get expected Cash amount from payment_reconciliation child table"""
    cash_amt = 0.0
    for row in doc.payment_reconciliation or []:
        if row.mode_of_payment == "Cash":
            cash_amt = flt(row.expected_amount)
            break
    doc.custom_cash_amt = cash_amt

def sum_amount(doc):
    """Calculate total expenses and balance amount"""
    custom_cash_amt = flt(doc.custom_cash_amt)
    total_expenses  = flt(sum(flt(r.amount) for r in doc.custom_pos_expenses or []))
    total_in        = flt(doc.custom_total_cash_in_amount)
    balance         = custom_cash_amt + total_in - total_expenses

    doc.custom_total_amount   = total_expenses
    doc.custom_balance_amount = balance

def sum_cash_in_entries_amount(doc):
    """Calculate total cash-in entries and balance amount"""
    total_in        = flt(sum(flt(r.amount) for r in doc.custom_cash_in_entries or []))
    custom_cash_amt = flt(doc.custom_cash_amt)
    total_expenses  = flt(sum(flt(r.amount) for r in doc.custom_pos_expenses or []))
    balance         = custom_cash_amt + total_in - total_expenses

    doc.custom_total_cash_in_amount = total_in
    doc.custom_balance_amount       = balance