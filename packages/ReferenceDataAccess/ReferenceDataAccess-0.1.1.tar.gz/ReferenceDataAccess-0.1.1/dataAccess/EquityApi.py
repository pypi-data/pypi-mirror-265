# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 21:46:15 2021

@author: Sangoi
"""
import requests
import json
import pandas as pd

class EquityApi(object):
    """
        This class hold all methods to access equity data
      
    """
    
    def __init__(self, key, base_url='https://65stvtuo0h.execute-api.eu-west-2.amazonaws.com/FreeTrial/'):
        """ 
        Initialize the class
        Keyword Arguments:
            key:  RDUAccess api key

        """
        
        self.key = key
        self.base_url = base_url
    """
    This method calls the resp api.
    """
    
    def _clean_rdu_data(self, line):
        """
        This method cleans up the RDU API response by converting error code to blanks and 
        considering only the RDU domain values.
        """    
        d = json.loads(line)
        if d["instrument"]:
            for keys in d["instrument"]:
                # print(keys + "-" + str(len(d["instrument"][keys])))
                if keys not in ["securities","issuers"]:
                    if len(d["instrument"][keys]) > 1:
                        for i in range(len(d["instrument"][keys])):    #inside list
                            if d["instrument"][keys][i]["domain"] != "rdu":
                                # print(keys + "-" + str(len(d["instrument"][keys])))
                                d["instrument"][keys].pop(i)
                                break
            if "securities" in d["instrument"]:
                for i in range(len(d["instrument"]["securities"])):
                    for keys in d["instrument"]["securities"][i].copy():
                        if keys not in ["secFeedRawValues"]:
                            if len(d["instrument"]["securities"][i][keys]) > 1:
                                for j in range(len(d["instrument"]["securities"][i][keys])):
                                    if d["instrument"]["securities"][i][keys][j]["domain"] != "rdu":
                                        d["instrument"]["securities"][i][keys].pop(j)
                                        break
                        else:
                            del d["instrument"]["securities"][i]["secFeedRawValues"]

            if "issuers" in d["instrument"]:
                for i in range(len(d["instrument"]["issuers"])):
                    for keys in d["instrument"]["issuers"][i]:
                        if keys not in ["secFeedRawValues"]:
                            if len(d["instrument"]["issuers"][i][keys]) > 1:
                                for j in range(len(d["instrument"]["issuers"][i][keys])):
                                    if d["instrument"]["issuers"][i][keys][j]["domain"] != "rdu":
                                        d["instrument"]["issuers"][i][keys].pop(j)
                                        break
            ## removal of error code
            for keys in d["instrument"]:
                if "errorCode" in d["instrument"][keys][0]:
                    # print(keys + "-" + str(len(d["instrument"][keys])))
                    del d["instrument"][keys][0]["errorCode"]
                    d["instrument"][keys][0]["value"] = ""
            
            if "securities" in d["instrument"]:
                for i in range(len(d["instrument"]["securities"])):
                    for keys in d["instrument"]["securities"]:
                        if keys not in ["secFeedRawValues"]:
                            for keys in d["instrument"]["securities"][i]:
                                if keys not in ["secFeedRawValues"]:
                                    if "errorCode" in d["instrument"]["securities"][i][keys][0]:
                                        del d["instrument"]["securities"][i][keys][0]["errorCode"]
                                        d["instrument"]["securities"][i][keys][0]["value"] = ""

            if "issuers" in d["instrument"]:
                for i in range(len(d["instrument"]["issuers"])):
                    for keys in d["instrument"]["issuers"]:
                        for keys in d["instrument"]["issuers"][i]:
                            if "errorCode" in d["instrument"]["issuers"][i][keys][0]:
                                del d["instrument"]["issuers"][i][keys][0]["errorCode"]
                                d["instrument"]["issuers"][i][keys][0]["value"] = ""

        outdata = {}
        for k1 in d:
            outdata[k1] = {}
            for k2 in d[k1]:
                for it1 in range(len(d[k1][k2])):
                    for k3 in d[k1][k2][it1]:
                        if type(d[k1][k2][it1][k3]) == list:
                            if k2 not in outdata[k1]:
                                outdata[k1][k2] = []
                                outdata[k1][k2].append({})
                            if it1 > 0 and len(outdata[k1][k2]) > 0 and  it1 == len(outdata[k1][k2]):
                                outdata[k1][k2].append({})
                            if k3 not in outdata[k1][k2][it1]:
                                outdata[k1][k2][it1][k3] = {}
                            outdata[k1][k2][it1][k3] = d[k1][k2][it1][k3][0]
                        else:
                            outdata[k1][k2] = d[k1][k2][it1]

        return json.dumps(outdata)


    def __call_api(self, query, url):
        headers = {'x-api-key' : self.key,'accept':'application/json'}
        response = requests.get(url, params=query,headers=headers)
        data = response.text
        if not data:
            data = "{\"message\":\"No Data Found\"}"
        json_data = json.loads(data)
        return json_data


    def __convert_json_to_df(self, input_key,json_data, columnList=[]):

        content =  json_data["responseString"][0]
        msg = json_data["responseCode"][0]
        isSuccess = True if msg[0] == "S" else False

        instrument_dict = {}
        if(isSuccess):
            json_data = json_data["content"][0]
            json_data = self._clean_rdu_data(json.dumps(json_data))

            df = pd.DataFrame.from_dict(json.loads(json_data))
            
            
            ins_dict = {}

            securities = df["instrument"]["securities"]
            for i in range(len(df["instrument"]["securities"])):
                ins_dict = {}
                ins_dict['success'] = True
                
                for k1 in df.index:
                    if k1 not in ["issuers","securities"]:
                        ins_dict[k1] = df["instrument"][k1]["value"]

                for k2 in df["instrument"]["securities"][i]:
                    ins_dict[k2] = df["instrument"]["securities"][i][k2]["value"]

                for k3 in df["instrument"]["issuers"][0]:
                    ins_dict[k3] = df["instrument"]["issuers"][0][k3]["value"]
                exchCd = df["instrument"]["securities"][i]["exchangeCode"]["value"]
                input_key = input_key.replace(".","_")
                instrument_dict[input_key+"_"+ exchCd] = ins_dict
                
        else:
            ins_dict = {}
            ins_dict['success'] = False
            ins_dict['failed_message'] = "No data available"
            instrument_dict[input_key] = ins_dict

            
        data = pd.DataFrame.from_dict(instrument_dict, orient='index')
        
        return data       



    def get_by_isin(self, isin):
        """
        
        This will return the equity data given the isin
        Parameters
        ----------
        isin : String
            The ISIN code.

        Returns
        -------
        data : dataframe
            this will return a dataframe with key as isin.

        """
        #print("Calling getByIsin with isin "+isin)
        query = {'isin':isin}
        json_data = self.__call_api(query=query, url = self.base_url + 'equity/search/v1/getByISIN')
            
        data = self.__convert_json_to_df(isin,json_data)
        return data

    def get_by_isin_exchange(self, isin, exchange):
        """
        
        This will return the equity data given the isin
        Parameters
        ----------
        isin : String
            The ISIN code.
        exchange : String
            exchange code 
        Returns
        -------
        data : dataframe
            this will return a dataframe with key as isin+exchange.

        """
        #print("Calling getByIsin with isin "+isin)
        query = {'isin':isin,'mic':exchange}
        json_data = self.__call_api(query=query, url= self.base_url + 'equity/search/v1/getByISINMIC')
            
        data = self.__convert_json_to_df(isin,json_data)
        return data

    def get_by_ric(self, ric):
        """
        
        This will return the equity data given the isin
        Parameters
        ----------
        ric : String
            The RIC code.

        Returns
        -------
        data : dataframe
            this will return a dataframe with key as ric.

        """
        #print("Calling getByIsin with isin "+isin)
        query = {'ric': ric}
        json_data = self.__call_api(query=query, url = self.base_url + 'equity/search/v1/getByRIC')
            
        data = self.__convert_json_to_df(ric,json_data)
        return data
    
    def get_by_figi(self, figi):
        """
        
        This will return the equity data given the isin
        Parameters
        ----------
        figi : String
            The FIGI code.

        Returns
        -------
        data : dataframe
            this will return a dataframe with key as figi.

        """
        #print("Calling getByIsin with isin "+isin)
        query = {'bbgidbbglobal': figi}
        json_data = self.__call_api(query=query, url = self.base_url + 'equity/search/v1/getByBbgIdBbGlobal')
            
        data = self.__convert_json_to_df(figi,json_data)
        return data
    
    def get_by_rics(self, rics=[]):
        """
        
        This will return the equity data given the rics
        Parameters
        ----------
        rics : list
            The RIC codes in a list.

        Returns
        -------
        data : dataframe
            this will return a dataframe with key as ric.

        """
        #print("Calling getByIsin with isin "+isin)
        data = []
        for ric in rics:
            t_data = self.get_by_ric(ric=ric)
            data.append(t_data)
        df = pd.concat(data)
        return df

    def get_by_figis(self, figis=[]):
        """
        
        This will return the equity data given the rics
        Parameters
        ----------
        figis : list
            The FIGI codes in a list.

        Returns
        -------
        data : dataframe
            this will return a dataframe with key as figi.

        """
        #print("Calling getByIsin with isin "+isin)
        data = []
        for figi in figis:
            t_data = self.get_by_figi(figi=figi)
            data.append(t_data)
        df = pd.concat(data)
        return df
