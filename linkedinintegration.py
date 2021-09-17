from lusha_api_wrapper.lusha_api_wrapper import LushaAPI
from fill_config import fill_config
from LinkedInScraping_master import do_scraping as dos
import json
import pandas as pd
from company_exceptions import CompanyExceptions
from LinkedInScraping_master import utils as ut


def integration(df):
    df_list = []
    for i in range(0, df.shape[0]):
        if not df["Linkedin"].isnull()[i]:
            print(f'+++++++++++++++   Integrating for index = {i} +++++++++++++++++++++++++++++++')
            print("df['Linkedin'][", i, "]", df['Linkedin'][i])
            lnk_link = df['Linkedin'][i]
            fill_config(df['Linkedin'][i])
            success, lnk_results, lnk_data = dos.do_scraping()
            # print(lnk_data)

            if success:
                LUSHA_API_KEY = "Your Key"
                print('lnkdata ========>  ', json.loads(lnk_data[2])['company']['company_domain'])
                company_domain = json.loads(lnk_data[2])['company']['company_domain']
                print('lnkdata ========>  ', lnk_data)
                print('lnk_results jobs ==> ', lnk_results[0].profile.jobs[0])

                lush = LushaAPI(LUSHA_API_KEY)
                name = lnk_data[0].split('\n')[0]
                name = name.rstrip('  ').lstrip(' ')
                first_name = name.split(' ')[0]
                last_name = None
                if len(name) > 1:
                    last_name = name.split(' ')[1]
                last_name = last_name.strip(',')

                print('lnk_results ==> ', lnk_results[0].profile.email)
                try:
                    location = lnk_data[0].split('\n')[4]
                except:
                    location = lnk_data[0].split('\n')[2]
                    # if 'Contact info' in location:
                #    location = location.strip('Contact info').rstrip(' ')

                location = location.split('Contact info')[0].rstrip(' ')

                email = lnk_data[1]
                current_job = json.loads(lnk_data[2])
                last_job = json.loads(lnk_data[3])
                company = current_job['company']['name']
                last_company = last_job['company']['name']

                comp_ex = CompanyExceptions(first_name=first_name, last_name=last_name, company=company,
                                            company_domain=company_domain, last_company=last_company)

                comp_ex.try_company()

                if comp_ex.company is not None:
                    company = comp_ex.company

                # first_name = lnk_results[i].profile.name.split('\n')[0]
                # Last_name = lnk_results[i].profile.name.split('\n')[1]

                print('First_name: ', first_name)
                print('Last_name: ', last_name)
                print('company', company)

                phone = None
                try:
                    '''company_temp = lush.company(company=company)['data']['name']
                    if company_temp != '':
                        company = company_temp
                    print('company_temp ==> ', company_temp)

                    company = lush.company(company=company)['data']['name']'''
                    print('New company_name ==> ', company)
                    response_person = lush.person(first_name=first_name, last_name=last_name, company=company)
                    print('response_person ==> ', response_person)
                    response_person_phone = lush.person(first_name=first_name, last_name=last_name, company=company,
                                                        property='phoneNumbers')
                    response_person_email = lush.person(first_name=first_name, last_name=last_name, company=company,
                                                        property='emailAddresses')

                    df = pd.DataFrame(df)

                    # when lusha_api doesn't work, we use phone and email from linkedin
                    print('email ***===> ', email)
                    phone_temp = response_person_phone['data']['phoneNumbers'][0]['internationalNumber']
                    email_temp = response_person_email['data']['emailAddresses'][0]['email']
                    if email == '' or email is None:
                        print('não veio email do linkedin')
                        phone = phone_temp
                        email = email_temp
                except Exception as e:
                    print('It was not possible to find data on Lusha API')

                df.iloc[i, 2] = first_name
                df.iloc[i, 3] = last_name
                df.iloc[i, 4] = company
                df.iloc[i, 5] = location
                df.iloc[i, 7] = email
                df.iloc[i, 8] = phone

            else:
                print(f'It was not possible to scrap data from linkedin for {lnk_link}')

    return df
