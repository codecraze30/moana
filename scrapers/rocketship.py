import requests
import json
import csv
from utils.google_sheets import get_or_create_worksheet, save_to_google_sheet

def scrape_remoterocketship(tab_name):
    # URL and headers for the request
    job_function = "Software+Engineer"
    job_location = "United+States"
    limit = 200
    # url = f"https://qqgpkxvjliaqeipxsgco.supabase.co/rest/v1/jobOpening?select=id%2Ccreated_at%2CvalidUntilDate%2CdateDeleted%2CroleTitle%2CjobDescriptionSummary%2CtwoLineJobDescriptionSummary%2CeducationRequirementsCredentialCategory%2Curl%2CseniorityRange%2CsalaryRange%2CtechStack%2Cslug%2CisPromoted%2CemploymentType%2Clocation%2ClocationHumanReadableText%2CcategorizedJobTitle%2CcategorizedJobFunction%2Ccompany%21inner%28id%2Cname%2Cslug%2CprofilePicURL%2ChomePageURL%2ClinkedInURL%2CemployeeRange%2CfundingData%2CsponsorsH1B%2CsponsorsUKSkilledWorkerVisa%29&locationType=eq.remote&dateDeleted=is.null&order=created_at.desc.nullslast&or=%28categorizedJobFunction.in.%28{job_function}%29%29&or=%28location.in.%28{job_location}%2CWorldwide%29%2ClocationRegion.in.%28%29%29&limit={limit}&offset=0"
    url = f"https://qqgpkxvjliaqeipxsgco.supabase.co/rest/v1/jobOpening?select=id%2Ccreated_at%2CvalidUntilDate%2CdateDeleted%2CroleTitle%2CjobDescriptionSummary%2CtwoLineJobDescriptionSummary%2CeducationRequirementsCredentialCategory%2Curl%2CisEntryLevel%2CisJunior%2CisMidLevel%2CisSenior%2CisLead%2CsalaryRange%2CtechStack%2Cslug%2CisPromoted%2CemploymentType%2Clocation%2ClocationHumanReadableText%2ClocationUSStates%2CcategorizedJobTitle%2CcategorizedJobFunction%2Ccompany%21inner%28id%2Cname%2Cslug%2CprofilePicURL%2ChomePageURL%2CchatGPTIndustries%2ClinkedInURL%2CemployeeRange%2CfundingData%2CsponsorsH1B%2CindustrySpecialities%2CfoundedYear%2CsponsorsUKSkilledWorkerVisa%29&dateDeleted=is.null&order=created_at.desc.nullslast&categorizedJobTitle=in.%28{job_function}%29&location=in.%28{job_location}%2CWorldwide%2CNorth+America%29&limit={limit}&offset=0"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "accept-profile": "public",
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFxZ3BreHZqbGlhcWVpcHhzZ2NvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQ2NjE5NTgsImV4cCI6MjAzMDIzNzk1OH0.Bpuq94xi4pzldTsgTQhtiUoJ2xjJWJjmXPeOpVJXrhI",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFxZ3BreHZqbGlhcWVpcHhzZ2NvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQ2NjE5NTgsImV4cCI6MjAzMDIzNzk1OH0.Bpuq94xi4pzldTsgTQhtiUoJ2xjJWJjmXPeOpVJXrhI",
        "prefer": "count=exact",
        "priority": "u=1, i",
        "sec-ch-ua": '\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '\"Windows\"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "x-client-info": "@supabase/auth-helpers-nextjs@0.9.0"
    }

    try:
        # Make the GET request
        response = requests.get(url, headers=headers)

        # Check if the response is OK
        response.raise_for_status()

        data = response.json()

        # Transform data for Google Sheets
        transformed_data = []
        for job in data:
            transformed_data.append({
                'title': job.get('roleTitle', 'Not Specified'),
                'company': job.get('company', {}).get('name', 'Not Specified'),
                'pay': job.get('salaryRange', {}).get('salaryHumanReadableText', 'Not Specified') if job.get('salaryRange') else 'Not Specified',
                'job_type': job.get('employmentType', 'Not Specified'),
                'work_setting': job.get('locationHumanReadableText', 'Not Specified'),
                'url': job.get('url', 'Not Specified')
            })

        # Save to Google Sheets
        worksheet = get_or_create_worksheet(tab_name)
        save_to_google_sheet(worksheet, transformed_data)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")