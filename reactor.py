class Reactor: 
	event_types = {}
	event_i = 0
	@classmethod
	def event(cls, name=None):
		event = cls.event_i
		cls.event_i += 1
		if name:
			cls.event_types.setdefault(name, event)
		return event

	def __init__(self): 
		self.hooks = dict()
	
	def hook(self, event, callback):
		hooks = self.hooks.setdefault(event, [])
		hooks.append(callback)

	def unhook(self, event, callback):
		hooks = self.hooks.setdefault(event, [])
		if callback in hooks:
			hooks.remove(callback)

	def call(self, event, *args, **kwargs):
		hooks = self.hooks.setdefault(event, [])
		for hook in hooks:
			hook(*args, **kwargs)

