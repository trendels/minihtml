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
#       cog.outl(f"#: The ``{tag}`` element.")
#       cog.out(f'{name}: {type} = make_prototype("{tag}"')
#       if info.get("inline", False):
#           cog.out(", inline=True")
#       if info.get("empty", False):
#           cog.out(", empty=True")
#           if info.get("omit_end_tag", False):
#               cog.out(", omit_end_tag=True")
#       cog.out(")\n")
#       if alias:
#           cog.outl(f"#: The ``{tag}`` element. Alias for :data:`{name}`.")
#           cog.outl(f"{alias} = {name}")
#
# ]]]
#: The ``html`` element.
html: PrototypeNonEmpty = make_prototype("html")
#: The ``head`` element.
head: PrototypeNonEmpty = make_prototype("head")
#: The ``title`` element.
title: PrototypeNonEmpty = make_prototype("title")
#: The ``base`` element.
base: PrototypeEmpty = make_prototype("base", empty=True, omit_end_tag=True)
#: The ``link`` element.
link: PrototypeEmpty = make_prototype("link", empty=True, omit_end_tag=True)
#: The ``meta`` element.
meta: PrototypeEmpty = make_prototype("meta", empty=True, omit_end_tag=True)
#: The ``style`` element.
style: PrototypeNonEmpty = make_prototype("style")
#: The ``body`` element.
body: PrototypeNonEmpty = make_prototype("body")
#: The ``article`` element.
article: PrototypeNonEmpty = make_prototype("article")
#: The ``section`` element.
section: PrototypeNonEmpty = make_prototype("section")
#: The ``nav`` element.
nav: PrototypeNonEmpty = make_prototype("nav")
#: The ``aside`` element.
aside: PrototypeNonEmpty = make_prototype("aside")
#: The ``h1`` element.
h1: PrototypeNonEmpty = make_prototype("h1")
#: The ``h2`` element.
h2: PrototypeNonEmpty = make_prototype("h2")
#: The ``h3`` element.
h3: PrototypeNonEmpty = make_prototype("h3")
#: The ``h4`` element.
h4: PrototypeNonEmpty = make_prototype("h4")
#: The ``h5`` element.
h5: PrototypeNonEmpty = make_prototype("h5")
#: The ``h6`` element.
h6: PrototypeNonEmpty = make_prototype("h6")
#: The ``hgroup`` element.
hgroup: PrototypeNonEmpty = make_prototype("hgroup")
#: The ``header`` element.
header: PrototypeNonEmpty = make_prototype("header")
#: The ``footer`` element.
footer: PrototypeNonEmpty = make_prototype("footer")
#: The ``address`` element.
address: PrototypeNonEmpty = make_prototype("address")
#: The ``p`` element.
p: PrototypeNonEmpty = make_prototype("p")
#: The ``hr`` element.
hr: PrototypeEmpty = make_prototype("hr", empty=True, omit_end_tag=True)
#: The ``pre`` element.
pre: PrototypeNonEmpty = make_prototype("pre")
#: The ``blockquote`` element.
blockquote: PrototypeNonEmpty = make_prototype("blockquote")
#: The ``ol`` element.
ol: PrototypeNonEmpty = make_prototype("ol")
#: The ``ul`` element.
ul: PrototypeNonEmpty = make_prototype("ul")
#: The ``menu`` element.
menu: PrototypeNonEmpty = make_prototype("menu")
#: The ``li`` element.
li: PrototypeNonEmpty = make_prototype("li")
#: The ``dl`` element.
dl: PrototypeNonEmpty = make_prototype("dl")
#: The ``dt`` element.
dt: PrototypeNonEmpty = make_prototype("dt")
#: The ``dd`` element.
dd: PrototypeNonEmpty = make_prototype("dd")
#: The ``figure`` element.
figure: PrototypeNonEmpty = make_prototype("figure")
#: The ``figcaption`` element.
figcaption: PrototypeNonEmpty = make_prototype("figcaption")
#: The ``main`` element.
main: PrototypeNonEmpty = make_prototype("main")
#: The ``search`` element.
search: PrototypeNonEmpty = make_prototype("search")
#: The ``div`` element.
div: PrototypeNonEmpty = make_prototype("div")
#: The ``a`` element.
a: PrototypeNonEmpty = make_prototype("a", inline=True)
#: The ``em`` element.
em: PrototypeNonEmpty = make_prototype("em", inline=True)
#: The ``strong`` element.
strong: PrototypeNonEmpty = make_prototype("strong", inline=True)
#: The ``small`` element.
small: PrototypeNonEmpty = make_prototype("small", inline=True)
#: The ``s`` element.
s: PrototypeNonEmpty = make_prototype("s", inline=True)
#: The ``cite`` element.
cite: PrototypeNonEmpty = make_prototype("cite", inline=True)
#: The ``q`` element.
q: PrototypeNonEmpty = make_prototype("q", inline=True)
#: The ``dfn`` element.
dfn: PrototypeNonEmpty = make_prototype("dfn", inline=True)
#: The ``abbr`` element.
abbr: PrototypeNonEmpty = make_prototype("abbr", inline=True)
#: The ``ruby`` element.
ruby: PrototypeNonEmpty = make_prototype("ruby", inline=True)
#: The ``rt`` element.
rt: PrototypeNonEmpty = make_prototype("rt", inline=True)
#: The ``rp`` element.
rp: PrototypeNonEmpty = make_prototype("rp", inline=True)
#: The ``data`` element.
data: PrototypeNonEmpty = make_prototype("data", inline=True)
#: The ``time`` element.
time: PrototypeNonEmpty = make_prototype("time", inline=True)
#: The ``code`` element.
code: PrototypeNonEmpty = make_prototype("code", inline=True)
#: The ``var`` element.
var: PrototypeNonEmpty = make_prototype("var", inline=True)
#: The ``samp`` element.
samp: PrototypeNonEmpty = make_prototype("samp", inline=True)
#: The ``kbd`` element.
kbd: PrototypeNonEmpty = make_prototype("kbd", inline=True)
#: The ``sub`` element.
sub: PrototypeNonEmpty = make_prototype("sub", inline=True)
#: The ``sup`` element.
sup: PrototypeNonEmpty = make_prototype("sup", inline=True)
#: The ``i`` element.
i: PrototypeNonEmpty = make_prototype("i", inline=True)
#: The ``b`` element.
b: PrototypeNonEmpty = make_prototype("b", inline=True)
#: The ``u`` element.
u: PrototypeNonEmpty = make_prototype("u", inline=True)
#: The ``mark`` element.
mark: PrototypeNonEmpty = make_prototype("mark", inline=True)
#: The ``bdi`` element.
bdi: PrototypeNonEmpty = make_prototype("bdi", inline=True)
#: The ``bdo`` element.
bdo: PrototypeNonEmpty = make_prototype("bdo", inline=True)
#: The ``span`` element.
span: PrototypeNonEmpty = make_prototype("span", inline=True)
#: The ``br`` element.
br: PrototypeEmpty = make_prototype("br", inline=True, empty=True, omit_end_tag=True)
#: The ``wbr`` element.
wbr: PrototypeEmpty = make_prototype("wbr", inline=True, empty=True, omit_end_tag=True)
#: The ``ins`` element.
ins: PrototypeNonEmpty = make_prototype("ins", inline=True)
#: The ``del`` element.
del_: PrototypeNonEmpty = make_prototype("del", inline=True)
#: The ``picture`` element.
picture: PrototypeNonEmpty = make_prototype("picture")
#: The ``source`` element.
source: PrototypeEmpty = make_prototype("source", empty=True, omit_end_tag=True)
#: The ``img`` element.
img: PrototypeEmpty = make_prototype("img", inline=True, empty=True, omit_end_tag=True)
#: The ``iframe`` element.
iframe: PrototypeEmpty = make_prototype("iframe", empty=True)
#: The ``embed`` element.
embed: PrototypeEmpty = make_prototype("embed", empty=True, omit_end_tag=True)
#: The ``object`` element.
object: PrototypeNonEmpty = make_prototype("object")
#: The ``object`` element. Alias for :data:`object`.
object_ = object
#: The ``video`` element.
video: PrototypeNonEmpty = make_prototype("video")
#: The ``audio`` element.
audio: PrototypeNonEmpty = make_prototype("audio")
#: The ``track`` element.
track: PrototypeEmpty = make_prototype("track", empty=True, omit_end_tag=True)
#: The ``map`` element.
map: PrototypeNonEmpty = make_prototype("map")
#: The ``map`` element. Alias for :data:`map`.
map_ = map
#: The ``area`` element.
area: PrototypeEmpty = make_prototype("area", empty=True, omit_end_tag=True)
#: The ``table`` element.
table: PrototypeNonEmpty = make_prototype("table")
#: The ``caption`` element.
caption: PrototypeNonEmpty = make_prototype("caption")
#: The ``colgroup`` element.
colgroup: PrototypeNonEmpty = make_prototype("colgroup")
#: The ``col`` element.
col: PrototypeEmpty = make_prototype("col", empty=True, omit_end_tag=True)
#: The ``tbody`` element.
tbody: PrototypeNonEmpty = make_prototype("tbody")
#: The ``thead`` element.
thead: PrototypeNonEmpty = make_prototype("thead")
#: The ``tfoot`` element.
tfoot: PrototypeNonEmpty = make_prototype("tfoot")
#: The ``tr`` element.
tr: PrototypeNonEmpty = make_prototype("tr")
#: The ``td`` element.
td: PrototypeNonEmpty = make_prototype("td")
#: The ``th`` element.
th: PrototypeNonEmpty = make_prototype("th")
#: The ``form`` element.
form: PrototypeNonEmpty = make_prototype("form")
#: The ``label`` element.
label: PrototypeNonEmpty = make_prototype("label")
#: The ``input`` element.
input: PrototypeEmpty = make_prototype("input", empty=True, omit_end_tag=True)
#: The ``input`` element. Alias for :data:`input`.
input_ = input
#: The ``button`` element.
button: PrototypeNonEmpty = make_prototype("button")
#: The ``select`` element.
select: PrototypeNonEmpty = make_prototype("select")
#: The ``datalist`` element.
datalist: PrototypeNonEmpty = make_prototype("datalist")
#: The ``optgroup`` element.
optgroup: PrototypeNonEmpty = make_prototype("optgroup")
#: The ``option`` element.
option: PrototypeNonEmpty = make_prototype("option")
#: The ``textarea`` element.
textarea: PrototypeNonEmpty = make_prototype("textarea")
#: The ``output`` element.
output: PrototypeNonEmpty = make_prototype("output")
#: The ``progress`` element.
progress: PrototypeNonEmpty = make_prototype("progress")
#: The ``meter`` element.
meter: PrototypeNonEmpty = make_prototype("meter")
#: The ``fieldset`` element.
fieldset: PrototypeNonEmpty = make_prototype("fieldset")
#: The ``legend`` element.
legend: PrototypeNonEmpty = make_prototype("legend")
#: The ``details`` element.
details: PrototypeNonEmpty = make_prototype("details")
#: The ``summary`` element.
summary: PrototypeNonEmpty = make_prototype("summary")
#: The ``dialog`` element.
dialog: PrototypeNonEmpty = make_prototype("dialog")
#: The ``script`` element.
script: PrototypeNonEmpty = make_prototype("script")
#: The ``noscript`` element.
noscript: PrototypeNonEmpty = make_prototype("noscript")
#: The ``template`` element.
template: PrototypeNonEmpty = make_prototype("template")
#: The ``template`` element. Alias for :data:`template`.
template_ = template
#: The ``slot`` element.
slot: PrototypeNonEmpty = make_prototype("slot")
#: The ``canvas`` element.
canvas: PrototypeNonEmpty = make_prototype("canvas")
# [[[end]]] (checksum: 9d0f6f3a6fdd91db8b23518117d3e1e2)
