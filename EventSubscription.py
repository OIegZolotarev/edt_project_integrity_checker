
import xml.etree.ElementTree as ET
from edt_project import ProjectContext

class EventSubscirpiton:
    def __init__(self, objectName: str, edtProject: ProjectContext):
        
        self.project = edtProject

        mdoPath = '{1}src/EventSubscriptions/{0}/{0}.mdo'.format(objectName, edtProject.directory)
        self.mdoFile = mdoPath


    def validate(self) -> bool:

        mdoData = ET.parse(self.mdoFile)

        root = mdoData.getroot();

        source = root.find("source")

        

        if source != None:

            badNodes = []

            for item in source:
                
                itemData = item.text.split(".")

                # Подписка на суперкласс - к СправочникОбъект, ДокументОбъект и т.п.
                if (len(itemData) == 1):
                    continue    

                itemName = itemData[1]
                itemClass = ProjectContext.convertDerivedClassToBasic(itemData[0])

                if self.project.contains(itemClass, itemName) == False:
                    print("Неизвестный элемент в источниках подписки на событие: " + item.text)
                    badNodes.append(item)

            for node in badNodes:

                source.remove(node)                    


        mdoData.write(self.mdoFile)

        pass

        
        
        