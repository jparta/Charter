
import requests
import socket
from app.controller import tasks
from .cache import cache
from cachetools import cached, TTLCache
from flask import current_app as app, request, Blueprint
from flask.helpers import send_file
from io import open as iopen
from pprint import pformat
from urllib.parse import parse_qs, urlsplit

bp = Blueprint('charter', __name__)

# adapted from https://gist.github.com/hanleybrand/4221658
def save_png(file_url):
    image_dir = 'images/'
    file_name =  urlsplit(file_url)[2].split('/')[-1] 
    mime_type = 'png'
    file_path = image_dir + file_name + ('.' + mime_type if mime_type not in file_name else '')
    print(file_url)
    i = requests.get(file_url)
    if i.status_code == requests.codes.ok:
        with iopen(file_path, 'wb') as file:
            file.write(i.content)
        return '../' + file_path, mime_type
    else:
        return False

@cache.memoize(timeout=10)
def cached_generate(chart_ID):
    print("generated", chart_ID)
    size = 900
    url_base = "https://loremflickr.com/{0}/{0}/{1}"
    file_name =  urlsplit(url_base)[2].split('/')[-1]
    final_url = url_base.format(size, chart_ID)
    return save_png(final_url) 

@cached(TTLCache(100, ttl=30))
def get_url_ip_address_list(hostname):
    ips = (a[4][0] for a in socket.getaddrinfo(hostname, None, 0, socket.SOCK_STREAM, socket.IPPROTO_TCP))
    return tuple(set(ips))

                         
@bp.route('/submission', methods=['POST'])
def new_submission():
    parameters = request.args
    post_data = request.form
    token = post_data.get('token') or parameters.get('token') or None
    app.logger.info("HOOK with token %s", token)
    hook_token = app.config.get('HOOK_TOKEN')
    if hook_token and (not token or token != hook_token):
        app.logger.debug("Hook token doesn't match or was missing in POST")
        return "Bad auth token: missing or invalid", 401
    reported_site_parsed = urlsplit(post_data.get('site'))
    base_url_netloc = urlsplit(app.config['BASE_URL']).netloc
    reported_netloc = reported_site_parsed.netloc
    if base_url_netloc != reported_netloc:
        app.logger.debug("base_url netloc in config %s doesn't match POST parameter 'site' %s netloc",
                     base_url_netloc, reported_netloc)
        return "Base url given in parameter 'site' does not match config", 400
    supposed_ips = get_url_ip_address_list(reported_site_parsed.hostname)
    client_ip = request.remote_addr
    if client_ip not in supposed_ips:
        app.logger.debug("Client ip %s doesn't match reported ips %s in POST body", client_ip, supposed_ips)
        return "Deceptive: client does not match POST parameter 'site' after resolve", 400
    app.logger.debug(pformat(dict(post_data)))
    tasks.save_submission.apply_async(args=[post_data.get('submission_id')], countdown=5)

    return "OK", 204

@bp.route('/chart/<string:chart_ID>', methods=['GET'])
def give_chart(chart_ID):
    result = cached_generate(chart_ID)
    if result:
        path, extension = result
        resp = send_file(path, mimetype='image/' + extension)
    else:
        resp = ("Chart was not found", 404)
    return resp

@bp.route('/create', methods=['POST'])
def create_visualization():
    return "Under construction"        

