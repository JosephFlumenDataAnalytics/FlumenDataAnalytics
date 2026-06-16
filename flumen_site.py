from flask import Blueprint, render_template, Response

flumen_bp = Blueprint('flumen', __name__)

@flumen_bp.route('/')
def home():
    return render_template("analytics/index.html", metabase_url="https://dashboard.flumendataanalytics.com")

@flumen_bp.route('/sitemap.xml')
def sitemap():
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://flumendataanalytics.com/</loc>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://flumendataanalytics.com/analytics</loc>
    <priority>0.8</priority>
  </url>
</urlset>'''
    return Response(xml, mimetype='application/xml')
