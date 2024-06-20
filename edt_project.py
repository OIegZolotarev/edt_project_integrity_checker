import os
import xml.etree.ElementTree as ET
from alive_progress import alive_bar

class InvalidProjectPathError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ProjectContext:
    
    def _isMetadataTag(tag: str):
        acceptableTags = ["subsystems",
            "styleItems",
            "commonPictures",
            #"interfaces",
            "sessionParameters",
            "roles",
            "commonTemplates",
            "filterCriteria",
            "commonModules",
            "commonAttributes",
            "exchangePlans",
            "XDTOPackages",
            "webServices",
            "httpServices",
            "wsReferences",
            "eventSubscriptions",
            "scheduledJobs",
            "settingsStorages",
            "functionalOptions",
            "functionalOptionsParameters",
            "definedTypes",
            "commonCommands",
            "commandGroups",
            "constants",
            "commonForms",
            "catalogs",
            "documents",
            "documentNumerators",
            "documentJournals",
            "enums",
            "reports",
            "dataProcessors",
            "informationRegisters",
            "accumulationRegisters",
            "chartsOfCharacteristicTypes",
            "chartsOfAccounts",
            "accountingRegisters",
            "chartsOfCalculationTypes",
            "calculationRegisters",
            "businessProcesses",
            "tasks"]
        
        return tag in acceptableTags
            


    def __init__(self, directory: str) -> None:
        self.directory = directory
        
        configurationDescriptorPath = self.directory + "/src/Configuration/Configuration.mdo"

        if not os.path.exists(configurationDescriptorPath):
            raise (InvalidProjectPathError)
        
        tree = ET.parse(configurationDescriptorPath)
        configurationDescriptor = tree.getroot()

        self.objects = {}

        with alive_bar(len(configurationDescriptor), dual_line=True, title='Парсим configuration.mdo') as bar:        
            for item in configurationDescriptor:

                if ProjectContext._isMetadataTag(item.tag) == False:
                    bar()
                    continue
                    
                objectName = item.text.split(".")[1]
                itemSuperClass = item.text.split(".")[0]

                if not itemSuperClass in self.objects:
                    self.objects[itemSuperClass] = []
                
                self.objects[itemSuperClass].append(objectName)
                bar()

    def getClassDirectory(self, objectClass:str) -> str:
        
        pluralForms = {
                        "AccountingRegister" : "AccountingRegisters",
                        "AccumulationRegister" : "AccumulationRegisters",
                        "BusinessProcess" : "BusinessProcesses",
                        "CalculationRegister" : "CalculationRegisters",
                        "Catalog" : "Catalogs",
                        "ChartOfAccounts" : "ChartsOfAccounts",
                        "ChartOfCalculationTypes" : "ChartsOfCalculationTypes",
                        "ChartOfCharacteristicTypes" : "ChartsOfCharacteristicTypes",
                        "CommandGroup" : "CommandGroups",
                        "CommonAttribute" : "CommonAttributes",
                        "CommonCommand" : "CommonCommands",
                        "CommonForm" : "CommonForms",
                        "CommonModule" : "CommonModules",
                        "CommonPicture" : "CommonPictures",
                        "CommonTemplate" : "CommonTemplates",
                        "Configuration" : "Configuration",
                        "Constant" : "Constants",
                        "DataProcessor" : "DataProcessors",
                        "DefinedType" : "DefinedTypes",
                        "DocumentJournal" : "DocumentJournals",
                        "DocumentNumerator" : "DocumentNumerators",
                        "Document" : "Documents",
                        "Enum" : "Enums",
                        "EventSubscription" : "EventSubscriptions",
                        "ExchangePlan" : "ExchangePlans",
                        "FilterCriterion" : "FilterCriteria",
                        "FunctionalOption" : "FunctionalOptions",
                        "FunctionalOptionsParameter" : "FunctionalOptionsParameters",
                        "HTTPService" : "HTTPServices",
                        "InformationRegister" : "InformationRegisters",
                        "Report" : "Reports",
                        "Role" : "Roles",
                        "ScheduledJob" : "ScheduledJobs",
                        "SessionParameter" : "SessionParameters",
                        "SettingsStorage" : "SettingsStorages",
                        "StyleItem" : "StyleItems",
                        "Subsystem" : "Subsystems",
                        "Task" : "Tasks",
                        "WebService" : "WebServices",
                        "WSReference" : "WSReferences",
                        "XDTOPackage" : "XDTOPackages",
        }
        
        objectDir = pluralForms[objectClass]

        return self.directory + "src/" + objectDir
    
    def contains(self, objectclass: str, item: str) -> bool:

        return item in self.objects[objectclass]
