from .fetch import cache_fetch
from typing import Union
from bs4 import BeautifulSoup
import bs4
import re
import json

URL_PROGRAMS = 'https://catalog.shepherd.edu/content.php?catoid=19&navoid=3646'
URL_PREVIEW = 'https://catalog.shepherd.edu/preview_program.php?poid='


def elemHasClass(elem: bs4.Tag, string: str) -> bool:
    cl = elem.get('class')
    if cl and string in cl:
        return True
    else:
        return False


# Check if element has a class
def soupHasClass(soup: BeautifulSoup, class_) -> bool:
    for c in soup.get('class'):
        if class_ in str(c):
            return True
    return False


# Find a parent of an element.
def findSoupParent(source_soup: BeautifulSoup, element: str, tries: int = 10) -> bs4.Tag:
    current = source_soup.parent
    while True:
        if current and current.name == element:
            return current
        elif tries < 0:
            raise RuntimeError  # TODO "scraping" error?
        else:
            tries -= 1
            current = current.parent


# General function to find an element with class within soup
def findElementWithClassInSoup(source_soup: BeautifulSoup, element: str, _class: str) -> BeautifulSoup:
    e = source_soup.find_all(element)

    # FIXME no idea why this cant be gotten the normal way with find_all. This is concerning
    # i think i was using _class not class_? (in funciton call)

    for td in e:
        if [_class] == td.get('class'):  # TODO what if multiple classes
            return td

    raise RuntimeError  # FIXME Get better error


# def soupGetElementOfType(soup: BeautifulSoup, element: str):


# Get only DIRECT children.
def elemDirectChildren(elem: bs4.Tag, name: str = None) -> list[bs4.Tag]:
    """FIXME warning this has fidget brain"""
    if name:
        rows = elem.find_all(name, recursive=False)
    else:
        rows = elem.find_all(recursive=False)
    return rows


# Scraping is combined with the model. It just seems easier to understand this way.

class BaseNode():
    # These should be overwritten
    def render(self):
        raise RuntimeError

    def __json__(self):
        raise RuntimeError(
            f"Can't encode type {type(self)}"
        )


# Nodes that contain other nodes inherit this
class CollectionNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.nodes = []

    def __iter__(self):
        for n in self.nodes:
            yield n

    def __repr__(self):
        return str([i for i in self.nodes])

    def append(self, node: BaseNode):
        self.nodes.append(node)

    def __json__(self):
        return {
            'nodes': self.nodes
        }


class AdhocNode(BaseNode):
    def __init__(self, source_element: bs4.Tag):
        self.text = source_element.text

    def __json__(self):
        return {
            "text": [self.text]
        }


class ErrorNode(BaseNode):
    def __init__(self, text):
        self.text = text

    def __json__(self):
        return {
            'text': [self.text]
        }


class CourseNode(BaseNode):
    def __init__(self, elem: bs4.Tag):
        super().__init__()

        html = str(elem)
        find = lambda pattern: re.findall(pattern, html)

        # Course name
        # Get between the a tags
        self.name = find(r'<a[^>]*>([^<]+)<\/a>')[0]  # TODO test case test for more than 1 here

        self.credits = self.find_credits(elem)

    def find_credits(self, elem):
        strong = elem.find_all('strong')
        for i in str(strong):
            if i.isdigit():
                return int(i)
        raise RuntimeError

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __json__(self):
        return {
            'name': self.name,
            'credits': self.credits
        }


# This is to store relationships between courses.
class RelationshipNode(CollectionNode):
    conditions = {
        'OR',
        # 'AND',
        # None
    }

    def __json__(self):
        return {
            'condition': self.condition,
            'nodes': self.nodes
        }

    def __init__(self, condition):
        super().__init__()

        self.condition = condition


