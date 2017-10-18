'''
Created on Nov 25, 2014

@author: admin
'''

import os
import re
import string


class Extractor (object):
    def __init__(self,cifs_dir,core_dic_filepath,mpod_dic_filepath,cifs_dir_output,out_file_sql_path):
        self.cifs_dir=cifs_dir
        self.core_dic_filepath=core_dic_filepath
        self.mpod_dic_filepath=mpod_dic_filepath
        self.cifs_dir_output =cifs_dir_output
        self.fds=os.listdir(self.cifs_dir)
        self.fds2=filter(lambda x: x[-5:]==".mpod",  self.fds)
        self.filets=sorted(filter(lambda x: os.path.isfile(os.path.join(cifs_dir,  x)), self.fds2))
        #self.out_file_path=out_file_sql_path

    
    def read_file_1(self, mpod_filepath):
        in_file = open(mpod_filepath, 'r')
        texto = in_file.read()
        in_file.close()
        return texto
    
    
    def get_data_code(self, texto):
        lins = map(lambda x: x.strip(), texto.strip().split("\n"))
        code=0
        for li in lins:
            code = self.get_data_code_lin(li)
            if code>0:
                return code
        if code==0:
            raise Exception('Cid data_ code', 'missing')
        else:
            return code

    @classmethod
    def get_data_code_lin(self, lin):
        l=lin.strip()
        if l[0:5]=='data_':
            return int(l[5:])
        else:
            return 0

    def get_info_1(self, texto,  tags):
        vals=[]
        for tag in tags:
            val=""
            rf = texto.find(tag)
            if rf>-1:
                tl=len(tag)
                st=rf+tl
                rf2 = texto[st:].find('\n')
                val=texto[st:st+rf2].strip().strip("'")
            else:
                val = "None"
            vals.append(val)
        return vals

    def get_info_title(self, texto):
        title_lins=[]
        lins = map(lambda x: x.strip(), texto.strip().split("\n"))
        ind=0
        for i, lin in enumerate(lins):
            if lin.find("_publ_section_title")>-1:
                ind = i
                break
        flag = False
        if ind > 0:
           flag = True
           
        j=2
        while flag:
            stripped = lins[ind+j].strip().strip("'").strip()
            if stripped[0]==";":
                break
            else:
                title_lins.append(stripped)
                j=j+1
        return " ".join(title_lins)

    def get_info_authors(self, texto):
        authors=[]
        lins = map(lambda x: x.strip(), texto.strip().split("\n"))
        ind=0
        for i, lin in enumerate(lins):
            if lin.find("_publ_author_name")>-1:
                ind = i
                break
        if lins[ind-1]=="loop_":
            flag = True
            j=1
            while flag:
                stripped = lins[ind+j].strip().strip("'").strip()
                if stripped[0]=="_":
                    break
                else:
                    authors.append(stripped)
                    j=j+1
        else:
            authors_stri = lins[ind][len('_publ_author_name'):].strip().strip("'").strip()
            if authors_stri.find(',')>-1:
                authors = authors + authors_stri.split(',')
            else:
                authors.append(authors_stri)
        return authors

    def publi_sql(self, id, publi_vals, title, authors):
        kss = "id, title, authors, journal, year, volume, issue, first_page, last_page, reference, pages_number"
        ks = map(lambda x: x.strip(), kss.split(","))
        formatss = "%d, %s, %s, %s, %d, %s, %s, %d, %d, %s, %d"
        formats = map(lambda x: x.strip(), formatss.split(","))
        func=None
        tks = []
        tvs = []
        fs =[]
        publi_vals=[publi_vals[0]]+[title]+[authors]+publi_vals[1:]
        for i,v in enumerate(publi_vals):
            #if not v=="None":
                f=formats[i]
                if f=='%d':
                    func=int
                if f=='%s':
                    func=lambda x: "'"+str(x)+"'"
                if f=='%f':
                    func=float
                try:                    
                    if (i == 4 or i == 7 or i == 8 or i == 10) and (v == 'None' or  v == '?'):    
                        if v == 'None':
                          vv=func(-1)
                        elif v == '?':
                          vv=func(-2)
                    else:
                       vv=func(v)
                    
                    tks.append(ks[i])
                    tvs.append(vv)
                    fs.append(f)
                except:
                    pass

                
        tags_st = ", ".join(tks)
        frms_st = ", ".join(fs)
        vals_tup = tuple(tvs)
        text_publi="INSERT INTO data_publarticle ("+ kss + ") VALUES (" + frms_st+ ");"
        return text_publi %vals_tup

    def gen_info_sql(self, id, publi_id, info_vals):
        kss="code, filename, cod_code, phase_generic, phase_name, chemical_formula, publication_id"
        ks = map(lambda x: x.strip(), kss.split(","))
        formatss = "%d, %s, %d, %s, %s, %s, %d"
        formats = map(lambda x: x.strip(), formatss.split(","))
        func=None
        tks = []
        tvs = []
        fs =[]
        info_vals=info_vals+[publi_id]
        for i,v in enumerate(info_vals):
            #if not v=="None":
                f=formats[i]
                if f=='%d':
                    func=int
                if f=='%s':
                    func=lambda x: "'"+str(x)+"'"
                if f=='%f':
                    func=float
                try:
                    if (i == 0 or i == 2 or i == 6)  and (v == 'None' or  v == '?'):    
                       if v == 'None':
                          vv=func(-1)
                       elif v == '?':
                          vv=func(-2)                    
                    else:
                       vv=func(v)
                       
                    
                    tks.append(ks[i])
                    tvs.append(vv)
                    fs.append(f)
                except:
                    pass
        tags_st = ", ".join(tks)
        frms_st = ", ".join(fs)
        vals_tup = tuple(tvs)
        text_gen="INSERT INTO data_datafile ("+kss+ ") VALUES (" + frms_st+ ");"
        return text_gen %vals_tup

    def format_vals(self,vals, formats):
        func=None
        tvs = []
        fs =[]
        for i,v in enumerate(vals):
            if not v=="None":
                f=formats[i]
                if f=='%d':
                    func=int
                if f=='%s':
                    func=lambda x: "'"+str(x)+"'"
                if f=='%f':
                    func=float
                try:
                    vv=func(v)
                    tvs.append(vv)
                    fs.append(f)
                except:
                    pass
        frms_st = ", ".join(fs)
        vals_tup = tuple(tvs)
        return tvs
    
    def get_props(self,texto):
        tg="_prop"
        ntgs= ['conditions','measurement','frame','symmetry', 'data']
        props=[]
        props_agg=[]
        lins = map(lambda x: x.strip(), texto.strip().split("\n"))
        ind=0
        for i, lin in enumerate(lins):
            if lin.find(tg)>-1:
                lcs=lin.split()
                prstr=lcs[0].strip()[5:]
                parts=prstr.split('_')
                if parts[1] in ntgs:
                    if prstr not in props_agg:
                        props_agg.append(prstr)
                else:
                    if prstr not in props:
                        props.append(prstr)
        return props, props_agg
    
    
    def get_conds(self,texto):
        tg="_prop"
        ntgs= ['conditions','measurement','frame','symmetry']
        props=[]
        props_agg=[]
        lins = map(lambda x: x.strip(), texto.strip().split("\n"))
        ind=0
        for i, lin in enumerate(lins):
            if lin.find(tg)>-1:
                lcs=lin.split()
                prstr=lcs[0].strip()[5:]
                parts=prstr.split('_')
                if parts[1] in ntgs:
                    if prstr not in props_agg:
                        props_agg.append(prstr)
                else:
                    if prstr not in props:
                        props.append(prstr)
        return props_agg
    
    def props_info_in_dic(self,props):
        props_info = {}
        tgs = ['_name','_category','_type','_units', '_units_detail']
        texto = self.read_file_1(self.mpod_dic_filepath)
        lins = map(lambda x: x.strip(), texto.strip().split("\n"))
        for prop in props:
            pro_str = "data_prop"+prop
            print pro_str
            for ii, lin in enumerate(lins):
                ind = None
                if lin.startswith(pro_str):
                    ind = ii
                    break
            cond = True
            jj=1
            if ind:
                props_info[prop] = {}
                while cond:
                    pl = lins[ind+jj]
                    if pl:
                        plps = pl.split(None, 1)
                        try:
                            tg, vtg = plps
                        except:
                            cond = False
                        tg =tg.strip().strip("'").strip()
                        vtg =vtg.strip().strip("'").strip()
                        if tg in tgs:
                            indt = tgs.index(tg)
                            props_info[prop][tg] = vtg
                    else:
                        cond = False
                    jj = jj+1
    #                if jj > len(tgs) + 1 :
    #                    cond = False
        print "hecho"
        return props_info
    
    def extractConditions(self):
        tg="_prop"
        props = []
        data_props={}
        conds = []
        data_conds={}
        for i, fil in enumerate(self.filets):
            filepath=os.path.join(self.cifs_dir, fil)
            texto = self.read_file_1(filepath)
            code = self.get_data_code(texto)
            this_props, this_props_agg = self.get_props(texto)
            this_conds = self.get_conds(texto)
            for cn in this_conds:
                if not cn in conds:
                    conds.append(cn)
        conds = sorted(conds)
        
        for i, fil in enumerate(self.filets):
            filepath=os.path.join(self.cifs_dir, fil)
            texto = self.read_file_1(filepath)
            code = self.get_data_code(texto)
            this_props, this_props_agg = self.get_props(texto)
            this_conds = self.get_conds(texto)
            inds=[]
            for cn in this_conds:
                cond_ind=conds.index(cn)+1
                inds.append(cond_ind)
            
        data_conds[code]=inds        
        print conds, data_conds
        
        db_fields = ["tag", "description", 'name', 'units', 'units_detail']
        db_fields_str = ', '.join(db_fields)
        print
        print
        sql_lins = []
        for cn in conds:
            the_vals = [tg+cn,cn]
            formats = ['%s', '%s']
            the_vals_2 = self.format_vals(the_vals, formats)
            record_vals_str = ', '.join(the_vals_2)
            sql_lin="INSERT INTO data_experimentalparcond (" + db_fields_str + ") VALUES (" + record_vals_str + ", 'NULL', 'NULL', 'NULL');"
            sql_lins.append(sql_lin)
            
         
        aa = self.props_info_in_dic(conds)
        tgs = ['_name', '_units', '_units_detail']
        sql_lins2 = []
        for cond in conds:
            tp = cond
            na = aa[tp]['_name'][6:]
            try:
                un = aa[tp]['_units']
            except:
                un = 'n.a.'
            try:
                ud = aa[tp]['_units_detail']
            except:
                ud = 'n.a.'
            lin1 = "UPDATE data_experimentalparcond SET name = " + "'" + ' '.join(na.split('_')) + "'" + " WHERE tag = " + "'" + tg+cond + "';"
            lin2 = "UPDATE data_experimentalparcond SET units = " + "'" + un + "'" + " WHERE tag = " + "'" + tg+cond + "';"
            lin3 = "UPDATE data_experimentalparcond SET units_detail = " + "'" + ud + "'" + " WHERE tag = " + "'" + tg+cond + "';"
            sql_lins2.append(lin1)
            sql_lins2.append(lin2)
            sql_lins2.append(lin3)
        head = "USE giancarlo_mpod;\n"
        tail = "\nCOMMIT;\n"
        sql_text=head+ "\n".join(sql_lins) + "\n" + "\n".join(sql_lins2) + tail
        print sql_text
        out_file_path = "/EclipseWork/mpod/media/datafiles/test/load_conditions_2017_107_16.sql"
        out_file = open(out_file_path,"w")
        out_file.write(sql_text)
        out_file.close()  
        
        
    def extractProperties(self):
        tg="_prop"
        props = []
        data_props={}
        for i, fil in enumerate(self.filets):
            filepath=os.path.join(self.cifs_dir, fil)
            texto = self.read_file_1(filepath)
            code = self.get_data_code(texto)
            this_props, this_props_agg = self.get_props(texto)
            inds = []
            for pr in this_props:
                if not pr in props:
                    props.append(pr)
        props = sorted(props)
        for i, fil in enumerate(self.filets):
            filepath=os.path.join(self.cifs_dir, fil)
            texto = self.read_file_1(filepath)
            code = self.get_data_code(texto)
            this_props, this_props_agg = self.get_props(texto)
            inds=[]
            for pr in this_props:
                prop_ind=props.index(pr)+1
                inds.append(prop_ind)
            data_props[code]=inds
        print props, data_props
        db_fields = ["id", "tag", "description", "tensor_dimensions", "units", "units_detail"]
        db_fields_str = ', '.join(db_fields)
        print
        print
        sql_lins = []
        for i_pr, pr in enumerate(props):
            the_vals = [tg+pr,pr]
            formats = ['%s', '%s']
            the_vals_2 = self.format_vals(the_vals, formats)
            record_vals_str = ', '.join(the_vals_2)
            sql_lin="INSERT INTO data_property (" + db_fields_str + ") VALUES (" + str(i_pr+1) + ", "+  record_vals_str + ", 0, 'NULL', 'NULL');"
            sql_lins.append(sql_lin)
        db_fields = ["datafile_id", "property_id"]
        db_fields_str = ', '.join(db_fields)
        for dp in sorted(data_props.keys()):
            for prn in data_props[dp]:
                record_vals_str = ', '.join([str(dp),str(prn)])
                sql_lin="INSERT INTO data_datafile_property (" + db_fields_str + ") VALUES (" + record_vals_str + ");"
                sql_lins.append(sql_lin)
        aa = self.props_info_in_dic(props)
        tgs = ['_name', '_units', '_units_detail']
        sql_lins2 = []
        for prop in props:
            tp = prop
            print tp
            na = aa[tp]['_name']
            un = aa[tp]['_units']
            ud = aa[tp]['_units_detail']
            lin1 = "UPDATE data_property SET name = " + "'" + ' '.join(na.split('_')) + "'" + " WHERE tag = " + "'" + tg+prop + "';"
            lin2 = "UPDATE data_property SET units = " + "'" + un + "'" + " WHERE tag = " + "'" + tg+prop + "';"
            lin3 = "UPDATE data_property SET units_detail = " + "'" + ud + "'" + " WHERE tag = " + "'" + tg+prop + "';"
            sql_lins2.append(lin1)
            sql_lins2.append(lin2)
            sql_lins2.append(lin3)
        head = "USE giancarlo_mpod;\nDELETE FROM data_property;\nDELETE FROM data_datafile_property;\n"
        tail = "\nCOMMIT;\n"
        sql_text=head+ "\n".join(sql_lins) + "\n" + "\n".join(sql_lins2) + tail
        print sql_text
      
        out_file_path = "/EclipseWork/mpod/media/datafiles/test/load_properties_2017_107_16.sql"
        
        
        out_file = open(out_file_path,"w")
        out_file.write(sql_text)
        out_file.close()
        
        
        for prop in props:
            lin3 = "UPDATE data_property SET tensor_dimensions = '0' " + " WHERE tag = " + "'" + tg+prop + "';"
            print lin3
            
            
    def extractMpodToDatabase(self): 
        gen_tags = ['_cod_database_code', '_phase_generic', '_phase_name', '_chemical_formula_sum']
        publi_tags = ['_journal_name_full', '_journal_year', '_journal_volume',
                      '_journal_issue', '_journal_page_first', '_journal_page_last',
                      '_journal_article_reference', '_journal_pages_number' ]
        sql_lins_1=[]
        sql_lins_2=[]
        gen_info_lins=[]
        publi_info_lins=[]
        titles=[]
        ii = 1
        for i, fil in enumerate(self.filets):
            print fil
            filepath=os.path.join(self.cifs_dir, fil)
            texto = self.read_file_1(filepath)
            title = self.get_info_title(texto)
            if title in titles:
                ind=1+titles.index(title)  #python indexing starts from 0 index of publis from 1
            else:
                titles.append(title)
                publi_vals=[ii]
                publi_vals = publi_vals + self.get_info_1(texto, publi_tags)
                authors = self.get_info_authors(texto)
                authors_str = "; ".join(authors)
                #title = self.get_info_title(texto)
                aa = self.publi_sql(ii, publi_vals, title, authors_str)
                sql_lins_1.append(aa)
                ind = ii
                ii = ii+1
            code = self.get_data_code(texto)
            gen_vals=[code, fil]
            publi_vals=[ii]
            gen_info_lin = ""
            publi_info_lin = ""
            gen_vals = gen_vals + self.get_info_1(texto, gen_tags)
    #        print i, ind, gen_vals
            ''' 
             
             INSERT INTO data_publarticle (id, title, authors, journal, year, volume, issue, reference, pages_number) VALUES (1, 'Elastic constants and anisotropic internal frictions of decagonal Al72Ni18Co8 single quasicrystal at low temperature', 'Tarumi R.; Ledbetter H.; Shiomi S.; Ogi H.; Hirao M.; Tsai A.P.', 'Journal of Applied Physics', 2010, '108', '1', '013514', 5);
             INSERT INTO data_datafile (code, filename, phase_name, chemical_formula, publication_id) VALUES (1000001, '1000001.mpod', 'Al72Ni16Co8', 'Al72 Ni16 Co8', 1);
            '''
            #(self, id, publi_id, info_vals)
            bb = self.gen_info_sql(code,ind,gen_vals)
            #bb = self.gen_info_sql(1000001,,gen_vals)
            sql_lins_2.append(bb)
    #        gen_info_lin = "\t".join(gen_vals)
    #        gen_info_lins.append(gen_info_lin)
    #        publi_info_lins.append(gen_info_lin)
                      
            text_1 = "\n".join(sql_lins_1)
            text_2 = "\n".join(sql_lins_2)
            head = "USE giancarlo_mpod;\n"
            tail = "\nCOMMIT;\n"
            text_tot = head + text_1 + '\n' +  text_2 +tail
            print text_tot
           
           
            out_file_path = "/EclipseWork/mpod/media/datafiles/test/load_db_gen_2017_107_16.sql"
            out_file = open(out_file_path, "w")
            out_file.write(text_tot)
            out_file.close()       
           
            
            
