from minihtml.tags import a, body, div, head, html, img, li, p, title, ul

links = [("Home", "/"), ("About Me", "/about"), ("Projects", "/projects")]

with html(lang="en") as elem:
    with head:
        title("hello, world!")
    with body, div["#content main"]:
        p("Welcome to ", a(href="https://example.com/")("my website"))
        img(src="hello.png", alt="hello")
        with ul:
            for title, url in links:
                li(a(href=url)(title))

print(elem)
