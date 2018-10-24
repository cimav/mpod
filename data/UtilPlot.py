'''
Created on 17/10/2018

@author: Jorge Alberto Torres Acosta
'''

from data.Utils import *
import re
from data.WebT4 import * 
from data.WebRankTensors import *
from data.Magnetic import *
from data.Tensor import *

    

class Elasticity(BaseTensor):
    '''
    classdocs
    '''
    
    def __init__(self, *args):
        super(Elasticity, self).__init__(*args)


    def ComplianceAndYoungModulus(self):

        file_name, create_stl, file_nameYoungModulus,create_stlym   = self.getdata()
        
        self.jason_data['filename1'] = file_name
        self.jason_data['filenameYoungModulus'] = file_nameYoungModulus
        

        compliance = ComplianceT4()
        compliance.Compliance(self.valueij.value11,self.valueij.value12,self.valueij.value13,self.valueij.value14,self.valueij.value15,self.valueij.value16,self.valueij.value21,self.valueij.value22,self.valueij.value23,self.valueij.value24,self.valueij.value25,self.valueij.value26,self.valueij.value31,self.valueij.value32,self.valueij.value33,self.valueij.value34,self.valueij.value35,self.valueij.value36,self.valueij.value41,self.valueij.value42,self.valueij.value43,self.valueij.value44,self.valueij.value45,self.valueij.value46,self.valueij.value51,self.valueij.value52,self.valueij.value53,self.valueij.value54,self.valueij.value55,self.valueij.value56,self.valueij.value61,self.valueij.value62,self.valueij.value63,self.valueij.value64,self.valueij.value65,self.valueij.value66,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
        """XEC=compliance.stringValsOfXEC
        YEC = compliance.stringValsOfYEC
        ZEC= compliance.stringValsOfZEC"""
        
        self.jason_data['XEC'] = compliance.stringValsOfXEC
        self.jason_data['YEC'] = compliance.stringValsOfYEC
        self.jason_data['ZEC'] = compliance.stringValsOfZEC
   
        surfacecolorcompliance=   compliance.surfacecolorcompliance
        self.jason_data['surfacecolor'] = compliance.surfacecolorcompliance
        
        compliance.YoungModulus(self.valueij.value11,self.valueij.value12,self.valueij.value13,self.valueij.value14,self.valueij.value15,self.valueij.value16,self.valueij.value21,self.valueij.value22,self.valueij.value23,self.valueij.value24,self.valueij.value25,self.valueij.value26,self.valueij.value31,self.valueij.value32,self.valueij.value33,self.valueij.value34,self.valueij.value35,self.valueij.value36,self.valueij.value41,self.valueij.value42,self.valueij.value43,self.valueij.value44,self.valueij.value45,self.valueij.value46,self.valueij.value51,self.valueij.value52,self.valueij.value53,self.valueij.value54,self.valueij.value55,self.valueij.value56,self.valueij.value61,self.valueij.value62,self.valueij.value63,self.valueij.value64,self.valueij.value65,self.valueij.value66,self.color[0],file_nameYoungModulus,self.res,self.stl_dir,create_stlym,self.createdata)
        youngModulusXEC=compliance.stringValsOfXEC2
        youngModulusYEC = compliance.stringValsOfYEC2
        youngModulusZEC= compliance.stringValsOfZEC2    
        self.jason_data['youngModulusXEC'] = compliance.stringValsOfXEC2
        self.jason_data['youngModulusYEC'] = compliance.stringValsOfYEC2
        self.jason_data['youngModulusZEC'] = compliance.stringValsOfZEC2
        
        #surfacecolorYoungModulus=   compliance.surfacecolorYoungModulus 
        self.jason_data['surfacecolorYoungModulus'] = compliance.surfacecolorYoungModulus
        
        del compliance
     
    def ComplianceAndYoungModulusAndPoly(self):  
        
        self.ComplianceAndYoungModulus()

        file_name, create_stl, file_nameYoungModulus,create_stlym   = self.getdatapoly()
        
        self.jason_data_poly['filename1'] = file_name
        self.jason_data_poly['filenameYoungModulus'] = file_nameYoungModulus
        
        compliance = ComplianceT4()
        compliance.Compliance(self.valij.val1,self.valij.val2,self.valij.val3,self.valij.val4,self.valij.val5,self.valij.val6,self.valij.val7,self.valij.val8,self.valij.val9,self.valij.val10,self.valij.val11,self.valij.val12,self.valij.val13,self.valij.val14,self.valij.val15,self.valij.val16,self.valij.val17,self.valij.val18,self.valij.val19,self.valij.val20,self.valij.val21,self.valij.val22,self.valij.val23,self.valij.val24,self.valij.val25,self.valij.val26,self.valij.val27,self.valij.val28,self.valij.val29,self.valij.val30,self.valij.val31,self.valij.val32,self.valij.val33,self.valij.val34,self.valij.val35,self.valij.val36,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
       
        """XEC=compliance.stringValsOfXEC
        YEC = compliance.stringValsOfYEC
        ZEC= compliance.stringValsOfZEC"""
        self.jason_data_poly['XEC'] = compliance.stringValsOfXEC
        self.jason_data_poly['YEC'] = compliance.stringValsOfYEC
        self.jason_data_poly['ZEC'] = compliance.stringValsOfZEC
   
        #surfacecolorcompliancepoly=   compliance.surfacecolorcompliance
        self.jason_data_poly['surfacecolor'] = compliance.surfacecolorcompliance
        
        compliance.YoungModulus(self.valij.val1,self.valij.val2,self.valij.val3,self.valij.val4,self.valij.val5,self.valij.val6,self.valij.val7,self.valij.val8,self.valij.val9,self.valij.val10,self.valij.val11,self.valij.val12,self.valij.val13,self.valij.val14,self.valij.val15,self.valij.val16,self.valij.val17,self.valij.val18,self.valij.val19,self.valij.val20,self.valij.val21,self.valij.val22,self.valij.val23,self.valij.val24,self.valij.val25,self.valij.val26,self.valij.val27,self.valij.val28,self.valij.val29,self.valij.val30,self.valij.val31,self.valij.val32,self.valij.val33,self.valij.val34,self.valij.val35,self.valij.val36,self.color[0],file_nameYoungModulus,self.res,self.stl_dir,create_stlym,self.createdata)
        """youngModulusXEC=compliance.stringValsOfXEC2
        youngModulusYEC = compliance.stringValsOfYEC2
        youngModulusZEC= compliance.stringValsOfZEC2"""
        self.jason_data_poly['youngModulusXEC'] = compliance.stringValsOfXEC2
        self.jason_data_poly['youngModulusYEC'] = compliance.stringValsOfYEC2
        self.jason_data_poly['youngModulusZEC'] = compliance.stringValsOfZEC2
        
        #surfacecolorYoungModuluspoly=   compliance.surfacecolorYoungModulus 
        self.jason_data_poly['surfacecolorYoungModulus'] = compliance.surfacecolorYoungModulus
        
        del compliance
    
   
    def StiffnessAndYoungModulus(self):

        file_name, create_stl, file_nameYoungModulus,create_stlym   = self.getdata()
        
        self.jason_data['filename1'] = file_name
        self.jason_data['filenameYoungModulus'] = file_nameYoungModulus
        

        stiffness = StiffnessT4()
        stiffness.Stiffness(self.valueij.value11,self.valueij.value12,self.valueij.value13,self.valueij.value14,self.valueij.value15,self.valueij.value16,self.valueij.value21,self.valueij.value22,self.valueij.value23,self.valueij.value24,self.valueij.value25,self.valueij.value26,self.valueij.value31,self.valueij.value32,self.valueij.value33,self.valueij.value34,self.valueij.value35,self.valueij.value36,self.valueij.value41,self.valueij.value42,self.valueij.value43,self.valueij.value44,self.valueij.value45,self.valueij.value46,self.valueij.value51,self.valueij.value52,self.valueij.value53,self.valueij.value54,self.valueij.value55,self.valueij.value56,self.valueij.value61,self.valueij.value62,self.valueij.value63,self.valueij.value64,self.valueij.value65,self.valueij.value66,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
        if stiffness.error == None:
            self.jason_data['error']  = stiffness.error
            self.jason_data['XEC'] = stiffness.stringValsOfXEC
            self.jason_data['YEC'] = stiffness.stringValsOfYEC
            self.jason_data['ZEC'] = stiffness.stringValsOfZEC
    
            self.jason_data['surfacecolor'] = stiffness.surfacecolorstiffness
            
            stiffness.YoungModulus(self.valueij.value11,self.valueij.value12,self.valueij.value13,self.valueij.value14,self.valueij.value15,self.valueij.value16,self.valueij.value21,self.valueij.value22,self.valueij.value23,self.valueij.value24,self.valueij.value25,self.valueij.value26,self.valueij.value31,self.valueij.value32,self.valueij.value33,self.valueij.value34,self.valueij.value35,self.valueij.value36,self.valueij.value41,self.valueij.value42,self.valueij.value43,self.valueij.value44,self.valueij.value45,self.valueij.value46,self.valueij.value51,self.valueij.value52,self.valueij.value53,self.valueij.value54,self.valueij.value55,self.valueij.value56,self.valueij.value61,self.valueij.value62,self.valueij.value63,self.valueij.value64,self.valueij.value65,self.valueij.value66,self.color[0],file_nameYoungModulus,self.res,self.stl_dir,create_stlym,self.createdata)
    
            self.jason_data['youngModulusXEC'] = stiffness.stringValsOfXEC2
            self.jason_data['youngModulusYEC'] = stiffness.stringValsOfYEC2
            self.jason_data['youngModulusZEC'] = stiffness.stringValsOfZEC2
    
            self.jason_data['surfacecolorYoungModulus'] = stiffness.surfacecolorYoungModulus
        else:
            self.jason_data['error'] = stiffness.error
        
        del stiffness
     
    def StiffnessAndYoungModulusAndPoly(self):  
        
        self.StiffnessAndYoungModulus()

        file_name, create_stl, file_nameYoungModulus,create_stlym   = self.getdatapoly()
        
        self.jason_data_poly['filename1'] = file_name
        self.jason_data_poly['filenameYoungModulus'] = file_nameYoungModulus
        
        stiffness = StiffnessT4()
        stiffness.Stiffness(self.valij.val1,self.valij.val2,self.valij.val3,self.valij.val4,self.valij.val5,self.valij.val6,self.valij.val7,self.valij.val8,self.valij.val9,self.valij.val10,self.valij.val11,self.valij.val12,self.valij.val13,self.valij.val14,self.valij.val15,self.valij.val16,self.valij.val17,self.valij.val18,self.valij.val19,self.valij.val20,self.valij.val21,self.valij.val22,self.valij.val23,self.valij.val24,self.valij.val25,self.valij.val26,self.valij.val27,self.valij.val28,self.valij.val29,self.valij.val30,self.valij.val31,self.valij.val32,self.valij.val33,self.valij.val34,self.valij.val35,self.valij.val36,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
        if stiffness.error == None:
            self.jason_data_poly['error']  = stiffness.error
            self.jason_data_poly['XEC'] = stiffness.stringValsOfXEC
            self.jason_data_poly['YEC'] = stiffness.stringValsOfYEC
            self.jason_data_poly['ZEC'] = stiffness.stringValsOfZEC
       
            #surfacecolorcompliancepoly=   compliance.surfacecolorcompliance
            self.jason_data_poly['surfacecolor'] = stiffness.surfacecolorstiffness
            
            stiffness.YoungModulus(self.valij.val1,self.valij.val2,self.valij.val3,self.valij.val4,self.valij.val5,self.valij.val6,self.valij.val7,self.valij.val8,self.valij.val9,self.valij.val10,self.valij.val11,self.valij.val12,self.valij.val13,self.valij.val14,self.valij.val15,self.valij.val16,self.valij.val17,self.valij.val18,self.valij.val19,self.valij.val20,self.valij.val21,self.valij.val22,self.valij.val23,self.valij.val24,self.valij.val25,self.valij.val26,self.valij.val27,self.valij.val28,self.valij.val29,self.valij.val30,self.valij.val31,self.valij.val32,self.valij.val33,self.valij.val34,self.valij.val35,self.valij.val36,self.color[0],file_nameYoungModulus,self.res,self.stl_dir,create_stlym,self.createdata)
            """youngModulusXEC=compliance.stringValsOfXEC2
            youngModulusYEC = compliance.stringValsOfYEC2
            youngModulusZEC= compliance.stringValsOfZEC2"""
            self.jason_data_poly['youngModulusXEC'] = stiffness.stringValsOfXEC2
            self.jason_data_poly['youngModulusYEC'] = stiffness.stringValsOfYEC2
            self.jason_data_poly['youngModulusZEC'] = stiffness.stringValsOfZEC2
            
            #surfacecolorYoungModuluspoly=   compliance.surfacecolorYoungModulus 
            self.jason_data_poly['surfacecolorYoungModulus'] = stiffness.surfacecolorYoungModulus
        else:
            self.jason_data_poly['error'] = stiffness.error
            
            
        
        del stiffness



class FourthRankTensor(BaseTensor):
    def __init__(self, *args):
        super(FourthRankTensor, self).__init__(*args)
   
    def SingleCrystal(self):    
        file_name, create_stl, file_nameYoungModulus,create_stlym   = self.getdata()
        self.jason_data['filename1'] = file_name
        tensor = RankTensors()
        tensor.FourthRankTensor(self.valueij.value11,self.valueij.value12,self.valueij.value13,self.valueij.value14,self.valueij.value15,self.valueij.value16,self.valueij.value21,self.valueij.value22,self.valueij.value23,self.valueij.value24,self.valueij.value25,self.valueij.value26,self.valueij.value31,self.valueij.value32,self.valueij.value33,self.valueij.value34,self.valueij.value35,self.valueij.value36,self.valueij.value41,self.valueij.value42,self.valueij.value43,self.valueij.value44,self.valueij.value45,self.valueij.value46,self.valueij.value51,self.valueij.value52,self.valueij.value53,self.valueij.value54,self.valueij.value55,self.valueij.value56,self.valueij.value61,self.valueij.value62,self.valueij.value63,self.valueij.value64,self.valueij.value65,self.valueij.value66,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
        self.jason_data['XEC'] = tensor.stringValsOfXEC
        self.jason_data['YEC'] = tensor.stringValsOfYEC
        self.jason_data['ZEC'] = tensor.stringValsOfZEC
        self.jason_data['surfacecolor'] = tensor.surfacecolorFourthRankTensor     
        del tensor

    
    def SingleCrystalAndPoly(self):
        self.SingleCrystal()
        
        file_name, create_stl, file_nameYoungModulus,create_stlym   = self.getdatapoly()
        self.jason_data_poly['filename1'] = file_name
        tensor = RankTensors()
        tensor.FourthRankTensor(self.valij.val1,self.valij.val2,self.valij.val3,self.valij.val4,self.valij.val5,self.valij.val6,self.valij.val7,self.valij.val8,self.valij.val9,self.valij.val10,self.valij.val11,self.valij.val12,self.valij.val13,self.valij.val14,self.valij.val15,self.valij.val16,self.valij.val17,self.valij.val18,self.valij.val19,self.valij.val20,self.valij.val21,self.valij.val22,self.valij.val23,self.valij.val24,self.valij.val25,self.valij.val26,self.valij.val27,self.valij.val28,self.valij.val29,self.valij.val30,self.valij.val31,self.valij.val32,self.valij.val33,self.valij.val34,self.valij.val35,self.valij.val36,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
        self.jason_data_poly['XEC'] = tensor.stringValsOfXEC
        self.jason_data_poly['YEC'] = tensor.stringValsOfYEC
        self.jason_data_poly['ZEC'] = tensor.stringValsOfZEC
        self.jason_data_poly['surfacecolor'] = tensor.surfacecolorFourthRankTensor
      
        del tensor
 
 

class SecondRankTensor(BaseTensor):
    def __init__(self, *args):
        super(SecondRankTensor, self).__init__(*args)
   
    def SingleCrystal(self):    
        file_name, create_stl, file_nameYoungModulus,create_stlym   = self.getdata()
        self.jason_data['filename1'] = file_name
        tensor = RankTensors()
        tensor.SecondRankTensor(self.valueij.value11,self.valueij.value12,self.valueij.value13,self.valueij.value21,self.valueij.value22,self.valueij.value23,self.valueij.value31,self.valueij.value32,self.valueij.value33,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
        self.jason_data['XEC'] = tensor.stringValsOfXEC
        self.jason_data['YEC'] = tensor.stringValsOfYEC
        self.jason_data['ZEC'] = tensor.stringValsOfZEC
        self.jason_data['surfacecolor'] = tensor.surfacecolorSecondRankTensor     
        del tensor

    
    def SingleCrystalAndPoly(self):
        self.SingleCrystal()
        
        file_name, create_stl, file_nameYoungModulus,create_stlym   = self.getdatapoly()
        self.jason_data_poly['filename1'] = file_name
        tensor = RankTensors()
        tensor.SecondRankTensor(self.valij.val1,self.valij.val2,self.valij.val3,self.valij.val4,self.valij.val5,self.valij.val6,self.valij.val7,self.valij.val8,self.valij.val9,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
        self.jason_data_poly['XEC'] = tensor.stringValsOfXEC
        self.jason_data_poly['YEC'] = tensor.stringValsOfYEC
        self.jason_data_poly['ZEC'] = tensor.stringValsOfZEC
        self.jason_data_poly['surfacecolor'] = tensor.surfacecolorSecondRankTensor
      
        del tensor
        
        


class ThirdRankTensoreh(BaseTensor):
    def __init__(self, *args):
        super(ThirdRankTensoreh, self).__init__(*args)
   
    def SingleCrystal(self):    
        file_name, create_stl, file_nameYoungModulus,create_stlym   = self.getdata()
        self.jason_data['filename1'] = file_name
        tensor = RankTensors()
        tensor.ThirdRankTensoreh(self.valueij.value11,self.valueij.value12,self.valueij.value13,self.valueij.value14,self.valueij.value15,self.valueij.value16,self.valueij.value21,self.valueij.value22,self.valueij.value23,self.valueij.value24,self.valueij.value25,self.valueij.value26,self.valueij.value31,self.valueij.value32,self.valueij.value33,self.valueij.value34,self.valueij.value35,self.valueij.value36,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
 
        #tensor.SecondRankTensor(self.valueij.value11,self.valueij.value12,self.valueij.value13,self.valueij.value21,self.valueij.value22,self.valueij.value23,self.valueij.value31,self.valueij.value32,self.valueij.value33,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
        self.jason_data['XEC'] = tensor.stringValsOfXEC
        self.jason_data['YEC'] = tensor.stringValsOfYEC
        self.jason_data['ZEC'] = tensor.stringValsOfZEC
        self.jason_data['surfacecolor'] = tensor.surfacecolorThirdRankTensor     
        del tensor

    
    def SingleCrystalAndPoly(self):
        self.SingleCrystal()
        
        file_name, create_stl, file_nameYoungModulus,create_stlym   = self.getdatapoly()
        self.jason_data_poly['filename1'] = file_name
        tensor = RankTensors()
        #tensor.ThirdRankTensoreh(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,color,filename1,res,stl_dir,createstl,createdata)
        tensor.ThirdRankTensoreh(self.valij.val1,self.valij.val2,self.valij.val3,self.valij.val4,self.valij.val5,self.valij.val6,self.valij.val7,self.valij.val8,self.valij.val9,self.valij.val10,self.valij.val11,self.valij.val12,self.valij.val13,self.valij.val14,self.valij.val15,self.valij.val16,self.valij.val17,self.valij.val18,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
        self.jason_data_poly['XEC'] = tensor.stringValsOfXEC
        self.jason_data_poly['YEC'] = tensor.stringValsOfYEC
        self.jason_data_poly['ZEC'] = tensor.stringValsOfZEC
        self.jason_data_poly['surfacecolor'] = tensor.surfacecolorThirdRankTensor
      
        del tensor
        
class ThirdRankTensordg(BaseTensor):
    def __init__(self, *args):
        super(ThirdRankTensordg, self).__init__(*args)
   
    def SingleCrystal(self):    
        file_name, create_stl, file_nameYoungModulus,create_stlym   = self.getdata()
        self.jason_data['filename1'] = file_name
        tensor = RankTensors()
        tensor.ThirdRankTensordg(self.valueij.value11,self.valueij.value12,self.valueij.value13,self.valueij.value14,self.valueij.value15,self.valueij.value16,self.valueij.value21,self.valueij.value22,self.valueij.value23,self.valueij.value24,self.valueij.value25,self.valueij.value26,self.valueij.value31,self.valueij.value32,self.valueij.value33,self.valueij.value34,self.valueij.value35,self.valueij.value36,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
 
        #tensor.SecondRankTensor(self.valueij.value11,self.valueij.value12,self.valueij.value13,self.valueij.value21,self.valueij.value22,self.valueij.value23,self.valueij.value31,self.valueij.value32,self.valueij.value33,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
        self.jason_data['XEC'] = tensor.stringValsOfXEC
        self.jason_data['YEC'] = tensor.stringValsOfYEC
        self.jason_data['ZEC'] = tensor.stringValsOfZEC
        self.jason_data['surfacecolor'] = tensor.surfacecolorThirdRankTensor     
        del tensor

    
    def SingleCrystalAndPoly(self):
        self.SingleCrystal()
        
        file_name, create_stl, file_nameYoungModulus,create_stlym   = self.getdatapoly()
        self.jason_data_poly['filename1'] = file_name
        tensor = RankTensors()
        #tensor.ThirdRankTensoreh(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,color,filename1,res,stl_dir,createstl,createdata)
        tensor.ThirdRankTensordg(self.valij.val1,self.valij.val2,self.valij.val3,self.valij.val4,self.valij.val5,self.valij.val6,self.valij.val7,self.valij.val8,self.valij.val9,self.valij.val10,self.valij.val11,self.valij.val12,self.valij.val13,self.valij.val14,self.valij.val15,self.valij.val16,self.valij.val17,self.valij.val18,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
        self.jason_data_poly['XEC'] = tensor.stringValsOfXEC
        self.jason_data_poly['YEC'] = tensor.stringValsOfYEC
        self.jason_data_poly['ZEC'] = tensor.stringValsOfZEC
        self.jason_data_poly['surfacecolor'] = tensor.surfacecolorThirdRankTensor
      
        del tensor
        
        
        
class MagnetoCrystallineAnisotropy(BaseTensor):
    def __init__(self, *args):
        super(MagnetoCrystallineAnisotropy, self).__init__(*args)
   
    def SingleCrystal(self):    
        file_name, create_stl, file_nameYoungModulus,create_stlym   = self.getdata()
        self.jason_data['filename1'] = file_name
        #tensor = RankTensors()
        #tensor.ThirdRankTensordg(self.valueij.value11,self.valueij.value12,self.valueij.value13,self.valueij.value14,self.valueij.value15,self.valueij.value16,self.valueij.value21,self.valueij.value22,self.valueij.value23,self.valueij.value24,self.valueij.value25,self.valueij.value26,self.valueij.value31,self.valueij.value32,self.valueij.value33,self.valueij.value34,self.valueij.value35,self.valueij.value36,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
        tensor =  Magneto();
        tensor.MagnetocrystallineAnisotropy(self.valueij.value1,self.valueij.value2, self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata);
        #tensor.SecondRankTensor(self.valueij.value11,self.valueij.value12,self.valueij.value13,self.valueij.value21,self.valueij.value22,self.valueij.value23,self.valueij.value31,self.valueij.value32,self.valueij.value33,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
        self.jason_data['XEC'] = tensor.stringValsOfXEC
        self.jason_data['YEC'] = tensor.stringValsOfYEC
        self.jason_data['ZEC'] = tensor.stringValsOfZEC
        self.jason_data['surfacecolor'] = tensor.surfacecolorMagneticAnisotropy     
        del tensor

    
    def SingleCrystalAndPoly(self):
        self.SingleCrystal()
        
        file_name, create_stl, file_nameYoungModulus,create_stlym   = self.getdatapoly()
        self.jason_data_poly['filename1'] = file_name
        tensor = RankTensors()
        #tensor.ThirdRankTensoreh(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,color,filename1,res,stl_dir,createstl,createdata)
        tensor.MagnetocrystallineAnisotropy(self.valij.val1,self.valij.val2,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
        self.jason_data_poly['XEC'] = tensor.stringValsOfXEC
        self.jason_data_poly['YEC'] = tensor.stringValsOfYEC
        self.jason_data_poly['ZEC'] = tensor.stringValsOfZEC
        self.jason_data_poly['surfacecolor'] = tensor.surfacecolorMagneticAnisotropy
      
        del tensor
        
        
        
        
class Magnetostriction(BaseTensor):
    def __init__(self, *args):
        super(Magnetostriction, self).__init__(*args)
   
    def SingleCrystal(self):    
        file_name, create_stl, file_nameYoungModulus,create_stlym   = self.getdata()
        self.jason_data['filename1'] = file_name
        #tensor = RankTensors()
        #tensor.ThirdRankTensordg(self.valueij.value11,self.valueij.value12,self.valueij.value13,self.valueij.value14,self.valueij.value15,self.valueij.value16,self.valueij.value21,self.valueij.value22,self.valueij.value23,self.valueij.value24,self.valueij.value25,self.valueij.value26,self.valueij.value31,self.valueij.value32,self.valueij.value33,self.valueij.value34,self.valueij.value35,self.valueij.value36,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
        tensor =  Magneto();
        tensor.MagnetoStriction(self.valueij.value1,self.valueij.value2, self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata);
        #tensor.SecondRankTensor(self.valueij.value11,self.valueij.value12,self.valueij.value13,self.valueij.value21,self.valueij.value22,self.valueij.value23,self.valueij.value31,self.valueij.value32,self.valueij.value33,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
        self.jason_data['XEC'] = tensor.stringValsOfXEC
        self.jason_data['YEC'] = tensor.stringValsOfYEC
        self.jason_data['ZEC'] = tensor.stringValsOfZEC
        self.jason_data['surfacecolor'] = tensor.surfacecolorMagnetostriction     
        del tensor

    
    def SingleCrystalAndPoly(self):
        self.SingleCrystal()
        
        file_name, create_stl, file_nameYoungModulus,create_stlym   = self.getdatapoly()
        self.jason_data_poly['filename1'] = file_name
        tensor = RankTensors()
        #tensor.ThirdRankTensoreh(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,color,filename1,res,stl_dir,createstl,createdata)
        tensor.MagnetoStriction(self.valij.val1,self.valij.val2,self.color[0],file_name,self.res,self.stl_dir,create_stl,self.createdata)
        self.jason_data_poly['XEC'] = tensor.stringValsOfXEC
        self.jason_data_poly['YEC'] = tensor.stringValsOfYEC
        self.jason_data_poly['ZEC'] = tensor.stringValsOfZEC
        self.jason_data_poly['surfacecolor'] = tensor.surfacecolorMagnetostriction
      
        del tensor