class Category:
	def __init__(self, name):
		self.name = name
		self.ledger = []

	# Appends a "amount" and "description" to ledger list
	def deposit(self, amount, description = ''):
		self.ledger.append({"amount": amount, "description": description})

	def withdraw(self, amount, description = ''):
		if self.check_funds(amount):
			self.ledger.append({"amount": -amount, "description": description})
			return True
		else:
			return False

	# Calculates balance based on ledger list "amount" entries
	def get_balance(self):
		balance = 0
		for x in self.ledger:
			balance += x['amount']
		return balance

	# Creates 2 entries on ledger, 1 as withdraw to the category where the transfer comes from
	# and 1 as deposit on the category where the amount goes to
	def transfer(self, amount, category):
		if self.check_funds(amount):
			self.withdraw(amount, f'Transfer to {category.name}')
			category.deposit(amount, f'Transfer from {self.name}')
			return True
		else:
			return False

	# Check if "amount" can be removed from balance, considering balance can't be negative
	def check_funds(self, amount):
		if amount > self.get_balance():
			return False
		else:
			return True

	def __str__(self):
		title = f"{self.name:*^30}\n"
		items = ""
		total = 0
		for i in range(len(self.ledger)):
			items += f"{self.ledger[i]['description'][0:23]:23}" + \
			f"{self.ledger[i]['amount']:>7.2f}" + '\n'
			total += self.ledger[i]['amount']

		output = title + items + "Total: " + str(total)
		return output

def create_spend_chart(categories):
	category_names = []
	spent = []
	spent_percentages = []

	# Separates spent 'amounts' and calculates spent %
	# rounded to the nearest 10
	for category in categories:
		total = 0
		for item in category.ledger:
			if item['amount'] < 0:
				total -= item['amount']
		spent.append(round(total, 2))
		category_names.append(category.name)

	for amount in spent:
		spent_percentages.append(round(amount / sum(spent), 2)*100)

	graph = "Percentage spent by category\n"

	labels = range(100, -10, -10)

	# Adds the 'o' characters to the graph, displaing percentage
	for label in labels:
		graph += str(label).rjust(3) + "| "
		for percent in spent_percentages:
			if percent >= label:
				graph += "o  "
			else:
				graph += "   "
		graph += "\n"

	graph += "    ----" + ("---" * (len(category_names) - 1))
	graph += "\n     "

	longest_name_length = 0

	for name in category_names:
		if longest_name_length < len(name):
			longest_name_length = len(name)

	for i in range(longest_name_length):
		for name in category_names:
			if len(name) > i:
				graph += name[i] + "  "
			else:
				graph += "   "
		if i < longest_name_length-1:
			graph += "\n     "

	return(graph)
