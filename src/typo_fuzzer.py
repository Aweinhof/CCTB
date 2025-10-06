from src.cctb import CCTB
import time


class TypoFuzzer:
    book = [
        ['i', 'l', 'I', '1'],
        ['o', '0'],
        ['m', 'rn']
    ]
    cctb = CCTB()

    def __init__(self, base_url):
        self.base_url = base_url
        self.tld = ""

    def hide_tld(self):
        splitted = self.base_url.split('.')
        self.tld = '.' + splitted[-1]
        self.base_url = '.'.join(splitted[:-1])

    def show_tld(self):
        self.base_url += self.tld

    def fuzz(self):
        self.hide_tld()

        lal = self.trick__look_alike()
        lal = [word + self.tld for word in lal]

        regex1 = self.trick__regex_single_char()
        regex1 = [word + self.tld for word in regex1]

        self.show_tld()

        print(lal)
        print()
        print(regex1)
        print('\n')

        # self.treat_domains(lal)
        self.treat_domains(regex1, True)

    def treat_domains(self, domains: list, isRegex: bool = False):
        for host in domains:
            print(host + ' :\n')
            indexes = self.cctb.get_indexes_filtered("*." + host)
            for index in indexes:
                print(index['url'])
            print('\n')
            time.sleep(20)

    def get_look_alike_chars(self, char):
        res = []
        for li in self.book:
            if char in li:
                for c in li:
                    if c.lower() != char.lower():
                        res.append(c)
        return res

    def trick__look_alike(self):
        domains = []
        for i in range(len(self.base_url)):
            if lal := self.get_look_alike_chars(self.base_url[i]):
                for ch in lal:
                    dom = self.base_url[:i] + ch + self.base_url[i + 1:]
                    dom = dom.lower()
                    if dom not in domains:
                        domains.append(dom)
        return domains

    def trick__regex_single_char(self):
        regexes = []
        for i in range(len(self.base_url) + 1):
            regexes.append(self.base_url[:i] + "*" + self.base_url[i:])
        return regexes
