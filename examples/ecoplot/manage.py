'''
Script for running a stand-alone Web application for testing the ecoplot plugin.
It requires djpcms (https://github.com/lsbardel/djpcms)

To run the server simply::

    python manage.py serve

Then open a web browser and go to

http://localhost:8060
'''
import djpcms


class Loader(djpcms.SiteLoader):
    
    def load(self):
        djpcms.MakeSite(__file__,
            APPLICATION_URLS = self.urls,
            INSTALLED_APPS = ('djpcms',
                              'medplate', 
                              'dynts',
                              'ecoplot'),
            TEMPLATE_CONTEXT_PROCESSORS = (
                              'djpcms.core.context_processors.djpcms',
                              'djpcms.core.context_processors.messages',
                              'ecoplot.application.context_process'),
            ENABLE_BREADCRUMBS = 1,
            DEFAULT_LAYOUT = 1, #Floating layout
            FAVICON_MODULE = 'dynts',
            PROFILING_KEY = 'prof',
            STYLING = 'dark',
            DEBUG = True
        )
    
    def urls(self):
        from djpcms.apps.included import static
        from ecoplot.application import Application
        
        # we serve static files too in this case
        return (
                static.FavIcon(),
                static.Static(djpcms.sites.settings.MEDIA_URL,
                              show_indexes=True),
                Application('/', name = 'Econometric plotting with dynts')
                )
    
    
if __name__ == '__main__':
    djpcms.execute(Loader())
