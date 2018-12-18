from pymongo import MongoClient

class mdb(object):

	def __init__(self, my_host, port, data_base):
		try:
			self.client = MongoClient(my_host, port)
		except Exception:
			raise Exception(f"client can't connect to mongodb.")
		print(f"connected to MongoDB")
		self.db = self.client[data_base]
		self.events = self.db.events
		self.chats = self.db.chats

		def insert_event_in_db(self, data):
			#poka tak, na praktike posmotrim chto da kak.
			if data is None:
				raise Exception(f"empty data for save.")
			else:
				event_id = self.events.insert_one(data).inserted_id
				print(f"insert_event_in_db - {event_id}")

		def insert_user_in_db(self, data):
			if data is None:
				raise Exception(f"empty data for save.")
			else:
				chat_id = self.chats.insert_one(data).inserted_id
				print(f"insert_chat_in_db - {chat_id}")
		
		def find_event_in_db(self, d_url):
			if d_url is None:
				raise Exception(f"empty f_name")
			else:
				finded_event = self.events.find_one({"downloaded_url":d_url})
				return finded_event

		def find_chat_in_db(self, u_id):
			if u_id is None:
				raise Exception(f"empty u_id")
			else:
				finded_chat = self.chats.find_one({'u_id': u_id})
				return finded_chat
		
		#think about delete_one or delete_many
		def delete_event_in_db(self, e_name):
			if f_name is None:
				raise Exception(f"empty f_name")
			result = self.events.delete_one({"event_name":e_name})
			if result["acknowledged"]:
				print(f"result delete_event_in_db - {result}")
			else:
				print(f"can't delete this obj")

		def delete_chat_in_db(self, u_id):
			if u_id is None:
				raise Exception(f"empty f_name")
			result = self.events.delete_one({"u_id":u_id})
			if result["acknowledged"]:
				print(f"result delete_chat_in_db - {result}")
			else:
				print(f"can't delete this obj")

		def update_event_in_db(self, f_name, data):
			if f_name is None:
				raise Exception(f"empty f_name")
			result = self.events.update_one({"event_name":f_name}, {"$set": data}, upsert=True)
			if result:
				print(f"result update_event_in_db - {result}")
			else:
				print(f"can't update this obj")

		def update_chat_in_db(self, u_id, data):
			if u_id is None:
				raise Exception(f"empty u_name")
			result = self.events.update_one({"u_id":u_id}, {"$set": data}, upsert=True)
			if result:
				print(f"result update_chat_in_db - {result}")
			else:
				print(f"can't update this obj")
