import cherrypy

class MockController:

    def poi(self, location):
        with open("poi.json") as poifile:
        	return poifile.read()
    def faq(self, location):
        with open("faq.json") as faqfile:
            return poifile.read()
    def phrasebook(self, location):
        with open("phrasebook.json") as phrasebookfile:
            return poifile.read()

def setup_routes():
    d = cherrypy.dispatch.RoutesDispatcher()
    d.connect('mock', '/:action/:location', controller=MockController())
    dispatcher = d
    return dispatcher

conf = {
    '/': {
        'request.dispatch': setup_routes()
    }
}
if __name__ == '__main__':
    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.quickstart(app)