
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb+srv://mymongo:mymongo123@cluster0.qtg3a9q.mongodb.net/DemoManoj?retryWrites=true&w=majority")
db = client['DemoManoj']
students_collection = db['students']
