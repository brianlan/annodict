from typing import List
import requests


def post_docs(resource: str, docs: List[dict], api_server: str) -> List[str]:
    """post docs to db using restful api, get the object ids from the response and return them.
    The response will look like:
    {
        "_status": "OK",
        "_items": [
            {
                "_updated": "Tue, 25 Jul 2023 10:49:02 GMT",
                "_created": "Tue, 25 Jul 2023 10:49:02 GMT",
                "_id": "64bfa89e9ba8e90aa82b7c21",
                "_links": {
                    "self": {
                        "title": "annoattr",
                        "href": "annoattr/64bfa89e9ba8e90aa82b7c21"
                    }
                },
                "_status": "OK"
            },
            {
                "_updated": "Tue, 25 Jul 2023 10:49:02 GMT",
                "_created": "Tue, 25 Jul 2023 10:49:02 GMT",
                "_id": "64bfa89e9ba8e90aa82b7c22",
                "_links": {
                    "self": {
                        "title": "annoattr",
                        "href": "annoattr/64bfa89e9ba8e90aa82b7c22"
                    }
                },
                "_status": "OK"
            }
        ]
    }
        
    """
    headers = {"Content-Type": "application/json"}
    resp = requests.post(f"{api_server}/{resource}", json=docs, headers=headers)
    if resp.status_code != 201:
        print(resp.text)
        raise ValueError(f"Failed to post doc: {docs}")
    if "_items" in resp.json():
        return [item["_id"] for item in resp.json()["_items"]]
    return [resp.json()["_id"]]
 