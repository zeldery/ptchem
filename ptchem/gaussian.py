'''
Chemical File Convert
Convert output and input file of Gaussian 09 program
 - originally written by: Thien-Phuc Tu-Nguyen
 - current version: 0.2
 - last update: September 2017
 - by: Thien-Phuc Tu-Nguyen
 - tested on: Anaconda3 4.4
All right reserved
'''


class Gaussian09:
    
    def __init__(self,energy_search_str = ''):
        # Run attributes:
        self.run_dict = {}
        # Energy search
        self.energy_search_str = energy_search_str
        # Molecule information
        self.struct_dict = {}
        # Properties information
        self.prop_dict = {}
        
    def read_input(self,file_name):
        f = open(file_name,'r')
        line = f.readline()
        while line != '\n' and line != ' \n':
            line = line[:-1]
            if line.lower().find('%nproc') != -1:
                self.run_dict['processor'] = int(line.split('=')[1])
            if line.lower().find('%mem') != -1:
                self.run_dict['mem'] = line.split('=')[1]
            if line.lower().find('%chk') != -1:
                self.run_dict['chk'] = line.split('=')[1]
            if line.find('#') != -1:
                self.run_dict['modified'] = line.split('#')[1]
            line = f.readline()
        line = f.readline()
        self.run_dict['title'] = line[:-1]
        line = f.readline()
        line = f.readline()
        line = line[:-1]
        self.struct_dict['charge'] = int(line.split()[0])
        self.struct_dict['spin'] = int(line.split()[1])
        self.struct_dict['atom'] = []
        self.struct_dict['x'] = []
        self.struct_dict['y'] = []
        self.struct_dict['z'] = []
        line = f.readline()
        while line != '' and line != '\n' and line != ' \n':
            line = line[:-1]
            temp = line.split()
            self.struct_dict['atom'] += [temp[0]]
            if len(temp) == 4:
                self.struct_dict['x'] += [float(temp[1])]
                self.struct_dict['y'] += [float(temp[2])]
                self.struct_dict['z'] += [float(temp[3])]
            if len(temp) == 5:
                self.struct_dict['x'] += [float(temp[2])]
                self.struct_dict['y'] += [float(temp[3])]
                self.struct_dict['z'] += [float(temp[4])]
            line = f.readline()
        self.run_dict['add_info'] = ''
        line = f.readline()
        while line != '':
            self.run_dict['add_info'] += line
            line = f.readline()
        f.close()
    
    def read_output(self,file_name):
        f = open(file_name,'r')
        finish_tag = False
        temp = None
        while not finish_tag:
            temp = f.readline()
            if temp == '':
                finish_tag = True
            if temp.find('Dipole moment (field-independent basis, Debye)') != -1:
                temp = f.readline()
                self.prop_dict['dipole'] = float(temp[84:-1])
                temp = f.readline()
            if temp.find(' Alpha  occ. eigenvalues --') != -1:
                self.prop_dict['occupied'] = []
                self.prop_dict['unoccupied'] = []
                values = temp[27:-1]
                temp = f.readline()
                while temp.find(' Alpha  occ. eigenvalues --') != -1:
                    values += temp[27:-1]
                    temp = f.readline()
                for number in values.split():
                    if len(number) == 20:
                        self.prop_dict['occupied'] += [float(number[:10])]
                        self.prop_dict['occupied'] += [float(number[10:])]
                    elif len(number) == 30:
                        self.prop_dict['occupied'] += [float(number[:10])]
                        self.prop_dict['occupied'] += [float(number[10:20])]
                        self.prop_dict['occupied'] += [float(number[20:])]
                    else:
                        self.prop_dict['occupied'] += [float(number)]
                values = temp[27:-1]
                while temp.find(' Alpha virt. eigenvalues --') != -1:
                    values += temp[27:-1]
                    temp = f.readline()
                for number in values.split():
                    self.prop_dict['unoccupied'] += [float(number)]
            if temp.find(' Excited State') != -1:
                if 'wave' not in self.prop_dict.keys():
                    self.prop_dict['wave'] = []
                    self.prop_dict['os'] = []
                self.prop_dict['wave'] += [float(temp.split()[6])]
                self.prop_dict['os'] += [float(temp.split()[8][2:])]
                temp = f.readline()
            if temp.find('SCF Done:  E('+self.energy_search_str+')') != -1:
                value = temp[(temp.find('=')+1):-1]
                self.prop_dict['energy'] = float(value.split()[0])
                temp = f.readline()
            if temp.find(' Frequencies --') != -1:
                if 'freq' not in self.prop_dict.keys():
                    self.prop_dict['freq'] = []
                    self.prop_dict['inten'] = []
                temp = temp.split()[2:]
                for num in temp:
                    self.prop_dict['freq'] += [float(num)]
                temp = f.readline()
                temp = f.readline()
                temp = f.readline()
                temp = temp.split()[3:]
                for num in temp:
                    self.prop_dict['inten'] += [float(num)]
                temp = f.readline()
            if temp.find('Octapole moment (field-independent basis, Debye-Ang**2):') != -1:
                temp = f.readline()
                self.prop_dict['xxx'] = float(temp[6:28])
                self.prop_dict['yyy'] = float(temp[34:52])
                self.prop_dict['zzz'] = float(temp[58:78])
                self.prop_dict['xyy'] = float(temp[84:-1])
                temp = f.readline()
                self.prop_dict['xxy'] = float(temp[6:28])
                self.prop_dict['xxz'] = float(temp[34:52])
                self.prop_dict['xzz'] = float(temp[58:78])
                self.prop_dict['yzz'] = float(temp[84:-1])
                temp = f.readline()
                self.prop_dict['yyz'] = float(temp[6:28])
                self.prop_dict['xyz'] = float(temp[34:52])
                self.prop_dict['octapole'] = (self.prop_dict['xxx'] + self.prop_dict['xyy'] + self.prop_dict['xzz']) **2
                self.prop_dict['octapole'] += (self.prop_dict['xyy'] + self.prop_dict['yzz'] + self.prop_dict['xxy']) **2
                self.prop_dict['octapole'] += (self.prop_dict['zzz'] + self.prop_dict['xxz'] + self.prop_dict['yyz']) **2
                self.prop_dict['octapole'] = self.prop_dict['octapole'] ** 0.5
            if temp.find('Zero-point correction=') != -1:
                self.prop_dict['zero_correction'] = float(temp[42:58])
                temp = f.readline()
                self.prop_dict['energy_correction'] = float(temp[42:58])
                temp = f.readline()
                self.prop_dict['enthalpy_correction'] = float(temp[42:58])
                temp = f.readline()
                self.prop_dict['gibbs_correction'] = float(temp[42:58])
                temp = f.readline()
                self.prop_dict['zero_sum'] = float(temp[46:])
                temp = f.readline()
                self.prop_dict['energy_sum'] = float(temp[46:])
                temp = f.readline()
                self.prop_dict['enthalpy_sum'] = float(temp[46:])
                temp = f.readline()
                self.prop_dict['gibbs_sum'] = float(temp[46:])
                temp = f.readline()                 
            if temp.find(' 1\\1\\') != -1 or temp.find(' 1|1|') != -1:
                sep = temp[2]
                next_line = f.readline()
                while next_line.find('@') == -1:
                    temp = temp[:-1] + next_line[1:]
                    next_line = f.readline()
                temp = temp[:-1] + next_line[1:-1]
                temp = temp[5:-1]
                info = temp.split(sep*2)
                # Basic infomation of the run
                temp = info[0].split(sep)
                self.run_dict['run_type'] = temp[1]
                self.run_dict['method'] = temp[2]
                self.run_dict['basis_set'] = temp[3]
                # The title
                self.run_dict['title'] = info[2]
                # The coordination
                sub_info = info[3].split(sep)
                self.struct_dict['charge'] = int(sub_info[0].split(',')[0])
                self.struct_dict['spin'] = int(sub_info[0].split(',')[1])
                del sub_info[0]
                self.struct_dict['atom'] = []
                self.struct_dict['x'] = []
                self.struct_dict['y'] = []
                self.struct_dict['z'] = []
                for atom in sub_info:
                    temp = atom.split(',')
                    self.struct_dict['atom'] += [temp[0]]
                    if len(temp) == 4:
                        self.struct_dict['x'] += [float(temp[1])]
                        self.struct_dict['y'] += [float(temp[2])]
                        self.struct_dict['z'] += [float(temp[3])]
                    if len(temp) == 5:
                        self.struct_dict['x'] += [float(temp[2])]
                        self.struct_dict['y'] += [float(temp[3])]
                        self.struct_dict['z'] += [float(temp[4])]
        f.close()
    
    def write_input(self,file_name):
        f = open(file_name,'w')
        if 'processor' in self.run_dict.keys():
            f.write('%nprocshared='+str(self.run_dict['processor'])+'\n')
        if 'chk' in self.run_dict.keys():
            f.write('%chk='+self.run_dict['chk']+'\n')
        if 'mem' in self.run_dict.keys() :
            f.write('%mem='+self.run_dict['mem']+'\n')
        f.write('#{} {}/{}'.format(self.run_dict['run_type'],self.run_dict['method'],self.run_dict['basis_set']))
        if 'modified' in self.run_dict.keys():
            f.write(' {}\n'.format(self.run_dict['modified']))
        else:
            f.write('\n')
        f.write('\n')
        f.write(self.run_dict['title']+'\n')
        f.write('\n')
        f.write(str(self.struct_dict['charge'])+' '+str(self.struct_dict['spin'])+'\n')
        for i in range(len(self.struct_dict['atom'])):
            f.write('{:2s} {:14.8f} {:14.8f} {:14.8f}\n'.format(self.struct_dict['atom'][i],self.struct_dict['x'][i],self.struct_dict['y'][i],self.struct_dict['z'][i]))
        f.write('\n')
        if 'add_info' in self.run_dict.keys():
            f.write(self.add_info)
        f.close()
        
    def write_xyz(self,file_name):
        f = open(file_name,'w')
        f.write(self.run_dict['title'] + '\n')
        f.write('\n')
        for i in range(len(self.struct_dict['atom'])):
            f.write('{:2s} {:14.8f} {:14.8f} {:14.8f}\n'.format(self.struct_dict['atom'][i],self.struct_dict['x'][i],self.struct_dict['y'][i],self.struct_dict['z'][i]))
        f.close()
