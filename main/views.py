from django.shortcuts import render
from .forms import InputForm
import re

def get_coords(request):
      submitbutton= request.POST.get("submit")  #if button was pressed
      coords=''
      convert1=None
      convert2=None
      res=None
      res_not=None
      res_len=None

      form_field= InputForm(request.POST or None)     
      if form_field.is_valid():     #some default valid-check
            coords= form_field.cleaned_data.get("coords_input")   #str
            res=re.findall(r"\b\d+\b", coords) #list; search for digits groups with both boundaries of nonword
            res_not=re.findall(r"\b(-|n|N|s|S|w|W|e|E|с|С|ю|Ю|в|В|з|З)", coords)  #search for latitude-longitude notation simbols with nonword boundary in the beginning
            if res_not==[]: #if no letters found in input then we create it ourselves
                  res_not=["N","E"] 
            else:
                  pass  
            lat=res_not[0]  #create notations variables
            lon=res_not[1]

            if len(res)==8:   #if input data is DMs-format
                  convDM_lat=int(res[1])+float(res[2]+"."+res[3])/60   #latitude convertation minutes and seconds into minutes with decimals: =M+S/60
                  convDM_lon=int(res[5])+float(res[6]+"."+res[7])/60   #longitude convertation minutes and seconds into minutes with decimals: =M+S/60
                  convDD_lat=int(res[0])+int(res[1])/60+(float(res[2]+"."+res[3]))/3600   #latitude convertation =D+M/60+S/3600 
                  convDD_lon=int(res[4])+int(res[5])/60+(float(res[6]+"."+res[7]))/3600   #longitude convertation =D+M/60+S/3600
                  convert1=str(f"{res[0]}\u00b0 {round(convDM_lat,4)}\"{lat.upper()}\t{res[4]}\u00b0 {round(convDM_lon,4)}\"{lon.upper()}")  #dms2dm
                  convert2=str(f"{round(convDD_lat,5)}\u00b0{lat.upper()}\t{round(convDD_lon,5)}\u00b0{lon.upper()}")   #dms2dd

            elif len(res)==6:   #if input data is DM-format
                  convDMS_lat=float("0."+res[2])*60   #latitude convertation decimal minutes into seconds: =.s*60->S"
                  convDMS_lon=float("0."+res[5])*60   #longitude convertation decimal minutes into seconds:  =.s*60->S"
                  convDD_lat=int(res[0])+int(res[1])/60+float("0."+res[2])/3600   #latitude convertation =D+M/60+S/3600 
                  convDD_lon=int(res[3])+int(res[4])/60+float("0."+res[5])/3600   #longitude convertation =D+M/60+S/3600
                  convert1=str(f"{res[0]}\u00b0 {res[1]}\' {round(convDMS_lat,2)}\"{lat.upper()}\n{res[3]}\u00b0 {res[4]}\' {round(convDMS_lon,2)}\"{lon.upper()}")  #print joined unchagned degrees and minutes with converted values
                  convert2=str(f"{round(convDD_lat,5)}\u00b0{lat.upper()}\n{round(convDD_lon,5)}\u00b0{lon.upper()}")   #print joined degrees with the decimal of degrees
            
            elif len(res)==4:   #if input data is DD-format
                  convDMS_lat_conv=float("0."+(res[1]))*60   #latitude convertation decimal degrees into floating minutes: =float(.d*60)->M"
                  convDMS_lat_min=int(convDMS_lat_conv)    #latitude convertation floating minutes into int minutes: =int(M.m)->M"
                  convDMS_lat_sec=round(((convDMS_lat_conv-int(convDMS_lat_conv))*60) , 2)    #latitude convertation remainder into rounded seconds: =round(.m*60)->S"
                  convDMS_lon_conv=float("0."+(res[3]))*60   #longitude convertation decimal degrees into floating minutes: =float(0.d*60)->M"
                  convDMS_lon_min=int(convDMS_lon_conv)    #longitude convertation floating minutes into int minutes: =int(M.m)->M"
                  convDMS_lon_sec=round(((convDMS_lon_conv-int(convDMS_lon_conv))*60) , 2)    #longitude convertation remainder into rounded seconds: =round(.m*60)->S"
                  convert1=str(f"{res[0]}\u00b0 {convDMS_lat_min}\' {round(convDMS_lat_sec,2)}\"{lat.upper()}\n{res[2]}\u00b0 {convDMS_lon_min}\' {round(convDMS_lon_sec,2)}\"{lon.upper()}")  #print joined unchagned degrees, minutes and seconds with converted values
                  convDM_lat_min=float("0."+(res[1]))*60   #latitude convertation decimal degrees into floating minutes: =float(.d*60)->M.m"
                  convDM_lon_min=float("0."+(res[3]))*60   #longitude convertation decimal degrees into floating minutes: =float(0.d*60)->M.m"
                  convert2=str(f"{res[0]}\u00b0 {round(convDM_lat_min,4)}\"{lat.upper()}\n{res[2]}\u00b0 {round(convDM_lon_min,4)}\"{lon.upper()}")  #print joined unchagned degrees with converted float minutes

            else:
                  convert1=str('Please check your data.')
                  convert2=str('Please check your data.')

      context= {'form_field': form_field, 'convert1': convert1, 'convert2': convert2, 
            'submitbutton': submitbutton, 'res': res, 'res_not': res_not, 'res_len': res_len,   
            } #output content of the page

      return render(request, 'main/index.html', context) #rendering the page