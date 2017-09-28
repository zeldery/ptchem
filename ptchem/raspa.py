'''
RASPA 2.0 reader and modifier
Extract the data from RASPA 2.0 output file
 - originally written by: Nhut-Minh Bui
 - current version: 0.2
 - last update: September 2017
 - by: Thien-Phuc Tu-Nguyen
 - tested on: Anaconda3 4.4
All right reserved
'''

import pandas as pd

class Raspa2():
    def __init__(self):
        # Output information
        self.energy = []
        self.cycle = []
        self.units = []
        self.adsorb = [ [] , [] , [] , [] , [] ]
        
        # Input information
        self.general = {}
        self.framework = []
        self.component = []
    
    def reset(self):
        self.energy = []
        self.cycle = []
        self.units = []
        self.adsorb = [ [] , [] , [] , [] , [] ]
    
    def _get_unit(self,st):
        i = 0
        ind = 0
        for i in range(len(st)):
            if st[i] == '[':
                ind = i 
            if st[i] == ']':
                self.units.append(st[ind:(i+1)])
    
    def _get_num(self,st):
        ind1 = 0
        ind2 = 0	
        st = st[:-1]
        st = st.replace(',',' ')
        
        while st.rfind(')') != -1: 
            ind1 = st.rfind('(')
            ind2 = st.rfind(')')
            st = st.replace(st[(ind1-1):(ind2+1)],' ')	
            
        while st.rfind(']') != -1:
            ind1 = st.rfind('[')
            ind2 = st.rfind(']')
            st = st.replace(st[(ind1-1):(ind2+1)],' ')
    
        if len(st.split()) == 3:
            tmp = st.split()
            self.adsorb[0].append(float(tmp[0]))
            self.adsorb[1].append(float(tmp[1]))
            self.adsorb[2].append(float(tmp[2]))
        else:
            tmp = st.split()
            self.adsorb[3].append(float(tmp[0]))
            self.adsorb[4].append(float(tmp[1]))
        
    def to_csv(self,name):
        dat = pd.DataFrame({'N' : self.cycle, 'E' : self.energy, self.units[0] : self.adsorb[0],
                          self.units[1] : self.adsorb[1] , self.units[2] : self.adsorb[2] , 
                          self.units[3] : self.adsorb[3] , self.units[4] : self.adsorb[4]})
        dat = dat.iloc[:,[1,0,2,3,4,5,6]]
        dat.to_csv(name,index = False)
        
    def read_output(self,name):
        f = open(name,"r+")
        s00 = '[Init] Current cycle:'
        s01 = 'Current cycle:'
        s02 = 'absolute adsorption:'
        s03 = 'Current total potential energy:'
        l00 = len(s00)
        l01 = len(s01)
        l02 = len(s02)
        l03 = len(s03)
        n = 0 
        tmpp = 0
        m = -1
        ncycle = -1
        trace = False
        #Getting Unit Array
        tmp = f.readline()
        while tmp != '':
            if tmp.rfind(s02) != -1:
                st = tmp.replace(s02,' ')
                self._get_unit(st)
                st = f.readline()
                self._get_unit(st)
                break
            tmp = f.readline()
        #Getting Numbers of Current Cycle, Current total potential energy: 
        tmp = f.readline()
        while tmp != '':
            # Getting Number of Current Cycle
            if (tmp.rfind(s01) != -1) and (tmp.rfind(s01) == 0):
                ind1 = tmp.rfind(s01) + l01 + 1
                ind2 = tmp.rfind('out') - 1
                tmpp = int(tmp[ind1:ind2])
                trace = True
            # Getting Number of Absolute Adsorption and Energy
            while trace:
                tmp = f.readline()
                if tmp.rfind(s02) != -1:
                    st = tmp.replace(s02,' ')
                    self._get_num(st)             
                    st = f.readline()
                    self._get_num(st)
                if tmp.find(s03) != -1:
                    ind1 = tmp.rfind(s03) + l03 + 1
                    ind2 = tmp.rfind('[') - 1
                    self.energy.append(float(tmp[ind1:ind2]))
                    self.cycle.append(int(tmpp))
                    trace = False
            tmp = f.readline()
    
    def read_input(self,name):
        f = open(name,'r')
        mode = 'G'
        temp = f.readline()
        while temp != '':
            dat = temp.split()
            if len(dat) == 0:
                temp = f.readline()
                continue
            if dat[0] == 'Framework':
                mode = 'F'
                self.framework += [{'Name':dat[1]}]
                dat = dat[2:]
            if len(dat) == 0:
                temp = f.readline()
                continue
            if dat[0] == 'Component':
                mode = 'C'
                self.component += [{'Name':dat[1]}]
                dat = dat[2:]
            if len(dat)>=2:
                if mode == 'G':
                    self.general[dat[0]] = dat[1]
                if mode == 'F':
                    if len(dat) == 2:
                        self.framework[-1][dat[0]] = dat[1]
                    else:
                        self.framework[-1][dat[0]] = dat[1:]
                if mode == 'C':
                    if len(dat) == 2:
                        self.component[-1][dat[0]] = dat[1]
                    else:
                        self.component[-1][dat[0]] = dat[1:]
            # To be continued
            temp = f.readline()
            
        f.close()
        
    def write_input(self,name):
        f = open(name,'w')
        for index,content in self.general.items():
            if isinstance(content,list):
                f.write(index)
                for sub_content in content:
                    f.write(' ' + str(sub_content))
                f.write('\n')
            else:
                f.write(index + ' ' + str(content) + '\n' )
        f.write('\n')
        for frame in self.framework:
            f.write('Framework ' + str(frame['Name']) + '\n')
            for index,content in frame.items():
                if index != 'Name':
                    if isinstance(content,list):
                        f.write(index)
                        for sub_content in content:
                            f.write(' ' + str(sub_content))
                        f.write('\n')
                    else:
                        f.write(index + ' ' + str(content) + '\n' )
            f.write('\n')
        for component in self.component:
            f.write('Component ' + str(component['Name']) + '\n')
            for index,content in component.items():
                if index != 'Name':
                    if isinstance(content,list):
                        f.write(index)
                        for sub_content in content:
                            f.write(' ' + str(sub_content))
                        f.write('\n')
                    else:
                        f.write(index + ' ' + str(content) + '\n' )
            f.write('\n')
        f.close()
        
    def plot_energy(self,name = None):
        pass
    
    def plot_adsorption(self,unit = 0, name = None):
        pass
    
    
