frappe.ui.form.on("POS Closing Entry", {
	
	
});

frappe.ui.form.on("Pos Expenses", {
	amount: function(frm, cdt, cdn) {
		sum_amount(frm);
	}
});

function sum_amount(frm) {
	let total_amount = 0;
    let balance_amount = 0;
    
	frm.doc.custom_pos_expenses.forEach((row) => {
		total_amount += row.amount;
	});
	frm.set_value("custom_total_amount", total_amount);
    balance_amount = (total_amount || 0) - (frm.doc.net_total || 0);
    frm.set_value("custom_balance_amount", balance_amount);
}
	
