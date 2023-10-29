import pandas as pd
from bs4 import BeautifulSoup
from function import Scrap_data,opened_link_chroome

df=Scrap_data(driver=opened_link_chroome(url_search="https://www.google.com/maps/search/kursus+stir+mobil"))

# print(df)
#df=pd.read_csv("Out.txt",delimiter="|")
kf=pd.DataFrame()
for index, row in df.iterrows():
    while True:
        try:
            
            data=BeautifulSoup(opened_link_chroome(url_search=row['link']).page_source, 'html.parser')
            E_text = data.find_all('div', class_="Io6YTe fontBodyMedium kR99db")
            E_image = data.find_all('img', class_='Liguzb')
        
            array_image = []
            for element in E_image:
                E_image = element.get('src')
                array_image.append(E_image)
            
            array_text = []
            for element in E_text:
                E_text = element.get_text()
                array_text.append(E_text)
                
                
            df_text = pd.DataFrame(array_text)
            df_image = pd.DataFrame(array_image)
            result = df_image.merge(df_text, left_index=True, right_index=True, how='inner')
            if not result['0_x'].str.contains('phone_gm_blue_24dp.png').any():
                result=result.append({'0_x': 'phone_gm_blue_24dp.png', '0_y': ''},ignore_index=True)
            if not result['0_x'].str.contains('place_gm_blue_24dp.png').any():
                result=result.append({'0_x': 'place_gm_blue_24dp.png', '0_y': ''},ignore_index=True)
            if not result['0_x'].str.contains('public_gm_blue_24dp.png').any():
                result=result.append({'0_x': 'public_gm_blue_24dp.png', '0_y': ''},ignore_index=True)
            if not result['0_x'].str.contains('ic_plus_code.png').any():
                result=result.append({'0_x': 'ic_plus_code.png', '0_y': ''},ignore_index=True)
            result=result[result['0_x'].str.contains('phone_gm_blue_24dp.png|place_gm_blue_24dp.png|public_gm_blue_24dp.png|ic_plus_code.png')]
        

            
            
            result_phone_gm_blue_24dp_png=result[result['0_x'].str.contains('phone_gm_blue_24dp.png')]
            result_place_gm_blue_24dp_png=result[result['0_x'].str.contains('place_gm_blue_24dp.png')]
            result_public_gm_blue_24dp_png=result[result['0_x'].str.contains('public_gm_blue_24dp.png')]
            result_ic_plus_code_png=result[result['0_x'].str.contains('ic_plus_code.png')]

            result=pd.concat([result_phone_gm_blue_24dp_png,
                            result_place_gm_blue_24dp_png,
                            result_public_gm_blue_24dp_png,
                            result_ic_plus_code_png])
            result['0_x'].loc[result['0_x'].str.contains('phone_gm_blue_24dp.png')] = 'phone_gm_blue_24dp.png'
            result['0_x'].loc[result['0_x'].str.contains('place_gm_blue_24dp.png')] = 'place_gm_blue_24dp.png'
            result['0_x'].loc[result['0_x'].str.contains('public_gm_blue_24dp.png')] = 'public_gm_blue_24dp.png'
            result['0_x'].loc[result['0_x'].str.contains('ic_plus_code.png')] = 'ic_plus_code.png'
            
            result = result.append(pd.DataFrame([{'0_x':'id','0_y':row['id']}]), ignore_index=True)
            result = result.append(pd.DataFrame([{'0_x':'nama','0_y':row['nama']}]), ignore_index=True)
            result = result.append(pd.DataFrame([{'0_x':'rating','0_y':row['rating']}]), ignore_index=True)
            result = result.append(pd.DataFrame([{'0_x':'link','0_y':row['link']}]), ignore_index=True)
            
            result=result.reset_index(drop=True)
            result=result.T
            result=result.iloc[1:]
            break
        except:
            pass
    
    result=result[[4,5,6,7,0,1,2,3]]
    print(result)
    kf=kf.append(result)
    #break


kf.to_excel("test.xlsx")
print(kf)