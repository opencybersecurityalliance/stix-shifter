class JSONMergeError(Exception):
	def __init__(self, message, value=None, strategy_name=None):
		self.message = message
		self.value = value
		self.strategy_name = strategy_name

	def __str__(self):
		r = self.message

		try:
			ref = self.value.ref
		except:
			ref = None

		if ref is not None:
			r = "%s: %s" % (r, ref)

		if self.strategy_name is not None:
			r = "'%s' merge strategy: %s" % (self.strategy_name, r)

		return r

class BaseInstanceError(JSONMergeError): pass
class HeadInstanceError(JSONMergeError): pass
class SchemaError(JSONMergeError): pass
