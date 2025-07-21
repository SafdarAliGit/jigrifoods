frappe.ui.form.on("POS Closing Entry", {
    pos_opening_entry: function(frm) {
		setTimeout(() => {  // Wait 500ms before executing
		let cashAmount = 0;
        
        (frm.doc.payment_reconciliation || []).forEach(row => {
            if (row.mode_of_payment === "Cash") {
                cashAmount = flt(row.expected_amount);
            }
        });
        
        frm.set_value("custom_cash_amt", cashAmount);
        
        if (typeof sum_amount === "function") {
            sum_amount(frm);
        }
		}, 2000);  // 500ms = 0.5 seconds delay
    }
});

frappe.ui.form.on("Pos Expenses", {
    amount(frm) {
        sum_amount(frm);
    }
});

frappe.ui.form.on("Cash In Entries", {
    amount(frm) {
        sum_cash_in_entries_amount(frm);
    }
});

function sum_amount(frm) {
    const custom_cash_amt = flt(frm.doc.custom_cash_amt);
    const total_expenses = flt((frm.doc.custom_pos_expenses || [])
        .reduce((sum, r) => sum + flt(r.amount), 0));
    const total_in = flt(frm.doc.custom_total_cash_in_amount);
    const balance = custom_cash_amt + total_in - total_expenses;
    frm.set_value("custom_total_amount", total_expenses);
    frm.set_value("custom_balance_amount", balance);
}

function sum_cash_in_entries_amount(frm) {
    const total_in = flt((frm.doc.custom_cash_in_entries || [])
        .reduce((sum, r) => sum + flt(r.amount), 0));
    const custom_cash_amt = flt(frm.doc.custom_cash_amt);
    const total_expenses = flt(frm.doc.custom_total_amount);
    const balance = custom_cash_amt + total_in - total_expenses;
    frm.set_value("custom_total_cash_in_amount", total_in);
    frm.set_value("custom_balance_amount", balance);
}
