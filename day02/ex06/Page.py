from elements import (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td,
                      Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Elem, Text)


class Page:
    def __init__(self, elem: Elem) -> None:
        if not isinstance(elem, Elem):
            raise Elem.ValidationError()
        self.elem = elem

    def __str__(self):
        result = ""
        if isinstance(self.elem, Html):
            result += "<!DOCTYPE html>\n"
        result += str(self.elem)
        return result

    def is_valid(self):
        return self._recursive_check(self.elem)

    def write_to_file(self, path):
        with open(path, "w") as f:
            f.write(str(self))

    def _recursive_check(self, elem: Elem) -> bool:
        if not isinstance(elem, (Elem, Text)):
            return False
        if isinstance(elem, (Text, Meta)):
            return True
        if (
                isinstance(elem, Html)
                and len(elem.content) == 2
                and isinstance(elem.content[0], Head)
                and isinstance(elem.content[1], Body)
        ):
            if all(self._recursive_check(el) for el in elem.content):
                return True
        elif (
                isinstance(elem, Head) and
                len(elem.content) == 1 and
                isinstance(elem.content[0], Title)
        ):
            if self._recursive_check(elem.content[0]):
                return True
        elif isinstance(elem, (Body, Div)):
            if all([isinstance(el, (H1, H2, Div, Table, Ul, Ol, Span, Text))
                    and self._recursive_check(el)
                    for el in elem.content]):
                return True
        elif (isinstance(elem, (Title, H1, H2, Li, Th, Td))
              and len(elem.content) == 1
              and isinstance(elem.content[0], Text)):
            return True
        elif (isinstance(elem, P)
              and all([isinstance(el, Text) for el in elem.content])):
            return True
        elif isinstance(elem, Span):
            if all([isinstance(el, (Text, P)) and self._recursive_check(el)
                    for el in elem.content]):
                return True
        elif isinstance(elem, (Ul, Ol)) and len(elem.content) > 0:
            if all([isinstance(el, Li) and self._recursive_check(el)
                    for el in elem.content]):
                return True
        elif (isinstance(elem, Tr) and len(elem.content) > 0
              and all([isinstance(el, (Th, Td))
                       and isinstance(el, type(elem.content[0]))
                       for el in elem.content])):
            return True
        elif (isinstance(elem, Table)
              and all([isinstance(el, Tr) for el in elem.content])):
            return True
        return False


def print_test(target: Page, to_be: bool):
    print("================START===============")
    print(target)
    print("===============IS_VALID=============")
    assert target.is_valid() == to_be
    print("{:^36s}".format(str(target.is_valid())))
    print("=================END================")


def test_table():
    print("\n%{:=^34s}%\n".format("Table"))
    target = Page(Table())
    print_test(target, True)
    target = Page(
        Table(
            [
                Tr(),
            ]))
    print_test(target, True)
    target = Page(
        Table(
            [
                H1(
                    Text("Hello World!")
                ),
            ]))
    print_test(target, False)


def test_tr():
    print("\n%{:=^34s}%\n".format("Tr"))
    target = Page(Tr())
    print_test(target, False)
    target = Page(
        Tr(
            [
                Th(Text("title")),
                Th(Text("title")),
                Th(Text("title")),
                Th(Text("title")),
                Th(Text("title")),
            ]))
    print_test(target, True)
    target = Page(
        Tr(
            [
                Td(Text("content")),
                Td(Text("content")),
                Td(Text("content")),
                Td(Text("content")),
                Td(Text("content")),
                Td(Text("content")),
            ]))
    print_test(target, True)
    target = Page(
        Tr(
            [
                Th(Text("title")),
                Td(Text("content")),
            ]))
    print_test(target, False)


