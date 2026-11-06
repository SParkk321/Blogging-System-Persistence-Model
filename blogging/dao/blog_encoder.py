import json
from blogging.blog import Blog

class BlogEncoder(json.JSONEncoder):


    def default(self, obj):

        if isinstance(obj, Blog):
            return {"__type__": "Blog", "id": obj.id, "name": obj.name, "url": obj.url, "email": obj.email}

        return super().default(obj)