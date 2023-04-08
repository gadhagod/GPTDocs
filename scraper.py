from requests import get
from bs4 import BeautifulSoup, Tag
from json import dumps

class Page():
    def __init__(self, url):
        self.page = get(url).text
        self.sections = []
        soup = BeautifulSoup(self.page, "html.parser")
        start = soup.find("p")
        try:
            self.sections.append(start.get_text())
        except AttributeError:
            return
        self.addSection(start)
    
    def addSection(self, start):    
        curr_section = ""
        for elem in start.next_siblings:
            if elem.name == "h2" or elem.name == "h3":
                curr_soup = BeautifulSoup(curr_section, features="lxml")
                self.sections.append(curr_soup.getText())
                curr_section = ""
            else:
                curr_section += elem.__str__()
                
class RocksetDocs():
    def __init__(self):
        soup = BeautifulSoup(get("https://rockset.com/docs").text, "html.parser")
        sidebarItems = soup.find_all("a", {"class": lambda value: value and value.startswith("Sidebar__Item")})
        for i in range(len(sidebarItems)):
            sidebarItems[i] = f"https://rockset.com{sidebarItems[i]['href']}"
        self.sections = []
        for pageUrl in sidebarItems:
            self.sections = self.sections + Page(pageUrl).sections