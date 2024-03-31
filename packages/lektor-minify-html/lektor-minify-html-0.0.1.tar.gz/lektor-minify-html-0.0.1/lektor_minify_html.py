# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin
import minify_html

class MinifyHtmlPlugin(Plugin):
    name = 'Lektor minify html'
    description = u'Minify content using minify-html'

    def minify(self, source: str) -> str:
        return minify_html.minify(source, minify_js=True, minify_css=True)

    def on_after_build(self, builder, **extra) -> None:
        if not len(extra["prog"].artifacts):
            return

        dst_filename = extra["prog"].artifacts[0].dst_filename

        with open(dst_filename, 'r+') as file:
            html_content = file.read()
            file.seek(0)
            file.write(self.minify(html_content))
            file.truncate()
