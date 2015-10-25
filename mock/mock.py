import cherrypy

class MockController:
    def poi(self, location):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        with open("poi.json") as poifile:
        	return poifile.read()
    def faq(self, location):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        with open("faq.json") as faqfile:
            return faqfile.read()
    def phrasebook(self, location):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        with open("phrasebook.json") as phrasebookfile:
            return phrasebookfile.read()

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
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(app)
