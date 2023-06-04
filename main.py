from rop_src.architecture.architecture import ARM
from rop_src.services.file_service import FileService
from rop_src.services.gadget_service import GadgetService
from src.startUI import StartUIApplication

if __name__ == '__main__':
    StartUIApplication(ARM.NAME)
