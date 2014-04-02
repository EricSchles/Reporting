import lxml.html
import requests
import csv
#for testing - 'https://www.law.umich.edu/clinical/HuTrafficCases/Pages/CaseDisp.aspx?caseID=464'
#http://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words - the general idea
#grabbing all the # links
def linkGrab():
    url = "https://www.law.umich.edu/clinical/HuTrafficCases/Pages/searchdatabase.aspx"
    res = requests.get(url)
    html = res.text
    to_lxml =lxml.html.fromstring(html)
    tags = to_lxml.xpath('//tr[@class="ms-alternating"]/td/a')
    links = []

    for i in tags:
        links.append("https://www.law.umich.edu/clinical/HuTrafficCases/Pages/"+str(i.attrib['href']))

    return links
def informationGrab(links):
    
    with open("caseFiles.csv","w") as caseFiles:

        writer = csv.writer(caseFiles,quoting=csv.QUOTE_MINIMAL)
        fields = [
            "CASE NAME:",
            "ALL PLAINTIFFS:",
            "ALL DEFENDANTS:", 
            "CITATION:",
            "DOCKET NUMBER:",
            "SOURCE:",
            "TYPE OF CASE:",
            "RELATED CASE CITATION:",
            "TYPE OF TRIAL",
            "TRIAL JUDGE(S):",
            "YEAR OF ARREST",
            "YEAR OF VERDICT", 
            "TYPE OF COURT:",
            "STATE:",
            "FEDERAL DISTRICT:",
            "STATE COUNTY:",
            "AGE OF VICTIM(S):",
            "NUMBER OF VICTIMS:",
            "GENDER OF VICTIM(S):",
            "VICTIM'S COUNTRY OF ORIGIN:",
            "METHOD OF ENTRY INTO THE U.S.:",
            "WAS VICTIM CHARGED WITH A CRIME:",
            "NUMBER OF DEFENDANT(S):",
            "GENDER OF DEFENDANT(S):",
            "TYPE OF INDUSTRY:",
            "CASE CATEGORIZATION:",
            "FIRST CHARGE:",
            "FIRST CHARGE  US/STATE CODE CITATION:",
            "FIRST CHARGE VERDICT/PLEA:",
            "FIRST CHARGE SENTENCE:",
            "SECOND CHARGE:",
            "SECOND CHARGE US/STATE CODE CITATION:",
            "SECOND CHARGE VERDICT/PLEA:",
            "SECOND CHARGE SENTENCE:",
            "THIRD CHARGE:",
            "THIRD CHARGE US/STATE CODE CITATION:",
            "THIRD CHARGE VERDICT/PLEA",
            "THIRD CHARGE SENTENCE:",
            "FOURTH CHARGE:",
            "FOURTH CHARGE US/STATE CODE CITATION:",
            "FOURTH CHARGE VERDICT/PLEA:",
            "FOURTH CHARGE SENTENCE:",
            "FIFTH CHARGE:",
            "FIFTH CHARGE US/STATE CODE CITATION:",
            "FIFTH CHARGE VERDICT/PLEA",
            "FIFTH CHARGE SENTENCE:",
            "CORE TERMS:",
            "SENTENCING OPINION CITATION:",
            "LENGTH OF GREATEST SENTENCE:",
            "RESTITUTION REQUIRED:",
            "FINE IMPOSED:",
            "FORFEITURE IMPOSED:",
            "FIRST CLAIM:",
            "FIRST CLAIM US/STATE CODE CITATION:",
            "FIRST CLAIM RESULT:",
            "DAMAGES AWARDED FOR FIRST CLAIM:",
            "SECOND CLAIM:",
            "SECOND CLAIM US/STATE CODE CITATION:",
            "SECOND CLAIM RESULT:",
            "DAMAGES AWARDED FOR SECOND CLAIM:",
            "THIRD CLAIM:",
            "THIRD CLAIM US/STATE CODE CITATION:",
            "THIRD CLAIM RESULT:",
            "DAMAGES AWARDED FOR THIRD CLAIM:",
            "FOURTH CLAIM:",
            "FOURTH CLAIM US/STATE CODE CITATION:",
            "FOURTH CLAIM RESULT:",
            "DAMAGES AWARDED FOR FOURTH CLAIM:",
            "FIFTH CLAIM:",
            "FIFTH CLAIM US/STATE CODE CITATION:",
            "FIFTH CLAIM RESULT:",
            "DAMAGES AWARDED FOR FIFTH CLAIM:",
            "SIXTH CLAIM:",
            "SIXTH CLAIM US/STATE CODE CITATION:",
            "SIXTH CLAIM RESULT:",
            "DAMAGES AWARDED FOR SIXTH CLAIM:",
            "TOTAL AWARD:",
            "APPEAL:",
            "EXPLANATION OF APPEAL:",
            "APPELLATE OPINION CITATION:",
            "HOLDING OF APPEALS COURT:",
            "APPEAL STILL PENDING?:",
            "SUMMARY:"]

        writer.writerow(fields)

        for link in links:
            res = requests.get(link)
            html = res.text
            to_lxml = lxml.html.fromstring(html)
            info = to_lxml.xpath('//table[@id="datatablehiderowsID0EAAA"]')
           
            raw_text = info[0].text_content().encode("ascii","ignore")
            case_name = raw_text.split("ALL PLAINTIFFS:")[0].replace("CASE NAME:","")
            all_plaintiffs = raw_text.split("ALL DEFENDANTS:")[0].split("ALL PLAINTIFFS:")[1]
            all_defendants = raw_text.split("CITATION:")[0].split("ALL DEFENDANTS:")[1]
            
            case_array = []
            case_array.append(case_name)
            i = 1
            while i < len(fields)-1:

                case_array.append(raw_text.split(fields[i+1])[0].split(fields[i])[1])
                i += 1
            
            case_array.append(raw_text.split("SUMMARY:")[1])
            writer.writerow(case_array)
            



if __name__ == '__main__':        
    links = linkGrab()
    # for testing - links = ["https://www.law.umich.edu/clinical/HuTrafficCases/Pages/CaseDisp.aspx?caseID=464"]
    informationGrab(links)
