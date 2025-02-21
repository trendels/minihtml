from minihtml import PrototypeEmpty, PrototypeNonEmpty, make_prototype

__all__ = [
    # [[[cog
    #   from yaml import safe_load
    #
    #   with open(TAGS) as f:
    #       SPEC = safe_load(f)
    #
    #   for tag in SPEC["tags"]:
    #       info = SPEC["tags"][tag] or {}
    #       cog.outl(f'"{info.get("alias", tag)}",')
    # ]]]
    "html",
    "head",
    "title",
    "base",
    "link",
    "meta",
    "style",
    "body",
    "article",
    "section",
    "nav",
    "aside",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hgroup",
    "header",
    "footer",
    "address",
    "p",
    "hr",
    "pre",
    "blockquote",
    "ol",
    "ul",
    "menu",
    "li",
    "dl",
    "dt",
    "dd",
    "figure",
    "figcaption",
    "main",
    "search",
    "div",
    "a",
    "em",
    "strong",
    "small",
    "s",
    "cite",
    "q",
    "dfn",
    "abbr",
    "ruby",
    "rt",
    "rp",
    "data",
    "time",
    "code",
    "var",
    "samp",
    "kbd",
    "sub",
    "sup",
    "i",
    "b",
    "u",
    "mark",
    "bdi",
    "bdo",
    "span",
    "br",
    "wbr",
    "ins",
    "del_",
    "picture",
    "source",
    "img",
    "iframe",
    "embed",
    "object_",
    "video",
    "audio",
    "track",
    "map_",
    "area",
    "table",
    "caption",
    "colgroup",
    "col",
    "tbody",
    "thead",
    "tfoot",
    "tr",
    "td",
    "th",
    "form",
    "label",
    "input_",
    "button",
    "select",
    "datalist",
    "optgroup",
    "option",
    "textarea",
    "output",
    "progress",
    "meter",
    "fieldset",
    "legend",
    "details",
    "summary",
    "dialog",
    "script",
    "noscript",
    "template_",
    "slot",
    "canvas",
    # [[[end]]] (checksum: 8f9d1678585a7aed604675580615b43b)
]

