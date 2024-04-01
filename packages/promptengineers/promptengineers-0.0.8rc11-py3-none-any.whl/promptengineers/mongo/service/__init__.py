"""Service for interacting with the history collection in MongoDB."""
import time
import motor.motor_asyncio

class MongoService:
	"""Service for interacting with the history collection in MongoDB."""

	def __init__(self, host: str, db: str, collection: str):
		client = motor.motor_asyncio.AsyncIOMotorClient(host)
		self.database = client[db]
		self.collection = self.database[collection]

	async def ensure_ttl_index(self):
		"""Ensure that the TTL index is set on the created_at field."""
		await self.collection.create_index("created_at", expireAfterSeconds=3600 * 24 * 7)

	async def list_docs(self, params: dict, limit=None, page=1, projection={'user_id': 0}) -> list:
		"""List documents in the collection with pagination."""
		cursor = self.collection.find(params, projection).sort("updated_at", -1)

		if limit:
			skip = (page - 1) * limit
			cursor = cursor.skip(skip).limit(limit)
		else:
			limit = 1000

		documents = await cursor.to_list(length=limit)
		return documents

	async def create(self, document: dict) -> str:
		"""Insert a new document into the collection."""
		document['created_at'] = int(time.time())
		document['updated_at'] = int(time.time())
		result = await self.collection.insert_one(dict(document))
		return {
			'_id': str(result.inserted_id)
		}

	async def read_one(self, params: dict, projection={'user_id': 0}) -> dict:
		"""Find and return a single document from the collection."""
		document = await self.collection.find_one(params, projection)
		return document

	async def update_one(self, params: dict, update: dict) -> bool:
		"""Update a single document in the collection."""
		update['updated_at'] = int(time.time())
		result = await self.collection.update_one(
			params,
			{'$set': update}
		)
		return result.modified_count > 0

	async def delete_one(self, params: dict) -> bool:
		"""Delete a single document from the collection."""
		result = await self.collection.delete_one(params)
		return result.deleted_count > 0
