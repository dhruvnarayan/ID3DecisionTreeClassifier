from node import Node
import math


def ID3(examples, default):
	allAttr = list(examples[0].keys())
	allAttr.remove('Class')
	sub = {}
	last = len(allAttr) - 1  # index of target[Class]
	vals = [i['Class'] for i in examples]
	if not examples or len(allAttr) == 0:
		return Node(default)
	elif vals.count(vals[0]) == len(vals):
		return Node(vals[0])
	else:
		best = chooseAttr(allAttr, examples, allAttr[last])
		t = Node(best, {})
		best_v = values(allAttr, examples, best)
		for v in best_v:
			if v == '?':
				v = mode(examples, best)
			new_ex = newExample(examples, best, v)
			subtree = ID3(new_ex, mode(new_ex, 'Class'))
			sub.update({v: subtree})
			t.setChild(sub)
		return t


def mode(examples, target):
	freq = {}
	if len(examples) != 0:
		for j in examples:
			if j[target] in freq:
				freq[j[target]] += 1
			else:
				freq[j[target]] = 1

		return max(freq, key=freq.get)


def values(allAttr, examples, best):
	i = allAttr.index(best)
	vals = []
	for e in examples:
		if e[best] not in vals:
			vals.append(e[best])
	return vals


def newExample(examples, best, best_v):
	# remove best attribute from all elements of examples
	result = []

	for e in examples:
		if e[best] == best_v:
			copy = e.copy()
			del copy[best]
			result.append(copy)

	return result


def chooseAttr(allAttr, examples, target):
	best = allAttr[0]
	maxgain = 0
	new = 0.0
	for a in allAttr:
		if a != target:
			new = gain(examples, a, target)
		if new > maxgain:
			maxgain = new
			best = a
	return best


def entropy(examples, attr, target=None):
	# calculate entropy
	e = 0.0
	subset = []
	# calculate decision attribute entroy
	if target is None:
		values = [a[attr] for a in examples]  # store all attribute value
		count = {val: values.count(val) for val in values}

		for val in count.keys():
			p = float(count[val]) / len(values)
			e -= p * math.log(p, 2)

		return e

	else:
		values1 = [a[target] for a in examples]  # store all attribute value
		count1 = {val: values1.count(val) for val in values1}

		for val in count1.keys():
			p = float(count1[val]) / len(values1)
			for t in examples:
				if t[target] == val:
					subset.append(t)

			e += p * entropy(subset, attr)
		return e


def gain(examples, attr, target):
	# calculate information gain
	return entropy(examples, target) - entropy(examples, attr, target)


def prune(node, examples):
	if len(node.children) == 0:
		return

	if len(examples) == 0:
		node.children = {}
		node.label = mode(examples, 'Class')
		return

	parts = segment(examples, node.label)

	for child in node.children.keys():
		if child in parts.keys():
			prune(node.children[child], parts[child])
		else:
			prune(node.children[child], {})

	if can_prune(node, examples):
		node.children = {}
		node.label = mode(examples, 'Class')


def segment(examples, label):
	parts = {}

	for eg in examples:
		if not eg[label] in parts.keys():
			parts[eg[label]] = [eg]
		else:
			parts[eg[label]].append(eg)

	return parts


def can_prune(node, examples):
	if len(examples) == 0:
		return True

	flag = 0
	for eg in examples:
		if eg['Class'] == mode(examples, 'Class'):
			flag += 1

	if float(flag) / len(examples) >= test(node, examples):
		return True

	return False


def test(node, examples):
	"""
	Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
	of examples the tree classifies correctly).
	"""

	correct = 0
	total = 0

	for instance in examples:
		total += 1
		label = evaluate(node, instance)
		if label == instance['Class']:
			correct += 1

	return float(correct) / float(total)


def evaluate(node, example):
	"""
	Takes in a tree and one example.  Returns the Class value that the tree
	assigns to the example.
	"""
	nextNode = node
	while nextNode.getChild() != {}:
		templ = nextNode.getLabel()
		tempc = nextNode.getChild()
		if example[templ] in tempc:
			nextNode = tempc[example[templ]]
		else:
			# for cases not found, assign the first branch
			nextNode = tempc[list(tempc.keys())[0]]
	return nextNode.getLabel()
