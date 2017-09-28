'''
Chemical File Convert
Convert output and input file of MOPAC program
 - originally written by: Thien-Phuc Tu-Nguyen
 - current version: 0.2
 - last update: September 2017
 - by: Thien-Phuc Tu-Nguyen
 - tested on: Anaconda3 4.4
All right reserved
'''

class Mopac2016:
    def __init__(self):
        # Run information
        self.method = 'PM7'
        self.single = False
        self.freq_calc = False
        self.pdbout = False
        self.title = ''
        # Geometry
        self.atom = []
        self.x = []
        self.y = []
        self.z = []
        # Result
        self.prop_dict = {}
        
    def write_input(self,file_name):
        f = open(file_name,'w')
        f.write(self.method)
        if self.single:
            f.write(' 1SCF')
        if self.freq_calc:
            f.write(' FORCE FREQCY')
        if self.pdbout:
            f.write(' PDBOUT')
        f.write('\n' + self.title + '\n\n')
        for i in range(len(self.atom)):
            f.write('{:>3} {:12.8f} {:12.8f} {:12.8f}\n'.format(self.atom[i],self.x[i],self.y[i],self.z[i]))
        f.close()
    
    def read_output(self,file_name):
        filled_level = 0
        f = open(file_name,'r')
        temp = f.readline()
        self.freq = []
        while temp != '':
            if temp.find('TOTAL ENERGY') != -1:
                self.prop_dict['energy'] = float(temp.split()[3])
            if temp.find('COSMO AREA') != -1:
                self.prop_dict['area'] = float(temp.split()[3])
            if temp.find('COSMO VOLUME') != -1:
                self.prop_dict['volume'] = float(temp.split()[3])
            if temp.find('FINAL HEAT OF FORMATION') != -1:
                self.prop_dict['heat_formation'] = float(temp.split()[8])
            if temp.find('IONIZATION POTENTIAL') != -1:
                self.prop_dict['ionization'] = float(temp.split()[3])
            if temp.find('NO. OF FILLED LEVELS') != -1:
                filled_level = int(temp.split()[-1])
            if temp.find('CARTESIAN COORDINATES')!= -1 and filled_level != 0:
                temp = f.readline()
                temp = f.readline()
                self.atom = []
                self.x = []
                self.y = []
                self.z = []
                while temp != '\n':
                    temp = temp.split()
                    self.atom += [temp[1]]
                    self.x += [float(temp[2])]
                    self.y += [float(temp[3])]
                    self.z += [float(temp[4])]
                    temp = f.readline()
            if temp.find('DIPOLE') != -1 and temp.find('CHARGES') == -1:
                temp = f.readline()
                temp = f.readline()
                temp = f.readline()
                self.prop_dict['dipole'] = float(temp.split()[4])
            if temp.find('VIBRATION')!= -1 and temp.find('ENERGY CONTRIBUTION') != -1:
                temp = f.readline()
                if 'freq' not in self.prop_dict.keys():
                        self.prop_dict['freq'] = []
                self.prop_dict['freq'] += [float(temp.split()[1])]
                temp = f.readline()
            if temp.find('EIGENVALUES') != -1:
                temp = f.readline()
                raw = ''
                while temp != '\n':
                    raw += temp[:-1]
                    temp = f.readline()
                values = []
                for x in raw.split():
                    values += [float(x)]
                self.prop_dict['occupied'] = values[:filled_level]
                self.prop_dict['unoccupied'] = values[filled_level:]
            temp = f.readline()
        f.close()
    
    def copy_g09(self,original):
        self.atom = original.struct_dict['atom']
        self.x = original.struct_dict['x']
        self.y = original.struct_dict['y']
        self.z = original.struct_dict['z']
        self.title = original.run_dict['title']
        

