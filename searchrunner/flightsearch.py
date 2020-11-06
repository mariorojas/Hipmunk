from tornado import escape, ioloop, httpclient, web
from tornado.gen import multi


PROVIDERS = [
    "expedia",
    "orbitz",
    "priceline",
    "travelocity",
    "united",
]

class FlightSearchHandler(web.RequestHandler):

    async def get(self):
        base_url = "http://localhost:9000/scrapers/"
        urls = [base_url + p for p in PROVIDERS]

        http_client = httpclient.AsyncHTTPClient()
        responses = await multi([http_client.fetch(url) for url in urls])
        
        responses = [
            escape.json_decode(response.body)["results"]
            for response in responses
        ]

        results = [r for provider_list in responses for r in provider_list]
        results.sort(key=lambda x: x["agony"])

        self.write({"results": results})


ROUTES = [
    (r"/flights/search", FlightSearchHandler),
]


def run():
    app = web.Application(
        ROUTES, 
        debug=True,
    )

    app.listen(8000)
    print("Server (re)started. Listening on por 8000")

    ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run()
