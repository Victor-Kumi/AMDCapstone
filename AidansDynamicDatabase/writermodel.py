from mongowrite import MongoWriter, DBInserter

class ModelDictionary(dict):
    def make_fields(self, *, hardware_id, specs_ls_of_dict, library_name, rocm_version, suite_name, added_fields=None, suite_data, plots=None, axis_titles=None):
        self['hardware_id'] = hardware_id
        self['specs_data'] = specs_ls_of_dict
        self['library_name'] = library_name
        self['rocm_version'] = rocm_version
        self['suite_name'] = suite_name
        self['field_types'] = ['HardWare-ID', 'Test-Suite', 'Version(s)', 'Graph', 'SpeedUp-Options']
        if added_fields:
            added_field_types = list(added_fields.keys())
            self['field_types'] = self['field_types'] + added_field_types
            self['added_field_values'] = list(added_fields.values())
        self['suite_data'] = suite_data
        self['plots'] = plots
        self['axis_titles'] = axis_titles
        if self['library_name'].lower() == 'rocfft' or self['library_name'].lower() == 'rocblas':  
            self['field_types'] = ['HardWare-ID', 'Test-Suite', 'Version(s)', 'Graph', 'SpeedUp-Options']
            self['plots'] = ['line', 'line+marker']
        if self['library_name'].lower() == 'rocfft':
            self['axis_titles'] = ['xlength','median'] 
        if  self['library_name'].lower() == 'rocblas':     
            self['axis_titles'] = ['rocblas-Gflops','us']

class DBWriter(MongoWriter):
    def __init__(self, dictobj, client_ip, client_port):
        self.data = dictobj
        self.inserter = DBInserter(client_ip, client_port)
        MongoWriter.__init__(self, self.inserter)
          
    def run_writer(self):
        self.suite_collection_name = self.data['hardware_id'].lower() + '/' + self.data['library_name'].lower() + '/' + self.data['rocm_version'].lower() + \
            '/'  + self.data['suite_name'].lower() 
    
        self.aux_db = 'REG_DATA'
        self.register_data()

    def __write_data_to_mongo(self):
        self.write_data_to_mongo(self.data['hardware_id'].lower(), self.suite_collection_name, self.data['suite_data'])

    def __register_suite_name(self):
        collection_name = self.data['library_name'].lower() + 'test-suitefieldvalue'
        ls_of_dicts = [{'name': self.data['suite_name']}]
        self.write_data_to_mongo(self.aux_db, collection_name, ls_of_dicts)

    def __register_hardware_id(self):
        collection_name = self.data['library_name'].lower() + 'hardware-idfieldvalue'
        ls_of_dicts = [{'name': self.data['hardware_id']}]
        self.write_data_to_mongo(self.aux_db, collection_name, ls_of_dicts)

    def __register_rocm_version(self):
        collection_name = self.data['library_name'].lower() + 'version(s)fieldvalue'
        ls_of_dicts = [{'name': self.data['rocm_version']}]
        self.write_data_to_mongo(self.aux_db, collection_name, ls_of_dicts)

    def __register_plots(self):
        collection_name = self.data['library_name'].lower() + 'graphfieldvalue'
        ls_of_dicts = [{'name': plot} for plot in self.data['plots']]
        self.write_data_to_mongo(self.aux_db, collection_name, ls_of_dicts)

    def __register_library(self):
        collection_name = 'libraries'
        ls_of_dicts = [{'name': self.data['library_name']}]
        self.write_data_to_mongo(self.aux_db, collection_name, ls_of_dicts)

    def __register_dash_field_types(self):
        collection_name = self.data['library_name'].lower() + 'field_type' 
        ls_of_dicts = [{'name': field_type} for field_type in self.data['field_types'] if self.data['field_types'] is not None and isinstance(self.data['field_types'], list)]
        self.write_data_to_mongo(self.aux_db, collection_name, ls_of_dicts)
        
    def __register_axis_titles(self):
        if self.data['axis_titles'] is not None:
            collection_name = self.data['library_name'].lower() + 'plot_axis'
            ls_of_dicts = [{'name': title} for title in self.data['axis_titles']]  
            self.write_data_to_mongo(self.aux_db, collection_name, ls_of_dicts)
        else: 
            pass 
    
    def __register_field_values(self):
        if len(self.data['field_types']) > 5:
            for i in range(len(self.data['field_types'][5:])):
                collection_name = self.data['library_name'].lower() + self.data['field_types'][5:][i].lower() + 'fieldvalue'
                ls_of_dicts = [{'name': field_value} for field_value in self.data['added_field_values'][i]]
                self.write_data_to_mongo(self.aux_db, collection_name, ls_of_dicts)
        else:
            pass        

    def __write_specs_to_mongo(self):
        collection_name = self.data['hardware_id'].lower() + '/' + self.data['library_name'].lower() + '/' + self.data['rocm_version'].lower() + \
            '/'  + self.data['suite_name'].lower() +  'hostspecs' 
        ls_of_dicts =  [self.data['specs_data'][0]['Host info']]  
        self.write_data_to_mongo(self.aux_db, collection_name, ls_of_dicts) 

        collection_name = self.data['hardware_id'].lower() + '/' + self.data['library_name'].lower() + '/' + self.data['rocm_version'].lower() + \
            '/'  + self.data['suite_name'].lower() +  'devicespecs'
        ls_of_dicts =  [self.data['specs_data'][1]['Device info']]  
        self.write_data_to_mongo(self.aux_db, collection_name, ls_of_dicts) 

    def __write_gpu_rocm_specs(self):
        collection_name =  self.data['hardware_id'].lower() + '/' + self.data['rocm_version'] + '/' + 'hostspecs'
        ls_of_dicts =  [self.data['specs_data'][0]['Host info']] 
        self.write_data_to_mongo(self.aux_db, collection_name, ls_of_dicts)

        collection_name =  self.data['hardware_id'].lower() + '/' + self.data['rocm_version'] + '/' + 'devicespecs'
        ls_of_dicts =  [self.data['specs_data'][1]['Device info']] 
        self.write_data_to_mongo(self.aux_db, collection_name, ls_of_dicts)



    def register_data(self):
        self.__register_dash_field_types()
        self.__register_field_values()
        self.__register_hardware_id()
        self.__register_library()
        self.__register_axis_titles()
        self.__register_suite_name()
        self.__register_rocm_version()
        self.__register_plots()
        self.__write_specs_to_mongo()
        self.__write_gpu_rocm_specs()
        self.__write_data_to_mongo()


