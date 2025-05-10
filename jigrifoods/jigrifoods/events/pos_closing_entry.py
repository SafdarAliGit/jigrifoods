import frappe
from frappe.model.document import Document

def custom_on_submit(doc, method):
    if doc.custom_pos_expenses:
        je = frappe.new_doc("Journal Entry")
        je.voucher_type = "Journal Entry"
        je.posting_date = frappe.utils.nowdate()
        je.custom_pos_closing_entry = doc.name
   
        # Example debit entries
        for item in doc.custom_pos_expenses:
            je.append("accounts", {
                "account": item.account_name,   # Replace with actual account
                "debit_in_account_currency": item.amount,
                "user_remark": item.description
            })

        je.append("accounts", {
            "account": "Cash - JF",    # Replace with actual account
            "credit_in_account_currency": doc.custom_total_amount,
        })


        # Save and submit the Journal Entry
        je.save()
        je.submit()
        frappe.msgprint(f"Journal Entry {je.name} created and submitted.")

        return je.name
