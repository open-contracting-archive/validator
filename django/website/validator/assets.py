from django_assets import Bundle, register

"""
# Javascript
js = Bundle(filters='rjsmin',
            output='js/site.js')
register('js_all', js)
"""

# CSS
standard_scss = Bundle('scss/main.scss',
                       filters='pyscss',
                       output='css/standard.css',
                       depends='scss/*.scss')
css = Bundle(  # Other components like bootstrap
             standard_scss,
             filters='cssmin',
             output='css/site.css')
register('css_all', css)
