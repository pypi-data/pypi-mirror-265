from googleapiclient.discovery import build
from google.oauth2 import service_account

class GoogleSheet:

    CREDS           = None
    SERVICE         = None
    SHEET           = None
    FORMAT          = None
    FORMAT_DEFAULT  = "JSON"
    SCOPE           = ["https://www.googleapis.com/auth/spreadsheets"]

    def __init__(self, key: str = "", format = FORMAT_DEFAULT):
        """
            Creates a GoogleSheet instance.
            
            Args:
                key (str)           : The path to the service account json file.
        """
        try:
            self.CREDS          = service_account.Credentials.from_service_account_file(key, scopes=self.SCOPE)
            self.SERVICE        = build("sheets", "v4", credentials=self.CREDS)
            self.SHEET          = self.SERVICE.spreadsheets()
            self.FORMAT         = format.upper()
        except Exception as e:
            print({
                "error"     : True,
                "response"  : str(e)
            })
            exit(1)

    def get(self, spreadsheetId: str = "", range: str = "", filter: str = None) -> dict:
        """
            Get the data from the sheet.
            
            Args:
                spreadsheetId (str) : Id google sheet.
                range (str)         : Column or row range.
                filter (str)        : filter by str.

            Returns:
                dict                : return list
        """
        try:
            
            if filter != None:
                self.SHEET_NAME = "FILTER"
                auxRange        = range.split(":")
                range           = "B1"
                self.update(filter)
                range           = f"{auxRange[0]}2:{auxRange[1]}"

            result              = self.SHEET.values().get(
                spreadsheetId   = spreadsheetId, 
                range           = range
            ).execute()

            auxReturn           = result["values"]

            if(self.FORMAT == self.FORMAT_DEFAULT):

                auxReturn           = []

                for element in result["values"][1:]:
                    obj             = {}
                    lenList         = len(element)
                    for index, item in enumerate(result["values"][0]):
                        obj[item]   = element[index] if lenList > index else ""
                    
                    auxReturn.append(obj)

            return auxReturn
        except Exception as e:
            return {
                "error"     : True,
                "response"  : str(e)
            }

    def add(self, spreadsheetId: str = "", range: str = "", data: dict = {}) -> dict:
        """
            Add data to the sheet.
            
            Args:
                spreadsheetId (str) : Id google sheet.
                range (str)         : Column or row range.
                data (dict)         : array data.

            Returns:
                dict                : return response of the sheet
        """
        try:
            return self.SHEET.values().append(
                spreadsheetId    = spreadsheetId, 
                range            = range, 
                valueInputOption = "USER_ENTERED", 
                body             = {"values": data}
            ).execute()
        except Exception as e:
            return {
                "error"     : True,
                "response"  : str(e)
            }

    def update(self, spreadsheetId: str = "", range: str = "", data: dict = {}) -> dict:
        """
            Update data to the sheet.
            
            Args:
                spreadsheetId (str) : Id google sheet.
                range (str)         : Column or row range.
                data (dict)         : array data.

            Returns:
                dict                : return response of the sheet
        """
        try:
            return self.SHEET.values().update(
                spreadsheetId    = spreadsheetId, 
                range            = range, 
                valueInputOption = "USER_ENTERED", 
                body             = {"values": data}
            ).execute()
        except Exception as e:
            return {
                "error"     : True,
                "response"  : str(e)
            }

    def delete(self, spreadsheetId: str = "", idSheet: str = "", range: str = "") -> dict:
        """
            Delete data to the sheet.
            
            Args:
                spreadsheetId (str) : Id sheet.
                range (str)         : Column or row range.
                idSheet (dict)      : id sheet.

            Returns:
                dict                : return response of the sheet
        """
        try:
            auxRange                = range.split(":")
            return self.SHEET.batchUpdate(
                spreadsheetId       = spreadsheetId, 
                body                = {
                    "requests"      : [
                        {
                            "deleteDimension": {
                                "range": {
                                    "sheetId"    : idSheet,
                                    "dimension"  : "ROWS",
                                    "startIndex" : auxRange[0],
                                    "endIndex"   : auxRange[1]
                                }
                            }
                        }
                    ]
                }
            ).execute()
        except Exception as e:
            return {
                "error"     : True,
                "response"  : str(e)
            }

    def info(self) -> object:
        """
            Get sheet info.

            Returns:
                object              : return sheet info
        """
        return self.SHEET.sheets()