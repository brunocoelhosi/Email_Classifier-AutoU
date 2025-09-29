from ninja import NinjaAPI
from email_classifier.api import router

api = NinjaAPI()
api.add_router('', router)
