import time

from dateutil.parser import parse
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from py2neo import Graph

from livarava.job import Job
from settings import NEO4J_BOLT

app = Flask(__name__)
app.jinja_env.auto_reload = True
bootstrap = Bootstrap(app)
fa = FontAwesome(app)
graph = Graph(NEO4J_BOLT)


@app.route('/')
def index():
    items = Job.match(graph).order_by("_.created DESC").limit(4)
    return render_template('index.html', items=items)


@app.route('/details/<int:job_id>')
def job(job_id):
    # Fetch Job Item
    item = Job.match(graph).where("ID(_)={0}".format(job_id)).first()
    # print(item)

    # Main
    url = request.url
    title = item.header or item.meta_title or item.title or ''

    # Meta
    meta_title = item.meta_title or item.title or ''
    meta_description = item.meta_description or item.summary or ''
    meta_keywords = item.meta_keywords or ''

    # Facebook
    meta_fb_app_id = 259898127536918
    meta_fb_pages = 153877091338401
    meta_og_type = 'article'
    meta_og_site_name = 'LivaRava'
    meta_og_url = url
    meta_og_locale = item.language or 'en'
    meta_og_title = item.meta_title or item.title
    meta_og_description = item.meta_description or item.summary
    meta_og_image = item.meta_image_url or item.image_url

    # Twitter
    meta_twitter_url = url
    meta_twitter_site = u'@livarava'

    # Meta Data
    meta = dict(
        title=meta_title,
        description=meta_description,
        keywords=meta_keywords,
        fb_app_id=meta_fb_app_id,
        fb_pages=meta_fb_pages,
        og_type=meta_og_type,
        og_site_name=meta_og_site_name,
        og_url=meta_og_url,
        og_locale=meta_og_locale,
        og_title=meta_og_title,
        og_description=meta_og_description,
        og_image=meta_og_image,
        twitter_url=meta_twitter_url,
        twitter_site=meta_twitter_site
    )

    # Share Data
    share = dict(
        facebook='https://www.facebook.com/sharer/sharer.php?u={0}'
                 ''.format(url),
        twitter='https://twitter.com/home?status={0} {1}'
                ''.format(title, url),
        linkedin='https://www.linkedin.com/shareArticle?mini=true&url={0}&title={1}'
                 ''.format(url, title),
        pinterest='https://pinterest.com/pin/create/button/?url={0}&description={1}'
                  ''.format(url, title),
    )

    return render_template('job.html',
                           item=item,
                           meta=meta,
                           share=share)


@app.template_filter('time')
def time_filter(s):
    return int(round(time.time() * 1000))


@app.template_filter('isodatetime')
def reverse_filter(s):
    dt = parse(s)
    return dt.strftime('%b %d, %Y')


if __name__ == '__main__':
    app.run()
