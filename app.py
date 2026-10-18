from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary storage
expenses = []
budget = 20000.0
next_id = 1


@app.route("/", methods=["GET", "POST"])
def index():
    global budget, next_id

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        date = request.form.get("date", "").strip()

        try:
            amount = float(request.form.get("amount", "0"))

            if title and category and date and amount > 0:
                expenses.append({
                    "id": next_id,
                    "title": title,
                    "category": category,
                    "date": date,
                    "amount": amount
                })
                next_id += 1
        except ValueError:
            pass

        return redirect(url_for("index"))

    total = sum(e["amount"] for e in expenses)

    category_totals = {}
    for expense in expenses:
        category = expense["category"]
        category_totals[category] = (
            category_totals.get(category, 0) + expense["amount"]
        )

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        budget=budget,
        remaining=budget - total,
        expense_count=len(expenses),
        category_totals=category_totals
    )


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    global expenses
    expenses = [e for e in expenses if e["id"] != expense_id]
    return redirect(url_for("index"))


@app.route("/set-budget", methods=["POST"])
def set_budget():
    global budget

    try:
        new_budget = float(request.form.get("budget", "0"))
        if new_budget > 0:
            budget = new_budget
    except ValueError:
        pass

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