# [[[cog
#   for tag in SPEC["tags"]:
#       info = SPEC["tags"][tag] or {}
#       if info.get("hidden"):
#           name, alias = info["alias"], None
#       else:
#           name, alias = tag, info.get("alias")
#
#       type = "PrototypeEmpty" if info.get("empty", False) else "PrototypeNonEmpty"
#
#       cog.out(f'{name}: {type} = make_prototype("{tag}"')
#       if info.get("inline", False):
#           cog.out(", inline=True")
#       if info.get("empty", False):
#           cog.out(", empty=True")
#           if info.get("omit_end_tag", False):
#               cog.out(", omit_end_tag=True")
#       cog.out(")\n")
#       if alias:
#           cog.outl(f"{alias} = {name}")
#
# ]]]
html: PrototypeNonEmpty = make_prototype("html")
head: PrototypeNonEmpty = make_prototype("head")
title: PrototypeNonEmpty = make_prototype("title")
base: PrototypeEmpty = make_prototype("base", empty=True, omit_end_tag=True)
link: PrototypeEmpty = make_prototype("link", empty=True, omit_end_tag=True)
meta: PrototypeEmpty = make_prototype("meta", empty=True, omit_end_tag=True)
style: PrototypeNonEmpty = make_prototype("style")
body: PrototypeNonEmpty = make_prototype("body")
article: PrototypeNonEmpty = make_prototype("article")
section: PrototypeNonEmpty = make_prototype("section")
nav: PrototypeNonEmpty = make_prototype("nav")
aside: PrototypeNonEmpty = make_prototype("aside")
h1: PrototypeNonEmpty = make_prototype("h1")
h2: PrototypeNonEmpty = make_prototype("h2")
h3: PrototypeNonEmpty = make_prototype("h3")
h4: PrototypeNonEmpty = make_prototype("h4")
h5: PrototypeNonEmpty = make_prototype("h5")
h6: PrototypeNonEmpty = make_prototype("h6")
hgroup: PrototypeNonEmpty = make_prototype("hgroup")
header: PrototypeNonEmpty = make_prototype("header")
footer: PrototypeNonEmpty = make_prototype("footer")
address: PrototypeNonEmpty = make_prototype("address")
p: PrototypeNonEmpty = make_prototype("p")
hr: PrototypeEmpty = make_prototype("hr", empty=True, omit_end_tag=True)
pre: PrototypeNonEmpty = make_prototype("pre")
blockquote: PrototypeNonEmpty = make_prototype("blockquote")
ol: PrototypeNonEmpty = make_prototype("ol")
ul: PrototypeNonEmpty = make_prototype("ul")
menu: PrototypeNonEmpty = make_prototype("menu")
li: PrototypeNonEmpty = make_prototype("li")
dl: PrototypeNonEmpty = make_prototype("dl")
dt: PrototypeNonEmpty = make_prototype("dt")
dd: PrototypeNonEmpty = make_prototype("dd")
figure: PrototypeNonEmpty = make_prototype("figure")
figcaption: PrototypeNonEmpty = make_prototype("figcaption")
main: PrototypeNonEmpty = make_prototype("main")
search: PrototypeNonEmpty = make_prototype("search")
div: PrototypeNonEmpty = make_prototype("div")
a: PrototypeNonEmpty = make_prototype("a", inline=True)
em: PrototypeNonEmpty = make_prototype("em", inline=True)
strong: PrototypeNonEmpty = make_prototype("strong", inline=True)
small: PrototypeNonEmpty = make_prototype("small", inline=True)
s: PrototypeNonEmpty = make_prototype("s", inline=True)
cite: PrototypeNonEmpty = make_prototype("cite", inline=True)
q: PrototypeNonEmpty = make_prototype("q", inline=True)
dfn: PrototypeNonEmpty = make_prototype("dfn", inline=True)
abbr: PrototypeNonEmpty = make_prototype("abbr", inline=True)
ruby: PrototypeNonEmpty = make_prototype("ruby", inline=True)
rt: PrototypeNonEmpty = make_prototype("rt", inline=True)
rp: PrototypeNonEmpty = make_prototype("rp", inline=True)
data: PrototypeNonEmpty = make_prototype("data", inline=True)
time: PrototypeNonEmpty = make_prototype("time", inline=True)
code: PrototypeNonEmpty = make_prototype("code", inline=True)
var: PrototypeNonEmpty = make_prototype("var", inline=True)
samp: PrototypeNonEmpty = make_prototype("samp", inline=True)
kbd: PrototypeNonEmpty = make_prototype("kbd", inline=True)
sub: PrototypeNonEmpty = make_prototype("sub", inline=True)
sup: PrototypeNonEmpty = make_prototype("sup", inline=True)
i: PrototypeNonEmpty = make_prototype("i", inline=True)
b: PrototypeNonEmpty = make_prototype("b", inline=True)
u: PrototypeNonEmpty = make_prototype("u", inline=True)
mark: PrototypeNonEmpty = make_prototype("mark", inline=True)
bdi: PrototypeNonEmpty = make_prototype("bdi", inline=True)
bdo: PrototypeNonEmpty = make_prototype("bdo", inline=True)
span: PrototypeNonEmpty = make_prototype("span", inline=True)
br: PrototypeEmpty = make_prototype("br", inline=True, empty=True, omit_end_tag=True)
wbr: PrototypeEmpty = make_prototype("wbr", inline=True, empty=True, omit_end_tag=True)
ins: PrototypeNonEmpty = make_prototype("ins", inline=True)
del_: PrototypeNonEmpty = make_prototype("del", inline=True)
picture: PrototypeNonEmpty = make_prototype("picture")
source: PrototypeEmpty = make_prototype("source", empty=True, omit_end_tag=True)
img: PrototypeEmpty = make_prototype("img", inline=True, empty=True, omit_end_tag=True)
iframe: PrototypeEmpty = make_prototype("iframe", empty=True)
embed: PrototypeEmpty = make_prototype("embed", empty=True, omit_end_tag=True)
object: PrototypeNonEmpty = make_prototype("object")
object_ = object
video: PrototypeNonEmpty = make_prototype("video")
audio: PrototypeNonEmpty = make_prototype("audio")
track: PrototypeEmpty = make_prototype("track", empty=True, omit_end_tag=True)
map: PrototypeNonEmpty = make_prototype("map")
map_ = map
area: PrototypeEmpty = make_prototype("area", empty=True, omit_end_tag=True)
table: PrototypeNonEmpty = make_prototype("table")
caption: PrototypeNonEmpty = make_prototype("caption")
colgroup: PrototypeNonEmpty = make_prototype("colgroup")
col: PrototypeEmpty = make_prototype("col", empty=True, omit_end_tag=True)
tbody: PrototypeNonEmpty = make_prototype("tbody")
thead: PrototypeNonEmpty = make_prototype("thead")
tfoot: PrototypeNonEmpty = make_prototype("tfoot")
tr: PrototypeNonEmpty = make_prototype("tr")
td: PrototypeNonEmpty = make_prototype("td")
th: PrototypeNonEmpty = make_prototype("th")
form: PrototypeNonEmpty = make_prototype("form")
label: PrototypeNonEmpty = make_prototype("label")
input: PrototypeEmpty = make_prototype("input", empty=True, omit_end_tag=True)
input_ = input
button: PrototypeNonEmpty = make_prototype("button")
select: PrototypeNonEmpty = make_prototype("select")
datalist: PrototypeNonEmpty = make_prototype("datalist")
optgroup: PrototypeNonEmpty = make_prototype("optgroup")
option: PrototypeNonEmpty = make_prototype("option")
textarea: PrototypeNonEmpty = make_prototype("textarea")
output: PrototypeNonEmpty = make_prototype("output")
progress: PrototypeNonEmpty = make_prototype("progress")
meter: PrototypeNonEmpty = make_prototype("meter")
fieldset: PrototypeNonEmpty = make_prototype("fieldset")
legend: PrototypeNonEmpty = make_prototype("legend")
details: PrototypeNonEmpty = make_prototype("details")
summary: PrototypeNonEmpty = make_prototype("summary")
dialog: PrototypeNonEmpty = make_prototype("dialog")
script: PrototypeNonEmpty = make_prototype("script")
noscript: PrototypeNonEmpty = make_prototype("noscript")
template: PrototypeNonEmpty = make_prototype("template")
template_ = template
slot: PrototypeNonEmpty = make_prototype("slot")
canvas: PrototypeNonEmpty = make_prototype("canvas")
# [[[end]]] (checksum: b3b6a50dc8f4e349aca1295554ccf095)
