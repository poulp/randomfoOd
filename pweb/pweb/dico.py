#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import xml.etree.ElementTree as ET

class gramary():
    dictionary = {'singular' : "", 'plural': "", 'gender': ""}
    root = ET

    def research(self, word):
        queryHTML = 'http://fr.wiktionary.org/wiki/'+word
        HTMLresponse = urllib2.urlopen(queryHTML.encode(encoding='utf-8'))
        self.root = ET.fromstring(HTMLresponse.read())
        self.find_number()
        self.find_gender()
        return self.get_dictionary()

    def find_number(self):
        """
        Retourne le pluriel d'un mot singulier.
        """
        results = list()
        for table in self.root.iter('table'):
            if table.get('class') == "flextable flextable-fr-mfsp":
                for td in table.iter('td'):
                    if len(results) == 2:
                        break
                    try:
                        results.append(td.find('strong').text)
                    except AttributeError:
                        pass
                    try:
                        results.append(td.find('a').text)
                    except AttributeError:
                        pass
                if len(results) > 0:
                    self.set_dictionary('singular',results.pop(0))
                    self.set_dictionary('plural',results.pop(0))
                    return 0;


        # word was not found in the preceding case.
        for ol in self.root.iter('ol'):
            try:
                print ol.find('li').find('a').text
                self.research(ol.find('li').find('a').text)
                break
            except AttributeError:
                pass

        #for b in self.root.iter('b'):
        #    try:
        #        print b.find('a').text
        #        self.research(b.find('a').text)
        #        break;
        #    except AttributeError:
        #        pass

    def find_gender(self):
        """
        Retourne m : masculin ou f : pour féminin.
        """
        for p in self.root.iter('p'):
            try:
                i = (p.find('span').find('i').text).encode(encoding='utf-8')
                if cmp(i, "masculin") == 0 or cmp(i,"féminin") == 0:
                    self.set_dictionary('gender', i[0])
            except AttributeError:
                pass

    def get_dictionary(self):
        return self.dictionary

    def set_dictionary(self,key,value):
        self.dictionary[key] = value


if __name__ == "__main__":
## Exemple d'utilisation ##
    g = gramary()
    #print g.research('enveloppe')
    #print g.research('tableaux')
    #print g.research('tableau')
    print g.research('sucre')




    print g.research('fenêtres')