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

import os

class Collector:
    def __init__(self,properties = '', energy_search_str = ''):
        self.special = ['HOMO','LUMO','HOMO-1','LUMO+1','fmax','Lmax','Inten','OS']
        self.properties = properties
        self.energy_search_str = energy_search_str
    
    def collect_g09(self,src = '.'):
        if len(self.properties) == 0:
            raise ValueError('The properties contains nothing')
        if src[-1] == '/':
            src = src[:-1]
        list_file = os.listdir(src)
        descriptor = []
        x = G09Info(self.energy_search_str)
        x.readg09out(src + '/' + list_file[0])
        for describ in self.properties:
            if describ in x.prop_dict.keys() or describ in self.special:
                descriptor += [describ]
            else:
                raise IndexError('The descriptor is not available')
        dat = pd.DataFrame(index = list_file, columns = descriptor)
        for name in list_file:
            x = G09Info(self.energy_search_str)
            x.readg09out(src + '/' + name)
            for describ in descriptor:
                if describ in x.prop_dict:
                    dat.loc[name,describ] = x.prop_dict[describ]
                else:
                    if describ == 'HOMO':
                        dat.loc[name,describ] = x.prop_dict['occupied'][-1]
                    elif describ == 'LUMO':
                        dat.loc[name,describ] = x.prop_dict['unoccupied'][0]
                    elif describ == 'HOMO-1':
                        dat.loc[name,describ] = x.prop_dict['occupied'][-2]
                    elif describ == 'LUMO+1':
                        dat.loc[name,describ] = x.prop_dict['unoccupied'][1]
                    elif describ == 'inten':
                        dat.loc[name,describ] = max(x.prop_dict['inten'])
                    elif describ == 'fmax':
                        ind = x.prop_dict['inten'].index(max(x.prop_dict['inten']))
                        dat.loc[name,describ] = x.prop_dict['freq'][ind]
                    elif describ == 'OS':
                        dat.loc[name,describ] = max(x.prop_dict['OS'])
                    elif describ == 'Lmax':
                        ind = x.prop_dict['OS'].index(max(x.prop_dict['OS']))
                        dat.loc[name,describ] = x.prop_dict['wave'][ind]
        dat['Name'] = dat.index
        for name in dat.index:
            dat.loc[name,'Name'] = name[:-4]
        dat.index = dat['Name']    
        self.dat = dat.drop(['Name'],axis = 1)
        
    def to_csv(self,name):
        self.dat.to_csv(name)