# Check an HTML adhoc element for good elements to be turned into nodes
def checkAdhoc(source_element: bs4.Tag) -> list[bs4.Tag]:
    p_list = elemDirectChildren(source_element, 'p')

    if len(p_list) > 0:
        good = []
        for element in p_list:
            new = AdhocNode(element)

            # Element is bad ignore it
            if new.text.isspace():
                continue

            else:
                # Element is good and gets to go on the webpage
                good.append(element)
        return good
    else:
        return []


# Turn acalog-adhocs into GOOD elements
def cleanAdhoc(my_list: list[bs4.Tag]) -> list[bs4.Tag]:
    new_list = []

    i = 0
    while my_list:
        if elemHasClass(my_list[0], 'acalog-adhoc'):
            list_to_concat = checkAdhoc(my_list[0])
            my_list.pop(0)
            my_list = list_to_concat + my_list


        else:

            new_list.append(my_list[0])
            i += 1
            my_list.pop(0)

    return new_list


# Cores contain courses (As well as other cores)
class CoreNode(CollectionNode):
    def __init__(self, elem: bs4.Tag):
        super().__init__()
        html = str(elem)
        # self.parent = parent

        self.name = self.find_name(html)
        if self.name.isspace():
            raise ValueError

        self.heading = self.find_heading(html)

        # Determine if element has a list, and parse its data if so
        ul = self.find_ul(elem)
        if ul:
            self.nodes = self.find_nodes(ul)

        elif self.find_table(elem):
            self.nodes.append(
                ErrorNode(
                    "(Table not implemented)"
                )
            )

        self.text = self.find_text(elem)

    def find_table(self, elem):
        return elem.find_all('table')

    # HTML list (ul) element containing acalog-course and adhoc (il)
    def find_ul(self, source_element: bs4.Tag) -> Union[bs4.Tag, None]:
        mylist = elemDirectChildren(source_element, 'ul')
        if len(mylist) > 1:
            raise RuntimeError
        elif len(mylist) == 1:
            return mylist[0]
        else:
            return None

        #     pattern = r'acalog-course.*?<\/li>'
        # list_course_html = re.findall(pattern, html)

    # TODO This was built when using regex
    def find_nodes(self, source_element: bs4.Tag):
        master = []
        current_coll = master
        was_or = False

        il_elements = elemDirectChildren(source_element)
        il_elements = cleanAdhoc(il_elements)
        for i, element in enumerate(il_elements):
            # Is course
            if elemHasClass(element, 'acalog-course'):
                new_node = CourseNode(element)

            # Is adhoc
            else:
                new_node = AdhocNode(element)

            # The goal of this is to get the next HTML.
            def next_course_html():

                if i + 1 > len(il_elements) - 1:
                    return None
                else:
                    nex = il_elements[i + 1]
                    return str(nex)

            def find_is_or():
                html = next_course_html()
                pattern = r'>OR<'

                if html is None:  # Last course of core
                    return False
                else:
                    x = re.findall(pattern, html)

                    # regex returns a list.
                    return x  # Empty lists evaluate to False, while non-empty evaluates to True

            is_or = find_is_or()

            # In the middle of an OR
            if is_or and was_or:
                current_coll.append(new_node)

            # Starting an OR
            elif is_or:
                was_or = True

                new_coll = RelationshipNode('or')

                current_coll.append(new_coll)
                current_coll = new_coll

                current_coll.append(new_node)

            # End of OR
            elif was_or:
                was_or = False
                current_coll.append(new_node)
                current_coll = master

            # No OR
            else:
                current_coll.append(new_node)
        return master

    # This is different from adhoc-core. This is text attached to this node's HTML element
    def find_text(self, elem: bs4.Tag):
        a = elemDirectChildren(elem, 'p')  # Get direct children because it will go find the ORs (TODO ANDs?)

        texts = []
        for i in a:
            if not i.text.isspace():  # Some p tags have just blank space
                texts.append(i.text)

        return texts

    def __repr__(self):
        return f'{self.name}: {str(self.nodes)}'

    def __json__(self):
        return {
            'name': self.name,
            'heading': self.heading,
            'nodes': self.nodes,
            'text': self.text
        }

    # def propagate(self):

    # Find the core's heading number
    def find_heading(self, html):
        pattern = r'<h(\d)>'
        heading_value = re.findall(pattern, html)

        return heading_value[0]

    def find_name(self, html: str) -> str:
        # h\d finds h1-h5 headings, which are used to denote core
        a = re.findall(
            '\/a>([^<]+)(?:.(?!\/a))+h\d',  # FIXME backtracking will blow it up on big htmls
            html
        )

        if a == []:
            raise RuntimeError
            # return 'BROKEN'
        else:
            return a[0]  # TODO Testcase for more than 1


