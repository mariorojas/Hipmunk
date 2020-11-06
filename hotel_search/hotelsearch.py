from tornado import escape, httpclient, ioloop, web
from tornado.gen import multi


BASE_URL = "http://localhost:9000/scrapers/"
PROVIDERS = ["expedia", "orbitz", "priceline", "travelocity", "hilton"]


class HotelSearchHandler(web.RequestHandler):

    async def get(self):
        urls = [BASE_URL + p for p in PROVIDERS]

        http_client = httpclient.AsyncHTTPClient()
        responses = await multi([http_client.fetch(url) for url in urls])

        responses = [self.extract_results(r) for r in responses]

        # Flattening and sorting results list
        results = [row for response in responses for row in response]
        results.sort(key=lambda k: k["ecstasy"], reverse=True)
        
        self.write({"results": results})

    def extract_results(self, response):
        r = escape.json_decode(response.body)
        return r["results"]


ROUTES = [
    (r"/hotels/search", HotelSearchHandler),
]


def run():
    app = web.Application(ROUTES, debug=True)

    app.listen(8000)
    print("Server (re)started. Listening on por 8000")

    ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run()