def test_ul_ol():
    print("\n%{:=^34s}%\n".format("Ul_OL"))
    target = Page(
        Ul()
    )
    print_test(target, False)
    target = Page(
        Ol()
    )
    print_test(target, False)
    target = Page(
        Ul(
            Li(
                Text('test')
            )
        )
    )
    print_test(target, True)
    target = Page(
        Ol(
            Li(
                Text('test')
            )
        )
    )
    print_test(target, True)
    target = Page(
        Ul([
            Li(
                Text('test')
            ),
            Li(
                Text('test')
            ),
        ])
    )
    print_test(target, True)
    target = Page(
        Ol([
            Li(
                Text('test')
            ),
            Li(
                Text('test')
            ),
        ])
    )
    print_test(target, True)
    target = Page(
        Ul([
            Li(
                Text('test')
            ),
            H1(
                Text('test')
            ),
        ])
    )
    print_test(target, False)
    target = Page(
        Ol([
            Li(
                Text('test')
            ),
            H1(
                Text('test')
            ),
        ])
    )
    print_test(target, False)


def test_span():
    print("\n%{:=^34s}%\n".format("Span"))
    target = Page(
        Span()
    )
    print_test(target, True)
    target = Page(
        Span([
            Text("Hello?"),
            P(Text("World!")),
        ])
    )
    print_test(target, True)
    target = Page(
        Span([
            H1(Text("World!")),
        ])
    )
    print_test(target, False)


def test_p():
    print("\n%{:=^34s}%\n".format("P"))
    target = Page(
        P()
    )
    print_test(target, True)
    target = Page(
        P([
            Text("Hello?"),
        ])
    )
    print_test(target, True)
    target = Page(
        P([
            H1(Text("World!")),
        ])
    )
    print_test(target, False)


def test_title_h1_h2_li_th_td():
    print("\n%{:=^34s}%\n".format("H1_H2_Li_Th_Td"))
    for c in [H1, H2, Li, Th, Td]:
        target = Page(
            c()
        )
        print_test(target, False)
        target = Page(
            c([
                Text("Hello?"),
            ])
        )
        print_test(target, True)
        target = Page(
            c([
                H1(Text("World!")),
            ])
        )
        print_test(target, False)
        target = Page(
            c([
                Text("Hello?"),
                Text("Hello?"),
            ])
        )
        print_test(target, False)


def test_body_div():
    print("\n%{:=^34s}%\n".format("Body_Div"))
    for c in [Body, Div]:
        target = Page(
            c()
        )
        print_test(target, True)
        target = Page(
            c([
                Text("Hello?"),
            ])
        )
        print_test(target, True)
        target = Page(
            c([
                H1(Text("World!")),
            ])
        )
        print_test(target, True)
        target = Page(
            c([
                Text("Hello?"),
                Span(),
            ])
        )
        print_test(target, True)
        target = Page(
            c([
                Html(),
                c()
            ])
        )
        print_test(target, False)


def test_title():
    print("\n%{:=^34s}%\n".format("Title"))
    target = Page(
        Title()
    )
    print_test(target, False)
    target = Page(
        Title([
            Title(Text("Hello?")),
        ])
    )
    print_test(target, True)
    target = Page(
        Title([
            Title(Text("Hello?")),
            Title(Text("Hello?")),
        ])
    )
    print_test(target, False)


def test_html():
    print("\n%{:=^34s}%\n".format("Html"))
    target = Page(
        Html()
    )
    print_test(target, False)
    target = Page(
        Html([
            Head([
                Title(Text("Hello?")),
            ]),
            Body([
                H1(Text("Hello?")),
            ])
        ])
    )
    print_test(target, True)
    target = Page(
        Html(
            Div()
        )
    )
    print_test(target, False)


def test_elem():
    print_test(Page(Elem()), False)


def test_write_to_file(target: Page, path: str):
    print("================START===============")
    print(str(target))
    print("==========WRITE_TO_FILE=============")
    target.write_to_file(path)
    print("{:^36s}".format(path))
    print("=================END================")


def test():
    test_table()
    test_tr()
    test_ul_ol()
    test_span()
    test_p()
    test_title_h1_h2_li_th_td()
    test_body_div()
    test_html()
    test_elem()
    test_write_to_file(
        Page(Html([
            Head(Title(Text("hello world!"))),
            Body(H1(Text("HELLO WORLD!")))
        ])),
        "test_write_to_file.html"
    )


if __name__ == '__main__':
    test()