# TODO I feel like this should live inside of a class
# Recursively find cores
# This takes an HTML tag.
def recurseForCores(elem: bs4.Tag) -> CollectionNode:
    def nodeHasCoreChildren(node: bs4.Tag) -> bool:
        return c.find_all('div', class_='acalog-core') != []

    # We will be parsing cores and "lists" of cores.
    childs = elemDirectChildren(elem, 'div')  # Get all direct div children.
    new_nodes = CollectionNode()
    # "For tag every tag that is direct child of given HTML element"

    last_parent_node = None
    for c in childs:
        elem_class = c.get('class')[0]  # FIXME what if more than one

        # Element is a list
        if elem_class == 'custom_leftpad_20':
            f = recurseForCores(c)  # Recursively run this function and find it's children

            # For whatever reason, the parent and the child are siblings in the source HTML (FIXME different in some places?)
            last_parent_node.append(
                f
            )


        # Element is a core
        elif elem_class == 'acalog-core':
            new = CoreNode(c)
            new_nodes.append(new)
            last_parent_node = new

        else:
            raise RuntimeError(f'Bad class: {elem_class}')

    return new_nodes


# Programs contain cores
class ProgramNode(CollectionNode):
    def __init__(self, _id: str, name: str):
        super().__init__()

        self._id = _id
        self.name = name

        # html = self.make_html()

        # self.nodes = self.find_cores(html)

    def render(self):
        html = self.make_html()

        self.nodes = self.find_cores(html)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __json__(self):
        return {
            'name': self.name,
            'id': self._id,
            'nodes': self.nodes
        }

    def make_html(self) -> str:
        return cache_fetch(URL_PREVIEW + self._id)

    # Find all of the cores
    def find_cores(self, html) -> list[CoreNode]:
        # FIXME evil awful partition this and make it testable
        soup = BeautifulSoup(
            html, 'html.parser'
        )

        # Everything we care about is in a big fat td element
        a = findElementWithClassInSoup(
            soup,
            "td",
            'block_content'
        )

        table = a.findChild()  # First child will be this table. (Have to be specific because tables are everywhere)
        if not soupHasClass(table, 'table_default'):
            raise RuntimeError

        table_rows = elemDirectChildren(table)
        a = table_rows[1]  # TODO override implement every row
        if a.name != 'tr':  # This should be a table row
            raise RuntimeError

        core_div = a.find('div')  # First div contains list of cores

        # Purposefully throwing away the rest of this obj
        found_core = recurseForCores(core_div).nodes
        # Self will take on the nodes. This is necessary because of the way this function recurses

        return found_core


# Get list of all programs from Shepherd website
def get_program_list() -> list[ProgramNode]:
    # Get list of programs
    html = cache_fetch(URL_PROGRAMS)

    # Capture ID and name
    pattern = r'<a href="[^"]*poid=(\d+)[^"]*">([^<]+)</a>'
    matches = re.findall(pattern, html)

    l = []
    for program in matches:
        l.append(
            ProgramNode(program[0], program[1])
        )

    return l


def get_program(_id: int) -> ProgramNode:
    l = get_program_list()
    for program in l:
        if int(program._id) == _id:
            program.render()
            return program

    raise RuntimeError(f"Bad ID: {_id}")
