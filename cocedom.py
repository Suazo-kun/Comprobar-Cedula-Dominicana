import bs4, copy, json, requests

URL = "https://dgii.gov.do/app/WebApps/ConsultasWeb/consultas/ciudadanos.aspx"
URL2 = "https://servicios.mirex.gob.do/proxy/api/padron"
URL3 = "https://api-ov.intrant.gob.do/api/User/ValidaCedula"

FORM_DATA = {
    'ctl00$smMain': "ctl00$cphMain$upBusqueda|ctl00$cphMain$btnBuscarCedula",
    'ctl00$cphMain$txtCedula': "",
    '__EVENTTARGET': "",
    '__EVENTARGUMENT': "",
    '__VIEWSTATE':
    "/wEPDwUKLTE4NTE1MjQ5MQ9kFgJmD2QWAgIBD2QWAgIDD2QWAmYPZBYCAgEPZBYCAgMPFgIeB1Zpc2libGVnFgICAw9kFgICAQ88KwAPAgAPFgQeC18hRGF0YUJvdW5kZx4LXyFJdGVtQ291bnQCAWQKEBYBAgMWATwrAAUBABYCHgpIZWFkZXJUZXh0BQ1STkMgbyBDw6lkdWxhFgFmFgJmD2QWDmYPDxYCHwBoZGQCAQ9kFgICAQ8PFgIeBFRleHQFEkpVQU4gU0VQVElNTyBCUkFORGRkAgIPZBYCAgEPDxYCHwQFBkFDVElWT2RkAgMPZBYCAgEPZBYCZg8VAQZGSVNJQ09kAgQPZBYCAgEPDxYCHwQFDTAwMS0wNjEyOTgwLTJkZAIFD2QWAgIBDw8WAh8EBQYmbmJzcDtkZAIGDw8WAh8AaGRkGAEFH2N0bDAwJGNwaE1haW4kZHZSZXN1bHRhZG9DZWR1bGEPFCsAB2RkZGRkFgACAWShJq3yIsgxSd/0RcA8vrgIHf7l4A==",
    '__EVENTVALIDATION':
    "/wEWAwLezuDWDAKpmY77CQLhjvSgAeuiGz2lxzTWaW6TDe4/7GkwVEta",
    '__ASYNCPOST': True,
    'ctl00$cphMain$btnBuscarCedula': "Buscar"
}

def ComprobarCedula1(cedula: str):
    cedula = cedula.replace("-", "")

    if len(cedula) != 11:
        raise ValueError("Cédula invalida.")

    out = {'nombre': "", 'cedula': ""}
    form_data = copy.copy(FORM_DATA)
    form_data['ctl00$cphMain$txtCedula'] = cedula

    response = requests.post(URL, data=form_data)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    soup = soup.find("table")

    if soup is None:
        return out

    for element in soup.findAll("tr"):
        if "nombre" in element.text.lower():
            out['nombre'] = element.findAll("td")[-1].text
        elif "rnc" in element.text.lower():
            out['cedula'] = element.findAll("td")[-1].text

    return out

def ComprobarCedula2(cedula: str):
    out = {'nombre': "", 'cedula': ""}

    cedula = cedula.replace("-", "")

    if len(cedula) != 11:
        raise ValueError("Cédula invalida.")

    response = requests.get(f"{URL2}/{cedula}")
    data = json.loads(response.text)['result']

    out['nombre'] = " ".join((data['nombres'], data['apellido1'], data['apellido2']))
    out['cedula'] = "-".join((cedula[0:3], cedula[3:10], cedula[-1]))

    return out

def ComprobarCedula3(cedula: str):
    out = {'nombre': "", 'cedula': ""}

    cedula = cedula.replace("-", "")
    cedula = "-".join((cedula[0:3], cedula[3:10], cedula[-1]))

    if len(cedula) != 13:
        raise ValueError("Cédula invalida.")

    cedula = cedula.split("-")
    data = {"ID1": cedula[0], "ID2": cedula[1], "ID3": cedula[2]}
    response = requests.post(URL3, json=data)
    data = json.loads(response.text)

    if data['Nombre'] is None:
        return out

    out['nombre'] = " ".join((data['Nombre'], data['Apellidos']))
    out['cedula'] = "-".join(cedula)
    return out

def ComprobarCedula(cedula: str):
    for function in (ComprobarCedula1, ComprobarCedula2, ComprobarCedula3):

        try: out = function(cedula)
        except Exception: continue

        if out['nombre'] != "":
            return out

    return {'nombre': "", 'cedula': ""}
